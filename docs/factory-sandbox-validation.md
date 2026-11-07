# Sandbox pre-merge validation, 2026-11-02

Checks 1–3 completed against PR #184 commit
`206bd658ed87d2c0d98c999be87eeaf4bbaad308`, image
`carlo-worker:b30d0763fb6bcab5`. SDK 0.2.174, Claude CLI 2.1.312,
model `claude-sonnet-5-5`, effort `high`. Run: 18:52:05–18:53:22 UTC.

The validation used the production `SdkWorker`, `PodmanBackend`, launcher,
workspace refresh/sync-back and container restrictions. It used a separate network,
proxy, container label, workspaces and session folders. No dispatcher was started;
no production ledger, Run, service, checkout or account credential was modified.
Account configuration and token files were read from `~/carlo-factory`.

## Authentication and account routing

Both `first` and `second` authenticated using their configured `worker_token_file`,
executed Bash inside their worker container, wrote an `AUTH_OK` file, and returned
`ok`. The output was synced back to the temporary trusted workspace. Both SDK
results contained usage, model usage and cost estimates. Allowed rate-limit events
arrived for both accounts; no rejected-limit condition was induced.

Each account's five-hour and weekly reset timestamps in the worker events matched
the usage endpoint queried with that account's existing login (within one second
of rounding). The distinct windows matched the intended accounts. Both logins
report Pro, and worker events reported `isUsingOverage: false`. Workers received
OAuth tokens and an empty `ANTHROPIC_API_KEY`. This verifies subscription-account
routing and reporting; an invoice charge was not independently checked.

SDK cost estimates for initial attempt plus resume: first `$0.0338366`, second
`$0.0338232`; total `$0.0676598`. These are model cost estimates, not confirmed
charges to a payment method.

## Session resume

For each account, the first attempt remembered a random 128-bit nonce, without
writing it to a workspace file. That container was removed. A second attempt used
a different container name, the same session ID, and the same per-Run sessions
mount. Its prompt asked for the nonce without including the nonce; tools were
disabled for that request.

Both returned the exact nonce and `ok`, kept the original session ID, and appended
the resume question to the same transcript. Usage, model usage, cost and allowed
rate-limit events were present after resume. Both containers were removed.

This tests the resume mechanism used by send-backs; an actual dispatcher send-back
and a production `factory inspect` remain part of the live canaries.

## Headed eCatholic access

Through the isolated proxy, plain Python HTTP requests received Cloudflare `403`
responses with `cf-ray` headers from both sites. Headed `visit.py` then returned:

- `https://queenofpeacehawley.com/`: `200`, `ok`, first load,
  publication `ecatholic:24839`, parish title and bulletin link present.
- `https://stlouischurch.org/`: `200`, `ok`, first load,
  publication `ecatholic:29150`, parish title and bulletin links present.

Screenshots and rendered HTML were saved. Google Chrome's command line had no
`--no-sandbox`; `chrome://sandbox` reported PID/network namespaces and seccomp-BPF
enabled and “You are adequately sandboxed.” This uses the PR's vendored seccomp
profile, not Podman's unchanged default profile. Access can vary on future requests.

## Artifacts and reproduction

Private artifacts from this run remain in
`/tmp/carlo-pr184-validation-fve8bfv2/`: `report.json`, `account-usage.json`,
per-account sessions, browser output, and `browser/scratch/` screenshots, HTML and
the sandbox status. No token values are written to reports or command arguments.
Temporary containers, proxy and network were removed after the run.

Repeat from the PR checkout:

```bash
uv run python factory/sandbox/validate-live.py
```

The script reads existing account paths from the live local configuration, uses
trusted `HEAD` for the pre-merge image, and prints a new private artifact directory.
Authenticated runs consume account usage. It never calls the production backend's
global startup cleanup. Ruff passed; the additional account-window and browser
assertions were also checked against this run's saved evidence.

## Network edge cases and refresh timing, 2026-11-02

These checks also passed against the same PR commit. The proxy image was
`carlo-egress:aa474a53afb256a4` (the production smokescreen image and deny policy).

### Controlled network fixture

The fixture used two isolated bridges: an RFC 5737 documentation subnet
(`203.0.113.0/24`, treated as public by the production policy) and a private subnet
(`10.231.184.0/24`). The DNS/HTTP fixture listened at both `203.0.113.10` and
`10.231.184.10`. The worker could reach only the private bridge; the proxy had both
bridges. Its resolver was the controlled fixture. This exercises the real proxy
without changing public DNS or contacting a third-party redirect service.

- An ordinary public-classified HTTP request and public-to-public redirect returned
  `200` with the expected response body.
- Public-to-private redirects to `127.0.0.1`, `10.231.184.10`, `169.254.169.254`,
  `192.168.1.1`, and `::1` each returned proxy `407` denials. Explicit proxy use
  prevented client-side loopback bypass from hiding the policy being tested.
- The same hostname resolved first to the public-classified address, then to the
  private address, then back. HTTP and CONNECT worked in the public phases and
  returned `407` denials in the private phase. DNS logs confirm the changed answers
  were actually queried.
- Two additional per-connection tests configured DNS to answer public on the first
  A lookup and private on any subsequent A lookup. HTTP and CONNECT each made one
  A lookup and connected to the public fixture. This checks that the validated
  address is pinned rather than resolved again when dialing.
- The private HTTP canary received **zero requests** across all cases.

This is a deterministic rebinding simulation; it does not claim exhaustive coverage
of all resolvers, DNS record types, TLS behavior or internet DNS timing.

Final artifacts: `/tmp/carlo-pr184-network-p9zrvmzj/` (12 result groups, DNS/HTTP
event log, proxy log, client output, and `report.json`). The earlier run before
adding the per-connection checks is `/tmp/carlo-pr184-network-7dp_4obo/`.
Both runs cleaned up their containers and networks.

Repeat: `uv run python factory/sandbox/validate-network.py`.

### Representative workspace refresh

Source: completed Camden Run, commit
`f3f11de70d9c8f0f56439983083b54c41b4bfefe`. A `git archive` plus a read-only SQLite
online backup created a temporary trusted snapshot. No untracked files or
credentials were copied. The snapshot held 6,867 files totaling 78,389,330 bytes
(74.76 MiB), including `data/parish_events.db`; production refresh exclusions
reduced this to 4,127 non-private snapshot entries.

- Three empty-destination refreshes: **0.288–0.299 seconds**.
- Five unchanged refreshes: **0.130–0.135 seconds**.
- Refresh after worker edits: **0.135 seconds**.
- Refresh after a trusted source update: **0.128 seconds**.

Timings include rsync, first-copy SQLite backup when applicable, and the production
file snapshot. OS page caches were not flushed, so empty-destination means an empty
directory, not a cold disk. These are measurements of this representative snapshot,
not a guarantee for larger Runs or heavy concurrent load. All measurements were
well below the 1,800-second rsync timeout.

Assertions passed: changed tool code was restored, out-of-scope additions were
removed, a worker-private cache file and database marker survived, the trusted
database did not acquire the marker, and a trusted code update reached the worker.
The source Run's git status remained clean.

Artifacts: `/tmp/carlo-pr184-refresh-m60u3_5t/report.json` and temporary workspaces.
Repeat:

```bash
uv run python factory/sandbox/validate-refresh.py \
  /home/lyonsl2/carlo-factory/data/factory/worktrees/camden-map-1
```

Ruff and `git diff --check` passed. Live clone migration, real map/seed/seed-review
jobs, production send-backs, and switching the live backend remain open.

## Container permission mode

Sandboxed workers now select `bypassPermissions`; host workers keep `auto`.
An isolated authenticated rerun with this change confirmed `bypassPermissions` in
the CLI's init message for both accounts, on both the initial attempt and a
fresh-container resume. Both accounts wrote their output, returned usage and cost,
and recalled the nonce after resume. Artifacts:
`/tmp/carlo-pr184-validation-rdqrvbk9/`. The harness now asserts this permission mode.
The earlier validation above predates the mode change and used `auto`.
