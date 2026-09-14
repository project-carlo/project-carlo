"""Probability plumbing: odds conversion and normal-distribution helpers.

Everything downstream speaks in terms of ``p_fav`` -- the probability that the
favorite wins a given game.  This module is the only place that knows how to
turn bookmaker prices into such a number, and the only place with statistics
approximations in it.
"""

from __future__ import annotations

import math

SQRT2 = math.sqrt(2.0)


def american_to_prob(odds: float) -> float:
    """Convert American moneyline odds to an implied (vigged) probability."""
    if odds < 0:
        return -odds / (-odds + 100.0)
    return 100.0 / (odds + 100.0)


def devig_two_way(prob_a: float, prob_b: float) -> tuple[float, float]:
    """Strip the bookmaker's hold from a two-way market, proportionally.

    The two implied probabilities sum to more than 1; rescaling both by the
    overround is the standard (and for near-even markets, quite accurate)
    correction.
    """
    total = prob_a + prob_b
    if total <= 0:
        raise ValueError("implied probabilities must be positive")
    return prob_a / total, prob_b / total


def moneyline_to_p_home(home_odds: float, away_odds: float) -> float:
    """Home win probability from a pair of American moneylines."""
    home, _away = devig_two_way(american_to_prob(home_odds), american_to_prob(away_odds))
    return home


def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / SQRT2)


_A = (
    -3.969683028665376e01,
    2.209460984245205e02,
    -2.759285104469687e02,
    1.383577518672690e02,
    -3.066479806614716e01,
    2.506628277459239e00,
)
_B = (
    -5.447609879822406e01,
    1.615858368580409e02,
    -1.556989798598866e02,
    6.680131188771972e01,
    -1.328068155288572e01,
)
_C = (
    -7.784894002430293e-03,
    -3.223964580411365e-01,
    -2.400758277161838e00,
    -2.549732539343734e00,
    4.374664141464968e00,
    2.938163982698783e00,
)
_D = (
    7.784695709041462e-03,
    3.224671290700398e-01,
    2.445134137142996e00,
    3.754408661907416e00,
)
_P_LOW = 0.02425


def norm_ppf(p: float) -> float:
    """Inverse standard normal CDF (Acklam's approximation + one Halley step)."""
    if p <= 0.0:
        return -40.0
    if p >= 1.0:
        return 40.0
    if p < _P_LOW:
        q = math.sqrt(-2.0 * math.log(p))
        x = (((((_C[0] * q + _C[1]) * q + _C[2]) * q + _C[3]) * q + _C[4]) * q + _C[5]) / (
            (((_D[0] * q + _D[1]) * q + _D[2]) * q + _D[3]) * q + 1.0
        )
    elif p <= 1.0 - _P_LOW:
        q = p - 0.5
        r = q * q
        x = (((((_A[0] * r + _A[1]) * r + _A[2]) * r + _A[3]) * r + _A[4]) * r + _A[5]) * q / (
            ((((_B[0] * r + _B[1]) * r + _B[2]) * r + _B[3]) * r + _B[4]) * r + 1.0
        )
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        x = -(((((_C[0] * q + _C[1]) * q + _C[2]) * q + _C[3]) * q + _C[4]) * q + _C[5]) / (
            (((_D[0] * q + _D[1]) * q + _D[2]) * q + _D[3]) * q + 1.0
        )
    # Halley refinement -- brings the error down to roughly machine precision.
    err = norm_cdf(x) - p
    denom = math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    if denom > 1e-300:
        u = err / denom
        x = x - u / (1.0 + 0.5 * x * u)
    return x
