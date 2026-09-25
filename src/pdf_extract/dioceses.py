"""Staging area for dioceses whose parishes are still being explored.

Each diocese gets a folder under `data/dioceses/<diocese>/`:

- `diocese.json`: name, state, website and where its parish directory lives
- `parishes.json`: parishes found so far, the columns of `data/parishes.csv`
  plus an `explanation` and `sources`
- `churches.json`: their churches, the columns of `data/churches.csv` plus
  `explanation` and `sources`
- `not-parishes.md` / `not-churches.md`: places that looked like a parish or a
  church but should not be added, each with the reason why

Nothing here feeds the pipeline. `export` writes a diocese out in the live CSV
format once it is ready to be promoted. Every write goes through the same
checks as `validate`, and is refused only if it would add a new error, so one
stale problem elsewhere in a diocese never blocks unrelated edits.

The live CSVs take part in the cross-checks: the database gives parish slugs,
church slugs and parish websites UNIQUE constraints across every diocese, so a
collision here would fail `db create` the day the diocese is promoted.
"""

from __future__ import annotations

import csv
import json
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.storage import CHURCHES_CSV_PATH, DIOCESES_DIR, PARISHES_CSV_PATH

META_FILE = "diocese.json"

# Every value `data/parishes.csv` uses. `fetch` only knows the first four;
# the other two are recorded so a parish can say why it is not fetched.
KNOWN_BULLETIN_PROVIDERS = frozenset(
    {"parishes_online", "ecatholic", "discover_mass", "other", "google_drive", "no_bulletin"}
)
# Providers whose bulletins are looked up by account id, not the homepage.
PROVIDERS_NEEDING_ID = frozenset({"parishes_online", "discover_mass"})

LIVE = "live"  # the `diocese` search reports for rows in data/parishes.csv and churches.csv

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_STATE_RE = re.compile(r"^[A-Z]{2}$")
_POSTAL_RE = re.compile(r"^\d{5}(?:-\d{4})?$")
_URL_RE = re.compile(r"^https?://\S+$")


class DioceseError(ValueError):
    """A diocese command was given bad input; the message says what to fix."""


# ── Record kinds ────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class _Kind:
    name: str
    file: str
    fields: tuple[str, ...]
    text_fields: tuple[str, ...] = ()
    bool_fields: tuple[str, ...] = ()
    float_fields: tuple[str, ...] = ()
    title: str = ""  # heading for a markdown file

    @property
    def is_markdown(self) -> bool:
        return self.file.endswith(".md")


PARISH = _Kind(
    name="parish",
    file="parishes.json",
    fields=(
        "slug", "name", "website", "bulletin_provider", "provider_id",
        "explanation", "sources",
    ),
    text_fields=("slug", "name", "website", "bulletin_provider", "provider_id", "explanation"),
)
CHURCH = _Kind(
    name="church",
    file="churches.json",
    fields=(
        "parish_id", "slug", "name", "line1", "line2", "city", "state", "postal_code",
        "name_verified", "address_verified", "latitude", "longitude",
        "explanation", "sources",
    ),
    text_fields=(
        "parish_id", "slug", "name", "line1", "line2", "city", "state", "postal_code",
        "explanation",
    ),
    bool_fields=("name_verified", "address_verified"),
    float_fields=("latitude", "longitude"),
)
_EXCLUSION_FIELDS = ("slug", "name", "website", "address", "parish", "sources", "added", "explanation")
_EXCLUSION_TEXT = ("slug", "name", "website", "address", "parish", "added", "explanation")
NOT_PARISH = _Kind(
    name="not-parish",
    file="not-parishes.md",
    fields=_EXCLUSION_FIELDS,
    text_fields=_EXCLUSION_TEXT,
    title="Not parishes",
)
NOT_CHURCH = _Kind(
    name="not-church",
    file="not-churches.md",
    fields=_EXCLUSION_FIELDS,
    text_fields=_EXCLUSION_TEXT,
    title="Not churches",
)
KINDS: dict[str, _Kind] = {k.name: k for k in (PARISH, CHURCH, NOT_PARISH, NOT_CHURCH)}

# The kind an exclusion stands in for, and back: a slug may not be in both.
_EXCLUDES = {NOT_PARISH.name: PARISH.name, NOT_CHURCH.name: CHURCH.name}

# Column order of the live CSVs, for `export`.
_PARISH_CSV_FIELDS = ["slug", "name", "website", "bulletin_provider", "provider_id"]
_CHURCH_CSV_FIELDS = [
    "parish_id", "slug", "name", "line1", "line2", "city", "state", "postal_code",
    "name_verified", "address_verified", "latitude", "longitude",
]


# ── Helpers ─────────────────────────────────────────────────────────────────
def slugify(name: str) -> str:
    """`St. Mary's Church` -> `st-marys-church`."""
    text = re.sub(r"['’]", "", name.lower())
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


_ABBREVIATIONS = {"st": "saint", "sts": "saints", "ss": "saints", "mt": "mount"}


def normalize(text: str) -> str:
    """Lowercase, drop punctuation and spell out St./Sts./Mt., for matching names."""
    text = re.sub(r"['’]", "", text.lower())
    tokens = re.sub(r"[^a-z0-9]+", " ", text).split()
    return " ".join(_ABBREVIATIONS.get(t, t) for t in tokens)


def _coerce(kind: _Kind, field: str, value: Any) -> Any:
    """Turn a CLI string (or a Python value) into the type stored for `field`."""
    if field == "sources":
        if value is None:
            return []
        if isinstance(value, str):
            value = [value]
        return [str(s).strip() for s in value if str(s).strip()]
    if field in kind.bool_fields:
        if isinstance(value, bool):
            return value
        text = str(value or "").strip().lower()
        if text in ("true", "yes", "1"):
            return True
        if text in ("", "false", "no", "0"):
            return False
        raise DioceseError(f"{field} must be true or false, got {value!r}")
    if field in kind.float_fields:
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            raise DioceseError(f"{field} must be a number, got {value!r}") from None
    return "" if value is None else str(value).strip()


def _blank(kind: _Kind) -> dict[str, Any]:
    return {f: _coerce(kind, f, None) for f in kind.fields}


def _sort_key(kind: _Kind):
    if kind is CHURCH:
        return lambda r: (r["parish_id"], r["slug"])
    return lambda r: r["slug"]


# ── Files ───────────────────────────────────────────────────────────────────
def _diocese_dir(diocese: str, *, must_exist: bool = True) -> Path:
    if not _SLUG_RE.match(diocese or ""):
        raise DioceseError(f"diocese must be a slug like 'syracuse', got {diocese!r}")
    path = DIOCESES_DIR / diocese
    if must_exist and not (path / META_FILE).exists():
        known = ", ".join(_diocese_slugs()) or "none yet"
        raise DioceseError(
            f"no diocese {diocese!r} (known: {known}); create it with `diocese init`"
        )
    return path


def _diocese_slugs() -> list[str]:
    if not DIOCESES_DIR.exists():
        return []
    return sorted(p.parent.name for p in DIOCESES_DIR.glob(f"*/{META_FILE}"))


def _write_text(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _write_json(path: Path, data: Any) -> None:
    _write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def _load_meta(diocese: str) -> dict[str, Any]:
    return json.loads((_diocese_dir(diocese) / META_FILE).read_text(encoding="utf-8"))


def _load(diocese: str, kind: _Kind) -> list[dict[str, Any]]:
    path = _diocese_dir(diocese) / kind.file
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    if kind.is_markdown:
        return _parse_markdown(text)[1]
    try:
        rows = json.loads(text)
    except json.JSONDecodeError as e:
        raise DioceseError(f"{path} is not valid JSON: {e}") from None
    if not isinstance(rows, list):
        raise DioceseError(f"{path} must hold a JSON array")
    return rows


def _save(diocese: str, kind: _Kind, rows: list[dict[str, Any]]) -> None:
    path = _diocese_dir(diocese) / kind.file
    if kind.is_markdown:
        preamble = None
        if path.exists():
            preamble = _parse_markdown(path.read_text(encoding="utf-8"))[0]
        _write_text(path, _render_markdown(kind, diocese, rows, preamble))
    else:
        _write_json(path, sorted(rows, key=_sort_key(kind)))


def _read_live_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [dict(row) for row in csv.DictReader(f)]


# ── Markdown exclusion files ────────────────────────────────────────────────
# One `## Name` section per entry: `- **Label:** value` lines, then the
# explanation as free text. Sources may repeat. Hand edits are fine as long
# as that shape holds; anything else in the field block becomes explanation.
_MD_LABELS = {
    "slug": "Slug", "website": "Website", "address": "Address", "parish": "Parish",
    "sources": "Source", "added": "Added",
}
_MD_FIELDS = {label.lower(): field for field, label in _MD_LABELS.items()}
_MD_FIELD_RE = re.compile(r"^- \*\*([A-Za-z ]+):\*\*\s*(.*?)\s*$")


def _parse_markdown(text: str) -> tuple[str, list[dict[str, Any]]]:
    """Split an exclusion file into its preamble and its entries."""
    sections = re.split(r"^## ", text, flags=re.MULTILINE)
    preamble, entries = sections[0].strip(), []
    for section in sections[1:]:
        heading, _, body = section.partition("\n")
        entry = _blank(NOT_PARISH)
        entry["name"] = heading.strip()
        lines = body.strip("\n").splitlines()
        i = 0
        while i < len(lines):
            m = _MD_FIELD_RE.match(lines[i])
            if not m or m.group(1).strip().lower() not in _MD_FIELDS:
                break
            field = _MD_FIELDS[m.group(1).strip().lower()]
            if field == "sources":
                entry["sources"].append(m.group(2))
            else:
                entry[field] = m.group(2)
            i += 1
        entry["explanation"] = "\n".join(lines[i:]).strip()
        entries.append(entry)
    return preamble, entries


def _render_markdown(
    kind: _Kind, diocese: str, entries: list[dict[str, Any]], preamble: str | None,
) -> str:
    if not preamble:
        target = _EXCLUDES[kind.name]
        preamble = (
            f"# {kind.title}: {_load_meta(diocese).get('name') or diocese}\n\n"
            f"Places found while exploring this diocese that looked like a {target} but\n"
            f"should not be added, and why. Check here before adding a {target}.\n"
            f"Managed with `pnpm diocese {kind.name} ...`; hand edits are fine if each entry\n"
            "keeps its `## Name` heading and `- **Field:** value` lines."
        )
    parts = [preamble.strip()]
    for e in entries:
        lines = [f"## {e['name']}"]
        for field, label in _MD_LABELS.items():
            values = e[field] if field == "sources" else [e[field]]
            lines += [f"- **{label}:** {v}" for v in values if v]
        if e["explanation"]:
            lines += ["", e["explanation"]]
        parts.append("\n".join(lines))
    return "\n\n".join(parts) + "\n"


# ── Checks ──────────────────────────────────────────────────────────────────
@dataclass
class _Problems:
    errors: list[str]
    warnings: list[str]


def _other_owners(diocese: str) -> dict[str, dict[str, str]]:
    """Slugs and websites taken outside `diocese`, mapped to where they live."""
    owners: dict[str, dict[str, str]] = {"parish": {}, "church": {}, "website": {}}
    for row in _read_live_csv(PARISHES_CSV_PATH):
        owners["parish"][row.get("slug", "")] = "data/parishes.csv"
        owners["website"][_url_key(row.get("website", ""))] = "data/parishes.csv"
    for row in _read_live_csv(CHURCHES_CSV_PATH):
        owners["church"][row.get("slug", "")] = "data/churches.csv"
    for other in _diocese_slugs():
        if other == diocese:
            continue
        where = f"diocese {other!r}"
        for row in _load(other, PARISH):
            owners["parish"].setdefault(row.get("slug", ""), where)
            owners["website"].setdefault(_url_key(row.get("website", "")), where)
        for row in _load(other, CHURCH):
            owners["church"].setdefault(row.get("slug", ""), where)
    for table in owners.values():
        table.pop("", None)
    return owners


def _url_key(url: str) -> str:
    """Compare websites without scheme, `www.` or a trailing slash."""
    url = re.sub(r"^https?://(www\.)?", "", (url or "").strip().lower())
    return url.rstrip("/")


def _check_record(kind: _Kind, row: Mapping[str, Any], p: _Problems) -> None:
    label = f"{kind.name} {row.get('slug') or row.get('name') or '?'!r}"
    for field in row:
        if field not in kind.fields:
            p.warnings.append(f"{label}: unknown field {field!r}")
    slug = row.get("slug", "")
    if not _SLUG_RE.match(slug or ""):
        p.errors.append(f"{label}: slug must be lowercase words joined by '-', got {slug!r}")
    if not row.get("name"):
        p.errors.append(f"{label}: name is required")
    if not (row.get("explanation") or "").strip():
        p.errors.append(f"{label}: explanation is required (say how you know, or why it is excluded)")
    sources = row.get("sources") or []
    if not isinstance(sources, list):
        p.errors.append(f"{label}: sources must be a list of URLs")
    else:
        for s in sources:
            if not _URL_RE.match(str(s)):
                p.warnings.append(f"{label}: source {s!r} is not a URL")
    website = row.get("website") or ""
    if website and not _URL_RE.match(website):
        p.errors.append(f"{label}: website must start with http:// or https://, got {website!r}")

    if kind is PARISH:
        if not website:
            p.errors.append(f"{label}: website is required")
        if not sources:
            p.warnings.append(f"{label}: no sources recorded")
        provider = row.get("bulletin_provider") or ""
        if provider and provider not in KNOWN_BULLETIN_PROVIDERS:
            known = ", ".join(sorted(KNOWN_BULLETIN_PROVIDERS))
            p.errors.append(f"{label}: bulletin_provider {provider!r} is not one of {known}")
        if not provider:
            p.warnings.append(f"{label}: bulletin_provider not identified yet")
        if provider in PROVIDERS_NEEDING_ID and not row.get("provider_id"):
            p.warnings.append(f"{label}: {provider} needs a provider_id to be fetched")
    elif kind is CHURCH:
        if not sources:
            p.warnings.append(f"{label}: no sources recorded")
        for field in ("line1", "city", "state", "postal_code"):
            if not row.get(field):
                p.warnings.append(f"{label}: {field} is missing")
        state = row.get("state") or ""
        if state and not _STATE_RE.match(state):
            p.errors.append(f"{label}: state must be a two-letter code like 'NY', got {state!r}")
        postal = row.get("postal_code") or ""
        if postal and not _POSTAL_RE.match(postal):
            p.errors.append(f"{label}: postal_code must look like 13202, got {postal!r}")
        for field in CHURCH.bool_fields:
            if not isinstance(row.get(field, False), bool):
                p.errors.append(f"{label}: {field} must be true or false")
        lat, lng = row.get("latitude"), row.get("longitude")
        if (lat is None) != (lng is None):
            p.errors.append(f"{label}: set latitude and longitude together")
        if lat is not None and not (isinstance(lat, int | float) and -90 <= lat <= 90):
            p.errors.append(f"{label}: latitude must be a number between -90 and 90")
        if lng is not None and not (isinstance(lng, int | float) and -180 <= lng <= 180):
            p.errors.append(f"{label}: longitude must be a number between -180 and 180")


def _problems(diocese: str, data: Mapping[str, list[dict[str, Any]]]) -> _Problems:
    """Every error and warning for one diocese, given its (possibly unsaved) records."""
    p = _Problems([], [])
    owners = _other_owners(diocese)

    for kind in KINDS.values():
        seen: set[str] = set()
        for row in data[kind.name]:
            _check_record(kind, row, p)
            slug = row.get("slug", "")
            if slug in seen:
                p.errors.append(f"{kind.name} {slug!r}: slug is used twice in {kind.file}")
            seen.add(slug)

    parish_slugs = {r["slug"] for r in data[PARISH.name]}
    for kind in (PARISH, CHURCH):
        for row in data[kind.name]:
            where = owners[kind.name].get(row.get("slug", ""))
            if where:
                p.errors.append(
                    f"{kind.name} {row['slug']!r}: slug already used in {where}; "
                    "slugs must be unique across all dioceses"
                )
    websites: dict[str, str] = {}
    for row in data[PARISH.name]:
        key = _url_key(row.get("website", ""))
        if not key:
            continue
        where = owners["website"].get(key) or websites.get(key)
        if where:
            p.errors.append(f"parish {row['slug']!r}: website {row['website']!r} already used by {where}")
        websites[key] = f"parish {row['slug']!r}"

    churches_by_parish: dict[str, int] = {}
    for row in data[CHURCH.name]:
        parish = row.get("parish_id", "")
        churches_by_parish[parish] = churches_by_parish.get(parish, 0) + 1
        if parish not in parish_slugs:
            p.errors.append(
                f"church {row.get('slug')!r}: parish_id {parish!r} is not in parishes.json"
            )
    for slug in sorted(parish_slugs - set(churches_by_parish)):
        p.warnings.append(f"parish {slug!r}: no churches recorded")

    for excl, target in _EXCLUDES.items():
        kept = {r["slug"] for r in data[target]}
        for row in data[excl]:
            if row.get("slug") in kept:
                p.errors.append(
                    f"{excl} {row['slug']!r}: also listed in {KINDS[target].file}; keep one"
                )
    return p


def _load_all(diocese: str) -> dict[str, list[dict[str, Any]]]:
    return {name: _load(diocese, kind) for name, kind in KINDS.items()}


def _commit(
    diocese: str, before: dict[str, list[dict[str, Any]]],
    after: dict[str, list[dict[str, Any]]], changed: Iterable[str],
) -> list[str]:
    """Save `after` unless it adds errors; return the warnings it adds."""
    old, new = _problems(diocese, before), _problems(diocese, after)
    added_errors = [e for e in new.errors if e not in old.errors]
    if added_errors:
        raise DioceseError("refused, nothing was written:\n  " + "\n  ".join(added_errors))
    for name in changed:
        _save(diocese, KINDS[name], after[name])
    return [w for w in new.warnings if w not in old.warnings]


def _find(rows: list[dict[str, Any]], kind: _Kind, slug: str, diocese: str) -> int:
    for i, row in enumerate(rows):
        if row.get("slug") == slug:
            return i
    raise DioceseError(f"no {kind.name} {slug!r} in diocese {diocese!r}")


def _exclusion_hint(diocese: str, kind: _Kind, row: Mapping[str, Any]) -> list[str]:
    """Warn when a new record shares a name with something already excluded."""
    excl = next((k for k, t in _EXCLUDES.items() if t == kind.name), None)
    if not excl:
        return []
    name = normalize(row.get("name", ""))
    return [
        f"{kind.name} {row['slug']!r}: same name as {excl} {e['slug']!r} "
        f"in {KINDS[excl].file}; check it is not the place excluded there"
        for e in _load(diocese, KINDS[excl])
        if name and normalize(e["name"]) == name
    ]


# ── Public operations ───────────────────────────────────────────────────────
def list_dioceses() -> dict[str, Any]:
    dioceses = []
    for slug in _diocese_slugs():
        meta = _load_meta(slug)
        data = _load_all(slug)
        dioceses.append({
            "slug": slug,
            "name": meta.get("name", ""),
            "state": meta.get("state", ""),
            **{f"{name.replace('-', '_')}_count": len(rows) for name, rows in data.items()},
        })
    return {"dioceses_dir": str(DIOCESES_DIR), "dioceses": dioceses}


def init_diocese(
    diocese: str, *, name: str, state: str = "", website: str = "",
    parish_directory_url: str = "", notes: str = "",
) -> dict[str, Any]:
    if diocese == LIVE:
        raise DioceseError(f"{LIVE!r} is reserved: search uses it for the live CSVs")
    path = _diocese_dir(diocese, must_exist=False)
    if (path / META_FILE).exists():
        raise DioceseError(f"diocese {diocese!r} already exists at {path}")
    if not name.strip():
        raise DioceseError("name is required, e.g. 'Roman Catholic Diocese of Syracuse'")
    if state and not _STATE_RE.match(state):
        raise DioceseError(f"state must be a two-letter code like 'NY', got {state!r}")
    path.mkdir(parents=True, exist_ok=True)
    meta = {
        "slug": diocese, "name": name.strip(), "state": state, "website": website,
        "parish_directory_url": parish_directory_url, "notes": notes,
    }
    _write_json(path / META_FILE, meta)
    for kind in KINDS.values():
        _save(diocese, kind, [])
    return {"created": str(path), "diocese": meta}


def edit_diocese(diocese: str, changes: Mapping[str, Any]) -> dict[str, Any]:
    meta = _load_meta(diocese)
    for field, value in changes.items():
        if value is None:
            continue
        if field not in ("name", "state", "website", "parish_directory_url", "notes"):
            raise DioceseError(f"diocese.json has no field {field!r}")
        meta[field] = str(value).strip()
    if not meta.get("name"):
        raise DioceseError("name cannot be empty")
    if meta.get("state") and not _STATE_RE.match(meta["state"]):
        raise DioceseError(f"state must be a two-letter code like 'NY', got {meta['state']!r}")
    _write_json(_diocese_dir(diocese) / META_FILE, meta)
    return {"diocese": meta}


def show_diocese(diocese: str) -> dict[str, Any]:
    """The diocese at a glance: parishes with their churches, and what was excluded."""
    data = _load_all(diocese)
    churches: dict[str, list[dict[str, str]]] = {}
    for c in data[CHURCH.name]:
        churches.setdefault(c["parish_id"], []).append(
            {"slug": c["slug"], "name": c["name"], "city": c.get("city", "")}
        )
    return {
        "diocese": _load_meta(diocese),
        "parishes": [
            {
                "slug": p["slug"], "name": p["name"], "website": p.get("website", ""),
                "bulletin_provider": p.get("bulletin_provider", ""),
                "churches": churches.get(p["slug"], []),
            }
            for p in data[PARISH.name]
        ],
        "not_parishes": [{"slug": e["slug"], "name": e["name"]} for e in data[NOT_PARISH.name]],
        "not_churches": [{"slug": e["slug"], "name": e["name"]} for e in data[NOT_CHURCH.name]],
    }


def get_record(diocese: str, kind_name: str, slug: str) -> dict[str, Any]:
    kind = KINDS[kind_name]
    rows = _load(diocese, kind)
    record = rows[_find(rows, kind, slug, diocese)]
    result: dict[str, Any] = {kind.name: record}
    if kind is PARISH:
        result["churches"] = [c for c in _load(diocese, CHURCH) if c["parish_id"] == slug]
    return result


def list_records(diocese: str, kind_name: str, parish: str | None = None) -> dict[str, Any]:
    rows = _load(diocese, KINDS[kind_name])
    if parish is not None:
        rows = [r for r in rows if r.get("parish_id", r.get("parish")) == parish]
    return {"diocese": diocese, "kind": kind_name, "count": len(rows), "records": rows}


def add_record(diocese: str, kind_name: str, fields: Mapping[str, Any]) -> dict[str, Any]:
    kind = KINDS[kind_name]
    _diocese_dir(diocese)
    record = _blank(kind)
    for field, value in fields.items():
        if value is None:
            continue
        if field not in kind.fields:
            raise DioceseError(f"{kind.name} has no field {field!r}")
        record[field] = _coerce(kind, field, value)
    if not record["slug"] and record["name"]:
        record["slug"] = slugify(record["name"])
    if "added" in record and not record["added"]:
        record["added"] = date.today().isoformat()

    before = _load_all(diocese)
    after = {**before, kind.name: [*before[kind.name], record]}
    warnings = _commit(diocese, before, after, [kind.name])
    warnings += _exclusion_hint(diocese, kind, record)
    return {"added": kind.name, "diocese": diocese, kind.name: record, "warnings": warnings}


def edit_record(
    diocese: str, kind_name: str, slug: str, changes: Mapping[str, Any], *,
    new_slug: str | None = None, append_explanation: str | None = None,
    add_sources: Iterable[str] = (), clear_sources: bool = False,
) -> dict[str, Any]:
    """Change the given fields of one record; fields passed as None stay as they are."""
    kind = KINDS[kind_name]
    before = _load_all(diocese)
    rows = [dict(r) for r in before[kind.name]]
    record = rows[_find(rows, kind, slug, diocese)]

    for field, value in changes.items():
        if value is None:
            continue
        if field not in kind.fields or field == "slug":
            raise DioceseError(f"{kind.name} has no editable field {field!r}")
        record[field] = _coerce(kind, field, value)
    if append_explanation:
        record["explanation"] = "\n\n".join(
            filter(None, [record.get("explanation", "").strip(), append_explanation.strip()])
        )
    if clear_sources:
        record["sources"] = []
    for source in _coerce(kind, "sources", list(add_sources)):
        if source not in record.setdefault("sources", []):
            record["sources"].append(source)

    after = {**before, kind.name: rows}
    changed = [kind.name]
    if new_slug and new_slug != slug:
        record["slug"] = new_slug
        if kind is PARISH:  # churches follow their parish
            after[CHURCH.name] = [
                {**c, "parish_id": new_slug} if c["parish_id"] == slug else c
                for c in before[CHURCH.name]
            ]
            changed.append(CHURCH.name)

    warnings = _commit(diocese, before, after, changed)
    return {"edited": kind.name, "diocese": diocese, kind.name: record, "warnings": warnings}


def remove_record(
    diocese: str, kind_name: str, slug: str, *, cascade: bool = False,
) -> dict[str, Any]:
    kind = KINDS[kind_name]
    before = _load_all(diocese)
    rows = list(before[kind.name])
    removed = rows.pop(_find(rows, kind, slug, diocese))
    after = {**before, kind.name: rows}
    changed = [kind.name]
    removed_churches: list[str] = []
    if kind is PARISH:
        removed_churches = [c["slug"] for c in before[CHURCH.name] if c["parish_id"] == slug]
        if removed_churches and not cascade:
            raise DioceseError(
                f"parish {slug!r} still has churches {removed_churches}; move them with "
                "`church edit --parish`, or pass --cascade to remove them too"
            )
        after[CHURCH.name] = [c for c in before[CHURCH.name] if c["parish_id"] != slug]
        changed.append(CHURCH.name)
    _commit(diocese, before, after, changed)
    return {
        "removed": kind.name, "diocese": diocese, kind.name: removed,
        "removed_churches": removed_churches,
    }


def _summary(kind: _Kind, row: Mapping[str, Any]) -> str:
    if kind is PARISH:
        return row.get("website", "")
    if kind is CHURCH:
        address = ", ".join(filter(None, [row.get("line1"), row.get("city"), row.get("state")]))
        return f"{address} (parish {row.get('parish_id', '')})"
    explanation = " ".join((row.get("explanation") or "").split())
    return explanation[:160] + ("…" if len(explanation) > 160 else "")


def search(
    query: str, *, diocese: str | None = None, kinds: Iterable[str] | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    """Find records whose text contains every word of `query`.

    Covers every diocese and the live CSVs (reported as diocese `live`), so it
    doubles as a duplicate check before adding a parish or church. Matching
    ignores case and punctuation and treats St./Saint, Sts./Ss./Saints alike.
    """
    words = normalize(query).split()
    if not words:
        raise DioceseError("query must contain at least one letter or digit")
    wanted = set(kinds or KINDS)
    for k in wanted:
        if k not in KINDS:
            raise DioceseError(f"unknown kind {k!r}; use one of {', '.join(KINDS)}")

    sources: list[tuple[str, _Kind, list[dict[str, Any]]]] = []
    if diocese in (None, LIVE):
        sources.append((LIVE, PARISH, _read_live_csv(PARISHES_CSV_PATH)))
        sources.append((LIVE, CHURCH, _read_live_csv(CHURCHES_CSV_PATH)))
    if diocese is None:
        explored = _diocese_slugs()
    elif diocese == LIVE:
        explored = []
    else:
        _diocese_dir(diocese)
        explored = [diocese]
    for slug in explored:
        for kind in KINDS.values():
            sources.append((slug, kind, _load(slug, kind)))

    hits = []
    for where, kind, rows in sources:
        if kind.name not in wanted:
            continue
        for row in rows:
            text = normalize(" ".join(
                " ".join(v) if isinstance(v, list) else str(v)
                for v in row.values() if v is not None
            ))
            if all(w in text for w in words):
                hits.append({
                    "diocese": where, "kind": kind.name, "slug": row.get("slug", ""),
                    "name": row.get("name", ""), "summary": _summary(kind, row),
                })
    return {"query": query, "count": len(hits), "results": hits[:limit], "truncated": len(hits) > limit}


def validate(diocese: str | None = None) -> dict[str, Any]:
    """Check one diocese, or all of them; `passed` is false if any has errors."""
    report = {}
    for slug in [diocese] if diocese else _diocese_slugs():
        _diocese_dir(slug)
        p = _problems(slug, _load_all(slug))
        report[slug] = {"errors": p.errors, "warnings": p.warnings}
    return {
        "passed": not any(r["errors"] for r in report.values()),
        "dioceses": report,
    }


def export_csv(diocese: str, out_dir: Path) -> dict[str, Any]:
    """Write the diocese as `parishes.csv` and `churches.csv` in the live format.

    Refuses while the diocese has validation errors. The files are for review
    and appending to `data/`; this never touches the live CSVs itself.
    """
    data = _load_all(diocese)
    problems = _problems(diocese, data)
    if problems.errors:
        raise DioceseError(
            "fix these first (see `diocese validate`):\n  " + "\n  ".join(problems.errors)
        )
    out_dir.mkdir(parents=True, exist_ok=True)

    def cell(value: Any) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        return "" if value is None else str(value)

    written = {}
    for kind, columns in ((PARISH, _PARISH_CSV_FIELDS), (CHURCH, _CHURCH_CSV_FIELDS)):
        path = out_dir / kind.file.replace(".json", ".csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
            writer.writeheader()
            for row in data[kind.name]:
                writer.writerow({c: cell(row.get(c)) for c in columns})
        written[str(path)] = len(data[kind.name])
    return {"diocese": diocese, "written": written, "warnings": problems.warnings}
