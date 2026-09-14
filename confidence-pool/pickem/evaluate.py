"""Scoring a candidate entry against a simulated league.

The objective is **expected share of the weekly pot**, not expected score.
Those two come apart badly: the entry that maximizes expected points is chalk,
and chalk loses a winner-take-all pool to whoever got differentiated and lucky.
What matters is the probability of finishing strictly first, plus a split of
the ties.

Every candidate entry is scored against the *same* sampled weeks and the *same*
sampled opponent cards (common random numbers), so two candidates differing by
a single swap are compared on identical luck.  That turns a noisy absolute
estimate into a much sharper paired comparison, which is what the local search
actually consumes.

One deliberate approximation: adaptive opponents react to the field leader, and
the field leader might be us, so strictly their behaviour depends on our own
candidate.  Recomputing the whole field for every candidate would be
prohibitive, so opponents react to a *reference* version of our entry, and the
optimizer re-runs the field against its own answer for a couple of passes
(``refine_passes``).  That is a best-response iteration and it converges fast,
because our card moves the leader's projection only slightly.
"""

from __future__ import annotations

from array import array
from dataclasses import dataclass
from random import Random
from typing import Callable

from .model import FAV, Card, WeekState
from .opponents import OpponentModel, sample_card
from .policy import PolicyParams, revise_wave
from .sim import Scenarios


@dataclass
class EvalResult:
    ev_share: float
    p_win: float  # strictly first
    p_tie: float
    mean_score: float
    sd_score: float

    def __str__(self) -> str:
        return (
            f"EV share {self.ev_share * 100:5.2f}%  "
            f"P(win outright) {self.p_win * 100:5.2f}%  "
            f"mean score {self.mean_score:5.1f}"
        )


class Evaluator:
    def __init__(
        self,
        state: WeekState,
        scenarios: Scenarios,
        opp_models: list[OpponentModel],
        params: PolicyParams,
        rng: Random,
        card_sampler: "Callable[[int, Random], Card] | None" = None,
    ):
        """``card_sampler(j, rng)`` overrides how opponent ``j``'s card is drawn.

        Defaults to sampling from that opponent's behavioural model, which is
        what you want against a real league.  The equilibrium solver passes a
        sampler that draws from the current population mixture instead.
        """
        self.state = state
        self.sc = scenarios
        self.models = opp_models
        self.params = params
        self.M = len(opp_models)
        S, G, E = scenarios.S, scenarios.G, scenarios.E
        self.S, self.G, self.E = S, G, E

        slate = state.slate
        self.p_fav = [g.p_fav for g in slate]
        self.kickoffs = [g.kickoff for g in slate]

        # --- structural precomputation -----------------------------------
        # Games already under way when this decision is being made.
        self.started_now = [i for i in range(G) if state.has_started(i)]
        self.open_idx = state.open_indices()

        # For each remaining deadline: what is decidable, what is running, and
        # what is still in the future.
        self.wave: list[list[int]] = []
        self.started_by: list[list[int]] = []
        self.later: list[list[int]] = []
        self.not_started: list[list[int]] = []
        for e, t in enumerate(scenarios.epochs):
            dt = scenarios.decision_times[e]
            self.wave.append([i for i in range(G) if abs(self.kickoffs[i] - t) < 1.0])
            self.started_by.append([i for i in range(G) if self.kickoffs[i] <= dt])
            self.not_started.append([i for i in range(G) if self.kickoffs[i] > dt])
            self.later.append([i for i in range(G) if self.kickoffs[i] > t + 1.0])
        # Fixed for the week: each wave ordered by ascending favorite
        # probability, i.e. cheapest contrarian bet first.
        self.wave_order = [sorted(w, key=lambda g: self.p_fav[g]) for w in self.wave]
        # Favorite probabilities of the not-yet-started games at each deadline,
        # best first. Used to infer what an opponent's unspent confidence
        # values are worth without looking at picks we cannot legally see.
        self.p_sorted = [sorted((self.p_fav[g] for g in ns), reverse=True) for ns in self.not_started]

        # --- opponent cards ----------------------------------------------
        # Conditioned on their locked picks, which are public once a game starts.
        self.opp_pts = array("b", bytes(S * self.M * G))
        self.opp_sides = bytearray(S * self.M * G)
        if card_sampler is None:
            def card_sampler(j: int, r: Random) -> Card:  # type: ignore[misc]
                model = self.models[j]
                return sample_card(model, state, state.opponents.get(model.name, {}), r)

        for j, model in enumerate(self.models):
            for s in range(S):
                card = card_sampler(j, rng)
                base = (s * self.M + j) * G
                for g in range(G):
                    self.opp_pts[base + g] = card.points[g]
                    self.opp_sides[base + g] = card.sides[g]

        self.opp_final = array("i", bytes(4 * S * self.M))
        self.opp_max = array("i", bytes(4 * S))
        self.opp_ties = array("i", bytes(4 * S))
        self.target = array("d", [0.0]) * (S * E)  # projected score to beat, per epoch
        self._reference_set = False

    # ------------------------------------------------------------------
    def set_reference(self, card: Card) -> None:
        """Simulate the field, with adaptive opponents reacting to ``card``.

        Produces, per sample: every opponent's final score, the field maximum,
        the number of opponents tied at it, and -- for each future deadline --
        the score we should be trying to beat.
        """
        my_proj = self._trajectory(card)  # our projected total at each deadline
        S, G, E, M = self.S, self.G, self.E, self.M
        sc = self.sc
        wp = sc.wp
        opp_pts, opp_sides = self.opp_pts, self.opp_sides
        p_fav = self.p_fav
        params = self.params
        adaptive = [m.adapts for m in self.models]
        cushions = [m.cushion for m in self.models]

        for s in range(S):
            sbase = s * M * G
            # Working cards for this sample (adaptive opponents mutate theirs).
            pts = [[opp_pts[sbase + j * G + g] for g in range(G)] for j in range(M)]
            sides = [[opp_sides[sbase + j * G + g] for g in range(G)] for j in range(M)]

            # Each opponent's unspent confidence values, biggest first. Public
            # knowledge: the values are a permutation, so what they have locked
            # determines what they still hold.
            remaining = [sorted((pts[j][g] for g in self.open_idx), reverse=True) for j in range(M)]

            # Running "not started yet" expectation, one per opponent.
            not_started = [0.0] * M
            for j in range(M):
                pj, sj = pts[j], sides[j]
                tot = 0.0
                for g in self.open_idx:
                    pf = p_fav[g]
                    tot += pj[g] * (pf if sj[g] == FAV else 1.0 - pf)
                not_started[j] = tot

            for e in range(E):
                wbase = (s * E + e) * G
                started = self.started_by[e]
                wave = self.wave[e]
                later = self.later[e]

                proj = [0.0] * M
                for j in range(M):
                    pj, sj = pts[j], sides[j]
                    tot = not_started[j]
                    for g in started:
                        q = wp[wbase + g]
                        tot += pj[g] * (q if sj[g] == FAV else 1.0 - q)
                    proj[j] = tot

                # The score to beat, built only from what is actually public
                # at this deadline: an opponent's picks on started games, plus
                # their unspent confidence values -- known exactly, since the
                # values are a permutation -- laid out chalk-fashion over the
                # games still to come. Using their sampled future picks here
                # would be clairvoyance: nobody can see those yet.
                ps = self.p_sorted[e]
                best_now = -1e18
                for j in range(M):
                    pj, sj = pts[j], sides[j]
                    seen = 0.0
                    for g in started:
                        q = wp[wbase + g]
                        seen += pj[g] * (q if sj[g] == FAV else 1.0 - q)
                    vals = remaining[j]
                    inferred = 0.0
                    for k in range(len(vals)):
                        inferred += vals[k] * ps[k]
                    tot = seen + inferred
                    if tot > best_now:
                        best_now = tot
                self.target[s * E + e] = best_now

                if not wave:
                    continue

                # Each adaptive opponent chases the best score that is not theirs.
                mine = my_proj[s * E + e]
                best = second = -1e18
                for v in proj:
                    if v > best:
                        second, best = best, v
                    elif v > second:
                        second = v
                for j in range(M):
                    if not adaptive[j]:
                        continue
                    rival = second if proj[j] >= best else best
                    if mine > rival:
                        rival = mine
                    pj, sj = pts[j], sides[j]
                    before = 0.0
                    for g in wave:
                        pf = p_fav[g]
                        before += pj[g] * (pf if sj[g] == FAV else 1.0 - pf)
                    capacity = sum(pj[g] for g in later)
                    jp = PolicyParams(
                        cushion=cushions[j],
                        defer_slack=params.defer_slack,
                        swing_multiplier=params.swing_multiplier,
                    )
                    revise_wave(wave, self.wave_order[e], pj, sj, rival + jp.cushion - proj[j], capacity, jp)
                    after = 0.0
                    for g in wave:
                        pf = p_fav[g]
                        after += pj[g] * (pf if sj[g] == FAV else 1.0 - pf)
                    not_started[j] += after - before

                for j in range(M):
                    sj = sides[j]
                    for g in wave:
                        pf = p_fav[g]
                        not_started[j] -= pts[j][g] * (pf if sj[g] == FAV else 1.0 - pf)
                        remaining[j].remove(pts[j][g])  # those values are spent now

            # Final scores for this sample.
            fbase = s * G
            best = -1
            ties = 0
            for j in range(M):
                pj, sj = pts[j], sides[j]
                total = 0
                for g in range(G):
                    if (sj[g] == FAV) == bool(sc.fav_win[fbase + g]):
                        total += pj[g]
                self.opp_final[s * M + j] = total
                if total > best:
                    best, ties = total, 1
                elif total == best:
                    ties += 1
            self.opp_max[s] = best
            self.opp_ties[s] = ties

        self._reference_set = True

    # ------------------------------------------------------------------
    def _trajectory(self, card: Card) -> array:
        """Our projected total at each deadline, under the rollout policy."""
        S, G, E = self.S, self.G, self.E
        out = array("d", [0.0]) * (S * E)
        wp = self.sc.wp
        p_fav = self.p_fav
        for s in range(S):
            pts = list(card.points)
            sides = list(card.sides)
            for e in range(E):
                wbase = (s * E + e) * G
                tot = 0.0
                for g in range(G):
                    if self.kickoffs[g] > self.sc.decision_times[e]:
                        pf = p_fav[g]
                        tot += pts[g] * (pf if sides[g] == FAV else 1.0 - pf)
                    else:
                        q = wp[wbase + g]
                        tot += pts[g] * (q if sides[g] == FAV else 1.0 - q)
                out[s * E + e] = tot
        return out

    # ------------------------------------------------------------------
    def evaluate(self, card: Card) -> EvalResult:
        """Play ``card`` forward through every sampled week under the policy."""
        if not self._reference_set:
            raise RuntimeError("call set_reference() before evaluate()")
        S, G, E = self.S, self.G, self.E
        sc = self.sc
        wp = sc.wp
        fav_win = sc.fav_win
        p_fav = self.p_fav
        params = self.params
        cushion = params.cushion
        target = self.target
        opp_max, opp_ties = self.opp_max, self.opp_ties
        waves, orders, started_by, laters = self.wave, self.wave_order, self.started_by, self.later

        total_share = 0.0
        wins = 0
        ties_hit = 0
        score_sum = 0.0
        score_sq = 0.0
        base_points = card.points
        base_sides = card.sides

        # Expected contribution of the games that have not kicked off yet,
        # under the opening card. Maintained incrementally as waves lock.
        ns0 = 0.0
        for g in self.not_started[0] if E else []:
            pf = p_fav[g]
            ns0 += base_points[g] * (pf if base_sides[g] == FAV else 1.0 - pf)

        for s in range(S):
            pts = list(base_points)
            sides = list(base_sides)
            ns_sum = ns0

            for e in range(E):
                wave = waves[e]
                wbase = (s * E + e) * G
                started = 0.0
                for g in started_by[e]:
                    q = wp[wbase + g]
                    started += pts[g] * (q if sides[g] == FAV else 1.0 - q)
                if not wave:
                    continue

                before = 0.0
                for g in wave:
                    pf = p_fav[g]
                    before += pts[g] * (pf if sides[g] == FAV else 1.0 - pf)

                deficit = target[s * E + e] + cushion - (started + ns_sum)
                capacity = 0.0
                for g in laters[e]:
                    capacity += pts[g]
                revise_wave(wave, orders[e], pts, sides, deficit, capacity, params)

                # This wave is now locked, so it leaves the not-started pool
                # carrying whatever contribution it had when we entered.
                ns_sum -= before

            fbase = s * G
            score = 0
            for g in range(G):
                if (sides[g] == FAV) == bool(fav_win[fbase + g]):
                    score += pts[g]

            score_sum += score
            score_sq += score * score
            best = opp_max[s]
            if score > best:
                total_share += 1.0
                wins += 1
            elif score == best:
                total_share += 1.0 / (1 + opp_ties[s])
                ties_hit += 1

        mean = score_sum / S
        var = max(0.0, score_sq / S - mean * mean)
        return EvalResult(
            ev_share=total_share / S,
            p_win=wins / S,
            p_tie=ties_hit / S,
            mean_score=mean,
            sd_score=var**0.5,
        )
