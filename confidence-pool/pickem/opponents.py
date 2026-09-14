"""Models of what the rest of the league does.

Three behaviours matter, and they are the three knobs here:

``temperature``
    How tightly an opponent orders confidence values by win probability.  0 is
    perfect chalk (16 on the biggest favorite, 1 on the coin flip); larger
    values shuffle the order, which is what real entrants do because they have
    opinions.

``upset_rate``
    How often they take a dog outright.  Scaled by how close the game is, since
    nobody takes the 88% favorite's opponent but plenty of people take a pick
    'em dog.

``adapts``
    Whether they play the endgame -- i.e. whether, once trailing late, they
    deliberately take the other side of the leader to create a swing.  This is
    the single most important opponent trait for our own strategy, because an
    adaptive field is much harder to hold a lead against.

Crucially, an opponent's locked picks are public, and confidence values are a
permutation, so once some of their games have kicked off we know the exact
multiset of values they still hold.  ``sample_card`` conditions on that: it
only samples the part we cannot see.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from random import Random

from .model import DOG, FAV, Card, WeekState


@dataclass(frozen=True)
class OpponentModel:
    name: str
    temperature: float = 0.35
    upset_rate: float = 0.08
    adapts: bool = False
    cushion: float = 2.0

    def dog_prob(self, p_fav: float) -> float:
        """Chance this entrant takes the underdog, tilted toward close games."""
        closeness = max(0.0, 1.0 - 2.0 * (p_fav - 0.5))  # 1.0 at a pick'em, 0 at 100%
        return min(0.45, self.upset_rate * closeness * 2.0)


def default_field(size: int, rng: Random | None = None) -> list[OpponentModel]:
    """A plausible mixed league: mostly near-chalk, a few sharper entrants.

    Reflects how these pools actually look -- the median entrant sorts by gut
    feel and never revisits their card, a couple of people are deliberate.
    """
    rng = rng or Random(7)
    archetypes = [
        ("chalk", 0.10, 0.03, False),
        ("homer", 0.55, 0.18, False),
        ("casual", 0.40, 0.10, False),
        ("sharp", 0.18, 0.06, True),
        ("gambler", 0.70, 0.26, False),
        ("late-mover", 0.25, 0.08, True),
    ]
    field = []
    for i in range(size):
        base, temp, upset, adapts = archetypes[i % len(archetypes)]
        jitter = 1.0 + 0.3 * (rng.random() - 0.5)
        field.append(
            OpponentModel(
                name=f"{base}-{i + 1}",
                temperature=temp * jitter,
                upset_rate=upset * jitter,
                adapts=adapts,
            )
        )
    return field


def sample_card(model: OpponentModel, state: WeekState, observed: dict[str, tuple[int, int]], rng: Random) -> Card:
    """Draw one plausible full card for an opponent, consistent with what we see.

    Confidence values are drawn by a Plackett-Luce style process: give each
    remaining game a utility of ``logit(p_fav) + temperature * Gumbel`` and hand
    out the biggest remaining value to the biggest utility.  At temperature 0
    this is exactly chalk.
    """
    slate = state.slate
    card = Card.empty(slate.n)

    spent: set[int] = set()
    open_idx: list[int] = []
    for i, g in enumerate(slate):
        if g.gid in observed:
            pts, side = observed[g.gid]
            card.points[i] = pts
            card.sides[i] = side
            spent.add(pts)
        else:
            open_idx.append(i)

    remaining = [p for p in slate.all_points if p not in spent]

    scored = []
    for i in open_idx:
        p = min(0.999, max(0.001, slate[i].p_fav))
        utility = math.log(p / (1.0 - p))
        if model.temperature > 0:
            u = rng.random()
            utility += model.temperature * -math.log(-math.log(max(1e-12, u)))
        scored.append((utility, i))
    scored.sort(reverse=True)

    for rank, (_u, i) in enumerate(scored):
        card.points[i] = remaining[len(remaining) - 1 - rank]
        card.sides[i] = DOG if rng.random() < model.dog_prob(slate[i].p_fav) else FAV
    return card
