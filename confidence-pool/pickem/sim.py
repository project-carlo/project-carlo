"""Monte Carlo scenario generation.

Two things have to be simulated jointly, and they have to be *consistent* with
each other:

1. Who wins each game.
2. What the live win probability of each game looks like at each future
   decision deadline.

Point 2 is what makes the 4:05pm decision interesting: the 1:00pm games are not
final yet, but they are three quarters old, so you know a great deal about them
without knowing anything for certain.  Modelling that as "you know nothing"
throws away most of the edge; modelling it as "you know everything" invents
edge that is not there.

Construction
------------
For each game let ``z = Phi^-1(p_fav)`` and let the outcome be driven by a
latent ``X_1 = z + W`` with ``W ~ N(0,1)``: the favorite wins iff ``X_1 > 0``,
which happens with probability ``Phi(z) = p_fav``.  Reading ``X`` as a Brownian
motion pinned to that terminal value, the win probability partway through the
game is the martingale

    ``WP(t) = Phi( X_t / sqrt(1 - t) )``

with ``t`` the fraction of the game elapsed.  It starts at ``p_fav``, wanders,
and is forced to 0 or 1 at ``t = 1``.  Sampling ``X_1`` first and then filling
in intermediate values with a Brownian bridge keeps the path and the result
consistent by construction, and lets the same draw be reused across every
candidate entry (common random numbers).

Correlation across games comes from a one-factor Gaussian copula on ``W``: a
single latent "chalk factor" per week decides whether favorites broadly hold or
broadly fall.  That correlation matters a lot for a pool -- an all-chalk week
bunches everyone's score together and makes differentiation cheap, while an
upset-heavy week blows the field apart.

A game already in progress enters with its live win probability ``q`` at
elapsed fraction ``u``; the same algebra applies on the residual interval, so
in-progress and not-yet-started games share one code path.
"""

from __future__ import annotations

import math
from array import array
from random import Random

from .model import FAV, WeekState
from .probs import norm_cdf, norm_ppf


class Scenarios:
    """A frozen bundle of sampled weeks, reused for every candidate entry.

    Attributes
    ----------
    fav_win : bytearray of length ``S * G``; 1 if the favorite won.
    wp : array('d') of length ``S * E * G``; the favorite's win probability for
        game ``g`` as it would appear on screen at decision epoch ``e``.
    """

    def __init__(self, state: WeekState, samples: int, rho: float, rng: Random, lock_lead: float = 300.0):
        slate = state.slate
        self.state = state
        self.S = samples
        self.G = slate.n
        self.epochs = state.decision_epochs()
        # Picks lock five minutes before kickoff, so every projection is read
        # from the scoreboard as it looks at the deadline, not at kickoff.
        self.lock_lead = lock_lead
        self.decision_times = [t - lock_lead for t in self.epochs]
        self.E = len(self.epochs)
        self.rho = rho

        G, S, E = self.G, self.S, self.E
        self.fav_win = bytearray(S * G)
        self.wp = array("d", [0.0]) * (S * E * G)

        # Per-game setup: where the game stands right now.
        #   u0    fraction elapsed at decision time
        #   mu    latent value already accumulated (so that WP now == q)
        #   fixed None, or the known result for a finished game
        u0: list[float] = []
        mu: list[float] = []
        fixed: list[int | None] = []
        for i, g in enumerate(slate):
            if g.gid in state.results:
                u0.append(1.0)
                mu.append(0.0)
                fixed.append(state.results[g.gid])
                continue
            u = slate.elapsed_fraction(i, state.now)
            q = state.live_wp.get(g.gid, g.p_fav)
            q = min(1.0 - 1e-9, max(1e-9, q))
            u0.append(u)
            mu.append(norm_ppf(q) * math.sqrt(max(1e-12, 1.0 - u)))
            fixed.append(None)

        # Elapsed fraction of every game at every remaining decision epoch.
        frac = [[slate.elapsed_fraction(i, t) for i in range(G)] for t in self.decision_times]

        sqrt_rho = math.sqrt(rho)
        sqrt_1mrho = math.sqrt(1.0 - rho)
        gauss = rng.gauss

        for s in range(S):
            chalk = gauss(0.0, 1.0)  # week-level factor: >0 means favorites hold
            base = s * G
            for i in range(G):
                if fixed[i] is not None:
                    won = fixed[i]
                    self.fav_win[base + i] = won
                    for e in range(E):
                        self.wp[(s * E + e) * G + i] = float(won)
                    continue

                u = u0[i]
                var = max(0.0, 1.0 - u)
                w = sqrt_rho * chalk + sqrt_1mrho * gauss(0.0, 1.0)
                x1 = mu[i] + math.sqrt(var) * w
                self.fav_win[base + i] = 1 if x1 > 0.0 else 0

                # Walk the bridge forward through the epochs this game is live for.
                t_prev, x_prev = u, mu[i]
                for e in range(E):
                    t = frac[e][i]
                    idx = (s * E + e) * G + i
                    if t <= u + 1e-12:
                        self.wp[idx] = norm_cdf(mu[i] / math.sqrt(var)) if var > 1e-12 else float(x1 > 0)
                        continue
                    if t >= 1.0 - 1e-9:
                        self.wp[idx] = 1.0 if x1 > 0.0 else 0.0
                        continue
                    span = 1.0 - t_prev
                    mean = x_prev + (t - t_prev) / span * (x1 - x_prev)
                    sd = math.sqrt(max(0.0, (t - t_prev) * (1.0 - t) / span))
                    x = mean + sd * gauss(0.0, 1.0) if sd > 0 else mean
                    self.wp[idx] = norm_cdf(x / math.sqrt(1.0 - t))
                    t_prev, x_prev = t, x

    # -- convenience accessors (hot loops index the flat arrays directly) ---
    def won(self, s: int, g: int) -> int:
        return self.fav_win[s * self.G + g]

    def wp_at(self, s: int, e: int, g: int) -> float:
        return self.wp[(s * self.E + e) * self.G + g]

    def realized_fav_rate(self) -> float:
        return sum(self.fav_win) / float(self.S * self.G)


def side_prob(wp_fav: float, side: int) -> float:
    return wp_fav if side == FAV else 1.0 - wp_fav
