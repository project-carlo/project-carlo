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

    return PodmanBackend(main_repo(tmp), "main", launcher=BOX, podman=podman, call=fake)


def test_the_container_is_locked_down(tmp_path: Path) -> None:
    from pdf_extract.factory.sandbox import NETWORK, PROXY_URL

    fake = FakePodman()
    wt = tmp_path / "wt"
    (wt / ".git").mkdir(parents=True)
    req = request(wt, attempt_id=42, secrets={"OPENAI_API_KEY": "stage-secret"})
    launch = podman_backend(tmp_path, fake).launch(req, worker_env(req.account, req.secrets))
    argv = json.loads(launch.env["CARLO_BOX"])["argv"]
    joined = " ".join(argv)
    assert launch.container == "carlo-job-42"
    for flag in ("--rm", "-i", "--init", "--cap-drop=ALL", "no-new-privileges", "--read-only",
                 "--ipc=private", "--pid=private", "--userns=keep-id:uid=1000,gid=1000",
                 "--label carlo.factory=1", f"--network {NETWORK}", "--pids-limit 2048",
                 "--memory 6g", f"--workdir {wt.resolve()}"):
        assert flag in joined, flag
    assert "--privileged" not in joined and "host" not in argv
    volumes = [argv[i + 1] for i, a in enumerate(argv) if a == "--volume"]
    assert volumes == [f"{wt.resolve()}:{wt.resolve()}:rw",
                       f"{wt.resolve() / '.git'}:{wt.resolve() / '.git'}:ro"]
    # Secrets go by name, their values from podman's environment, never on its command line.
    assert "stage-secret" not in joined and "--env OPENAI_API_KEY" in joined
    assert f"--env HTTPS_PROXY={PROXY_URL}" in joined
    assert f"--env PYTHONPATH={wt.resolve() / 'src'}" in joined
    for name in ("CLAUDE_CONFIG_DIR", "DISPLAY", "SSH_AUTH_SOCK", "GH_CONFIG_DIR"):
        assert f"--env {name}" not in joined
    assert argv[-3:] == ["xvfb-run", "-a", "claude"]
    assert ("rm", "--force", "carlo-job-42") in fake.calls  # a leftover goes first


def test_the_sandbox_launcher_gives_podman_only_what_it_names(tmp_path: Path) -> None:
    fake_podman = tmp_path / "podman"
    fake_podman.write_text("#!/usr/bin/env python3\nimport json, os, sys\n"
                           "print(json.dumps({'args': sys.argv[1:], 'env': dict(os.environ)}))\n")
    fake_podman.chmod(0o755)
    req = request(tmp_path, attempt_id=7, secrets={"GEMINI_API_KEY": "stage-key"})
    backend = podman_backend(tmp_path, FakePodman(), podman=str(fake_podman))
    got = run_launcher(backend.launch(req, worker_env(req.account, req.secrets)),
                       ["--verbose"])
    assert got["args"][0] == "run" and got["args"][-1] == "--verbose"
    env = got["env"]
    assert env["GEMINI_API_KEY"] == "stage-key"
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
