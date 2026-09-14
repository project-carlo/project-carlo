"""Domain model for a weekly confidence pool.

Rules encoded here (Yahoo Pro Football Pick'em, confidence format):

* A week has ``N`` games.  Each entrant picks a winner for every game and
  assigns each game a distinct confidence value from ``1..N``.
* Score = sum of the confidence values on correctly picked games.
* Highest weekly score takes the payout; ties split it.
* An entrant may change both the pick and the confidence value on a game until
  five minutes before that game kicks off.  Because the values must stay a
  permutation of ``1..N``, values already spent on kicked-off games are frozen,
  and the remaining values may only be permuted among games not yet started.
* An opponent's pick and confidence value on a game become public when that
  game kicks off -- never before.

That last pair of rules is the whole game: your unspent confidence values are a
portfolio of options you may re-strike, and every kickoff hands you information
about the field for free.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable

FAV = 0
DOG = 1
SIDE_NAMES = {FAV: "FAV", DOG: "DOG"}

DEFAULT_DURATION = 190.0 * 60.0  # seconds; a touch over three hours


@dataclass(frozen=True)
class Game:
    """One game, with its market price expressed as a home win probability."""

    gid: str
    away: str
    home: str
    kickoff: float  # unix seconds
    p_home: float
    duration: float = DEFAULT_DURATION

    @property
    def p_fav(self) -> float:
        return max(self.p_home, 1.0 - self.p_home)

    @property
    def favorite(self) -> str:
        return self.home if self.p_home >= 0.5 else self.away

    @property
    def underdog(self) -> str:
        return self.away if self.p_home >= 0.5 else self.home

    def team(self, side: int) -> str:
        return self.favorite if side == FAV else self.underdog

    def side_of(self, team: str) -> int:
        return FAV if team == self.favorite else DOG

    def p_side(self, side: int) -> float:
        return self.p_fav if side == FAV else 1.0 - self.p_fav

    @property
    def label(self) -> str:
        return f"{self.away}@{self.home}"

    def kickoff_str(self) -> str:
        return datetime.fromtimestamp(self.kickoff, timezone.utc).strftime("%a %H:%MZ")


@dataclass
class Slate:
    """The week's games, in kickoff order."""

    games: list[Game]

    def __post_init__(self) -> None:
        self.games = sorted(self.games, key=lambda g: (g.kickoff, g.gid))
        self.index = {g.gid: i for i, g in enumerate(self.games)}

    def __len__(self) -> int:
        return len(self.games)

    def __iter__(self):
        return iter(self.games)

    def __getitem__(self, i: int) -> Game:
        return self.games[i]

    @property
    def n(self) -> int:
        return len(self.games)

    @property
    def all_points(self) -> list[int]:
        return list(range(1, self.n + 1))

    def waves(self) -> list[tuple[float, list[int]]]:
        """Games grouped by kickoff time -- one decision deadline per group."""
        out: list[tuple[float, list[int]]] = []
        for i, g in enumerate(self.games):
            if out and abs(out[-1][0] - g.kickoff) < 1.0:
                out[-1][1].append(i)
            else:
                out.append((g.kickoff, [i]))
        return out

    def elapsed_fraction(self, i: int, when: float) -> float:
        g = self.games[i]
        return min(1.0, max(0.0, (when - g.kickoff) / g.duration))


@dataclass
class Card:
    """A full entry: a confidence value and a side for every game.

    Stored positionally against the slate so the hot loops can stay on lists.
    """

    points: list[int]
    sides: list[int]

    @classmethod
    def empty(cls, n: int) -> "Card":
        return cls([0] * n, [FAV] * n)

    def copy(self) -> "Card":
        return Card(list(self.points), list(self.sides))

    def score(self, fav_won: Iterable[int]) -> int:
        return sum(p for p, s, w in zip(self.points, self.sides, fav_won) if (s == FAV) == bool(w))

    def validate(self, n: int) -> None:
        if sorted(self.points) != list(range(1, n + 1)):
            raise ValueError(f"confidence values must be a permutation of 1..{n}, got {self.points}")


@dataclass
class WeekState:
    """Everything known at the moment a decision is being made."""

    slate: Slate
    now: float
    results: dict[str, int] = field(default_factory=dict)  # gid -> 1 if favorite won
    live_wp: dict[str, float] = field(default_factory=dict)  # gid -> live favorite win prob
    my_card: dict[str, tuple[int, int]] = field(default_factory=dict)  # gid -> (points, side)
    opponents: dict[str, dict[str, tuple[int, int]]] = field(default_factory=dict)

    # --- game status -----------------------------------------------------
    def has_started(self, i: int) -> bool:
        return self.slate[i].kickoff <= self.now

    def is_final(self, i: int) -> bool:
        return self.slate[i].gid in self.results

    def locked_indices(self) -> list[int]:
        return [i for i in range(self.slate.n) if self.has_started(i)]

    def open_indices(self) -> list[int]:
        """Games still editable: confidence value and side can both change."""
        return [i for i in range(self.slate.n) if not self.has_started(i)]

    def decision_epochs(self) -> list[float]:
        """Remaining deadlines, one per distinct kickoff time still ahead."""
        return sorted({self.slate[i].kickoff for i in self.open_indices()})

    # --- my entry --------------------------------------------------------
    def locked_points(self) -> list[int]:
        return [self.my_card[self.slate[i].gid][0] for i in self.locked_indices() if self.slate[i].gid in self.my_card]

    def available_points(self) -> list[int]:
        """Confidence values not yet spent on a kicked-off game."""
        spent = set(self.locked_points())
        return [p for p in self.slate.all_points if p not in spent]

    # --- opponents -------------------------------------------------------
    def opponent_available_points(self, name: str) -> list[int]:
        """What an opponent has left.

        Their locked picks are public, and the values are a permutation, so the
        multiset of values they still hold is known exactly even though we
        cannot see where they have put them.
        """
        spent = {pts for pts, _ in self.opponents.get(name, {}).values()}
        return [p for p in self.slate.all_points if p not in spent]

    def settled_score(self, card: dict[str, tuple[int, int]]) -> int:
        total = 0
        for gid, (pts, side) in card.items():
            if gid in self.results:
                if (side == FAV) == bool(self.results[gid]):
                    total += pts
        return total


# ---------------------------------------------------------------------------
# JSON I/O
# ---------------------------------------------------------------------------


def _parse_time(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    dt = datetime.fromisoformat(str(value))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def load_week(path: str) -> WeekState:
    with open(path) as fh:
        blob = json.load(fh)
    return week_from_dict(blob)


def week_from_dict(blob: dict) -> WeekState:
    games = []
    for raw in blob["games"]:
        if "p_home" in raw:
            p_home = float(raw["p_home"])
        else:
            from .probs import moneyline_to_p_home

            p_home = moneyline_to_p_home(float(raw["home_ml"]), float(raw["away_ml"]))
        games.append(
            Game(
                gid=raw["id"],
                away=raw["away"],
                home=raw["home"],
                kickoff=_parse_time(raw["kickoff"]),
                p_home=p_home,
                duration=float(raw.get("duration_minutes", 190.0)) * 60.0,
            )
        )
    slate = Slate(games)
    now = _parse_time(blob["now"]) if "now" in blob else min(g.kickoff for g in games) - 3600.0

    state = WeekState(slate=slate, now=now)
    for gid, winner in (blob.get("results") or {}).items():
        g = slate[slate.index[gid]]
        state.results[gid] = 1 if winner in (1, "1", True, g.favorite) else 0
    state.live_wp = {k: float(v) for k, v in (blob.get("live_win_prob") or {}).items()}

    for gid, raw in (blob.get("my_picks") or {}).items():
        g = slate[slate.index[gid]]
        side = g.side_of(raw["team"]) if "team" in raw else int(raw["side"])
        state.my_card[gid] = (int(raw["points"]), side)

    for name, picks in (blob.get("opponent_picks") or {}).items():
        entry: dict[str, tuple[int, int]] = {}
        for gid, raw in picks.items():
            g = slate[slate.index[gid]]
            side = g.side_of(raw["team"]) if "team" in raw else int(raw["side"])
            entry[gid] = (int(raw["points"]), side)
        state.opponents[name] = entry
    return state


def card_from_state(state: WeekState) -> Card:
    """Positional card built from whatever picks the state carries."""
    card = Card.empty(state.slate.n)
    for gid, (pts, side) in state.my_card.items():
        i = state.slate.index[gid]
        card.points[i] = pts
        card.sides[i] = side
    return card
