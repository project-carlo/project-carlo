"""The second opinion on each parish of a seed Run (docs/seed-second-opinion-plan.md).

While a seed Run is active, `fire` asks gpt-6-luna to read each of its parishes' newest
bulletins, in the background on a small thread pool, so the tick goes on while the calls
run. Each request is a `seed_opinion` row. Its reply is stored under its request key
(`second_opinion.request_key`) as soon as it comes back, and a row whose request was
answered before takes that reply instead of calling, so a retried or restarted
dispatcher never pays twice for one request. A row a stopped dispatcher left asking is
asked again on the next tick, at most `MAX_ATTEMPTS` times in all.

Replies stay in the ledger, which workers can't see, until the engine reveals one to the
seed job's drafter (`Engine._second_opinion`); the nightly backup leaves out those not
yet revealed (`backup.backup_ledger`). Nothing here writes a Run's files.

Worker threads each open their own ledger and database connections: a SQLite connection
belongs to the thread that made it.
"""

from __future__ import annotations

import json
import logging
import threading
from collections.abc import Callable
from concurrent.futures import Executor, ThreadPoolExecutor
from pathlib import Path
from typing import Any

from pdf_extract.factory.config import Config
from pdf_extract.factory.ledger import DONE as JOB_DONE
from pdf_extract.factory.ledger import JOB_BLOCKED, Ledger, now
from pdf_extract.factory.plan import seed_status
from pdf_extract.seeding.queries import bulletin_pdf, parish_bulletins, pdf_stored
from pdf_extract.seeding.second_opinion import (
    MIN_BULLETINS,
    Caller,
    pick_bulletins,
    request_key,
    run_opinion,
    today_of,
)
from pdf_extract.storage import churches_for_parish, connect_db

LOGGER = logging.getLogger(__name__)

QUEUED, ASKING, DONE, FAILED, SKIPPED = "queued", "asking", "done", "failed", "skipped"
WAITING = (QUEUED, ASKING)
# A call cut off by a dispatcher restart is asked once more, then given up.
MAX_ATTEMPTS = 2
# A Run's checkout has the seed CLI that reads a second opinion once it has this file:
# a Run that started before it (and hasn't merged main since) gets none.
OPINION_CODE = Path("src") / "pdf_extract" / "seeding" / "second_opinion.py"


def supported(worktree: Path) -> bool:
    return (worktree / OPINION_CODE).exists()


class _LedgerReplies:
    """`second_opinion.ReplyStore` over the ledger, for one row being answered."""

    def __init__(self, ledger: Ledger, row_id: int) -> None:
        self.ledger, self.row_id = ledger, row_id

    def get(self, key: str) -> dict[str, Any] | None:
        """A stored reply to the same request, which this row then takes. With none, the
        row is marked asking (one more attempt), since its call starts next."""
        prior = self.ledger.one(
            "SELECT * FROM seed_opinion WHERE request_key = ? AND status = ? AND reply IS NOT "
            "NULL AND id != ? ORDER BY id LIMIT 1", key, DONE, self.row_id)
        if prior is not None:
            self.ledger.run_sql(
                "UPDATE seed_opinion SET status = ?, reply = ?, reused_from = ?, cost_usd = 0, "
                "answered_at = ?, error = NULL WHERE id = ?", DONE, prior["reply"], prior["id"],
                now(), self.row_id)
            return json.loads(prior["reply"])
        self.ledger.run_sql("UPDATE seed_opinion SET status = ?, attempts = attempts + 1, "
                            "asked_at = ?, error = NULL WHERE id = ?", ASKING, now(), self.row_id)
        return None

    def put(self, key: str, record: dict[str, Any]) -> None:
        self.ledger.run_sql(
            "UPDATE seed_opinion SET status = ?, reply = ?, cost_usd = ?, answered_at = ? "
            "WHERE id = ?", DONE, json.dumps(record, ensure_ascii=False),
            record.get("cost_usd"), now(), self.row_id)


class Opinions:
    def __init__(self, ledger: Ledger, config: Config, *, db_path: Path,
                 caller: Callable[[], Caller],
                 read_pdf: Callable[[str, str], bytes] = bulletin_pdf,
                 stored: Callable[[str, str], bool] = pdf_stored,
                 executor: Executor | None = None) -> None:
        self.ledger, self.config, self.db_path = ledger, config, db_path
        self.caller, self.read_pdf, self.stored = caller, read_pdf, stored
        self.executor = executor or ThreadPoolExecutor(
            max_workers=max(1, config.opinion_workers), thread_name_prefix="seed-opinion")
        self._inflight: set[int] = set()
        self._lock = threading.Lock()

    # ── Asking ──────────────────────────────────────────────────────────────
    def fire(self, run: Any) -> None:
        """Ask for each parish of an active seed Run that has no request yet, and ask
        again for those a stopped dispatcher left unanswered. Cheap enough for every tick.

        Not for a parish already approved, or whose seed job finished before this Run's
        checkout could read an opinion: should it come back, its reveal asks then.
        """
        worktree = Path(run["worktree"])
        if not supported(worktree):
            return
        asked = {r["parish"] for r in self.ledger.all(
            "SELECT parish FROM seed_opinion WHERE run_id = ?", run["id"])}
        finished = {json.loads(j["input"]).get("parish") for j in self.ledger.all(
            "SELECT input FROM job WHERE run_id = ? AND stage = 'seed' AND status IN (?, ?)",
            run["id"], JOB_DONE, JOB_BLOCKED)}
        for parish in json.loads(run["parishes"] or "[]"):
            if parish in asked or parish in finished or seed_status(worktree, parish) == "approved":
                continue
            self._add(run["id"], parish)
        self._resume(run["id"])

    def ask(self, run_id: str, parish: str, seed: dict[str, Any],
            newest: dict[str, Any] | None) -> Any:
        """A request on the drafter's own bulletins: the newest few in its file, fetched by
        its newest read one."""
        candidates = [{k: b.get(k) for k in ("content_hash", "fetched_at", "published_date")}
                      for b in seed.get("bulletins") or [] if isinstance(b, dict)
                      and isinstance(b.get("content_hash"), str) and b.get("fetched_at")]
        return self._add(run_id, parish, candidates=candidates,
                         as_of=newest.get("fetched_at") if newest else None,
                         drafter_newest=newest.get("content_hash") if newest else None)

    def _add(self, run_id: str, parish: str, *, candidates: list[dict[str, Any]] | None = None,
             as_of: str | None = None, drafter_newest: str | None = None) -> Any:
        row_id = self.ledger.run_sql(
            "INSERT INTO seed_opinion (run_id, parish, status, drafter_newest, as_of, "
            "candidates, created_at) VALUES (?,?,?,?,?,?,?)", run_id, parish, QUEUED,
            drafter_newest, as_of, None if candidates is None else json.dumps(candidates), now())
        self._submit(row_id)
        return self.row(row_id)

    def _resume(self, run_id: str) -> None:
        for row in self.ledger.all("SELECT id, status, attempts FROM seed_opinion WHERE "
                                   "run_id = ? AND status IN (?, ?)", run_id, *WAITING):
            with self._lock:
                if row["id"] in self._inflight:
                    continue
            if row["status"] == ASKING and row["attempts"] >= MAX_ATTEMPTS:
                self.ledger.run_sql("UPDATE seed_opinion SET status = ?, error = ? WHERE id = ?",
                                    FAILED, f"cut off by a restart {row['attempts']} times",
                                    row["id"])
                continue
            self._submit(row["id"])

    def _submit(self, row_id: int) -> None:
        with self._lock:
            if row_id in self._inflight:
                return
            self._inflight.add(row_id)
        try:
            self.executor.submit(self._work, row_id)
        except RuntimeError:  # the pool is shut down: a later tick asks again
            with self._lock:
                self._inflight.discard(row_id)

    def _work(self, row_id: int) -> None:
        ledger = Ledger(self.ledger.path)
        try:
            row = ledger.one("SELECT * FROM seed_opinion WHERE id = ?", row_id)
            if row is None or row["status"] not in WAITING:
                return
            parish = row["parish"]
            conn = connect_db(self.db_path)
            try:
                churches = churches_for_parish(conn, parish)
                candidates = json.loads(row["candidates"]) if row["candidates"] else [
                    b for b in parish_bulletins(conn, parish) if b["duplicate_of"] is None]
            finally:
                conn.close()
            bulletins = pick_bulletins(candidates, lambda h: self.stored(parish, h),
                                       most=self.config.opinion_max_bulletins, as_of=row["as_of"])
            ledger.run_sql("UPDATE seed_opinion SET bulletins = ?, churches = ? WHERE id = ?",
                           json.dumps(bulletins), json.dumps(churches, ensure_ascii=False),
                           row_id)
            if len(bulletins) < MIN_BULLETINS:
                ledger.run_sql("UPDATE seed_opinion SET status = ?, error = ? WHERE id = ?",
                               SKIPPED, f"only {len(bulletins)} bulletin(s) with a stored PDF",
                               row_id)
                return
            caller = self.caller()
            today = today_of(bulletins)
            ledger.run_sql("UPDATE seed_opinion SET today = ?, request_key = ?, model = ?, "
                           "version = ? WHERE id = ?", today.isoformat(),
                           request_key(caller.version, parish, bulletins, churches, today),
                           caller.model, caller.version, row_id)
            run_opinion(caller, parish, bulletins, churches, _LedgerReplies(ledger, row_id),
                        read_pdf=self.read_pdf)
        except Exception as exc:  # luna unreachable, a PDF missing...: the seed goes on
            LOGGER.warning("second opinion %s failed: %s", row_id, exc)
            ledger.run_sql("UPDATE seed_opinion SET status = ?, error = ? WHERE id = ?",
                           FAILED, f"{type(exc).__name__}: {exc}"[:500], row_id)
        finally:
            ledger.close()
            with self._lock:
                self._inflight.discard(row_id)

    # ── Reading ─────────────────────────────────────────────────────────────
    def row(self, row_id: int) -> Any:
        return self.ledger.one("SELECT * FROM seed_opinion WHERE id = ?", row_id)

    def latest(self, run_id: str, parish: str) -> Any | None:
        return self.ledger.one("SELECT * FROM seed_opinion WHERE run_id = ? AND parish = ? "
                               "ORDER BY id DESC LIMIT 1", run_id, parish)

    def revealed(self, parish: str, key: Any) -> Any | None:
        """The revealed request a seed file's second opinion came from, in any Run."""
        if not isinstance(key, str):
            return None
        return self.ledger.one("SELECT * FROM seed_opinion WHERE parish = ? AND request_key = ? "
                               "AND revealed_at IS NOT NULL ORDER BY id DESC LIMIT 1", parish, key)

    def wait_all(self, timeout: float | None = None) -> None:
        """Until no call is in flight (tests, and the stub)."""
        import time

        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            with self._lock:
                if not self._inflight:
                    return
            if deadline is not None and time.monotonic() > deadline:
                return
            time.sleep(0.01)


def newest_bulletin(row: Any) -> str | None:
    """The content hash of the newest bulletin a request read, once it is known."""
    bulletins = json.loads(row["bulletins"] or "[]") if row is not None else []
    return bulletins[0]["content_hash"] if bulletins else None
