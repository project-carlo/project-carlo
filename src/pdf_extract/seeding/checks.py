"""`seed check`: a seed file against the database, as the loader and the labeler need it.

`files.validate_seed` checks the file's shape. This adds what needs the
database (docs/seeding-plan.md, "Implementation decisions"; the drafting
rules it enforces are .claude/skills/draft-parish-seed/rules.md R1, R2, R5):

- every entry parses as `pnpm schedule seed` would (`schedule.entries.parse_entry`),
  with an included entry's church one of the parish's (one left out, or an
  option, may name a chapel elsewhere);
- no two included entries share a slot;
- the dated entries a seed holds are on or after its `as_of` date;
- the file's bulletins are the parish's, and `as_of` is the fetch time of the
  newest one the agent read;
- the newest listed bulletin is marked read, and an agent's settled inclusions
  cite its own reading there at their page (reviewer answers may include older slots),
  or cite an assessed current website schedule in that bulletin's context,
  or retain an established weekly slot after one assessed omission;
  except what the newest bulletin can't be expected to print (`older_evidence_ok`):
  a weeks-of-the-month slot none of whose weeks fall in the newest bulletin's
  week, or a dated entry from `as_of` on that an older bulletin announced.

A source seed (docs/source-schedules-plan.md) has no bulletins: its `as_of` is
its newest capture's time, and with `check_evidence` its parish is
`website_schedule`, each capture's committed text is there with the hash the
file gives and says it is of the page the file gives, its website captures are on
(and stay on) the parish's own site, its Facebook captures are the parish's own
page (its website, or one its website's captures link), and every source's
`said` is in its capture's text. One read from the screenshot (`from_image`)
can't be matched: it must name the capture's screenshot, committed, so a
reviewer can see it.
"""

from __future__ import annotations

import calendar
import hashlib
import sqlite3
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from pdf_extract.bulletin_week import bulletin_reference_date, bulletin_week, parse_iso_date
from pdf_extract.model import (
    DAYS,
    FACEBOOK,
    WEBSITE,
    WEBSITE_SCHEDULE,
    WEEKS_OF_MONTH,
    facebook_page,
    normalize_as_of,
    sha256_text,
    source_platform,
)
from pdf_extract.parish_sites.links import registrable_domain, url_host
from pdf_extract.schedule.entries import UNKNOWN_CHURCH, Entry, EntryError, parse_entry
from pdf_extract.schedule.store import parish_churches
from pdf_extract.seeding.files import (
    AGENT,
    BLOCKED,
    DRAFTING,
    INCLUDE,
    NEEDS_HUMAN,
    SEEDS_DIR,
    captures,
    is_source_seed,
    newest_capture,
    newest_read_bulletin,
    normalize_quote,
    parse_capture_document,
    read_capture_text,
    resolve_capture,
    resolve_hash,
    screenshot_path,
    validate_seed,
)

# The days a bulletin's calendar is taken to cover: its week's Sunday through
# the next Sunday (an issue's calendar usually runs from its Sunday to the next).
COVERED_DAYS = 8


def weeks_of(day: date) -> set[str]:
    """Which of `weeks_of_month`'s weeks `day` is in for its weekday: `first` to
    `fifth`, and `last` when it is that weekday's last in the month."""
    weeks = {WEEKS_OF_MONTH[(day.day - 1) // 7]}
    if day.day + 7 > calendar.monthrange(day.year, day.month)[1]:
        weeks.add("last")
    return weeks


def covered_weeks(bulletin: dict[str, Any], day_of_week: str) -> set[str] | None:
    """The weeks of the month `day_of_week` falls in during the days `bulletin` covers,
    or None when the bulletin has no date to tell."""
    start = bulletin_week(bulletin)
    if start is None or day_of_week not in DAYS:
        return None
    weeks: set[str] = set()
    for offset in range(COVERED_DAYS):
        day = start + timedelta(days=offset)
        if DAYS[day.weekday()] == day_of_week:
            weeks |= weeks_of(day)
    return weeks


def older_evidence_ok(
    seed: dict[str, Any], slot: dict[str, Any], newest: dict[str, Any], as_of_date: str | None,
) -> bool:
    """Whether a settled inclusion may rest on an older bulletin than the newest read.

    Two kinds of slot don't appear in every issue, so the newest one not printing
    them says nothing:

    - a weekly slot on some weeks of the month ("First Friday"), when none of its
      weeks falls in the newest bulletin's week. It must cite the newest bulletin
      read whose week does hold one of them, if any does: that one would print it.
    - a dated entry on or after `as_of` an older bulletin announced (a Mass on
      All Souls Day printed a month ahead).

    Either way the slot has no `page` (the newest bulletin doesn't print it) and
    an agent source on a read bulletin at a page.
    """
    entry = slot["entry"]
    if slot["page"] is not None or not isinstance(entry, dict):
        return False
    read = sorted(
        (b for b in seed["bulletins"] if b["read"]),
        key=lambda b: normalize_as_of(b["fetched_at"]), reverse=True,
    )
    cited = {
        resolve_hash(seed, s.get("bulletin")) for s in slot["sources"]
        if s.get("source") == AGENT and s.get("page") is not None
    }
    cited_read = [b for b in read if b["content_hash"] in cited]
    if not cited_read:
        return False
    if entry.get("event_kind") == "weekly":
        weeks = set(entry.get("weeks_of_month") or [])
        if not weeks or entry.get("exclude_weeks"):
            return False
        here = covered_weeks(newest, entry.get("day_of_week") or "")
        if here is None or here & weeks:
            return False
        covering = [b for b in read if (covered_weeks(b, entry["day_of_week"]) or set()) & weeks]
        if not covering:
            return True
        return covering[0]["content_hash"] in cited
    return bool(as_of_date and entry.get("date") and entry["date"] >= as_of_date)


def _parish_id(conn: sqlite3.Connection, parish_slug: str) -> int | None:
    row = conn.execute("SELECT id FROM parish WHERE slug = ?", (parish_slug,)).fetchone()
    return None if row is None else int(row[0])


def weekly_omission_ok(
    seed: dict[str, Any], slot: dict[str, Any], newest: dict[str, Any],
) -> bool:
    """Auditable carry-forward after one omission, not a semantic schedule check.

    The assessment and this slot's paged agent quotes assert that the same
    church/type/weekday/time recurs and that the newest issue merely omits it,
    rather than cancelling or changing it. Code cannot decide those meanings.
    It checks distinct older issue weeks, including the immediately preceding
    read issue exactly one week before newest. Fetch dates cannot establish
    recurrence: missing/invalid/implausible publication dates get no credit.
    Named monthly patterns must use their targeted older-evidence rules.
    """
    entry = slot["entry"]
    assessment = slot.get("weekly_omission")
    if (slot["page"] is not None or not isinstance(entry, dict)
            or entry.get("event_kind") != "weekly" or entry.get("weeks_of_month")
            or entry.get("exclude_weeks") or entry.get("cancelled")
            or not isinstance(assessment, dict)
            or resolve_hash(seed, assessment.get("bulletin")) != newest["content_hash"]):
        return False

    def issue_week(bulletin: dict[str, Any]) -> date | None:
        published = parse_iso_date(bulletin.get("published_date"))
        if published is None or bulletin_reference_date(bulletin) != published:
            return None
        return bulletin_week(bulletin)

    read = sorted(
        (b for b in seed["bulletins"] if b["read"]),
        key=lambda b: normalize_as_of(b["fetched_at"]), reverse=True,
    )
    if len(read) < 3:
        return False
    here = issue_week(newest)
    previous = read[1]
    if (here is None or issue_week(previous) != here - timedelta(days=7)
            or normalize_as_of(previous["fetched_at"]) >= normalize_as_of(newest["fetched_at"])):
        return False
    cited = {
        resolve_hash(seed, source.get("bulletin")) for source in slot["sources"]
        if source.get("source") == AGENT and source.get("page") is not None
    }
    if previous["content_hash"] not in cited:
        return False
    weeks = {
        week for b in read[1:] if b["content_hash"] in cited
        and (week := issue_week(b)) is not None and week < here
    }
    return len(weeks) >= 2


def website_evidence_ok(
    seed: dict[str, Any], slot: dict[str, Any], newest: dict[str, Any],
) -> bool:
    """A quoted website schedule assessed against the newest read bulletin.

    Shape validation requires the URL, quote, check time and both explanations.
    These record the agent's judgment; code cannot establish semantic freshness.
    A website-only slot has no bulletin page or manufactured bulletin sighting.
    """
    return slot["page"] is None and any(
        source.get("source") == WEBSITE
        and isinstance(source.get("schedule_check"), dict)
        and resolve_hash(seed, source["schedule_check"].get("bulletin")) == newest["content_hash"]
        for source in slot["sources"]
    )


def entry_problem(
    raw: dict[str, Any], churches: dict[str, int], where: str, *, outside_ok: bool = False,
) -> str | None:
    """Why the entry can't be stored, or None. With `outside_ok`, a church that isn't the
    parish's is fine: an entry left out on purpose may be a chapel elsewhere."""
    try:
        parse_entry(raw, churches)
    except EntryError as exc:
        if outside_ok and exc.reason == UNKNOWN_CHURCH:
            return None
        return f"{where}: {exc.reason}: {exc}"
    return None


def check_seed(
    conn: sqlite3.Connection,
    seed: Any,
    *,
    parish_slug: str,
    check_bulletins: bool = True,
    check_evidence: bool = True,
    seeds_dir: Path = SEEDS_DIR,
) -> list[str]:
    """Every problem with a seed file (empty when it can be reviewed and loaded).

    A file still `drafting` is reported as such, since `seed check` is the
    last step of a draft. `check_bulletins` off skips comparing the file's
    bulletins with the database's, for a database that may not hold them all
    (the loader resolves what it can and needs only the entries).
    `check_evidence` off trusts a person's already-approved decisions: newer
    drafting evidence rules must not prevent previously approved seeds loading.
    `seeds_dir` is where a source seed's capture texts are (`captures/` in it).
    """
    problems = validate_seed(seed, parish_slug=parish_slug)
    if problems:
        return problems
    parish_id = _parish_id(conn, parish_slug)
    if parish_id is None:
        return [f"parish {parish_slug} is not in data/parishes.csv"]
    if seed["status"] == DRAFTING:
        problems.append(
            "status is still drafting: set needs_review (open questions) or ready, or blocked"
        )
    if seed["status"] == BLOCKED:
        return problems

    churches = parish_churches(conn, parish_id)
    source = is_source_seed(seed)
    if source and check_evidence:
        problems.extend(_source_problems(conn, seed, parish_id, seeds_dir))
    newest = newest_read_bulletin(seed)
    latest = max(seed["bulletins"], key=lambda b: normalize_as_of(b["fetched_at"]), default=None)
    if check_evidence and latest is not None and not latest["read"]:
        problems.append(
            f"newest listed bulletin {latest['content_hash'][:12]} must be marked read: "
            "use `pnpm seed mark-read` after reading it, even when no slot cites it"
        )
    as_of_date = normalize_as_of(seed["as_of"])[:10] if seed["as_of"] else None
    included_entries: list[tuple[Entry, str]] = []
    for i, slot in enumerate(seed["slots"]):
        where = f"slots[{i}] ({slot['id']})"
        included = slot["decision"] == INCLUDE and slot["status"] != NEEDS_HUMAN
        if check_evidence and included and slot["answer"] is None and not source:
            # A reviewer may explicitly include an older/website-backed option.
            # The agent may instead assess a quoted website schedule in its context.
            anchored = newest is not None and slot["page"] is not None and any(
                source.get("source") == AGENT
                and resolve_hash(seed, source.get("bulletin")) == newest["content_hash"]
                and source.get("page") == slot["page"]
                for source in slot["sources"]
            )
            if not anchored and not (
                newest is not None and (
                    older_evidence_ok(seed, slot, newest, as_of_date)
                    or website_evidence_ok(seed, slot, newest)
                    or weekly_omission_ok(seed, slot, newest)
                )
            ):
                problems.append(
                    f"{where}: a settled inclusion needs an agent source on the newest "
                    "bulletin at its page; otherwise leave it needs_human with page null "
                    "(a weeks-of-the-month slot whose weeks the newest bulletin's week "
                    "doesn't hold, or a dated entry from as_of on, may instead cite an older "
                    "bulletin read, with page null; or a quoted website schedule may use "
                    "schedule_check explaining why it is current and fits the newest "
                    "read bulletin, with page null; or an every-week slot may use "
                    "weekly_omission assessing the newest issue, with page null and "
                    "paged agent evidence from two older issue weeks, including the "
                    "immediately preceding read issue one week before newest)"
                )
        if slot["entry"] is not None:
            problem = entry_problem(
                slot["entry"], churches, f"{where}.entry", outside_ok=not included,
            )
            if problem:
                problems.append(problem)
            elif included:
                entry = parse_entry(slot["entry"], churches)
                for other, slot_id in included_entries:
                    if entry.conflicts_with(other):
                        problems.append(
                            f"{where} is the same slot as {slot_id}: "
                            "their recurrence patterns overlap; one of them must go"
                        )
                        break
                included_entries.append((entry, slot["id"]))
                date = slot["entry"].get("date")
                if as_of_date and slot["entry"]["event_kind"] != "weekly" and date < as_of_date:
                    problems.append(
                        f"{where} is dated {date}, before as_of ({as_of_date}): a seed holds "
                        "only dated entries from as_of on"
                    )
        for j, option in enumerate(slot["options"] or []):
            if option.get("entry") is not None:
                # An option is only a proposal: choosing one that names a church
                # outside the parish fails the included slot's check instead.
                problem = entry_problem(
                    option["entry"], churches, f"{where}.options[{j}].entry", outside_ok=True,
                )
                if problem:
                    problems.append(problem)

    if seed["as_of"] is not None and source:
        latest_capture = newest_capture(seed)
        if latest_capture is None:
            problems.append("as_of names a capture, but the file has none")
        elif normalize_as_of(latest_capture["captured_at"]) != normalize_as_of(seed["as_of"]):
            problems.append(
                f"as_of must be the time of the newest capture ({latest_capture['captured_at']}, "
                f"{latest_capture['content_hash'][:12]}), not {seed['as_of']}"
            )
    elif seed["as_of"] is not None:
        as_of = normalize_as_of(seed["as_of"])
        if newest is None:
            problems.append("as_of names a bulletin, but no bulletin is marked read")
        elif normalize_as_of(newest["fetched_at"]) != as_of:
            problems.append(
                f"as_of must be the fetch time of the newest bulletin read "
                f"({newest['fetched_at']}, {newest['content_hash'][:12]}), not {seed['as_of']}"
            )
        for b in seed["bulletins"]:
            if normalize_as_of(b["fetched_at"]) > as_of and b["read"]:
                problems.append(f"bulletin {b['content_hash'][:12]} is read but newer than as_of")
    if check_bulletins:
        problems.extend(_bulletin_problems(conn, seed, parish_id))
    return problems


def _source_problems(
    conn: sqlite3.Connection, seed: dict[str, Any], parish_id: int, seeds_dir: Path,
) -> list[str]:
    """What a source seed's evidence needs: the right parish, its own pages, real quotes,
    and each screenshot a quote was read from committed."""
    parish = conn.execute(
        "SELECT slug, homepage_url, bulletin_provider FROM parish WHERE id = ?", (parish_id,),
    ).fetchone()
    slug = parish["slug"]
    problems = []
    if parish["bulletin_provider"] != WEBSITE_SCHEDULE:
        problems.append(
            f"a source seed is for a {WEBSITE_SCHEDULE} parish, and this one's bulletin_provider "
            f"is {parish['bulletin_provider'] or 'empty'}: a parish with a bulletin is seeded "
            "from it"
        )
    homepage = parish["homepage_url"] or ""
    own_site = own_site_test(homepage)

    # Each capture's committed text, by its hash: its header, and the page's text.
    texts: dict[str, str | None] = {}
    headers: dict[str, dict[str, Any]] = {}
    for capture in captures(seed):
        short = capture["content_hash"][:12]
        document = read_capture_text(slug, capture["content_hash"], seeds_dir)
        parsed = None
        if document is None:
            problems.append(f"capture {short}'s text is missing: commit "
                            f"data/seeds/captures/{slug}/{capture['content_hash']}.txt")
        elif sha256_text(document) != capture["content_hash"]:
            problems.append(f"capture {short}'s text has changed since it was captured")
        elif (parsed := parse_capture_document(document)) is None:
            problems.append(f"capture {short}'s text doesn't say what page it is of: capture "
                            "the page again")
        elif (parsed[0]["url"], parsed[0]["final_url"]) != (capture["url"],
                                                             capture["final_url"]):
            problems.append(f"capture {short}'s url and final_url must be those its text "
                            f"was captured from ({parsed[0]['url']}, "
                            f"{parsed[0]['final_url']})")
            parsed = None
        texts[capture["content_hash"]] = parsed[1] if parsed else None
        if parsed:
            headers[capture["content_hash"]] = parsed[0]

    # The parish's own Facebook pages: its website, when that is a Facebook page, and
    # each one a page of its own website links.
    own_facebook = {facebook_page(homepage)} - {None}
    for capture in captures(seed):
        header = headers.get(capture["content_hash"])
        if header and capture["platform"] == WEBSITE and own_site(capture["url"]):
            own_facebook.update(header["facebook_pages"])

    for capture in captures(seed):
        short = capture["content_hash"][:12]
        url, final = capture["url"], capture["final_url"]
        if capture["platform"] == WEBSITE:
            if not own_site(url):
                problems.append(f"capture {short} ({url}) is not on the parish's own website, "
                                f"{homepage or 'none in data/parishes.csv'}")
            elif final and not own_site(final):
                problems.append(f"capture {short} ({url}) ended on another site, {final}: "
                                "quote the parish's own pages (if the parish has moved, "
                                "correct its website in the diocese's records first)")
        elif capture["platform"] == FACEBOOK:
            if facebook_page(url) not in own_facebook:
                problems.append(
                    f"capture {short} ({url}) is not the parish's own Facebook page: capture "
                    "the page of its website that links it"
                    + (f" (its website links {', '.join(sorted(own_facebook))})"
                       if own_facebook else " (no capture of its website links one)"))
            elif final and source_platform(final) != FACEBOOK:
                problems.append(f"capture {short} ({url}) ended off Facebook, at {final}")

    for slot in seed["slots"]:
        for j, src in enumerate(slot["sources"]):
            capture = resolve_capture(seed, src.get("capture"))
            if capture is None:
                continue
            at = f"{slot['id']}.sources[{j}]"
            if "from_image" in src:
                problems.extend(_screenshot_problems(slug, capture, src["from_image"], at,
                                                     seeds_dir))
                continue
            text = texts.get(capture["content_hash"])
            if text is not None and normalize_quote(src["said"]) not in normalize_quote(text):
                problems.append(
                    f"{at}.said is not in capture {capture['content_hash'][:12]}'s text: quote "
                    "the page as it reads (`pnpm seed capture-text`), or cite a quote read "
                    "from its screenshot as `cap <capture> image: …`"
                )
    return problems


def own_site_test(homepage: str) -> Callable[[str], bool]:
    """Whether an address is on the parish's own website, `homepage` its address.

    A site on a domain of its own (stmary.org) is every host of that domain. One on a
    host it shares, a platform's or a diocese's subdomain (stmary.weebly.com,
    sites.google.com/view/stmary/home, parishes.rcda.org/stmary/), is that host only,
    and on it the homepage's folder, since the rest of the domain is other sites'.
    """
    home_host = (url_host(homepage) or "").removeprefix("www.")
    domain = registrable_domain(home_host)
    if not domain:
        return lambda url: False
    if home_host == domain:
        return lambda url: registrable_domain(url_host(url) or "") == domain
    # The homepage's folder: its path, less the page's name unless it ends with a slash.
    folder = _path_segments(homepage)
    if not _path(homepage).endswith("/"):
        folder = folder[:-1]

    def own(url: str) -> bool:
        host = (url_host(url) or "").removeprefix("www.")
        return host == home_host and _path_segments(url)[:len(folder)] == folder
    return own


def _path(url: str) -> str:
    try:
        return urlsplit(url).path
    except ValueError:  # a malformed address
        return ""


def _path_segments(url: str) -> list[str]:
    """An address's path as lowercase segments."""
    return [unquote(s).lower() for s in _path(url).split("/") if s]


def _screenshot_problems(slug: str, capture: dict[str, Any], shot_hash: Any, at: str,
                         seeds_dir: Path) -> list[str]:
    """A quote read from a screenshot: the capture's current one, committed as it was."""
    if not isinstance(shot_hash, str) or shot_hash != capture["screenshot_hash"]:
        return [f"{at} was read from a screenshot the capture no longer has (the page was "
                "captured again): read its new tiles and write the source again"]
    try:
        path = screenshot_path(slug, shot_hash, seeds_dir)
        data = path.read_bytes()
    except (OSError, ValueError):
        return [f"{at} quotes screenshot {shot_hash[:12]}, which isn't committed in "
                f"data/seeds/captures/{slug}/: `pnpm seed finalize` commits it from this "
                "machine's store, or capture the page again here"]
    if hashlib.sha256(data).hexdigest() != shot_hash:
        return [f"{at}: the committed screenshot {shot_hash[:12]} has changed since it was "
                "captured"]
    return []


def _bulletin_problems(
    conn: sqlite3.Connection, seed: dict[str, Any], parish_id: int,
) -> list[str]:
    problems = []
    for b in seed["bulletins"]:
        rows = conn.execute(
            "SELECT fetched_at FROM bulletin WHERE parish_id = ? AND content_hash = ?",
            (parish_id, b["content_hash"]),
        ).fetchall()
        short = b["content_hash"][:12]
        if not rows:
            problems.append(f"bulletin {short} is not one of the parish's in the database")
            continue
        fetched = {normalize_as_of(r["fetched_at"]) for r in rows if r["fetched_at"]}
        if normalize_as_of(b["fetched_at"]) not in fetched:
            problems.append(
                f"bulletin {short} was fetched at {', '.join(sorted(fetched))}, "
                f"not {b['fetched_at']}"
            )
    return problems
