"""Where does this end up if everybody plays well?

The whole strategy depends on what the rest of the league does, which is
circular: the right amount of deferral depends on how much the field defers.
The non-circular version of the question is the symmetric Nash equilibrium --
a way of playing such that, if everyone plays it, nobody can do better by
deviating.

This solves it by **fictitious play over cards**.  Keep a population mixture
over entries.  Each round, compute a best response to the current mixture and
fold it into the mixture with weight ``1/t``.  If the best response stops being
able to beat ``1/M``, the mixture is (approximately) an equilibrium: the
league has no exploitable tendency left.

The number to watch is **exploitability** -- how much a single optimizing
entrant beats their fair share by.  Against a naive field it is large; at
equilibrium it goes to zero.  That difference is the honest measure of how much
of the edge here is strategy and how much is just other people playing badly.

Caveat worth stating plainly: this searches over the space of *opening cards*
with the in-flight policy of :mod:`pickem.policy` bolted on, not over the space
of all possible adaptive policies.  So it is an equilibrium of a restricted
game.  A genuinely different in-flight rule could in principle beat it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from random import Random

from .model import DOG, FAV, Card, WeekState
from .opponents import OpponentModel
from .optimize import Config, optimize


@dataclass
class EquilibriumRound:
    index: int
    best_response_share: float
    exploitability: float
    card: Card


@dataclass
class EquilibriumReport:
    rounds: list[EquilibriumRound]
    pool: list[Card]
    weights: list[float]
    fair_share: float

    @property
    def final_exploitability(self) -> float:
        return self.rounds[-1].exploitability if self.rounds else float("nan")

    def mixture_summary(self, state: WeekState) -> list[tuple[str, float, float]]:
        """Average confidence value and contrarian rate per kickoff wave.

        This is the readable shape of the equilibrium: which slots the
        population puts its big numbers on, and how often it fades favorites.
        """
        waves = state.slate.waves()
        out = []
        for t, idx in waves:
            tot_pts = 0.0
            tot_dog = 0.0
            for card, w in zip(self.pool, self.weights):
                for g in idx:
                    tot_pts += w * card.points[g]
                    tot_dog += w * (1.0 if card.sides[g] == DOG else 0.0)
            label = state.slate[idx[0]].kickoff_str()
            out.append((label, tot_pts / len(idx), tot_dog / len(idx)))
        return out


def fictitious_play(
    state: WeekState,
    base_cfg: Config,
    rounds: int = 6,
    seed: int = 99,
    verbose: bool = False,
) -> EquilibriumReport:
    rng = Random(seed)
    entrants = base_cfg.entrants
    fair = 1.0 / entrants

    # Seed the population with chalk, which is where a real league starts.
    from .policy import chalk_card

    p_fav = [g.p_fav for g in state.slate]
    pts, sides = chalk_card(state.open_indices(), state.available_points(), p_fav)
    seed_card = Card([pts.get(i, 0) for i in range(state.slate.n)], [sides.get(i, FAV) for i in range(state.slate.n)])
    for gid, (v, s) in state.my_card.items():
        i = state.slate.index[gid]
        seed_card.points[i], seed_card.sides[i] = v, s

    pool: list[Card] = [seed_card]
    weights: list[float] = [1.0]
    history: list[EquilibriumRound] = []

    for t in range(1, rounds + 1):
        snapshot = list(pool)
        snap_w = list(weights)
        cum: list[float] = []
        acc = 0.0
        for w in snap_w:
            acc += w
            cum.append(acc)

        def sampler(_j: int, r: Random, _cum=cum, _snap=snapshot, _tot=acc) -> Card:
            x = r.random() * _tot
            for k, c in enumerate(_cum):
                if x <= c:
                    return _snap[k].copy()
            return _snap[-1].copy()

        # Everyone in the field plays the population mixture, adaptively.
        models = [
            OpponentModel(name=f"eq-{j}", temperature=0.0, upset_rate=0.0, adapts=True, cushion=base_cfg.params.cushion)
            for j in range(entrants - 1)
        ]
        cfg = Config(
            search_samples=base_cfg.search_samples,
            final_samples=base_cfg.final_samples,
            entrants=entrants,
            rho=base_cfg.rho,
            seed=base_cfg.seed + 1000 * t,
            sweeps=base_cfg.sweeps,
            refine_passes=base_cfg.refine_passes,
            min_gain=base_cfg.min_gain,
            params=base_cfg.params,
            opponents=models,
            card_sampler=sampler,
        )
        res = optimize(state, cfg)
        br_share = res.holdout.ev_share
        history.append(EquilibriumRound(t, br_share, br_share - fair, res.card))
        if verbose:
            print(
                f"  round {t}: best response {br_share * 100:5.2f}%  "
                f"(fair {fair * 100:.2f}%)  exploitability {(br_share - fair) * 100:+5.2f} pts"
            )

        # Fictitious-play update: fold the best response into the population.
        # Fictitious play: the new response enters with weight 1/(t+1) and the
        # incumbents are scaled down to make room. Weights stay normalized.
        pool.append(res.card)
        step = 1.0 / (t + 1.0)
        weights = [w * (1.0 - step) for w in weights] + [step]

    return EquilibriumReport(history, pool, weights, fair)
