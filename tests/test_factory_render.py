"""Golden tests for the worker-facing text the factory builds in code (`render.py`).

Each case renders one piece (a stage's first message from a fixture Run, the handoff
schema, the resume prompts) and compares it with `tests/golden/factory/<case>.md`. After
an intended change to that text, rewrite the files and review their diff:

    UPDATE_GOLDENS=1 uv run pytest tests/test_factory_render.py

The stage prompt files (`factory/prompts/*.md`) and specs aren't covered: a fixed spec
stands in for the real one, so a prompt or spec edit shows up once in its PR.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

import pytest

from pdf_extract.factory import render
from pdf_extract.factory.config import FactoryError
from pdf_extract.factory.ledger import MAP, SEED, Ledger
from pdf_extract.factory.quota import fingerprint
from pdf_extract.factory.stages import STAGES, StageSpec, load_stage

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = Path(__file__).parent / "golden" / "factory"
UPDATE = bool(os.environ.get("UPDATE_GOLDENS"))
D = "testd"

META = """\
---
name: Diocese of Testd
---
## Sources

### Bulletin publishers here

- Parishes Online prints most bulletins.

## New lessons

- Solutio /file links answer 403; use the parish page.
- St. Clare's bulletin moved to Discover Mass in 2026.

## Rules settled for this diocese

- Campus Masses are left out.

## Seeding precedents

- Is a summer-only Mass weekly? → Leave it out. Seasonal. (st-ann s2; 004-seed-review, 2026-10-01)

## Log
"""
ROSTER = {"name": "directory", "entries": [
    {"id": "1", "name": "St. Ann", "city": "Dover", "state": "DE"},
    {"id": "2", "name": "St. Bede", "city": "Dover"},
    {"id": "3", "name": "St. Clare"},
]}
BATCHES = {"version": 1, "diocese": D, "first_batch": "b2", "batches": [
    {"id": "b1", "name": "Dover", "why": "One town, two parishes that may share a bulletin.",
     "entries": ["directory:1", "directory:2"]},
    {"id": "b2", "name": "Lewes", "why": "A typical parish first.", "entries": ["directory:3"]},
]}
SPEC = StageSpec(stage="any", kind="agent",
                 writes=["data/dioceses/{diocese}/**", "scratch/{run}/{job}/**"],
                 gates=["pnpm --silent diocese check {diocese}"])


def check(case: str, text: str) -> None:
    path = GOLDEN / f"{case}.md"
    if UPDATE:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return
    assert path.exists(), f"no golden for {case}: run with UPDATE_GOLDENS=1"
    assert text == path.read_text(encoding="utf-8"), (
        f"{case} changed; if intended, rewrite with UPDATE_GOLDENS=1 and review the diff")


class Fixture:
    """A map Run partway through, and a seed Run, with what each stage's input reads."""

    def __init__(self, tmp: Path) -> None:
        self.ledger = Ledger(tmp / "ledger.db")
        self.map = self.ledger.run(self.ledger.add_run(
            diocese=D, kind=MAP, worktrees_dir=tmp / "wt", notes="Start with the cathedral."))
        self.seed = self.ledger.run(self.ledger.add_run(diocese=D, kind=SEED,
                                                        worktrees_dir=tmp / "wt"))
        for run in (self.map, self.seed):
            folder = Path(run["worktree"]) / "data" / "dioceses" / D
            (folder / "rosters").mkdir(parents=True)
            (folder / "diocese.md").write_text(META, encoding="utf-8")
            (folder / "rosters" / "directory.json").write_text(json.dumps(ROSTER))
            (folder / "batches.json").write_text(json.dumps(BATCHES))
        run_id = self.map["id"]
        survey = self.add(self.map, "survey", {})
        first_review = self.add(self.map, "survey-review", {"survey_job": survey})
        self.verdict(first_review, survey, D, "send_back", ["Split b1 by town.",
                                                             "Give b2 a reason."])
        self.add(self.map, "survey-review", {"survey_job": survey})
        b2 = self.add(self.map, "map", {"batch": "b2"})
        self.ledger.run_sql("INSERT INTO lead (run_id, job_id, touches, note) VALUES "
                            "(?,?,?,?)", run_id, b2, "b1", "St. Ann may share St. Bede's")
        self.ledger.run_sql("INSERT INTO lead (run_id, job_id, touches, note) VALUES "
                            "(?,?,?,?)", run_id, b2, "directory:2", "St. Bede has a new site")
        self.ledger.run_sql("INSERT INTO lead (run_id, job_id, touches, note) VALUES "
                            "(?,?,?,?)", run_id, b2, "b9", "A lead no batch takes")
        self.ledger.add_flag(run_id, b2, severity="advisory", scope="parish",
                             subject="st-clare", question="Merge the chapel into St. Clare?",
                             suggestion="Merge it")
        self.ledger.add_flag(run_id, b2, severity="advisory", scope="parish",
                             subject="st-ann", question="Two mastheads?")
        self.ledger.add_flag(run_id, b2, severity="blocking", scope="parish",
                             subject="directory:9", question="Is St. Zita open?")
        self.add(self.map, "map", {"batch": "b1"})
        self.add(self.map, "integrate", {})
        self.add(self.map, "reconcile", {})
        self.add(self.map, "map", {"batch": "b1", "entries": ["directory:2"],
                                   "answer": "Yes, it shares St. Ann's bulletin.",
                                   "question": "Does St. Bede share a bulletin?",
                                   "subject": "directory:2", "flag": 3})
        seed_id = self.seed["id"]
        drafted = self.add(self.seed, "seed", {"parish": "st-ann", "batch": "b1"})
        review = self.add(self.seed, "seed-review", {"batch": "b1", "parishes": ["st-ann"]})
        self.verdict(review, drafted, "st-ann", "send_back", ["Slot s1 has no source.",
                                                               "Check the 9:00."])
        self.add(self.seed, "seed-review", {"batch": "b1", "parishes": ["st-ann", "st-bede"],
                                            "redrafted": ["st-ann"]})
        assert seed_id

    def add(self, run: Any, stage: str, data: dict[str, Any]) -> int:
        return self.ledger.add_job(run["id"], stage, data)

    def verdict(self, job: int, reviewed: int, subject: str, verdict: str,
                problems: list[str]) -> None:
        self.ledger.run_sql("INSERT INTO verdict (job_id, reviewed_job, subject, verdict, "
                            "problems, at) VALUES (?,?,?,?,?,?)", job, reviewed, subject,
                            verdict, json.dumps(problems), "2026-10-01T00:00:00+00:00")

    def job(self, run: Any, name: str) -> Any:
        return self.ledger.one("SELECT * FROM job WHERE run_id = ? AND name = ?", run["id"], name)


def values(run: Any, job: Any) -> dict[str, str]:
    data = json.loads(job["input"])
    return {"diocese": run["diocese"], "run": run["id"], "job": job["name"],
            "branch": run["branch"], "parish": data.get("parish", ""),
            "parishes": " ".join(data.get("parishes") or []), "approved": ""}


@pytest.fixture
def fx(tmp_path: Path) -> Fixture:
    return Fixture(tmp_path)


CASES = [("map", "001-survey"), ("map", "003-survey-review"), ("map", "004-map"),
         ("map", "005-map"), ("map", "006-integrate"), ("map", "007-reconcile"),
         ("map", "008-map"), ("seed", "001-seed"), ("seed", "003-seed-review")]


@pytest.mark.parametrize(("kind", "name"), CASES)
def test_first_message(fx: Fixture, kind: str, name: str) -> None:
    run = fx.map if kind == "map" else fx.seed
    job = fx.job(run, name)
    check(f"input-{name}", render.job_input(fx.ledger, run, job, SPEC, values(run, job)))


@pytest.mark.parametrize("stage", [s for s in STAGES if s not in ("promote", "pr")])
def test_handoff_schema(stage: str) -> None:
    check(f"schema-{stage}", render.schema_text(stage) + "\n")


def test_resume_prompts() -> None:
    rel = "scratch/testd-map-1/004-map/handoff.json"
    check("prompts", "\n\n---\n\n".join([
        render.send_back_prompt(["`pnpm diocese check testd` failed", "No handoff"], rel),
        render.continue_prompt(rel),
        render.resume_prompt(rel),
        render.answer_prompt("Is St. Zita open?", "Closed in 2025.", rel, "directory:9"),
    ]) + "\n")


# ── Reads, sizes and the context fingerprint ────────────────────────────────
README = """\
# Dioceses

Intro.

## Fields

- `name`: the parish's name.

### Dates

Use ISO dates.

## Traps

Don't guess.
"""


def test_a_read_is_a_whole_file_or_one_section() -> None:
    def text_of(path: str) -> str | None:
        return README if path == "data/dioceses/README.md" else None

    assert render.read_entry(text_of, "data/dioceses/README.md") == README
    assert render.read_entry(text_of, "data/dioceses/README.md#Fields") == (
        "## Fields\n\n- `name`: the parish's name.\n\n### Dates\n\nUse ISO dates.\n")
    assert render.read_entry(text_of, "data/dioceses/README.md#Dates") == (
        "### Dates\n\nUse ISO dates.\n")
    with pytest.raises(FactoryError, match="no heading 'Method'"):
        render.read_entry(text_of, "data/dioceses/README.md#Method")
    with pytest.raises(FactoryError, match="no file"):
        render.read_entry(text_of, "data/missing.md")
    spec = StageSpec(stage="map", kind="agent", prompt="p.md", skills=["s"],
                     reads=["data/dioceses/README.md#Traps", "data/dioceses/README.md#Method"])
    parts = render.given(spec, "first", lambda p: {"p.md": "---\nx: 1\n---\nDo it.",
                                                    "data/dioceses/README.md": README}.get(p))
    assert [(p["part"], p["chars"], p["missing"]) for p in parts] == [
        ("system prompt", 6, False), ("first message", 5, False), ("skill", 0, True),
        ("read", len("## Traps\n\nDon't guess.\n"), False), ("read", 0, True)]
    assert "no heading" in parts[-1]["error"]


def test_every_stage_reads_files_that_exist_on_main() -> None:
    for stage in STAGES:
        spec = load_stage(stage, ROOT)
        for entry in spec.reads:
            render.read_entry(render.worktree_text(ROOT), entry)
        for name in spec.skills:
            assert (ROOT / render.skill_path(name)).exists(), f"{stage}: no skill {name}"


def test_context_hashes_change_with_a_skill_or_a_read(tmp_path: Path) -> None:
    skill = tmp_path / ".claude" / "skills" / "s"
    (skill / "scripts").mkdir(parents=True)
    (skill / "SKILL.md").write_text("Method.")
    (skill / "scripts" / "go.py").write_text("print(1)")
    (tmp_path / "README.md").write_text(README)
    spec = StageSpec(stage="map", kind="agent", skills=["s"], reads=["README.md#Traps"])
    before = render.context_hashes(tmp_path, spec)
    (skill / "scripts" / "__pycache__").mkdir()
    (skill / "scripts" / "__pycache__" / "go.cpython-313.pyc").write_bytes(b"x")
    assert render.context_hashes(tmp_path, spec) == before  # running a script changes nothing
    (skill / "scripts" / "go.py").write_text("print(2)")
    changed = render.context_hashes(tmp_path, spec)
    assert changed["skills"] != before["skills"] and changed["render"] == before["render"]
    (tmp_path / "README.md").write_text(README.replace("Don't guess.", "Never guess."))
    assert render.context_hashes(tmp_path, spec)["reads"] != changed["reads"]
    (tmp_path / "README.md").write_text(README.replace("Intro.", "Another intro."))
    assert render.context_hashes(tmp_path, spec)["reads"] == changed["reads"]  # not a read


def test_the_fingerprint_without_code_hashes_as_before() -> None:
    old = hashlib.sha256(json.dumps(["spec", "prompt", ["a", "b"]]).encode()).hexdigest()[:12]
    assert fingerprint("spec", "prompt", ["b", "a"]) == old  # backfilled attempts match
    code = {"render": "1", "skills": {}, "reads": {}, "dispatcher": "abc"}
    assert fingerprint("spec", "prompt", ["a", "b"], code) != old
    assert fingerprint("spec", "prompt", ["a", "b"], code | {"dispatcher": "def"}) != \
        fingerprint("spec", "prompt", ["a", "b"], code)
