"""Generate data/week_example_live.json: the same week, frozen at 4:00pm Sunday.

Five minutes before the 4:05 kickoffs. The Thursday and London games are final,
the 1:00pm games are mostly final but three are still being played, and every
entrant's picks on those games are now public. Nine of sixteen confidence
values are spent; seven are still in play.
"""

import json
import os
import sys
from random import Random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pickem.model import load_week
from pickem.opponents import OpponentModel, sample_card
from pickem.policy import late_heavy_card

HERE = os.path.dirname(os.path.abspath(__file__))
src = load_week(os.path.join(HERE, "week_example.json"))
slate = src.slate
rng = Random(2026)

NOW = "2026-09-20T16:00:00-04:00"
FINAL = {"TNF": 1, "LON": 0, "E1": 0, "E2": 1, "E4": 1, "E5": 1}  # 1 = favorite won
LIVE = {"E3": 0.22, "E6": 0.91, "E7": 0.48}  # still being played at 4:00pm

# My entry, as it stood before any of this started: chalk tilted a little late.
p_fav = [g.p_fav for g in slate]
kicks = [g.kickoff for g in slate]
pts, sides = late_heavy_card(list(range(slate.n)), slate.all_points, p_fav, kicks, 0.35)

started = [i for i, g in enumerate(slate) if g.gid in FINAL or g.gid in LIVE]
my_picks = {
    slate[i].gid: {"team": slate[i].team(sides[i]), "points": pts[i]}
    for i in started
}

rivals = {}
for name, model in [
    ("Dana", OpponentModel("Dana", temperature=0.12, upset_rate=0.04)),
    ("Reggie", OpponentModel("Reggie", temperature=0.45, upset_rate=0.16)),
    ("Sam", OpponentModel("Sam", temperature=0.28, upset_rate=0.09, adapts=True)),
]:
    card = sample_card(model, src, {}, rng)
    card.validate(slate.n)
    rivals[name] = {
        slate[i].gid: {"team": slate[i].team(card.sides[i]), "points": card.points[i]}
        for i in started
    }

blob = {
    "note": (
        "The same week frozen five minutes before the 4:05 kickoffs. Thursday, London and "
        "four of the 1:00 games are final; three 1:00 games are still being played and carry "
        "a live win probability. Every entrant's picks on started games are public, which also "
        "reveals exactly which confidence values they have left."
    ),
    "now": NOW,
    "games": json.load(open(os.path.join(HERE, "week_example.json")))["games"],
    "results": FINAL,
    "live_win_prob": LIVE,
    "my_picks": my_picks,
    "opponent_picks": rivals,
}
out = os.path.join(HERE, "week_example_live.json")
with open(out, "w") as fh:
    json.dump(blob, fh, indent=2)
    fh.write("\n")
print("wrote", out)

st = load_week(out)
print("  started:", len(st.locked_indices()), " open:", len(st.open_indices()))
print("  my values still in play:", st.available_points())
for r in rivals:
    print(f"  {r}'s values still in play:", st.opponent_available_points(r))
print("  my settled score so far:", st.settled_score(st.my_card))
for r in rivals:
    print(f"  {r} settled score so far:", st.settled_score(st.opponents[r]))
