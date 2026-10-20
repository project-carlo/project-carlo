"""Choosing this week's bulletin among the PDFs a parish site lists."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

# A bulletin dated within this many days of today is taken as the current one.
CURRENT_WINDOW_DAYS = 7
# A bulletin dated further than this from today is an archive's, not the
# current one: a fallback page's pick that old is refused, and a first-listed
# PDF that old gives way to a recent one listed after it.
FALLBACK_MAX_AGE_DAYS = 45
# Recent dated PDFs that make a page's list a series of issues, so that an
# undated, unlabelled one listed first is something else.
MIN_RECENT_SERIES = 2


@dataclass(frozen=True)
class Candidate:
    """A PDF a parish site offers, and what its link says about it."""

    source_url: str
    fetch_url: str
    parsed_date: date | None
    # "bulletin" appears in the link's text or address.
    labelled: bool = False
    # The link's whole text names the bulletin ("Bulletin", "Weekly Bulletin").
    titled_bulletin: bool = False
    # ...and says it is this week's ("This Week's Bulletin", "Current Bulletin").
    titled_current: bool = False


# Why a candidate was chosen, most to least sure. Every reason but CURRENT
# means the site did not plainly date this week's issue.
CURRENT = "current"  # dated within CURRENT_WINDOW_DAYS of today
NEWEST_RECENT = "newest-recent"  # the first listed was old; the newest recent one
TITLED = "titled"  # undated, but its link is titled "Bulletin"
FIRST_LISTED = "first-listed"  # the first PDF the page lists
ONLY_LINK = "only-link"  # the bulletin link itself was the PDF


@dataclass(frozen=True)
class Choice:
    candidate: Candidate
    reason: str


class OldBulletinOnly(ValueError):
    """The only bulletin a page offers is older than the caller accepts."""


def is_current(parsed_date: date | None, reference_date: date) -> bool:
    return (
        parsed_date is not None
        and abs((parsed_date - reference_date).days) <= CURRENT_WINDOW_DAYS
    )


def is_convincing(candidates: list[Candidate], reference_date: date) -> bool:
    """Whether any candidate is plainly a bulletin: labelled one, or dated this week."""
    return any(c.labelled or is_current(c.parsed_date, reference_date) for c in candidates)


def _age_days(candidate: Candidate, reference_date: date) -> int:
    return (reference_date - (candidate.parsed_date or reference_date)).days


def choose(
    candidates: list[Candidate], *, reference_date: date, max_age_days: int | None = None,
) -> Choice:
    """The newest bulletin dated within a week of today, else a fallback.

    With none that current, the first one listed, except:
    - if it is plainly old (dated over FALLBACK_MAX_AGE_DAYS ago), the newest
      dated within that, when one is listed: a listing oldest first (St.
      Joseph, Troy) or a parish a few weeks behind;
    - a link whose whole text is "Bulletin" beats a first one that is not
      dated (St. Mary's, Glens Falls lists a Confirmation PDF first), and one
      titled "This Week's Bulletin" beats a bare "Bulletin" (St. Ignatius,
      Orrtanna's site header links a 2018 issue as "Bulletin");
    - a first one neither dated nor labelled "bulletin" gives way to the
      newest recent one when the page lists a dated series of them (Our Lady
      of Peace, Hazleton lists a "Parish Consolidation" PDF above its weekly
      issues, which can be a week or two late).
    With `max_age_days`, a pick dated further than that from today is refused
    with OldBulletinOnly.
    """
    current = [c for c in candidates if is_current(c.parsed_date, reference_date)]
    if current:
        return Choice(max(current, key=lambda c: c.parsed_date or date.min), CURRENT)

    first = candidates[0]
    recent = [
        c for c in candidates
        if c.parsed_date is not None
        and -CURRENT_WINDOW_DAYS <= _age_days(c, reference_date) <= FALLBACK_MAX_AGE_DAYS
    ]

    def newest_recent() -> Choice:
        return Choice(max(recent, key=lambda c: c.parsed_date or date.min), NEWEST_RECENT)

    if first.parsed_date is not None and _age_days(first, reference_date) > FALLBACK_MAX_AGE_DAYS:
        if recent:
            return newest_recent()
    reason = FIRST_LISTED
    if first.parsed_date is None:
        titled = next((c for c in candidates if c.titled_current), None) or next(
            (c for c in candidates if c.titled_bulletin), None
        )
        if titled is not None:
            first, reason = titled, TITLED
        elif not first.labelled and len(recent) >= MIN_RECENT_SERIES:
            return newest_recent()
    if (
        max_age_days is not None
        and first.parsed_date is not None
        and abs((reference_date - first.parsed_date).days) > max_age_days
    ):
        raise OldBulletinOnly(
            f"Only PDF found is dated {first.parsed_date.isoformat()}: {first.source_url}"
        )
    return Choice(first, reason)
