"""Keeping the factory's workers apart from the dispatcher (docs/factory-sandbox-plan.md).

The launcher, the environments, the git safety settings and (with Podman) the container.
Everything here runs without Podman, except the tests marked `needs_podman`.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

from pdf_extract import __main__ as cli
from pdf_extract.factory import git
from pdf_extract.factory.backup import backup_ledger
from pdf_extract.factory.config import Account, FactoryError
from pdf_extract.factory.dispatcher import run_command
from pdf_extract.factory.sandbox import LAUNCHER, HostBackend, Launch
from pdf_extract.factory.secrets import check_patterns, command_env, pick
from pdf_extract.factory.stages import StageSpec, load_stage
from pdf_extract.factory.workers import WorkerRequest, sdk_options, worker_env

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / LAUNCHER

# What the dispatcher's own environment might hold: none of it may reach a worker.
DISPATCHER_SECRETS = {
    "CANARY_SECRET": "canary-1", "GH_TOKEN": "gh-real", "GITHUB_TOKEN": "gh-real",
    "R2_ACCESS_KEY_ID": "r2-real", "R2_SECRET_ACCESS_KEY": "r2-real",
    "CLOUDFLARE_API_TOKEN": "cf-real", "OPENAI_API_KEY": "oa-real",
    "SSH_AUTH_SOCK": "/tmp/ssh-agent.sock", "DISPLAY": ":99", "XDG_RUNTIME_DIR": "/run/user/1",
    "CLAUDE_CODE_OAUTH_TOKEN": "owner-token",
}


def fake_claude(tmp: Path) -> Path:
    """A stand-in CLI that prints its arguments and environment as JSON."""
    path = tmp / "claude"
    path.write_text("#!/usr/bin/env python3\nimport json, os, sys\n"
                    "print(json.dumps({'args': sys.argv[1:], 'env': dict(os.environ)}))\n")
    path.chmod(0o755)
    return path


def run_launcher(launch: Launch, args: list[str], extra: dict[str, str] | None = None,
                 ) -> dict:
    """The launcher as the SDK starts it: the dispatcher's environment, then options.env."""
    env = {**os.environ, **DISPATCHER_SECRETS, **(extra or {}),
           "CLAUDE_CODE_ENTRYPOINT": "sdk-py", **launch.env, "CLAUDE_AGENT_SDK_VERSION": "x"}
    out = subprocess.run([launch.cli_path, *args], env=env, capture_output=True, text=True,
                         check=True)
    return json.loads(out.stdout)


def request(tmp: Path, **kw) -> WorkerRequest:
    spec = StageSpec(stage="map", kind="agent", prompt="p.md", tools=["Bash"])
    return WorkerRequest(job_id=1, run_id="r", job_name="001-map", stage="map", spec=spec,
                         worktree=tmp, account=Account("a", tmp / ".claude_a"), prompt="go",
                         system_append="", values={}, **kw)


# ── Phase 0: the host launcher and clean environments ─────────────────────────
def test_the_host_launcher_passes_only_the_workers_environment(tmp_path: Path) -> None:
    backend = HostBackend(BOX, claude=str(fake_claude(tmp_path)), xvfb="")
    secrets = {"GEMINI_API_KEY": "stage-key"}
    launch = backend.launch(request(tmp_path), worker_env(Account("a", tmp_path / "a"), secrets))
    got = run_launcher(launch, ["--output-format", "stream-json"])
    assert got["args"] == ["--output-format", "stream-json"]
    env = got["env"]
    for name, value in DISPATCHER_SECRETS.items():
        assert env.get(name) in (None, ""), name
        assert value not in env.values()
    assert env["GEMINI_API_KEY"] == "stage-key"
    assert env["CLAUDE_CONFIG_DIR"] == str(tmp_path / "a")
    assert env["CARLO_NO_DOTENV"] == "1" and env["CLAUDE_CODE_ENTRYPOINT"] == "sdk-py"
    assert env["PATH"] == os.environ["PATH"]
    assert "CARLO_BOX" not in env


def test_the_host_launcher_runs_the_cli_under_a_private_xvfb(tmp_path: Path) -> None:
    xvfb = tmp_path / "xvfb-run"
    xvfb.write_text("#!/bin/sh\nshift\nDISPLAY=:7 exec \"$@\"\n")
    xvfb.chmod(0o755)
    backend = HostBackend(BOX, claude=str(fake_claude(tmp_path)), xvfb=str(xvfb))
    got = run_launcher(backend.launch(request(tmp_path), worker_env(None)), [])
    assert got["env"]["DISPLAY"] == ":7"  # its own, not the dispatcher's :99


def test_the_launcher_refuses_to_run_without_a_plan(tmp_path: Path) -> None:
    proc = subprocess.run([str(BOX), "--print"], capture_output=True, text=True,
                          env={"PATH": os.environ["PATH"]})
    assert proc.returncode == 2 and "CARLO_BOX" in proc.stderr


def test_sigterm_stops_everything_the_worker_started(tmp_path: Path) -> None:
    pids = tmp_path / "pids"
    cli_ = tmp_path / "claude"
    # The CLI starts a child that ignores SIGTERM (as a stuck browser might), then waits.
    cli_.write_text(f"""#!/bin/sh
sh -c 'trap "" TERM; echo $$ >> {pids}; while :; do sleep 1; done' &
echo $$ >> {pids}
wait
""")
    cli_.chmod(0o755)
    launch = HostBackend(BOX, claude=str(cli_), xvfb="").launch(request(tmp_path), {})
    env = {**os.environ, **launch.env}
    proc = subprocess.Popen([launch.cli_path], env=env)
    for _ in range(100):
        if pids.exists() and len(pids.read_text().split()) == 2:
            break
        time.sleep(0.05)
    started = [int(p) for p in pids.read_text().split()]
    proc.send_signal(signal.SIGTERM)
    assert proc.wait(20) == 128 + signal.SIGTERM
    time.sleep(0.2)
    for pid in started:
        with pytest.raises(ProcessLookupError):
            os.kill(pid, 0)


def test_sdk_options_never_run_tools_in_the_dispatcher(tmp_path: Path) -> None:
    pytest.importorskip("claude_agent_sdk")
    req = request(tmp_path, secrets={"R2_ACCESS_KEY_ID": "k"})
    launch = HostBackend(BOX, claude="claude", xvfb="").launch(
        req, worker_env(req.account, req.secrets))
    options = sdk_options(req, launch)
    # §3.1: the SDK in the dispatcher only reads the CLI's messages. A hook, a permission
    # callback or an in-process MCP server would run here, outside the worker's box.
    assert not options.hooks
    assert options.can_use_tool is None
    assert not options.mcp_servers
    assert options.cli_path == str(BOX)
    assert "CARLO_BOX" in options.env and options.env["R2_ACCESS_KEY_ID"] == "k"


def test_factory_does_not_load_dotenv_into_its_environment(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("CANARY_FROM_DOTENV=leaked\n")
    monkeypatch.delenv("CANARY_FROM_DOTENV", raising=False)
    monkeypatch.delenv("CARLO_NO_DOTENV", raising=False)
    assert cli.main(["factory", "status", "--stub"]) == 0
    assert "CANARY_FROM_DOTENV" not in os.environ
    # Other commands still read it, unless the dispatcher said not to.
    cli._load_dotenv()
    assert os.environ.pop("CANARY_FROM_DOTENV") == "leaked"
    monkeypatch.setenv("CARLO_NO_DOTENV", "1")
    cli._load_dotenv()
    assert "CANARY_FROM_DOTENV" not in os.environ


def test_gate_commands_get_a_scrubbed_environment(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for name, value in DISPATCHER_SECRETS.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setenv("CARLO_REMOTE_WRITE", "1")
    ok, out = run_command(f"{sys.executable} -c 'import json,os;print(json.dumps(dict(os.environ)))'",
                          tmp_path, {"R2_ACCESS_KEY_ID": "gate-key"})
    assert ok
    env = json.loads(out)
    for name in DISPATCHER_SECRETS:
        if name != "XDG_RUNTIME_DIR":
            assert name not in env or name == "R2_ACCESS_KEY_ID", name
    assert env["R2_ACCESS_KEY_ID"] == "gate-key"
    assert "CARLO_REMOTE_WRITE" not in env and env["CARLO_NO_DOTENV"] == "1"
    assert command_env()["PATH"] == os.environ["PATH"]


def test_stage_secrets_never_pass_publishing_or_login_keys() -> None:
    secrets = {"R2_ACCESS_KEY_ID": "a", "CLOUDFLARE_API_TOKEN": "b", "GH_TOKEN": "c"}
    assert pick(secrets, ["R2_*", "CLOUDFLARE_*", "GH_TOKEN"]) == {"R2_ACCESS_KEY_ID": "a"}
    for bad in (["*_TOKEN"], ["CLOUDFLARE_API_TOKEN"], ["SSH_AUTH_SOCK"], ["*"]):
        with pytest.raises(FactoryError):
            check_patterns(bad, "spec")
    check_patterns(["R2_*", "GEMINI_API_KEY", "OPENAI_API_KEY"], "spec")
    seed = load_stage("seed", ROOT)
    assert seed.secrets == ["R2_*", "GEMINI_API_KEY", "OPENAI_API_KEY"]
    assert seed.gate_secrets == ["R2_*"]
    for stage in ("survey", "survey-review", "map", "reconcile", "integrate"):
        assert load_stage(stage, ROOT).secrets == []


def test_the_backup_reads_r2_keys_from_the_dotenv_dict_only(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import sqlite3

    db = tmp_path / "ledger.db"
    sqlite3.connect(db).close()
    monkeypatch.setenv("R2_ACCESS_KEY_ID", "env-key")
    monkeypatch.setenv("R2_SECRET_ACCESS_KEY", "env-secret")
    monkeypatch.setenv("R2_ACCOUNT_ID", "acct")
    out = backup_ledger(db, "factory/backups/", {}, out_dir=tmp_path / "b")
    assert "not uploaded" in out


def test_dispatcher_git_runs_no_hooks_or_fsmonitor(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    ran = tmp_path / "ran"
    hook = repo / ".git" / "hooks" / "post-commit"
    hook.write_text(f"#!/bin/sh\necho hook >> {ran}\n")
    hook.chmod(0o755)
    monitor = tmp_path / "monitor"
    monitor.write_text(f"#!/bin/sh\necho fsmonitor >> {ran}\n")
    monitor.chmod(0o755)
    subprocess.run(["git", "config", "core.fsmonitor", str(monitor)], cwd=repo, check=True)
    (repo / "a.txt").write_text("a")
    for name in ("GIT_AUTHOR", "GIT_COMMITTER"):
        monkeypatch.setenv(f"{name}_NAME", "t")
        monkeypatch.setenv(f"{name}_EMAIL", "t@example.com")
    assert git.changed_paths(repo) == ["a.txt"]
    git.git(repo, "add", "-A")
    git.git(repo, "commit", "-qm", "x")  # no --no-verify: hooksPath alone stops it
    assert not ran.exists()


# ── Phase 2: the Podman backend, without Podman ───────────────────────────────
class FakePodman:
    """Answers the backend's podman calls; `fail` makes a subcommand fail."""

    def __init__(self, *, have_image: bool = True, proxy_running: bool = True,
                 fail: tuple[str, ...] = ()) -> None:
        self.calls: list[tuple[str, ...]] = []
        self.have_image, self.proxy_running, self.fail = have_image, proxy_running, fail

    def __call__(self, *args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
        self.calls.append(args)
        out, code = "", 0
        if args[0] in self.fail or " ".join(args[:2]) in self.fail:
            code = 1
        elif args[:2] == ("image", "exists"):
            code = 0 if self.have_image else 1
        elif args[:2] == ("network", "exists"):
            code = 1
        elif args[:2] == ("container", "inspect"):
            out = "true" if self.proxy_running else "false"
        elif args[0] == "ps":
            out = "aaa\nbbb\n"
        return subprocess.CompletedProcess(args, code, out, "failed" if code else "")


def main_repo(tmp: Path) -> Path:
    repo = tmp / "main"
    (repo / "factory" / "sandbox").mkdir(parents=True)
    (repo / "factory" / "sandbox" / "Containerfile").write_text("FROM scratch\n")
    (repo / "pyproject.toml").write_text("[project]\n")
    (repo / "uv.lock").write_text("lock\n")
    for args in (["init", "-q", "-b", "main"], ["add", "-A"],
                 ["-c", "user.name=t", "-c", "user.email=t@x", "commit", "-qm", "x"]):
        subprocess.run(["git", *args], cwd=repo, check=True)
    return repo


def podman_backend(tmp: Path, fake: FakePodman, podman: str = "/usr/bin/podman"):
    from pdf_extract.factory.sandbox import PodmanBackend

    return PodmanBackend(main_repo(tmp), "main", launcher=BOX, podman=podman, call=fake,
                         sandbox_dir=tmp / "sandbox", sessions_dir=tmp / "sessions")


def boxed_request(tmp: Path, worktree: Path, **kw) -> WorkerRequest:
    """A request whose account has a `claude setup-token` token, as sandboxed ones need."""
    token = tmp / "token"
    token.write_text("worker-token\n")
    req = request(worktree, **kw)
    req.account = Account("a", tmp / ".claude_a", worker_token_file=token)
    return req


def test_the_container_is_locked_down(tmp_path: Path) -> None:
    from pdf_extract.factory.sandbox import NETWORK, PROXY_URL

    fake = FakePodman()
    wt = tmp_path / "wt"
    (wt / ".git").mkdir(parents=True)
    (wt / "src").mkdir()
    (wt / "data").mkdir()
    req = boxed_request(tmp_path, wt, attempt_id=42, secrets={"OPENAI_API_KEY": "stage-secret"})
    launch = podman_backend(tmp_path, fake).launch(req, worker_env(req.account, req.secrets))
    work = (tmp_path / "sandbox" / "r" / "work").resolve()
    sessions = (tmp_path / "sessions" / "r").resolve()
    assert launch.work == work and launch.trusted == wt.resolve()
    assert launch.sessions == sessions and sessions.is_dir()
    argv = json.loads(launch.env["CARLO_BOX"])["argv"]
    joined = " ".join(argv)
    assert launch.container == "carlo-job-42"
    for flag in ("--rm", "-i", "--init", "--cap-drop=ALL", "no-new-privileges", "--read-only",
                 "--ipc=private", "--pid=private", "--userns=keep-id:uid=1000,gid=1000",
                 "--label carlo.factory=1", f"--network {NETWORK}", "--pids-limit 2048",
                 "--memory 6g", f"--workdir {work}", "--shm-size 1g",
                 "--tmpfs /home/worker/.claude:rw,mode=1777"):
        assert flag in joined, flag
    assert "--privileged" not in joined and "host" not in argv
    # The private copy, without .git, its tools read-only on top; never the Run's worktree.
    volumes = [argv[i + 1] for i, a in enumerate(argv) if a == "--volume"]
    assert volumes == [f"{work}:{work}:rw", f"{work / 'src'}:{work / 'src'}:ro",
                       f"{sessions}:/home/worker/.claude/projects:rw"]
    assert not (work / ".git").exists() and str(wt.resolve()) not in joined
    # Secrets go by name, their values from podman's environment, never on its command line.
    assert "stage-secret" not in joined and "--env OPENAI_API_KEY" in joined
    assert "worker-token" not in joined and "--env CLAUDE_CODE_OAUTH_TOKEN" in joined
    assert launch.env["CLAUDE_CODE_OAUTH_TOKEN"] == "worker-token"
    assert f"--env HTTPS_PROXY={PROXY_URL}" in joined
    assert f"--env PYTHONPATH={work / 'src'}" in joined
    for name in ("CLAUDE_CONFIG_DIR", "DISPLAY", "SSH_AUTH_SOCK", "GH_CONFIG_DIR"):
        assert f"--env {name}" not in joined
    assert argv[-3:] == ["xvfb-run", "-a", "claude"]
    assert ("rm", "--force", "carlo-job-42") in fake.calls  # a leftover goes first


def test_the_sandbox_launcher_gives_podman_only_what_it_names(tmp_path: Path) -> None:
    fake_podman = tmp_path / "podman"
    fake_podman.write_text("#!/usr/bin/env python3\nimport json, os, sys\n"
                           "print(json.dumps({'args': sys.argv[1:], 'env': dict(os.environ)}))\n")
    fake_podman.chmod(0o755)
    (tmp_path / "wt").mkdir()
    req = boxed_request(tmp_path, tmp_path / "wt", attempt_id=7,
                        secrets={"GEMINI_API_KEY": "stage-key"})
    backend = podman_backend(tmp_path, FakePodman(), podman=str(fake_podman))
    got = run_launcher(backend.launch(req, worker_env(req.account, req.secrets)),
                       ["--verbose"])
    assert got["args"][0] == "run" and got["args"][-1] == "--verbose"
    env = got["env"]
    assert env["GEMINI_API_KEY"] == "stage-key"
    assert env["CLAUDE_CODE_OAUTH_TOKEN"] == "worker-token"  # the account's, not the owner's
    assert env["XDG_RUNTIME_DIR"] == "/run/user/1"  # podman's own, not passed in (no --env)
    assert "--env XDG_RUNTIME_DIR" not in " ".join(got["args"])
    for name in ("CANARY_SECRET", "GH_TOKEN", "R2_ACCESS_KEY_ID", "CLOUDFLARE_API_TOKEN",
                 "SSH_AUTH_SOCK", "DISPLAY", "CLAUDE_CONFIG_DIR"):
        assert env.get(name) in (None, ""), name


@pytest.mark.parametrize(("fake", "podman", "says"), [
    (FakePodman(), "", "podman is not installed"),
    (FakePodman(have_image=False, fail=("build",)), "/usr/bin/podman", "podman build"),
    (FakePodman(fail=("network create",)), "/usr/bin/podman", "podman network create"),
    (FakePodman(proxy_running=False, fail=("run",)), "/usr/bin/podman", "podman run"),
])
def test_a_sandbox_that_cant_start_fails_closed(tmp_path: Path, fake: FakePodman, podman: str,
                                                says: str) -> None:
    from pdf_extract.factory.sandbox import SandboxError

    with pytest.raises(SandboxError, match=says):
        podman_backend(tmp_path, fake, podman=podman).launch(request(tmp_path), {})


def test_a_sandboxed_worker_needs_its_accounts_token(tmp_path: Path) -> None:
    from pdf_extract.factory.sandbox import SandboxError

    (tmp_path / "wt").mkdir()
    backend = podman_backend(tmp_path, FakePodman())
    with pytest.raises(SandboxError, match="no worker_token_file"):
        backend.launch(request(tmp_path / "wt"), {})
    req = boxed_request(tmp_path, tmp_path / "wt")
    (tmp_path / "token").write_text("\n")
    with pytest.raises(SandboxError, match="empty"):
        backend.launch(req, {})


def test_local_yaml_names_each_accounts_worker_token(tmp_path: Path) -> None:
    from pdf_extract.factory.config import load_config

    local = tmp_path / "local.yaml"
    local.write_text("accounts:\n  - {name: a, config_dir: ~/.claude}\n"
                     "  - {name: b, config_dir: ~/.claude_2, worker_token_file: ~/.t/b}\n"
                     "sandbox_cpus: 4\n")
    config = load_config(tmp_path / "none.yaml", local)
    assert config.sandbox_cpus == "4"
    a, b = config.accounts
    assert a.worker_token_file is None
    assert b.worker_token_file == Path.home() / ".t" / "b"


def test_a_sandboxed_transcript_is_found_in_its_session_folder(tmp_path: Path) -> None:
    from pdf_extract.factory.workers import find_transcript

    (tmp_path / "sessions" / "-work").mkdir(parents=True)
    (tmp_path / "sessions" / "-work" / "s1.jsonl").write_text("{}")
    account = Account("a", tmp_path / ".claude_a")
    assert find_transcript(account, "s1", tmp_path / "sessions") == \
        tmp_path / "sessions" / "-work" / "s1.jsonl"
    assert find_transcript(account, "s1") is None


def test_the_image_is_built_from_mains_files_and_tagged_by_their_hash(tmp_path: Path) -> None:
    from pdf_extract.factory.sandbox import image_tag, main_files

    fake = FakePodman(have_image=False)
    backend = podman_backend(tmp_path, fake)
    (backend.repo / "uv.lock").write_text("a worker's edit\n")  # not committed to main
    tag = backend.image()
    assert tag == image_tag(main_files(backend.repo, "main"))
    assert main_files(backend.repo, "main")["uv.lock"] == b"lock\n"
    build = next(c for c in fake.calls if c[0] == "build")
    assert tag in build and "--file" in build
    assert backend.image() == tag and sum(c[0] == "build" for c in fake.calls) == 1
    assert image_tag({"a": b"1"}) != image_tag({"a": b"2"})


def test_the_proxy_refuses_private_and_host_addresses(tmp_path: Path) -> None:
    from pdf_extract.factory.sandbox import NETWORK, PROXY, proxy_argv

    argv = proxy_argv(["172.20.0.5"])
    joined = " ".join(argv)
    for cidr in ("10.0.0.0/8", "127.0.0.0/8", "169.254.0.0/16", "172.16.0.0/12",
                 "192.168.0.0/16", "100.64.0.0/10", "fc00::/7", "fe80::/10", "::1/128"):
        assert f"--deny-range {cidr}" in joined
    assert "--deny-address 172.20.0.5" in joined
    assert f"--name {PROXY}" in joined and f"--network {NETWORK}" in joined
    assert "--unsafe-allow-private-ranges" not in joined
    fake = FakePodman(proxy_running=False)
    podman_backend(tmp_path, fake).proxy()
    assert ("rm", "--force", PROXY) in fake.calls and any(c[0] == "run" for c in fake.calls)


def test_restart_cleanup_removes_every_labelled_container(tmp_path: Path) -> None:
    fake = FakePodman()
    podman_backend(tmp_path, fake).cleanup()
    assert ("ps", "--all", "--quiet", "--filter", "label=carlo.factory=1") in fake.calls
    assert ("rm", "--force", "--time", "0", "aaa", "bbb") in fake.calls


def test_a_sandbox_failure_never_starts_the_worker_on_the_host(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from pdf_extract.factory import workers
    from pdf_extract.factory.sandbox import SandboxError

    class Broken:
        name = "sandbox"

        def launch(self, request, env):
            raise SandboxError("podman is not installed")

        def finish(self, launch):
            raise AssertionError("nothing was launched")

        def cleanup(self):
            pass

    async def never(*args, **kw):
        raise AssertionError("the SDK must not start")

    worker = workers.SdkWorker(Broken())
    monkeypatch.setattr(worker, "_run", never)
    result = worker.run(request(tmp_path))
    assert result.outcome == workers.SANDBOX and "podman" in result.error


def test_chrome_gets_the_proxy_only_when_one_is_set(monkeypatch: pytest.MonkeyPatch) -> None:
    pytest.importorskip("playwright_stealth")
    from pdf_extract.browser import proxy_from_env

    for name in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "NO_PROXY",
                 "no_proxy"):
        monkeypatch.delenv(name, raising=False)
    assert proxy_from_env() is None
    monkeypatch.setenv("HTTPS_PROXY", "http://carlo-egress:4750")
    monkeypatch.setenv("NO_PROXY", "localhost")
    assert proxy_from_env() == {"server": "http://carlo-egress:4750", "bypass": "localhost"}
    monkeypatch.setenv("HTTPS_PROXY", "http://u%40x:p@proxy:8080")
    assert proxy_from_env() == {"server": "http://proxy:8080", "username": "u@x",
                                "password": "p", "bypass": "localhost"}


# ── Phase 3: the private workspace and bringing changes back ──────────────────
WRITES = ["data/dioceses/d/**", "scratch/r/**"]


def trusted_tree(tmp: Path) -> Path:
    """A Run worktree as the dispatcher has it: a git checkout with a database copy."""
    import sqlite3

    wt = tmp / "wt"
    (wt / "data" / "dioceses" / "d").mkdir(parents=True)
    (wt / "src").mkdir()
    (wt / "src" / "tool.py").write_text("print('tool')\n")
    (wt / "data" / "dioceses" / "d" / "a.md").write_text("a\n")
    (wt / "data" / "parishes.csv").write_text("slug\n")
    (wt / ".gitignore").write_text(".venv/\n*.db\nscratch/\n.env\n")
    (wt / ".venv").mkdir()
    sqlite3.connect(wt / "data" / "parish_events.db").close()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=wt, check=True)
    return wt


def fresh(tmp: Path) -> tuple[Path, Path, dict]:
    from pdf_extract.factory import workspace

    wt = trusted_tree(tmp)
    work = workspace.workspace(tmp / "sandbox", "r")
    return wt, work, workspace.refresh(wt, work)


def test_the_workspace_is_a_copy_without_git_or_the_venv(tmp_path: Path) -> None:
    from pdf_extract.factory import workspace

    wt, work, _ = fresh(tmp_path)
    assert (work / "data" / "dioceses" / "d" / "a.md").read_text() == "a\n"
    assert not (work / ".git").exists() and not (work / ".venv").exists()
    assert (work / "data" / "parish_events.db").exists()  # its own copy
    # Out of scope last time: gone. Private state (the database, caches): kept.
    (work / "data" / "parishes.csv").write_text("sneaky\n")
    (work / "data" / "parish_events.db").write_bytes(b"worker's")
    (work / ".cache").mkdir()
    (work / ".cache" / "x").write_text("cached")
    workspace.refresh(wt, work)
    assert (work / "data" / "parishes.csv").read_text() == "slug\n"
    assert (work / "data" / "parish_events.db").read_bytes() == b"worker's"
    assert (work / ".cache" / "x").read_text() == "cached"
    assert [p for p, ro in workspace.mounts(work) if ro] == [work / "src"]


def test_in_scope_changes_come_back_and_the_rest_is_refused(tmp_path: Path) -> None:
    from pdf_extract.factory import workspace

    wt, work, before = fresh(tmp_path)
    d = work / "data" / "dioceses" / "d"
    (d / "a.md").write_text("edited\n")
    (d / "new" / "b.md").parent.mkdir()
    (d / "new" / "b.md").write_text("b\n")
    (work / "scratch" / "r" / "001-map").mkdir(parents=True)
    (work / "scratch" / "r" / "001-map" / "handoff.json").write_text("{}")
    (work / "data" / "parishes.csv").write_text("sneaky\n")  # out of scope
    (work / "src" / "tool.py").write_text("evil\n")  # out of scope (read-only in the box)
    (work / ".env").write_text("CARLO_REMOTE_WRITE=1\n")  # out of scope and gitignored
    (d / "link.md").symlink_to("/etc/passwd")
    (d / "escape").symlink_to("/etc")
    os.link(d / "a.md", d / "hard.md")
    os.mkfifo(d / "pipe")
    sync = workspace.sync_back(work, wt, before, WRITES)
    assert sorted(sync.applied) == ["data/dioceses/d/new/b.md",
                                    "scratch/r/001-map/handoff.json"]
    refused = " ".join(sync.rejected)
    for path, why in (("data/parishes.csv", "outside your write boundaries"),
                      ("src/tool.py", "outside"), ("link.md", "a symlink"),
                      ("escape", "a symlink"), ("hard.md", "a hard link"),
                      ("pipe", "not an ordinary file"), ("a.md", "a hard link")):
        assert path in refused and why in refused, path
    assert sync.dropped == [".env"]
    assert (wt / "data" / "dioceses" / "d" / "new" / "b.md").read_text() == "b\n"
    assert (wt / "data" / "parishes.csv").read_text() == "slug\n"
    assert (wt / "src" / "tool.py").read_text() == "print('tool')\n"
    assert not (wt / ".env").exists()
    for name in ("link.md", "escape", "hard.md", "pipe"):
        assert not os.path.lexists(wt / "data" / "dioceses" / "d" / name)


def test_sync_back_deletes_and_catches_a_backdated_edit(tmp_path: Path) -> None:
    from pdf_extract.factory import workspace

    wt, work, before = fresh(tmp_path)
    (wt / "data" / "dioceses" / "d" / "gone.md").write_text("x\n")
    before = workspace.refresh(wt, work)
    (work / "data" / "dioceses" / "d" / "gone.md").unlink()
    a = work / "data" / "dioceses" / "d" / "a.md"
    st = a.stat()
    a.write_text("b\n")  # same size, then its mtime set back
    os.utime(a, ns=(st.st_atime_ns, st.st_mtime_ns))
    sync = workspace.sync_back(work, wt, before, WRITES)
    assert sync.deleted == ["data/dioceses/d/gone.md"]
    assert sync.applied == ["data/dioceses/d/a.md"]
    assert (wt / "data" / "dioceses" / "d" / "a.md").read_text() == "b\n"
    assert not (wt / "data" / "dioceses" / "d" / "gone.md").exists()


def test_sync_back_never_writes_through_a_link_in_the_run_worktree(tmp_path: Path) -> None:
    from pdf_extract.factory import workspace

    wt, work, before = fresh(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (wt / "data" / "dioceses" / "d" / "via").symlink_to(outside)
    (work / "data" / "dioceses" / "d" / "via").mkdir()  # a real folder in the workspace
    (work / "data" / "dioceses" / "d" / "via" / "x.md").write_text("x\n")
    sync = workspace.sync_back(work, wt, before, WRITES)
    assert any("via/x.md" in r and "not a real folder" in r for r in sync.rejected)
    assert list(outside.iterdir()) == []


def test_sync_back_caps_size_and_count(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from pdf_extract.factory import workspace

    monkeypatch.setattr(workspace, "MAX_FILE_BYTES", 10)
    monkeypatch.setattr(workspace, "MAX_FILES", 2)
    wt, work, before = fresh(tmp_path)
    d = work / "data" / "dioceses" / "d"
    (d / "big.md").write_text("x" * 11)
    for n in range(3):
        (d / f"n{n}.md").write_text("n\n")
    sync = workspace.sync_back(work, wt, before, WRITES)
    assert any("big.md" in r and "over" in r for r in sync.rejected)
    assert len(sync.applied) == 2
    assert any("more than 2 files" in r for r in sync.rejected)
    assert not (wt / "data" / "dioceses" / "d" / "big.md").exists()


def test_unsafe_paths_are_refused() -> None:
    from pdf_extract.factory.workspace import _unsafe

    for rel in ("../x", "a/../b", "/etc/passwd", "a//b", "a/./b", ".git/config",
                "data/.git/hooks/post-commit"):
        assert _unsafe(rel), rel
    assert _unsafe("data/dioceses/d/a.md") is None


def test_a_sandboxed_attempt_brings_back_its_changes_or_ends_as_sandbox(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from pdf_extract.factory import workers
    from pdf_extract.factory.sandbox import SandboxError

    class Box:
        name = "sandbox"

        def __init__(self, fail: bool) -> None:
            self.fail = fail

        def launch(self, request, env):
            return Launch("claude", env, container="c", work=tmp_path / "work")

        def finish(self, launch):
            if self.fail:
                raise SandboxError("couldn't remove c")
            return ["data/x (a symlink)"]

        def cleanup(self):
            pass

    async def ran(request, launch):
        return workers.WorkerResult(workers.OK, cost_usd=1.5)

    for fail, outcome in ((False, workers.OK), (True, workers.SANDBOX)):
        worker = workers.SdkWorker(Box(fail))
        monkeypatch.setattr(worker, "_run", ran)
        result = worker.run(request(tmp_path))
        assert result.outcome == outcome
        assert result.refused == ([] if fail else ["data/x (a symlink)"])
    pytest.importorskip("claude_agent_sdk")
    options = workers.sdk_options(request(tmp_path),
                                  Launch("claude", {}, work=tmp_path / "work"))
    assert options.cwd == str(tmp_path / "work")  # the copy, not the Run's worktree


# ── Phase 4: standalone clones ────────────────────────────────────────────────
def sh_git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout


def owner_checkout(tmp: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An `origin` and a checkout of it, like the owner's (or the dispatcher's)."""
    for name in ("GIT_AUTHOR", "GIT_COMMITTER"):
        monkeypatch.setenv(f"{name}_NAME", "t")
        monkeypatch.setenv(f"{name}_EMAIL", "t@example.com")
    sh_git(tmp, "init", "-q", "--bare", "-b", "main", "origin.git")
    repo = tmp / "repo"
    repo.mkdir()
    sh_git(repo, "init", "-q", "-b", "main")
    (repo / ".gitignore").write_text("*.db\n")
    (repo / "a.txt").write_text("a\n")
    sh_git(repo, "add", "-A")
    sh_git(repo, "commit", "-qm", "init")
    sh_git(repo, "remote", "add", "origin", str(tmp / "origin.git"))
    sh_git(repo, "push", "-q", "-u", "origin", "main")
    return repo


def test_a_new_run_checkout_shares_nothing_with_the_dispatchers(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = owner_checkout(tmp_path, monkeypatch)
    path = tmp_path / "wt" / "run-1"
    assert git.ensure_worktree(repo, path, "factory/run-1", remote="origin", base="origin/main")
    assert (path / ".git").is_dir()
    assert not (path / ".git" / "objects" / "info" / "alternates").exists()
    assert sh_git(path, "branch", "--show-current").strip() == "factory/run-1"
    assert (path / "a.txt").read_text() == "a\n"
    assert len(sh_git(repo, "worktree", "list").splitlines()) == 1
    assert not git.ensure_worktree(repo, path, "factory/run-1", remote="origin",
                                   base="origin/main")
    # Lost with the machine: the pushed branch is checked out again.
    (path / "b.txt").write_text("b\n")
    sh_git(path, "add", "-A")
    sh_git(path, "commit", "-qm", "b")
    git.push(path, "origin", "factory/run-1")
    git.remove_worktree(repo, path, "factory/run-1")
    assert not path.exists()
    git.ensure_worktree(repo, path, "factory/run-1", remote="origin", base="origin/main")
    assert (path / "b.txt").read_text() == "b\n"
    # worktrees_dir is relative to the dispatcher's checkout by default.
    monkeypatch.chdir(repo)
    rel = Path("data") / "factory" / "worktrees" / "run-2"
    git.ensure_worktree(repo, rel, "factory/run-2", remote="origin", base="origin/main")
    assert (repo / rel / "a.txt").exists()
    assert sh_git(repo / rel, "branch", "--show-current").strip() == "factory/run-2"


def test_a_linked_worktree_becomes_a_standalone_clone_in_place(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = owner_checkout(tmp_path, monkeypatch)
    path = tmp_path / "wt" / "run-1"
    sh_git(repo, "worktree", "add", "-q", "--no-track", "-b", "factory/run-1", str(path),
           "origin/main")
    (path / "b.txt").write_text("b\n")
    sh_git(path, "add", "-A")
    sh_git(path, "commit", "-qm", "not pushed yet")
    sha = sh_git(path, "rev-parse", "HEAD").strip()
    (path / "data.db").write_text("ignored, kept")
    (path / "wip.txt").write_text("uncommitted, kept")
    assert git.is_linked(path)
    git.make_standalone(path, "origin")
    assert not git.is_linked(path) and (path / ".git").is_dir()
    assert not (path / ".git" / "objects" / "info" / "alternates").exists()
    assert sh_git(path, "branch", "--show-current").strip() == "factory/run-1"
    assert sh_git(path, "rev-parse", "HEAD").strip() == sha
    assert sh_git(path, "status", "--porcelain").split() == ["??", "wip.txt"]
    assert (path / "data.db").read_text() == "ignored, kept"
    assert sh_git(path, "remote", "get-url", "origin").strip() == str(tmp_path / "origin.git")
    assert len(sh_git(repo, "worktree", "list").splitlines()) == 1
    git.make_standalone(path, "origin")  # already one: nothing to do
    git.remove_worktree(repo, path, "factory/run-1")
    assert not path.exists()


def test_factory_clones_lists_then_converts_linked_checkouts(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    repo = owner_checkout(tmp_path, monkeypatch)
    dispatcher = tmp_path / "carlo-factory"
    sh_git(repo, "worktree", "add", "-q", "--detach", str(dispatcher), "origin/main")
    monkeypatch.chdir(dispatcher)
    assert cli.main(["factory", "clones", "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == {"linked": [str(dispatcher)],
                                                   "converted": False}
    assert git.is_linked(dispatcher)
    assert cli.main(["factory", "clones", "--apply", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["converted"] is True
    assert not git.is_linked(dispatcher)
    assert len(sh_git(repo, "worktree", "list").splitlines()) == 1


def test_a_linked_run_worktree_from_before_is_still_removed(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = owner_checkout(tmp_path, monkeypatch)
    path = tmp_path / "wt" / "old"
    sh_git(repo, "worktree", "add", "-q", "-b", "factory/old", str(path), "origin/main")
    assert not git.ensure_worktree(repo, path, "factory/old", remote="origin",
                                   base="origin/main")
    git.remove_worktree(repo, path, "factory/old")
    assert not path.exists() and not sh_git(repo, "branch", "--list", "factory/old").strip()


# ── With Podman: the real launcher and container (skipped without Podman) ─────
needs_podman = pytest.mark.skipif(not shutil.which("podman"),
                                  reason="needs Podman (sudo apt install podman)")
TEST_IMAGE = "docker.io/library/alpine:3.20"  # sh and wget are enough to probe the box
CANARIES = {k: v for k, v in DISPATCHER_SECRETS.items() if k != "XDG_RUNTIME_DIR"}


def box_command(tmp: Path, script: str, *, secrets: dict[str, str] | None = None,
                read_only: tuple[str, ...] = (".git",)) -> tuple[list[str], dict[str, str], str]:
    """The launcher command and environment for `script` in a worker container."""
    from pdf_extract.factory.sandbox import (
        PODMAN_PASS,
        Box,
        Mount,
        PodmanBackend,
        container_env,
        plan_env,
        run_argv,
    )

    wt = (tmp / "wt").resolve()
    wt.mkdir(parents=True, exist_ok=True)
    for name in read_only:
        (wt / name).mkdir(exist_ok=True)
    backend = PodmanBackend(ROOT, "HEAD", launcher=BOX)
    backend.network()
    backend.proxy()
    if subprocess.run(["podman", "image", "exists", TEST_IMAGE]).returncode != 0:
        subprocess.run(["podman", "pull", "-q", TEST_IMAGE], check=True, capture_output=True)
    name = f"carlo-job-test-{os.getpid()}"
    box = Box(name=name, image=TEST_IMAGE, workdir=wt,
              mounts=[Mount(wt, wt)] + [Mount(wt / n, wt / n, True) for n in read_only],
              env=container_env(wt), pass_env=list(secrets or {}),
              command=["sh", "-c", script])
    env = plan_env(secrets or {}, run_argv(backend.podman, box),
                   [*PODMAN_PASS, *(secrets or {})], name)
    return [str(BOX)], {**os.environ, **CANARIES, **env}, name


def in_box(tmp: Path, script: str, **kw) -> subprocess.CompletedProcess[str]:
    cmd, env, _ = box_command(tmp, script, **kw)
    return subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=300)


def containers(name: str) -> list[str]:
    return subprocess.run(["podman", "ps", "-aq", "--filter", f"name={name}"],
                          capture_output=True, text=True).stdout.split()


@needs_podman
def test_box_sees_no_host_secrets_files_or_sockets(tmp_path: Path) -> None:
    out = in_box(tmp_path, f"""env; echo ---
test -e {Path.home()} && echo HOST_HOME
test -e /tmp/.X11-unix && echo X11
test -e /run/podman/podman.sock -o -e /var/run/docker.sock && echo RUNTIME_SOCKET
test -e "{os.environ.get('XDG_RUNTIME_DIR', '/run/user/x')}" && echo XDG
test -e {ROOT / '.git'} && echo MAIN_REPO
true""", secrets={"GEMINI_API_KEY": "stage-key"})
    assert out.returncode == 0, out.stderr
    env, found = out.stdout.split("---")
    for value in CANARIES.values():
        assert value not in env
    assert "GEMINI_API_KEY=stage-key" in env
    assert found.split() == []


@needs_podman
def test_box_tools_and_git_metadata_are_read_only(tmp_path: Path) -> None:
    wt = (tmp_path / "wt").resolve()
    out = in_box(tmp_path, f"""touch /usr/x 2>/dev/null && echo ROOT_WRITABLE
touch {wt}/.git/config 2>/dev/null && echo GIT_WRITABLE
touch {wt}/ok && echo WORKTREE_OK""")
    assert out.stdout.split() == ["WORKTREE_OK"], out.stderr


@needs_podman
@pytest.mark.parametrize("url", [
    "http://127.0.0.1/", "http://169.254.169.254/latest/meta-data/", "http://10.0.0.1/",
    "http://192.168.1.1/", "http://[::1]/", "http://localtest.me/",  # resolves to 127.0.0.1
])
def test_box_cant_reach_private_or_metadata_addresses(tmp_path: Path, url: str) -> None:
    out = in_box(tmp_path, f"wget -q -T 10 -O- '{url}' >/dev/null && echo REACHED")
    assert "REACHED" not in out.stdout


@needs_podman
def test_box_reaches_the_web_only_through_the_proxy(tmp_path: Path) -> None:
    out = in_box(tmp_path, """wget -q -T 15 -O- https://example.com/ >/dev/null && echo PROXIED
wget -q -Y off -T 10 -O- http://1.1.1.1/ >/dev/null && echo DIRECT""")
    assert out.stdout.split() == ["PROXIED"], out.stderr


@needs_podman
def test_box_is_removed_on_sigterm(tmp_path: Path) -> None:
    cmd, env, name = box_command(tmp_path, "sleep 600")
    proc = subprocess.Popen(cmd, env=env)  # as the SDK starts it, then stops it on a timeout
    for _ in range(100):
        if containers(name):
            break
        time.sleep(0.2)
    assert containers(name)
    proc.send_signal(signal.SIGTERM)
    proc.wait(60)
    assert containers(name) == []
