# Strategy notes

## 1. The objective is not the one the game looks like it has

The scoring rule invites you to maximize expected points. The payout rule does
not. Only the single highest score each week gets paid, so what matters is

    P(my score is the maximum of the league)   (+ a share of ties)

and those two objectives disagree sharply. Sorting confidence values by win
probability — the biggest number on the biggest favorite — is exactly the entry
that maximizes expected points. In the simulated 10-entrant league it earns
**5.66% of the pot** against a fair share of 10%. It is the single worst
strategy measured here.

The reason is that maximizing expected points also *minimizes differentiation*.
Everyone can compute the market's favorites, so everyone's chalk card is nearly
the same card. If all ten entries are near-identical, the winner is decided by
the small residual differences, and you have no control over which way they
fall. You do not need a high score. You need a score higher than nine other
people's, which is a different thing and is achieved by being different in the
right direction at the right moment.

Everything below follows from that one substitution of objective.

## 2. What the rules actually give you

Three provisions do all the work:

1. **Picks are editable until five minutes before each game kicks off.** A
   confidence value sitting on a Monday night game is not a commitment. It is a
   commitment you get to reconsider six more times.
2. **Confidence values are a permutation of `1..N`.** Values spent on
   kicked-off games are frozen; the rest may be permuted freely among games
   that have not started. So your unspent values are a portfolio whose total is
   fixed but whose allocation is free.
3. **Opponents' picks become public at kickoff — and only then.** You cannot
   see what anyone did with a game before you have to commit to it yourself.
   But after kickoff you see everything, and because values are a permutation,
   seeing fifteen of an opponent's picks tells you the sixteenth by
   subtraction.

Provision 3 has a consequence worth stating on its own: **by Monday night there
is no hidden information except which side each person took.** Everyone's score
is known and everyone's stake on the last game is known.

## 3. Where the value actually is

Measured on held-out simulated weeks, 10-entrant league, fair share 10.00%:

| | EV pot share | Mean points |
|---|---|---|
| Chalk, never revisited | 6.14% | 96.1 |
| Chalk, played in-flight | 13.05% | 87.0 |
| Naive late-heavy tilt (0.4), in-flight | 10.71% | 81.2 |
| Naive late-heavy tilt (0.8), in-flight | 10.64% | 78.7 |
| Optimized card, in-flight | 17.12% | 84.2 |

(The first rows share one holdout sample; the optimized row is from
`recommend`'s own holdout, where chalk-in-flight scored 13.27% / 87.0 points,
so its deltas are quoted against that.)

**Adaptivity is worth far more than card shape.** Taking the identical chalk
card and merely playing it — revisiting sides as the deficit becomes clear —
more than doubles its value. Meanwhile the crude version of "put big numbers on
late games" *loses* 2.3 points relative to not doing it.

That deserves an explanation rather than a shrug. Tilting confidence toward
late games is not free: it means putting a 16 on a coin-flip Monday game and a
4 on an 86% Sunday favorite, and that costs real expected points. Comparing
like with like — the same in-flight policy in both cases — the naive tilt
spends 5.8 expected points (87.0 → 81.2) and gets *less* pot share for them.
The option value you buy is genuine but small; buying it indiscriminately
across the whole card overpays. The optimizer's answer is a *selective* tilt
that spends half as much, 2.8 points, and reaches 17.1%.

What the optimizer actually produces on this slate is worth looking at, because
it is not what the intuition predicts. It keeps chalk where the market is
lopsided (16 on the 86% favorite, 14 on the 78%), puts **15 on a 56% London
game and 12 on a 52% coin flip in the 1:00 wave**, and leaves Sunday night with
1 and Monday night with 5. In a ten-entrant league it differentiates on *early
coin flips*, not by hoarding for Monday. The reason is in section 3a.

So the originating intuition is right about the mechanism and wrong about the
dose. And, as the next section shows, right about the dose too — but only if
your league is big.

### 3a. The dose depends on league size, and reverses

`slotvalue` isolates the question exactly: hold the card fixed, force each
confidence value onto the Monday night game (swapping it with whichever game
held it), and re-score. Expected pot share by value placed on MNF:

| Value on MNF | 4 entrants | 10 entrants | 25 entrants |
|---|---|---|---|
| 1 | 37.4% | 12.8% | **4.15%** |
| 2 | 38.0% | 11.7% | 2.83% |
| 4 | 38.9% | 11.7% | 2.46% |
| 6 | **41.8%** | 13.1% | 2.88% |
| 8 | 40.7% | 12.1% | 2.34% |
| 10 | 39.3% | 12.3% | 2.79% |
| 12 | 35.2% | 11.1% | 3.29% |
| 14 | 32.7% | 10.8% | 3.54% |
| 16 | 29.6% | 10.7% | 3.65% |
| *fair share* | *25.0%* | *10.0%* | *4.0%* |

Three different shapes:

* **Four entrants: strongly decreasing.** Hoarding for Monday costs 12 points
  of pot share. With only three rivals you are beating specific scores, the
  maximum is not far above the mean, and expected points still pay.
* **Ten entrants: mildly decreasing.** A middling value is right.
* **Twenty-five entrants: a barbell.** Both ends beat the middle. The bar is
  the maximum of 24 draws, sitting far above any reasonable mean, so the only
  thing that wins is extreme differentiation — and there are exactly two cheap
  ways to buy it: a maximum stake on the last game, where you can choose sides
  knowing everything, or a maximum stake on an early coin flip. A middling
  value on Monday night buys neither.

(The 25-entrant differences are 1–2 standard errors apart; the *shape* is the
result, not the individual digits. The 4- and 10-entrant trends are far outside
noise.)

The practical summary: **the "load up the late games" instinct is a large-league
strategy.** In a small league it is close to backwards.

## 4. The option value, proven exactly

`python3 -m pickem.cli toy` reduces the pool to two games and the values
`{1, 2}`, against three chalk opponents, and enumerates every case in exact
rational arithmetic:

```
  where the 2 sits         commit up front    decide B on the news   option value
  EARLY game (chalk)                0.4000                  0.4000        +0.0000
  LATE game                         0.4000                  0.4600        +0.0600
```

Two things are established with no sampling error:

* The right to revise is worth **+3/50 of the pot** — a 15% relative
  improvement — when the big value is still unspent.
* It is worth **exactly zero** when the big value is already committed.

The optimal adaptive plan is also instructive:

    if the early favorite wins  -> take the UNDERDOG in the late game
    if the early favorite loses -> take the FAVORITE in the late game

That is not a prediction about the late game; the late game's probability never
changed. It is a statement about the *field*. When the chalk field cashes the
early favorite, everyone is bunched high and you must differentiate to win.
When the early favorite loses, the chalk field is damaged and you can win by
simply being correct.

## 5. The in-flight rule

This is the policy in `policy.py`, applied at every deadline:

> Project the best final score in the league. If you are ahead of it, **take
> every favorite** — correlating with the field freezes the margin, and the
> margin is yours. If you are behind it, you need a **swing**: games where you
> are on one side and the leader is on the other, so a single result moves the
> margin by your value plus theirs. Do not swing yet if you can still cover the
> gap later — waiting is free information. When you must swing, cover the
> deficit with the **fewest and likeliest** contrarian bets available, and move
> that wave's **biggest values onto exactly those games**.

"Fewest and likeliest" is the fourth-quarter logic: down three scores, you do
not want the best play, you want the play whose *distribution* reaches the
number.

Two constants were tuned by grid search (`python3 -m pickem.cli tune`):

* `cushion = 0`. The target is already the *maximum* over the field's
  projections, which sits well above any individual's mean. Adding further
  cushion on top overshoots and costs share.
* `defer_slack = 12`. The deferral test is `later_capacity >= slack × deficit`.
  Raw capacity — confidence still riding on later games — badly overstates the
  swing you can actually realize, because collecting it means *winning*
  underdog bets, each at maybe 35%. The tuned value is therefore far above 1.
  Performance is flat from about 8 upward (14.18% at 8, 14.64% at 100 — inside
  sampling noise); 12 sits in that plateau and keeps the printed threshold
  interpretable.

The practical reading of `defer_slack = 12`: **you are behind the projected
winner more often than it feels like**, because the bar is the maximum of the
whole league and not the average. Waiting for certainty means waiting until
there are too few games left to fix anything.

## 6. The endgame, solved exactly

By the last game there is no hidden information but the sides, so it is a
finite `M`-player, two-action simultaneous game and can be solved rather than
simulated. `endgame.py` does this by enumerating all `2^M` side profiles and
running damped fictitious play to a mixed equilibrium.

The structure is **matching pennies**. A trailer wants to mismatch the leader —
only opposite sides create a swing. The leader wants to match the trailer —
matching freezes a margin that is in their favor. Wanting to match while
someone wants to mismatch has no pure equilibrium.

```
$ python3 -m pickem.cli endgame --scores 100,104 --values 10,6 --p 0.59
  YOU     score 100  stake 10   P(take underdog) 55.2%   pot share 36.2%
  opp 1   score 104  stake  6   P(take underdog) 21.3%   pot share 63.8%
```

Three practical consequences:

* **If you lead, do not automatically take the favorite.** It is exploitable: a
  trailer simply takes the other side and you have handed them a free swing.
  Mix. Roughly one time in five here.
* **If you trail, check whether your stake even covers the deficit.** If it does
  not, the contrarian bet cannot win the week and you are taking variance for
  nothing — unless it reaches a tie. `endgame.deficit_threshold` is this check.
  Trailing by 12 with a 5 on the last game is worth exactly 0.00%.
* **Against opponents who do *not* mix**, exploit them directly rather than
  playing the equilibrium: `best_response()` against a leader who always takes
  the favorite returns DOG worth 41.0% versus 29.5% for the favorite.

One caveat specific to Yahoo: many leagues break ties with a Monday-night total
points guess. That converts some of the ties modelled here into outright wins
or losses and makes mirroring slightly less attractive than the split-ties
model assumes.

## 7. Is there a Nash equilibrium?

Yes, and `equilibrium.py` approximates it by **fictitious play over cards**:
maintain a population mixture, best-respond to it, fold the response back in,
repeat. Exploitability — how much a single optimizer beats `1/M` by — is the
number that matters.

Seven rounds against a 10-entrant league, starting from an all-chalk
population (`python3 -m pickem.cli equilibrium data/week_example.json`):

| Round | Best response share | Exploitability |
|---|---|---|
| 1 | 52.34% | +42.34 |
| 2 | 38.99% | +28.99 |
| 3 | 30.50% | +20.50 |
| 4 | 21.70% | +11.70 |
| 5 | 26.15% | +16.15 |
| 6 | 18.68% | +8.68 |
| 7 | 18.34% | +8.34 |

Against a field of nine identical chalk cards, a single optimizer takes **more
than half the pot**. That is the honest measure of how bad undifferentiated
play is: nine entrants playing the same card are effectively one entrant, and
beating one entrant is easy. As the population diversifies, that collapses by a
factor of five — and it is still falling when the run stops. Note round 5 going
back up: fictitious play is not monotone, and this has not converged.

The shape of the resulting population, averaged over the mixture:

| Deadline | Avg confidence | Contrarian rate |
|---|---|---|
| Thu 8:15 | 8.75 | 0.0% |
| London | 7.88 | 0.0% |
| Sun 1:00 (7 games) | 9.05 | 7.1% |
| Sun 4:05 | 4.19 | 0.0% |
| Sun 4:25 | 12.08 | 0.0% |
| SNF | 2.88 | 0.0% |
| MNF | 8.50 | 0.0% |

Even at equilibrium the population does **not** hoard confidence for Monday
night in a ten-entrant league — MNF averages 8.5, barely above the 8.5 mean of
`1..16`. It concentrates on the 4:25 wave and spreads contrarian picks across
the crowded 1:00 wave. That is consistent with section 3a: hoarding late is a
large-league play.

The shape of the result is the important part, and it is the standard shape for
this class of game. Against an undiversified field, a single optimizer is
enormously exploitative. As the population diversifies, that collapses. **The
equilibrium is a mixed strategy: there is no single best card**, and there
cannot be, because any card that everyone played would be beaten by the card
that differentiates from it. What survives is a *distribution* over cards plus
the in-flight rule.

This has a blunt practical implication. Most of the edge measured in this
document is not edge against the game; it is **edge against a field that does
not revisit its picks**. If your league ever starts playing this way, the
returns fall toward `1/M` and stay there.

Two honest limitations:

* The search is over *opening cards* with one fixed in-flight policy attached,
  not over the space of all adaptive policies. It is an equilibrium of a
  restricted game; a genuinely different in-flight rule could beat it.
* Fictitious play is a heuristic for equilibrium, not a proof of one, and the
  run above has not fully converged. The direction is informative; the final
  digit is not.

## 8. How optimal play shifts with opponent tendencies

This is the part that most deserves real data from your actual league. What the
model says, with the knob that controls it in `opponents.py`:

**League size** is the single biggest factor. Best in-flight play versus a
static chalk card, by league size:

| Entrants | Fair share | Achieved | Gain vs static chalk |
|---|---|---|---|
| 4 | 25.0% | 42.4% | +9.2 |
| 6 | 16.7% | 28.1% | +11.8 |
| 10 | 10.0% | 13.7% | +8.5 |
| 16 | 6.2% | 9.0% | +7.3 |
| 25 | 4.0% | 6.8% | +6.2 |

The *mechanism* shifts even where the gain looks similar. In a small league you
are trying to beat a handful of specific scores and expected points still
matter; near-chalk with a late hedge is close to right. In a large league the
bar is the maximum of many draws, which sits far above any sensible mean, so
you are behind essentially from kickoff and must carry variance from the start.
The tuned `defer_slack` rises with league size for exactly this reason.

**Do they revisit their picks at all?** (`adapts`) This is the tendency worth
observing first, and it is easy to observe: note each rival's picks at Sunday
1pm, then check whether their Monday-night pick is still what a chalk card
would have. Against a field that never revisits, a lead is safe and you should
protect it by mirroring. Against a field that does, **leads are not safe** —
trailers will fade you, so you must mix in the endgame rather than sit on the
favorite.

**How chalky are they?** (`temperature`) A disciplined, low-temperature field
produces tightly bunched scores, which makes differentiation cheap and
valuable: small deliberate deviations pay well. A high-temperature field
produces a scattered maximum that is hard to predict and hard to beat; you need
more variance simply to reach it, and the edge from being clever shrinks.

**Do they take underdogs?** (`upset_rate`) A field that never takes a dog leaves
the entire contrarian side of every game uncontested — fade them cheaply and
often. A field full of dog-takers means your contrarian bets are crowded, and
the favorites side becomes the differentiated one. Fade the *field*, not the
favorite; those coincide only when the field is chalky.

**Payout structure**, which is not modelled here and should be. Everything above
assumes winner-take-all. If your league pays the top two or three, the
objective becomes `P(finish top k)`, variance is much less valuable, and play
moves sharply back toward chalk. This is a one-function change in
`evaluate.py` (the share computation) and is the first thing to adjust if your
league does not actually pay only first.

**What to record in your own league**, in priority order: (1) does each rival
ever change a pick after submitting, (2) their underdog rate, (3) the rank
correlation between their confidence order and the closing market. Those three
numbers instantiate `OpponentModel` directly and are the difference between
this being calibrated and being a plausible guess.

## 9. Modelling assumptions

Stated plainly, because they bound how much to trust the numbers:

* **Market probabilities are correct.** No handicapping edge is assumed or
  used. If you have one, the algorithm exploits it automatically by feeding
  better `p_home` values.
* **Live win probability is a martingale pinned to the final result**, modelled
  as a Brownian motion renormalized by time remaining. Verified calibrated in
  the tests: games displaying a given win probability win at that rate. This is
  what lets the 4:05 decision use the fact that 1:00 games are ~80% resolved
  without pretending they are final.
* **Games are correlated within a week** via a one-factor copula (`rho = 0.15`
  by default) — some weeks favorites broadly hold, some weeks they fall.
* **Opponents react to the field leader, including us, but to a reference
  version of our card.** Recomputing the whole field for every candidate would
  be prohibitive, so the optimizer iterates best responses instead
  (`refine_passes`). The approximation is mild because our card moves the
  leader's projection only slightly.
* **Our own reference trajectory ignores our future adaptations** when the
  field is simulated. This slightly understates our projected score at early
  deadlines and so slightly overstates the deficit.
* **Ties split the pot.** See the Monday-night tiebreaker caveat above.

## 10. Making it live

The algorithm is the part that needed thought; the plumbing is not, and it is
deliberately not built yet. What it would take:

* **Odds** → `p_home`. Any moneyline feed; `probs.moneyline_to_p_home` already
  de-vigs a two-way market.
* **Scores and live win probability** → `results` and `live_win_prob`. A live
  scores feed gives results directly. Win probability either comes from the
  feed or gets computed from score, time, possession and spread.
* **Opponent picks** → `opponent_picks`, pulled from the league page after each
  kickoff. This is the only piece with no clean API, and it is the highest-value
  input: without it the engine cannot see the field and falls back to
  behavioural priors.
* **A scheduler** firing ~10 minutes before each kickoff wave, running
  `recommend` on the current state and submitting the diff.

The state file is the interface. Anything that can produce
`week_example_live.json` can drive this.

One practical note: `recommend` takes a couple of minutes at default sample
counts, so run it early enough to leave room to act. The in-flight thresholds
printed alongside the card exist precisely so that you can make the right call
in ten seconds if the deadline arrives before the optimizer does.
