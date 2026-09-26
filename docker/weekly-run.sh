#!/usr/bin/env bash
# The weekly pipeline, on the GitHub runner and in the local image:
#   get the published database -> run -> upload the result as a candidate.
# Publishing the candidate is a separate step (the workflow decides, based on
# the run's status). Exit code is the run's: 0 passed, 10 held, other = failed.
set -euo pipefail

RUN_ID="${RUN_ID:-local-$(date -u +%Y%m%dT%H%M%SZ)}"

if [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "Missing credentials: GEMINI_API_KEY is not set." >&2
  exit 1
fi

pdf() { uv run --no-sync python -m pdf_extract "$@"; }

pdf data pull --no-snapshot

run() {
  if [[ -z "${DISPLAY:-}" ]] && command -v xvfb-run >/dev/null 2>&1; then
    xvfb-run -a "$@"
  else
    "$@"
  fi
}

weekly_args=(
  weekly
  --run-id "${RUN_ID}"
  --git-sha "${GIT_SHA:-}"
  --trigger "${RUN_TRIGGER:-}"
)
# Optional manual limits. Empty (the scheduled run) refreshes every parish.
if [[ -n "${PARISHES:-}" ]]; then
  weekly_args+=(--parish "${PARISHES}")
fi
if [[ -n "${DIOCESES:-}" ]]; then
  weekly_args+=(--diocese "${DIOCESES}")
fi

set +e
run uv run --no-sync python -m pdf_extract "${weekly_args[@]}"
status=$?
set -e

# Held runs are uploaded too, so a person can inspect and publish them; a
# failed run is not, since it can't be published. Without write access (a
# local run) the outputs stay in data/out/ only.
if [[ "${CARLO_REMOTE_WRITE:-}" == "1" && ( "${status}" == 0 || "${status}" == 10 ) ]]; then
  pdf data push --run-id "${RUN_ID}" --git-sha "${GIT_SHA:-}"
fi

exit "${status}"
