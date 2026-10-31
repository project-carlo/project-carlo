"""Compare two frontend snapshots by what they say, not by how they say it.

Pure: takes decoded snapshot tables (`extract_frontend_db.read_snapshot`) and
a comparison date, and returns plain dicts. The snapshot verifier's gates,
the weekly report and `replay-gates` all use it, for both modes, since the
snapshot is the one place extract- and update-mode parishes look the same.

Each row is reduced to a fingerprint of its meaning. Row ids, row order, page
numbers, bulletin links and notes are left out, and the weeks of the month and
season become the exact set of month-days the slot can fall on
(`qualifiers.recurrence_mask`), so "every Sunday except the last" and "first
to fourth Sunday" compare equal while "every Friday" and "first Friday" don't.
A cancellation is its date plus the fingerprint of the weekly row it cancels.

Two views come out of it:

- the schedule's content: recurring slots matched, removed and added; dated
  events and cancellations removed and added; note changes alongside;
- near-term availability: both schedules expanded over the same window
  (`WINDOW_DAYS` from `as_of`), the dates a visitor could go, as the web
  app's `nextForWeekly` reads them. An occurrence is a church, event type,
  date and start time, so an end-time change is a content change but loses
  no date.

Removed and added rows of one church, type and weekday (or date) are shown
as one modification only when there is exactly one of each. That pairing is
for people; no count depends on it.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from pdf_extract.bulletin_week import parse_iso_date
from pdf_extract.labeling.labels import DAYS
from pdf_extract.schedule.qualifiers import (
    QualifierError,
    columns_to_season,
    describe_schedule_pattern,
    recurrence_includes_date,
    recurrence_mask,
    weeks_to_mask,
)
from pdf_extract.timeparse import minutes_to_time

WINDOW_DAYS = 42

_WEEKDAY = {day.lower(): index for index, day in enumerate(DAYS)}
_TYPE_LABELS = {"mass": "Mass", "confession": "Confession", "adoration": "Adoration"}
_MAX_ERRORS = 20

Tables = dict[str, list[dict[str, Any]]]
Occurrence = tuple[str, str, str, int | None]  # church slug, event type, date, start


class ComparisonError(ValueError):
    """A snapshot whose references don't resolve, so it can't be compared safely."""


@dataclass(frozen=True)
class Item:
    """One snapshot row, with its church resolved."""

    id: int
    parish_id: int | None
    church: str
    event_type: str
    kind: str
    day: str | None
    date: str | None
    start: int | None
    end: int | None
    weeks: tuple[str, ...]
    exclude: bool
    season: tuple[int | None, int | None, int | None, int | None]
    valid_from: str | None
    valid_until: str | None
    cancelled: bool
    note: str | None
    cancels: int | None

    @property
    def weekly(self) -> bool:
        return self.kind == "weekly"

    @property
    def cancellation(self) -> bool:
        return not self.weekly and self.cancelled and self.cancels is not None

    @property
    def weekday(self) -> int | None:
        return _WEEKDAY.get((self.day or "").strip().lower())

    def weeks_mask(self) -> int:
        return weeks_to_mask(list(self.weeks), self.exclude)


@dataclass
class Projection:
    """A snapshot as of one date: its rows canonical, its past rows gone."""

    as_of: date
    items: list[Item]
    by_id: dict[int, Item]
    church_parish: dict[str, int | None]
    parish_churches: dict[int | None, list[str]]
    parish_bulletin: dict[int | None, dict[str, str | None]]
    fingerprints: dict[int, tuple]

    def cancelled_dates(self) -> dict[int, set[str]]:
        """Weekly row id -> the dates cancellations name for it."""
        out: dict[int, set[str]] = {}
        for item in self.items:
            if item.cancellation and item.date:
                out.setdefault(item.cancels, set()).add(item.date)
        return out


def _item(row: dict[str, Any], church: dict[str, Any]) -> Item:
    weeks = row.get("weeks_of_month") or []
    return Item(
        id=int(row["id"]),
        parish_id=church.get("parish_id"),
        church=str(church["slug"]),
        event_type=str(row["event_type"]),
        kind=str(row["event_kind"] or "").lower(),
        day=row.get("day_of_week"),
        date=row.get("date"),
        start=row.get("start_time"),
        end=row.get("end_time"),
        weeks=tuple(weeks) if isinstance(weeks, list) else weeks,
        exclude=bool(row.get("exclude_weeks")),
        season=(
            row.get("season_start_month"), row.get("season_start_day"),
            row.get("season_end_month"), row.get("season_end_day"),
        ),
        valid_from=row.get("valid_from"),
        valid_until=row.get("valid_until"),
        cancelled=bool(row.get("cancelled")),
        note=row.get("note") or None,
        cancels=row.get("cancels_event_id"),
    )


def current_rows(tables: Tables, as_of: date) -> list[dict[str, Any]]:
    """The snapshot's event rows still to come on `as_of`, as its exporter would keep them.

    Drops dated rows before `as_of` and rows whose `valid_until` is before it.
    """
    today = as_of.isoformat()
    return [
        row for row in tables.get("events", [])
        if (str(row.get("event_kind") or "").lower() == "weekly"
            or (row.get("date") or "") >= today)
        and (row.get("valid_until") is None or row["valid_until"] >= today)
    ]


def canonicalize(tables: Tables, as_of: date) -> Projection:
    """The snapshot as it reads on `as_of`.

    Dated rows before `as_of` and rows whose `valid_until` is before it are
    dropped, as the exporter does on its build date, so a snapshot saved
    earlier compares on the same footing as one built today. Raises
    ComparisonError for an event naming a church the snapshot doesn't have,
    a cancellation naming no weekly row, and weeks of the month that can't
    be read.
    """
    today = as_of.isoformat()
    churches = {row["id"]: row for row in tables.get("churches", [])}
    errors: list[str] = []
    items: list[Item] = []
    for row in tables.get("events", []):
        church = churches.get(row["church_id"])
        if church is None:
            errors.append(
                f"event {row['id']} names church id {row['church_id']}, which is not in the "
                "snapshot's churches; rebuild the snapshot from its database"
            )
            continue
        items.append(_item(row, church))
    all_by_id = {item.id: item for item in items}
    kept = [
        item for item in items
        if (item.weekly or (item.date or "") >= today)
        and (item.valid_until is None or item.valid_until >= today)
    ]
    by_id = {item.id: item for item in kept}
    out: list[Item] = []
    for item in kept:
        if item.cancels is not None and item.cancelled and not item.weekly:
            target = all_by_id.get(item.cancels)
            if target is None or not target.weekly:
                errors.append(
                    f"`{item.church}` cancellation {item.id} on {item.date} names event "
                    f"{item.cancels}, which is not a weekly row in the snapshot"
                )
                continue
            if target.id not in by_id:
                continue  # its slot ended before as_of: nothing left to cancel
        if item.weekly:
            try:
                item.weeks_mask()
            except QualifierError as exc:
                errors.append(f"`{item.church}` event {item.id}: {exc}")
                continue
        out.append(item)
    if errors:
        more = len(errors) - _MAX_ERRORS
        raise ComparisonError(
            "; ".join(errors[:_MAX_ERRORS]) + (f"; and {more} more" if more > 0 else "")
        )
    by_id = {item.id: item for item in out}
    parish_churches: dict[int | None, list[str]] = {}
    parish_bulletin: dict[int | None, dict[str, str | None]] = {}
    for church in sorted(churches.values(), key=lambda c: str(c["slug"])):
        parish_churches.setdefault(church.get("parish_id"), []).append(str(church["slug"]))
        parish_bulletin.setdefault(church.get("parish_id"), {
            "bulletin_url": church.get("bulletin_url"),
            "bulletin_week": church.get("bulletin_week"),
        })
    projection = Projection(
        as_of=as_of,
        items=out,
        by_id=by_id,
        church_parish={str(c["slug"]): c.get("parish_id") for c in churches.values()},
        parish_churches=parish_churches,
        parish_bulletin=parish_bulletin,
        fingerprints={},
    )
    for item in out:
        projection.fingerprints[item.id] = fingerprint(item, projection)
    return projection


def slot_fingerprint(item: Item, as_of: date) -> tuple:
    """A weekly row's meaning: when it can happen, from when, until when."""
    valid_from = item.valid_from
    if valid_from is not None and valid_from <= as_of.isoformat():
        valid_from = None  # already in force: the same as no start date
    return (
        "weekly", item.church, item.event_type, (item.day or "").strip().lower(),
        item.start, item.end, recurrence_mask(item.weeks_mask(), *item.season),
        valid_from, item.valid_until, item.cancelled,
    )


def fingerprint(item: Item, projection: Projection) -> tuple:
    if item.weekly:
        return slot_fingerprint(item, projection.as_of)
    if item.cancellation:
        target = projection.by_id[item.cancels]
        return ("cancellation", item.date, slot_fingerprint(target, projection.as_of))
    return ("dated", item.church, item.event_type, item.date, item.start, item.end,
            item.cancelled)


def _section(item: Item) -> str:
    if item.weekly:
        return "recurring"
    return "cancellations" if item.cancellation else "dated"


# ── Availability ────────────────────────────────────────────────────────────
def window(as_of: date, days: int = WINDOW_DAYS) -> list[date]:
    return [as_of + timedelta(days=offset) for offset in range(days)]


def item_occurrences(
    item: Item, dates: list[date], cancelled: dict[int, set[str]],
) -> list[Occurrence]:
    """The dates in `dates` a visitor could go to this row, as the web app reads it."""
    if item.cancelled:
        return []
    if not item.weekly:
        day = parse_iso_date(item.date)
        if day is None or day not in dates:
            return []
        return [(item.church, item.event_type, item.date, item.start)]
    weekday = item.weekday
    if weekday is None:
        return []
    mask = item.weeks_mask()
    skipped = cancelled.get(item.id, set())
    out = []
    for day in dates:
        text = day.isoformat()
        if (
            day.weekday() == weekday
            and (item.valid_from is None or text >= item.valid_from)
            and (item.valid_until is None or text <= item.valid_until)
            and recurrence_includes_date(day, mask, *item.season)
            and text not in skipped
        ):
            out.append((item.church, item.event_type, text, item.start))
    return out


def availability(projection: Projection, dates: list[date]) -> dict[Occurrence, int | None]:
    """Every occurrence in `dates` -> the parish of its church."""
    cancelled = projection.cancelled_dates()
    out: dict[Occurrence, int | None] = {}
    for item in projection.items:
        for occurrence in item_occurrences(item, dates, cancelled):
            out[occurrence] = item.parish_id
    return out


# ── Descriptions ────────────────────────────────────────────────────────────
def _time_range(item: Item) -> str:
    start = minutes_to_time(item.start) or "?"
    end = minutes_to_time(item.end)
    return f"{start}–{end}" if end else start


def _pattern(item: Item) -> str:
    day = (item.day or "").strip().capitalize() or "week"
    pattern = describe_schedule_pattern(
        list(item.weeks), columns_to_season(*item.season), item.day, item.exclude,
    )
    return pattern or f"every {day}"


def describe_parts(item: Item, projection: Projection | None = None) -> tuple[str, list[str]]:
    """(head, details): "Adoration · Fri", ["7:00 PM–8:00 PM", "every Friday"]."""
    label = _TYPE_LABELS.get(item.event_type, item.event_type or "Event")
    if item.weekly:
        head = f"{label} · {(item.day or '?').strip().capitalize()[:3]}"
        details = [_time_range(item), _pattern(item)]
        if item.valid_from:
            details.append(f"from {item.valid_from}")
        if item.valid_until:
            details.append(f"through {item.valid_until}")
    else:
        head = f"{label} · {item.date or '?'}"
        details = [_time_range(item)]
        if item.cancellation and projection is not None:
            target = projection.by_id.get(item.cancels)
            if target is not None:
                details.append(f"cancels {describe(target)}")
    if item.cancelled:
        details.append("cancelled")
    return head, details


def describe(item: Item, projection: Projection | None = None) -> str:
    """"Adoration · Fri 7:00 PM–8:00 PM, First Friday of the month"."""
    head, details = describe_parts(item, projection)
    return f"{head} {', '.join(details)}"


def describe_change(before: Item, after: Item) -> str:
    """"Adoration · Fri 7:00 PM–8:00 PM, every Friday → First Friday of the month"."""
    head_b, details_b = describe_parts(before)
    head_a, details_a = describe_parts(after)
    if head_a != head_b:
        return f"{describe(before)} → {describe(after)}"
    changed = [d for d in details_a if d not in details_b] or details_a
    return f"{head_b} {', '.join(details_b)} → {', '.join(changed)}"


# ── The comparison ──────────────────────────────────────────────────────────
def _item_dict(
    item: Item, projection: Projection, dates: list[date],
    cancelled: dict[int, set[str]], lost: set[Occurrence] | None = None,
) -> dict[str, Any]:
    occurrences = item_occurrences(item, dates, cancelled)
    out = {
        "church_slug": item.church,
        "event_type": item.event_type,
        "event_kind": item.kind,
        "day_of_week": item.day,
        "date": item.date,
        "start_time": minutes_to_time(item.start),
        "end_time": minutes_to_time(item.end),
        "weeks_of_month": list(item.weeks),
        "exclude_weeks": item.exclude,
        "season": columns_to_season(*item.season),
        "valid_from": item.valid_from,
        "valid_until": item.valid_until,
        "cancelled": item.cancelled,
        "note": item.note,
        "summary": describe(item, projection),
        "window_dates": len(occurrences),
    }
    if lost is not None:
        out["window_dates_lost"] = sum(1 for o in occurrences if o in lost)
    return out


def _window_note(before: dict[str, Any]) -> str:
    total, lost = before.get("window_dates", 0), before.get("window_dates_lost", 0)
    if not total:
        return ""
    return f"; {lost} of {total} dates in the window removed" if lost else ""


def _pair_key(item: Item) -> tuple:
    return (item.church, item.event_type, item.kind, (item.day or "").lower() or item.date)


def _changes(
    removed: list[Item], added: list[Item],
    before: Projection, after: Projection, dates: list[date], lost: set[Occurrence],
    *, pair: bool,
) -> list[dict[str, Any]]:
    """Removed and added rows, a lone removal and addition of one slot paired up."""
    cancelled_b, cancelled_a = before.cancelled_dates(), after.cancelled_dates()
    by_key: dict[tuple, tuple[list[Item], list[Item]]] = {}
    for item in removed:
        by_key.setdefault(_pair_key(item), ([], []))[0].append(item)
    for item in added:
        by_key.setdefault(_pair_key(item), ([], []))[1].append(item)
    out = []
    for key in sorted(by_key, key=lambda k: tuple("" if v is None else str(v) for v in k)):
        olds, news = by_key[key]
        if pair and len(olds) == 1 and len(news) == 1:
            old = _item_dict(olds[0], before, dates, cancelled_b, lost)
            new = _item_dict(news[0], after, dates, cancelled_a)
            out.append({
                "change": "modified", "church_slug": key[0], "before": old, "after": new,
                "summary": describe_change(olds[0], news[0]) + _window_note(old),
            })
            continue
        for item in sorted(olds, key=lambda i: (i.start or 0, i.id)):
            old = _item_dict(item, before, dates, cancelled_b, lost)
            out.append({
                "change": "removed", "church_slug": item.church, "before": old, "after": None,
                "summary": old["summary"] + _window_note(old),
            })
        for item in sorted(news, key=lambda i: (i.start or 0, i.id)):
            new = _item_dict(item, after, dates, cancelled_a)
            out.append({
                "change": "added", "church_slug": item.church, "before": None, "after": new,
                "summary": new["summary"],
            })
    return out


def _first(projection: Projection) -> dict[tuple, Item]:
    """Fingerprint -> its lowest-id row."""
    out: dict[tuple, Item] = {}
    for item in sorted(projection.items, key=lambda i: i.id):
        out.setdefault(projection.fingerprints[item.id], item)
    return out


def _notes(projection: Projection) -> dict[tuple, tuple[str, ...]]:
    notes: dict[tuple, set[str]] = {}
    for item in projection.items:
        bucket = notes.setdefault(projection.fingerprints[item.id], set())
        if item.note:
            bucket.add(item.note)
    return {fp: tuple(sorted(values)) for fp, values in notes.items()}


def _shown(projection: Projection, firsts: dict[tuple, Item]) -> Counter:
    """Parish -> the distinct recurring and dated items it shows (not cancelled)."""
    return Counter(
        item.parish_id for item in firsts.values() if not item.cancelled and not item.cancellation
    )


def compare(
    previous: Tables, current: Tables, as_of: date, window_days: int = WINDOW_DAYS,
) -> dict[str, Any]:
    """What changed between two snapshots, read on the same date.

    Raises ComparisonError when either snapshot can't be canonicalized.
    """
    before = canonicalize(previous, as_of)
    after = canonicalize(current, as_of)
    dates = window(as_of, window_days)
    firsts_b, firsts_a = _first(before), _first(after)
    avail_b, avail_a = availability(before, dates), availability(after, dates)
    lost = set(avail_b) - set(avail_a)
    gained = set(avail_a) - set(avail_b)

    parishes: dict[int | None, dict[str, Any]] = {}

    def parish(parish_id: int | None) -> dict[str, Any]:
        if parish_id not in parishes:
            parishes[parish_id] = {
                "parish_id": parish_id,
                "churches": after.parish_churches.get(parish_id)
                or before.parish_churches.get(parish_id) or [],
                **(after.parish_bulletin.get(parish_id)
                   or before.parish_bulletin.get(parish_id)
                   or {"bulletin_url": None, "bulletin_week": None}),
                "events_before": 0, "events_after": 0,
                "recurring_before": 0, "recurring_after": 0, "recurring_matched": 0,
                "recurring_removed": 0, "recurring_added": 0,
                "dated_removed": 0, "dated_added": 0,
                "cancellations_removed": 0, "cancellations_added": 0,
                "recurring": [], "dated": [], "cancellations": [], "notes": [],
                "diagnostics": [],
                "availability": {"before": 0, "after": 0, "lost": 0, "gained": 0, "groups": []},
            }
        return parishes[parish_id]

    for parish_id in set(before.parish_churches) | set(after.parish_churches):
        parish(parish_id)
    for parish_id, count in _shown(before, firsts_b).items():
        parish(parish_id)["events_before"] = count
    for parish_id, count in _shown(after, firsts_a).items():
        parish(parish_id)["events_after"] = count

    # Content: removed and added fingerprints per section and parish.
    removed: dict[tuple, list[Item]] = {}
    added: dict[tuple, list[Item]] = {}
    for fp, item in firsts_b.items():
        section = _section(item)
        if section == "recurring":
            parish(item.parish_id)["recurring_before"] += 1
        if fp not in firsts_a:
            removed.setdefault((item.parish_id, section), []).append(item)
    for fp, item in firsts_a.items():
        section = _section(item)
        if section == "recurring":
            parish(item.parish_id)["recurring_after"] += 1
            if fp in firsts_b:
                parish(firsts_b[fp].parish_id)["recurring_matched"] += 1
        if fp not in firsts_b:
            added.setdefault((item.parish_id, section), []).append(item)
    for parish_id, section in set(removed) | set(added):
        olds = removed.get((parish_id, section), [])
        news = added.get((parish_id, section), [])
        entry = parish(parish_id)
        entry[f"{section}_removed"] += len(olds)
        entry[f"{section}_added"] += len(news)
        entry[section] = _changes(
            olds, news, before, after, dates, lost, pair=section != "cancellations",
        )

    # Notes on rows that still mean the same thing.
    notes_b, notes_a = _notes(before), _notes(after)
    for fp in sorted(set(firsts_b) & set(firsts_a), key=lambda f: firsts_a[f].id):
        if notes_b[fp] != notes_a[fp]:
            item = firsts_a[fp]
            parish(item.parish_id)["notes"].append({
                "church_slug": item.church,
                "summary": describe(item, after),
                "before": list(notes_b[fp]),
                "after": list(notes_a[fp]),
            })

    # Rows that say the same thing twice: compared once, reported here.
    counts = Counter(after.fingerprints.values())
    for fp, count in counts.items():
        if count > 1:
            item = firsts_a[fp]
            parish(item.parish_id)["diagnostics"].append(
                f"`{item.church}` {describe(item, after)} appears {count} times"
            )

    # Availability, per parish and per church and event type.
    groups: dict[tuple, dict[str, Any]] = {}
    for side, occurrences in (("before", avail_b), ("after", avail_a)):
        for occurrence, parish_id in occurrences.items():
            church, event_type = occurrence[0], occurrence[1]
            parish(parish_id)["availability"][side] += 1
            group = groups.setdefault((parish_id, church, event_type), {
                "church_slug": church, "event_type": event_type,
                "before": 0, "after": 0, "lost": 0, "gained": 0, "lost_dates": [],
            })
            group[side] += 1
    for occurrence in lost:
        parish_id = avail_b[occurrence]
        parish(parish_id)["availability"]["lost"] += 1
        group = groups[(parish_id, occurrence[0], occurrence[1])]
        group["lost"] += 1
        group["lost_dates"].append(f"{occurrence[2]} {minutes_to_time(occurrence[3])}")
    for occurrence in gained:
        parish_id = avail_a[occurrence]
        parish(parish_id)["availability"]["gained"] += 1
        groups[(parish_id, occurrence[0], occurrence[1])]["gained"] += 1
    for (parish_id, _church, _type), group in sorted(
        groups.items(), key=lambda kv: (str(kv[0][1]), str(kv[0][2])),
    ):
        group["lost_dates"].sort()
        parish(parish_id)["availability"]["groups"].append(group)

    recurring_before = len([i for i in firsts_b.values() if i.weekly])
    matched = sum(p["recurring_matched"] for p in parishes.values())
    return {
        "as_of": as_of.isoformat(),
        "window": {
            "start": dates[0].isoformat() if dates else as_of.isoformat(),
            "end": (as_of + timedelta(days=window_days)).isoformat(),
            "days": window_days,
        },
        "recurring": {
            "before": recurring_before,
            "after": len([i for i in firsts_a.values() if i.weekly]),
            "matched": matched,
            "removed": recurring_before - matched,
            "added": sum(p["recurring_added"] for p in parishes.values()),
        },
        "availability": {
            "before": len(avail_b), "after": len(avail_a),
            "lost": len(lost), "gained": len(gained),
        },
        "parishes": [parishes[k] for k in sorted(parishes, key=lambda k: (k is None, k or 0))],
    }


def parish_changed(section: dict[str, Any]) -> bool:
    """Whether a parish's schedule content changed (notes and duplicates aside)."""
    return bool(section["recurring"] or section["dated"] or section["cancellations"])
