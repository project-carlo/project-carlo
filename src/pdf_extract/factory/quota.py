"""Quota attribution: how many five-hour and weekly points an attempt used, from readings.

Computed on demand from the ledger's usage readings and attempt times, never stored. The
meter shows whole percents and lags by a minute or two, so every answer is a range with a
label, never a bare number:

- settled: an idle reading before, a reading `settle` after it finished, and no other
  attempt on the account in between: the delta ±1 (a displayed 0 is [0, 1)).
- immediate: the only reading after came sooner than `settle`: a minimum.
- shared: another attempt on the account started before this one settled. The group's
  total over its combined interval is measured; no exact share per attempt (the first
  one's early reading still gives it a minimum).
- reset: the window reset in between (resets_at jumped, or the meter fell): a minimum.
- missing or inconsistent (the meter fell without a reset): no number.

An account's meter rising while the factory was idle on it is outside use: attempts near
it are flagged. Account and window totals (`window_totals`) stay useful when per-attempt
attribution is uncertain.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

WINDOWS = ("five_hour", "seven_day")
SETTLED, IMMEDIATE, SHARED, RESET = "settled", "immediate", "shared", "reset"
MISSING, INCONSISTENT = "missing", "inconsistent"
# Worst first: a job's label is its worst attempt's.
ORDER = (INCONSISTENT, MISSING, RESET, SHARED, IMMEDIATE, SETTLED)
# Reset times jitter by a second or so between readings.
TOLERANCE = timedelta(minutes=3)
# How close to a rise while idle an attempt is flagged as possibly including outside use.
NEARBY = timedelta(hours=1)


def when(value: Any) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


@dataclass(frozen=True)
class Reading:
    id: int
    account: str
    at: datetime
    values: dict[str, float | None]
    resets: dict[str, datetime | None]
    source: str = "select"
    attempt_id: int | None = None

    @classmethod
    def from_row(cls, row: Any) -> Reading:
        keys = row.keys()
        return cls(row["id"], row["account"], when(row["at"]),  # type: ignore[arg-type]
                   {w: row[w] for w in WINDOWS}, {w: when(row[f"{w}_resets"]) for w in WINDOWS},
                   row["source"] if "source" in keys else "select",
                   row["attempt_id"] if "attempt_id" in keys else None)

    def brief(self, window: str) -> dict[str, Any]:
        resets = self.resets[window]
        return {"id": self.id, "at": self.at.isoformat(), "source": self.source,
                "value": self.values[window], "resets": resets.isoformat() if resets else None}


@dataclass(frozen=True)
class Span:
    """An attempt's time on its account."""

    id: int
    job_id: int
    account: str | None
    started: datetime
    finished: datetime | None

    @classmethod
    def from_row(cls, row: Any) -> Span:
        return cls(row["id"], row["job_id"], row["account"],
                   when(row["started_at"]), when(row["finished_at"]))  # type: ignore[arg-type]


@dataclass
class Measure:
    """One attempt's points in one window."""

    window: str
    label: str
    low: float | None = None
    high: float | None = None  # None with a low: a minimum
    before: Reading | None = None
    after: Reading | None = None
    group: list[int] = field(default_factory=list)  # the attempts measured together
    group_low: float | None = None
    group_high: float | None = None
    outside_use: bool = False
    approximate: bool = False
    note: str = ""

    def text(self) -> str:
        out = f"{self.label} {range_text(self.low, self.high)}"
        if self.group:
            out += (f" (group {','.join(map(str, self.group))}: "
                    f"{range_text(self.group_low, self.group_high)})")
        if self.outside_use:
            out += " outside use?"
        if self.approximate:
            out += " approx"
        return out

    def as_dict(self) -> dict[str, Any]:
        return {"label": self.label, "low": self.low, "high": self.high,
                "text": range_text(self.low, self.high), "group": self.group,
                "group_low": self.group_low, "group_high": self.group_high, "outside_use": self.outside_use,
                "approximate": self.approximate, "note": self.note,
                "before": self.before.brief(self.window) if self.before else None,
                "after": self.after.brief(self.window) if self.after else None}


def _num(x: float) -> str:
    return f"{x:g}"


def range_text(low: float | None, high: float | None) -> str:
    if low is None:
        return "-"
    if high is None:
        return f"≥{_num(low)}"
    if low == 0 and high == 1:
        return "<1"
    return f"{_num(low)}–{_num(high)}"


def _delta_range(d: float, settled: bool) -> tuple[float, float | None]:
    """Each reading rounds to a whole percent: the true delta is within ±1."""
    if not settled:
        return max(0.0, d - 1), None
    return max(0.0, d - 1), d + 1


@dataclass
class _Group:
    spans: list[Span]
    before: Reading | None = None
    end: Reading | None = None
    settled: bool = False
    first_after: Reading | None = None  # an early reading between the first two members
    why: str = ""

    @property
    def ids(self) -> list[int]:
        return [s.id for s in self.spans]


def _jumped(a: Reading, b: Reading, window: str, tolerance: timedelta) -> bool:
    ra, rb = a.resets[window], b.resets[window]
    # A window with nothing used yet has no real reset time to compare.
    return bool(a.values[window]) and ra is not None and rb is not None \
        and abs(rb - ra) > tolerance


def _delta(a: Reading, b: Reading, window: str,
           tolerance: timedelta) -> tuple[str, float | None]:
    va, vb, resets = a.values[window], b.values[window], a.resets[window]
    if va is None or vb is None:
        return MISSING, None
    # The window reset: its reset time moved, or passed before the second reading.
    if _jumped(a, b, window, tolerance) or (va and resets is not None
                                             and resets < b.at - tolerance):
        return RESET, vb
    if vb < va:
        return INCONSISTENT, None
    return "ok", vb - va


class Analysis:
    """Every attempt's measures, idle rises and window totals, for one set of readings."""

    def __init__(self, spans: list[Span], readings: list[Reading], settle: timedelta,
                 tolerance: timedelta = TOLERANCE,
                 approximate: frozenset[int] | set[int] = frozenset()) -> None:
        self.settle, self.tolerance, self.approximate = settle, tolerance, set(approximate)
        self.spans = sorted(spans, key=lambda s: s.started)
        self.readings = sorted(readings, key=lambda r: r.at)
        self.groups: dict[int, _Group] = {}
        self.rises: list[dict[str, Any]] = []
        accounts = sorted({s.account for s in self.spans if s.account}
                          | {r.account for r in self.readings})
        for account in accounts:
            mine = [s for s in self.spans if s.account == account]
            reads = [r for r in self.readings if r.account == account]
            for g in self._chain(mine):
                self._measure(g, mine, reads)
            self.rises += self._idle_rises(account, mine, reads)

    # ── Groups: attempts on an account less than `settle` apart ──────────────
    def _chain(self, spans: list[Span]) -> list[_Group]:
        groups: list[_Group] = []
        for s in spans:
            last = groups[-1].spans[-1] if groups else None
            if last is not None and (last.finished is None
                                     or s.started - last.finished < self.settle):
                groups[-1].spans.append(s)
            else:
                groups.append(_Group([s]))
        for g in groups:
            for s in g.spans:
                self.groups[s.id] = g
        return groups

    def _measure(self, g: _Group, spans: list[Span], reads: list[Reading]) -> None:
        start, end = g.spans[0].started, g.spans[-1].finished
        if end is None:
            g.why = "still running"
            return
        prev = [s for s in spans if s.finished is not None and s.finished <= start
                and s not in g.spans]
        nxt = [s for s in spans if s.started > end]
        idle_from = max((s.finished for s in prev), default=None)  # type: ignore[type-var]
        before = [r for r in reads if r.at <= start
                  and (idle_from is None or r.at >= idle_from + self.settle)]
        if not before:
            g.why = "no idle reading before"
            return
        g.before = before[-1]
        until = nxt[0].started if nxt else None
        after = [r for r in reads if r.at >= end and (until is None or r.at <= until)]
        if not after:
            g.why = "no reading after"
            return
        settled = [r for r in after if r.at >= end + self.settle]
        g.end, g.settled = (settled[0], True) if settled else (after[0], False)
        if len(g.spans) > 1:
            first, second = g.spans[0], g.spans[1]
            early = [r for r in reads if first.finished is not None
                     and first.finished <= r.at <= second.started]
            g.first_after = early[0] if early else None

    # ── Per attempt ─────────────────────────────────────────────────────────
    def measure(self, span: Span, window: str) -> Measure:
        m = Measure(window, MISSING, approximate=span.id in self.approximate)
        if span.account is None:
            m.note = "no account (a stub run)"
            return m
        g = self.groups.get(span.id)
        if g is None or g.before is None or g.end is None:
            m.note = g.why if g else "no readings"
            return m
        m.before, m.after = g.before, g.end
        settled = g.settled and not any(s.id in self.approximate for s in g.spans)
        kind, d = _delta(g.before, g.end, window, self.tolerance)
        m.outside_use = self._near_rise(span.account, g.before.at, g.end.at)
        if len(g.spans) > 1:
            m.group = g.ids
        if kind == MISSING:
            m.note = f"no {window} in a reading"
            return m
        if kind == INCONSISTENT:
            m.label, m.note = INCONSISTENT, "the meter fell without a reset"
            return m
        assert d is not None
        if kind == RESET:
            m.label, m.note = RESET, "the window reset in between: a minimum"
            m.low = max(0.0, d - 1) if not m.group else 0.0
            return m
        if not m.group:
            m.label = SETTLED if settled else IMMEDIATE
            m.low, m.high = _delta_range(d, settled)
            if not g.settled:
                m.note = "read sooner than the meter settles: a minimum"
            elif not settled:
                m.note = "historical: treated as a minimum"
            return m
        m.label = SHARED
        m.group_low, m.group_high = _delta_range(d, settled)
        m.low, m.high = 0.0, m.group_high
        m.note = "another attempt ran before this one settled: the group's total"
        if span.id == g.spans[0].id and g.first_after is not None:
            k, d1 = _delta(g.before, g.first_after, window, self.tolerance)
            if k == "ok" and d1 is not None:
                m.low = max(0.0, d1 - 1)
        return m

    # ── Outside use ─────────────────────────────────────────────────────────
    def _idle(self, spans: list[Span], a: datetime, b: datetime) -> bool:
        """No attempt on the account ran in [a - settle, b]."""
        return not any(s.started <= b and (s.finished is None or s.finished > a - self.settle)
                       for s in spans)

    def _idle_rises(self, account: str, spans: list[Span],
                    reads: list[Reading]) -> list[dict[str, Any]]:
        out = []
        for a, b in zip(reads, reads[1:], strict=False):
            if not self._idle(spans, a.at, b.at):
                continue
            for w in WINDOWS:
                kind, d = _delta(a, b, w, self.tolerance)
                if kind == "ok" and d:
                    out.append({"account": account, "window": w, "from": a.at, "to": b.at,
                                "points": d, "readings": [a.id, b.id]})
        return out

    def _near_rise(self, account: str, a: datetime, b: datetime) -> bool:
        return any(r["account"] == account and r["from"] - NEARBY <= b
                   and r["to"] + NEARBY >= a for r in self.rises)

    # ── Account and window totals ───────────────────────────────────────────
    def window_totals(self) -> list[dict[str, Any]]:
        """Per account, window and window instance (keyed by its reset time): the points
        used, the factory's settled, shared and uncertain portions, and the rest."""
        out = []
        groups = list({id(g): g for g in self.groups.values()}.values())
        for account in sorted({r.account for r in self.readings}):
            reads = [r for r in self.readings if r.account == account]
            for w in WINDOWS:
                for inst in _instances(reads, w, self.tolerance):
                    ids = {r.id for r in inst}
                    parts = {"settled": 0.0, "shared": 0.0, "uncertain": 0.0}
                    for g in groups:
                        if g.before is None or g.end is None or g.spans[0].account != account \
                                or g.before.id not in ids or g.end.id not in ids:
                            continue
                        kind, d = _delta(g.before, g.end, w, self.tolerance)
                        if kind != "ok" or d is None:
                            continue
                        settled = g.settled and not any(s.id in self.approximate
                                                        for s in g.spans)
                        key = ("shared" if len(g.spans) > 1 else "settled") if settled \
                            else "uncertain"
                        parts[key] += d
                    total = max(r.values[w] or 0 for r in inst)
                    resets = next((r.resets[w] for r in inst if r.values[w]), None)
                    out.append({
                        "account": account, "window": w,
                        "resets": resets.isoformat() if resets else None,
                        "first": inst[0].at.isoformat(), "last": inst[-1].at.isoformat(),
                        "readings": len(inst), "total": total, **parts,
                        "unexplained": max(0.0, total - sum(parts.values())),
                        "idle_rises": sum(r["points"] for r in self.rises
                                          if r["account"] == account and r["window"] == w
                                          and r["readings"][1] in ids),
                    })
        return out


def _instances(reads: list[Reading], w: str, tolerance: timedelta) -> list[list[Reading]]:
    """Readings split where the window reset."""
    out: list[list[Reading]] = []
    resets: datetime | None = None
    for r in reads:
        v, rs = r.values[w], r.resets[w]
        if v is None:
            continue
        last = out[-1][-1].values[w] if out else None
        jumped = resets is not None and rs is not None and abs(rs - resets) > tolerance
        if not out or (jumped and (v > 0 or (last or 0) > 0)) or (last and v < last):
            out.append([])
            resets = None
        if v > 0 and resets is None:
            resets = rs
        out[-1].append(r)
    return out


def combine(measures: list[Measure]) -> dict[str, Any]:
    """A job's points in one window, over its attempts: the sum of their ranges."""
    if not measures:
        return {"label": MISSING, "low": None, "high": None, "text": "-"}
    label = min((m.label for m in measures), key=ORDER.index)
    low: float | None = sum(m.low or 0 for m in measures)
    highs = [m.high for m in measures]
    high = None if any(h is None for h in highs) else sum(h for h in highs if h is not None)
    if label in (MISSING, INCONSISTENT):
        low, high = (low or None), None
    return {"label": label, "low": low, "high": high, "text": range_text(low, high),
            "outside_use": any(m.outside_use for m in measures),
            "approximate": any(m.approximate for m in measures)}


# ── Work units and the prompt/context version ───────────────────────────────
def work_units(stage: str, inputs: dict[str, Any],
               batches: list[dict[str, Any]] | None = None) -> int | None:
    """What a job completes: map, the batch's roster entries; seed and seed-review, their
    parishes; anything else (survey, its review, integrate...) 1. None if unknown."""
    if stage == "map":
        entries = inputs.get("entries")
        if not entries and batches is not None:
            entries = next((b.get("entries") for b in batches
                            if b.get("id") == inputs.get("batch")), None)
        return len(entries) if entries else None
    if stage in ("seed", "seed-review"):
        parishes = inputs.get("parishes") or ([inputs["parish"]] if inputs.get("parish")
                                              else [])
        return len(parishes) or 1
    return 1


def fingerprint(spec_text: str, prompt_text: str, skills: list[str]) -> str:
    """The stage's prompt and context configuration: its spec, prompt file and skills."""
    blob = json.dumps([spec_text, prompt_text, sorted(skills)])
    return hashlib.sha256(blob.encode()).hexdigest()[:12]
