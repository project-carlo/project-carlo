"""The files under `data/dioceses/<diocese>/` and every operation on them.

A diocese being explored is a folder of small Markdown files, one per record:

    diocese.md            the diocese: its sources and their quirks, and a dated log
    parishes/<slug>.md    one per bulletin publisher, i.e. one row of data/parishes.csv
    churches/<slug>.md    one per worship site, i.e. one row of data/churches.csv
    excluded/<slug>.md    a place that was looked at and ruled out, with the reason
    open/<slug>.md        a place or question not decided yet, with what would settle it
    rosters/<name>.json   snapshots of outside lists (see `rosters`)

Each record is YAML frontmatter (the structured fields, including its dated
`evidence`) followed by a Markdown body: the explanation, written so that
someone auditing the row later can check it quickly. The slug is the file name.

Agents and people edit these files directly; the `diocese` command validates
them and does the operations that touch several files at once (merging
parishes, renaming, excluding a church, promoting to the live CSVs). Those
operations are refused, with nothing written, if they would add a validation
error.
"""

from __future__ import annotations

import csv
import datetime as dt
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from pdf_extract import storage
from pdf_extract.fetch import PROVIDERS_TAKING_RECIPE
from pdf_extract.parish_sites import Recipe

META_FILE = "diocese.md"
ROSTERS_DIR = "rosters"
LIVE = "live"  # how `search` labels rows of data/parishes.csv and data/churches.csv

# Every value a parish record may use. `fetch` reads the first four; `no_bulletin`
# rows stay out of data/parishes.csv (see `unpublished`).
NO_BULLETIN = "no_bulletin"
KNOWN_BULLETIN_PROVIDERS = frozenset(
    {"parishes_online", "ecatholic", "discover_mass", "other", "google_drive", NO_BULLETIN}
)
# Providers `fetch` looks up by account id rather than by the parish website.
PROVIDERS_NEEDING_ID = frozenset({"parishes_online", "discover_mass"})

# Why a place is not modelled. Keep the classes apart: `closed` has to stay a
# record of what shut down, so an open church that publishes nothing is
# `no-bulletin`, never `closed`.
EXCLUSION_REASONS = {
    "closed": "no longer holds Mass: closed, merged away, sold or demolished",
    "no-bulletin": "holds public Mass but publishes nothing the pipeline could read",
    "no-public-mass": "not a public worship site: office, school, pregnancy center, "
                      "cemetery, private convent or hospital chapel",
    "not-catholic": "a same-named church of another denomination",
    "other-jurisdiction": "belongs to another diocese or eparchy, or is listed here in error",
    "other": "none of the above; the explanation says what",
}

# Publication ids name the bulletin itself, so two parish rows may never share
# one. `scheme:value`.
PUBLICATION_SCHEMES = {
    "po-container": r"\d+/\d+",              # container.parishesonline.com/bulletins/14/0434/
    "po-org": r"[a-z0-9-]+",                 # parishesonline.com/organization/<slug>
    "lpi": r"[A-Za-z0-9]{15}(?:[A-Za-z0-9]{3})?",  # publicationWidget?id=, a Salesforce id
    "ecatholic": r"\d+",                     # files.ecatholic.com/<site id>/
    "discovermass": r"[a-z0-9-]+",           # discovermass.com/church/<slug>/
    "url": r"https?://\S+",                  # anything else: the page the bulletin is posted on
}

COORDINATE_SOURCES = (
    "gcatholic-plus-code", "osm-node", "diocese-directory", "parishes-online-org", "nominatim",
    "geocode-stage", "manual",
)

TODO = "TODO"

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_STATE_RE = re.compile(r"^[A-Z]{2}$")
_POSTAL_RE = re.compile(r"^\d{5}(?:-\d{4})?$")
_URL_RE = re.compile(r"^https?://\S+$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PARTIAL_DATE_RE = re.compile(r"^\d{4}(-(0[1-9]|1[0-2]))?$")
_ROSTER_REF_RE = re.compile(r"^([a-z0-9-]+):(\S+)$")


class DioceseError(ValueError):
    """A diocese command was given bad input; the message says what to fix."""


# ── Record kinds ────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Kind:
    name: str
    dir: str
    always: tuple[str, ...]      # written even when empty, so the file shows what can be set
    optional: tuple[str, ...]    # written only when set
    template: str                # body of a new record

    @property
    def fields(self) -> tuple[str, ...]:
        return self.always + self.optional


_REVISIT = ("revisit", "revisit_after")
_ADDRESS = ("line1", "city", "state", "postal_code")

PARISH = Kind(
    name="parish",
    dir="parishes",
    always=(
        "name", "website", "bulletin_provider", "provider_id", "publication", "group", "evidence",
    ),
    optional=("replaces", *_REVISIT, "promoted"),
    template="""\
## Publisher

TODO: Who publishes this bulletin and which worship sites it covers. Name the issue you
read (its date, and the page) and quote the masthead or Mass schedule that lists them. If
the diocese groups this parish with others, say whether they share this bulletin and what
shows it.

## Worship sites

TODO: Why exactly these churches. Name any building the bulletin, the diocese or a roster
still lists that is not here, and where it went (excluded/, open/, another parish).

## Website and bulletin provider

TODO: Why this URL is where the bulletin can be found, and where bulletin_provider,
provider_id and publication came from. For `other`, the provider_id recipe and the
`fetch:check` run that suggested it.

## Not yet confirmed

TODO: Anything you could not check, and what would settle it. "Nothing." if nothing.
""",
)
CHURCH = Kind(
    name="church",
    dir="churches",
    always=(
        "parish", "name", "line1", "line2", "city", "state", "postal_code",
        "latitude", "longitude", "coordinates_from", "name_verified", "address_verified",
        "roster", "evidence",
    ),
    optional=("replaces", *_REVISIT, "promoted"),
    template="""\
## Holds Mass

TODO: Evidence that Mass is celebrated here now: the current bulletin or the parish's own
Mass schedule, with its date. Four Masses a year still counts; say so if that is all.

## Name and address

TODO: Which sources give this name and address, whether they agree, and which one you
followed when they do not. Say where the coordinates came from.
""",
)
EXCLUDED = Kind(
    name="excluded",
    dir="excluded",
    always=("name", "reason", *_ADDRESS, "decided", "roster", "evidence"),
    optional=("parish", "last_mass", *_REVISIT, "promoted"),
    template="""\
## Why it is excluded

TODO: The claim (closed on <date>, no public Mass, publishes nothing, ...) and the source
that states it, quoted and dated. Being absent from a list is not enough on its own: say
which current bulletin or schedule you read and that it does not include this place.

## What would change this

TODO: A pending appeal, a reopening, a new bulletin... or "Nothing expected."
""",
)
OPEN = Kind(
    name="open",
    dir="open",
    always=("name", "revisit", "revisit_after", "roster", "evidence"),
    optional=("parish", *_ADDRESS, "promoted"),
    template="""\
## What is known

TODO: What each source says, dated, including the ones that disagree.

## Why it is not decided

TODO: Why neither a church row nor an exclusion is justified yet.
""",
)
KINDS: dict[str, Kind] = {k.name: k for k in (PARISH, CHURCH, EXCLUDED, OPEN)}

_LIST_FIELDS = {"publication", "replaces", "roster"}
_BOOL_FIELDS = {"name_verified", "address_verified"}
_FLOAT_FIELDS = {"latitude", "longitude"}
_DATE_FIELDS = {"decided", "last_mass", "revisit_after", "promoted"}
_EVIDENCE_FIELDS = ("url", "seen", "quote", "note")

META_FIELDS = ("name", "state", "website", "status", "gcatholic", "city_aliases", "promoted")
META_STATUSES = ("exploring", "promoted")
META_TEMPLATE = """\
## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.
Fill this in as you find them (see data/dioceses/README.md, "Sources").

- Parish directory:
- GCatholic:
- Clusters / families of parishes:
- Mass times:
- Closed parishes and where their records went:
- Pastoral plan / closure announcements:

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.
"""


def _empty(fname: str) -> Any:
    if fname in _LIST_FIELDS or fname == "evidence":
        return []
    if fname in _BOOL_FIELDS:
        return False
    if fname in _FLOAT_FIELDS or fname in _DATE_FIELDS:
        return None
    return ""


# ── Helpers ─────────────────────────────────────────────────────────────────
def slugify(text: str) -> str:
    """`St. Mary's Church` -> `st-marys-church`."""
    text = re.sub(r"['’]", "", text.lower().replace("&", " and "))
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


_CHURCH_WORDS = re.compile(r"\b(church|parish|roman catholic|catholic|rc)\b", re.I)


def church_slug(name: str, city: str) -> str:
    """Dedication plus town: `St. Mary Church`, Mayville -> `st-mary-mayville`.

    Always suffixed with the town, not only on a collision: every diocese has a
    dozen St. Marys, and a slug that is unique today gets renamed tomorrow.
    """
    base = slugify(_CHURCH_WORDS.sub(" ", name)) or slugify(name)
    town = slugify(city)
    return base if not town or base.endswith(town) else f"{base}-{town}"


_ABBREVIATIONS = {"st": "saint", "sts": "saints", "ss": "saints", "mt": "mount"}


def normalize(text: str) -> str:
    """Lowercase, no punctuation, St./Sts./Mt. spelled out: for matching names."""
    text = re.sub(r"['’]", "", str(text).lower().replace("&", " and "))
    tokens = re.sub(r"[^a-z0-9]+", " ", text).split()
    return " ".join(_ABBREVIATIONS.get(t, t) for t in tokens)


def url_key(url: str) -> str:
    """Compare websites without scheme, `www.` or a trailing slash."""
    url = re.sub(r"^https?://(www\.)?", "", (url or "").strip().lower())
    return url.rstrip("/")


def today() -> str:
    return dt.date.today().isoformat()


def _plain(value: Any) -> Any:
    """YAML turns 2026-09-06 into a date; keep every date an ISO string."""
    if isinstance(value, dt.datetime):
        return value.date().isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, list):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    return value


# ── Frontmatter files ───────────────────────────────────────────────────────
_FRONT_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)(.*)\Z", re.S)


def parse_file(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = _FRONT_RE.match(text)
    if not m:
        raise DioceseError(f"{path}: must start with a '---' YAML frontmatter block")
    try:
        front = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        raise DioceseError(f"{path}: frontmatter is not valid YAML: {e}") from None
    if not isinstance(front, dict):
        raise DioceseError(f"{path}: frontmatter must be a mapping of field: value")
    front = _plain(front)
    if isinstance(front, dict) and type(front.get("last_mass")) is int:
        front["last_mass"] = str(front["last_mass"])  # a bare year: last_mass: 2017
    return front, m.group(2).strip("\n")


class _Flow(list):
    """A list written inline: `roster: [gcatholic:123, directory:45]`."""


class _Dumper(yaml.SafeDumper):
    pass


def _represent_str(dumper: yaml.SafeDumper, value: str) -> yaml.Node:
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_Dumper.add_representer(str, _represent_str)
_Dumper.add_representer(
    _Flow, lambda d, v: d.represent_sequence("tag:yaml.org,2002:seq", v, flow_style=True),
)


def _as_dates(value: Any, key: str = "") -> Any:
    """ISO date strings back to dates for writing, so they come out unquoted."""
    if isinstance(value, dict):
        return {k: _as_dates(v, k) for k, v in value.items()}
    if isinstance(value, list) and not isinstance(value, _Flow):
        return [_as_dates(v) for v in value]
    if key in _DATE_FIELDS | {"seen"} and isinstance(value, str) and _DATE_RE.match(value):
        try:
            return dt.date.fromisoformat(value)
        except ValueError:
            return value
    return value


def _dump_front(front: Mapping[str, Any]) -> str:
    return yaml.dump(
        _as_dates(dict(front)), Dumper=_Dumper, sort_keys=False, allow_unicode=True, width=100,
        default_flow_style=False,
    )


def render(kind: Kind, record: Mapping[str, Any]) -> str:
    """A record as file text: frontmatter in the kind's field order, then the body."""
    front: dict[str, Any] = {}
    for fname in kind.fields:
        value = record.get(fname, _empty(fname))
        if fname in kind.optional and value in ("", [], None, False):
            continue
        if fname in _LIST_FIELDS:
            value = _Flow(value or [])
        elif fname == "evidence":
            value = [
                {k: e[k] for k in _EVIDENCE_FIELDS if e.get(k) not in (None, "")}
                | {k: v for k, v in e.items() if k not in _EVIDENCE_FIELDS}
                for e in (value or []) if isinstance(e, Mapping)
            ] or []
        front[fname] = value
    # Keep fields this version does not know, so a hand-added one is not lost;
    # validate warns about them.
    for fname, value in record.items():
        if fname not in front and fname not in kind.fields and fname not in ("slug", "body"):
            front[fname] = value
    body = (record.get("body") or "").strip("\n")
    return f"---\n{_dump_front(front)}---\n\n{body}\n"


# ── Loading and saving ──────────────────────────────────────────────────────
def dioceses_dir() -> Path:
    return storage.DIOCESES_DIR


def diocese_slugs() -> list[str]:
    root = dioceses_dir()
    if not root.exists():
        return []
    return sorted(p.parent.name for p in root.glob(f"*/{META_FILE}"))


def diocese_dir(diocese: str, *, must_exist: bool = True) -> Path:
    if not _SLUG_RE.match(diocese or ""):
        raise DioceseError(f"diocese must be a slug like 'syracuse', got {diocese!r}")
    path = dioceses_dir() / diocese
    if must_exist and not (path / META_FILE).exists():
        known = ", ".join(diocese_slugs()) or "none yet"
        raise DioceseError(f"no diocese {diocese!r} (known: {known}); create it with `diocese init`")
    return path


def load_meta(diocese: str) -> dict[str, Any]:
    front, body = parse_file(diocese_dir(diocese) / META_FILE)
    return {"slug": diocese, **front, "body": body}


def _load_kind(diocese: str, kind: Kind, unreadable: list[str]) -> dict[str, dict[str, Any]]:
    folder = diocese_dir(diocese) / kind.dir
    records: dict[str, dict[str, Any]] = {}
    for path in sorted(folder.glob("*.md")) if folder.exists() else []:
        try:
            front, body = parse_file(path)
        except DioceseError as e:
            unreadable.append(str(e))
            continue
        records[path.stem] = {"slug": path.stem, **front, "body": body}
    return records


@dataclass
class Diocese:
    """Every record of one diocese, keyed by kind name then slug."""

    slug: str
    records: dict[str, dict[str, dict[str, Any]]] = field(default_factory=dict)
    unreadable: list[str] = field(default_factory=list)  # files that failed to parse

    def of(self, kind: Kind) -> dict[str, dict[str, Any]]:
        return self.records.setdefault(kind.name, {})

    def copy(self) -> Diocese:
        return Diocese(self.slug, {
            k: {s: _deep_copy(r) for s, r in recs.items()} for k, recs in self.records.items()
        }, list(self.unreadable))


def _deep_copy(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _deep_copy(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_deep_copy(v) for v in value]
    return value


def load(diocese: str) -> Diocese:
    """Every record of a diocese. A file that does not parse is left out and reported by
    `problems`, so one bad hand edit does not hide the rest."""
    unreadable: list[str] = []
    recs = {k.name: _load_kind(diocese, k, unreadable) for k in KINDS.values()}
    return Diocese(diocese, recs, unreadable)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _save(before: Diocese, after: Diocese) -> dict[str, list[str]]:
    """Write the records that changed and delete the ones that went away."""
    root = diocese_dir(after.slug)
    written, deleted = [], []
    for kind in KINDS.values():
        old, new = before.of(kind), after.of(kind)
        for slug, record in new.items():
            if old.get(slug) != record:
                _write_text(root / kind.dir / f"{slug}.md", render(kind, record))
                written.append(f"{kind.dir}/{slug}.md")
        for slug in old.keys() - new.keys():
            (root / kind.dir / f"{slug}.md").unlink()
            deleted.append(f"{kind.dir}/{slug}.md")
    return {"written": sorted(written), "deleted": sorted(deleted)}


def read_live_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


# ── Validation ──────────────────────────────────────────────────────────────
@dataclass
class Problems:
    """`errors` block every write; `incomplete` blocks export and promote."""

    errors: list[str] = field(default_factory=list)
    incomplete: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, list[str]]:
        return {"errors": self.errors, "incomplete": self.incomplete, "warnings": self.warnings}


def _label(kind: Kind, slug: str) -> str:
    return f"{kind.name} {slug!r}"


def _check_date(label: str, fname: str, value: Any, p: Problems) -> None:
    if value in (None, ""):
        return
    if fname == "last_mass" and isinstance(value, str) and _PARTIAL_DATE_RE.match(value):
        return  # a source that gives only the year or month ("final Mass in 2017")
    if not isinstance(value, str) or not _DATE_RE.match(value):
        hint = " (or 2017, or 2017-06, when a source gives no day)" if fname == "last_mass" else ""
        p.errors.append(f"{label}: {fname} must be a date like 2026-09-06{hint}, got {value!r}")


def _check_evidence(label: str, evidence: Any, p: Problems) -> None:
    if not isinstance(evidence, list):
        p.errors.append(f"{label}: evidence must be a list of {{url, seen, quote, note}} items")
        return
    if not evidence:
        p.incomplete.append(f"{label}: no evidence recorded")
    for i, item in enumerate(evidence, 1):
        where = f"{label}: evidence #{i}"
        if not isinstance(item, Mapping):
            p.errors.append(f"{where} must be a mapping with url and seen, got {item!r}")
            continue
        if not _URL_RE.match(str(item.get("url") or "")):
            p.errors.append(f"{where}: url must start with http:// or https://")
        if not item.get("seen"):
            p.errors.append(f"{where}: seen (the date you read it) is required")
        else:
            _check_date(where, "seen", item.get("seen"), p)
            if str(item.get("seen")) > today():
                p.errors.append(f"{where}: seen {item['seen']} is in the future")
        if not (item.get("quote") or item.get("note")):
            p.warnings.append(f"{where}: add a quote or a note saying what this source shows")
        for key in item:
            if key not in _EVIDENCE_FIELDS:
                p.warnings.append(f"{where}: unknown field {key!r} (use url, seen, quote, note)")


def _check_record(kind: Kind, r: Mapping[str, Any], rosters: Mapping[str, set[str]] | None,
                  p: Problems) -> None:
    slug = r["slug"]
    label = _label(kind, slug)
    if not _SLUG_RE.match(slug):
        p.errors.append(f"{label}: the file name must be a slug (lowercase words joined by '-')")
    for fname in r:
        if fname not in kind.fields and fname not in ("slug", "body"):
            p.warnings.append(f"{label}: unknown field {fname!r}")
    if not str(r.get("name") or "").strip():
        p.errors.append(f"{label}: name is required")
    for fname in kind.fields:
        value = r.get(fname)
        if value is None:
            continue
        if fname in _LIST_FIELDS and not isinstance(value, list):
            p.errors.append(f"{label}: {fname} must be a list, e.g. {fname}: [a, b]")
        elif fname in _BOOL_FIELDS and not isinstance(value, bool):
            p.errors.append(f"{label}: {fname} must be true or false")
        elif fname in _FLOAT_FIELDS and (isinstance(value, bool)
                                         or not isinstance(value, int | float)):
            p.errors.append(f"{label}: {fname} must be a number or null")
        elif fname in _DATE_FIELDS:
            _check_date(label, fname, value, p)
        elif (fname not in _LIST_FIELDS | _BOOL_FIELDS | _FLOAT_FIELDS | {"evidence"}
              and not isinstance(value, str)):
            hint = " (quote it: postal_code: \"01234\")" if fname == "postal_code" else ""
            p.errors.append(f"{label}: {fname} must be text, got {value!r}{hint}")

    _check_evidence(label, r.get("evidence", []), p)
    body = r.get("body") or ""
    if not body.strip():
        p.incomplete.append(f"{label}: the explanation (the text below the frontmatter) is empty")
    elif TODO in body:
        p.incomplete.append(f"{label}: the explanation still has {TODO} placeholders")

    if r.get("revisit_after") and not r.get("revisit"):
        p.errors.append(f"{label}: revisit_after needs revisit (what to check then)")

    for ref in r.get("roster") or []:
        m = _ROSTER_REF_RE.match(str(ref))
        if not m:
            p.errors.append(f"{label}: roster entry {ref!r} must look like <roster>:<id>")
        elif rosters is not None:
            if m.group(1) not in rosters:
                p.warnings.append(f"{label}: roster {m.group(1)!r} has no file in rosters/")
            elif m.group(2) not in rosters[m.group(1)]:
                p.warnings.append(f"{label}: {ref} is not in rosters/{m.group(1)}.json any more")

    if kind in (CHURCH, EXCLUDED, OPEN):
        state = r.get("state") or ""
        if state and not _STATE_RE.match(str(state)):
            p.errors.append(f"{label}: state must be a two-letter code like 'NY', got {state!r}")
        postal = r.get("postal_code") or ""
        if postal and isinstance(postal, str) and not _POSTAL_RE.match(postal):
            p.errors.append(f"{label}: postal_code must look like \"13202\", got {postal!r}")

    if kind is PARISH:
        _check_parish(label, r, p)
    elif kind is CHURCH:
        _check_church(label, r, p)
    elif kind is EXCLUDED:
        reason = r.get("reason") or ""
        if reason not in EXCLUSION_REASONS:
            p.errors.append(f"{label}: reason must be one of {', '.join(EXCLUSION_REASONS)}")
        if reason == "closed" and not r.get("last_mass"):
            p.warnings.append(f"{label}: closed without last_mass; date it if any source does")
        if not r.get("decided"):
            p.errors.append(f"{label}: decided (the date you excluded it) is required")
    elif kind is OPEN:
        if not str(r.get("revisit") or "").strip():
            p.errors.append(f"{label}: revisit (the next thing to check) is required")


def _check_parish(label: str, r: Mapping[str, Any], p: Problems) -> None:
    website = str(r.get("website") or "")
    if not website:
        p.errors.append(f"{label}: website is required (where the bulletin can be found)")
    elif not _URL_RE.match(website):
        p.errors.append(f"{label}: website must start with http:// or https://")
    provider = r.get("bulletin_provider") or ""
    if provider and provider not in KNOWN_BULLETIN_PROVIDERS:
        p.errors.append(
            f"{label}: bulletin_provider {provider!r} is not one of "
            f"{', '.join(sorted(KNOWN_BULLETIN_PROVIDERS))}"
        )
    if not provider:
        p.incomplete.append(f"{label}: bulletin_provider not identified yet")
    if provider in PROVIDERS_NEEDING_ID and not r.get("provider_id"):
        p.incomplete.append(f"{label}: {provider} needs a provider_id for fetch to find it")
    if provider in PROVIDERS_TAKING_RECIPE and r.get("provider_id"):
        try:
            Recipe.parse(str(r["provider_id"]), website=website)
        except ValueError as exc:
            p.errors.append(f"{label}: provider_id is not a fetch recipe: {exc}")
    for pub in r.get("publication") or []:
        problem = publication_problem(str(pub))
        if problem:
            p.errors.append(f"{label}: publication {pub!r}: {problem}")
    if not r.get("publication") and provider != NO_BULLETIN:
        p.warnings.append(
            f"{label}: no publication id recorded, so nothing can check that no other "
            "row publishes the same bulletin"
        )


def publication_problem(pub: str) -> str | None:
    scheme, _, value = pub.partition(":")
    pattern = PUBLICATION_SCHEMES.get(scheme)
    if pattern is None:
        return f"scheme must be one of {', '.join(PUBLICATION_SCHEMES)}"
    if not re.fullmatch(pattern, value):
        if scheme == "lpi":
            return ("an LPi publicationWidget id is 15 or 18 letters and digits, e.g. "
                    "0018000000Qbyz4AAB; a digits-only value is the truncated shared prefix")
        return f"does not look like a {scheme} id"
    return None


def _check_church(label: str, r: Mapping[str, Any], p: Problems) -> None:
    for fname in ("line1", "city", "state", "postal_code"):
        if not r.get(fname):
            p.incomplete.append(f"{label}: {fname} is missing")
    lat, lng = r.get("latitude"), r.get("longitude")
    if (lat is None) != (lng is None):
        p.errors.append(f"{label}: set latitude and longitude together")
    if isinstance(lat, int | float) and not isinstance(lat, bool) and not -90 <= lat <= 90:
        p.errors.append(f"{label}: latitude must be between -90 and 90")
    if isinstance(lng, int | float) and not isinstance(lng, bool) and not -180 <= lng <= 180:
        p.errors.append(f"{label}: longitude must be between -180 and 180")
    source = r.get("coordinates_from") or ""
    if lat is not None and not source:
        p.warnings.append(f"{label}: say where the coordinates came from (coordinates_from)")
    if source and source not in COORDINATE_SOURCES:
        p.warnings.append(
            f"{label}: coordinates_from {source!r} is not one of {', '.join(COORDINATE_SOURCES)}"
        )


@dataclass
class _Owners:
    """Slugs, websites and publication ids claimed outside one diocese."""

    parish: dict[str, str] = field(default_factory=dict)
    church: dict[str, str] = field(default_factory=dict)
    website: dict[str, str] = field(default_factory=dict)
    publication: dict[str, str] = field(default_factory=dict)
    live_parish: dict[str, dict[str, str]] = field(default_factory=dict)
    live_church: dict[str, dict[str, str]] = field(default_factory=dict)


def _owners(diocese: str) -> _Owners:
    o = _Owners()
    for row in read_live_csv(storage.PARISHES_CSV_PATH):
        o.live_parish[row.get("slug", "")] = row
    for row in read_live_csv(storage.CHURCHES_CSV_PATH):
        o.live_church[row.get("slug", "")] = row
    for other in diocese_slugs():
        if other == diocese:
            continue
        where = f"diocese {other!r}"
        d = load(other)
        for slug, r in d.of(PARISH).items():
            o.parish.setdefault(slug, where)
            o.website.setdefault(url_key(r.get("website", "")), where)
            for pub in r.get("publication") or []:
                o.publication.setdefault(str(pub), f"{where} parish {slug!r}")
        for slug in d.of(CHURCH):
            o.church.setdefault(slug, where)
    for table in (o.parish, o.church, o.website):
        table.pop("", None)
    return o


def roster_ids(diocese: str) -> dict[str, set[str]]:
    """Entry ids of every roster file of the diocese, by roster name."""
    import json

    folder = diocese_dir(diocese) / ROSTERS_DIR
    out: dict[str, set[str]] = {}
    for path in sorted(folder.glob("*.json")) if folder.exists() else []:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            out[path.stem] = {str(e.get("id")) for e in data.get("entries", [])}
        except (ValueError, AttributeError):
            out[path.stem] = set()
    return out


def problems(d: Diocese, *, owners: _Owners | None = None,
             rosters: Mapping[str, set[str]] | None = None) -> Problems:
    """Every error, gap and warning in one diocese, given its (possibly unsaved) records."""
    p = Problems()
    p.errors.extend(d.unreadable)
    owners = owners or _owners(d.slug)
    for kind in KINDS.values():
        for r in d.of(kind).values():
            _check_record(kind, r, rosters, p)

    parishes, churches = d.of(PARISH), d.of(CHURCH)
    excluded, open_ = d.of(EXCLUDED), d.of(OPEN)

    # Cross-kind slug clashes: a place is a church, an exclusion or an open question.
    for a, b in ((CHURCH, EXCLUDED), (CHURCH, OPEN), (EXCLUDED, OPEN)):
        for slug in d.of(a).keys() & d.of(b).keys():
            p.errors.append(f"{slug!r} is both in {a.dir}/ and {b.dir}/; keep one")

    # Uniqueness the database enforces, across dioceses and the live CSVs. A
    # record stamped `promoted` owns the live row with its slug.
    for kind, own, live in ((PARISH, owners.parish, owners.live_parish),
                            (CHURCH, owners.church, owners.live_church)):
        for slug, r in d.of(kind).items():
            if slug in own:
                p.errors.append(f"{_label(kind, slug)}: slug already used in {own[slug]}")
            elif slug in live and not r.get("promoted"):
                p.errors.append(
                    f"{_label(kind, slug)}: slug already used in data/{kind.dir}.csv; slugs are "
                    "unique across all dioceses"
                )
    live_sites = {url_key(row.get("website", "")): slug
                  for slug, row in owners.live_parish.items()}
    seen_sites: dict[str, str] = {}
    for slug, r in parishes.items():
        key = url_key(r.get("website", ""))
        if not key:
            continue
        label = _label(PARISH, slug)
        if key in owners.website:
            p.errors.append(f"{label}: website already used by {owners.website[key]}")
        elif key in live_sites and not (r.get("promoted") and live_sites[key] == slug):
            p.errors.append(f"{label}: website already used by data/parishes.csv "
                            f"row {live_sites[key]!r}")
        if key in seen_sites:
            p.errors.append(f"{label}: website also used by parish {seen_sites[key]!r}; one "
                            "website is one bulletin, so these are probably one parish")
        seen_sites[key] = slug

    # One bulletin, one row: the check with no other symptom anywhere.
    pubs: dict[str, str] = {}
    for slug, r in parishes.items():
        for pub in r.get("publication") or []:
            pub = str(pub)
            if pub in pubs:
                p.errors.append(
                    f"parishes {pubs[pub]!r} and {slug!r} both publish {pub}; one bulletin is "
                    "one parish row (`diocese merge`), unless the id is wrong"
                )
            elif pub in owners.publication:
                p.errors.append(f"{_label(PARISH, slug)}: {pub} is also claimed by "
                                f"{owners.publication[pub]}")
            pubs.setdefault(pub, slug)

    with_churches = set()
    for slug, r in churches.items():
        parish = r.get("parish") or ""
        with_churches.add(parish)
        if parish not in parishes:
            p.errors.append(f"{_label(CHURCH, slug)}: parish {parish!r} is not in parishes/")
    for slug in sorted(parishes.keys() - with_churches):
        p.incomplete.append(f"{_label(PARISH, slug)}: no churches")
    for kind, recs in ((EXCLUDED, excluded), (OPEN, open_)):
        for slug, r in recs.items():
            parish = r.get("parish") or ""
            if parish and parish not in parishes and parish not in owners.live_parish:
                p.warnings.append(f"{_label(kind, slug)}: parish {parish!r} is not a known parish")
    for slug, r in parishes.items():
        for old in r.get("replaces") or []:
            if old in parishes:
                p.errors.append(f"{_label(PARISH, slug)}: replaces {old!r}, which still exists")

    refs: dict[str, str] = {}
    for kind in (CHURCH, EXCLUDED, OPEN):
        for slug, r in d.of(kind).items():
            for ref in r.get("roster") or []:
                if ref in refs:
                    p.warnings.append(f"{ref} is linked from both {refs[ref]} and "
                                      f"{_label(kind, slug)}; a roster entry is one place")
                refs.setdefault(ref, _label(kind, slug))

    _check_drift(d, owners, p)
    return p


def unpublished(d: Diocese) -> tuple[set[str], set[str]]:
    """Parishes and churches kept in the records but left off the site.

    A `no_bulletin` parish publishes nothing the pipeline can read, so its
    churches would only ever show an empty schedule. Its records stay, with
    their evidence and revisit date, and go live when a bulletin turns up.
    """
    parishes = {slug for slug, r in d.of(PARISH).items()
                if r.get("bulletin_provider") == NO_BULLETIN}
    churches = {slug for slug, r in d.of(CHURCH).items() if r.get("parish") in parishes}
    return parishes, churches


def export_rows(d: Diocese) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """The diocese's rows in the column layout of the live CSVs, without `unpublished` ones."""
    def cell(value: Any) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        return "" if value is None else str(value)

    skip_p, skip_c = unpublished(d)
    parishes = [
        {"slug": slug, "name": cell(r.get("name")), "website": cell(r.get("website")),
         "bulletin_provider": cell(r.get("bulletin_provider")),
         "provider_id": cell(r.get("provider_id"))}
        for slug, r in sorted(d.of(PARISH).items()) if slug not in skip_p
    ]
    churches = [
        {"parish_id": cell(r.get("parish")), "slug": slug,
         **{c: cell(r.get(c)) for c in CHURCH_CSV_FIELDS[2:]}}
        for slug, r in sorted(d.of(CHURCH).items(), key=lambda kv: (kv[1].get("parish"), kv[0]))
        if slug not in skip_c
    ]
    return parishes, churches


PARISH_CSV_FIELDS = ["slug", "name", "website", "bulletin_provider", "provider_id"]
# Set on the parish rows `promote` adds; kept as it is on rows already live.
FETCH_ONLY_COLUMN = "fetch_only"
CHURCH_CSV_FIELDS = [
    "parish_id", "slug", "name", "line1", "line2", "city", "state", "postal_code",
    "name_verified", "address_verified", "latitude", "longitude",
]


def _same_cell(a: str, b: str) -> bool:
    if a == b:
        return True
    try:
        return float(a) == float(b)
    except ValueError:
        return a.strip().lower() == b.strip().lower() and a.lower() in ("true", "false")


def _check_drift(d: Diocese, owners: _Owners, p: Problems) -> None:
    """Promoted records whose live row has since changed (or gone, or should go)."""
    for kind, off_site, live in zip((PARISH, CHURCH), unpublished(d),
                                    (owners.live_parish, owners.live_church), strict=True):
        for slug in sorted(off_site & live.keys()):
            if d.of(kind)[slug].get("promoted"):
                p.warnings.append(f"{_label(kind, slug)}: no_bulletin, but still in "
                                  f"data/{kind.dir}.csv; run `diocese promote` to take it off")
    parishes, churches = export_rows(d)
    for kind, rows, live in ((PARISH, parishes, owners.live_parish),
                             (CHURCH, churches, owners.live_church)):
        for row in rows:
            record = d.of(kind)[row["slug"]]
            if not record.get("promoted"):
                continue
            current = live.get(row["slug"])
            if current is None:
                p.warnings.append(f"{_label(kind, row['slug'])}: promoted, but no longer in "
                                  f"data/{kind.dir}.csv; run `diocese promote` or exclude it")
                continue
            differ = [c for c, v in row.items() if not _same_cell(v, current.get(c, ""))]
            if differ:
                p.warnings.append(f"{_label(kind, row['slug'])}: data/{kind.dir}.csv differs in "
                                  f"{', '.join(differ)}; run `diocese promote` to reconcile")


def _commit(before: Diocese, after: Diocese, *, tolerate_unreadable: bool = False
            ) -> dict[str, Any]:
    """Save `after` unless it adds errors; return what changed and the new warnings.

    A file that doesn't parse blocks commands that move references between
    files (merge, rename, exclude): they could miss the ones inside it. Changes
    confined to readable records (a new file, roster links) pass
    `tolerate_unreadable`, so one half-written file doesn't stop everyone
    else's work; the unparseable files are named in the warnings.
    """
    if before.unreadable and not tolerate_unreadable:
        raise DioceseError("fix these files first; they do not parse:\n  "
                           + "\n  ".join(before.unreadable))
    owners = _owners(after.slug)
    ids = roster_ids(after.slug)
    old, new = problems(before, owners=owners, rosters=ids), problems(after, owners=owners,
                                                                      rosters=ids)
    added = [e for e in new.errors if e not in old.errors]
    if added:
        raise DioceseError("refused, nothing was written:\n  " + "\n  ".join(added))
    changes = _save(before, after)
    return {**changes, "warnings": [w for w in new.warnings + new.incomplete
                                    if w not in old.warnings + old.incomplete]
            + [f"does not parse (left alone): {u}" for u in before.unreadable]}


def _get(d: Diocese, kind: Kind, slug: str) -> dict[str, Any]:
    try:
        return d.of(kind)[slug]
    except KeyError:
        raise DioceseError(f"no {kind.name} {slug!r} in diocese {d.slug!r}") from None


# ── Operations ──────────────────────────────────────────────────────────────
def list_dioceses() -> dict[str, Any]:
    out = []
    for slug in diocese_slugs():
        meta = load_meta(slug)
        d = load(slug)
        out.append({
            "slug": slug, "name": meta.get("name", ""), "status": meta.get("status", ""),
            **{kind.dir: len(d.of(kind)) for kind in KINDS.values()},
        })
    return {"dioceses_dir": str(dioceses_dir()), "dioceses": out}


def init_diocese(diocese: str, *, name: str, state: str = "", website: str = "",
                 gcatholic: str = "") -> dict[str, Any]:
    if diocese == LIVE:
        raise DioceseError(f"{LIVE!r} is reserved: search uses it for the live CSVs")
    path = diocese_dir(diocese, must_exist=False)
    if (path / META_FILE).exists():
        raise DioceseError(f"diocese {diocese!r} already exists at {path}")
    if not name.strip():
        raise DioceseError("name is required, e.g. 'Roman Catholic Diocese of Syracuse'")
    if state and not _STATE_RE.match(state):
        raise DioceseError(f"state must be a two-letter code like 'NY', got {state!r}")
    front = {"name": name.strip(), "state": state, "website": website, "status": "exploring",
             "gcatholic": gcatholic}
    _write_text(path / META_FILE, f"---\n{_dump_front(front)}---\n\n{META_TEMPLATE}")
    for kind in KINDS.values():
        (path / kind.dir).mkdir(parents=True, exist_ok=True)
        (path / kind.dir / ".gitkeep").touch()
    (path / ROSTERS_DIR).mkdir(exist_ok=True)
    (path / ROSTERS_DIR / ".gitkeep").touch()
    return {"created": str(path), "diocese": front}


def new_record(diocese: str, kind_name: str, fields: Mapping[str, Any], *,
               slug: str | None = None, body: str | None = None) -> dict[str, Any]:
    """Create one record file, with the kind's explanation template as its body.

    `fields` may hold any frontmatter field; strings are coerced for the typed
    ones, so this serves the CLI flags as well as scripts adding rows in bulk.
    """
    kind = KINDS[kind_name]
    record: dict[str, Any] = {f: _empty(f) for f in kind.fields}
    for fname, value in fields.items():
        if value is None:
            continue
        if fname not in kind.fields:
            raise DioceseError(f"{kind.name} has no field {fname!r}")
        record[fname] = _coerce(fname, value)
    if kind is EXCLUDED and not record["decided"]:
        record["decided"] = today()
    if not slug:
        if kind is CHURCH or (kind in (EXCLUDED, OPEN) and record.get("city")):
            slug = church_slug(record["name"], record.get("city", ""))
        else:
            slug = slugify(record["name"])
    record["slug"] = slug
    record["body"] = body if body is not None else kind.template

    before = load(diocese)
    # the file on disk, not the loaded records: an unparseable one isn't loaded
    if slug in before.of(kind) or (diocese_dir(diocese) / kind.dir / f"{slug}.md").exists():
        raise DioceseError(f"{kind.dir}/{slug}.md already exists; edit it, or pick another slug")
    after = before.copy()
    after.of(kind)[slug] = record
    result = _commit(before, after, tolerate_unreadable=True)
    return {"created": f"{kind.dir}/{slug}.md", "diocese": diocese, "slug": slug, **result}


def _coerce(fname: str, value: Any) -> Any:
    """A CLI string (or Python value) as the type stored for `fname`."""
    if fname in _LIST_FIELDS:
        if isinstance(value, str):
            value = [value]
        return [str(v).strip() for v in value if str(v).strip()]
    if fname == "evidence":
        return list(value)
    if fname in _BOOL_FIELDS:
        if isinstance(value, bool):
            return value
        text = str(value).strip().lower()
        if text in ("true", "yes", "1"):
            return True
        if text in ("", "false", "no", "0"):
            return False
        raise DioceseError(f"{fname} must be true or false, got {value!r}")
    if fname in _FLOAT_FIELDS:
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            raise DioceseError(f"{fname} must be a number, got {value!r}") from None
    if fname in _DATE_FIELDS:
        return str(value).strip() or None
    return str(value).strip()


def merge_parishes(diocese: str, sources: Iterable[str], into: str,
                   *, note: str = "") -> dict[str, Any]:
    """Fold parish rows that turned out to share one bulletin into `into`.

    Their churches move to `into`; their publication ids, evidence and (when
    `into` has none) provider id are carried over, so nothing learned about
    them is lost; their explanations are appended under a heading; and their
    slugs go in `into`'s `replaces`, which is how `promote` knows to delete
    their live rows.
    """
    before = load(diocese)
    after = before.copy()
    target = _get(after, PARISH, into)
    sources = [s for s in dict.fromkeys(sources)]
    if not sources:
        raise DioceseError("name at least one parish to merge")
    if into in sources:
        raise DioceseError(f"cannot merge {into!r} into itself")
    moved: list[str] = []
    stamp = today()
    for slug in sources:
        source = _get(after, PARISH, slug)
        for cslug, church in after.of(CHURCH).items():
            if church.get("parish") == slug:
                church["parish"] = into
                moved.append(cslug)
        for kind in (EXCLUDED, OPEN):
            for r in after.of(kind).values():
                if r.get("parish") == slug:
                    r["parish"] = into
        target["replaces"] = list(dict.fromkeys(
            [*(target.get("replaces") or []), slug, *(source.get("replaces") or [])]
        ))
        target["publication"] = list(dict.fromkeys(
            [*(target.get("publication") or []), *(source.get("publication") or [])]
        ))
        if not target.get("provider_id") and source.get("provider_id"):
            target["provider_id"] = source["provider_id"]
            target["bulletin_provider"] = target.get("bulletin_provider") or source.get(
                "bulletin_provider", "")
        known = {(e.get("url"), e.get("quote")) for e in target.get("evidence") or []}
        target["evidence"] = [*(target.get("evidence") or []), *(
            e for e in source.get("evidence") or [] if (e.get("url"), e.get("quote")) not in known
        )]
        if source.get("promoted") and not target.get("promoted"):
            target["promoted"] = source["promoted"]
        old_body = re.sub(r"^(#+) ", r"#\1 ", (source.get("body") or "").strip(), flags=re.M)
        target["body"] = (
            f"{(target.get('body') or '').rstrip()}\n\n"
            f"## Merged in: {slug} ({source.get('name', '')}), {stamp}\n\n"
            + (f"{note.strip()}\n\n" if note.strip() else "")
            + "Its explanation before the merge:\n\n" + old_body
        )
        del after.of(PARISH)[slug]
    result = _commit(before, after)
    return {"merged": sources, "into": into, "moved_churches": sorted(moved), **result}


def rename_record(diocese: str, kind_name: str, old: str, new: str) -> dict[str, Any]:
    """Change a slug, and every reference to it."""
    kind = KINDS[kind_name]
    before = load(diocese)
    after = before.copy()
    record = _get(after, kind, old)
    if new in after.of(kind):
        raise DioceseError(f"{kind.dir}/{new}.md already exists")
    del after.of(kind)[old]
    record["slug"] = new
    if record.get("promoted") and kind in (PARISH, CHURCH):
        record["replaces"] = list(dict.fromkeys([*(record.get("replaces") or []), old]))
    after.of(kind)[new] = record
    if kind is PARISH:
        for k in (CHURCH, EXCLUDED, OPEN):
            for r in after.of(k).values():
                if r.get("parish") == old:
                    r["parish"] = new
    return {"renamed": f"{kind.dir}/{old}.md -> {kind.dir}/{new}.md", **_commit(before, after)}


def exclude_church(diocese: str, slug: str, *, reason: str, last_mass: str = "",
                   explanation: str = "") -> dict[str, Any]:
    """Turn a church row into an exclusion: it closed, or should never have been added.

    Name, address, roster links and evidence carry over; the church's old
    explanation is kept under a heading. If the church was promoted, `promote`
    will delete its live row.
    """
    if reason not in EXCLUSION_REASONS:
        raise DioceseError(f"reason must be one of {', '.join(EXCLUSION_REASONS)}")
    before = load(diocese)
    after = before.copy()
    church = _get(after, CHURCH, slug)
    if slug in after.of(EXCLUDED):
        raise DioceseError(f"excluded/{slug}.md already exists")
    old_body = re.sub(r"^(#+) ", r"#\1 ", (church.get("body") or "").strip(), flags=re.M)
    why = explanation.strip() or EXCLUDED.template
    excluded = {
        "slug": slug, "name": church.get("name", ""), "reason": reason,
        "parish": church.get("parish", ""),
        **{f: church.get(f, "") for f in _ADDRESS},
        "last_mass": last_mass or None, "decided": today(),
        "roster": church.get("roster") or [], "evidence": church.get("evidence") or [],
        "promoted": church.get("promoted"),
        "body": f"{why.rstrip()}\n\n## When it was a church row\n\n{old_body}",
    }
    del after.of(CHURCH)[slug]
    after.of(EXCLUDED)[slug] = excluded
    return {"excluded": slug, "reason": reason, **_commit(before, after)}


def question_church(diocese: str, slug: str, *, revisit: str,
                    revisit_after: str = "") -> dict[str, Any]:
    """Turn a church row into an open question: no current Mass found, nothing says it closed.

    Carries over what `exclude_church` does. If the church was promoted,
    `promote` will delete its live row until the question is settled.
    """
    if not revisit.strip():
        raise DioceseError("revisit (the next thing to check) is required")
    before = load(diocese)
    after = before.copy()
    church = _get(after, CHURCH, slug)
    if slug in after.of(OPEN):
        raise DioceseError(f"open/{slug}.md already exists")
    old_body = re.sub(r"^(#+) ", r"#\1 ", (church.get("body") or "").strip(), flags=re.M)
    question = {
        "slug": slug, "name": church.get("name", ""), "revisit": revisit.strip(),
        "revisit_after": revisit_after or None, "parish": church.get("parish", ""),
        **{f: church.get(f, "") for f in _ADDRESS},
        "roster": church.get("roster") or [], "evidence": church.get("evidence") or [],
        "promoted": church.get("promoted"),
        "body": f"{OPEN.template.rstrip()}\n\n## When it was a church row\n\n{old_body}",
    }
    del after.of(CHURCH)[slug]
    after.of(OPEN)[slug] = question
    return {"question": slug, **_commit(before, after)}


def show_diocese(diocese: str) -> dict[str, Any]:
    """The diocese at a glance: parishes with their churches, exclusions, open questions."""
    meta = load_meta(diocese)
    d = load(diocese)
    churches: dict[str, list[dict[str, str]]] = {}
    for slug, c in d.of(CHURCH).items():
        churches.setdefault(c.get("parish", ""), []).append(
            {"slug": slug, "name": c.get("name", ""), "city": c.get("city", "")}
        )
    by_reason: dict[str, list[str]] = {}
    for slug, r in d.of(EXCLUDED).items():
        by_reason.setdefault(r.get("reason", ""), []).append(slug)
    return {
        "diocese": {k: meta.get(k) for k in ("slug", *META_FIELDS) if meta.get(k)},
        "counts": {kind.dir: len(d.of(kind)) for kind in KINDS.values()},
        "parishes": [
            {
                "slug": slug, "name": r.get("name", ""), "website": r.get("website", ""),
                "bulletin_provider": r.get("bulletin_provider", ""),
                "publication": r.get("publication") or [],
                "churches": churches.get(slug, []),
            }
            for slug, r in d.of(PARISH).items()
        ],
        "excluded": by_reason,
        "open": {slug: r.get("revisit", "") for slug, r in d.of(OPEN).items()},
    }


def validate(diocese: str | None = None) -> dict[str, Any]:
    """Check one diocese, or all; `passed` is false if any has errors."""
    report = {}
    for slug in [diocese] if diocese else diocese_slugs():
        report[slug] = problems(load(slug), rosters=roster_ids(slug)).as_dict()
        report[slug]["counts"] = {k: len(v) for k, v in report[slug].items()}
    return {"passed": not any(r["errors"] for r in report.values()), "dioceses": report}


def _ready(diocese: str) -> Diocese:
    d = load(diocese)
    p = problems(d, rosters=roster_ids(diocese))
    blocking = p.errors + p.incomplete
    if blocking:
        shown = "\n  ".join(blocking[:40])
        more = f"\n  ... and {len(blocking) - 40} more" if len(blocking) > 40 else ""
        raise DioceseError(f"not ready (see `diocese validate {diocese}`):\n  {shown}{more}")
    return d


def export_csv(diocese: str, out_dir: Path) -> dict[str, Any]:
    """Write the diocese as parishes.csv and churches.csv in the live layout, for review."""
    parishes, churches = export_rows(_ready(diocese))
    out_dir.mkdir(parents=True, exist_ok=True)
    written = {}
    for name, columns, rows in (("parishes.csv", PARISH_CSV_FIELDS, parishes),
                                ("churches.csv", CHURCH_CSV_FIELDS, churches)):
        path = out_dir / name
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        written[str(path)] = len(rows)
    return {"diocese": diocese, "written": written}


def _write_live_csv(path: Path, columns: list[str], rows: list[dict[str, str]]) -> None:
    """Write `rows` under the file's own header, adding any of `columns` it lacks."""
    with open(path, encoding="utf-8", newline="") as f:
        header = next(csv.reader(f), [])
    header += [col for col in columns if col not in header]
    tmp = path.with_suffix(".csv.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


def promote(diocese: str, *, dry_run: bool = False) -> dict[str, Any]:
    """Bring data/parishes.csv and data/churches.csv in line with this diocese.

    New rows are appended and promoted rows updated in place. Live rows the
    diocese has retired are deleted: slugs in a record's `replaces` (merged or
    renamed away), promoted churches that are now in excluded/ or open/, and `no_bulletin`
    parishes with their churches (see `unpublished`). A record
    that is blank where the live row has a value (coordinates from `geocode`,
    flags from `verify`) takes the live value instead of erasing it. Every
    promoted record is stamped `promoted: <date>`, which is what lets it share
    its slug with a live row from then on; an `unpublished` one loses its stamp.

    A parish row added here is marked `fetch_only`: the weekly run fetches its
    bulletins but makes no model call for it and leaves it off the website
    until the flag is cleared. Rows already live keep their flag.
    """
    d = _ready(diocese)
    after = d.copy()
    parish_rows, church_rows = export_rows(d)
    live_p = read_live_csv(storage.PARISHES_CSV_PATH)
    live_c = read_live_csv(storage.CHURCHES_CSV_PATH)
    stamp = today()
    report: dict[str, Any] = {"diocese": diocese, "dry_run": dry_run}

    retired_p = {old for r in d.of(PARISH).values() for old in r.get("replaces") or []}
    retired_c = {old for r in d.of(CHURCH).values() for old in r.get("replaces") or []}
    retired_c |= {slug for kind in (EXCLUDED, OPEN) for slug, r in d.of(kind).items()
                  if r.get("promoted")}
    unpublished_p, unpublished_c = unpublished(d)
    retired_p |= unpublished_p
    retired_c |= unpublished_c

    def apply(kind: Kind, live: list[dict[str, str]], rows: list[dict[str, str]],
              retired: set[str]) -> tuple[list[dict[str, str]], dict[str, Any]]:
        mine = {row["slug"]: row for row in rows}
        out, changed, adopted = [], {}, {}
        for row in live:
            slug = row.get("slug", "")
            if slug in retired and slug not in mine:
                continue
            if slug in mine:
                new = mine.pop(slug)
                record = after.of(kind)[slug]
                for col, value in new.items():
                    current = row.get(col, "")
                    if value == "" and current != "" and col in (
                        "latitude", "longitude", "name_verified", "address_verified"
                    ):
                        record[col] = _coerce(col, current)
                        adopted.setdefault(slug, []).append(col)
                        new[col] = current
                    elif not _same_cell(value, current):
                        changed.setdefault(slug, []).append(col)
                if slug in adopted and {"latitude", "longitude"} & set(adopted[slug]):
                    record["coordinates_from"] = record.get("coordinates_from") or "geocode-stage"
                row = {**row, **new}
            out.append(row)
        added = list(mine)
        out.extend(mine.values())
        kept = {r["slug"] for r in rows}
        removed = sorted({row.get("slug", "") for row in live} & (retired - kept))
        return out, {"added": added, "updated": changed, "removed": removed,
                     "kept_live_values": adopted}

    new_p, report["parishes"] = apply(PARISH, live_p, parish_rows, retired_p)
    added_p = set(report["parishes"]["added"])
    for row in new_p:
        if row.get("slug") in added_p:
            row[FETCH_ONLY_COLUMN] = "true"
    new_c, report["churches"] = apply(CHURCH, live_c, church_rows, retired_c)

    live_church_parents = {row.get("parish_id") for row in new_c}
    orphans = sorted(live_church_parents - {row.get("slug") for row in new_p} - {None, ""})
    if orphans:
        raise DioceseError(f"refused: churches.csv would reference missing parishes {orphans}")
    report["removed_rows_with_events"] = _referenced_by_events(
        report["churches"]["removed"], report["parishes"]["removed"],
    )

    if not dry_run:
        # The stamp means "owns a live row", so an unpublished record carries none.
        for kind, off_site in ((PARISH, unpublished_p), (CHURCH, unpublished_c)):
            for slug, r in after.of(kind).items():
                if slug in off_site:
                    r.pop("promoted", None)
                else:
                    r["promoted"] = r.get("promoted") or stamp
        _write_live_csv(
            storage.PARISHES_CSV_PATH, [*PARISH_CSV_FIELDS, FETCH_ONLY_COLUMN], new_p,
        )
        _write_live_csv(storage.CHURCHES_CSV_PATH, CHURCH_CSV_FIELDS, new_c)
        _save(d, after)
        meta_path = diocese_dir(diocese) / META_FILE
        front, body = parse_file(meta_path)
        front.update(status="promoted", promoted=stamp)
        _write_text(meta_path, f"---\n{_dump_front(front)}---\n\n{body}\n")
        report["next"] = (
            "run `pnpm test`; the next pipeline command seeds the new rows into the database"
            + (
                f". The {len(added_p)} new parishes are fetch-only: clear `fetch_only` in"
                " data/parishes.csv to process them and show them on the site"
                if added_p else ""
            )
        )
    return report


def _referenced_by_events(church_slugs: list[str], parish_slugs: list[str] = ()) -> list[str]:
    """Churches that would lose events in the local pipeline database.

    Worth knowing before promoting: the next pipeline command re-seeds the
    database from the CSVs. A removed church loses its events, and a removed
    parish takes its bulletins, and every event read from them, with it, even
    for churches that move to another parish. The weekly run holds for review
    when that happens.
    """
    import sqlite3

    if not (church_slugs or parish_slugs) or not storage.DEFAULT_DB_PATH.exists():
        return []
    churches, parishes = list(church_slugs) or [""], list(parish_slugs) or [""]
    try:
        conn = sqlite3.connect(f"file:{storage.DEFAULT_DB_PATH}?mode=ro", uri=True)
        try:
            rows = conn.execute(
                f"""SELECT DISTINCT c.slug FROM church c
                    JOIN event e ON e.church_id = c.id
                    JOIN bulletin b ON b.id = e.bulletin_id
                    JOIN parish p ON p.id = b.parish_id
                    WHERE c.slug IN ({", ".join("?" * len(churches))})
                       OR p.slug IN ({", ".join("?" * len(parishes))})""",
                [*churches, *parishes],
            ).fetchall()
        finally:
            conn.close()
    except sqlite3.Error:
        return []
    return sorted(slug for (slug,) in rows)


# ── Search ──────────────────────────────────────────────────────────────────
def _summary(kind: Kind, r: Mapping[str, Any]) -> str:
    if kind is PARISH:
        return str(r.get("website", ""))
    address = ", ".join(str(r.get(f)) for f in ("line1", "city") if r.get(f))
    extra = {CHURCH: f"parish {r.get('parish', '')}", EXCLUDED: str(r.get("reason", "")),
             OPEN: str(r.get("revisit", ""))[:80]}[kind]
    return f"{address} ({extra})" if address else extra


def search(query: str, *, diocese: str | None = None, kinds: Iterable[str] | None = None,
           limit: int = 50) -> dict[str, Any]:
    """Records whose text contains every word of `query`, across every diocese and the live CSVs.

    Use it before adding anything: it catches a place that is already a row, a
    live row, an exclusion or an open question. St./Saint and Sts./Ss. match.
    """
    words = normalize(query).split()
    if not words:
        raise DioceseError("query must contain at least one letter or digit")
    wanted = set(kinds or KINDS)
    unknown = wanted - set(KINDS)
    if unknown:
        raise DioceseError(f"unknown kind {sorted(unknown)}; use {', '.join(KINDS)}")

    sources: list[tuple[str, Kind, Mapping[str, Mapping[str, Any]]]] = []
    if diocese in (None, LIVE):
        sources.append((LIVE, PARISH, {r["slug"]: r for r in
                                       read_live_csv(storage.PARISHES_CSV_PATH)}))
        sources.append((LIVE, CHURCH, {
            r["slug"]: {**r, "parish": r.get("parish_id", "")}
            for r in read_live_csv(storage.CHURCHES_CSV_PATH)
        }))
    explored = diocese_slugs() if diocese is None else [] if diocese == LIVE else [diocese]
    for slug in explored:
        d = load(slug)
        sources.extend((slug, kind, d.of(kind)) for kind in KINDS.values())

    hits = []
    for where, kind, records in sources:
        if kind.name not in wanted:
            continue
        for slug, r in records.items():
            text = normalize(" ".join([slug, *(
                " ".join(map(str, v)) if isinstance(v, list) else str(v)
                for k, v in r.items() if k not in ("body", "evidence") and v is not None
            )]))
            if all(w in text.split() or w in text for w in words):
                hits.append({"diocese": where, "kind": kind.name, "slug": slug,
                             "name": r.get("name", ""), "summary": _summary(kind, r)})
    return {"query": query, "count": len(hits), "results": hits[:limit],
            "truncated": len(hits) > limit}
