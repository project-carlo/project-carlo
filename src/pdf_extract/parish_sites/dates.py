"""Reading a bulletin's date from a link's text or address.

Parish sites name each issue in every way people write a date: "September 27,
2026", "Sept. 27", "9-27-26", "20260927.pdf", "september-27-twenty-sixth-sunday".
"""

from __future__ import annotations

import re
from datetime import date, datetime

# A date without a year ("March 28", "12-28") is taken as the nearest such day,
# but no further ahead than the coming Sunday: "October 4" read on 27 September
# is in an archive of last year's bulletins, not next week's.
YEARLESS_MAX_DAYS_AHEAD = 6


# A folder named by the year alone ("/bulletins/2025/September_28.pdf"), not a
# WordPress upload folder ("/2025/12/..."), whose year is the upload's.
_PATH_YEAR_RE = re.compile(r"/(20\d{2})/(?!\d{1,2}/)")


# Ids that hosts put in addresses, which can hold what reads as a date ("e2-4a"
# in a Wix host's UUID): a UUID, or a long run of hex digits.
_HEX_ID_RE = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    r"|(?<![0-9a-z])[0-9a-f]{16,}(?![0-9a-z])"
)


# When a WordPress file was uploaded, not the issue's date: in
# "uploads/2026/10/10-04-2026-1.pdf" it would read as 10 October.
_WORDPRESS_UPLOAD_FOLDER_RE = re.compile(r"/uploads/20\d{2}/\d{2}/")


# Stands in for an ordinal's suffix ("4th" reads "4º") once it is stripped.
_ORDINAL = "º"


def parse_date_from_texts(texts: list[str], reference_date: date) -> date | None:
    """The first date in texts; a yearless one takes its year from a year folder in them."""
    year = next(
        (int(m.group(1)) for text in texts if (m := _PATH_YEAR_RE.search(text or ""))), None,
    )
    for text in texts:
        parsed = parse_date(text, reference_date, year=year)
        if parsed is not None:
            return parsed
    return None


def parse_date(
    text: str, reference_date: date, *, year: int | None = None,
) -> date | None:
    """A date in text. One without a year is `year`'s if given, else the nearest."""
    if not text:
        return None

    def yearless(month: int, day: int) -> date | None:
        if year is not None:
            return safe_date(year, month, day)
        return _resolve_yearless_date(month=month, day=day, reference_date=reference_date)

    normalized = _WORDPRESS_UPLOAD_FOLDER_RE.sub("/", _HEX_ID_RE.sub(" ", text.lower()))
    # An ordinal is a day, never a month or a year: "Oct.-4th-27th-Sun" is 4
    # October in the 27th week, not 27 April. Mark where one was.
    normalized = re.sub(r"(\d+)(st|nd|rd|th)", rf"\1{_ORDINAL}", normalized)
    normalized = normalized.replace(",", " ")
    normalized = re.sub(r"\s+", " ", normalized).strip()

    month_name = (
        r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|"
        r"jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t)?(?:ember)?|"
        r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?"
    )
    # A day is never part of a longer number ("October 2026" is not October 20).
    # A weekend can be named by both its days before the year ("September 26 &
    # 27, 2026", "Oct-4-5-2025"); the year is still the issue's.
    month_day_pattern = re.compile(
        rf"(?P<month>{month_name})\s+(?P<day>\d{{1,2}})(?!\d){_ORDINAL}?"
        rf"(?:\s*(?:&|and|-|\s)\s*\d{{1,2}}{_ORDINAL}?(?=\s+\d{{4}}(?!\d)))?"
        rf"(?:\s+(?P<year>\d{{2,4}})(?![\d{_ORDINAL}]))?",
        flags=re.IGNORECASE,
    )
    day_month_pattern = re.compile(
        rf"(?<!\d)(?P<day>\d{{1,2}}){_ORDINAL}?\s+(?P<month>{month_name})"
        rf"(?:\s+(?P<year>\d{{2,4}})(?![\d{_ORDINAL}]))?",
        flags=re.IGNORECASE,
    )

    for pattern in (month_day_pattern, day_month_pattern):
        for match in pattern.finditer(normalized):
            month_num = _month_name_to_number(match.group("month"))
            if month_num is None:
                continue
            day = int(match.group("day"))
            raw_year = match.group("year")
            if raw_year:
                parsed = safe_date(_normalize_year(raw_year, reference_date), month_num, day)
            else:
                parsed = yearless(month_num, day)
            if parsed is not None:
                return parsed

    # Not the tail of a longer number: Weebly's "/38133239/02-12-2017" is no year 3239.
    for match in re.finditer(
        r"(?<!\d)(?P<year>\d{4})[-/.](?P<month>\d{1,2})[-/.](?P<day>\d{1,2})(?!\d)", normalized,
    ):
        parsed = safe_date(int(match.group("year")), int(match.group("month")), int(match.group("day")))
        if parsed is not None:
            return parsed

    for match in re.finditer(
        r"(?<!\d)(?P<a>\d{1,2})[-/.](?P<b>\d{1,2})[-/.](?P<c>\d{2,4})(?!\d)", normalized,
    ):
        parsed = safe_date(
            _normalize_year(match.group("c"), reference_date),
            int(match.group("a")), int(match.group("b")),
        )
        if parsed is not None:
            return parsed

    # Not a run of numbered folders either: Weebly's "/uploads/1/3/1/4/" is no 3 January.
    for match in re.finditer(
        r"(?<!\d)(?<!\d[-/.])(?P<a>\d{1,2})[-/.](?P<b>\d{1,2})(?!\d)(?![-/.]\d)", normalized,
    ):
        parsed = yearless(int(match.group("a")), int(match.group("b")))
        if parsed is not None:
            return parsed

    # File names often carry the Sunday as one run of digits: "20260927.pdf",
    # "20260927B.pdf". Only this century's years, so ids and timestamps don't
    # read as dates.
    for match in re.finditer(r"(?<!\d)(20\d{2})(\d{2})(\d{2})(?!\d)", normalized):
        parsed = safe_date(*(int(part) for part in match.groups()))
        if parsed is not None:
            return parsed

    # Slugs and file names join words with hyphens or underscores
    # ("september-27-twenty-sixth-sunday", "Bulletin_Sept_27_2026.pdf"), and
    # abbreviations end in a period ("Sept. 27"), where the month-name
    # patterns above need a space.
    words_split = re.sub(r"[-_]+|(?<=[a-z])\.", " ", normalized)
    if words_split != normalized:
        return parse_date(words_split, reference_date, year=year)
    return None


def _month_name_to_number(month_name: str) -> int | None:
    month_lookup = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "sept": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }
    return month_lookup.get(month_name.lower())


def _normalize_year(raw_year: str | None, reference_date: date) -> int:
    if not raw_year:
        return reference_date.year
    year = int(raw_year)
    if len(raw_year) == 2:
        year = 2000 + year
    return year


def _resolve_yearless_date(*, month: int, day: int, reference_date: date) -> date | None:
    candidates = [
        safe_date(reference_date.year - 1, month, day),
        safe_date(reference_date.year, month, day),
        safe_date(reference_date.year + 1, month, day),
    ]
    valid = [d for d in candidates if d is not None]
    if not valid:
        return None
    not_too_far_ahead = [
        d for d in valid if (d - reference_date).days <= YEARLESS_MAX_DAYS_AHEAD
    ]
    return min(not_too_far_ahead or valid, key=lambda d: abs((d - reference_date).days))


def safe_date(year: int, month: int, day: int) -> date | None:
    try:
        return datetime(year, month, day).date()
    except ValueError:
        return None
