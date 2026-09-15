#!/usr/bin/env bash
#
# Move confidence-pool/ out of project-carlo and into its own repository,
# at that repository's root, on a branch, and open a pull request.
#
# The project is self-contained (stdlib only, no build), so the move is a file
# copy plus three small layout fixes: the README's `cd confidence-pool` line is
# no longer needed, the project needs its own .gitignore, and nothing else
# references the old path.
#
# Usage:
#   tools/extract-to-standalone-repo.sh <owner/repo> [branch]
#
# Example:
#   tools/extract-to-standalone-repo.sh lyonsl2/yahoo-picks
#
# Requires: git, and the `gh` CLI authenticated for the target repo.
# Run it from anywhere; it locates itself.

set -euo pipefail

TARGET="${1:-}"
BRANCH="${2:-claude/confidence-pool-engine}"

if [[ -z "$TARGET" ]]; then
  echo "usage: $0 <owner/repo> [branch]" >&2
  exit 2
fi

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Accept either owner/repo or a full clone URL (the latter is what the
# self-test uses, pointing at a local bare repository).
if [[ "$TARGET" == *://* || "$TARGET" == /* ]]; then
  CLONE_URL="$TARGET"
else
  CLONE_URL="https://github.com/$TARGET.git"
fi
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "==> source:  $SRC"
echo "==> target:  https://github.com/$TARGET"
echo "==> branch:  $BRANCH"

git clone "$CLONE_URL" "$WORK/repo"
cd "$WORK/repo"

# A brand new repository may have no commits at all, in which case there is no
# base for a pull request to target. Give it one.
if ! git rev-parse HEAD >/dev/null 2>&1; then
  BASE="$(git symbolic-ref --short HEAD)"
  echo "==> repository is empty; seeding base branch '$BASE'"
  printf '%s\n' '__pycache__/' '*.py[cod]' '.venv/' '.pytest_cache/' '.DS_Store' > .gitignore
  git add .gitignore
  git commit -q -m "Initialize repository"
  git push -u origin "$BASE"
else
  BASE="$(git symbolic-ref --short HEAD)"
  echo "==> base branch is '$BASE'"
fi

git checkout -q -b "$BRANCH"

# Copy the project to the repository root, skipping build detritus and this
# script (which is about the migration, not about the project).
for item in README.md STRATEGY.md demo.sh pickem data tests; do
  cp -r "$SRC/$item" .
done
find . -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true

# Layout fix: at the repository root there is no subdirectory to cd into.
if [[ -f README.md ]]; then
  perl -0pi -e 's/```bash\ncd confidence-pool\n/```bash\n/' README.md
fi

if [[ ! -f .gitignore ]]; then
  printf '%s\n' '__pycache__/' '*.py[cod]' '.venv/' '.pytest_cache/' '.DS_Store' > .gitignore
fi

echo "==> running the test suite before committing"
python3 -m unittest discover -s tests

git add -A
git commit -q -F - <<'MSG'
Confidence pool strategy engine

A strategy engine for a Yahoo-style NFL confidence pool: pick a winner in each
of ~16 games, assign each a distinct confidence value 1..N, highest weekly
score takes the payout. Picks stay editable until five minutes before each
kickoff, and opponents' picks become public at kickoff -- so the week is a
sequence of decisions under improving information, not a single guess.

Stdlib-only Python, no dependencies, no install.

The objective is expected share of the weekly pot, not expected points --
those disagree sharply, and chalk is the worst strategy measured. Candidate
cards are scored by Monte Carlo with common random numbers, rolling an
adaptive in-flight policy forward through every sampled week; local search on
top is a policy-improvement step, so the search can see the value of holding a
confidence value back. Live win probabilities are modelled as a martingale
pinned to the sampled outcome, so a 4:05 decision correctly sees the 1:00
games as mostly-but-not-fully resolved. Games are correlated within a week by
a one-factor copula.

The last game is solved exactly rather than simulated: once values are a
permutation and fifteen are public, the sixteenth is known by subtraction, so
only sides are hidden. It is matching pennies, and the equilibrium has the
leader taking the underdog ~21% of the time to avoid being exploitable.

Findings, on held-out simulated weeks (10-entrant league, fair share 10%):
  - playing the card in-flight at all: 6.14% -> 13.05%
  - a naive late-heavy tilt: 10.71%, i.e. worse than not doing it
  - optimized card: 17.12%, spending 2.8 expected points for 3.85 of share
  - the "load up the late games" instinct reverses with league size: clearly
    wrong at 4 entrants, a barbell (both extremes) at 25
A two-game pool solved in exact rational arithmetic shows the option value is
real and attributable entirely to the late slot (+3/50, vs exactly 0 when the
big value is already spent).

Fictitious play puts an optimizer at 52% of the pot against an all-chalk
field, falling to 18% after seven rounds -- most of the edge here is edge
against a field that never revisits its picks, not against the game.

Includes 46 tests covering win-probability calibration, the permutation
invariant through the rollout, opponent-belief conditioning on public picks,
and the exact endgame and toy results.
MSG

git push -u origin "$BRANCH"

gh pr create --repo "$TARGET" --base "$BASE" --head "$BRANCH" \
  --title "Confidence pool strategy engine" \
  --body-file - <<'BODY'
Seeds this repository with a strategy engine for a Yahoo-style NFL confidence
pool. Stdlib-only Python, no dependencies, no install: `python3 -m pickem.cli
recommend data/week_example.json`.

## What it does

Decides both the opening card and the in-flight adjustments, given that picks
stay editable until five minutes before each kickoff and opponents' picks
become public at kickoff.

The objective is expected **share of the pot**, not expected points. Those
disagree sharply — the entry that maximizes expected points is chalk, and
chalk is the worst strategy measured here, because everyone can compute the
market's favorites and so everyone's chalk card is nearly the same card.

## Results

Held-out simulated weeks, 10-entrant league, fair share 10%:

| Strategy | EV pot share | Mean points |
|---|---|---|
| Chalk, never revisited | 6.14% | 96.1 |
| Chalk, played in-flight | 13.05% | 87.0 |
| Naive late-heavy tilt | 10.71% | 81.2 |
| Optimized card, in-flight | 17.12% | 84.2 |

Three findings worth the reading:

1. **Playing the card in-flight is most of the edge.** The identical opening
   card more than doubles its pot share just by being revisited.
2. **A crude "big numbers on late games" tilt backfires.** The option value of
   an unspent confidence value is real — `pickem/toy.py` proves it in exact
   rational arithmetic, +3/50, and exactly **zero** when the big value is
   already spent — but it is smaller than what a global tilt costs in expected
   points.
3. **That instinct reverses with league size.** At 4 entrants hoarding for
   Monday night costs 12 points of pot share; at 25 the curve becomes a
   barbell where both extremes beat the middle. `slotvalue` measures this.

## How it works

Monte Carlo with common random numbers, rolling an adaptive policy forward
inside every sampled week; local search over opening cards on top is a
policy-improvement step. Live win probability is modelled as a martingale
pinned to the sampled outcome, so the 4:05 decision correctly sees the 1:00
games as mostly-but-not-fully resolved (tests verify calibration). The final
game is solved exactly rather than simulated — it is matching pennies, and the
leader has to mix.

`STRATEGY.md` has the reasoning, the equilibrium results, and notes on how
optimal play shifts with opponent tendencies.

## Honesty about the numbers

Search quality is reported on both the optimizer's own sample and an
independent one; the gap is overfit and it is visible rather than hidden.
Every edge is measured against a *modelled* field of plausible casual
entrants, not real data — fictitious play shows an optimizer taking 52% of the
pot against an all-chalk field and only 18% after seven rounds of the field
diversifying. Most of the edge here is edge against a field that never
revisits its picks.

## Tests

46 tests, `python3 -m unittest discover -s tests`.
BODY

echo
echo "==> done"
