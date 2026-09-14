"""The last game, solved exactly.

By Monday night everything except one game is settled, and something unusual
happens: confidence values are a permutation of ``1..N``, so once fifteen of an
opponent's sixteen values are public, the sixteenth is known by subtraction.
Every entrant therefore knows every other entrant's score *and* exactly how
many points is riding on the final game.  The only hidden variable left is
which side each of them took.

That makes the endgame a finite simultaneous-move game: ``M`` players, two
actions each, payoffs given by the pot split.  It can be solved exactly rather
than simulated, and the solution is not "take the favorite".

The structure is matching pennies.  A trailing player wants to be on the
opposite side from the leader (only an opposite side creates a swing).  The
leader wants to be on the *same* side as the trailer (matching sides freezes
the margin, and the margin is in the leader's favor).  Wanting to match while
someone else wants to mismatch has no pure equilibrium, so the equilibrium is
mixed -- the leader should sometimes take the underdog, not out of a read, but
to stop being predictable.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import DOG, FAV


@dataclass
class EndgameSolution:
    dog_prob: list[float]  # equilibrium probability each entrant takes the underdog
    value: list[float]  # equilibrium expected pot share
    exploitability: float  # most any single entrant gains by deviating
    iterations: int


def _shares(scores: list[int]) -> list[float]:
    best = max(scores)
    tied = sum(1 for v in scores if v == best)
    return [1.0 / tied if v == best else 0.0 for v in scores]


def action_values(
    scores: list[int],
    values: list[int],
    p_fav: float,
    dog_prob: list[float],
) -> list[tuple[float, float]]:
    """Expected pot share for each entrant from taking FAV vs DOG.

    Exact: enumerates all ``2^M`` side profiles and both outcomes.
    """
    m = len(scores)
    probs = [min(1.0 - 1e-12, max(1e-12, q)) for q in dog_prob]
    out = [[0.0, 0.0] for _ in range(m)]

    for mask in range(1 << m):
        joint = 1.0
        for j in range(m):
            joint *= probs[j] if (mask >> j) & 1 else (1.0 - probs[j])
        if joint <= 0.0:
            continue
        for fav_won in (1, 0):
            w = p_fav if fav_won else 1.0 - p_fav
            finals = []
            for j in range(m):
                took_dog = (mask >> j) & 1
                correct = (took_dog == 0) == bool(fav_won)
                finals.append(scores[j] + (values[j] if correct else 0))
            share = _shares(finals)
            for j in range(m):
                # Condition on player j's own action by dividing it back out.
                pj = probs[j] if (mask >> j) & 1 else (1.0 - probs[j])
                others = joint / pj
                out[j][(mask >> j) & 1] += others * w * share[j]
    return [(o[FAV], o[DOG]) for o in out]


def solve_endgame(
    scores: list[int],
    values: list[int],
    p_fav: float,
    iterations: int = 400,
) -> EndgameSolution:
    """Approximate the mixed-strategy equilibrium by damped fictitious play.

    ``scores`` are the totals going into the final game, ``values`` the
    confidence each entrant has riding on it, index 0 being us.
    """
    m = len(scores)
    dog_prob = [0.5] * m
    for it in range(1, iterations + 1):
        av = action_values(scores, values, p_fav, dog_prob)
        step = 1.0 / (it + 1.0)
        for j in range(m):
            br = 1.0 if av[j][DOG] > av[j][FAV] else 0.0
            dog_prob[j] += step * (br - dog_prob[j])

    av = action_values(scores, values, p_fav, dog_prob)
    value = [q * a[DOG] + (1.0 - q) * a[FAV] for q, a in zip(dog_prob, av)]
    exploitability = max(max(a) - v for a, v in zip(av, value))
    return EndgameSolution(dog_prob, value, exploitability, iterations)


def best_response(
    scores: list[int],
    values: list[int],
    p_fav: float,
    dog_prob: list[float],
    me: int = 0,
) -> tuple[int, float, float]:
    """Our best action against a fixed read on the field.

    Returns ``(side, ev_if_fav, ev_if_dog)``.  Use this when you have a genuine
    read; use :func:`solve_endgame` when you do not and would rather be
    unexploitable.
    """
    av = action_values(scores, values, p_fav, dog_prob)
    fav_ev, dog_ev = av[me]
    return (DOG if dog_ev > fav_ev else FAV), fav_ev, dog_ev


def deficit_threshold(my_value: int, leader_value: int, deficit: int) -> bool:
    """Can a single contrarian final-game bet actually catch the leader?

    Going opposite the leader moves the margin by your value if you are right.
    If your value does not cover the deficit, the swing cannot win the week and
    you are taking variance for nothing -- unless it can reach a *tie*.
    """
    return my_value >= deficit
