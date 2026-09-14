"""Unit tests. Run with: python -m unittest discover -s tests -v"""

import os
import statistics
import sys
import unittest
from fractions import Fraction
from random import Random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pickem.endgame import action_values, solve_endgame  # noqa: E402
from pickem.evaluate import Evaluator  # noqa: E402
from pickem.model import DOG, FAV, Card, Game, Slate, WeekState, load_week  # noqa: E402
from pickem.opponents import OpponentModel, default_field, sample_card  # noqa: E402
from pickem.policy import PolicyParams, chalk_card, late_heavy_card, revise_wave  # noqa: E402
from pickem.probs import american_to_prob, moneyline_to_p_home, norm_cdf, norm_ppf  # noqa: E402
from pickem.sim import Scenarios  # noqa: E402
from pickem.toy import ToyCard, solve_toy  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WEEK = os.path.join(os.path.dirname(HERE), "data", "week_example.json")


def tiny_state(n=6, now_offset=-600.0):
    base = 1_700_000_000.0
    games = [
        Game(f"g{i}", f"A{i}", f"H{i}", base + 3600.0 * i, 0.50 + 0.06 * i)
        for i in range(n)
    ]
    return WeekState(Slate(games), now=base + now_offset)


class TestProbs(unittest.TestCase):
    def test_ppf_cdf_roundtrip(self):
        for p in (1e-6, 0.001, 0.02, 0.25, 0.5, 0.77, 0.999, 1 - 1e-6):
            self.assertAlmostEqual(norm_cdf(norm_ppf(p)), p, places=10)

    def test_american_odds(self):
        self.assertAlmostEqual(american_to_prob(-200), 2 / 3, places=9)
        self.assertAlmostEqual(american_to_prob(+150), 0.4, places=9)

    def test_devig_sums_to_one(self):
        p = moneyline_to_p_home(-200, +170)
        q = moneyline_to_p_home(+170, -200)
        self.assertAlmostEqual(p + q, 1.0, places=12)


class TestModel(unittest.TestCase):
    def test_favorite_identification(self):
        g = Game("x", "AWAY", "HOME", 0.0, 0.7)
        self.assertEqual(g.favorite, "HOME")
        self.assertEqual(g.underdog, "AWAY")
        self.assertAlmostEqual(g.p_fav, 0.7)
        g2 = Game("y", "AWAY", "HOME", 0.0, 0.3)
        self.assertEqual(g2.favorite, "AWAY")
        self.assertAlmostEqual(g2.p_fav, 0.7)

    def test_card_validation(self):
        Card([1, 2, 3], [FAV] * 3).validate(3)
        with self.assertRaises(ValueError):
            Card([1, 2, 2], [FAV] * 3).validate(3)

    def test_available_points_excludes_locked(self):
        st = tiny_state(6)
        st.now = st.slate[2].kickoff + 60  # first three games under way
        st.my_card = {"g0": (6, FAV), "g1": (1, DOG), "g2": (4, FAV)}
        self.assertEqual(sorted(st.available_points()), [2, 3, 5])
        self.assertEqual(st.open_indices(), [3, 4, 5])

    def test_opponent_remaining_values_are_deducible(self):
        """A permutation plus public locked picks pins down what is left."""
        st = tiny_state(6)
        st.now = st.slate[3].kickoff + 60
        st.opponents = {"rival": {"g0": (2, FAV), "g1": (6, FAV), "g2": (1, DOG), "g3": (5, FAV)}}
        self.assertEqual(st.opponent_available_points("rival"), [3, 4])

    def test_waves_group_by_kickoff(self):
        base = 1e6
        games = [Game("a", "x", "y", base, 0.6), Game("b", "x", "y", base, 0.7), Game("c", "x", "y", base + 3600, 0.8)]
        waves = Slate(games).waves()
        self.assertEqual([len(w[1]) for w in waves], [2, 1])

    def test_load_example_week(self):
        st = load_week(WEEK)
        self.assertEqual(st.slate.n, 16)
        self.assertEqual(len(st.decision_epochs()), 7)
        self.assertEqual(sorted(st.available_points()), list(range(1, 17)))


class TestScenarios(unittest.TestCase):
    def test_marginals_match_market(self):
        st = tiny_state(4)
        sc = Scenarios(st, 40000, rho=0.0, rng=Random(11))
        for g in range(4):
            rate = sum(sc.fav_win[s * 4 + g] for s in range(sc.S)) / sc.S
            self.assertAlmostEqual(rate, st.slate[g].p_fav, delta=0.012)

    def test_live_wp_is_calibrated(self):
        """Games showing a given win probability must win at that rate."""
        st = tiny_state(2)
        sc = Scenarios(st, 30000, rho=0.0, rng=Random(5))
        e = sc.E - 1
        buckets = {}
        for s in range(sc.S):
            w = sc.wp_at(s, e, 0)
            key = min(4, int(w * 5))
            buckets.setdefault(key, []).append((w, sc.won(s, 0)))
        for key, rows in buckets.items():
            if len(rows) < 400:
                continue
            shown = statistics.fmean(r[0] for r in rows)
            actual = statistics.fmean(r[1] for r in rows)
            self.assertAlmostEqual(shown, actual, delta=0.035)

    def test_live_wp_is_a_martingale(self):
        st = tiny_state(2)
        sc = Scenarios(st, 20000, rho=0.0, rng=Random(6))
        mean_wp = statistics.fmean(sc.wp_at(s, sc.E - 1, 0) for s in range(sc.S))
        self.assertAlmostEqual(mean_wp, st.slate[0].p_fav, delta=0.015)

    def test_finished_games_are_fixed(self):
        st = tiny_state(3)
        st.now = st.slate[0].kickoff + 100000
        st.results = {"g0": 0}
        sc = Scenarios(st, 200, rho=0.1, rng=Random(1))
        self.assertTrue(all(sc.won(s, 0) == 0 for s in range(sc.S)))

    def test_correlation_spreads_the_field(self):
        """A week-level factor must widen the spread of favorite-win counts."""
        st = tiny_state(8)
        lo = Scenarios(st, 8000, rho=0.0, rng=Random(2))
        hi = Scenarios(st, 8000, rho=0.6, rng=Random(2))

        def spread(sc):
            counts = [sum(sc.fav_win[s * sc.G : (s + 1) * sc.G]) for s in range(sc.S)]
            return statistics.pstdev(counts)

        self.assertGreater(spread(hi), spread(lo) * 1.2)


class TestOpponents(unittest.TestCase):
    def test_zero_temperature_is_pure_chalk(self):
        st = tiny_state(6)
        card = sample_card(OpponentModel("t", temperature=0.0, upset_rate=0.0), st, {}, Random(1))
        card.validate(6)
        order = sorted(range(6), key=lambda i: st.slate[i].p_fav, reverse=True)
        self.assertEqual([card.points[i] for i in order], [6, 5, 4, 3, 2, 1])
        self.assertTrue(all(s == FAV for s in card.sides))

    def test_sampling_respects_observed_picks(self):
        st = tiny_state(6)
        obs = {"g0": (4, DOG), "g1": (6, FAV)}
        for seed in range(20):
            card = sample_card(OpponentModel("t", 0.5, 0.2), st, obs, Random(seed))
            card.validate(6)
            self.assertEqual((card.points[0], card.sides[0]), (4, DOG))
            self.assertEqual((card.points[1], card.sides[1]), (6, FAV))

    def test_upset_rate_favours_close_games(self):
        m = OpponentModel("t", 0.3, upset_rate=0.2)
        self.assertGreater(m.dog_prob(0.52), m.dog_prob(0.85))


class TestPolicy(unittest.TestCase):
    def setUp(self):
        self.p_fav = [0.80, 0.55, 0.65]
        self.wave = [0, 1, 2]
        self.order = sorted(self.wave, key=lambda g: self.p_fav[g])  # 1, 2, 0

    def test_ahead_takes_all_favorites(self):
        pts, sides = [5, 3, 1], [DOG, DOG, DOG]
        revise_wave(self.wave, self.order, pts, sides, deficit=-4.0, later_capacity=0.0, params=PolicyParams())
        self.assertEqual(sides, [FAV, FAV, FAV])

    def test_defers_when_it_can_still_cover_later(self):
        pts, sides = [5, 3, 1], [FAV, FAV, FAV]
        revise_wave(self.wave, self.order, pts, sides, deficit=6.0, later_capacity=40.0,
                    params=PolicyParams(defer_slack=1.0))
        self.assertEqual(sides, [FAV, FAV, FAV], "should keep its powder dry")

    def test_fades_cheapest_games_and_loads_them_up(self):
        pts, sides = [5, 3, 1], [FAV, FAV, FAV]
        revise_wave(self.wave, self.order, pts, sides, deficit=6.0, later_capacity=0.0, params=PolicyParams())
        faded = [g for g in self.wave if sides[g] == DOG]
        self.assertIn(1, faded, "the closest game is the cheapest place to differentiate")
        self.assertEqual(sorted(pts), [1, 3, 5], "confidence values must stay a permutation")
        self.assertEqual(max(pts[g] for g in faded), 5, "biggest value belongs on a faded game")
        self.assertGreaterEqual(sum(pts[g] for g in faded), 6, "the swing has to cover the deficit")

    def test_single_game_wave_fades_when_it_must(self):
        pts, sides = [7], [FAV]
        revise_wave([0], [0], pts, sides, deficit=5.0, later_capacity=0.0, params=PolicyParams())
        self.assertEqual(sides, [DOG])

    def test_uncoverable_deficit_goes_maximum_variance(self):
        pts, sides = [2, 1, 3], [FAV, FAV, FAV]
        revise_wave(self.wave, self.order, pts, sides, deficit=99.0, later_capacity=0.0, params=PolicyParams())
        self.assertTrue(all(sides[g] == DOG for g in self.wave))

    def test_chalk_and_late_heavy_are_permutations(self):
        st = tiny_state(8)
        p_fav = [g.p_fav for g in st.slate]
        kicks = [g.kickoff for g in st.slate]
        pts, _ = chalk_card(st.open_indices(), st.available_points(), p_fav)
        self.assertEqual(sorted(pts.values()), list(range(1, 9)))
        pts2, _ = late_heavy_card(st.open_indices(), st.available_points(), p_fav, kicks, 0.5)
        self.assertEqual(sorted(pts2.values()), list(range(1, 9)))

    def test_late_heavy_shifts_value_later_than_chalk(self):
        st = tiny_state(8)
        p_fav = [g.p_fav for g in st.slate]  # rises with index, so chalk is already late-loaded
        kicks = [g.kickoff for g in st.slate]
        flat = [0.6] * 8
        a, _ = chalk_card(st.open_indices(), st.available_points(), flat)
        b, _ = late_heavy_card(st.open_indices(), st.available_points(), flat, kicks, 1.0)
        last_two = st.open_indices()[-2:]
        self.assertGreater(sum(b[i] for i in last_two), sum(a[i] for i in last_two))


class TestEndgame(unittest.TestCase):
    def test_hopeless_trailer_has_no_value(self):
        sol = solve_endgame(scores=[80, 104], values=[5, 6], p_fav=0.6)
        self.assertAlmostEqual(sol.value[0], 0.0, places=6)
        self.assertAlmostEqual(sol.value[1], 1.0, places=6)

    def test_trailer_fades_a_predictable_leader(self):
        av = action_values([100, 104], [10, 6], 0.6, dog_prob=[0.5, 0.0])
        fav_ev, dog_ev = av[0]
        self.assertGreater(dog_ev, fav_ev)

    def test_leader_must_mix(self):
        """Against a live trailer, always taking the favorite is exploitable."""
        sol = solve_endgame([100, 104], [10, 6], 0.59, iterations=800)
        self.assertGreater(sol.dog_prob[1], 0.02)
        self.assertLess(sol.dog_prob[1], 0.98)
        self.assertLess(sol.exploitability, 0.02)

    def test_shares_sum_to_one(self):
        sol = solve_endgame([100, 101, 99], [8, 7, 9], 0.55, iterations=300)
        self.assertAlmostEqual(sum(sol.value), 1.0, places=4)

    def test_big_lead_is_safe(self):
        sol = solve_endgame([130, 100], [1, 2], 0.5)
        self.assertAlmostEqual(sol.value[0], 1.0, places=6)


class TestToy(unittest.TestCase):
    """The central claim, in exact arithmetic."""

    def test_option_value_comes_only_from_the_late_slot(self):
        pa, pb = Fraction(4, 5), Fraction(3, 5)
        opps = [ToyCard(2, FAV, FAV)] * 3
        r = solve_toy(pa, pb, opps)
        early = r.adaptive_by_placement[2] - r.static_by_placement[2]
        late = r.adaptive_by_placement[1] - r.static_by_placement[1]
        self.assertEqual(early, Fraction(0), "no option value when the big value is already spent")
        self.assertGreater(late, Fraction(0), "holding the big value late is worth something")
        self.assertEqual(late, Fraction(3, 50))

    def test_adaptive_beats_every_static_card(self):
        pa, pb = Fraction(4, 5), Fraction(3, 5)
        r = solve_toy(pa, pb, [ToyCard(2, FAV, FAV)] * 3)
        self.assertGreater(r.best_adaptive[3], r.best_static[1])

    def test_mirroring_a_lone_opponent_guarantees_a_split(self):
        """Degenerate but true: with one visible rival, copying them splits the pot."""
        pa, pb = Fraction(4, 5), Fraction(3, 5)
        r = solve_toy(pa, pb, [ToyCard(2, FAV, FAV)])
        self.assertEqual(r.best_static[1], Fraction(1, 2))


class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.st = load_week(WEEK)
        self.sc = Scenarios(self.st, 300, 0.15, Random(3))
        self.field = default_field(5)
        p_fav = [g.p_fav for g in self.st.slate]
        pts, sides = chalk_card(self.st.open_indices(), self.st.available_points(), p_fav)
        self.card = Card([pts[i] for i in range(16)], [sides[i] for i in range(16)])

    def _ev(self, params=None):
        ev = Evaluator(self.st, self.sc, self.field, params or PolicyParams(), Random(9))
        ev.set_reference(self.card)
        return ev

    def test_requires_reference_first(self):
        ev = Evaluator(self.st, self.sc, self.field, PolicyParams(), Random(9))
        with self.assertRaises(RuntimeError):
            ev.evaluate(self.card)

    def test_common_random_numbers_make_it_deterministic(self):
        ev = self._ev()
        a, b = ev.evaluate(self.card), ev.evaluate(self.card)
        self.assertEqual(a.ev_share, b.ev_share)
        self.assertEqual(a.mean_score, b.mean_score)

    def test_rollout_preserves_the_permutation(self):
        """revise_wave reorders values inside a wave; it must not invent any."""
        ev = self._ev(PolicyParams(cushion=0.0, defer_slack=50.0))
        scores = []
        for s in range(self.sc.S):
            pts = list(self.card.points)
            sides = list(self.card.sides)
            from pickem.policy import revise_wave as rw
            for e in range(ev.E):
                rw(ev.wave[e], ev.wave_order[e], pts, sides, 12.0, 0.0, PolicyParams())
            scores.append(sorted(pts))
        self.assertTrue(all(x == list(range(1, 17)) for x in scores))

    def test_shares_are_bounded(self):
        r = self._ev().evaluate(self.card)
        self.assertGreaterEqual(r.ev_share, 0.0)
        self.assertLessEqual(r.ev_share, 1.0)
        self.assertGreaterEqual(r.ev_share, r.p_win)

    def test_adaptive_play_beats_a_card_you_never_revisit(self):
        static = self._ev(PolicyParams(cushion=1e9, defer_slack=0.0)).evaluate(self.card)
        live = self._ev(PolicyParams(cushion=0.0, defer_slack=20.0)).evaluate(self.card)
        self.assertGreater(live.ev_share, static.ev_share)
        self.assertLess(live.mean_score, static.mean_score, "variance is bought with expected points")

    def test_locked_games_are_never_rewritten(self):
        st = load_week(WEEK)
        st.now = st.slate[2].kickoff + 60.0
        st.my_card = {"TNF": (16, FAV), "LON": (1, DOG), "E1": (15, FAV)}
        self.assertEqual(sorted(st.available_points()), [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        self.assertNotIn(0, st.open_indices())


class TestLiveState(unittest.TestCase):
    """Mid-week: what is public, and does the evaluator actually condition on it?"""

    def setUp(self):
        self.st = load_week(os.path.join(os.path.dirname(HERE), "data", "week_example_live.json"))

    def test_locked_and_open_split(self):
        self.assertEqual(len(self.st.locked_indices()), 9)
        self.assertEqual(len(self.st.open_indices()), 7)
        self.assertEqual(len(self.st.decision_epochs()), 4)

    def test_remaining_values_are_complements(self):
        mine = set(self.st.available_points())
        spent = {v for v, _ in self.st.my_card.values()}
        self.assertEqual(mine | spent, set(range(1, 17)))
        self.assertEqual(mine & spent, set())

    def test_named_rivals_are_modelled_under_their_own_names(self):
        from pickem.optimize import Config

        models = Config(entrants=10).field_models(self.st)
        names = {m.name for m in models}
        for rival in self.st.opponents:
            self.assertIn(rival, names)
        self.assertEqual(len(models), 9)

    def test_sampled_opponent_cards_match_their_public_picks(self):
        from pickem.optimize import Config

        models = Config(entrants=10).field_models(self.st)
        sc = Scenarios(self.st, 40, 0.15, Random(1))
        ev = Evaluator(self.st, sc, models, PolicyParams(), Random(2))
        rival = next(iter(self.st.opponents))
        j = [m.name for m in models].index(rival)
        G, M = ev.G, ev.M
        for s in range(sc.S):
            for gid, (v, side) in self.st.opponents[rival].items():
                g = self.st.slate.index[gid]
                self.assertEqual(ev.opp_pts[(s * M + j) * G + g], v)
                self.assertEqual(ev.opp_sides[(s * M + j) * G + g], side)

    def test_live_games_are_not_yet_decided(self):
        sc = Scenarios(self.st, 2000, 0.15, Random(3))
        g = self.st.slate.index["E3"]  # shown at 22% for the favorite
        rate = sum(sc.won(s, g) for s in range(sc.S)) / sc.S
        self.assertAlmostEqual(rate, 0.22, delta=0.03)
        settled = self.st.slate.index["E2"]  # already final
        self.assertTrue(all(sc.won(s, settled) == 1 for s in range(sc.S)))


class TestOptimize(unittest.TestCase):
    def test_missing_locked_picks_are_reported_clearly(self):
        from pickem.optimize import Config, optimize

        st = load_week(os.path.join(os.path.dirname(HERE), "data", "week_example_live.json"))
        st.my_card.pop("E2")
        with self.assertRaises(ValueError) as ctx:
            optimize(st, Config(search_samples=50, final_samples=50, sweeps=1, refine_passes=0))
        self.assertIn("E2", str(ctx.exception))

    def test_optimizer_returns_a_legal_card(self):
        from pickem.optimize import Config, optimize

        st = load_week(WEEK)
        res = optimize(st, Config(search_samples=200, final_samples=400, sweeps=1, refine_passes=0))
        res.card.validate(16)
        self.assertEqual(sorted(res.card.points), list(range(1, 17)))

    def test_optimizer_beats_chalk_given_enough_samples(self):
        """At small sample counts the search overfits and can lose to chalk;
        this is the reason the tool reports search and holdout separately."""
        from pickem.optimize import Config, optimize

        st = load_week(WEEK)
        res = optimize(st, Config(search_samples=1500, final_samples=3000, sweeps=2, refine_passes=0))
        self.assertGreater(res.holdout.ev_share, res.chalk_holdout.ev_share)


if __name__ == "__main__":
    unittest.main()
