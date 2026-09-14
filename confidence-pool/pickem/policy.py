"""The in-flight decision rule.

This is the policy that gets *rolled out* inside every Monte Carlo sample: at
each future deadline it asks "given where I stand, what should I do with the
games locking right now?".  The optimizer then searches over opening cards on
top of it, which is a policy-improvement step -- the search only sees the value
of holding big confidence values back because this rule is what will eventually
spend them.

The rule, in one paragraph:

    If you are projected to be ahead, mirror the field -- take every favorite.
    Correlating with the leader freezes the gap, and the gap is in your favor.
    If you are projected to be behind, you need a *swing*: games where you are
    on one side and the leader is on the other, so a single result moves the
    margin by your confidence value plus theirs.  But do not swing yet if the
    confidence values you are still holding on later games are enough to cover
    the deficit later -- waiting is free information, and the deficit estimate
    gets sharper every hour.  When you do have to swing, cover the deficit with
    the fewest and likeliest contrarian bets you can, and move your biggest
    remaining values onto exactly those games.

"Cover the deficit with the fewest, likeliest bets" is the same logic as being
down three scores in the fourth quarter: you do not need the *best* play, you
need the play whose *distribution* reaches the number.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import DOG, FAV


@dataclass(frozen=True)
class PolicyParams:
    cushion: float = 0.0
    """Extra points added to the target before computing the deficit.

    The target is already the *maximum* over the field's projections, which
    sits well above any single opponent's mean, so it is already the right
    bar.  Tuning confirms it: adding cushion on top overshoots and costs
    expected share.  Kept as a knob for leagues whose scoring differs.
    """

    defer_slack: float = 12.0
    """How much later capacity is required before postponing a needed swing.

    The test is ``later_capacity >= defer_slack * deficit``, where capacity is
    the raw confidence still riding on later games.  Raw capacity badly
    overstates the swing you can actually realize -- collecting it means
    *winning* underdog bets -- so the tuned value is far above 1.  Measured
    performance is flat anywhere from about 8 upward; 12 is chosen inside that
    plateau because it keeps the printed threshold (capacity / slack)
    interpretable rather than degenerating into "always fade".
    """

    swing_multiplier: float = 1.0
    """Credit for the leader's value on a game you go contrarian on.

    Going opposite the leader on a game moves the margin by your value *plus*
    theirs.  Their value on a not-yet-started game is not visible, but it is
    not zero either.  1.0 counts only your own value, which is deliberately
    conservative.
    """


def revise_wave(
    wave: list[int],
    order: list[int],
    points: list[int],
    sides: list[int],
    deficit: float,
    later_capacity: float,
    params: PolicyParams,
) -> None:
    """Decide sides (and in-wave value ordering) for the games locking now.

    Mutates ``points`` and ``sides`` in place for the indices in ``wave``.
    ``deficit`` is positive when trailing the target score.  ``order`` is
    ``wave`` pre-sorted by ascending favorite probability -- the cheapest
    contrarian bets first -- which is fixed for the week and so is hoisted out
    of the sampling loop by the caller.
    """
    if not wave:
        return

    # Ahead, or still able to cover the gap later: take the favorites.
    # Correlating with the field protects a lead, and holding values on later
    # games keeps the option alive for another hour of information.
    if deficit <= 0.0 or later_capacity >= params.defer_slack * deficit:
        for g in wave:
            sides[g] = FAV
        return

    if len(wave) == 1:
        sides[wave[0]] = DOG
        return

    need = deficit
    mult = params.swing_multiplier
    wave_values = sorted((points[g] for g in wave), reverse=True)

    # Cover the deficit with as few contrarian bets as possible, taken from the
    # least lopsided games and carrying this wave's largest values.
    take = len(order)
    acc = 0.0
    for k in range(len(order)):
        acc += wave_values[k] * mult
        if acc >= need:
            take = k + 1
            break

    contrarian = order[:take]
    flagged = [False] * len(points)
    for g in contrarian:
        flagged[g] = True
    ordered_games = contrarian + [g for g in wave if not flagged[g]]
    for value, g in zip(wave_values, ordered_games):
        points[g] = value
    for g in wave:
        sides[g] = DOG if flagged[g] else FAV


def chalk_card(open_idx: list[int], available: list[int], p_fav: list[float]) -> tuple[dict[int, int], dict[int, int]]:
    """The textbook entry: biggest confidence value on the biggest favorite.

    Maximizes expected score.  It is the right answer if the prize went to the
    highest average score; it is not the right answer when the prize goes to
    whoever is highest *this week*.
    """
    by_prob = sorted(open_idx, key=lambda g: p_fav[g], reverse=True)
    values = sorted(available, reverse=True)
    pts = {g: v for g, v in zip(by_prob, values)}
    sides = {g: FAV for g in open_idx}
    return pts, sides


def late_heavy_card(
    open_idx: list[int],
    available: list[int],
    p_fav: list[float],
    kickoffs: list[float],
    weight: float,
) -> tuple[dict[int, int], dict[int, int]]:
    """Chalk, tilted toward putting bigger values on later kickoffs.

    ``weight`` 0 reproduces chalk.  Used as a search seed, not as an answer --
    the optimizer decides how much tilt is actually worth it.
    """
    if not open_idx:
        return {}, {}
    times = [kickoffs[g] for g in open_idx]
    lo, hi = min(times), max(times)
    span = max(1.0, hi - lo)
    ranked = sorted(open_idx, key=lambda g: p_fav[g] + weight * (kickoffs[g] - lo) / span, reverse=True)
    values = sorted(available, reverse=True)
    pts = {g: v for g, v in zip(ranked, values)}
    sides = {g: FAV for g in open_idx}
    return pts, sides
