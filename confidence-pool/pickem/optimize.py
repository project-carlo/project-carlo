"""Searching for the best opening card.

The decision variable is the whole entry -- which confidence value and which
side goes on every game that has not kicked off.  The search is a plain
best-improvement hill climb over two moves (swap two values, flip one side)
with a handful of seeds, which is more than enough because the objective is
smooth in the swaps and the seeds already bracket the interesting region.

Two things make this honest rather than a machine for fooling itself:

* The search optimizes the average over one **fixed** set of sampled weeks, so
  the hill climb is deterministic -- no noise-chasing, no ratcheting on lucky
  draws.
* The answer is then re-scored on an **independent, larger** set of weeks and
  both numbers are reported.  The gap between them is the overfit, and it is
  visible instead of hidden.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Callable

from .evaluate import EvalResult, Evaluator
from .model import DOG, FAV, Card, WeekState, card_from_state
from .opponents import OpponentModel, default_field
from .policy import PolicyParams, chalk_card, late_heavy_card
from .sim import Scenarios


@dataclass
class Config:
    search_samples: int = 1500
    final_samples: int = 8000
    entrants: int = 10  # league size including me
    rho: float = 0.15  # week-level correlation between favorites holding
    seed: int = 20260914
    sweeps: int = 4
    refine_passes: int = 2
    min_gain: float = 5e-4  # ignore improvements this small; they are noise
    params: PolicyParams = field(default_factory=PolicyParams)
    opponents: list[OpponentModel] | None = None
    card_sampler: "Callable[[int, Random], Card] | None" = None
    """Override how opponent cards are drawn; see :class:`Evaluator`."""

    def field_models(self, state: WeekState | None = None) -> list[OpponentModel]:
        """Behavioural models for the rest of the league.

        Entrants whose picks are already visible in ``state`` are modelled
        under their own names, so the evaluator conditions on what they have
        actually done; the rest of the league is filled in with archetypes.
        """
        if self.opponents is not None:
            return self.opponents
        archetypes = default_field(max(1, self.entrants - 1))
        names = list(state.opponents.keys()) if state is not None else []
        models: list[OpponentModel] = []
        for i, nm in enumerate(names[: self.entrants - 1]):
            a = archetypes[i % len(archetypes)]
            models.append(OpponentModel(nm, a.temperature, a.upset_rate, a.adapts, a.cushion))
        for k in range(len(models), self.entrants - 1):
            a = archetypes[k % len(archetypes)]
            models.append(OpponentModel(f"field-{k + 1}", a.temperature, a.upset_rate, a.adapts, a.cushion))
        return models


@dataclass
class OptimizeResult:
    card: Card
    search: EvalResult
    holdout: EvalResult
    chalk_card: Card
    chalk_holdout: EvalResult
    evaluations: int


def _card_from(state: WeekState, pts: dict[int, int], sides: dict[int, int]) -> Card:
    """Merge a proposed assignment for the open games with the locked ones."""
    card = card_from_state(state)
    for g, v in pts.items():
        card.points[g] = v
    for g, s in sides.items():
        card.sides[g] = s
    return card


def _seeds(state: WeekState, rng: Random) -> list[Card]:
    open_idx = state.open_indices()
    avail = state.available_points()
    p_fav = [g.p_fav for g in state.slate]
    kicks = [g.kickoff for g in state.slate]

    out: list[Card] = []
    pts, sides = chalk_card(open_idx, avail, p_fav)
    out.append(_card_from(state, pts, sides))
    for w in (0.25, 0.6, 1.0):
        pts, sides = late_heavy_card(open_idx, avail, p_fav, kicks, w)
        out.append(_card_from(state, pts, sides))

    existing = card_from_state(state)
    if all(existing.points[i] > 0 for i in range(state.slate.n)):
        out.append(existing)

    # A couple of shuffled starts so the climb is not always entering the
    # basin from the same direction.
    for _ in range(2):
        vals = list(avail)
        rng.shuffle(vals)
        pts = {g: v for g, v in zip(open_idx, vals)}
        sides = {g: FAV for g in open_idx}
        out.append(_card_from(state, pts, sides))
    return out


def _hill_climb(ev: Evaluator, card: Card, open_idx: list[int], cfg: Config) -> tuple[Card, float, int]:
    best = card.copy()
    best_val = ev.evaluate(best).ev_share
    evals = 1
    for _sweep in range(cfg.sweeps):
        improved = False
        cand_val = best_val
        cand = None

        for a_i in range(len(open_idx)):
            for b_i in range(a_i + 1, len(open_idx)):
                a, b = open_idx[a_i], open_idx[b_i]
                trial = best.copy()
                trial.points[a], trial.points[b] = trial.points[b], trial.points[a]
                v = ev.evaluate(trial).ev_share
                evals += 1
                if v > cand_val + cfg.min_gain:
                    cand_val, cand = v, trial

        for g in open_idx:
            trial = best.copy()
            trial.sides[g] = DOG if trial.sides[g] == FAV else FAV
            v = ev.evaluate(trial).ev_share
            evals += 1
            if v > cand_val + cfg.min_gain:
                cand_val, cand = v, trial

        if cand is not None:
            best, best_val, improved = cand, cand_val, True
        if not improved:
            break
    return best, best_val, evals


def optimize(state: WeekState, cfg: Config | None = None, verbose: bool = False) -> OptimizeResult:
    cfg = cfg or Config()
    missing = [
        state.slate[i].gid
        for i in state.locked_indices()
        if state.slate[i].gid not in state.my_card
    ]
    if missing:
        raise ValueError(
            "these games have already kicked off but carry no pick in my_picks, so the "
            f"confidence values they consumed are unknown: {missing}"
        )
    rng = Random(cfg.seed)
    models = cfg.field_models(state)
    open_idx = state.open_indices()

    search_sc = Scenarios(state, cfg.search_samples, cfg.rho, Random(cfg.seed + 1))
    ev = Evaluator(state, search_sc, models, cfg.params, Random(cfg.seed + 2), cfg.card_sampler)

    seeds = _seeds(state, rng)
    chalk = seeds[0]
    ev.set_reference(chalk)

    best, best_val, evals = chalk.copy(), -1.0, 0
    for i, seed in enumerate(seeds):
        cand, val, n = _hill_climb(ev, seed, open_idx, cfg)
        evals += n
        if verbose:
            print(f"  seed {i}: {val * 100:5.2f}%  ({n} evaluations)")
        if val > best_val:
            best, best_val = cand, val

    # Adaptive opponents were reacting to the chalk version of us. Re-run the
    # field against what we actually intend to do, and re-optimize. This is a
    # best-response iteration; it settles within a pass or two.
    for p in range(cfg.refine_passes):
        ev.set_reference(best)
        cand, val, n = _hill_climb(ev, best, open_idx, cfg)
        evals += n
        if verbose:
            print(f"  refine {p + 1}: {val * 100:5.2f}%  ({n} evaluations)")
        best, best_val = cand, val

    best.validate(state.slate.n)

    # Fresh, larger sample set: the number we actually believe.
    holdout_sc = Scenarios(state, cfg.final_samples, cfg.rho, Random(cfg.seed + 101))
    hev = Evaluator(state, holdout_sc, models, cfg.params, Random(cfg.seed + 102), cfg.card_sampler)
    hev.set_reference(best)
    holdout = hev.evaluate(best)
    chalk_holdout = hev.evaluate(chalk)

    return OptimizeResult(
        card=best,
        search=ev.evaluate(best),
        holdout=holdout,
        chalk_card=chalk,
        chalk_holdout=chalk_holdout,
        evaluations=evals,
    )
