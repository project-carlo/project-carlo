"""A small generated dataset, so the labeler runs (and is tested) without R2.

`build_demo(root)` writes, under `root`:

- `parish_events.db`: three parishes, four bulletins
- `bulletins/<parish>/<hash>.pdf`: generated bulletin PDFs (hash = SHA-256 of the bytes)
- `runs/gemini-flash/cache/...`: fake Gemini results, under the current
  classifier version for one bulletin and an older version for another
- `labels/`: where the demo's labels go (kept when the dataset is rebuilt)
- `seeds/holy-family-demo.json`: a drafted seed with open questions, for the
  Seeds mode (written once; a rebuild keeps the review made of it)

Each Gemini source is covered: a cached result for the current version, one
for an older version, a bulletin with only post-processed rows in the `event`
table, and one that was never processed.
"""

from __future__ import annotations

import csv
import json
from hashlib import sha256
from pathlib import Path
from typing import Any

from pdf_extract.blobstore import CachedBlobStore, LocalBlobStore, bulletin_pdf_key
from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.db import migrate, seed_reference_data
from pdf_extract.runner import cache_key, flatten_extracted_events
from pdf_extract.seeding.files import new_seed, read_seed, write_seed_file
from pdf_extract.storage import (
    church_list_for_prompt,
    connect_db,
    delete_db,
    insert_bulletin,
    save_processed_bulletin,
)

OLD_CLASSIFIER_VERSION = "gemini-2.5-flash+prompt-0123456789ab"

PARISHES = [
    {"slug": "holy-family-demo", "name": "Holy Family Demo Parish",
     "website": "https://example.org/holy-family"},
    {"slug": "st-anne-demo", "name": "St. Anne Demo Parish",
     "website": "https://example.org/st-anne"},
    {"slug": "our-lady-demo", "name": "Our Lady of the Lake Demo Parish",
     "website": "https://example.org/our-lady"},
]
CHURCHES = [
    {"parish_id": "holy-family-demo", "slug": "holy-family-demo-rochester",
     "name": "Holy Family Church", "line1": "123 Main St", "city": "Rochester",
     "state": "NY", "postal_code": "14620"},
    {"parish_id": "holy-family-demo", "slug": "st-joseph-demo-penfield",
     "name": "St. Joseph Church", "line1": "45 Oak Ave", "city": "Penfield",
     "state": "NY", "postal_code": "14526"},
    {"parish_id": "st-anne-demo", "slug": "st-anne-demo-fairport",
     "name": "St. Anne Church", "line1": "9 Church St", "city": "Fairport",
     "state": "NY", "postal_code": "14450"},
    {"parish_id": "our-lady-demo", "slug": "our-lady-demo-webster",
     "name": "Our Lady of the Lake Church", "line1": "300 Lake Rd", "city": "Webster",
     "state": "NY", "postal_code": "14580"},
]

HF, SJ = "holy-family-demo-rochester", "st-joseph-demo-penfield"
SA, OL = "st-anne-demo-fairport", "our-lady-demo-webster"

# ── Minimal PDF writer ──────────────────────────────────────────────────────
Line = tuple[float, str] | tuple[float, str, str]  # (font size, text[, "b" for bold])


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_pdf(pages: list[list[Line]]) -> bytes:
    """A US Letter PDF with one text line per entry, top to bottom, in Helvetica.

    Deterministic (no timestamps), so the same pages always hash the same.
    """
    objects: list[bytes] = [b"", b""]  # 1: catalog, 2: page tree (filled in below)
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
                   b"/Encoding /WinAnsiEncoding >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold "
                   b"/Encoding /WinAnsiEncoding >>")
    page_ids = []
    for lines in pages:
        y = 740.0
        ops = []
        for line in lines:
            size, text = line[0], line[1]
            bold = len(line) > 2 and line[2] == "b"
            if text:
                ops.append(f"BT /{'F2' if bold else 'F1'} {size:g} Tf 60 {y:g} Td "
                           f"({_escape(text)}) Tj ET")
            y -= size * 1.5
        stream = "\n".join(ops).encode("latin-1")
        objects.append(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream")
        content_id = len(objects)
        objects.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents %d 0 R >>" % content_id
        )
        page_ids.append(len(objects))
    objects[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{i} 0 R" for i in page_ids).encode()
    objects[1] = b"<< /Type /Pages /Kids [%s] /Count %d >>" % (kids, len(page_ids))

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objects) + 1, xref,
    )
    return bytes(out)


# ── Bulletin contents ───────────────────────────────────────────────────────
def _cover(parish: str, churches: list[str], sunday: str, date_line: str) -> list[Line]:
    return [
        (24, parish.upper(), "b"),
        *[(11, c) for c in churches],
        (11, ""),
        (16, sunday, "b"),
        (14, date_line),
        (11, ""),
        (13, "From the Pastor's Desk", "b"),
        (11, "Dear friends, as the days grow shorter we give thanks for a summer of"),
        (11, "good work: the food pantry served more families than ever, and our"),
        (11, "young people returned from their service trip full of stories."),
        (11, "Please keep our catechists in your prayers as classes begin."),
        (11, ""),
        (11, "Parish office: Monday to Thursday, 9:00 AM to 3:00 PM."),
    ]


HOLY_FAMILY_SEP27 = make_pdf([
    _cover("Holy Family Demo Parish",
           ["Holy Family Church - 123 Main St, Rochester, NY 14620",
            "St. Joseph Church - 45 Oak Ave, Penfield, NY 14526"],
           "Twenty-Sixth Sunday in Ordinary Time", "September 27, 2026"),
    [
        (16, "WEEKEND & DAILY MASS SCHEDULE", "b"),
        (12, "Holy Family Church", "b"),
        (11, "Saturday Vigil: 4:00 PM"),
        (11, "Sunday: 8:00 AM and 10:30 AM"),
        (11, "Monday - Friday: 8:00 AM"),
        (12, "St. Joseph Church", "b"),
        (11, "Sunday: 9:00 AM"),
        (11, "Wednesday: 7:00 PM (Spanish)"),
        (11, ""),
        (16, "SACRAMENT OF RECONCILIATION (CONFESSION)", "b"),
        (11, "Holy Family: Saturday 3:00 - 3:45 PM"),
        (11, "St. Joseph: First Friday of the month, 6:00 - 7:00 PM"),
        (11, ""),
        (16, "EUCHARISTIC ADORATION", "b"),
        (11, "Holy Family: Thursdays 9:00 AM - 7:00 PM, September through May"),
        (11, "Holy Hour at St. Joseph: every Tuesday except the second Tuesday, 6:00 - 7:00 PM"),
    ],
    [
        (16, "THIS WEEK AT THE PARISH", "b"),
        (11, "Please note: the 8:00 AM Mass at Holy Family on Monday, October 5 is cancelled."),
        (11, "Feast of the Guardian Angels: Mass at St. Joseph on Friday, October 2 at 7:00 PM."),
        (11, ""),
        (11, "Parish picnic: Sunday, October 4 after the 10:30 AM Mass on the lawn."),
        (11, "Food pantry volunteers needed Saturdays from 9:00 to 11:00 AM."),
        (11, "Bible study meets Tuesdays at 10:00 AM in the parish hall."),
    ],
])

HOLY_FAMILY_SEP20 = make_pdf([
    _cover("Holy Family Demo Parish",
           ["Holy Family Church - 123 Main St, Rochester, NY 14620",
            "St. Joseph Church - 45 Oak Ave, Penfield, NY 14526"],
           "Twenty-Fifth Sunday in Ordinary Time", "September 20, 2026"),
    [
        (16, "MASS SCHEDULE", "b"),
        (11, "Holy Family: Saturday 4:00 PM; Sunday 8:00 AM, 10:30 AM; weekdays 8:00 AM"),
        (11, "St. Joseph: Sunday 9:00 AM; Wednesday 7:00 PM (Spanish)"),
        (11, ""),
        (16, "CONFESSIONS", "b"),
        (11, "Holy Family: Saturday 3:00 - 3:45 PM"),
    ],
])

ST_ANNE_SEP27 = make_pdf([
    _cover("St. Anne Demo Parish", ["St. Anne Church - 9 Church St, Fairport, NY 14450"],
           "Twenty-Sixth Sunday in Ordinary Time", "September 27, 2026"),
    [
        (16, "MASSES", "b"),
        (11, "Saturday 5:00 PM  |  Sunday 9:30 AM and 11:30 AM"),
        (11, "Tuesday and Thursday 12:10 PM"),
        (11, ""),
        (16, "CONFESSIONS", "b"),
        (11, "Saturday 3:30 - 4:30 PM, or by appointment"),
        (11, ""),
        (16, "ADORATION", "b"),
        (11, "First Friday of each month, 9:00 AM until noon"),
        (11, "No Tuesday Mass on October 13 (Father on retreat)."),
    ],
])

OUR_LADY_SEP27 = make_pdf([[
    (24, "OUR LADY OF THE LAKE DEMO PARISH", "b"),
    (11, "Our Lady of the Lake Church - 300 Lake Rd, Webster, NY 14580"),
    (14, "September 27, 2026"),
    (11, ""),
    (16, "MASS TIMES", "b"),
    (11, "Saturday 4:30 PM, Sunday 8:30 AM and 11:00 AM"),
    (11, "Daily Mass Monday, Wednesday, Friday 7:00 AM"),
    (16, "RECONCILIATION", "b"),
    (11, "Saturday 3:30 - 4:15 PM"),
]])


def _ev(church: str, event_type: str, kind: str, when: str, start: str, *,
        end: str | None = None, cancelled: bool = False, page: int | None = 2,
        note: str | None = None) -> dict[str, Any]:
    weekly = kind == "weekly"
    return {
        "church_slug": church, "type": event_type, "kind": kind,
        "day_of_week": when if weekly else None, "date": None if weekly else when,
        "start_time": start, "end_time": end, "cancelled": cancelled,
        "page_number": page, "note": note,
    }


HOLY_FAMILY_GEMINI = {
    "events": [
        _ev(HF, "mass", "weekly", "Saturday", "4:00 PM"),
        _ev(HF, "mass", "weekly", "Sunday", "8:00 AM"),
        _ev(HF, "mass", "weekly", "Sunday", "10:30 AM"),
        *[_ev(HF, "mass", "weekly", d, "8:00 AM")
          for d in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")],
        _ev(SJ, "mass", "weekly", "Sunday", "9:00 AM"),
        _ev(HF, "confession", "weekly", "Saturday", "3:00 PM", end="3:45 PM"),
        _ev(SJ, "confession", "weekly", "Friday", "6:00 PM", end="7:00 PM", note="First Friday"),
        _ev(HF, "adoration", "weekly", "Thursday", "9:00 AM", end="7:00 PM",
            note="September through May"),
        _ev(SJ, "adoration", "weekly", "Tuesday", "6:00 PM", end="7:00 PM", note="Holy Hour"),
        _ev(SJ, "mass", "specific_date", "2026-10-02", "7:00 PM", page=3,
            note="Feast of the Guardian Angels"),
        _ev(HF, "mass", "specific_date", "2026-10-05", "8:00 AM", cancelled=True, page=3),
    ],
    "church_list_needs_review": False,
    "published_date": "2026-09-27",
    "wrong_bulletin": False,
    "usage": {"prompt_tokens": 3000, "output_tokens": 800},
}

ST_ANNE_GEMINI_OLD = {
    "events": [
        _ev(SA, "mass", "weekly", "Saturday", "5:00 PM"),
        _ev(SA, "mass", "weekly", "Sunday", "9:30 AM"),
        _ev(SA, "mass", "weekly", "Sunday", "11:30 AM"),
        _ev(SA, "mass", "weekly", "Tuesday", "12:10pm"),
        _ev(SA, "confession", "weekly", "Saturday", "3:30 PM", end="4:30 PM"),
        _ev(SA, "adoration", "weekly", "Friday", "9:00 AM", end="after Mass", note="First Friday"),
    ],
    "church_list_needs_review": False,
    "published_date": "2026-09-26",
    "wrong_bulletin": False,
}

HOLY_FAMILY_SEP20_ROWS = [
    {"church_slug": c, "event_type": t, "event_kind": "weekly", "day_of_week": d, "date": None,
     "start_time": s, "end_time": e, "cancelled": False, "page_number": 2, "note": n}
    for c, t, d, s, e, n in [
        (HF, "mass", "Saturday", "4:00 PM", None, None),
        (HF, "mass", "Sunday", "8:00 AM", None, None),
        (HF, "mass", "Sunday", "10:30 AM", None, None),
        (SJ, "mass", "Sunday", "9:00 AM", None, None),
        (SJ, "mass", "Wednesday", "7:00 PM", None, "Spanish"),
        (HF, "confession", "Saturday", "3:00 PM", "3:45 PM", None),
    ]
]


def _entry(church: str, event_type: str, when: str, start: str, *, end: str | None = None,
           weekly: bool = True, cancelled: bool = False, weeks: list[str] | None = None,
           season: dict[str, Any] | None = None, note: str | None = None) -> dict[str, Any]:
    return {
        "church_slug": church, "event_type": event_type,
        "event_kind": "weekly" if weekly else "specific_date",
        "day_of_week": when if weekly else None, "date": None if weekly else when,
        "start_time": start, "end_time": end, "cancelled": cancelled,
        "weeks_of_month": weeks or [], "exclude_weeks": False, "season": season, "note": note,
    }


def _slot(slot_id: str, entry: dict[str, Any], said: str, rationale: str, *, page: int = 2,
          older: str | None = None, decision: str = "include") -> dict[str, Any]:
    sources = [{"source": "agent", "bulletin": "NEW", "page": page, "said": said}]
    if older:
        sources.append({"source": "agent", "bulletin": "OLD", "page": 2, "said": older})
    return {
        "id": slot_id, "decision": decision, "status": "settled", "entry": entry,
        "page": page, "sources": sources, "rationale": rationale,
        "question": None, "options": None, "answer": None,
    }


def demo_seed(new: dict[str, Any], old: dict[str, Any]) -> dict[str, Any]:
    """A drafted seed for Holy Family, two bulletins read, two questions left open."""
    seed = new_seed("holy-family-demo", [new, old])
    for b in seed["bulletins"]:
        b["read"] = True
    seed.update(status="needs_review", as_of=new["fetched_at"], summary=(
        "Two churches. Weekend and daily Masses agree across both bulletins. Two questions: "
        "whether the Monday Mass is weekly, and which Tuesdays the St. Joseph Holy Hour runs."
    ))
    weekend = "Printed in the Mass schedule of both bulletins read; history agrees."
    slots = [
        _slot("s1", _entry(HF, "mass", "Saturday", "16:00", note="Vigil"),
              "Saturday Vigil: 4:00 PM", weekend, older="Saturday 4:00 PM"),
        _slot("s2", _entry(HF, "mass", "Sunday", "08:00"), "Sunday: 8:00 AM and 10:30 AM",
              weekend, older="Sunday 8:00 AM, 10:30 AM"),
        _slot("s3", _entry(HF, "mass", "Sunday", "10:30"), "Sunday: 8:00 AM and 10:30 AM",
              weekend, older="Sunday 8:00 AM, 10:30 AM"),
        _slot("s4", _entry(SJ, "mass", "Sunday", "09:00"), "Sunday: 9:00 AM", weekend,
              older="St. Joseph: Sunday 9:00 AM"),
        _slot("s5", _entry(SJ, "mass", "Wednesday", "19:00", note="Spanish"),
              "Wednesday: 7:00 PM (Spanish)", weekend, older="Wednesday 7:00 PM (Spanish)"),
        _slot("s6", _entry(HF, "confession", "Saturday", "15:00", end="15:45"),
              "Holy Family: Saturday 3:00 - 3:45 PM", weekend,
              older="Holy Family: Saturday 3:00 - 3:45 PM"),
        _slot("s7", _entry(SJ, "confession", "Friday", "18:00", end="19:00", weeks=["first"]),
              "St. Joseph: First Friday of the month, 6:00 - 7:00 PM",
              "Printed in the newest bulletin only, as first Fridays: a monthly slot."),
        _slot("s8", _entry(HF, "adoration", "Thursday", "09:00", end="19:00", season={
            "start_month": 9, "start_day": None, "end_month": 5, "end_day": None}),
              "Holy Family: Thursdays 9:00 AM - 7:00 PM, September through May",
              "The bulletin gives the season; the policy keeps it on the slot."),
        _slot("s9", _entry(SJ, "mass", "2026-10-02", "19:00", weekly=False,
                           note="Feast of the Guardian Angels"),
              "Feast of the Guardian Angels: Mass at St. Joseph on Friday, October 2 at 7:00 PM.",
              "A one-off Mass printed with its date.", page=3),
        _slot("s10", _entry(HF, "mass", "2026-10-05", "08:00", weekly=False, cancelled=True),
              "the 8:00 AM Mass at Holy Family on Monday, October 5 is cancelled.",
              "A dated cancellation of the weekday Mass, after as_of: the seed keeps it.",
              page=3),
        _slot("s11", _entry(HF, "mass", "Saturday", "09:00",
                            note="Food pantry volunteers"),
              "Food pantry volunteers needed Saturdays from 9:00 to 11:00 AM.",
              "Not a Mass: a volunteer shift. Left out, as the policy asks.", page=3,
              decision="exclude"),
    ]
    for i, day in enumerate(("Tuesday", "Wednesday", "Thursday", "Friday"), start=12):
        slots.append(_slot(f"s{i}", _entry(HF, "mass", day, "08:00"), "Monday - Friday: 8:00 AM",
                           weekend, older="weekdays 8:00 AM"))
    slots.append({
        "id": "s16", "decision": None, "status": "needs_human", "entry": None, "page": 2,
        "sources": [
            {"source": "agent", "bulletin": "NEW", "page": 2, "said": "Monday - Friday: 8:00 AM"},
            {"source": "agent", "bulletin": "OLD", "page": 2, "said": "weekdays 8:00 AM"},
            {"source": "history", "bulletin": "OLD", "said": "no weekday Masses stored"},
        ],
        "rationale": "Both bulletins print a weekday Mass, but the newest also cancels the "
        "Monday, October 5 Mass, and extract mode never stored a weekday Mass. Monday is "
        "likely weekly with one date cancelled.",
        "question": "Holy Family: is the Monday 8:00 AM Mass weekly?",
        "options": [
            {"label": "Every Monday, 8:00 AM", "entry": _entry(HF, "mass", "Monday", "08:00"),
             "leaning": True},
            {"label": "Leave out", "entry": None},
        ],
        "answer": None,
    })
    slots.append({
        "id": "s17", "decision": None, "status": "needs_human", "entry": None, "page": 2,
        "sources": [{
            "source": "agent", "bulletin": "NEW", "page": 2,
            "said": "Holy Hour at St. Joseph: every Tuesday except the second Tuesday, "
            "6:00 - 7:00 PM",
        }],
        "rationale": "Adoration with an exception. The weeks that remain are first, third, "
        "fourth and fifth, but a reviewer should confirm that reading.",
        "question": "St. Joseph Holy Hour on Tuesdays: every week but the second?",
        "options": [
            {"label": "First, third, fourth and fifth Tuesdays",
             "entry": _entry(SJ, "adoration", "Tuesday", "18:00", end="19:00",
                             weeks=["first", "third", "fourth", "fifth"], note="Holy Hour"),
             "leaning": True},
            {"label": "Every Tuesday",
             "entry": _entry(SJ, "adoration", "Tuesday", "18:00", end="19:00",
                             note="Holy Hour")},
            {"label": "Leave out", "entry": None},
        ],
        "answer": None,
    })
    names = {"NEW": new["content_hash"], "OLD": old["content_hash"]}
    for slot in slots:
        for source in slot["sources"]:
            source["bulletin"] = names[source["bulletin"]]
    seed["slots"] = slots
    return seed


# ── Building it ─────────────────────────────────────────────────────────────
def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_demo(root: Path) -> dict[str, Path]:
    """(Re)build the demo dataset under `root`, keeping any labels already there."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "labels").mkdir(exist_ok=True)
    _write_csv(root / "parishes.csv", PARISHES)
    _write_csv(root / "churches.csv", CHURCHES)
    store = CachedBlobStore(LocalBlobStore(root))
    classifier = GeminiClassifier()

    db_path = root / "parish_events.db"
    delete_db(db_path)
    conn = connect_db(db_path)
    try:
        migrate(conn)
        seed_reference_data(
            conn, parishes_csv=root / "parishes.csv", churches_csv=root / "churches.csv",
        )
        parish_ids = {r["slug"]: r["id"] for r in conn.execute("SELECT id, slug FROM parish")}

        def add(parish: str, pdf: bytes, url: str, fetched_at: str) -> tuple[int, str]:
            content_hash = sha256(pdf).hexdigest()
            store.put(bulletin_pdf_key(parish, content_hash), pdf)
            bulletin_id = insert_bulletin(
                conn, parish_id=parish_ids[parish], source_url=url,
                content_hash=content_hash, fetched_at=fetched_at,
            )
            return bulletin_id, content_hash

        def cache(parish: str, version: str, content_hash: str, payload: dict) -> None:
            churches = church_list_for_prompt(conn, parish_ids[parish])
            key = cache_key(classifier.name, version, content_hash, churches)
            store.put(key, (json.dumps(payload, indent=2) + "\n").encode("utf-8"))

        def processed(bulletin_id: int, rows: list[dict], published: str, at: str) -> None:
            save_processed_bulletin(conn, bulletin_id, rows, processed_at=at,
                                    published_date=published)

        old_id, old_hash = add("holy-family-demo", HOLY_FAMILY_SEP20,
                        "https://example.org/holy-family/bulletins/2026-09-20.pdf",
                        "2026-09-18T21:00:00Z")
        processed(old_id, HOLY_FAMILY_SEP20_ROWS, "2026-09-20", "2026-09-18T21:05:00Z")

        new_url = "https://example.org/holy-family/bulletins/2026-09-27.pdf"
        new_id, new_hash = add("holy-family-demo", HOLY_FAMILY_SEP27, new_url,
                               "2026-09-25T21:00:00Z")
        cache("holy-family-demo", classifier.version, new_hash, HOLY_FAMILY_GEMINI)
        processed(new_id, flatten_extracted_events({"source_url": new_url}, HOLY_FAMILY_GEMINI),
                  "2026-09-27", "2026-09-25T21:05:00Z")

        anne_id, anne_hash = add("st-anne-demo", ST_ANNE_SEP27,
                                 "https://example.org/st-anne/bulletin-2026-09-27.pdf",
                                 "2026-09-25T21:01:00Z")
        cache("st-anne-demo", OLD_CLASSIFIER_VERSION, anne_hash, ST_ANNE_GEMINI_OLD)
        conn.execute("UPDATE bulletin SET published_date = ? WHERE id = ?",
                     ("2026-09-27", anne_id))
        conn.commit()

        add("our-lady-demo", OUR_LADY_SEP27,
            "https://example.org/our-lady/2026-09-27.pdf", "2026-09-25T21:02:00Z")
    finally:
        conn.close()
    seeds_dir = root / "seeds"
    if read_seed("holy-family-demo", seeds_dir) is None:
        write_seed_file(demo_seed(
            {"content_hash": new_hash, "fetched_at": "2026-09-25T21:00:00Z",
             "published_date": "2026-09-27"},
            {"content_hash": old_hash, "fetched_at": "2026-09-18T21:00:00Z",
             "published_date": "2026-09-20"},
        ), seeds_dir)
    return {"root": root, "db_path": db_path, "labels_dir": root / "labels",
            "seeds_dir": seeds_dir}
