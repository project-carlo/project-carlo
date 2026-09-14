#!/usr/bin/env bash
# Walk through the whole argument, fast parts first.
set -euo pipefail
cd "$(dirname "$0")"

echo "############ 1. The option value, in exact arithmetic ############"
python3 -m pickem.cli toy

echo
echo "############ 2. The endgame is matching pennies ############"
python3 -m pickem.cli endgame --scores 100,104 --values 10,6 --p 0.59

echo
echo "############ 3. Strategies head to head ############"
python3 -m pickem.cli compare data/week_example.json --final-samples 6000

echo
echo "############ 4. How much confidence belongs on Monday night? ############"
echo "   (small league: not much -- big league: as much as possible)"
python3 -m pickem.cli slotvalue data/week_example.json --game MNF --entrants 4  --final-samples 4000
python3 -m pickem.cli slotvalue data/week_example.json --game MNF --entrants 25 --final-samples 4000

echo
echo "############ 5. A recommended entry, mid-week ############"
python3 -m pickem.cli recommend data/week_example_live.json --search-samples 2000 --sweeps 2 --refine 0
