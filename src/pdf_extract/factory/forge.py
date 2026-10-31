"""GitHub: an issue for each blocking flag, reading your answers back, and the Run's PR (§7).

Only the dispatcher talks to GitHub, through `gh` with your login. Its own comments carry
a marker, so they are never read back as your answer.
"""

from __future__ import annotations

import json
import os
import subprocess
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from pdf_extract.factory import git
from pdf_extract.factory.config import FactoryError

MARKER = "<!-- factory -->"
ACCEPT = "/accept"
LABEL_COLORS = {"factory": "5319E7", "run": "C5DEF5", "stage": "BFDADC"}


@dataclass
class Comment:
    author: str
    body: str


@dataclass
class Issue:
    number: int
    state: str  # OPEN | CLOSED
    comments: list[Comment] = field(default_factory=list)


class Forge(Protocol):
    def open_issue(self, title: str, body: str, labels: list[str]) -> int: ...
    def issue(self, number: int) -> Issue: ...
    def comment(self, number: int, body: str) -> None: ...
    def reopen(self, number: int, body: str) -> None: ...
    def close(self, number: int, body: str) -> None: ...
    def open_pr(self, cwd: Path, branch: str, base: str, title: str, body: str) -> str: ...
    def pr_merged(self, url: str) -> bool: ...


def answer(issue: Issue, owner: str, suggestion: str) -> str | None:
    """Your last comment, or the suggestion for `/accept`; None when you haven't answered."""
    mine = [c for c in issue.comments
            if c.author.lower() == owner.lower() and MARKER not in c.body and c.body.strip()]
    if not mine:
        return None
    text = mine[-1].body.strip()
    if text.split()[0] == ACCEPT:
        rest = text[len(ACCEPT):].strip()
        return suggestion + (f"\n\n{rest}" if rest else "")
    return text


def issue_body(flag: Any, run: Any, job: Any | None) -> str:
    evidence = json.loads(flag["evidence"] or "[]")
    lines = [
        MARKER,
        f"**Run** `{run['id']}`  **Stage** `{job['stage'] if job else '-'}`  "
        f"**Job** `{job['name'] if job else '-'}`  **Subject** `{flag['subject']}`",
        "",
        "## Question",
        "",
        flag["question"],
        "",
        "## Evidence",
        "",
        *([f"- {e}" for e in evidence] or ["- (none given)"]),
        "",
        "## Suggestion",
        "",
        flag["suggestion"] or "(none)",
        "",
        "---",
        f"Answer with a comment, then close the issue. Your last comment is the answer; "
        f"`{ACCEPT}` takes the suggestion. Only comments from the owner's login count.",
    ]
    return "\n".join(lines)


def _gh(*args: str, cwd: Path | None = None, input: str | None = None) -> str:
    proc = subprocess.run(["gh", *args], cwd=cwd, capture_output=True, text=True, input=input,
                          env={**os.environ, **git.SAFE_ENV})
    if proc.returncode != 0:
        raise FactoryError(f"gh {' '.join(args[:2])}: {(proc.stderr or proc.stdout).strip()}")
    return proc.stdout


class GhForge:
    """GitHub through the `gh` CLI, in the dispatcher's checkout."""

    def __init__(self, cwd: Path) -> None:
        self.cwd = cwd
        self._labels: set[str] = set()

    def _label(self, name: str) -> None:
        if name in self._labels:
            return
        color = LABEL_COLORS.get(name.split(":")[0], "EDEDED")
        _gh("label", "create", name, "--color", color, "--force", cwd=self.cwd)
        self._labels.add(name)

    def open_issue(self, title: str, body: str, labels: list[str]) -> int:
        for label in labels:
            self._label(label)
        args = ["issue", "create", "--title", title, "--body-file", "-"]
        for label in labels:
            args += ["--label", label]
        url = _gh(*args, cwd=self.cwd, input=body).strip()
        return int(url.rstrip("/").rsplit("/", 1)[-1])

    def issue(self, number: int) -> Issue:
        data = json.loads(_gh("issue", "view", str(number), "--json", "state,comments",
                              cwd=self.cwd))
        return Issue(number, data["state"], [
            Comment((c.get("author") or {}).get("login", ""), c.get("body", ""))
            for c in data.get("comments", [])
        ])

    def comment(self, number: int, body: str) -> None:
        _gh("issue", "comment", str(number), "--body-file", "-", cwd=self.cwd,
            input=f"{MARKER}\n{body}")

    def reopen(self, number: int, body: str) -> None:
        _gh("issue", "reopen", str(number), cwd=self.cwd)
        self.comment(number, body)

    def close(self, number: int, body: str) -> None:
        self.comment(number, body)
        _gh("issue", "close", str(number), cwd=self.cwd)

    def open_pr(self, cwd: Path, branch: str, base: str, title: str, body: str) -> str:
        existing = json.loads(_gh("pr", "list", "--head", branch, "--state", "open",
                                  "--json", "url", cwd=cwd))
        if existing:
            return existing[0]["url"]
        return _gh("pr", "create", "--head", branch, "--base", base, "--title", title,
                   "--body-file", "-", cwd=cwd, input=body).strip()

    def pr_merged(self, url: str) -> bool:
        return _gh("pr", "view", url, "--json", "state", "--jq", ".state",
                   cwd=self.cwd).strip() == "MERGED"


def owner_login() -> str:
    return _gh("api", "user", "--jq", ".login").strip()


class LocalForge:
    """Issues and PRs as files, for stub runs: nothing reaches GitHub.

    Close an issue and answer it by editing its file: set `state` to `CLOSED` and add a
    comment `{"author": "<owner>", "body": "..."}`.
    """

    def __init__(self, folder: Path) -> None:
        self.folder = folder

    def _path(self, number: int) -> Path:
        return self.folder / "issues" / f"{number}.json"

    def _read(self, number: int) -> dict[str, Any]:
        return json.loads(self._path(number).read_text(encoding="utf-8"))

    def _write(self, data: dict[str, Any]) -> None:
        path = self._path(data["number"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=1), encoding="utf-8")

    def open_issue(self, title: str, body: str, labels: list[str]) -> int:
        existing = list((self.folder / "issues").glob("*.json"))
        number = 1 + max((int(p.stem) for p in existing), default=0)
        self._write({"number": number, "title": title, "body": body, "labels": labels,
                     "state": "OPEN", "comments": []})
        return number

    def issue(self, number: int) -> Issue:
        data = self._read(number)
        return Issue(number, data["state"], [Comment(c["author"], c["body"])
                                             for c in data["comments"]])

    def comment(self, number: int, body: str) -> None:
        data = self._read(number)
        data["comments"].append({"author": "factory", "body": f"{MARKER}\n{body}"})
        self._write(data)

    def reopen(self, number: int, body: str) -> None:
        data = self._read(number)
        data["state"] = "OPEN"
        self._write(data)
        self.comment(number, body)

    def close(self, number: int, body: str) -> None:
        self.comment(number, body)
        data = self._read(number)
        data["state"] = "CLOSED"
        self._write(data)

    def open_pr(self, cwd: Path, branch: str, base: str, title: str, body: str) -> str:
        path = self.folder / "prs" / f"{branch.replace('/', '__')}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {title}\n\nbase: {base}\n\n{body}\n", encoding="utf-8")
        return path.resolve().as_uri()

    def merge_pr(self, url: str) -> None:
        """Mark a PR merged, as a squash merge on GitHub would (its commits aren't in main)."""
        self._pr_path(url).with_suffix(".merged").touch()

    def pr_merged(self, url: str) -> bool:
        return self._pr_path(url).with_suffix(".merged").exists()

    @staticmethod
    def _pr_path(url: str) -> Path:
        return Path(urllib.parse.unquote(urllib.parse.urlparse(url).path))
