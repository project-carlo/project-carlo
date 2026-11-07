"""The dispatcher's `.env`: read into a dict, never into its own environment.

`pnpm factory` doesn't load `.env` into `os.environ` (`__main__.py`), so nothing the
dispatcher starts inherits its keys. The backup and `pnpm data:pull` get the R2 keys from
here, and a stage gets only the entries its spec names in `secrets:` (its workers) and
`gate_secrets:` (its gate commands).
"""

from __future__ import annotations

import fnmatch
import os
from pathlib import Path

from pdf_extract.dotenv import read_dotenv
from pdf_extract.factory.config import FactoryError

Secrets = dict[str, str]

# Never given to a worker or a gate, whatever a stage spec says: publishing, GitHub, SSH,
# the host display, Claude logins, and the switch that lets the blob store write to R2.
NEVER = ("CLOUDFLARE_*", "GH_*", "GITHUB_*", "SSH_*", "DISPLAY", "XAUTHORITY",
         "CLAUDE_*", "ANTHROPIC_*", "CARLO_REMOTE_WRITE")

# Keys NEVER is about, to catch a spec glob that would match one (`*_TOKEN`).
KNOWN = ("CLOUDFLARE_API_TOKEN", "GH_TOKEN", "GITHUB_TOKEN", "SSH_AUTH_SOCK", "DISPLAY",
         "XAUTHORITY", "CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY", "CARLO_REMOTE_WRITE")

# Dropped from the dispatcher's own environment before a command runs, in case the shell
# or the service exported some: a command gets keys only from `.env`, by name.
SECRET_LIKE = ("R2_*", "AWS_*", "*_API_KEY", "*_TOKEN", "*_SECRET", "*_SECRET_*",
               "*_PASSWORD", "OPENAI_*", "GEMINI_*", "GOOGLE_*")

# Set for every command the dispatcher runs, and every worker: `.env` in the directory it
# runs in is not read (a worker could have written one), only the keys passed in.
NO_DOTENV = {"CARLO_NO_DOTENV": "1"}


def load_secrets(path: Path = Path(".env")) -> Secrets:
    return read_dotenv(path)


def never(name: str) -> bool:
    return any(fnmatch.fnmatchcase(name, p) for p in NEVER)


def check_patterns(patterns: list[str], where: str) -> None:
    """A spec's `secrets:` may not name, or match, a key in NEVER. (`pick` drops those
    anyway; this makes the mistake an error in the spec instead of a silent gap.)"""
    for pattern in patterns:
        hits = [k for k in KNOWN if fnmatch.fnmatchcase(k, pattern)]
        if hits or never(pattern):
            raise FactoryError(f"{where}: {pattern!r} would pass {(hits or [pattern])[0]}, "
                               "which no stage may be given")


def pick(secrets: Secrets, patterns: list[str]) -> dict[str, str]:
    """The entries matching a spec's names or globs (`R2_*`), NEVER aside."""
    return {k: v for k, v in secrets.items()
            if any(fnmatch.fnmatchcase(k, p) for p in patterns) and not never(k)}


def command_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    """The environment for a gate, setup or promote command: the dispatcher's own, without
    anything secret, plus `extra` (a stage's `gate_secrets`)."""
    env = {k: v for k, v in os.environ.items() if not never(k)
           and not any(fnmatch.fnmatchcase(k, p) for p in SECRET_LIKE)}
    return env | NO_DOTENV | (extra or {})
