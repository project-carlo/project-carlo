"""The dispatcher's settings: `factory/config.yaml`, then this machine's `data/factory/local.yaml`.

Paths are relative to the directory the dispatcher runs in, its own checkout, like the
rest of the pipeline's `data/`.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any

import yaml

FACTORY_DIR = Path("factory")
CONFIG_PATH = FACTORY_DIR / "config.yaml"
QUEUE_PATH = FACTORY_DIR / "queue.json"
STAGES_DIR = FACTORY_DIR / "stages"
DATA = Path("data") / "factory"
LOCAL_PATH = DATA / "local.yaml"
LEDGER_PATH = DATA / "factory.db"
RUNS_DIR = DATA / "runs"
# A stub run's ledger, worktrees, issues and PRs, apart from the real ones.
STUB_DATA = DATA / "stub"


# How long after an attempt the usage meter has caught up (docs/factory-spec.md, Usage).
QUOTA_SETTLE_SECONDS = 150


class FactoryError(RuntimeError):
    """Something the dispatcher can't do; the message says what to fix."""


@dataclass(frozen=True)
class Account:
    name: str
    config_dir: Path
    plan: str | None = None  # if its login doesn't say (pro, max...)
    # Its `claude setup-token` token, for sandboxed workers (docs/factory-sandbox-plan.md
    # §3.5): never refreshed, so a worker can't rotate the login the dispatcher reads.
    worker_token_file: Path | None = None


@dataclass
class Config:
    five_hour_cap: float = 75
    weekly_cap: float = 100
    max_workers: int = 1
    max_send_backs: int = 2
    lessons_before_integrate: int = 8
    seed_ready_bulletins: int = 2
    seed_first_run_share: float = 0.8
    seed_follow_up_weeks: int = 6
    tick_seconds: int = 60
    issue_poll_minutes: int = 10
    readiness_check_hours: int = 24
    backup_hour: int = 3
    backup_prefix: str = "factory/backups/"
    base_branch: str = "main"
    remote: str = "origin"
    branch_prefix: str = "factory/"  # a Run's branch is <prefix><run>
    # Quota readings (docs/factory-spec.md, Usage): a settled reading once an account has
    # been idle this long after an attempt, one of every account this often, and an
    # optional idle gap between attempts on an account so each gets a settled reading.
    quota_settle_seconds: int = QUOTA_SETTLE_SECONDS
    quota_sample_minutes: int = 15
    calibration_gap_seconds: int = 0
    # This machine's, from local.yaml.
    accounts: list[Account] = field(default_factory=list)
    owner: str = ""
    worktrees_dir: Path = DATA / "worktrees"
    setup: list[str] = field(default_factory=lambda: ["uv sync --group dev"])
    # Where workers run (docs/factory-sandbox-plan.md): `host`, or `sandbox` (a rootless
    # Podman container per attempt, never falling back to the host), and its limits.
    worker_backend: str = "host"
    sandbox_memory: str = "6g"
    sandbox_cpus: str = "4"
    sandbox_pids: int = 2048

    @property
    def upstream(self) -> str:
        return f"{self.remote}/{self.base_branch}"


def _read(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise FactoryError(f"{path} must be a mapping")
    return data


def load_config(config_path: Path = CONFIG_PATH, local_path: Path = LOCAL_PATH) -> Config:
    raw = {**_read(config_path), **_read(local_path)}
    known = {f.name for f in fields(Config)}
    unknown = sorted(set(raw) - known)
    if unknown:
        raise FactoryError(f"unknown factory settings: {', '.join(unknown)}")
    accounts = [
        Account(str(a["name"]), Path(str(a["config_dir"])).expanduser(),
                str(a["plan"]) if a.get("plan") else None,
                Path(str(a["worker_token_file"])).expanduser()
                if a.get("worker_token_file") else None)
        for a in raw.pop("accounts", None) or []
    ]
    if "worktrees_dir" in raw:
        raw["worktrees_dir"] = Path(str(raw["worktrees_dir"])).expanduser()
    for key in ("sandbox_memory", "sandbox_cpus"):  # `4` in YAML is still podman's "4"
        if key in raw:
            raw[key] = str(raw[key])
    if raw.get("worker_backend", "host") not in ("host", "sandbox"):
        raise FactoryError(f"worker_backend must be host or sandbox, not "
                           f"{raw['worker_backend']!r}")
    return Config(**raw, accounts=accounts)
