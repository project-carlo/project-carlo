"""The onboarding factory: agent jobs, scheduled by code, that take a diocese from nothing
to seeded parishes. How it works and where a
change goes: docs/factory.md.

- `config`: the caps and limits (`factory/config.yaml`) and this machine's accounts and
  paths (`data/factory/local.yaml`).
- `spec`: the stage specs in `factory/stages/`.
- `handoff`: what a worker writes at the end of its job, and its check.
- `ledger`: SQLite state: Runs, jobs, attempts, steps, gates, flags, decisions.
- `git`: the Run's branch and worktree: commits, pushes, merging main.
- `plan`: which job a Run needs next.
- `render`: every piece of worker-facing text built in code.
- `workers`: the Agent SDK worker, and the stub worker the tests use.
- `playbook`: what the dispatcher appends to `diocese.md`.
- `dispatcher`: the loop, built from:
  - `engine`: one job, from picking it to its gates and what follows them;
  - `attempts`: one attempt: starting its worker, recording what came back;
  - `accounts`: the account each attempt runs on, against the caps;
  - `answers`: issues for blocking flags, and what the owner's answers do;
  - `housekeeping`: merged Runs, seed readiness and backups, between jobs.
- `usage`: the accounts' usage endpoint, and which account is under its caps.
- `metrics/`: what each attempt used: quota readings and attribution, tokens, attempt
  metadata, and the `quota` and `cost` reports (docs/factory-quota.md).
- `forge`: GitHub: issues for blocking flags, answers, and PRs.
- `readiness`: which mapped parishes are ready to seed.
- `report`: `status`, `queue`, `inspect`, `prompt` and the PR summary.
- `cli`: `pnpm factory`.
"""
