"""What is left to do in a diocese: coverage against rosters, the structure audit, todo.

`coverage` answers "which places on this list have we not accounted for?".
Every roster entry should end up linked to a church, an exclusion or an open
question. Entries are matched automatically on address and on name + town,
and a match you confirm by hand is saved on the record (`roster: [...]`), so
the naming artefacts that make up most of any diff (hamlet vs town, parish
name vs building name, "St. Jude" vs "St. Jude Chapel") are resolved once, not
every session.

`audit` answers the question coverage cannot see: are two parish rows really
one bulletin? Coverage counts buildings, and a family carried as four rows
instead of one has every building accounted for.
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections.abc import Mapping
from typing import Any

from pdf_extract.dioceses import records, web
from pdf_extract.dioceses.records import CHURCH, EXCLUDED, OPEN, PARISH, Diocese, DioceseError
from pdf_extract.dioceses.rosters import load_roster, roster_names

# ── Normalising names and addresses ─────────────────────────────────────────
_STREET = {
    "ave": "avenue", "av": "avenue", "st": "street", "rd": "road", "dr": "drive",
    "blvd": "boulevard", "ln": "lane", "pkwy": "parkway", "hwy": "highway", "ct": "court",
    "pl": "place", "ter": "terrace", "cir": "circle", "sq": "square", "tpke": "turnpike",
    "rt": "route", "rte": "route", "n": "north", "s": "south", "e": "east", "w": "west",
}
# Words that differ between lists naming the same building: the honorific, and
# "church"/"parish" (lists name the parish where we name the building).
_NAME_NOISE = re.compile(
    r"\b(the|of|church|parish|roman|catholic|rc|basilica|oratory|chapel|shrine|national"
    r"|cathedral|co cathedral|mission|worship site|community)\b"
)


def norm_name(name: str) -> str:
    s = unicodedata.normalize("NFKD", str(name or "")).lower().replace("&", " and ")
    s = re.sub(r"\([^)]*\)", " ", s)                 # "St. Mary's (Swormville)"
    s = re.sub(r"\b(\w+)['’]s\b", r"\1", s)          # mary's -> mary
    s = re.sub(r"\b(ss|sts)\b\.?", "saints", s)
    s = re.sub(r"\bst\b\.?", "saint", s)
    s = re.sub(r"\bmt\b\.?", "mount", s)
    s = s.replace("katherine", "katharine")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = _NAME_NOISE.sub(" ", s)
    return " ".join(s.split())


def norm_line1(line1: str) -> str:
    s = re.sub(r"[.,#]", " ", str(line1 or "").lower())
    s = re.sub(r"\b(suite|ste|apt|unit|po box|p o box)\b.*$", "", s)
    return " ".join(_STREET.get(w, w) for w in s.split())


def norm_city(city: str, aliases: Mapping[str, str]) -> str:
    c = " ".join(re.sub(r"[^a-z0-9 ]", " ", str(city or "").lower()).split())
    return aliases.get(c, c)


def metres_apart(a: Mapping[str, Any], b: Mapping[str, Any]) -> float | None:
    try:
        lat1, lon1 = float(a["latitude"]), float(a["longitude"])
        lat2, lon2 = float(b["latitude"]), float(b["longitude"])
    except (KeyError, TypeError, ValueError):
        return None
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))


# Two entries of one roster with the same name and town are one building listed
# twice only if they are also close together (Buffalo's feed had St. Mary,
# Mayville at "24 E. Chautauqua St" and "22 East Chautauqua St", 30 m apart).
SAME_SITE_METRES = 200


def _aliases(diocese: str) -> dict[str, str]:
    raw = records.load_meta(diocese).get("city_aliases") or {}
    return {norm_city(k, {}): norm_city(v, {}) for k, v in dict(raw).items()}


# ── Coverage ────────────────────────────────────────────────────────────────
def _index(d: Diocese, aliases: Mapping[str, str]) -> dict[str, dict[str, list[str]]]:
    """Match keys of every church, exclusion and open question -> record labels."""
    idx: dict[str, dict[str, list[str]]] = {"address": {}, "name": {}, "street": {}}
    for kind in (CHURCH, EXCLUDED, OPEN):
        for slug, r in d.of(kind).items():
            label = f"{kind.name}:{slug}"
            city = norm_city(r.get("city", ""), aliases)
            line1 = norm_line1(r.get("line1", ""))
            if line1:
                idx["address"].setdefault(f"{line1}|{city}", []).append(label)
                idx["street"].setdefault(line1, []).append(label)
            name = norm_name(r.get("name", ""))
            if name:
                idx["name"].setdefault(f"{name}|{city}", []).append(label)
    return idx


def _links(d: Diocese) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for kind in (CHURCH, EXCLUDED, OPEN):
        for slug, r in d.of(kind).items():
            for ref in r.get("roster") or []:
                out.setdefault(str(ref), []).append(f"{kind.name}:{slug}")
    return out


def _match(entry: Mapping[str, Any], idx: Mapping[str, Mapping[str, list[str]]],
           aliases: Mapping[str, str]) -> tuple[str, list[str]]:
    """The first net that catches the entry, and what it caught."""
    city = norm_city(entry.get("city", ""), aliases)
    line1 = norm_line1(entry.get("line1", ""))
    nets = [
        ("address", idx["address"].get(f"{line1}|{city}") if line1 else None),
        ("name", idx["name"].get(f"{norm_name(entry.get('name', ''))}|{city}")),
        ("group-name", idx["name"].get(f"{norm_name(entry.get('group', ''))}|{city}")
         if entry.get("group") else None),
        # Same street address in a differently spelled town: a hamlet vs its town.
        ("street-only", idx["street"].get(line1) if line1 else None),
    ]
    for net, hits in nets:
        if hits:
            return net, sorted(set(hits))
    return "", []


def coverage(diocese: str, roster: str | None = None, *, link: bool = False,
             show_matched: bool = False) -> dict[str, Any]:
    """Account for every roster entry: a church, an exclusion, an open question, or unmatched.

    `link` saves every unambiguous automatic match (all but street-only) on the
    record it matched, so the next run is exact. Coverage is of the roster, not
    of the diocese: a place no roster lists moves no number here.
    """
    names = [roster] if roster else roster_names(diocese)
    if not names:
        raise DioceseError(f"{diocese!r} has no rosters yet: `diocese roster fetch` or "
                           "`diocese roster import` one")
    d = records.load(diocese)
    aliases = _aliases(diocese)
    idx = _index(d, aliases)
    explicit = _links(d)
    _, off_site = records.unpublished(d)
    to_link: dict[str, set[str]] = {}
    reports = []
    in_any_roster: set[str] = set()
    for name in names:
        data = load_roster(diocese, name)
        rep: dict[str, Any] = {"roster": name, "title": data.get("title", ""),
                               "fetched": data.get("fetched", ""), "entries": len(data["entries"])}
        seen: dict[str, dict[str, Any]] = {}
        counts = {"church": 0, "excluded": 0, "open": 0, "repeat": 0, "unmatched": 0,
                  "off_site": 0}
        unmatched, auto, loose, ambiguous, repeats = [], [], [], [], []
        for entry in data["entries"]:
            ref = f"{name}:{entry.get('id')}"
            brief = {"ref": ref, "name": entry.get("name", ""), "group": entry.get("group", ""),
                     "address": ", ".join(str(entry[k]) for k in ("line1", "city")
                                          if entry.get(k)),
                     **({"website": entry["website"]} if entry.get("website") else {})}
            if ref in explicit:
                labels = explicit[ref]
                counts[labels[0].split(":")[0]] += 1
                counts["off_site"] += labels[0].removeprefix("church:") in off_site
                in_any_roster.update(labels)
                continue
            key = f"{norm_name(entry.get('name', ''))}|{norm_city(entry.get('city', ''), aliases)}"
            first = seen.get(key)
            if first is not None:
                gap = metres_apart(first, entry)
                if gap is None or gap <= SAME_SITE_METRES:
                    counts["repeat"] += 1
                    repeats.append({**brief, "repeat_of": f"{name}:{first.get('id')}"})
                    continue
            seen.setdefault(key, entry)
            net, hits = _match(entry, idx, aliases)
            if not hits:
                counts["unmatched"] += 1
                unmatched.append(brief)
                continue
            if len(hits) > 1:
                counts["unmatched"] += 1
                ambiguous.append({**brief, "candidates": hits, "net": net})
                continue
            counts[hits[0].split(":")[0]] += 1
            counts["off_site"] += hits[0].removeprefix("church:") in off_site
            in_any_roster.add(hits[0])
            match = {**brief, "matched": hits[0], "net": net}
            if net == "street-only":
                loose.append(match)
            else:
                auto.append(match)
                if link:
                    to_link.setdefault(hits[0], set()).add(ref)
        unique = rep["entries"] - counts["repeat"]
        accounted = counts["church"] + counts["excluded"] + counts["open"]
        rep["counts"] = counts
        rep["accounted_for"] = f"{accounted}/{unique}" + (
            f" ({accounted / unique:.0%})" if unique else "")
        # Churches of a `no_bulletin` parish are accounted for, but not on the site.
        live, shown = unique - counts["excluded"], counts["church"] - counts["off_site"]
        rep["modelled"] = f"{shown}/{live}" + (
            f" ({shown / live:.0%}) of the entries not excluded, as churches on the site"
            if live else "")
        rep["unmatched"] = _group(unmatched)
        if ambiguous:
            rep["ambiguous"] = ambiguous
        if loose:
            rep["street_only_matches"] = loose
        if repeats:
            rep["repeats"] = repeats
        rep["auto_matched"] = len(auto)
        if show_matched:
            rep["auto_matches"] = auto
        reports.append(rep)

    result: dict[str, Any] = {"diocese": diocese, "rosters": reports}
    if roster is None:
        result["churches_in_no_roster"] = sorted(
            slug for slug in d.of(CHURCH) if f"church:{slug}" not in in_any_roster
        )
    if link and to_link:
        result["linked"] = _save_links(d, to_link)
    elif to_link or any(r["auto_matched"] for r in reports):
        result["hint"] = ("run with --link to save the automatic matches on their records; "
                          "check the street_only_matches and ambiguous ones by hand and add "
                          "the ref to the record's roster list")
    return result


def _group(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for e in entries:
        out.setdefault(e.get("group") or "(no group)", []).append(
            {k: v for k, v in e.items() if k != "group"})
    return dict(sorted(out.items()))


def _save_links(d: Diocese, to_link: Mapping[str, set[str]]) -> dict[str, Any]:
    after = d.copy()
    for label, refs in to_link.items():
        kind_name, slug = label.split(":", 1)
        record = after.of(records.KINDS[kind_name])[slug]
        record["roster"] = sorted(set(record.get("roster") or []) | refs)
    return records._commit(d, after, tolerate_unreadable=True)


# ── Structure audit ─────────────────────────────────────────────────────────
def audit(diocese: str, *, fetch: bool = False) -> dict[str, Any]:
    """Groups of parish rows that might be one bulletin.

    A group is a set of parishes the diocese or a roster ties together: rows
    sharing a `group` value, or a roster group (canonical parish, family) whose
    entries map to churches of more than one row. For each group spanning more
    than one row, the rows' recorded publication ids decide it:

    - all different -> separate bulletins, settled;
    - any shared    -> one bulletin: merge the rows (validate already fails);
    - any missing   -> unknown: read the bulletins (`probe container`, `probe pdf`)
      and record the publication ids.

    `fetch` also opens each row's website and lists the publication ids it
    embeds: two rows embedding the same id is a lead, not a verdict. Confirm
    by reading the masthead, and check each member's own old channel has gone
    silent, before merging anything.
    """
    d = records.load(diocese)
    parishes, churches = d.of(PARISH), d.of(CHURCH)
    groups: dict[str, set[str]] = {}
    for slug, r in parishes.items():
        if r.get("group"):
            groups.setdefault(f"group: {r['group']}", set()).add(slug)
    aliases = _aliases(diocese)
    idx = _index(d, aliases)
    explicit = _links(d)
    for name in roster_names(diocese):
        for entry in load_roster(diocese, name)["entries"]:
            if not entry.get("group"):
                continue
            ref = f"{name}:{entry.get('id')}"
            labels = explicit.get(ref) or _match(entry, idx, aliases)[1]
            for label in labels:
                kind_name, slug = label.split(":", 1)
                if kind_name == "church":
                    groups.setdefault(f"{name}: {entry['group']}", set()).add(
                        churches[slug].get("parish", ""))

    out_groups = []
    for label, rows in sorted(groups.items()):
        rows.discard("")
        if len(rows) < 2:
            continue
        pubs = {slug: list(parishes[slug].get("publication") or []) for slug in sorted(rows)
                if slug in parishes}
        flat = [p for ps in pubs.values() for p in ps]
        if len(flat) != len(set(flat)):
            verdict = "shared publication: one bulletin, merge the rows"
        elif any(not ps for ps in pubs.values()):
            verdict = "unknown: some rows have no publication id; read their bulletins"
        else:
            verdict = "separate bulletins recorded"
        group: dict[str, Any] = {"group": label, "verdict": verdict, "rows": [
            {"parish": slug, "website": parishes[slug].get("website", ""), "publication": ps}
            for slug, ps in pubs.items()
        ]}
        out_groups.append(group)

    if fetch:
        targets = sorted({row["website"] for g in out_groups for row in g["rows"]
                          if row["website"] and not g["verdict"].startswith("separate")})
        found = {p["url"]: p for p in web.probe_urls(targets)}
        for g in out_groups:
            seen: dict[str, list[str]] = {}
            for row in g["rows"]:
                probe = found.get(row["website"])
                if probe:
                    row["found_on_site"] = probe.get("publications", [])
                    row["site_verdict"] = probe.get("verdict")
                    for pub in row["found_on_site"]:
                        seen.setdefault(pub, []).append(row["parish"])
            shared = {p: rows for p, rows in seen.items() if len(rows) > 1}
            if shared:
                g["lead"] = {p: rows for p, rows in shared.items()}

    unpinned = sorted(slug for slug, r in parishes.items()
                      if not r.get("publication") and r.get("bulletin_provider") != "no_bulletin")
    return {
        "diocese": diocese,
        "groups_spanning_rows": out_groups,
        "needs_a_look": [g["group"] for g in out_groups
                         if not g["verdict"].startswith("separate")],
        "parishes_without_publication_id": unpinned,
    }


# ── Todo ────────────────────────────────────────────────────────────────────
def todo(diocese: str, *, limit: int = 40) -> dict[str, Any]:
    """Everything left in a diocese, cheapest to act on first."""
    d = records.load(diocese)
    p = records.problems(d, rosters=records.roster_ids(diocese))
    now = records.today()
    due, later = [], []
    for kind in records.KINDS.values():
        for slug, r in d.of(kind).items():
            if kind is OPEN or r.get("revisit"):
                item = {"record": f"{kind.dir}/{slug}.md", "revisit": r.get("revisit", ""),
                        "after": r.get("revisit_after") or ""}
                (later if item["after"] and item["after"] > now else due).append(item)
    out: dict[str, Any] = {"diocese": diocese, "today": now}
    out["errors"] = p.errors[:limit]
    out["revisit_now"] = sorted(due, key=lambda i: i["after"])
    out["revisit_later"] = sorted(later, key=lambda i: i["after"])
    if roster_names(diocese):
        cov = coverage(diocese)
        out["coverage"] = [
            {"roster": r["roster"], "fetched": r["fetched"], "accounted_for": r["accounted_for"],
             "unmatched": sum(len(v) for v in r["unmatched"].values()),
             "ambiguous": len(r.get("ambiguous", [])),
             "street_only_matches": len(r.get("street_only_matches", []))}
            for r in cov["rosters"]
        ]
        out["churches_in_no_roster"] = cov.get("churches_in_no_roster", [])
    else:
        out["coverage"] = "no rosters yet: fetch or import the diocese's own list first"
    out["incomplete"] = p.incomplete[:limit]
    out["warnings"] = len(p.warnings)
    out["counts"] = {"errors": len(p.errors), "incomplete": len(p.incomplete),
                     "warnings": len(p.warnings)}
    return out
