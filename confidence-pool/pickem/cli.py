"""Command line interface.

    python -m pickem.cli recommend data/week_example.json
    python -m pickem.cli toy
    python -m pickem.cli endgame --scores 100,104,99 --values 10,6,13 --p 0.59
    python -m pickem.cli compare data/week_example.json
    python -m pickem.cli equilibrium data/week_example.json
    python -m pickem.cli tune data/week_example.json
"""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction
from random import Random

from .endgame import solve_endgame
from .evaluate import Evaluator
from .model import DOG, FAV, Card, load_week
from .optimize import Config, optimize
from .policy import PolicyParams, chalk_card
from .sim import Scenarios


def _fmt_pick(game, side: int) -> str:
    tag = "fav" if side == FAV else "DOG"
    return f"{game.team(side):>4} ({tag})"


def _print_card(state, card: Card, title: str) -> None:
    print(f"\n{title}")
    print("  " + "-" * 74)
    print(f"  {'deadline':<14}{'game':<12}{'pick':<14}{'conf':>5}{'mkt':>8}   status")
    print("  " + "-" * 74)
    last = None
    for i, g in enumerate(state.slate):
        wave = g.kickoff_str()
        shown = wave if wave != last else ""
        last = wave
        status = "LOCKED" if state.has_started(i) else ""
        if g.gid in state.results:
            status = "FINAL " + ("fav won" if state.results[g.gid] else "dog won")
        p = g.p_side(card.sides[i])
        print(
            f"  {shown:<14}{g.label:<12}{_fmt_pick(g, card.sides[i]):<14}"
            f"{card.points[i]:>5}{p * 100:>7.0f}%   {status}"
        )
    print("  " + "-" * 74)


def _print_plan(state, card: Card, params: PolicyParams) -> None:
    """The in-flight rule, written out as thresholds you can act on."""
    print("\n  In-flight plan -- what to do at each remaining deadline")
    print("  " + "-" * 74)
    print(f"  {'deadline':<14}{'locking':<9}{'conf at stake':>14}{'held back':>11}{'swing if behind by':>22}")
    print("  " + "-" * 74)
    waves = [(t, idx) for t, idx in state.slate.waves() if any(not state.has_started(i) for i in idx)]
    for t, idx in waves:
        held = sum(card.points[j] for j in range(state.slate.n) if state.slate[j].kickoff > t + 1.0)
        stake = sum(card.points[i] for i in idx)
        label = state.slate[idx[0]].kickoff_str()
        need = held / params.defer_slack if params.defer_slack > 0 else float("inf")
        thresh = f"> {need:.1f} pts" if held > 0 else "always (last games)"
        print(f"  {label:<14}{len(idx):<9}{stake:>14}{held:>11}{thresh:>22}")
    print("  " + "-" * 74)
    print("  Read: at each deadline, project the best final score in the league. If you")
    print("  trail it by less than the threshold, take the favorites -- you can still")
    print("  catch up later, and another hour of results is free information. If you")
    print("  trail by more, you cannot wait: fade the field now, starting with the games")
    print("  closest to a coin flip, and move that wave's biggest values onto them.")


def cmd_recommend(args) -> int:
    state = load_week(args.week)
    cfg = Config(
        search_samples=args.search_samples,
        final_samples=args.final_samples,
        entrants=args.entrants,
        rho=args.rho,
        sweeps=args.sweeps,
        refine_passes=args.refine,
        params=PolicyParams(cushion=args.cushion, defer_slack=args.defer_slack),
    )
    print(f"Optimizing {state.slate.n} games, {len(state.decision_epochs())} deadlines left, "
          f"league of {args.entrants}...")
    res = optimize(state, cfg, verbose=args.verbose)
    _print_card(state, res.card, "Recommended entry")
    _print_plan(state, res.card, cfg.params)
    print("\n  Expected pot share (independent holdout sample):")
    print(f"    this entry : {res.holdout}")
    print(f"    chalk      : {res.chalk_holdout}")
    print(f"    fair share : {100.0 / args.entrants:.2f}%")
    edge = (res.holdout.ev_share - res.chalk_holdout.ev_share) * 100
    give_up = res.chalk_holdout.mean_score - res.holdout.mean_score
    print(f"    edge over chalk: {edge:+.2f} points of pot share, "
          f"giving up {give_up:.1f} expected points to get it")
    print(f"\n  ({res.evaluations} candidate entries evaluated; search estimate was "
          f"{res.search.ev_share * 100:.2f}%, holdout {res.holdout.ev_share * 100:.2f}% -- "
          f"the gap is search overfit.)")
    return 0


def cmd_compare(args) -> int:
    """Score several fixed strategies on one common set of simulated weeks."""
    state = load_week(args.week)
    params = PolicyParams(cushion=args.cushion, defer_slack=args.defer_slack)
    sc = Scenarios(state, args.final_samples, args.rho, Random(4242))
    field = Config(entrants=args.entrants).field_models(state)
    p_fav = [g.p_fav for g in state.slate]
    open_idx = state.open_indices()
    avail = state.available_points()

    from .policy import late_heavy_card

    cards: list[tuple[str, Card, PolicyParams]] = []
    pts, sides = chalk_card(open_idx, avail, p_fav)
    chalk = Card([pts.get(i, 0) for i in range(state.slate.n)], [sides.get(i, FAV) for i in range(state.slate.n)])
    static = PolicyParams(cushion=1e9, defer_slack=0.0)  # never swings: a card you never revisit
    cards.append(("chalk, never revisited", chalk, static))
    cards.append(("chalk, played in-flight", chalk, params))
    kicks = [g.kickoff for g in state.slate]
    for w in (0.4, 0.8):
        pts, sides = late_heavy_card(open_idx, avail, p_fav, kicks, w)
        c = Card([pts.get(i, 0) for i in range(state.slate.n)], [sides.get(i, FAV) for i in range(state.slate.n)])
        cards.append((f"late-heavy (tilt {w}), in-flight", c, params))

    print(f"\n  {args.final_samples} simulated weeks, league of {args.entrants}, common random numbers")
    print("  " + "-" * 78)
    print(f"  {'strategy':<36}{'EV share':>10}{'P(win)':>9}{'mean pts':>10}{'sd':>7}")
    print("  " + "-" * 78)
    for name, card, pp in cards:
        ev = Evaluator(state, sc, field, pp, Random(77))
        ev.set_reference(card)
        r = ev.evaluate(card)
        print(f"  {name:<36}{r.ev_share * 100:>9.2f}%{r.p_win * 100:>8.2f}%{r.mean_score:>10.1f}{r.sd_score:>7.1f}")
    print("  " + "-" * 78)
    print(f"  fair share for {args.entrants} entrants: {100.0 / args.entrants:.2f}%")
    return 0


def cmd_toy(args) -> int:
    from .toy import ToyCard, solve_toy

    p_a, p_b = Fraction(args.p_a).limit_denominator(100), Fraction(args.p_b).limit_denominator(100)
    opps = [ToyCard(2, FAV, FAV)] * args.opponents
    r = solve_toy(p_a, p_b, opps)
    print(f"\n  Two games, confidence values {{1, 2}}, {args.opponents} chalk opponents.")
    print(f"  Game A kicks off first ({float(p_a):.0%} favorite); game B second ({float(p_b):.0%} favorite).")
    print(f"  Exact rational arithmetic -- no sampling anywhere.\n")
    print(f"  {'where the 2 sits':<22}{'commit up front':>18}{'decide B on the news':>24}{'option value':>15}")
    print("  " + "-" * 80)
    for k, label in ((2, "EARLY game (chalk)"), (1, "LATE game")):
        st, ad = r.static_by_placement[k], r.adaptive_by_placement[k]
        print(f"  {label:<22}{float(st):>18.4f}{float(ad):>24.4f}{float(ad - st):>+15.4f}")
    print("  " + "-" * 80)
    pts_a, side_a, plan, val = r.best_adaptive
    print(f"\n  Best overall: put {3 - pts_a} on the LATE game, {pts_a} on the early one, then")
    for res, side in sorted(plan.items(), reverse=True):
        cond = "the early favorite wins" if res else "the early favorite loses"
        print(f"    if {cond:<26} -> take the {'FAVORITE' if side == FAV else 'UNDERDOG'} in game B")
    print(f"  Value {float(val):.4f} vs {float(r.best_static[1]):.4f} for the best card you never revisit "
          f"({float(r.option_value):+.4f}).")
    print(f"  Fair share would be {1 / (args.opponents + 1):.4f}.")
    print("\n  Note the asymmetry: the right to change your mind is worth something only")
    print("  when a big confidence value is still unspent. On the early game it is worth")
    print("  exactly zero.")
    return 0


def cmd_endgame(args) -> int:
    scores = [int(x) for x in args.scores.split(",")]
    values = [int(x) for x in args.values.split(",")]
    if len(scores) != len(values):
        print("scores and values must have the same length", file=sys.stderr)
        return 2
    sol = solve_endgame(scores, values, args.p, iterations=args.iterations)
    print(f"\n  Final game, favorite wins with probability {args.p:.0%}.")
    print("  Entry 0 is you. Everyone's score and stake is public by now, because the")
    print("  confidence values are a permutation -- only the sides are hidden.\n")
    print(f"  {'entrant':<10}{'score':>7}{'stake':>7}{'max':>7}{'P(take underdog)':>20}{'pot share':>12}")
    print("  " + "-" * 66)
    for j, (s, v) in enumerate(zip(scores, values)):
        who = "YOU" if j == 0 else f"opp {j}"
        print(f"  {who:<10}{s:>7}{v:>7}{s + v:>7}{sol.dog_prob[j] * 100:>19.1f}%{sol.value[j] * 100:>11.1f}%")
    print("  " + "-" * 66)
    print(f"  equilibrium residual (max gain from deviating): {sol.exploitability * 100:.3f} points\n")
    if len(scores) == 2 and 0.02 < sol.dog_prob[1] < 0.98:
        print("  Note the leader is mixing too. Facing someone who must create a swing,")
        print("  taking the favorite every time is exploitable: the trailer simply takes")
        print("  the other side. The leader has to be unpredictable, not right.")
    return 0


def cmd_equilibrium(args) -> int:
    from .equilibrium import fictitious_play

    state = load_week(args.week)
    cfg = Config(
        search_samples=args.search_samples,
        final_samples=args.final_samples,
        entrants=args.entrants,
        rho=args.rho,
        sweeps=args.sweeps,
        refine_passes=0,
        params=PolicyParams(cushion=args.cushion, defer_slack=args.defer_slack),
    )
    print(f"\n  Fictitious play, league of {args.entrants}, {args.rounds} rounds.")
    print(f"  Fair share is {100.0 / args.entrants:.2f}%. Watch exploitability fall toward zero.\n")
    rep = fictitious_play(state, cfg, rounds=args.rounds, verbose=True)
    print("\n  Shape of the equilibrium mixture (average over the population):")
    print("  " + "-" * 60)
    print(f"  {'deadline':<16}{'avg confidence':>16}{'contrarian rate':>18}")
    print("  " + "-" * 60)
    for label, avg_pts, dog_rate in rep.mixture_summary(state):
        print(f"  {label:<16}{avg_pts:>16.2f}{dog_rate * 100:>17.1f}%")
    print("  " + "-" * 60)
    print(f"\n  final exploitability: {rep.final_exploitability * 100:+.2f} points of pot share")
    return 0


def cmd_tune(args) -> int:
    """Grid-search the two policy constants on held-out weeks."""
    state = load_week(args.week)
    sc = Scenarios(state, args.final_samples, args.rho, Random(909))
    field = Config(entrants=args.entrants).field_models(state)
    p_fav = [g.p_fav for g in state.slate]
    pts, sides = chalk_card(state.open_indices(), state.available_points(), p_fav)
    card = Card([pts.get(i, 0) for i in range(state.slate.n)], [sides.get(i, FAV) for i in range(state.slate.n)])
    print(f"\n  Tuning the in-flight policy on a fixed chalk card ({args.final_samples} weeks).")
    print("  cushion = points added to the leader's projection before measuring the deficit.")
    print("  defer_slack = how much headroom is needed before postponing a swing.\n")
    print(f"  {'cushion':>9}{'defer_slack':>13}{'EV share':>11}{'P(win)':>9}")
    print("  " + "-" * 44)
    best = None
    for cushion in args.cushions:
        for slack in args.slacks:
            pp = PolicyParams(cushion=cushion, defer_slack=slack)
            ev = Evaluator(state, sc, field, pp, Random(55))
            ev.set_reference(card)
            r = ev.evaluate(card)
            print(f"  {cushion:>9.1f}{slack:>13.1f}{r.ev_share * 100:>10.2f}%{r.p_win * 100:>8.2f}%")
            if best is None or r.ev_share > best[0]:
                best = (r.ev_share, cushion, slack)
    print("  " + "-" * 44)
    print(f"  best: cushion={best[1]}, defer_slack={best[2]} -> {best[0] * 100:.2f}%")
    return 0


def cmd_slotvalue(args) -> int:
    """How much confidence should actually go on one particular game?

    Takes the optimized card, then forces each possible confidence value onto
    the named game (swapping with whoever held it) and re-scores. This answers
    the question directly, rather than by rule of thumb.
    """
    state = load_week(args.week)
    params = PolicyParams(cushion=args.cushion, defer_slack=args.defer_slack)
    cfg = Config(
        search_samples=args.search_samples, final_samples=args.final_samples,
        entrants=args.entrants, rho=args.rho, sweeps=args.sweeps, refine_passes=0, params=params,
    )
    if args.optimize:
        print("Optimizing a base card first...")
        base = optimize(state, cfg).card
    else:
        p_fav = [g.p_fav for g in state.slate]
        pts, sides = chalk_card(state.open_indices(), state.available_points(), p_fav)
        base = Card([pts.get(i, 0) for i in range(state.slate.n)],
                    [sides.get(i, FAV) for i in range(state.slate.n)])

    i = state.slate.index[args.game]
    if state.has_started(i):
        print(f"{args.game} has already kicked off; its value is frozen.", file=sys.stderr)
        return 2
    g = state.slate[i]
    sc = Scenarios(state, args.final_samples, args.rho, Random(31337))
    ev = Evaluator(state, sc, cfg.field_models(state), params, Random(4711))
    ev.set_reference(base)

    print(f"\n  Marginal value of the confidence placed on {g.label} "
          f"({g.kickoff_str()}, {g.p_fav:.0%} favorite).")
    print(f"  Everything else held fixed; the value is swapped with whichever game holds it.")
    print(f"  {args.final_samples} weeks, league of {args.entrants}.\n")
    print(f"  {'value on ' + args.game:>16}{'EV share':>11}{'P(win)':>9}{'mean pts':>10}{'swapped with':>14}")
    print("  " + "-" * 62)
    rows = []
    for v in sorted(state.available_points()):
        trial = base.copy()
        j = trial.points.index(v)
        trial.points[i], trial.points[j] = trial.points[j], trial.points[i]
        r = ev.evaluate(trial)
        rows.append((v, r))
        other = state.slate[j].label if j != i else "-"
        print(f"  {v:>16}{r.ev_share * 100:>10.2f}%{r.p_win * 100:>8.2f}%{r.mean_score:>10.1f}{other:>14}")
    print("  " + "-" * 62)
    best = max(rows, key=lambda x: x[1].ev_share)
    chalky = base.points[i]
    print(f"  best: {best[0]} on {args.game} -> {best[1].ev_share * 100:.2f}%  "
          f"(base card had {chalky})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pickem", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, week=True):
        if week:
            sp.add_argument("week", help="path to the week JSON")
        sp.add_argument("--entrants", type=int, default=10, help="league size, including you")
        sp.add_argument("--rho", type=float, default=0.15, help="week-level correlation between favorites holding")
        sp.add_argument("--cushion", type=float, default=0.0)
        sp.add_argument("--defer-slack", dest="defer_slack", type=float, default=12.0)
        sp.add_argument("--final-samples", type=int, default=8000)
        return sp

    r = common(sub.add_parser("recommend", help="produce an entry for a week"))
    r.add_argument("--search-samples", type=int, default=3000)
    r.add_argument("--sweeps", type=int, default=3)
    r.add_argument("--refine", type=int, default=1)
    r.add_argument("-v", "--verbose", action="store_true")
    r.set_defaults(func=cmd_recommend)

    c = common(sub.add_parser("compare", help="score fixed strategies head to head"))
    c.set_defaults(func=cmd_compare)

    t = sub.add_parser("toy", help="exact two-game demonstration")
    t.add_argument("--p-a", dest="p_a", type=float, default=0.8)
    t.add_argument("--p-b", dest="p_b", type=float, default=0.6)
    t.add_argument("--opponents", type=int, default=3)
    t.set_defaults(func=cmd_toy)

    e = sub.add_parser("endgame", help="solve the final game exactly")
    e.add_argument("--scores", required=True, help="comma separated totals going into the last game; you first")
    e.add_argument("--values", required=True, help="comma separated confidence riding on the last game")
    e.add_argument("--p", type=float, required=True, help="favorite win probability")
    e.add_argument("--iterations", type=int, default=600)
    e.set_defaults(func=cmd_endgame)

    q = common(sub.add_parser("equilibrium", help="approximate the symmetric Nash equilibrium"))
    q.add_argument("--rounds", type=int, default=6)
    q.add_argument("--search-samples", type=int, default=1200)
    q.add_argument("--sweeps", type=int, default=2)
    q.set_defaults(func=cmd_equilibrium)

    sv = common(sub.add_parser("slotvalue", help="marginal value of the confidence on one game"))
    sv.add_argument("--game", required=True, help="game id, e.g. MNF")
    sv.add_argument("--optimize", action="store_true", help="optimize the base card first (slower)")
    sv.add_argument("--search-samples", type=int, default=2000)
    sv.add_argument("--sweeps", type=int, default=2)
    sv.set_defaults(func=cmd_slotvalue)

    u = common(sub.add_parser("tune", help="grid search the policy constants"))
    u.add_argument("--cushions", type=float, nargs="+", default=[0.0, 2.0, 4.0, 6.0, 9.0])
    u.add_argument("--slacks", type=float, nargs="+", default=[0.6, 1.0, 1.4, 2.0])
    u.set_defaults(func=cmd_tune)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
