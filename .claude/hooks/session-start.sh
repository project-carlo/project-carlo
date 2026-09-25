#!/bin/bash
# Installs the Python and JavaScript dependencies that a fresh Claude Code on
# the web container starts without, so pytest, ruff, eslint, vitest, tsc and
# vite resolve on the first turn instead of failing on a missing module.
set -euo pipefail

# Local checkouts already have their dependencies; only remote sessions start bare.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

# Python: pdf_extract plus pytest and ruff from the dev group.
uv sync --group dev

# JavaScript: pnpm-workspace.yaml pulls in apps/web.
# Not --frozen-lockfile, so a cached container can reuse the store on re-runs.
pnpm install

# Note: this does not run `playwright install`. The image ships browsers at
# $PLAYWRIGHT_BROWSERS_PATH, and cdn.playwright.dev is blocked by the egress
# policy, so `pnpm test:e2e` needs that host allowed for the environment.

# Data: the pipeline database and frontend snapshot are not in git. Pull the
# published copy when this environment has (read-only) R2 credentials; never
# fail the session over it.
# A database without a schema version was built by the old pipeline and must be replaced.
schema_version() {
  uv run python -c "import sqlite3; print(sqlite3.connect('data/parish_events.db').execute('pragma user_version').fetchone()[0])" 2>/dev/null || echo 0
}
if [ -n "${R2_ACCESS_KEY_ID:-}" ] && { [ ! -f data/parish_events.db ] || [ "$(schema_version)" = "0" ]; }; then
  uv run python -m pdf_extract data pull --log-level WARNING >/dev/null \
    || echo "session-start: data pull failed; run 'pnpm data:pull' to retry" >&2
fi
