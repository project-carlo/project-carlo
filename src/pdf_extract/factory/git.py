"""The Run's branch and checkout. Only the dispatcher commits, pushes and merges."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from pdf_extract.factory.config import FactoryError

# Conflicts the dispatcher settles itself: take main's version, then promote again.
REGENERATED = ("data/parishes.csv", "data/churches.csv")


# Git config a worker might have written (hooks, an fsmonitor command) never runs in the
# dispatcher's git calls, which hold the GitHub login. As `-c` options for git, and as
# environment for `gh`, which runs git itself.
SAFE = ("-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false")
SAFE_ENV = {"GIT_CONFIG_COUNT": "2",
            "GIT_CONFIG_KEY_0": "core.hooksPath", "GIT_CONFIG_VALUE_0": "/dev/null",
            "GIT_CONFIG_KEY_1": "core.fsmonitor", "GIT_CONFIG_VALUE_1": "false"}


def git(cwd: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *SAFE, *args], cwd=cwd, capture_output=True, text=True,
                          env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    if check and proc.returncode != 0:
        raise FactoryError(f"git {' '.join(args)}: {(proc.stderr or proc.stdout).strip()}")
    return proc.stdout


def ok(cwd: Path, *args: str) -> bool:
    return subprocess.run(["git", *SAFE, *args], cwd=cwd, capture_output=True).returncode == 0


def head(cwd: Path) -> str:
    return git(cwd, "rev-parse", "HEAD").strip()


def fetch(cwd: Path, remote: str) -> None:
    git(cwd, "fetch", "--quiet", remote)


def ensure_worktree(repo: Path, path: Path, branch: str, *, remote: str, base: str) -> bool:
    """The Run's checkout on its branch; True when it was just created.

    A standalone clone of `remote`, not a linked worktree of `repo`: nothing a Run does
    reaches the git metadata of the dispatcher's checkout, or the one it was made from
    (docs/factory-sandbox-plan.md §3.8). `repo`'s objects are copied, not shared, to
    save fetching them all. A branch already pushed (a checkout lost with the machine)
    is checked out again. A Run worktree from before the clones keeps working.
    """
    if (path / ".git").exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    url = git(repo, "remote", "get-url", remote).strip()
    git(path.parent, "clone", "--quiet", "--no-checkout", "--origin", remote,
        "--reference-if-able", str(common_dir(repo)), "--dissociate", url, str(path))
    if ok(path, "rev-parse", "--verify", "--quiet", f"refs/remotes/{remote}/{branch}"):
        git(path, "checkout", "--quiet", "-b", branch, f"{remote}/{branch}")
    else:
        git(path, "checkout", "--quiet", "--no-track", "-b", branch, base)
    return True


def common_dir(path: Path) -> Path:
    """The repository's own git folder, also from a linked worktree (which clone's
    --reference can't take)."""
    return Path(git(path, "rev-parse", "--path-format=absolute", "--git-common-dir").strip())


def is_linked(path: Path) -> bool:
    """A linked worktree (`.git` is a file pointing into another repository)."""
    return (path / ".git").is_file()


def make_standalone(path: Path, remote: str) -> None:
    """Turn a linked worktree into a standalone clone of `remote`, in place: same
    branch, same commits (local ones too), same files, gitignored ones included.

    For the move to clones (`pnpm factory clones`). Run it with the dispatcher stopped.
    """
    if not is_linked(path):
        return
    common = common_dir(path)
    url = git(path, "remote", "get-url", remote).strip()
    branch = git(path, "branch", "--show-current").strip()
    sha = head(path)
    fresh = path.parent / f".{path.name}.clone"
    if fresh.exists():
        shutil.rmtree(fresh)
    git(path.parent, "clone", "--quiet", "--no-checkout", "--origin", remote,
        "--reference-if-able", str(common), "--dissociate", url, str(fresh))
    # Commits only the old repository has (not pushed yet), then its branch.
    git(fresh, "fetch", "--quiet", str(common), sha)
    if branch:
        git(fresh, "branch", "--force", "--no-track", branch, sha)
        git(fresh, "symbolic-ref", "HEAD", f"refs/heads/{branch}")
        if ok(fresh, "rev-parse", "--verify", "--quiet", f"refs/remotes/{remote}/{branch}"):
            git(fresh, "branch", "--set-upstream-to", f"{remote}/{branch}", branch)
    else:
        git(fresh, "update-ref", "--no-deref", "HEAD", sha)
    linked = (path / ".git").read_text(encoding="utf-8")
    (path / ".git").unlink()
    try:
        (fresh / ".git").rename(path / ".git")
    except OSError:
        (path / ".git").write_text(linked, encoding="utf-8")
        raise
    shutil.rmtree(fresh)
    git(path, "reset", "--quiet")  # the index for HEAD; the files stay as they are
    # The old repository's record of it (prune keeps it: the path still has a .git).
    admin = (path / linked.removeprefix("gitdir:").strip()).resolve()
    if admin.parent == common.resolve() / "worktrees":
        shutil.rmtree(admin, ignore_errors=True)


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
    """Delete a merged Run's checkout (the pushed branch stays)."""
    if is_linked(path):  # from before the clones: its branch is in `repo`
        git(repo, "worktree", "remove", "--force", str(path))
        git(repo, "worktree", "prune")
        git(repo, "branch", "-D", branch, check=False)
    elif path.exists():
        shutil.rmtree(path)


def read_folder(repo: Path, ref: str, folder: str) -> dict[str, str]:
    """The files directly in `folder` as `ref` has them: name to text."""
    names = git(repo, "ls-tree", "--name-only", ref, f"{folder.rstrip('/')}/").split("\n")
    return {Path(n).name: git(repo, "show", f"{ref}:{n}") for n in names if n}


def is_merged(cwd: Path, sha: str, upstream: str) -> bool:
    return ok(cwd, "merge-base", "--is-ancestor", sha, upstream)
