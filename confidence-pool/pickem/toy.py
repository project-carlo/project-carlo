"""A two-game pool, solved exactly in rational arithmetic.

Monte Carlo is persuasive but it is not proof.  This module strips the problem
to two games and two confidence values and enumerates every outcome with
``Fraction``, so the option value of holding a big confidence value on a late
game can be read off exactly, with no sampling error anywhere.

Setup: game A kicks off first, game B second.  Confidence values are {1, 2}.
Opponents show fixed, known cards.  We compare

* **static** -- commit both sides up front, the way a card you never revisit
  behaves, and
* **adaptive** -- commit A's side up front, then pick B's side after watching A
  resolve,

across both ways of assigning the values.  The difference between the best
static card and the best adaptive card is the option value, exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from .model import DOG, FAV

FAV_LABEL = {FAV: "FAV", DOG: "DOG"}


@dataclass(frozen=True)
class ToyCard:
    pts_a: int
    side_a: int
    side_b: int

    @property
    def pts_b(self) -> int:
        return 3 - self.pts_a

    def __str__(self) -> str:
        return (
            f"A: {self.pts_a} on {FAV_LABEL[self.side_a]}, "
            f"B: {self.pts_b} on {FAV_LABEL[self.side_b]}"
        )


def _share(mine: int, others: list[int]) -> Fraction:
    best = max([mine] + others)
    if mine < best:
        return Fraction(0)
    tied = 1 + sum(1 for v in others if v == best)
    return Fraction(1, tied)


def _outcome_prob(p_a: Fraction, p_b: Fraction, a_fav: int, b_fav: int) -> Fraction:
    return (p_a if a_fav else 1 - p_a) * (p_b if b_fav else 1 - p_b)


def _score(pts_a: int, side_a: int, pts_b: int, side_b: int, a_fav: int, b_fav: int) -> int:
    total = 0
    if (side_a == FAV) == bool(a_fav):
        total += pts_a
    if (side_b == FAV) == bool(b_fav):
        total += pts_b
    return total


def _opp_scores(opps: list[ToyCard], a_fav: int, b_fav: int) -> list[int]:
    return [_score(c.pts_a, c.side_a, c.pts_b, c.side_b, a_fav, b_fav) for c in opps]


def static_value(card: ToyCard, opps: list[ToyCard], p_a: Fraction, p_b: Fraction) -> Fraction:
    total = Fraction(0)
    for a_fav, b_fav in product((1, 0), repeat=2):
        prob = _outcome_prob(p_a, p_b, a_fav, b_fav)
        mine = _score(card.pts_a, card.side_a, card.pts_b, card.side_b, a_fav, b_fav)
        total += prob * _share(mine, _opp_scores(opps, a_fav, b_fav))
    return total


def adaptive_value(
    pts_a: int, side_a: int, opps: list[ToyCard], p_a: Fraction, p_b: Fraction
) -> tuple[Fraction, dict[int, int]]:
    """Value of committing only game A, then choosing B's side on the news."""
    pts_b = 3 - pts_a
    total = Fraction(0)
    plan: dict[int, int] = {}
    for a_fav in (1, 0):
        p_branch = p_a if a_fav else 1 - p_a
        best_side, best_val = FAV, Fraction(-1)
        for side_b in (FAV, DOG):
            val = Fraction(0)
            for b_fav in (1, 0):
                prob = p_b if b_fav else 1 - p_b
                mine = _score(pts_a, side_a, pts_b, side_b, a_fav, b_fav)
                val += prob * _share(mine, _opp_scores(opps, a_fav, b_fav))
            if val > best_val:
                best_side, best_val = side_b, val
        plan[a_fav] = best_side
        total += p_branch * best_val
    return total, plan


@dataclass
class ToyReport:
    best_static: tuple[ToyCard, Fraction]
    best_adaptive: tuple[int, int, dict[int, int], Fraction]
    static_by_placement: dict[int, Fraction]
    adaptive_by_placement: dict[int, Fraction]

    @property
    def option_value(self) -> Fraction:
        return self.best_adaptive[3] - self.best_static[1]


def solve_toy(p_a: Fraction, p_b: Fraction, opps: list[ToyCard]) -> ToyReport:
    """Enumerate every card, static and adaptive, exactly.

    ``static_by_placement`` / ``adaptive_by_placement`` are keyed by where the
    **2** went: ``pts_a = 2`` means the big value sits on the early game.
    """
    best_static: tuple[ToyCard, Fraction] | None = None
    static_by: dict[int, Fraction] = {}
    for pts_a, side_a, side_b in product((1, 2), (FAV, DOG), (FAV, DOG)):
        card = ToyCard(pts_a, side_a, side_b)
        v = static_value(card, opps, p_a, p_b)
        if pts_a not in static_by or v > static_by[pts_a]:
            static_by[pts_a] = v
        if best_static is None or v > best_static[1]:
            best_static = (card, v)

    best_adaptive: tuple[int, int, dict[int, int], Fraction] | None = None
    adaptive_by: dict[int, Fraction] = {}
    for pts_a, side_a in product((1, 2), (FAV, DOG)):
        v, plan = adaptive_value(pts_a, side_a, opps, p_a, p_b)
        if pts_a not in adaptive_by or v > adaptive_by[pts_a]:
            adaptive_by[pts_a] = v
        if best_adaptive is None or v > best_adaptive[3]:
            best_adaptive = (pts_a, side_a, plan, v)

    assert best_static is not None and best_adaptive is not None
    return ToyReport(best_static, best_adaptive, static_by, adaptive_by)


def chalk_opponent(p_a: Fraction, p_b: Fraction) -> ToyCard:
    """The textbook card: 2 on the bigger favorite, favorites on both."""
    return ToyCard(2 if p_a >= p_b else 1, FAV, FAV)
