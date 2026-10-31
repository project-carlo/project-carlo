"""Where a worker's Claude CLI runs (docs/factory-sandbox-plan.md).

The SDK stays in the dispatcher and starts `factory/sandbox/claude-in-box` as its CLI
(`cli_path`). The dispatcher tells the launcher, in `CARLO_BOX`, what to run and which
environment names to keep; it drops the rest of what the SDK passes down, which is the
dispatcher's whole environment.

`worker_backend: host` (the default) runs the CLI on the host with that clean
environment, under its own Xvfb.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from pdf_extract.factory.config import FactoryError

# Relative to the dispatcher's own checkout, where it runs; never a Run's copy.
LAUNCHER = Path("factory") / "sandbox" / "claude-in-box"

# What a host worker keeps of the dispatcher's environment: what the CLI, uv, pnpm and
# Chrome need to run. Not DISPLAY, SSH_AUTH_SOCK or XDG_RUNTIME_DIR (its sockets).
HOST_PASS = ("PATH", "HOME", "USER", "LOGNAME", "SHELL", "LANG", "LC_ALL", "LC_CTYPE",
             "TZ", "TMPDIR", "PNPM_HOME")
# What the SDK adds to the CLI's environment itself.
SDK_ENV = ("CLAUDE_CODE_ENTRYPOINT", "CLAUDE_AGENT_SDK_VERSION",
           "CLAUDE_CODE_SDK_READS_SESSION_STATE", "CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING",
           "PWD")


class SandboxError(FactoryError):
    """The sandbox couldn't start a worker. The attempt ends as SANDBOX; never on the host."""


@dataclass
class Launch:
    """What the SDK gets for one attempt."""

    cli_path: str
    env: dict[str, str]  # options.env: the worker's environment and CARLO_BOX
    container: str | None = None


def plan_env(env: dict[str, str], argv: list[str], keep: list[str],
             container: str | None = None) -> dict[str, str]:
    """`env` plus the CARLO_BOX plan the launcher reads."""
    plan = {"argv": argv, "keep": sorted(set(keep)), "container": container}
    return env | {"CARLO_BOX": json.dumps(plan)}


class Backend(Protocol):
    name: str

    def launch(self, attempt: str, cwd: Path, env: dict[str, str]) -> Launch: ...

    def finish(self, launch: Launch) -> None: ...


class HostBackend:
    """The CLI on the host, with only `env` and HOST_PASS, under a private Xvfb."""

    name = "host"

    def __init__(self, launcher: Path = LAUNCHER, claude: str | None = None,
                 xvfb: str | None = None) -> None:
        self.launcher = launcher.resolve()
        self.claude = claude or shutil.which("claude") or "claude"
        self.xvfb = shutil.which("xvfb-run") if xvfb is None else xvfb

    def launch(self, attempt: str, cwd: Path, env: dict[str, str]) -> Launch:
        argv = ([self.xvfb, "-a"] if self.xvfb else []) + [self.claude]
        keep = [*HOST_PASS, *SDK_ENV, *env]
        return Launch(str(self.launcher), plan_env(env, argv, keep))

    def finish(self, launch: Launch) -> None:
        pass  # the launcher stops the worker's process group itself
