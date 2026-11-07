"""What one tick did: the result every part of the dispatcher returns for a job."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Outcome:
    """What one tick did, for the log and the tests."""

    action: str  # idle | paused | waiting | ran | blocked
    detail: str = ""
    wait_until: datetime | None = None
