"""A sandboxed worker's private copy of the Run's files, and bringing its changes back.

Each Run gets one workspace, `data/factory/sandbox/<run>/work`, next to its trusted
worktree, which only the dispatcher writes (docs/factory-sandbox-plan.md §3.3).

- Before each attempt, `refresh` makes it match the trusted worktree again (rsync
  --delete), without `.git`, `.venv` or `node_modules`, and keeping the worker's private
  state: its database copy and caches. Whatever it changed out of scope is gone.
- After each attempt, `sync_back` compares it with the snapshot taken after the refresh
  and copies each changed file into the trusted worktree, by content, only if it is in
  the stage's `writes` and is an ordinary file. Everything else is refused, and listed
  for the diff-scope gate.
"""

from __future__ import annotations

import fnmatch
import os
import shutil
import stat
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from pdf_extract.factory import git
from pdf_extract.factory.backup import copy_database
from pdf_extract.factory.sandbox import SandboxError
from pdf_extract.factory.stages import in_scope

# Never copied in, never looked at, never brought back.
EXCLUDED = (".git", ".venv", "node_modules/", "/data/factory/")
# The worker's own between attempts: copied in once, then kept; never brought back.
PRIVATE = ("/data/*.db", "/data/*.db-*", "/data/bulletins/", "/data/seed-work/",
           "/data/pipeline/", "/data/out/", "/data/runs/", "/.cache/", "__pycache__/",
           ".pytest_cache/", ".ruff_cache/")
# Mounted read-only in the container: workers can't change their tools, prompts or hooks.
READ_ONLY = ("src", ".claude", "factory", "scripts", "pyproject.toml", "package.json",
             "uv.lock", "pnpm-lock.yaml", "pnpm-workspace.yaml")

MAX_FILE_BYTES = 50 * 1024 * 1024
MAX_FILES = 2000
MAX_TOTAL_BYTES = 500 * 1024 * 1024

# How each entry looked: kind, size, mtime, ctime and inode. A worker can set a file's
# mtime back, but not its ctime, so any write shows.
Entry = tuple[str, int, int, int, int]
Snapshot = dict[str, Entry]


def _matches(rel: str, patterns: tuple[str, ...]) -> bool:
    """rsync's rules, for the patterns above: `/a/` anchored at the top, `name/` a
    directory at any depth, `/a/*.db` one path, `.git` any component."""
    parts = rel.split("/")
    for p in patterns:
        if p.startswith("/"):
            body = p[1:]
            if body.endswith("/"):
                if rel.startswith(body) or rel + "/" == body:
                    return True
            elif fnmatch.fnmatchcase(rel, body):
                return True
        elif p.endswith("/"):
            if p[:-1] in parts[:-1] or (p[:-1] == parts[-1]):
                return True
        elif p in parts:
            return True
    return False


def skipped(rel: str) -> bool:
    return _matches(rel, EXCLUDED + PRIVATE)


def workspace(sandbox_dir: Path, run_id: str) -> Path:
    return (sandbox_dir / run_id / "work").resolve()


def refresh(trusted: Path, work: Path) -> Snapshot:
    """Make `work` match `trusted` (private state aside); the snapshot to compare with."""
    work.mkdir(parents=True, exist_ok=True)
    excludes = [f"--exclude={p}" for p in EXCLUDED + PRIVATE]
    try:
        proc = subprocess.run(["rsync", "-a", "--delete", "--no-specials", "--no-devices",
                               *excludes, f"{trusted}/", f"{work}/"],
                              capture_output=True, text=True, timeout=1800)
    except (OSError, subprocess.SubprocessError) as exc:
        raise SandboxError(f"refreshing the workspace: {exc}") from None
    if proc.returncode != 0:
        raise SandboxError(f"refreshing the workspace: {proc.stderr.strip()[-500:]}")
    for db in (trusted / "data").glob("*.db"):  # the worker's own copy, made once
        if not (work / "data" / db.name).exists():
            copy_database(db, work / "data" / db.name)
    return snapshot(work)


def snapshot(root: Path) -> Snapshot:
    """Every entry under `root` but directories, without following links."""
    entries: Snapshot = {}
    for top, dirs, files in os.walk(root):
        base = Path(top).relative_to(root).as_posix()
        prefix = "" if base == "." else base + "/"
        keep = []
        for name in dirs:
            rel = prefix + name
            if skipped(rel):
                continue
            if os.path.islink(os.path.join(top, name)):
                files.append(name)  # a link to a directory is an entry, not walked
            else:
                keep.append(name)
        dirs[:] = keep
        for name in files:
            rel = prefix + name
            if skipped(rel):
                continue
            st = os.lstat(os.path.join(top, name))
            kind = ("file" if stat.S_ISREG(st.st_mode) else
                    "link" if stat.S_ISLNK(st.st_mode) else "special")
            if kind == "file" and st.st_nlink > 1:
                kind = "hardlink"
            entries[rel] = (kind, st.st_size, st.st_mtime_ns, st.st_ctime_ns, st.st_ino)
    return entries


@dataclass
class Sync:
    applied: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    # Refused, with why: reported by the diff-scope gate.
    rejected: list[str] = field(default_factory=list)
    # Out of scope but gitignored (a note in another job's scratch): not brought back,
    # and not a problem, as the diff-scope gate has always treated them.
    dropped: list[str] = field(default_factory=list)


def _unsafe(rel: str) -> str | None:
    parts = rel.split("/")
    if rel.startswith("/") or any(p in ("", ".", "..") for p in parts):
        return "not a plain relative path"
    if ".git" in parts:
        return ".git"
    return None


def _real_parent(trusted: Path, rel: str, create: bool) -> Path | None:
    """The trusted directory `rel` goes in, every part of it a real directory (never a
    link); None if one isn't."""
    here = trusted
    for part in rel.split("/")[:-1]:
        here = here / part
        try:
            st = os.lstat(here)
        except FileNotFoundError:
            if not create:
                return None
            here.mkdir()
            continue
        if not stat.S_ISDIR(st.st_mode):
            return None
    return here


def _read(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink > 1:
            raise OSError("not an ordinary file")
        with os.fdopen(fd, "rb") as f:
            fd = -1
            return f.read(MAX_FILE_BYTES + 1)
    finally:
        if fd != -1:
            os.close(fd)


def _same(path: Path, data: bytes) -> bool:
    try:
        st = os.lstat(path)
        return stat.S_ISREG(st.st_mode) and st.st_size == len(data) \
            and path.read_bytes() == data
    except OSError:
        return False


def _write(target: Path, data: bytes, mode: int) -> None:
    fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=".carlo-sync-")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp, mode)
        os.replace(tmp, target)  # replaces a link at `target` itself, never its target
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def sync_back(work: Path, trusted: Path, before: Snapshot, writes: list[str]) -> Sync:
    """Bring the attempt's changes in `work` into `trusted`; `writes` are filled globs."""
    after = snapshot(work)
    changed = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
    out = Sync()
    ignored = _ignored(trusted, changed)
    total = 0
    for rel in changed:
        why = _unsafe(rel)
        entry = after.get(rel)
        if why is None and not in_scope(rel, writes):
            if rel in ignored:
                out.dropped.append(rel)
                continue
            why = "outside your write boundaries"
        if why is None and entry is not None and entry[0] != "file":
            why = {"link": "a symlink", "hardlink": "a hard link"}.get(entry[0],
                                                                      "not an ordinary file")
        if why is None and len(out.applied) + len(out.deleted) >= MAX_FILES:
            why = f"more than {MAX_FILES} files changed"
        if why is None and entry is not None and entry[1] > MAX_FILE_BYTES:
            why = f"over {MAX_FILE_BYTES // 2**20} MB"
        if why is None and entry is not None and total + entry[1] > MAX_TOTAL_BYTES:
            why = f"over {MAX_TOTAL_BYTES // 2**20} MB changed in all"
        if why is None and _real_parent(trusted, rel, create=entry is not None) is None:
            if entry is None:
                continue  # deleted, and its folder isn't in the trusted worktree anyway
            why = "a folder on its path is not a real folder"
        if why is not None:
            out.rejected.append(f"{rel} ({why})")
            continue
        target = trusted / rel
        if entry is None:
            if os.path.islink(target) or os.path.isfile(target):
                target.unlink()
            out.deleted.append(rel)
            continue
        try:
            data = _read(work / rel)
        except OSError as exc:
            out.rejected.append(f"{rel} ({exc.strerror or exc})")
            continue
        if len(data) > MAX_FILE_BYTES:
            out.rejected.append(f"{rel} (over {MAX_FILE_BYTES // 2**20} MB)")
            continue
        if os.path.isdir(target) and not os.path.islink(target):
            out.rejected.append(f"{rel} (a folder in the Run's files)")
            continue
        total += len(data)
        if not _same(target, data):
            _write(target, data, os.lstat(work / rel).st_mode & 0o755 | 0o600)
        out.applied.append(rel)
    return out


def _ignored(trusted: Path, paths: list[str]) -> set[str]:
    """The paths git ignores in the trusted worktree (`git check-ignore`)."""
    if not paths or not (trusted / ".git").exists():
        return set()
    proc = subprocess.run(["git", *git.SAFE, "check-ignore", "--no-index", "--stdin", "-z"],
                          cwd=trusted, input="\0".join(paths) + "\0", capture_output=True,
                          text=True)
    return {p for p in proc.stdout.split("\0") if p}


def mounts(work: Path) -> list[tuple[Path, bool]]:
    """The workspace read-write, then its tools read-only on top."""
    return [(work, False)] + [(work / name, True) for name in READ_ONLY
                              if (work / name).exists()]


def remove(sandbox_dir: Path, run_id: str) -> None:
    """A retired Run's workspace."""
    shutil.rmtree(sandbox_dir / run_id, ignore_errors=True)
