"""Stage specs: `factory/stages/<stage>.yaml`, what a foreman review might change.

Read from the Run's worktree, so a job runs with the specs of the commit it records.
The order of stages is code (`plan`), not a spec.
"""

from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from pdf_extract.factory.config import STAGES_DIR, FactoryError

AGENT, REVIEWER, CODE = "agent", "reviewer", "code"
MAP_STAGES = ("survey", "survey-review", "map", "integrate", "reconcile", "promote", "pr")
SEED_STAGES = ("seed", "seed-review", "pr")
STAGES = tuple(dict.fromkeys(MAP_STAGES + SEED_STAGES))

_PLACEHOLDER = re.compile(r"\{(\w+)\}")


@dataclass(frozen=True)
class StageSpec:
    stage: str
    kind: str
    model: str | None = None
    effort: str | None = None
    prompt: str | None = None
    skills: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    writes: list[str] = field(default_factory=list)
    gates: list[str] = field(default_factory=list)
    # Files the worker reads first (`path` or `path#Heading`), and commands it may not run.
    # Unused until the prompt diet (docs/factory-refactor-plan.md, Phase 2); known now so a
    # spec that uses them loads in a dispatcher that hasn't restarted since.
    reads: list[str] = field(default_factory=list)
    deny: list[str] = field(default_factory=list)
    max_turns: int = 150
    max_minutes: int = 90

    @property
    def is_agent(self) -> bool:
        return self.kind in (AGENT, REVIEWER)


def load_stage(stage: str, root: Path) -> StageSpec:
    path = root / STAGES_DIR / f"{stage}.yaml"
    try:
        raw: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except OSError as exc:
        raise FactoryError(f"no stage spec for {stage}: {exc}") from None
    limits = raw.pop("limits", None) or {}
    if raw.get("stage") != stage:
        raise FactoryError(f"{path}: stage must be {stage!r}")
    if raw.get("kind") not in (AGENT, REVIEWER, CODE):
        raise FactoryError(f"{path}: kind must be agent, reviewer or code")
    try:
        return StageSpec(**raw, **{k: v for k, v in limits.items() if k in
                                   ("max_turns", "max_minutes")})
    except TypeError as exc:
        raise FactoryError(f"{path}: {exc}") from None


def fill(template: str, values: dict[str, str]) -> str:
    """`{diocese}` and the rest, from the job; an unknown name is an error in the spec."""
    def sub(m: re.Match[str]) -> str:
        if m.group(1) not in values:
            raise FactoryError(f"unknown placeholder {{{m.group(1)}}} in {template!r}")
        return values[m.group(1)]
    return _PLACEHOLDER.sub(sub, template)


def placeholders(template: str) -> set[str]:
    return set(_PLACEHOLDER.findall(template))


def in_scope(path: str, globs: list[str]) -> bool:
    """Whether a repo-relative path matches one of a stage's `writes` globs.

    `**` matches any depth, `*` one path segment.
    """
    return any(_glob_match(path, g) for g in globs)


def _glob_match(path: str, glob: str) -> bool:
    parts = glob.split("/")
    names = path.split("/")

    def match(i: int, j: int) -> bool:
        if i == len(parts):
            return j == len(names)
        if parts[i] == "**":
            return any(match(i + 1, k) for k in range(j, len(names) + 1))
        return j < len(names) and fnmatch.fnmatchcase(names[j], parts[i]) and match(i + 1, j + 1)

    return match(0, 0)
