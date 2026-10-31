"""The onboarding factory: agent jobs, scheduled by code, that take a diocese from nothing
to seeded parishes. The design is docs/factory-spec.md.

- `config`: the caps and limits (`factory/config.yaml`) and this machine's accounts and
  paths (`data/factory/local.yaml`).
- `stages`: the stage specs in `factory/stages/`.
- `handoff`: what a worker writes at the end of its job, and its check.
- `ledger`: SQLite state: Runs, jobs, attempts, steps, gates, flags, decisions.
- `git`: the Run's branch and worktree: commits, pushes, merging main.
- `gates`: the checks run after every job.
- `usage`: the two accounts' 5-hour and weekly limits.
- `workers`: the Agent SDK worker, and the stub worker the tests use.
- `inputs`: the prompt each job starts from, built in code.
- `playbook`: what the dispatcher appends to `diocese.md`.
- `plan`: which job a Run needs next.
- `forge`: GitHub: issues for blocking flags, answers, and PRs.
- `readiness`: which mapped parishes are ready to seed.
- `dispatcher`: picks, starts and finishes jobs.
- `report`: `status`, `inspect`, `cost` and the PR summary.
- `cli`: `pnpm factory`.
"""
