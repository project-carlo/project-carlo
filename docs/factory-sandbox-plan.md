# Plan: sandboxed factory workers (issue #168)

Status: written 2026-10-31 from the code at `01926ac2` and the live factory in
`~/carlo-factory`. Phases 0, 2, 3, 4 and 6 are built, with unit tests and container tests
that skip without Podman. Nothing has run in a real container yet: Phase 1 (spikes) and
Phase 5 (live checks) wait on Podman and the account tokens. Where the build differs from
this plan, the section says so ("Built:").

## 1. Decision

Run each worker's Claude Code CLI, and everything it starts (tools, hooks, Bash, `uv`,
Chrome, Xvfb), in a **fresh rootless Podman container per attempt**. The container sees a
private copy of the Run's files and reaches the internet only through an egress proxy that
refuses private, host and metadata addresses. The dispatcher, ledger, Git, gates, GitHub
and R2 publishing stay on the host and never run anything the worker wrote.

There is no fallback to host execution. If the sandbox can't start, the attempt fails and
the job waits.

Owner decisions (2026-10-31):

- Workers keep full public internet. The proxy (§3.6) only blocks private addresses.
- A long-lived Claude token inside the container is acceptable (§3.5).
- Scoped R2, Gemini and OpenAI keys are a follow-up. Until then, seed stages get the
  existing keys (§3.5).

## 1a. Why Podman

| Option | What it is | Fit here |
|---|---|---|
| **Podman, rootless** (chosen) | Ordinary Linux containers, no background daemon, run as your user | Standard images and flags; a container per job is cheap (about 1 s); nothing runs as root; works in WSL2 (cgroup limits already delegated here); widely documented; gVisor can be layered on later |
| Docker Engine | The same containers, through a daemon that runs as root | Works equally well, but anyone who can reach its socket is effectively root. Rootless Docker exists but is fiddlier than Podman |
| Docker Desktop (already on Windows) | Docker Engine managed by the Windows app | Has to be running on the Windows side for the 24/7 service. Not wired into this WSL distro today. Mounts from this distro cross a slower path |
| Docker Sandboxes (`sbx`) | Each agent in a small virtual machine, with a network policy and credential proxy built in | The strongest isolation (its own kernel), but new, built around Docker's own agent flow. Custom SDK runs, two subscription logins, resume and rate-limit events are all unproven. Good follow-up spike |
| gVisor (`runsc`) | A runtime that puts a user-space kernel between the container and the host | Adds protection against kernel exploits on top of Podman/Docker. Chrome compatibility and file speed need testing. Optional later layer, not a replacement |
| Anthropic `sandbox-runtime` / bubblewrap | Lightweight wrappers that restrict a process on the host, with no image | Quick to start, but they see the host's installed tools. You list what to hide rather than what to show, which is easy to get wrong. Same network proxy work. Weaker for running Chrome |

Podman gives the most isolation for the least new machinery on this machine. Everything
in this plan (image, mounts, internal network, proxy, limits) carries over to Docker
Engine if Podman hits a WSL2 problem in the spike, or to gVisor if kernel isolation is
wanted later. All containers share the host kernel; only Docker Sandboxes or a VM avoid
that.

## 2. What the code does today (checked, beyond the issue)

The issue's `worker_env()` point is right, and in practice the exposure is wider:

1. **Every key in `~/carlo-factory/.env` reaches workers.** `python -m pdf_extract`
   calls `_load_dotenv()` before any command (`__main__.py:812`), so the dispatcher's own
   `os.environ` holds `R2_*` (write keys), `CLOUDFLARE_API_TOKEN`, `GEMINI_API_KEY` and
   `OPENAI_API_KEY`. The SDK (0.2.174, `subprocess_cli.py:819`) starts the CLI with
   `{**os.environ, **options.env}`, so all of them are in every worker.
2. **`SSH_AUTH_SOCK` and the shared Xvfb `DISPLAY`** are in the dispatcher's
   environment (seen in `/proc/<pid>/environ`) and pass through the same way.
3. **Run worktrees share the owner's main repository metadata.** `~/carlo-factory` is a
   linked worktree of `~/projects/project-carlo`, and so is each Run worktree
   (`gitdir: /home/lyonsl2/projects/project-carlo/.git/worktrees/<run>`). A worker can
   write `.git/config` (`core.fsmonitor`, aliases) or `.git/hooks/*` there. That code then
   runs in the owner's own sessions, and in the dispatcher's `git status`, `merge` and
   `fetch`, which hold the GitHub login.
4. **Gates run in the worktree the worker edited, with the dispatcher's secrets.** The
   diff-scope gate only reverts files git tracks. Gitignored files stay: `.env`, `.venv`,
   `node_modules`, `scratch/`. For example, a planted `.env` with `CARLO_REMOTE_WRITE=1`
   is loaded by `pnpm diocese validate` (via `_load_dotenv`'s `setdefault`), alongside the
   R2 write keys already in that environment.
5. **Timeouts don't clean up.** On timeout the SDK sends SIGTERM to the CLI only. Chrome
   and Xvfb children can survive.
6. **Seed workers need secrets themselves.** `draft-parish-seed` reads bulletins from R2
   (read keys) and makes paid `seed ask` / `seed extract` calls (Gemini, OpenAI). The
   issue doesn't cover these. Map-side stages need none of them.

Points 1 to 4 can be fixed cheaply on the host before any container exists (Phase 0).

## 3. Design

### 3.1 Where the boundary sits: a CLI launcher, not the whole SDK

`ClaudeAgentOptions(cli_path=...)` lets the dispatcher keep the Python SDK in its own
process while the CLI it spawns is a launcher, `factory/sandbox/claude-in-box`, that runs
`podman run -i ... claude "$@"`. The SDK only parses the stream-json coming back, so
`on_step`, rate-limit events, `ResultMessage` usage and costs keep working unchanged.

This gives the same boundary the issue asks for (all execution is inside), on one
condition: **the host-side SDK must never run tools**. That means no `hooks`,
`can_use_tool` or in-process MCP servers in `ClaudeAgentOptions`. A unit test will assert
it. Running the whole Python worker in the container was considered too. It would need a
second RPC layer for steps and events, and it adds nothing as long as that condition holds.

The launcher:

- receives no inherited environment. It builds the container's environment from an
  explicit allowlist (§3.5) and passes nothing else, so the SDK's `os.environ` merge
  stops mattering;
- mounts the workspace at the **same absolute path** inside, so the SDK's `cwd`
  check passes, session project keys stay stable for resume, and paths in steps and
  transcripts match the host;
- names the container `carlo-job-<attempt id>` with label `carlo.factory=1`, traps
  SIGTERM/SIGINT and runs `podman rm -f` on it;
- answers the SDK's `claude -v` version probe by running the same image.
  Built: the host's `claude -v` answers it. The probe comes without the worker's
  environment, and the SDK only uses the answer for a warning.

### 3.2 Image

`factory/sandbox/Containerfile`, built by the dispatcher on the host from `origin/main`
files (never from a Run worktree). It is tagged by a hash of the Containerfile,
`uv.lock`, `pnpm-lock.yaml` and the pinned CLI version, and rebuilt when the hash changes:

- Ubuntu base, Python 3.13, uv, Node and pnpm, the pinned Claude CLI;
- Google Chrome, Xvfb/`xvfb-run`, poppler and the other PDF libraries the pipeline uses;
- the project's Python dependencies installed with `uv sync --frozen --group dev` into
  a read-only `/opt/venv` (`UV_PROJECT_ENVIRONMENT=/opt/venv`, `UV_NO_SYNC=1`), so
  workers' `pnpm diocese` / `pnpm seed` use the Run's `src/` without reinstalling;
- an unprivileged user `worker`. Mapped to the owner's uid with `--userns=keep-id`, so
  files it writes are the owner's on the host.

Dependencies are installed at build time, before any untrusted content is processed.
Built: the tag hashes the Containerfile (which pins the CLI, Node and pnpm), `pyproject.toml`
and `uv.lock`. Not `pnpm-lock.yaml`: workers' `pnpm` scripts only call `uv run`, so the
image installs no Node packages.

### 3.3 Workspace

One **private workspace per Run**, `data/factory/sandbox/<run>/work`, alongside the
trusted Run worktree (which stays where it is, for the dispatcher's Git work).

- **Before each attempt** the dispatcher refreshes it from the trusted worktree with
  `rsync --delete`. It excludes `.git`, `.venv`, `node_modules` and the worker-private
  state: the database copy, caches, and `scratch/<run>/`, which the worker keeps between
  attempts. Anything the worker changed out of scope last time is gone after this.
- There is **no `.git`** in it. Workers don't use git (no skill or prompt needs it, and
  the dispatcher already denies the commands that change it), so there's no shared
  metadata to protect and no `.git` file pointing outside.
- The container mounts the workspace read-write, then `src/`, `.claude/`, `factory/`,
  `pyproject.toml`, `package.json` and the lockfiles **read-only** on top. Workers can't
  change their own tools, prompts, settings or hooks mid-session.
- `/tmp` and the home directory are `tmpfs`.

**After each attempt, whatever its outcome**, the dispatcher (trusted code) compares the
workspace with the snapshot it wrote before the attempt and applies the changes to the
trusted worktree:

- a changed path is applied only if it matches the stage's `writes` (or is
  worker-private state);
- it is rejected if it is a symlink, hardlink, device or FIFO, if a component is `..` or
  `.git`, or if it exceeds a size or count cap;
- files are copied by content, never by link, into directories the dispatcher creates;
- rejected paths are recorded on the attempt and reported by the diff-scope gate as
  today ("changed outside your write boundaries...").

The existing diff-scope and HEAD checks stay as a second layer.

### 3.4 Container settings

```
podman run --rm -i --init --name carlo-job-<id> --label carlo.factory=1
  --userns=keep-id --user worker
  --cap-drop=ALL --security-opt no-new-privileges
  --security-opt seccomp=<default, or Playwright's Chrome profile if the spike needs it>
  --ipc=private --pid=private --uts=private
  --read-only --tmpfs /tmp --tmpfs /home/worker
  --memory 6g --cpus 4 --pids-limit 2048
  --network carlo-workers                      # internal, no gateway (§3.6)
  -v <workspace>:<same path>:rw  + read-only tool mounts (§3.3)
  -v <session dir>:/home/worker/.claude/projects:rw
  --env-file <per-attempt allowlist>
  carlo-worker:<hash> xvfb-run -a claude <SDK args>
```

There is no `--privileged`, no host network, and no mounts of the host home, Podman or
Docker sockets, SSH agent, X11 socket, `~/carlo-factory` or the main repository.
`cgroup v2` with `cpu memory pids` delegation is already enabled on this machine
(checked), so the limits work rootless.

### 3.5 Credentials

**Claude login: a long-lived token per account.** The owner accepts a long-lived token
in the container. The remaining problem is refresh, not exposure. Each account's
`.credentials.json` holds a rotating refresh token. If a worker refreshed it inside the
container, the host copy would go stale, and the dispatcher's usage readings would lose
that login. Bind-mounting the single file doesn't work either: the CLI writes it by
atomic rename (`.claude.json.tmp.*` files seen in `~/.claude_2`).

So each account gets a token from `claude setup-token`: one year, made for
non-interactive use, never refreshed. It is a one-time step per account,
`CLAUDE_CONFIG_DIR=~/.claude_2 claude setup-token`, saved to a mode-600 file named in
`local.yaml` (`worker_token_file:` on the account). The launcher passes it as
`CLAUDE_CODE_OAUTH_TOKEN`. Nothing in the container can refresh or rotate it. The
dispatcher keeps reading usage with the account's normal login on the host, as today.

The spike confirms that a job run with the token is billed to the right subscription, and
that `RateLimitEvent`s, `ResultMessage.usage`/`model_usage`, resume and the `init` message
look the same as today. If they don't, the fallback is a per-account worker config
directory holding a copy of the credentials, synced back after each attempt under a lock.

**Other secrets, per stage.** Stage specs gain an optional `secrets:` list naming `.env`
entries the dispatcher passes in. Phase 0 moves `.env` out of the dispatcher's own
environment into a dict.

| Stage | Gets |
|---|---|
| survey, survey-review, map, reconcile, integrate | nothing |
| seed, seed-review | the existing `R2_*`, `GEMINI_API_KEY` and `OPENAI_API_KEY`, unchanged for now |

`CLOUDFLARE_API_TOKEN`, GitHub and SSH never enter any container. Follow-up (owner): a
read-only, bucket-scoped R2 token and separate model keys with spend caps for seed
stages. It's a config change once `secrets:` exists. Until then, a seed worker could write
to R2.

### 3.6 Network

Workers keep **full public internet**: any website, any parish domain, web search. The
proxy only stops them reaching things that aren't the public internet: this PC and
Windows, the home network (router, other devices), and cloud metadata addresses.
Claude's `WebSearch` runs on Anthropic's side and doesn't pass through it at all.

Why a proxy rather than a firewall rule: rootless containers send traffic out as the
owner's own user, so a host firewall can't block private addresses for the container
without also blocking them for the owner. A proxy on the only route out does it cleanly.

- `podman network create --internal carlo-workers`: worker containers get no route out.
- One long-lived **egress proxy** container (Stripe's `smokescreen`, built for exactly
  this job) sits on that network and on the normal rootless network. Workers get
  `HTTP(S)_PROXY`/`NO_PROXY`. The pipeline's fetch code (`urllib.request`, `httpx`), curl
  and the Claude CLI pick these up automatically. Chrome doesn't, so the two Playwright
  launches (`src/pdf_extract/browser.py`, `parish-site-access/scripts/render.py`) pass
  `proxy=` from the environment. The proxy only forwards encrypted connections and does
  not decrypt them, so no certificate setup is needed.
- The proxy resolves each name itself and connects to the address it checked, which
  closes DNS rebinding. It refuses loopback, RFC 1918, CGNAT, link-local (including
  `169.254.169.254`), ULA and multicast addresses, and the host's own addresses. It
  only allows ports 80 and 443. Every redirect is a new request and is checked again.
  Built: smokescreen has no port allowlist, so any port on a public address is
  allowed. Private addresses are refused on every port.
- Tools that ignore the proxy fail closed, since there is no other route.
This doesn't stop a worker sending data to a public site. That's why §3.5 limits what is
inside rather than relying on the network. Per-stage hostname allowlists are not planned,
since workers need open web access.

### 3.7 Sessions and transcripts

- Each job gets `data/factory/sessions/<run>/<job>/`, mounted as the container's
  `~/.claude/projects`. Resume works because the job, its directory and its workspace
  path are stable. One Run can't read another's transcripts, and nothing lands in the
  account's own config directory.
  Built: per Run (`data/factory/sessions/<run>/`), not per job, because an answer job
  resumes the session of the job it answers. Jobs in a Run already share `scratch/`.
- `find_transcript` and `copy_transcript` look there for sandboxed attempts.
- Copied back after each attempt: nothing else. `.claude.json` and other CLI state stay
  in the container's tmpfs home.

### 3.8 Trusted gates

- Gates run in the trusted Run worktree after sync-back. It only ever contains files the
  dispatcher wrote, the database copy it made, and its own `.venv`.
- Gate commands get a **scrubbed environment** with no GitHub, R2 write or Cloudflare
  keys. A gate that needs to read R2 (check `pnpm seed check`) gets the R2 keys.
- `git commit` keeps `--no-verify`. Dispatcher git commands also run with
  `-c core.hooksPath=/dev/null -c core.fsmonitor=false`.
- Phase 4 makes Run worktrees and `~/carlo-factory` **standalone clones** of `origin`
  instead of linked worktrees of the owner's checkout, so nothing a Run touches shares
  metadata with `~/projects/project-carlo`.

### 3.9 Lifecycle

- **Timeout and cancel:** the SDK's SIGTERM reaches the launcher, which runs
  `podman rm -f`. The dispatcher also force-removes `carlo-job-<attempt>` in a `finally`.
  `--init` plus a fresh container means no stray Chrome or Xvfb survives.
- **Restart recovery:** on startup the dispatcher removes every container labelled
  `carlo.factory=1` before treating `running` jobs as crashed (the existing path).
- **Fail closed:** a missing image, a failed build, Podman missing, the proxy down or a
  workspace refresh error ends the attempt as a new outcome, `SANDBOX`. It doesn't count
  as a worker crash. The job waits and the Run blocks after N such failures in a row,
  with a clear issue. A `sandbox` setting never falls back to `host`.
  `worker_backend: sandbox | host` in `local.yaml`; `host` stays the default until the
  live checks pass (§8). Once `sandbox` is the default, real Runs refuse `host` unless
  `allow_host_workers: true` is also set, and `pnpm factory status` warns loudly when
  workers run on the host.

## 4. Phases

**Phase 0: host fixes, no containers (small, ship first).**
- Keep `.env` out of `os.environ` in the factory command. Load it into a `Secrets` dict
  that only the backup, publishing and (scoped) gate code read.
- Add the launcher in `host` mode: `env -i` plus the allowlist, then `exec claude`. Set
  it as `cli_path` so workers get a clean environment now.
- Scrub gate environments. Add `-c core.hooksPath=/dev/null -c core.fsmonitor=false` to
  dispatcher git calls.
- Tests: a canary secret in the dispatcher's environment is absent from the worker's
  (stub launcher prints its environment), and from gate commands.

**Phase 1: spikes, on this machine, written up in this file.**
- Install Podman (Ubuntu 26.04 apt). Confirm rootless `pasta` networking, cgroup limits
  and `--userns=keep-id` on WSL2.
- Headed Chrome under private Xvfb in the container: `visit.py` against a Cloudflare
  eCatholic site with Chromium's own sandbox on. Try the default seccomp profile first,
  then Playwright's. Never `--no-sandbox` or `--privileged`.
- A `claude setup-token` token as `CLAUDE_CODE_OAUTH_TOKEN`: billing account, rate-limit
  events, usage, resume.
- smokescreen on an internal network: the deny list, rebinding, redirects.
- `--userns=keep-id` file ownership, and the cost of refreshing the 170 MB workspace.

**Phase 2: image and launcher in `sandbox` mode.** Containerfile, hash-tagged builds,
the launcher, the network and proxy, `worker_backend`, the `SANDBOX` outcome, restart
cleanup. The workspace is still the trusted worktree, mounted directly; Phase 3 adds the
copy.

**Phase 3: private workspace and sync-back.** Refresh, read-only tool mounts, the
snapshot diff, path and symlink validation, recording on the attempt, and diff-scope
reporting.

**Phase 4: credentials, sessions, clones.** Per-account `worker_token_file` (or the
fallback the spike chose), per-stage `secrets:`, per-job session directories, standalone
clones for `~/carlo-factory` and Run worktrees (with a migration for live Runs).

**Phase 5: verification and real jobs** (§5), then switch the live factory to
`sandbox`.

**Phase 6: docs.** `docs/factory-spec.md` (§5 Worker setup, Running it, Future
enhancements: the Bash-sandbox item changes), `factory/local.example.yaml`, the systemd
unit (the dispatcher no longer needs `xvfb-run`), and machine setup.

## 5. Verification (the issue's acceptance criteria)

Automated, in `tests/test_factory_sandbox.py`. They run the real launcher against a tiny
test image, and are skipped when Podman is absent:

| Check | How |
|---|---|
| No host secrets | Canary file in `$HOME`, canary env var in the dispatcher, a fake `.env` in `~/carlo-factory`: a worker's `cat`/`env`/`find` finds none |
| No shared state | Writing to the main checkout, another Run's workspace, `.git` of any repo, the ledger: path absent or read-only |
| No sockets | Podman/Docker sockets, `SSH_AUTH_SOCK`, `/tmp/.X11-unix` of the host: absent |
| Network | `curl` to `127.0.0.1`, the host's LAN IP, `10/8`, `169.254.169.254`, a rebinding name, a public URL redirecting to a private one: refused; a public parish site: allowed |
| Outputs | In-scope edit applied; out-of-scope edit, symlink to `/etc/passwd`, symlink dir escape, `../` path, oversized file: rejected and reported |
| Read-only tools | Editing `src/`, `.claude/settings.json`, a hook: fails |
| Cleanup | Timeout with Chrome running: no `carlo-job-*` container or Chrome process left; dispatcher kill -9 then restart: leftovers removed, job resumes |
| Fail closed | No image / Podman missing / proxy down: attempt is `SANDBOX`, no host process started |

Manual, recorded in the PR: a real headed-browser **map** job and a **seed** plus
**seed-review** job, each with handoff, transcript, cost, usage, rate-limit events and
`factory inspect` output intact. Also: a send-back that resumes the same session, a token
refresh across a job boundary, and a second account.

## 6. Residual risks (to document)

- Rootless containers share the host kernel. A kernel exploit escapes. A microVM
  (Docker Sandboxes, or gVisor on a dedicated Linux host) would close this. WSL2 does
  expose `/dev/kvm`, but that is untested.
- Every container holds its account's one-year Claude token (accepted), and seed
  containers hold the current R2 keys (write-capable) and model keys until the scoped-key
  follow-up. A worker could send any of them to a public site. Revoke a token with
  `claude setup-token` again, or from the account's settings.
- Workers can still write wrong but in-scope data. Gates, reviewers and the PR remain
  the defence there.
- `scratch/{run}/**` is in map/survey/reconcile scope, so a worker can overwrite earlier
  jobs' handoffs in that Run. This is unchanged by this plan; worth a separate issue.

## 7. Owner decisions

All settled on 2026-10-31:

- Workers keep full public internet; the proxy only blocks private addresses.
- A long-lived Claude token per account (`claude setup-token`) inside the container is
  acceptable. The owner runs `setup-token` once per account before the live switch.
- Scoped R2, Gemini and OpenAI keys are a follow-up; seed stages keep the current keys.
- `~/carlo-factory` and Run worktrees become standalone clones of `origin`.
- No Docker Sandboxes follow-up spike.

## 8. Delivery

One PR, with a commit per phase (0, 2, 3, 4, 6), built in its own worktree. Constraints
for that PR:

- Podman isn't installed on this machine, and installing it needs the owner's `sudo`
  (`sudo apt install podman`; 5.7 is available). So the PR ships the code, the
  Containerfile, the launcher, and the container tests, which skip without Podman. It
  does not claim any live result. The Phase 1 spikes and Phase 5 live checks become a
  checklist in the PR, for after the owner installs Podman and creates the tokens.
- Nothing in the PR touches the live factory (`~/carlo-factory`, its ledger, its Run
  worktrees, the systemd service) or migrates live Runs. Migration is a documented
  command the owner runs.
- The default stays `worker_backend: host` (with Phase 0's clean environment) until the
  owner has run the live checks. The `allow_host_workers` safeguard then applies once
  `sandbox` becomes the default in a follow-up.
