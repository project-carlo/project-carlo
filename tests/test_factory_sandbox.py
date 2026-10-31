"""Keeping the factory's workers apart from the dispatcher (docs/factory-sandbox-plan.md).

The launcher, the environments, the git safety settings and (with Podman) the container.
Everything here runs without Podman, except the tests marked `needs_podman`.
"""

from __future__ import annotations

import json
import os
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
    launch = backend.launch("1-1", tmp_path, worker_env(Account("a", tmp_path / "a"), secrets))
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
    got = run_launcher(backend.launch("1-1", tmp_path, worker_env(None)), [])
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
    launch = HostBackend(BOX, claude=str(cli_), xvfb="").launch("1-1", tmp_path, {})
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
        "1-1", tmp_path, worker_env(req.account, req.secrets))
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
