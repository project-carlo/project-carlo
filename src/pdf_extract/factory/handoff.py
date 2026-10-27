"""The handoff: the JSON a worker writes at the end of its job (docs/factory-spec.md §4).

`scratch/<run>/<job>/handoff.json`, about 300 tokens. Reviewers add their verdicts. The
dispatcher takes the changed paths from git, never from the handoff.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

DONE, PARTIAL, BLOCKED = "done", "partial", "blocked"
BLOCKING, ADVISORY = "blocking", "advisory"
APPROVE, SEND_BACK = "approve", "send_back"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Flag(_Strict):
    severity: Literal["blocking", "advisory"]
    scope: Literal["parish", "run"]
    subject: str = Field(min_length=1)  # roster:id or parish slug; the Run's name for scope run
    question: str = Field(min_length=1)
    evidence: list[str] = []
    suggestion: str = ""


class Lead(_Strict):
    touches: str = Field(min_length=1)  # a batch id or roster:id
    note: str = Field(min_length=1)


class Handoff(_Strict):
    status: Literal["done", "partial", "blocked"]
    summary: str = Field(min_length=1)
    flags: list[Flag] = []
    leads: list[Lead] = []
    lessons: list[str] = []

    @field_validator("lessons")
    @classmethod
    def _no_blank_lessons(cls, v: list[str]) -> list[str]:
        if any(not s.strip() for s in v):
            raise ValueError("a lesson must not be empty")
        return v


class SurveyReview(Handoff):
    verdict: Literal["approve", "send_back"]
    problems: list[str] = []
    rules: list[str] = []  # proposed rules it accepts, as written


class SeedAnswer(_Strict):
    slot: str = Field(min_length=1)  # the slot id; one slot of a group answers the group
    question: str = ""
    choice: int | Literal["dropped", "edited"]
    entry: dict | None = None  # the entry, for `edited`
    page: int | None = None
    basis: Literal["precedent", "judgment"]
    why: str = Field(min_length=1)


class SeedVerdict(_Strict):
    parish: str = Field(min_length=1)
    verdict: Literal["approve", "send_back"]
    answers: list[SeedAnswer] = []
    problems: list[str] = []


class SeedReview(Handoff):
    seeds: list[SeedVerdict]


MODELS: dict[str, type[Handoff]] = {"survey-review": SurveyReview, "seed-review": SeedReview}


def handoff_path(worktree: Path, run: str, job: str) -> Path:
    return worktree / "scratch" / run / job / "handoff.json"


def read_handoff(path: Path, stage: str) -> tuple[Handoff | None, list[str]]:
    """The handoff, or the problems a worker is sent back with."""
    if not path.exists():
        return None, [f"no handoff: write {path.as_posix()} before you finish"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, [f"the handoff is not valid JSON: {exc}"]
    model = MODELS.get(stage, Handoff)
    try:
        handoff = model.model_validate(data)
    except ValidationError as exc:
        return None, [
            f"handoff {'.'.join(str(p) for p in e['loc']) or '(top)'}: {e['msg']}"
            for e in exc.errors()
        ]
    problems = []
    if handoff.status == BLOCKED and not any(f.severity == BLOCKING for f in handoff.flags):
        problems.append("status blocked needs a blocking flag saying what must be decided")
    if isinstance(handoff, SurveyReview) and handoff.verdict == SEND_BACK and not handoff.problems:
        problems.append("a send_back verdict lists the problems to fix")
    if isinstance(handoff, SeedReview):
        for v in handoff.seeds:
            if v.verdict == SEND_BACK and not v.problems:
                problems.append(f"seeds[{v.parish}]: a send_back lists the problems to fix")
            for a in v.answers:
                if a.choice == "edited" and not a.entry:
                    problems.append(f"seeds[{v.parish}] slot {a.slot}: edited needs an entry")
    return (None, problems) if problems else (handoff, [])


def schema_text(stage: str) -> str:
    """The handoff format, as the job input shows it to a worker."""
    base = {
        "status": "done | partial | blocked",
        "summary": "one or two sentences",
        "flags": [{
            "severity": "blocking | advisory", "scope": "parish | run",
            "subject": "roster:id or parish slug", "question": "what needs deciding",
            "evidence": ["path#section or URL with date"],
            "suggestion": "what you would do",
        }],
        "leads": [{"touches": "batch id or roster:id", "note": "..."}],
        "lessons": ["reusable publisher or rule lesson"],
    }
    if stage == "survey-review":
        base |= {"verdict": "approve | send_back", "problems": ["..."],
                 "rules": ["each proposed rule you accept, as written"]}
    if stage == "seed-review":
        base |= {"seeds": [{
            "parish": "slug", "verdict": "approve | send_back",
            "answers": [{"slot": "slot id", "question": "...",
                         "choice": "option index | dropped | edited",
                         "entry": "only for edited", "basis": "precedent | judgment",
                         "why": "..."}],
            "problems": ["..."],
        }]}
    return json.dumps(base, indent=1)
