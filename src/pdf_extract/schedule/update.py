"""The update-mode process stage: each new bulletin read against the believed schedule.

For every parish in update mode (one with a seed revision), each bulletin
fetched after its latest seed's `as_of` with no successful call yet is, in
fetch order:

1. rendered against: the parish's believed schedule as a canonical view;
2. called: the policy prompt, the church list, the date, the view and the PDF.
   The raw reply is stored in the blob store under `llm/calls/<request_key>.json`
   as soon as it arrives, and a failed call is stored in `llm_call` at once;
3. decided and applied, in one transaction: the `llm_call` row, its proposals
   with their decisions, the sightings, the revision with its log rows and the
   fold into `current_schedule`, and the bulletin's `published_date`,
   `wrong_bulletin` and `processed_at`.

A crash before step 3 commits leaves only the stored reply, which the next run
finds by its request key and decides without calling the API again. Calls run
in parallel across parishes and one at a time within a parish, since each reads
the schedule the one before it left. The database is only touched from the
calling thread; the worker threads only make API calls.

See docs/schedule-state-plan.md, "How a bulletin is processed (update mode)".
"""

from __future__ import annotations

import json
import logging
import sqlite3
from collections import deque
from collections.abc import Collection
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from pdf_extract.blobstore import get_store
from pdf_extract.classifiers.schedule_update import (
    API_ERROR,
    CONTEXT_TEMPLATE,
    CONTEXT_TEMPLATE_HASH,
    PARSE_FAILED,
    POLICY,
    POLICY_HASH,
    SCHEMA_HASH,
    SCHEMA_TEXT,
    TASK,
    OpenAIScheduleUpdater,
    ParsedReply,
    RawReply,
    parse_response,
    render_context,
)
from pdf_extract.evals.pricing import call_cost
from pdf_extract.runs import (
    PROCESS_CORRECTION,
    PROCESS_FAILED,
    PROCESS_GAVE_UP,
    PROCESS_MASS_DELETE,
    PROCESS_NO_CHANGE,
    PROCESS_REPEATED_WEEK,
    PROCESS_SKIPPED,
    PROCESS_STALE,
    PROCESS_UNDATED,
    PROCESS_UPDATED,
    PROCESS_WRONG_BULLETIN,
    join_details,
    record_parish_result,
)
from pdf_extract.schedule.history import SUCCEEDED, call_week, parish_history, place_call
from pdf_extract.schedule.policy import (
    APPLIED,
    DECIDED_BY,
    MASS_DELETE,
    STALE_BULLETIN,
    WRONG_BULLETIN,
    Proposal,
    decide,
    whole_call_reason,
)
from pdf_extract.schedule.store import (
    LLM,
    Change,
    append_revision,
    canonical_json,
    current_revision,
    intern_entry,
    live_entries,
    parish_churches,
    render_view,
    replace_sightings,
    retire_ended,
    sha256_text,
    store_prompt_blob,
    store_view,
    update_mode_parishes,
)
from pdf_extract.storage import church_list_for_prompt, read_bulletin_pdf, utc_now_iso

LOGGER = logging.getLogger(__name__)

# A bulletin whose call has failed this many times is no longer retried.
MAX_FAILED_CALLS = 3

CALL_RECORD_PREFIX = "llm/calls/"


def call_record_key(request_key: str) -> str:
    return f"{CALL_RECORD_PREFIX}{request_key}.json"


class BaseRevisionMismatch(RuntimeError):
    """The schedule no longer renders to the view a call was shown: a bug, not a disagreement."""


# ── Which bulletins ─────────────────────────────────────────────────────────
def _failed_calls_sql() -> str:
    return (
        "SELECT COUNT(*) FROM llm_call f WHERE f.bulletin_id = b.id"
        " AND f.status NOT IN ('ok', 'lenient')"
    )


def pending_bulletins(
    conn: sqlite3.Connection, as_of: dict[int, str],
) -> tuple[dict[int, list[dict[str, Any]]], list[dict[str, Any]]]:
    """Per parish, the bulletins to call, in fetch order; and the ones given up on.

    A bulletin is called when it was fetched after the parish's latest seed's
    `as_of` and neither it nor another bulletin of the parish with the same PDF
    has a successful call. One whose call has failed `MAX_FAILED_CALLS` times
    is given up on instead.
    """
    pending: dict[int, list[dict[str, Any]]] = {}
    gave_up: list[dict[str, Any]] = []
    for parish_id, seed_as_of in as_of.items():
        rows = conn.execute(
            f"""SELECT b.id, b.parish_id, p.slug AS parish_slug, b.source_url, b.content_hash,
                       b.fetched_at, ({_failed_calls_sql()}) AS failed_calls
                FROM bulletin b JOIN parish p ON p.id = b.parish_id
                WHERE b.parish_id = ? AND b.fetched_at > ?
                  AND NOT EXISTS (
                      SELECT 1 FROM llm_call c JOIN bulletin b2 ON b2.id = c.bulletin_id
                      WHERE c.status IN ('ok', 'lenient') AND b2.parish_id = b.parish_id
                        AND (b2.id = b.id OR b2.content_hash = b.content_hash)
                  )
                ORDER BY b.fetched_at, b.id""",
            (parish_id, seed_as_of),
        ).fetchall()
        for row in rows:
            item = dict(row)
            if item["failed_calls"] >= MAX_FAILED_CALLS:
                gave_up.append(item)
            else:
                pending.setdefault(parish_id, []).append(item)
    return pending, gave_up


# ── One call ────────────────────────────────────────────────────────────────
@dataclass
class Prepared:
    """One bulletin ready to call: everything the request is made of."""

    bulletin: dict[str, Any]
    as_of: str
    pdf_bytes: bytes
    context: str
    call_date: date
    view_text: str
    view_hash: str
    base_revision: int
    church_list_hash: str
    request_key: str
    started_at: str = field(default_factory=utc_now_iso)


def _call_date(bulletin: dict[str, Any]) -> date:
    """The bulletin's fetch date: "today" for the model, so a replay asks the same question."""
    fetched = str(bulletin.get("fetched_at") or "")[:10]
    try:
        return date.fromisoformat(fetched)
    except ValueError:
        return date.today()


def request_key(
    version: str, content_hash: str, view_hash: str, call_date: date, church_list_hash: str,
) -> str:
    return sha256_text("\x00".join(
        (version, content_hash, view_hash, call_date.isoformat(), church_list_hash)
    ))


def prepare(
    conn: sqlite3.Connection,
    bulletin: dict[str, Any],
    as_of: str,
    updater: OpenAIScheduleUpdater,
) -> Prepared | None:
    """Render the view and build the request; None when the PDF can't be loaded."""
    content_hash = bulletin.get("content_hash")
    if not isinstance(content_hash, str) or not content_hash:
        return None
    pdf_bytes = read_bulletin_pdf(bulletin["parish_slug"], content_hash)
    if pdf_bytes is None:
        return None
    parish_id = bulletin["parish_id"]
    call_date = _call_date(bulletin)
    view_text, view_hash = render_view(conn, parish_id, call_date)
    churches = church_list_for_prompt(conn, parish_id)
    church_list_hash = sha256_text(canonical_json(churches))
    return Prepared(
        bulletin=bulletin,
        as_of=as_of,
        pdf_bytes=pdf_bytes,
        context=render_context(churches, call_date, view_text),
        call_date=call_date,
        view_text=view_text,
        view_hash=view_hash,
        base_revision=current_revision(conn, parish_id),
        church_list_hash=church_list_hash,
        request_key=request_key(
            updater.version, content_hash, view_hash, call_date, church_list_hash,
        ),
    )


def load_call_record(key: str) -> dict[str, Any] | None:
    """A readable stored reply for this request key, if a run (here or elsewhere) made it."""
    try:
        data = get_store().get(call_record_key(key))
    except Exception:
        LOGGER.warning("Reading the stored reply for %s failed", key, exc_info=True)
        return None
    if data is None:
        return None
    try:
        record = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        LOGGER.warning("Discarding unreadable stored reply %s", key)
        return None
    if not isinstance(record, dict) or record.get("request_key") != key:
        return None
    # A reply that couldn't be read is kept for debugging, but a retry asks again.
    if parse_response(record.get("response_text") or "").status == PARSE_FAILED:
        return None
    return record


def store_call_record(prepared: Prepared, updater: OpenAIScheduleUpdater, reply: RawReply) -> dict:
    """Store the raw request and reply. Best effort: a failed write costs a future call."""
    record = {
        "request_key": prepared.request_key,
        "task": TASK,
        "provider": updater.provider,
        "model": updater.model,
        "served_model": reply.served_model,
        "service_tier": reply.service_tier,
        "params": updater.params,
        "version": updater.version,
        "policy_hash": POLICY_HASH,
        "schema_hash": SCHEMA_HASH,
        "context_template_hash": CONTEXT_TEMPLATE_HASH,
        "content_hash": prepared.bulletin["content_hash"],
        "call_date": prepared.call_date.isoformat(),
        "view_hash": prepared.view_hash,
        "church_list_hash": prepared.church_list_hash,
        "context": prepared.context,
        "response_text": reply.text,
        "usage": reply.usage,
        "latency_ms": reply.latency_ms,
        "started_at": prepared.started_at,
        "finished_at": utc_now_iso(),
    }
    data = (json.dumps(record, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    try:
        get_store().put(
            call_record_key(prepared.request_key), data, content_type="application/json",
        )
    except Exception:
        LOGGER.warning("Could not store the reply for %s", prepared.request_key, exc_info=True)
    return record


def _insert_call(
    conn: sqlite3.Connection,
    prepared: Prepared,
    updater: OpenAIScheduleUpdater,
    *,
    run_id: str | None,
    status: str,
    error: str | None = None,
    record: dict[str, Any] | None = None,
    parsed: ParsedReply | None = None,
) -> int:
    """Insert the call's `llm_call` row (with the blobs it points at). Returns its id."""
    store_prompt_blob(conn, "policy", POLICY)
    store_prompt_blob(conn, "schema", SCHEMA_TEXT)
    store_prompt_blob(conn, "context_template", CONTEXT_TEMPLATE)
    store_view(conn, prepared.view_text)
    usage = (record or {}).get("usage") or {}
    tier = (record or {}).get("service_tier")
    cost = call_cost(updater.model, usage, service_tier=tier) if usage else None
    cursor = conn.execute(
        """INSERT INTO llm_call (
               run_id, parish_id, bulletin_id, task, provider, model, served_model,
               policy_hash, schema_hash, context_template_hash, params_json, version,
               base_revision, view_hash, call_date, church_list_hash, request_key,
               status, error, response_key, published_date, wrong_bulletin,
               church_list_needs_review, input_tokens, cached_input_tokens, output_tokens,
               thinking_tokens, cost_usd, latency_ms, started_at, finished_at, service_tier
           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                     ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            run_id, prepared.bulletin["parish_id"], prepared.bulletin["id"], TASK,
            updater.provider, updater.model, (record or {}).get("served_model"),
            POLICY_HASH, SCHEMA_HASH, CONTEXT_TEMPLATE_HASH, updater.params_json,
            updater.version, prepared.base_revision, prepared.view_hash,
            prepared.call_date.isoformat(), prepared.church_list_hash, prepared.request_key,
            status, error, call_record_key(prepared.request_key) if record else None,
            parsed.published_date if parsed else None,
            int(parsed.wrong_bulletin) if parsed else None,
            int(parsed.church_list_needs_review) if parsed else None,
            usage.get("prompt_tokens", usage.get("input_tokens")),
            usage.get("cached_tokens"),
            usage.get("output_tokens"),
            usage.get("thinking_tokens", usage.get("reasoning_tokens")),
            cost,
            (record or {}).get("latency_ms"),
            (record or {}).get("started_at") or prepared.started_at,
            (record or {}).get("finished_at") or utc_now_iso(),
            tier,
        ),
    )
    return int(cursor.lastrowid)


@dataclass
class CallOutcome:
    status: str
    detail: str | None = None
    applied: int = 0
    rejected: int = 0
    llm_call_id: int | None = None


def decide_and_apply(
    conn: sqlite3.Connection,
    prepared: Prepared,
    updater: OpenAIScheduleUpdater,
    record: dict[str, Any],
    parsed: ParsedReply,
    *,
    run_id: str | None,
) -> CallOutcome:
    """Steps 4 to 6 for one successful reply, in one transaction."""
    bulletin = prepared.bulletin
    parish_id = bulletin["parish_id"]
    with conn:
        view_text, view_hash = render_view(conn, parish_id, prepared.call_date)
        if view_hash != prepared.view_hash:
            raise BaseRevisionMismatch(
                f"parish {bulletin['parish_slug']}: the schedule no longer renders to the view "
                f"bulletin #{bulletin['id']}'s call was shown (revision {prepared.base_revision} "
                f"-> {current_revision(conn, parish_id)})"
            )

        history = parish_history(conn, parish_id)
        mark = history.mark
        week = call_week(parsed.published_date, bulletin.get("fetched_at"))
        stale, same_week_before = place_call(
            week=week, wrong_bulletin=parsed.wrong_bulletin, mark=mark,
            counted_weeks=history.counted_weeks,
        )

        call_id = _insert_call(
            conn, prepared, updater, run_id=run_id, status=parsed.status,
            record=record, parsed=parsed,
        )
        live = live_entries(conn, parish_id)
        retired = retire_ended(live, prepared.call_date)
        proposals = [
            Proposal(
                seq=c.seq, op=c.op, raw=c.raw,
                target_entry_id=c.entry_id if c.op != "add" else None,
                entry=c.entry if c.op != "delete" else None,
                page_number=c.page_number, rationale=c.rationale,
            )
            for c in parsed.changes
        ]
        whole = whole_call_reason(
            wrong_bulletin=parsed.wrong_bulletin, stale=stale, proposals=proposals, live=live,
        )
        decisions = decide(
            proposals, live=live, churches=parish_churches(conn, parish_id),
            today=prepared.call_date, whole_call=whole, targetable=set(_view_ids(view_text)),
        )

        # Proposals are stored in `seq` order; their changes are logged in the order they were
        # applied, so a deferred add or modify folds in after the removals it waited for.
        applied_changes: list[tuple[int, Change]] = []
        new_sightings: list[tuple[int, int | None]] = []
        for decision in decisions:
            proposal = decision.proposal
            entry_id = intern_entry(conn, decision.entry) if decision.entry else None
            cursor = conn.execute(
                """INSERT INTO proposed_change (
                       llm_call_id, seq, op, raw_json, target_entry_id, entry_id, page_number,
                       rationale, decision, reason, decided_by
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    call_id, proposal.seq, proposal.op, canonical_json(proposal.raw),
                    proposal.target_entry_id, entry_id, proposal.page_number,
                    proposal.rationale, decision.decision, decision.reason, DECIDED_BY,
                ),
            )
            if decision.decision != APPLIED:
                continue
            applied_changes.append((decision.order, Change(
                proposal.op,
                before_entry_id=proposal.target_entry_id,
                after_entry_id=entry_id,
                proposed_change_id=int(cursor.lastrowid),
            )))
            if entry_id is not None:
                new_sightings.append((entry_id, proposal.page_number))

        changes = [change for _, change in sorted(applied_changes, key=lambda item: item[0])]
        if changes:
            append_revision(
                conn, parish_id, source_kind=LLM, changes=retired + changes, llm_call_id=call_id,
                run_id=run_id,
            )
        if not parsed.wrong_bulletin and not stale:
            in_view = set(_view_ids(view_text))
            seen = [(entry_id, page) for entry_id, page in parsed.seen if entry_id in in_view]
            replace_sightings(conn, bulletin["id"], seen + new_sightings, llm_call_id=call_id)

        conn.execute(
            """UPDATE bulletin
               SET processed_at = ?, published_date = COALESCE(?, published_date),
                   wrong_bulletin = ?
               WHERE id = ?""",
            (utc_now_iso(), parsed.published_date, int(parsed.wrong_bulletin), bulletin["id"]),
        )

    applied = len(changes)
    rejected = len(decisions) - applied
    if whole is not None:
        status = {
            WRONG_BULLETIN: PROCESS_WRONG_BULLETIN,
            STALE_BULLETIN: PROCESS_STALE,
            MASS_DELETE: PROCESS_MASS_DELETE,
        }[whole]
    elif week is None:
        status = PROCESS_UNDATED
    elif same_week_before >= 2:
        status = PROCESS_REPEATED_WEEK
    elif same_week_before == 1:
        status = PROCESS_CORRECTION
    else:
        status = PROCESS_UPDATED if applied else PROCESS_NO_CHANGE
    detail = join_details(
        f"#{bulletin['id']}: {applied} applied, {rejected} rejected"
        + (f" ({whole})" if whole else ""),
        f"for {week.isoformat()}, older than {mark.isoformat()}" if stale and week and mark
        else None,
        "from the stored reply" if record.get("_reused") else None,
    )
    return CallOutcome(status, detail, applied, rejected, call_id)


def _view_ids(view_text: str) -> list[int]:
    view = json.loads(view_text)
    return [entry["id"] for church in view["churches"] for entry in church["entries"]]


def finish_call(
    conn: sqlite3.Connection,
    prepared: Prepared,
    updater: OpenAIScheduleUpdater,
    reply: RawReply | dict[str, Any] | BaseException,
    *,
    run_id: str | None,
) -> CallOutcome:
    """Store and decide one call's reply (a fresh one, a stored record, or the error)."""
    if isinstance(reply, BaseException):
        # Notes say what was tried first, such as the flex call before a standard one.
        error = "; ".join([f"{type(reply).__name__}: {reply}", *getattr(reply, "__notes__", ())])
        with conn:
            call_id = _insert_call(
                conn, prepared, updater, run_id=run_id, status=API_ERROR, error=error[:2000],
            )
        return CallOutcome(
            PROCESS_FAILED, f"#{prepared.bulletin['id']}: {type(reply).__name__}: {reply}",
            llm_call_id=call_id,
        )
    if isinstance(reply, RawReply):
        record = store_call_record(prepared, updater, reply)
    else:
        record = {**reply, "_reused": True}
    parsed = parse_response(record.get("response_text") or "")
    if parsed.status == PARSE_FAILED:
        with conn:
            call_id = _insert_call(
                conn, prepared, updater, run_id=run_id, status=PARSE_FAILED,
                error=parsed.error, record=record,
            )
        return CallOutcome(
            PROCESS_FAILED, f"#{prepared.bulletin['id']}: {parsed.error}", llm_call_id=call_id,
        )
    return decide_and_apply(conn, prepared, updater, record, parsed, run_id=run_id)


# ── The stage ───────────────────────────────────────────────────────────────
# When a parish has several outcomes in one run, the run records the most notable.
_PRECEDENCE = (
    PROCESS_FAILED, PROCESS_SKIPPED, PROCESS_MASS_DELETE, PROCESS_WRONG_BULLETIN, PROCESS_STALE,
    PROCESS_REPEATED_WEEK, PROCESS_UNDATED, PROCESS_CORRECTION, PROCESS_UPDATED,
    PROCESS_NO_CHANGE, PROCESS_GAVE_UP,
)


@dataclass
class ParishRun:
    parish_id: int
    slug: str
    as_of: str
    queue: deque[dict[str, Any]]
    outcomes: list[CallOutcome] = field(default_factory=list)
    last_source: dict[str, Any] | None = None


def process_update_mode(
    conn: sqlite3.Connection,
    *,
    slugs: Collection[str] | None = None,
    run_id: str | None = None,
    updater: OpenAIScheduleUpdater | None = None,
    concurrency: int = 5,
) -> dict[str, int]:
    """Call and decide every pending bulletin of the update-mode parishes in `slugs`."""
    updater = updater or OpenAIScheduleUpdater()
    as_of = update_mode_parishes(conn)
    slug_by_id = {
        row["id"]: row["slug"] for row in conn.execute("SELECT id, slug FROM parish").fetchall()
    }
    if slugs is not None:
        wanted = set(slugs)
        as_of = {pid: value for pid, value in as_of.items() if slug_by_id[pid] in wanted}
    pending, gave_up = pending_bulletins(conn, as_of)

    stats = {
        "update_parishes": len(as_of),
        "update_calls": 0,
        "update_reused_replies": 0,
        "update_failed_calls": 0,
        "update_skipped_bulletins": 0,
        "update_changes_applied": 0,
        "update_changes_rejected": 0,
        "update_gave_up": len(gave_up),
    }
    runs = {
        pid: ParishRun(pid, slug_by_id[pid], as_of[pid], deque(items))
        for pid, items in pending.items()
    }
    for item in gave_up:
        run = runs.setdefault(
            item["parish_id"],
            ParishRun(item["parish_id"], item["parish_slug"], as_of[item["parish_id"]], deque()),
        )
        run.outcomes.append(CallOutcome(
            PROCESS_GAVE_UP,
            f"#{item['id']}: its call failed in {item['failed_calls']} runs; no longer retried",
        ))

    def record(outcome: CallOutcome, parish: ParishRun) -> None:
        parish.outcomes.append(outcome)
        stats["update_changes_applied"] += outcome.applied
        stats["update_changes_rejected"] += outcome.rejected
        if outcome.status == PROCESS_FAILED:
            stats["update_failed_calls"] += 1

    def advance(parish: ParishRun) -> tuple[Future[RawReply], Prepared] | None:
        """Work through the parish's queue until a call has to go to the API."""
        while parish.queue:
            bulletin = parish.queue.popleft()
            parish.last_source = bulletin
            prepared = prepare(conn, bulletin, parish.as_of, updater)
            if prepared is None:
                stats["update_skipped_bulletins"] += 1
                parish.outcomes.append(CallOutcome(
                    PROCESS_SKIPPED, f"#{bulletin['id']}: PDF could not be loaded",
                ))
                continue
            if _already_decided(conn, prepared.request_key) or _pdf_already_read(conn, bulletin):
                continue
            stored = load_call_record(prepared.request_key)
            if stored is not None:
                stats["update_reused_replies"] += 1
                if not _finish(parish, prepared, stored):
                    return None
                continue
            stats["update_calls"] += 1
            return pool.submit(updater.call, prepared.pdf_bytes, prepared.context), prepared
        return None

    def _finish(parish: ParishRun, prepared: Prepared, reply: Any) -> bool:
        """Decide one reply. False when the parish must stop for this run."""
        try:
            record(finish_call(conn, prepared, updater, reply, run_id=run_id), parish)
        except BaseRevisionMismatch as exc:
            LOGGER.error("%s", exc)
            record(CallOutcome(PROCESS_FAILED, str(exc)), parish)
            parish.queue.clear()
            return False
        except Exception as exc:
            # Rolled back; the parish fails for this run and the others go on.
            LOGGER.exception("Deciding bulletin #%s failed", prepared.bulletin["id"])
            record(CallOutcome(
                PROCESS_FAILED,
                f"#{prepared.bulletin['id']}: {type(exc).__name__}: {exc}",
            ), parish)
            parish.queue.clear()
            return False
        return True

    waiting = deque(runs.values())
    in_flight: dict[Future[RawReply], tuple[ParishRun, Prepared]] = {}
    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        while waiting or in_flight:
            while waiting and len(in_flight) < max(1, concurrency):
                parish = waiting.popleft()
                started = advance(parish)
                if started is not None:
                    in_flight[started[0]] = (parish, started[1])
            if not in_flight:
                continue
            done, _ = wait(in_flight, return_when=FIRST_COMPLETED)
            for future in done:
                parish, prepared = in_flight.pop(future)
                try:
                    reply: Any = future.result()
                except Exception as exc:
                    LOGGER.warning(
                        "Update call failed for %s", prepared.bulletin.get("source_url"),
                        exc_info=True,
                    )
                    reply = exc
                if _finish(parish, prepared, reply):
                    started = advance(parish)
                    if started is not None:
                        in_flight[started[0]] = (parish, started[1])

    for parish in runs.values():
        _record_parish(conn, run_id, parish)
    LOGGER.info("Update mode finished: %s", stats)
    return stats


def _pdf_already_read(conn: sqlite3.Connection, bulletin: dict[str, Any]) -> bool:
    """Whether another bulletin of the parish with the same PDF has a successful call.

    `pending_bulletins` checks this when the run starts; this catches a copy
    whose original was called earlier in the same run.
    """
    return conn.execute(
        f"""SELECT 1 FROM llm_call c JOIN bulletin b ON b.id = c.bulletin_id
            WHERE b.parish_id = ? AND b.content_hash = ?
              AND c.status IN ({", ".join("?" * len(SUCCEEDED))}) LIMIT 1""",
        (bulletin["parish_id"], bulletin["content_hash"], *SUCCEEDED),
    ).fetchone() is not None


def _already_decided(conn: sqlite3.Connection, key: str) -> bool:
    return conn.execute(
        f"""SELECT 1 FROM llm_call WHERE request_key = ?
            AND status IN ({", ".join("?" * len(SUCCEEDED))})""",
        (key, *SUCCEEDED),
    ).fetchone() is not None


def _record_parish(conn: sqlite3.Connection, run_id: str | None, parish: ParishRun) -> None:
    if not parish.outcomes:
        return
    status = min(
        (o.status for o in parish.outcomes),
        key=lambda s: _PRECEDENCE.index(s) if s in _PRECEDENCE else len(_PRECEDENCE),
    )
    source = parish.last_source or {}
    record_parish_result(
        conn, run_id, parish.slug, "process", status,
        source_url=source.get("source_url"),
        content_hash=source.get("content_hash"),
        event_count=len(live_entries(conn, parish.parish_id)),
        detail=join_details(*(o.detail for o in parish.outcomes)),
    )

