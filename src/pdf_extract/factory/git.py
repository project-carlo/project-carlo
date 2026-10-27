"""The Run's branch and worktree. Only the dispatcher commits, pushes and merges."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from pdf_extract.factory.config import FactoryError

# Conflicts the dispatcher settles itself: take main's version, then promote again.
REGENERATED = ("data/parishes.csv", "data/churches.csv")


def git(cwd: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                          env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    if check and proc.returncode != 0:
        raise FactoryError(f"git {' '.join(args)}: {(proc.stderr or proc.stdout).strip()}")
    return proc.stdout


def ok(cwd: Path, *args: str) -> bool:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True).returncode == 0


def head(cwd: Path) -> str:
    return git(cwd, "rev-parse", "HEAD").strip()


def fetch(cwd: Path, remote: str) -> None:
    git(cwd, "fetch", "--quiet", remote)


def ensure_worktree(repo: Path, path: Path, branch: str, *, remote: str, base: str) -> bool:
    """The Run's worktree on its branch; True when it was just created.

    A branch already pushed (a worktree lost with the machine) is checked out again.
    """
    if (path / ".git").exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    git(repo, "worktree", "prune")
    if ok(repo, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"):
        git(repo, "worktree", "add", str(path), branch)
    elif ok(repo, "rev-parse", "--verify", "--quiet", f"refs/remotes/{remote}/{branch}"):
        git(repo, "worktree", "add", "-b", branch, str(path), f"{remote}/{branch}")
    else:
        git(repo, "worktree", "add", "--no-track", "-b", branch, str(path), base)
    return True


def changed_paths(cwd: Path) -> list[str]:
    """Every path git tracks or would track that differs from HEAD (gitignored ones aside)."""
    out = git(cwd, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    paths: list[str] = []
    items = out.split("\0")
    i = 0
    while i < len(items):
        item = items[i]
        i += 1
        if not item:
            continue
        status, path = item[:2], item[3:]
        paths.append(path)
        if "R" in status or "C" in status:
            paths.append(items[i])  # the rename's source
            i += 1
    return sorted(set(paths))


def revert(cwd: Path, paths: list[str], source: str = "HEAD") -> None:
    """Put paths back as `source` has them; delete those it lacks."""
    for path in paths:
        if ok(cwd, "cat-file", "-e", f"{source}:{path}"):
            git(cwd, "restore", f"--source={source}", "--staged", "--worktree", "--", path)
            continue
        git(cwd, "rm", "--cached", "--quiet", "--ignore-unmatch", "--", path, check=False)
        target = cwd / path
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()


def commit(cwd: Path, subject: str, trailers: dict[str, str]) -> str | None:
    """Commit everything changed; the new commit, or None when there was nothing."""
    git(cwd, "add", "-A")
    if ok(cwd, "diff", "--cached", "--quiet"):
        return None
    message = subject + "\n\n" + "\n".join(f"{k}: {v}" for k, v in trailers.items())
    git(cwd, "commit", "--quiet", "--no-verify", "-m", message)
    return head(cwd)


def push(cwd: Path, remote: str, branch: str) -> None:
    git(cwd, "push", "--quiet", "-u", remote, f"HEAD:refs/heads/{branch}")


@dataclass
class Merge:
    merged: bool = False
    conflicts: list[str] = field(default_factory=list)
    repromote: bool = False  # parishes.csv or churches.csv took main's version


def merge_upstream(cwd: Path, upstream: str) -> Merge:
    """Merge main into the Run branch when it has moved."""
    if ok(cwd, "merge-base", "--is-ancestor", upstream, "HEAD"):
        return Merge()
    if ok(cwd, "merge", "--quiet", "--no-edit", upstream):
        return Merge(merged=True)
    conflicts = git(cwd, "diff", "--name-only", "--diff-filter=U").split()
    if conflicts and all(c in REGENERATED for c in conflicts):
        git(cwd, "checkout", "--theirs", "--", *conflicts)
        git(cwd, "add", "--", *conflicts)
        git(cwd, "commit", "--quiet", "--no-edit", "--no-verify")
        return Merge(merged=True, repromote=True)
    git(cwd, "merge", "--abort", check=False)
    return Merge(conflicts=conflicts or ["(merge failed)"])


def remove_worktree(repo: Path, path: Path, branch: str) -> None:
    """Delete a merged Run's worktree and its local branch (the pushed branch stays)."""
    if path.exists():
        git(repo, "worktree", "remove", "--force", str(path))
    git(repo, "worktree", "prune")
    git(repo, "branch", "-D", branch, check=False)


def read_folder(repo: Path, ref: str, folder: str) -> dict[str, str]:
    """The files directly in `folder` as `ref` has them: name to text."""
    names = git(repo, "ls-tree", "--name-only", ref, f"{folder.rstrip('/')}/").split("\n")
    return {Path(n).name: git(repo, "show", f"{ref}:{n}") for n in names if n}


def is_merged(cwd: Path, sha: str, upstream: str) -> bool:
    return ok(cwd, "merge-base", "--is-ancestor", sha, upstream)
