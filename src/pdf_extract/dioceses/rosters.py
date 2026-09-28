"""Outside lists of a diocese's churches, saved as `rosters/<name>.json`.

A roster is whatever list you are measuring the diocese against: the diocese's
own parish finder, GCatholic, a cluster/family list, a Mass-times page. None of
them is the diocese: each lags in its own way, and every one of them has listed
buildings closed for years. They are the denominator for `coverage`, never
evidence on their own.

    {
      "name": "gcatholic",
      "title": "GCatholic: churches of the Diocese of Syracuse",
      "url": "https://gcatholic.org/churches/local/syra0",
      "fetched": "2026-09-25",
      "command": "pnpm diocese roster fetch syracuse gcatholic",
      "notes": "",
      "entries": [
        {"id": "18006", "name": "St. John the Evangelist", "group": "", "kind": "Church",
         "line1": "34 S Main St.", "city": "Bainbridge", "state": "NY", "postal_code": "13733",
         "latitude": 42.29, "longitude": -75.48, "website": "", "url": "https://gcatholic.org/..."}
      ]
    }

`id` must be stable across fetches of the same source, because records link to
entries as `<name>:<id>`. `group` is the source's grouping (canonical parish,
family, cluster). Any other keys are kept as they are.
"""

from __future__ import annotations

import html
import json
import re
from collections.abc import Callable, Mapping
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from pdf_extract.dioceses import web
from pdf_extract.dioceses.records import (
    ROSTERS_DIR,
    DioceseError,
    diocese_dir,
    load_meta,
    slugify,
    today,
)

ENTRY_FIELDS = ("id", "name", "group", "kind", "line1", "city", "state", "postal_code",
                "latitude", "longitude", "website", "url")
_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

US_STATES = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "district of columbia": "DC",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID", "illinois": "IL",
    "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA",
    "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI", "minnesota": "MN",
    "mississippi": "MS", "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR",
    "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC", "south dakota": "SD",
    "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA",
    "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
    "puerto rico": "PR",
}


# ── Files ───────────────────────────────────────────────────────────────────
def roster_path(diocese: str, name: str) -> Path:
    if not _NAME_RE.match(name or ""):
        raise DioceseError(f"roster name must be a slug like 'gcatholic', got {name!r}")
    return diocese_dir(diocese) / ROSTERS_DIR / f"{name}.json"


def load_roster(diocese: str, name: str) -> dict[str, Any]:
    path = roster_path(diocese, name)
    if not path.exists():
        raise DioceseError(f"no roster {name!r} in {diocese!r}; fetch or import it first")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        raise DioceseError(f"{path} is not valid JSON: {e}") from None
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise DioceseError(f"{path} must be an object with an 'entries' list")
    return data


def roster_names(diocese: str) -> list[str]:
    folder = diocese_dir(diocese) / ROSTERS_DIR
    return sorted(p.stem for p in folder.glob("*.json")) if folder.exists() else []


def list_rosters(diocese: str) -> dict[str, Any]:
    out = []
    for name in roster_names(diocese):
        data = load_roster(diocese, name)
        out.append({k: data.get(k) for k in ("name", "title", "url", "fetched", "notes")}
                   | {"entries": len(data["entries"])})
    return {"diocese": diocese, "rosters": out}


def get_entry(diocese: str, ref: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """The roster and the entry a `<roster>:<id>` reference points at."""
    name, _, entry_id = ref.partition(":")
    roster = load_roster(diocese, name)
    for entry in roster["entries"]:
        if str(entry.get("id")) == entry_id:
            return roster, entry
    raise DioceseError(f"{ref}: no entry with id {entry_id!r} in rosters/{name}.json")


def _clean_entry(raw: Mapping[str, Any]) -> dict[str, Any]:
    entry = {k: raw.get(k, "") for k in ENTRY_FIELDS}
    entry.update({k: v for k, v in raw.items() if k not in ENTRY_FIELDS})
    for k in ("latitude", "longitude"):
        try:
            entry[k] = float(entry[k]) if entry[k] not in ("", None) else None
        except (TypeError, ValueError):
            entry[k] = None
    for k in ENTRY_FIELDS:
        if k not in ("latitude", "longitude") and entry[k] is None:
            entry[k] = ""
    entry["id"] = str(entry["id"])
    return entry


def save_roster(diocese: str, name: str, entries: list[Mapping[str, Any]], *, title: str,
                url: str, command: str, notes: str = "") -> dict[str, Any]:
    """Write a roster, and say what changed since the last copy of it."""
    path = roster_path(diocese, name)
    clean = [_clean_entry(e) for e in entries]
    ids = [e["id"] for e in clean]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise DioceseError(f"roster ids must be unique; repeated: {dupes[:10]}")
    changes: dict[str, Any] = {}
    if path.exists():
        old = {str(e.get("id")): e for e in load_roster(diocese, name)["entries"]}
        new = {e["id"]: e for e in clean}
        changes = {
            "previously_fetched": load_roster(diocese, name).get("fetched"),
            "added": [f"{i}: {new[i]['name']} ({new[i]['city']})" for i in new.keys() - old.keys()],
            "removed": [f"{i}: {old[i].get('name')} ({old[i].get('city')})"
                        for i in old.keys() - new.keys()],
        }
        if not notes:
            notes = load_roster(diocese, name).get("notes", "")
    data = {"name": name, "title": title, "url": url, "fetched": today(), "command": command,
            "notes": notes, "entries": clean}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"roster": str(path), "entries": len(clean), **({"changes": changes} if changes else {})}


# Common spellings of the entry fields, for rosters built by hand or by an ad-hoc script.
_IMPORT_ALIASES = {
    "zip": "postal_code", "zipcode": "postal_code", "postal": "postal_code",
    "address": "line1", "street": "line1", "address1": "line1", "lat": "latitude",
    "lng": "longitude", "lon": "longitude", "long": "longitude", "homepage": "website",
    "site": "name", "parish": "group", "family": "group", "town": "city", "locale": "city",
}


def import_roster(diocese: str, name: str, source: Path, *, title: str = "", url: str = "",
                  notes: str = "") -> dict[str, Any]:
    """Save a list you built yourself (a JSON list of objects, or a CSV) as a roster.

    For the lists no fetcher covers: a cluster/family list in a PDF, the diocese's
    Mass-times pages, a closed-parishes table. Keys are matched loosely (`zip`,
    `address`, `lat`, `parish`...). Entries without an `id` get one from their
    name and city, which stays stable as long as those do.
    """
    import csv

    if source.suffix.lower() == ".csv":
        with open(source, encoding="utf-8", newline="") as f:
            rows: list[dict[str, Any]] = list(csv.DictReader(f))
    else:
        rows = json.loads(source.read_text(encoding="utf-8"))
        if isinstance(rows, dict):
            rows = rows.get("entries", [])
    entries = []
    for raw in rows:
        entry = {}
        for k, v in raw.items():
            key = _IMPORT_ALIASES.get(str(k).strip().lower(), str(k).strip().lower())
            entry.setdefault(key, v)
        if not entry.get("name"):
            raise DioceseError(f"every entry needs a name; got {raw!r}")
        entry.setdefault("id", slugify(f"{entry['name']} {entry.get('city', '')}"))
        entries.append(entry)
    return save_roster(diocese, name, entries, title=title or name, url=url,
                       command=f"pnpm diocese roster import {diocese} {name} {source}",
                       notes=notes)


# ── Open Location Codes ─────────────────────────────────────────────────────
_OLC_ALPHABET = "23456789CFGHJMPQRVWX"


def decode_plus_code(code: str) -> tuple[float, float] | None:
    """The centre of a full Open Location Code (Plus Code), as (latitude, longitude).

    GCatholic gives one per church, placed on the building, so decoding it
    gives building-precise coordinates without a geocoder. Short codes (fewer
    than 8 characters before the '+') need a reference point and return None.
    """
    code = code.strip().upper()
    if "+" not in code or code.index("+") != 8:
        return None
    clean = code.replace("+", "").rstrip("0")
    if len(clean) < 2 or any(c not in _OLC_ALPHABET for c in clean):
        return None
    lat, lng = -90.0, -180.0
    lat_res = lng_res = 400.0
    for i in range(0, min(len(clean), 10), 2):
        lat_res /= 20.0
        lng_res /= 20.0
        lat += lat_res * _OLC_ALPHABET.index(clean[i])
        if i + 1 < len(clean):
            lng += lng_res * _OLC_ALPHABET.index(clean[i + 1])
    for c in clean[10:]:
        row, col = divmod(_OLC_ALPHABET.index(c), 4)
        lat_res /= 5.0
        lng_res /= 4.0
        lat += row * lat_res
        lng += col * lng_res
    return round(lat + lat_res / 2, 7), round(lng + lng_res / 2, 7)


# ── GCatholic ───────────────────────────────────────────────────────────────
GCATHOLIC = "https://gcatholic.org"


def parse_gcatholic_index(page: str) -> list[dict[str, str]]:
    """Rows of a gcatholic.org/churches/local/<key> page: id, city, name, type, parish.

    GCatholic lists Eastern Catholic churches in the territory too (class
    `che`, with their rite); those belong to an eparchy, not this diocese, and
    come back with `rite` set so they are easy to exclude as other-jurisdiction.
    """
    out = []
    for row in re.findall(r"<tr id=\"L\d+\">(.*?)</tr>", page, flags=re.S):
        link = re.search(r'href="\.\./([a-z0-9-]+)/(\d+)"\s+class="(ch[a-z])"[^>]*>(.*?)</a>',
                         row, flags=re.S)
        if not link:
            continue
        notes = [web.html_text(n).strip() for n in
                 re.findall(r'class="znote"[^>]*>(.*?)</span>', row, flags=re.S)]
        title = re.search(r'title="([^"]+)"', row)
        rite = re.search(r'class="zrite">([^<]+)</a>', row)
        entry = {
            "id": link.group(2), "path": f"{link.group(1)}/{link.group(2)}",
            "name": web.html_text(link.group(4)), "index_city": notes[0] if notes else "",
            "group": next((n for n in notes[1:] if not n.startswith("(")), ""),
            "kind": html.unescape(title.group(1)).split(" of ")[0] if title else "",
        }
        qualifier = next((n.strip("() ") for n in notes[1:] if n.startswith("(")), "")
        if qualifier:
            entry["qualifier"] = qualifier
        if link.group(3) == "che" or rite:
            entry["rite"] = rite.group(1) if rite else "Eastern"
        out.append(entry)
    return out


_GC_LABELS = ("Jurisdiction", "Type", "Rite", "History", "Location", "Address", "Country",
              "Telephone", "Website", "Email", "GCatholic Church ID")
_GC_LABEL_RE = re.compile(r"(" + "|".join(_GC_LABELS) + r"|Show Map|Churches Nearby):?")


def parse_gcatholic_detail(page: str) -> dict[str, Any]:
    """Address, Plus Code (decoded), type, phone and website from a church's own page."""
    text = " ".join(web.html_text(page).split())
    fields: dict[str, str] = {}
    marks = list(_GC_LABEL_RE.finditer(text))
    for mark, nxt in zip(marks, [*marks[1:], None]):
        label = mark.group(1)
        if label in _GC_LABELS and label not in fields:
            fields[label] = text[mark.end():nxt.start() if nxt else len(text)].strip(" ,")
    rec: dict[str, Any] = {}
    if fields.get("Address"):
        rec["address"] = fields["Address"]
        rec.update(parse_address(fields["Address"]))
    code = re.match(r"[0-9A-Z]{4,8}\+[0-9A-Z]{2,3}", fields.get("Location", ""))
    if code:
        rec["plus_code"] = code.group(0)
        coords = decode_plus_code(code.group(0))
        if coords:
            rec["latitude"], rec["longitude"] = coords
    for label, key in (("Type", "type"), ("Telephone", "phone"), ("History", "history")):
        if fields.get(label):
            rec[key] = fields[label]
    links = [h for h in re.findall(r'href="(https?://[^"]+)"', page)
             if not re.search(r"gcatholic|jsdelivr|googleapis|facebook|x\.com|twitter|youtube"
                              r"|instagram|google\.com/maps", h)]
    if links:
        rec["website"] = links[0]
    return rec


def parse_address(raw: str) -> dict[str, str]:
    """'34 S Main St., Bainbridge, New York 13733-1215' -> line1, city, state, postal_code."""
    out = {"line1": "", "city": "", "state": "", "postal_code": ""}
    # GCatholic sometimes ends an address with an invisible direction mark (U+200E).
    raw = re.sub(r"[\u200b-\u200f\u202a-\u202e\u2066-\u2069]", "", raw or "")
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if parts and parts[-1].upper() in ("USA", "UNITED STATES"):
        parts.pop()
    if parts:
        m = re.match(r"^(.*?)\s*(\d{5})(?:-\d{4})?$", parts[-1])
        if m:
            state = m.group(1).strip()
            out["state"] = US_STATES.get(state.lower(), state.upper() if len(state) == 2 else state)
            out["postal_code"] = m.group(2)
            parts.pop()
        elif (m := re.match(r"^(.*?)\s*\d{1,4}$", parts[-1])) and m.group(1).lower() in US_STATES:
            # A mistyped ZIP ("Stamford, New York 1890"): keep the state, drop the number.
            out["state"] = US_STATES[m.group(1).lower()]
            parts.pop()
    if parts:
        out["city"] = parts.pop()
    out["line1"] = ", ".join(parts)
    return out


def fetch_gcatholic(key: str, *, limit: int | None = None, workers: int = 6
                    ) -> tuple[list[dict[str, Any]], str]:
    index_url = f"{GCATHOLIC}/churches/local/{key}"
    resp = web.fetch(index_url)
    if not resp.ok:
        raise DioceseError(f"{index_url}: {resp.error or resp.status}")
    rows = parse_gcatholic_index(resp.text())
    if not rows:
        raise DioceseError(f"{index_url}: no churches found; is {key!r} the GCatholic key "
                           "(as in gcatholic.org/dioceses/diocese/<key>.htm)?")
    rows = rows[:limit] if limit else rows

    def enrich(row: dict[str, str]) -> dict[str, Any]:
        url = f"{GCATHOLIC}/churches/{row['path']}"
        detail = web.fetch(url)
        entry: dict[str, Any] = {
            "id": row["id"], "name": row["name"], "group": row["group"], "kind": row["kind"],
            "city": row["index_city"], "url": url,
            **{k: row[k] for k in ("qualifier", "rite") if row.get(k)},
        }
        if detail.ok:
            info = parse_gcatholic_detail(detail.text())
            entry.update({k: v for k, v in info.items() if v not in ("", None)})
        else:
            entry["fetch_error"] = detail.error
        return entry

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(enrich, rows)), index_url


# ── WP Store Locator parish finders ─────────────────────────────────────────
def fetch_wpsl(page_url: str, *, radius: int = 300, max_results: int = 2000
               ) -> tuple[list[dict[str, Any]], str]:
    """Every location of a parish finder built on the WordPress "WP Store Locator" plugin.

    The plugin answers an unauthenticated `store_search` request with every
    location at once: name, address, coordinates, homepage. Location names
    often carry the structure, e.g. "St. Mary of Lourdes [2008] - Our Lady of
    Lourdes Worship Site" (canonical parish, year, worship site), which becomes
    `group` and `name`.
    """
    page = web.fetch(page_url)
    if not page.ok:
        raise DioceseError(f"{page_url}: {page.error or page.status}")
    body = page.text()
    ajax = re.search(r'"ajaxurl":"(https?:[^"]+admin-ajax\.php)"', body)
    if not ajax:
        raise DioceseError(f"{page_url}: no WP Store Locator 'ajaxurl'; not a wpsl page?")
    start = re.search(r'"startLatlng":"(-?[\d.]+),(-?[\d.]+)"', body)
    lat, lng = start.groups() if start else ("0", "0")
    query = urlencode({"action": "store_search", "lat": lat, "lng": lng, "autoload": "1",
                       "max_results": max_results, "search_radius": radius})
    api = f"{ajax.group(1).replace(chr(92) + '/', '/')}?{query}"
    resp = web.fetch(api)
    try:
        raw = json.loads(resp.body or b"[]")
    except ValueError:
        raise DioceseError(f"{api}: did not return JSON ({resp.error or resp.status})") from None
    entries = []
    for x in raw:
        name = " ".join(html.unescape(x.get("store") or "").split())
        m = re.match(r"^(.*?)\s+[-–—]\s+(.*)$", name)
        group, site = (m.group(1), m.group(2)) if m else ("", name)
        year = re.search(r"\[(\d{4})\]", name)
        group = re.sub(r"\s*\[[^\]]*\]", "", group).strip()
        site = re.sub(r"\s*\[[^\]]*\]", "", site).strip()
        kind = ""
        for suffix in ("worship site", "oratory", "chapel", "mission"):
            if site.lower().endswith(suffix):
                kind = suffix
                site = site[: -len(suffix)].strip(" -–") or site
                break
        entries.append({
            "id": str(x.get("id")), "name": site or group, "group": group, "kind": kind,
            "year": year.group(1) if year else "",
            "line1": " ".join(html.unescape(x.get("address") or "").split()),
            "line2": " ".join(html.unescape(x.get("address2") or "").split()),
            "city": x.get("city") or "", "state": x.get("state") or "",
            "postal_code": x.get("zip") or "", "latitude": x.get("lat"),
            "longitude": x.get("lng"), "website": x.get("url") or "",
            "phone": x.get("phone") or "", "full_name": name,
        })
    return entries, page_url


FETCHERS: dict[str, Callable[..., tuple[list[dict[str, Any]], str]]] = {
    "gcatholic": fetch_gcatholic, "wpsl": fetch_wpsl,
}


def fetch_roster(diocese: str, source: str, target: str = "", *, name: str = "",
                 limit: int | None = None) -> dict[str, Any]:
    """Fetch a roster with one of the built-in fetchers and save it."""
    meta = load_meta(diocese)
    if source == "gcatholic":
        key = target or meta.get("gcatholic") or ""
        if not key:
            raise DioceseError("give the GCatholic key (e.g. syra0), or set gcatholic: in "
                               "diocese.md")
        entries, url = fetch_gcatholic(key, limit=limit)
        title = f"GCatholic: churches of the {meta.get('name', diocese)}"
        notes = ("group is GCatholic's canonical parish when it differs from the church; "
                 "coordinates are decoded from GCatholic's Plus Code (gcatholic-plus-code).")
        command = f"pnpm diocese roster fetch {diocese} gcatholic {key}"
    elif source == "wpsl":
        if not target:
            raise DioceseError("give the URL of the diocese's parish-finder page")
        entries, url = fetch_wpsl(target)
        title = f"Parish finder: {meta.get('name', diocese)}"
        notes = "group is the canonical parish from the location name."
        command = f"pnpm diocese roster fetch {diocese} wpsl {target}"
    else:
        raise DioceseError(f"unknown roster source {source!r}; use {', '.join(FETCHERS)}, or "
                           "`roster import` a list you built yourself")
    return save_roster(diocese, name or source, entries, title=title, url=url,
                       command=command, notes=notes)
