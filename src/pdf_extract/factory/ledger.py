"""The ledger: SQLite state of Runs, jobs, attempts, worker steps, gates, flags and costs.

Work lives in git; the ledger holds the history foreman reviews need and what the
dispatcher must not do twice. A parish's state comes from its files, not from here.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pdf_extract.factory.config import LEDGER_PATH

# Run states and kinds.
ACTIVE, BLOCKED, IN_REVIEW, MERGED = "active", "blocked", "in_review", "merged"
PENDING = "pending"  # created, waiting for its turn (a follow-up waiting for a merge)
MAP, SEED = "map", "seed"

# Job states.
QUEUED, RUNNING, GATING, DONE = "queued", "running", "gating", "done"
WAITING_USAGE, SENT_BACK, JOB_BLOCKED, FAILED = "waiting_usage", "sent_back", "blocked", "failed"
UNFINISHED = (QUEUED, RUNNING, GATING, WAITING_USAGE, SENT_BACK)

# Flag states: open (an issue waits for you), answered (its answer not yet acted on),
# settled, or listed (advisory, for the PR).
OPEN, ANSWERED, SETTLED, LISTED = "open", "answered", "settled", "listed"

SCHEMA = """
CREATE TABLE IF NOT EXISTS run (
    id TEXT PRIMARY KEY,            -- wilmington-map-1
    diocese TEXT NOT NULL,
    kind TEXT NOT NULL,             -- map | seed
    number INTEGER NOT NULL,
    status TEXT NOT NULL,
    branch TEXT NOT NULL,
    worktree TEXT NOT NULL,
    follow_up_of TEXT,              -- a follow-up Run: the Run whose parked parishes it takes
    parishes TEXT,                  -- JSON: the parishes or roster refs a follow-up or seed Run covers
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    pr_url TEXT,
    head_sha TEXT,                  -- the last commit, which is in main once merged
    merged_at TEXT,
    blocked_reason TEXT
);
CREATE TABLE IF NOT EXISTS job (
    id INTEGER PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES run(id),
    name TEXT NOT NULL,             -- 004-map: its scratch folder under scratch/<run>/
    stage TEXT NOT NULL,
    input TEXT NOT NULL,            -- JSON: batch, entries, parish, answers...
    status TEXT NOT NULL,
    account TEXT,                   -- set on first start; a job stays on its account
    session_id TEXT,
    commit_sha TEXT,                -- the commit it ran at: its stage spec, skills, CLI
    send_backs INTEGER NOT NULL DEFAULT 0,
    continues INTEGER NOT NULL DEFAULT 0,
    pending_prompt TEXT,            -- what the next attempt is told (problems, an answer)
    handoff TEXT,                   -- JSON, once it passed the handoff gate
    resumes_job INTEGER,            -- a parked parish's job, resumed with your answer
    wait_until TEXT,
    cost_usd REAL NOT NULL DEFAULT 0,
    turns INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    started_at TEXT,
    finished_at TEXT,
    UNIQUE (run_id, name)
);
CREATE TABLE IF NOT EXISTS attempt (
    id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES job(id),
    n INTEGER NOT NULL,
    kind TEXT NOT NULL,             -- start | send_back | continue | resume | answer | fresh
    prompt TEXT NOT NULL,
    account TEXT,
    session_id TEXT,
    commit_sha TEXT,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    outcome TEXT,                   -- ok | crash | usage | timeout | partial | error
    error TEXT,
    cost_usd REAL NOT NULL DEFAULT 0,
    turns INTEGER NOT NULL DEFAULT 0,
    transcript TEXT
);
CREATE TABLE IF NOT EXISTS step (
    id INTEGER PRIMARY KEY,
    attempt_id INTEGER NOT NULL REFERENCES attempt(id),
    n INTEGER NOT NULL,
    kind TEXT NOT NULL,             -- tool | text | result | rate_limit
    name TEXT,
    detail TEXT,
    at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS gate (
    id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES job(id),
    attempt_id INTEGER,
    name TEXT NOT NULL,
    passed INTEGER NOT NULL,
    output TEXT NOT NULL,
    at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS action (   -- steps after the gates, each done once
    job_id INTEGER NOT NULL REFERENCES job(id),
    name TEXT NOT NULL,
    result TEXT,
    at TEXT NOT NULL,
    PRIMARY KEY (job_id, name)
);
CREATE TABLE IF NOT EXISTS flag (
    id INTEGER PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES run(id),
    job_id INTEGER REFERENCES job(id),
    severity TEXT NOT NULL,
    scope TEXT NOT NULL,
    subject TEXT NOT NULL,
    question TEXT NOT NULL,
    evidence TEXT NOT NULL DEFAULT '[]',
    suggestion TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL,
    issue_number INTEGER,
    answer TEXT,
    answered_at TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS lead (
    id INTEGER PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES run(id),
    job_id INTEGER REFERENCES job(id),
    touches TEXT NOT NULL,
    note TEXT NOT NULL,
    used_by INTEGER REFERENCES job(id)
);
CREATE TABLE IF NOT EXISTS lesson (
    id INTEGER PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES run(id),
    job_id INTEGER REFERENCES job(id),
    stage TEXT NOT NULL,
    text TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS decision (  -- seed-review's answers, for the PR and foremen
    id INTEGER PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES run(id),
    job_id INTEGER REFERENCES job(id),
    parish TEXT NOT NULL,
    slot TEXT NOT NULL,
    question TEXT NOT NULL,
    lean TEXT,
    choice TEXT NOT NULL,
    basis TEXT NOT NULL,
    why TEXT NOT NULL,
    against_lean INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS verdict (   -- every reviewer verdict on a piece of work
    id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES job(id),
    reviewed_job INTEGER REFERENCES job(id),
    subject TEXT NOT NULL,
    verdict TEXT NOT NULL,
    problems TEXT NOT NULL DEFAULT '[]',
    at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS usage (
    id INTEGER PRIMARY KEY,
    account TEXT NOT NULL,
    at TEXT NOT NULL,
    five_hour REAL,
    five_hour_resets TEXT,
    seven_day REAL,
    seven_day_resets TEXT
);
CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT);
CREATE INDEX IF NOT EXISTS job_run ON job (run_id, status);
CREATE INDEX IF NOT EXISTS flag_run ON flag (run_id, status);
CREATE INDEX IF NOT EXISTS step_attempt ON step (attempt_id);
"""


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds")


class Ledger:
    """A connection to the ledger, with the queries the dispatcher and reports share."""

    def __init__(self, path: Path = LEDGER_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.conn = sqlite3.connect(path, isolation_level=None, timeout=30)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode = WAL")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)

    def close(self) -> None:
        self.conn.close()

    @contextmanager
    def tx(self) -> Iterator[sqlite3.Connection]:
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            yield self.conn
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise
        self.conn.execute("COMMIT")

    def one(self, sql: str, *args: Any) -> sqlite3.Row | None:
        return self.conn.execute(sql, args).fetchone()

    def all(self, sql: str, *args: Any) -> list[sqlite3.Row]:
        return self.conn.execute(sql, args).fetchall()

    def run_sql(self, sql: str, *args: Any) -> int:
        return self.conn.execute(sql, args).lastrowid or 0

    # ── key-value ───────────────────────────────────────────────────────────
    def get(self, key: str, default: Any = None) -> Any:
        row = self.one("SELECT value FROM kv WHERE key = ?", key)
        return json.loads(row["value"]) if row else default

    def set(self, key: str, value: Any) -> None:
        self.run_sql("INSERT INTO kv (key, value) VALUES (?, ?) ON CONFLICT (key) "
                     "DO UPDATE SET value = excluded.value", key, json.dumps(value))

    # ── Runs ────────────────────────────────────────────────────────────────
    def run(self, run_id: str) -> sqlite3.Row:
        row = self.one("SELECT * FROM run WHERE id = ?", run_id)
        if row is None:
            raise KeyError(run_id)
        return row

    def runs(self, *statuses: str) -> list[sqlite3.Row]:
        if not statuses:
            return self.all("SELECT * FROM run ORDER BY created_at, id")
        marks = ",".join("?" * len(statuses))
        return self.all(f"SELECT * FROM run WHERE status IN ({marks}) ORDER BY created_at, id",
                        *statuses)

    def add_run(self, *, diocese: str, kind: str, worktrees_dir: Path, status: str = ACTIVE,
                follow_up_of: str | None = None, parishes: list[str] | None = None,
                notes: str = "", branch_prefix: str = "factory/") -> str:
        with self.tx():
            number = 1 + (self.one("SELECT MAX(number) AS n FROM run WHERE diocese = ? AND "
                                   "kind = ?", diocese, kind)["n"] or 0)
            run_id = f"{diocese}-{kind}-{number}"
            self.run_sql(
                "INSERT INTO run (id, diocese, kind, number, status, branch, worktree, "
                "follow_up_of, parishes, notes, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                run_id, diocese, kind, number, status, f"{branch_prefix}{run_id}",
                str(worktrees_dir / run_id), follow_up_of,
                json.dumps(parishes) if parishes is not None else None, notes, now())
        return run_id

    def set_run(self, run_id: str, **values: Any) -> None:
        cols = ", ".join(f"{k} = ?" for k in values)
        self.run_sql(f"UPDATE run SET {cols} WHERE id = ?", *values.values(), run_id)

    # ── Jobs ────────────────────────────────────────────────────────────────
    def job(self, job_id: int) -> sqlite3.Row:
        row = self.one("SELECT * FROM job WHERE id = ?", job_id)
        if row is None:
            raise KeyError(job_id)
        return row

    def jobs(self, run_id: str, stage: str | None = None) -> list[sqlite3.Row]:
        if stage is None:
            return self.all("SELECT * FROM job WHERE run_id = ? ORDER BY id", run_id)
        return self.all("SELECT * FROM job WHERE run_id = ? AND stage = ? ORDER BY id",
                        run_id, stage)

    def add_job(self, run_id: str, stage: str, inputs: dict[str, Any], *,
                resumes_job: int | None = None, status: str = QUEUED) -> int:
        with self.tx():
            seq = 1 + self.one("SELECT COUNT(*) AS n FROM job WHERE run_id = ?", run_id)["n"]
            return self.run_sql(
                "INSERT INTO job (run_id, name, stage, input, status, resumes_job, created_at) "
                "VALUES (?,?,?,?,?,?,?)", run_id, f"{seq:03d}-{stage}", stage,
                json.dumps(inputs), status, resumes_job, now())

    def set_job(self, job_id: int, **values: Any) -> None:
        cols = ", ".join(f"{k} = ?" for k in values)
        self.run_sql(f"UPDATE job SET {cols} WHERE id = ?", *values.values(), job_id)

    def unfinished_job(self, run_id: str) -> sqlite3.Row | None:
        marks = ",".join("?" * len(UNFINISHED))
        return self.one(f"SELECT * FROM job WHERE run_id = ? AND status IN ({marks}) "
                        "ORDER BY id LIMIT 1", run_id, *UNFINISHED)

    # ── Attempts and steps ──────────────────────────────────────────────────
    def add_attempt(self, job_id: int, kind: str, prompt: str, account: str | None,
                    commit_sha: str | None) -> int:
        n = 1 + self.one("SELECT COUNT(*) AS n FROM attempt WHERE job_id = ?", job_id)["n"]
        return self.run_sql(
            "INSERT INTO attempt (job_id, n, kind, prompt, account, commit_sha, started_at) "
            "VALUES (?,?,?,?,?,?,?)", job_id, n, kind, prompt, account, commit_sha, now())

    def finish_attempt(self, attempt_id: int, **values: Any) -> None:
        values.setdefault("finished_at", now())
        cols = ", ".join(f"{k} = ?" for k in values)
        self.run_sql(f"UPDATE attempt SET {cols} WHERE id = ?", *values.values(), attempt_id)

    def add_step(self, attempt_id: int, n: int, kind: str, name: str | None,
                 detail: str | None) -> None:
        self.run_sql("INSERT INTO step (attempt_id, n, kind, name, detail, at) "
                     "VALUES (?,?,?,?,?,?)", attempt_id, n, kind, name, detail, now())

    def add_gate(self, job_id: int, attempt_id: int | None, name: str, passed: bool,
                 output: str) -> None:
        self.run_sql("INSERT INTO gate (job_id, attempt_id, name, passed, output, at) "
                     "VALUES (?,?,?,?,?,?)", job_id, attempt_id, name, int(passed),
                     output[-4000:], now())

    # ── Actions after the gates: each done once, even across a restart ──────
    def done_action(self, job_id: int, name: str) -> bool:
        return self.one("SELECT 1 FROM action WHERE job_id = ? AND name = ?",
                        job_id, name) is not None

    def record_action(self, job_id: int, name: str, result: Any = None) -> None:
        self.run_sql("INSERT OR REPLACE INTO action (job_id, name, result, at) VALUES (?,?,?,?)",
                     job_id, name, json.dumps(result), now())

    def action_result(self, job_id: int, name: str) -> Any:
        row = self.one("SELECT result FROM action WHERE job_id = ? AND name = ?", job_id, name)
        return json.loads(row["result"]) if row else None

    def clear_actions(self, job_id: int) -> None:
        self.run_sql("DELETE FROM action WHERE job_id = ?", job_id)

    # ── Flags ───────────────────────────────────────────────────────────────
    def add_flag(self, run_id: str, job_id: int | None, *, severity: str, scope: str,
                 subject: str, question: str, evidence: list[str] | None = None,
                 suggestion: str = "") -> int:
        status = OPEN if severity == "blocking" else LISTED
        return self.run_sql(
            "INSERT INTO flag (run_id, job_id, severity, scope, subject, question, evidence, "
            "suggestion, status, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
            run_id, job_id, severity, scope, subject, question, json.dumps(evidence or []),
            suggestion, status, now())

    def flags(self, run_id: str, *statuses: str) -> list[sqlite3.Row]:
        if not statuses:
            return self.all("SELECT * FROM flag WHERE run_id = ? ORDER BY id", run_id)
        marks = ",".join("?" * len(statuses))
        return self.all(f"SELECT * FROM flag WHERE run_id = ? AND status IN ({marks}) "
                        "ORDER BY id", run_id, *statuses)

    def parked(self, run_id: str) -> list[sqlite3.Row]:
        """Parishes set aside by a blocking flag whose answer hasn't been acted on."""
        return self.all("SELECT * FROM flag WHERE run_id = ? AND severity = 'blocking' AND "
                        "scope = 'parish' AND status IN (?, ?) ORDER BY id",
                        run_id, OPEN, ANSWERED)
