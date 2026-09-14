# Confidence pool strategy engine

An algorithm for a Yahoo-style NFL **confidence pool**: every week you pick a
winner in each of the ~16 games and assign each game a distinct confidence
value from 1 to N. Your score is the sum of the values on the games you got
right, and the highest weekly score takes the payout.

The interesting part is not picking winners. It is that **picks stay editable
until five minutes before each game kicks off**, and **everyone's picks on a
game become public the moment it starts**. That turns a single guess into a
week-long sequence of decisions made under steadily improving information, and
it is where essentially all of the edge lives.

Pure stdlib Python, no dependencies, no install:

```bash
cd confidence-pool
python3 -m pickem.cli recommend data/week_example.json
python3 -m pickem.cli toy
python3 -m unittest discover -s tests
```

## The short version of the answer

Three separate things were measured, and they are worth very different amounts.
All figures are expected share of the weekly pot in a simulated 10-entrant
league, where **10.00% is a fair share**, scored on held-out simulated weeks:

| Strategy | EV pot share | P(win) | Mean points |
|---|---|---|---|
| Chalk card, never revisited | 6.14% | 3.99% | 96.1 |
| Chalk card, played in-flight | 13.05% | 11.91% | 87.0 |
| Naive late-heavy tilt (0.4), in-flight | 10.71% | 10.09% | 81.2 |
| Naive late-heavy tilt (0.8), in-flight | 10.64% | 10.11% | 78.7 |
| **Optimized card, played in-flight** | **17.12%** | **15.59%** | 84.2 |

The first four rows share one holdout sample; the optimized row comes from
`recommend`'s own holdout (a different seed), where chalk-in-flight scored
13.27% / 87.0 points. Deltas quoted below for the optimized card are computed
within that run.

1. **Playing in-flight at all is the whole ballgame.** Revisiting the identical
   opening card as results land more than doubles its pot share (6.1% → 13.1%).
2. **Crudely front-loading confidence onto late games backfires.** The option
   value of an unspent big value is real — proven exactly below — but it is
   *smaller* than the expected-points cost of a global tilt. Against the same
   card played the same way, the naive tilt spends 5.8 expected points (87.0 →
   81.2) and *loses* 2.3 points of pot share for them.
3. **The right tilt is selective**, and worth finding: the optimized card
   spends half as much — 2.8 expected points — and gains 3.85 points of share.

So the intuition that started this is right about the mechanism and wrong about
the dose — **and how big the right dose is depends almost entirely on how many
people are in your league** (see below).

### How much confidence should actually go on Monday night?

`slotvalue` answers this directly: force each value onto MNF, swap it with
whichever game held it, re-score. The answer reverses with league size.

| Value on MNF | 4-entrant league | 10-entrant league | 25-entrant league |
|---|---|---|---|
| 1 | 37.4% | 12.8% | **4.15%** |
| 6 | **41.8%** | 13.1% | 2.88% |
| 8 | 40.7% | 12.1% | 2.34% |
| 12 | 35.2% | 11.1% | 3.29% |
| 16 | 29.6% | 10.7% | 3.65% |
| *fair share* | *25%* | *10%* | *4%* |

* **Small league (4):** hoarding is clearly wrong. A 16 on Monday night costs
  12 points of pot share versus a 6. Expected points still matter, because you
  only have to beat three specific scores.
* **Ten-entrant league:** mildly downward. A middling value is right; the big
  numbers belong on the big favorites.
* **Large league (25):** the curve becomes a **barbell** — both extremes beat
  the middle. You need extreme differentiation, and the two ways to get it are
  a maximum stake on the last game or a maximum stake on an early coin flip.
  A middling value on Monday night is the one thing that is definitely wrong.
  (Differences here are 1–2 standard errors; the shape is the finding, not the
  digits.)

So the original intuition is a **large-league strategy**. It is close to
backwards in a small one.

### Proof that the option is real

`python3 -m pickem.cli toy` solves a two-game, two-value pool in exact rational
arithmetic — no sampling anywhere:

```
  where the 2 sits         commit up front    decide B on the news   option value
  EARLY game (chalk)                0.4000                  0.4000        +0.0000
  LATE game                         0.4000                  0.4600        +0.0600
```

The right to change your mind is worth **+0.06 of the pot when the big value is
still unspent, and exactly zero when it is not**. That is the mechanism, with
no Monte Carlo error and nothing to argue with.

### The endgame is matching pennies, and the leader has to mix

By Monday night, confidence values are a permutation of `1..N` and fifteen of
everyone's sixteen are public — so the sixteenth is known by subtraction.
Every entrant knows every other entrant's score *and* their stake. Only the
sides are hidden. That is a finite simultaneous-move game, solvable exactly:

```
$ python3 -m pickem.cli endgame --scores 100,104 --values 10,6 --p 0.59

  entrant     score  stake    max    P(take underdog)   pot share
  YOU           100     10    110               55.2%       36.2%
  opp 1         104      6    110               21.3%       63.8%
```

The trailing player fades the leader — but **the leader takes the underdog 21%
of the time too**, not from a read, but because a leader who always takes the
favorite is trivially exploited by the trailer taking the other side.

### What it does when you are losing

`data/week_example_live.json` freezes the week at 4:00pm Sunday. Six games are
final, three are still being played, nine confidence values are spent, and one
rival is 19 points clear. `recommend` on that state produces:

```
  Sun 20:05Z    DEN@LV       DEN (fav)       15     53%      <- biggest value left,
  Sun 20:25Z    HOU@KC        KC (fav)        6     81%         on the closest game
  Mon 00:20Z    BAL@DET      DET (fav)       13     53%
  Tue 00:15Z    LAC@CIN      LAC (DOG)       11     41%      <- deliberately fading
```

Nobody told it to do that. Behind by 19 with seven games left, it moves its
largest remaining values onto the two games closest to a coin flip and takes
the underdog outright on Monday night — because from 19 back, the favorite
cannot win the week and a 41% shot can. Expected share 4.95% against 3.66% for
chalk; both are below the 10% fair share, which is correct. You are losing.
The algorithm cannot fix that, only play it properly.

## Commands

| Command | What it does |
|---|---|
| `recommend WEEK.json` | Optimize an entry, print it plus the in-flight decision thresholds |
| `compare WEEK.json` | Score fixed strategies head-to-head on common random numbers |
| `toy` | Exact two-game demonstration of the option value |
| `slotvalue WEEK.json --game MNF` | Marginal value of the confidence on one game |
| `endgame --scores ... --values ... --p ...` | Solve the final game exactly |
| `equilibrium WEEK.json` | Fictitious play toward a symmetric Nash equilibrium |
| `tune WEEK.json` | Grid-search the two policy constants |

Useful flags: `--entrants` (league size — this matters a lot, see STRATEGY.md),
`--rho` (how correlated favorites are week to week), `--search-samples`,
`--final-samples`.

## Input format

```json
{
  "now": "2026-09-20T16:00:00-04:00",
  "games": [
    {"id": "MNF", "away": "LAC", "home": "CIN",
     "kickoff": "2026-09-21T20:15:00-04:00", "p_home": 0.59}
  ],
  "results":       {"TNF": 1},
  "live_win_prob": {"E3": 0.22},
  "my_picks":        {"TNF": {"team": "BUF", "points": 12}},
  "opponent_picks": {"Dana": {"TNF": {"team": "MIA", "points": 4}}}
}
```

* `p_home` may be replaced by `home_ml` / `away_ml` American moneylines, which
  get de-vigged automatically.
* `results` uses `1` for "the favorite won" (or name the winning team).
* `live_win_prob` is the favorite's current win probability for games being
  played right now — this is what lets the 4:05pm decision use the fact that
  the 1:00pm games are three quarters old but not final.
* `opponent_picks` should contain only picks that are already public. The
  engine infers the rest: because values are a permutation, an opponent's
  locked picks reveal exactly which values they still hold.

`data/week_example.json` is a full pre-kickoff week.
`data/week_example_live.json` is the same week frozen at 4:00pm Sunday with six
games final, three in progress, and nine confidence values already spent.

## How it works

```
probs.py       odds -> de-vigged probabilities; normal CDF/inverse
model.py       games, slates, cards, week state; the rules of the pool
sim.py         Monte Carlo weeks: outcomes AND live win-probability paths
opponents.py   behavioural models of the rest of the league
policy.py      the in-flight decision rule, rolled out inside every sample
evaluate.py    scores a candidate entry against simulated leagues (CRN)
optimize.py    local search over opening cards
endgame.py     exact solution of the final game
equilibrium.py fictitious play toward a symmetric equilibrium
toy.py         exact two-game pool in rational arithmetic
cli.py         command line
```

The core loop is **approximate dynamic programming by rollout**. Evaluating a
candidate card plays it forward through each sampled week, applying the
in-flight policy at every future deadline; the local search on top is then a
policy-improvement step. The search only sees the value of holding a big value
back because the rollout is what eventually spends it.

Two modelling choices carry most of the realism:

* **Live win probability is a martingale pinned to the outcome.** Each game's
  result is driven by a latent Brownian motion; the on-screen win probability
  partway through is that motion renormalized by the time remaining. Sampling
  the terminal value first and bridging back keeps path and result consistent.
  This is what makes "the 1:00pm games are 80% resolved but not final when the
  4:05 lock hits" a modelled fact rather than a hand-wave. Verified calibrated:
  games showing 50% win 50% of the time.
* **Games are correlated within a week** through a one-factor copula — some
  weeks favorites broadly hold and everyone bunches up, some weeks they fall
  and the field scatters. This matters because bunching is what makes
  differentiation cheap.

## Honesty about the numbers

* Search quality is reported twice — on the sample set the optimizer used, and
  on an independent larger one. The gap is overfit, and at low sample counts it
  is large (4.6 points of pot share at 1200 samples, 2.1 at 3000). Do not trust
  the search figure.
* Every edge quoted here is measured **against the modelled field**
  (`opponents.py`), which is a plausible casual league: mostly near-chalk
  entrants who never revisit their card, a couple of sharper ones. Against a
  league that all plays this way, the edge collapses. `equilibrium` measures
  that directly: against nine identical chalk cards a single optimizer takes
  **52%** of the pot, and seven rounds of fictitious play drive that down to
  **18%** and still falling. Most of the edge here is edge against a field
  that does not revisit its picks, not edge against the game.
* The opponent behaviour model is the weakest link. It is a guess at how people
  play, not a fit to data. STRATEGY.md lists which of its parameters actually
  move the answer, so you know what to observe in your own league.

See **[STRATEGY.md](STRATEGY.md)** for the reasoning, the equilibrium results,
and how optimal play shifts with opponent tendencies.
