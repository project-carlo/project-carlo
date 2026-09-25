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
