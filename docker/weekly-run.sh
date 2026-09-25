#!/usr/bin/env bash
# The weekly pipeline inside the container:
#   get the published database -> run -> upload the result as a candidate.
# Publishing the candidate is a separate step (the workflow decides, based on
# the run's status). Exit code is the run's: 0 passed, 2 held, other = failed.
set -euo pipefail

RUN_ID="${RUN_ID:-local-$(date -u +%Y%m%dT%H%M%SZ)}"

if [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "Missing credentials: GEMINI_API_KEY is not set." >&2
  exit 1
fi

pdf() { uv run --no-sync python -m pdf_extract "$@"; }

if [[ -n "${LEGACY_DATA_DIR:-}" ]]; then
  echo "Bootstrapping the database from the legacy JSON files in ${LEGACY_DATA_DIR}"
  pdf data import-legacy --dir "${LEGACY_DATA_DIR}"
else
  pdf data pull --no-snapshot
fi

run() {
  if [[ -z "${DISPLAY:-}" ]] && command -v xvfb-run >/dev/null 2>&1; then
    xvfb-run -a "$@"
  else
    "$@"
  fi
}

set +e
run uv run --no-sync python -m pdf_extract weekly \
  --run-id "${RUN_ID}" --git-sha "${GIT_SHA:-}" --trigger "${RUN_TRIGGER:-}"
status=$?
set -e

# Held runs are uploaded too, so a person can inspect and publish them.
if [[ -f "data/out/${RUN_ID}/frontend.snapshot" ]]; then
  pdf data push --run-id "${RUN_ID}" --git-sha "${GIT_SHA:-}"
fi

exit "${status}"
