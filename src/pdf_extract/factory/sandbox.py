"""Where a worker's Claude CLI runs (docs/factory-sandbox-plan.md).

The SDK stays in the dispatcher and starts `factory/sandbox/claude-in-box` as its CLI
(`cli_path`). The dispatcher tells the launcher, in `CARLO_BOX`, what to run and which
environment names to keep; it drops the rest of what the SDK passes down, which is the
dispatcher's whole environment.

- `worker_backend: host` (the default for now) runs the CLI on the host with that clean
  environment, under its own Xvfb.
- `worker_backend: sandbox` runs it in a fresh rootless Podman container per attempt, on
  an internal network whose only way out is an egress proxy that refuses private
  addresses. If anything about the sandbox is missing, the attempt ends as SANDBOX and
  the job waits: it never falls back to the host.
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

from pdf_extract.factory.config import FactoryError

if TYPE_CHECKING:
    from pdf_extract.factory.workers import WorkerRequest

LOGGER = logging.getLogger(__name__)

# Relative to the dispatcher's own checkout, where it runs; never a Run's copy.
SANDBOX_DIR = Path("factory") / "sandbox"
LAUNCHER = SANDBOX_DIR / "claude-in-box"

# What a host worker keeps of the dispatcher's environment: what the CLI, uv, pnpm and
# Chrome need to run. Not DISPLAY, SSH_AUTH_SOCK or XDG_RUNTIME_DIR (its sockets).
HOST_PASS = ("PATH", "HOME", "USER", "LOGNAME", "SHELL", "LANG", "LC_ALL", "LC_CTYPE",
             "TZ", "TMPDIR", "PNPM_HOME")
# What the SDK adds to the CLI's environment itself.
SDK_ENV = ("CLAUDE_CODE_ENTRYPOINT", "CLAUDE_AGENT_SDK_VERSION",
           "CLAUDE_CODE_SDK_READS_SESSION_STATE", "CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING")
# What rootless `podman` itself needs (not passed into the container).
PODMAN_PASS = ("PATH", "HOME", "USER", "LOGNAME", "XDG_RUNTIME_DIR", "XDG_CONFIG_HOME",
               "XDG_DATA_HOME", "CONTAINERS_CONF", "CONTAINERS_STORAGE_CONF")

# Names in the worker's environment that are host paths or host-only settings.
HOST_ONLY = ("CLAUDE_CONFIG_DIR", "GH_CONFIG_DIR")

IMAGE = "carlo-worker"
IMAGE_FILES = ("factory/sandbox/Containerfile", "pyproject.toml", "uv.lock")
LABEL = "carlo.factory=1"
NETWORK = "carlo-workers"
PROXY = "carlo-egress"
PROXY_PORT = 4750
PROXY_IMAGE = "ghcr.io/stripe/smokescreen:v0.1.0"
PROXY_URL = f"http://{PROXY}:{PROXY_PORT}"
WORKER_UID = 1000  # `worker` in the Containerfile

# What the proxy refuses, besides its own addresses (smokescreen's default) and the
# host's (added at start): loopback, RFC 1918, CGNAT, link-local and cloud metadata
# (169.254.169.254), IETF and benchmarking ranges, multicast, reserved, IPv6 ULA,
# link-local and multicast.
DENY_RANGES = (
    "0.0.0.0/8", "10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8", "169.254.0.0/16",
    "172.16.0.0/12", "192.0.0.0/24", "192.168.0.0/16", "198.18.0.0/15", "224.0.0.0/4",
    "240.0.0.0/4", "::/128", "::1/128", "fc00::/7", "fe80::/10", "ff00::/8",
)


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

    def launch(self, request: WorkerRequest, env: dict[str, str]) -> Launch: ...

    def finish(self, launch: Launch) -> None: ...

    def cleanup(self) -> None: ...


class HostBackend:
    """The CLI on the host, with only `env` and HOST_PASS, under a private Xvfb."""

    name = "host"

    def __init__(self, launcher: Path = LAUNCHER, claude: str | None = None,
                 xvfb: str | None = None) -> None:
        self.launcher = launcher.resolve()
        self.claude = claude or shutil.which("claude") or "claude"
        self.xvfb = shutil.which("xvfb-run") if xvfb is None else xvfb

    def launch(self, request: WorkerRequest, env: dict[str, str]) -> Launch:
        argv = ([self.xvfb, "-a"] if self.xvfb else []) + [self.claude]
        keep = [*HOST_PASS, *SDK_ENV, "PWD", *env]
        return Launch(str(self.launcher), plan_env(env, argv, keep))

    def finish(self, launch: Launch) -> None:
        pass  # the launcher stops the worker's process group itself

    def cleanup(self) -> None:
        pass


# ── Podman ──────────────────────────────────────────────────────────────────
class PodmanCall(Protocol):
    def __call__(self, *args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]: ...


def podman_runner(podman: str) -> PodmanCall:
    def call(*args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
        return subprocess.run([podman, *args], capture_output=True, text=True,
                              timeout=timeout)
    return call


def image_tag(files: dict[str, bytes]) -> str:
    """carlo-worker:<hash of the files it's built from>."""
    digest = hashlib.sha256()
    for name in sorted(files):
        digest.update(name.encode() + b"\0" + files[name] + b"\0")
    return f"{IMAGE}:{digest.hexdigest()[:16]}"


def main_files(repo: Path, upstream: str) -> dict[str, bytes]:
    """The image's files as main has them: a Run can't change what its workers run in."""
    files = {}
    for name in IMAGE_FILES:
        proc = subprocess.run(["git", "show", f"{upstream}:{name}"], cwd=repo,
                              capture_output=True)
        if proc.returncode != 0:
            raise SandboxError(f"can't read {name} from {upstream}: "
                               f"{proc.stderr.decode(errors='replace').strip()}")
        files[name] = proc.stdout
    return files


def host_addresses() -> list[str]:
    """This machine's own addresses, for the proxy to refuse (`ip -j addr`)."""
    try:
        out = subprocess.run(["ip", "-j", "addr"], capture_output=True, text=True, timeout=10)
        links = json.loads(out.stdout or "[]")
    except (OSError, subprocess.SubprocessError, ValueError):
        return []
    return sorted({a["local"] for link in links for a in link.get("addr_info", [])
                   if a.get("local")})


def proxy_argv(deny_addresses: list[str]) -> list[str]:
    """`podman run` for the egress proxy: on the workers' internal network and the
    normal one, the only container on both."""
    args = ["run", "-d", "--name", PROXY, "--label", "carlo.proxy=1",
            "--network", "podman", "--network", NETWORK,
            "--read-only", "--cap-drop=ALL", "--security-opt", "no-new-privileges",
            "--memory", "512m", "--pids-limit", "256", "--restart", "always",
            PROXY_IMAGE, "--listen-ip", "0.0.0.0", "--listen-port", str(PROXY_PORT)]
    for cidr in DENY_RANGES:
        args += ["--deny-range", cidr]
    for address in deny_addresses:
        args += ["--deny-address", address]
    return args


@dataclass
class Limits:
    memory: str = "6g"
    cpus: str = "4"
    pids: int = 2048


@dataclass
class Mount:
    source: Path
    target: Path
    read_only: bool = False

    def arg(self) -> str:
        return f"{self.source}:{self.target}:{'ro' if self.read_only else 'rw'}"


@dataclass
class Box:
    """One attempt's container: what `run_argv` turns into `podman run`."""

    name: str
    image: str
    workdir: Path
    mounts: list[Mount] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)  # fixed, not secret: in argv
    pass_env: list[str] = field(default_factory=list)  # names only: values from podman's env
    limits: Limits = field(default_factory=Limits)
    command: list[str] = field(default_factory=lambda: ["xvfb-run", "-a", "claude"])


def run_argv(podman: str, box: Box) -> list[str]:
    """`podman run ... claude` (§3.4). The SDK's arguments are added by the launcher."""
    argv = [podman, "run", "--rm", "-i", "--init", "--name", box.name, "--label", LABEL,
            f"--userns=keep-id:uid={WORKER_UID},gid={WORKER_UID}",
            "--user", f"{WORKER_UID}:{WORKER_UID}",
            "--cap-drop=ALL", "--security-opt", "no-new-privileges",
            "--ipc=private", "--pid=private", "--uts=private",
            "--read-only", "--tmpfs", "/tmp:rw,exec,mode=1777",
            "--tmpfs", "/home/worker:rw,exec,mode=1777",
            "--memory", box.limits.memory, "--cpus", box.limits.cpus,
            "--pids-limit", str(box.limits.pids),
            "--network", NETWORK, "--workdir", str(box.workdir)]
    for mount in box.mounts:
        argv += ["--volume", mount.arg()]
    for name, value in sorted(box.env.items()):
        argv += ["--env", f"{name}={value}"]
    for name in sorted(set(box.pass_env)):
        argv += ["--env", name]
    return argv + [box.image, *box.command]


def container_env(workdir: Path) -> dict[str, str]:
    """What every worker container gets besides its own environment: the proxy, and the
    Run's src/ for the image's /opt/venv."""
    no_proxy = "localhost,127.0.0.1,::1"
    return {"HOME": "/home/worker", "PYTHONPATH": str(workdir / "src"),
            "HTTP_PROXY": PROXY_URL, "HTTPS_PROXY": PROXY_URL, "http_proxy": PROXY_URL,
            "https_proxy": PROXY_URL, "NO_PROXY": no_proxy, "no_proxy": no_proxy,
            "LANG": "C.UTF-8"}


class PodmanBackend:
    """A fresh rootless Podman container per attempt (§3.4).

    Before each attempt it makes sure of the image (built from main when its files have
    changed), the internal network and the proxy. Any of them failing raises
    SandboxError: the attempt is SANDBOX and nothing starts on the host.
    """

    name = "sandbox"

    def __init__(self, repo: Path, upstream: str, *, launcher: Path = LAUNCHER,
                 podman: str | None = None, limits: Limits | None = None,
                 call: PodmanCall | None = None) -> None:
        self.repo, self.upstream = repo, upstream
        self.launcher = launcher.resolve()
        self.podman = podman or shutil.which("podman") or ""
        self.limits = limits or Limits()
        self.call = call or podman_runner(self.podman or "podman")
        self._image: str | None = None

    # ── Before an attempt ────────────────────────────────────────────────────
    def _ok(self, *args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
        try:
            proc = self.call(*args, timeout=timeout)
        except (OSError, subprocess.SubprocessError) as exc:
            raise SandboxError(f"podman {args[0]}: {exc}") from None
        if proc.returncode != 0:
            raise SandboxError(f"podman {' '.join(args[:3])}: "
                               f"{(proc.stderr or proc.stdout).strip()[-500:]}")
        return proc

    def image(self) -> str:
        """The image for main's files, built if this machine doesn't have it yet."""
        files = main_files(self.repo, self.upstream)
        tag = image_tag(files)
        if self._image == tag:
            return tag
        if self.call("image", "exists", tag).returncode != 0:
            LOGGER.info("building worker image %s", tag)
            with tempfile.TemporaryDirectory(prefix="carlo-image-") as ctx:
                for name, data in files.items():
                    (Path(ctx) / Path(name).name).write_bytes(data)
                self._ok("build", "--pull=newer", "--tag", tag, "--label", LABEL,
                         "--file", str(Path(ctx) / "Containerfile"), ctx, timeout=3600)
        self._image = tag
        return tag

    def network(self) -> None:
        if self.call("network", "exists", NETWORK).returncode != 0:
            self._ok("network", "create", "--internal", NETWORK)

    def proxy(self) -> None:
        """The egress proxy, started (again) if it isn't running."""
        state = self.call("container", "inspect", PROXY, "--format", "{{.State.Running}}")
        if state.returncode == 0 and state.stdout.strip() == "true":
            return
        self.call("rm", "--force", PROXY)
        self._ok(*proxy_argv(host_addresses()))

    def ready(self) -> str:
        """Everything a worker container needs, or SandboxError saying what's missing."""
        if not self.podman:
            raise SandboxError("podman is not installed (sudo apt install podman)")
        image = self.image()
        self.network()
        self.proxy()
        return image

    # ── An attempt ───────────────────────────────────────────────────────────
    def mounts(self, request: WorkerRequest) -> list[Mount]:
        """The Run's worktree at its own path. Its .git and .venv read-only: the
        dispatcher's git and gates use them."""
        wt = request.worktree.resolve()
        mounts = [Mount(wt, wt)]
        for name in (".git", ".venv"):
            if (wt / name).exists():
                mounts.append(Mount(wt / name, wt / name, read_only=True))
        return mounts

    def launch(self, request: WorkerRequest, env: dict[str, str]) -> Launch:
        image = self.ready()
        name = f"carlo-job-{request.attempt_id or request.job_id}"
        self.call("rm", "--force", name)  # a leftover from a crash
        workdir = request.worktree.resolve()
        passed = {k: v for k, v in env.items() if k not in HOST_ONLY}
        box = Box(name=name, image=image, workdir=workdir, mounts=self.mounts(request),
                  env=container_env(workdir), pass_env=[*passed, *SDK_ENV, "PWD"],
                  limits=self.limits)
        keep = [*PODMAN_PASS, *SDK_ENV, "PWD", *passed]
        return Launch(str(self.launcher),
                      plan_env(passed, run_argv(self.podman, box), keep, name), container=name)

    def finish(self, launch: Launch) -> None:
        if launch.container:
            try:
                self.call("rm", "--force", "--time", "0", launch.container)
            except (OSError, subprocess.SubprocessError) as exc:
                LOGGER.warning("removing %s failed: %s", launch.container, exc)

    def cleanup(self) -> None:
        """At startup: remove every worker container a crashed dispatcher left."""
        if not self.podman:
            return
        out = self.call("ps", "--all", "--quiet", "--filter", f"label={LABEL}")
        ids = out.stdout.split() if out.returncode == 0 else []
        if ids:
            self.call("rm", "--force", "--time", "0", *ids)


def backend(name: str, repo: Path, upstream: str, limits: Limits | None = None) -> Backend:
    if name == "host":
        return HostBackend()
    if name == "sandbox":
        return PodmanBackend(repo, upstream, limits=limits)
    raise FactoryError(f"worker_backend must be host or sandbox, not {name!r}")
