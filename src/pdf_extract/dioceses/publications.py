"""Shared content-evidence rules and conservative publisher recipe separation."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

from pdf_extract.fetch import PROVIDERS_TAKING_RECIPE
from pdf_extract.parish_sites import Recipe

_CONTENT = re.compile(
    r"\b(serves|serving|published by|bulletin (?:for|of))\b", re.I,
)
_MEMBER_DETAIL = re.compile(
    r"\b(names?|lists?|includes?|identifies|shows?)\b",
    re.I,
)
# Within one sentence: "running head 310, not Holy Family's 308. Checked 2026-10-27"
# observed both. Abbreviations ("St.", "Msgr.") don't end a sentence.
_IN_SENTENCE = r"(?:[^.;!?]|\b(?:St|Sts|Ste|Mt|Rev|Msgr|Fr|Sr|Dr|No|Nos|p|pp)\.)"
_NOT_OBSERVED = re.compile(
    rf"\b(?:not|never|haven't|hasn't|didn't|without)\b{_IN_SENTENCE}{{0,60}}"
    r"\b(?:read|inspect\w*|check\w*|observ\w*|compar\w*)\b|"
    r"\b(?:unread|uninspected|unchecked|unverified)\b|"
    r"\b(?:need(?:s)? to|must|will|should|plan to)\b.{0,40}"
    r"\b(?:read|inspect|check|observe|compare)\b",
    re.I,
)


def _http_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
        return parsed.scheme.lower() in {"http", "https"} and bool(parsed.hostname)
    except ValueError:
        return False


REVIEW_WORDING = ("a dated http(s) url and a note of 5+ words on whose bulletin it is: "
                  "'serves …', 'published by …', 'bulletin for …', or 'masthead' with "
                  "'names/lists/includes/shows …'")


def review_gap(review: Mapping[str, Any]) -> str | None:
    """Why `supported_review` turns this review down, or None when it doesn't.

    The gap is the first evidence item's, since every item fails.
    """
    evidence_items = review.get("evidence")
    if not isinstance(evidence_items, list):
        return "no evidence list"
    gaps = []
    for evidence in evidence_items:
        if not isinstance(evidence, Mapping):
            continue
        text = " ".join(str(evidence.get(k) or "") for k in ("quote", "note"))
        if not (_http_url(str(evidence.get("url") or "")) and evidence.get("seen")):
            gaps.append("no http(s) url with a seen date")
            continue
        if len(text.split()) < 5:
            gaps.append("quote and note under 5 words")
            continue
        if _NOT_OBSERVED.search(text):
            gaps.append("it reads as not yet observed ('not … checked', 'need to read')")
            continue
        content = _CONTENT.search(text) or (
            re.search(r"\b(mastheads?|members?|membership)\b", text, re.I)
            and _MEMBER_DETAIL.search(text)
        )
        # Calling ID differences "separate bulletins" is still only ID evidence.
        if (re.search(r"\b(ids?|identifiers?|urls?|accounts?|containers?)\b", text, re.I)
                and not re.search(r"\b(mastheads?|members?|membership|serves|serving|"
                                  r"published|publishes|coverage)\b", text, re.I)):
            gaps.append("only ids, urls or accounts differ")
            continue
        if not content:
            gaps.append("it doesn't say whose bulletin it is")
            continue
        return None
    return gaps[0] if gaps else "no evidence items"


def supported_review(review: Mapping[str, Any]) -> bool:
    """Require a content explanation, not just URL/account differences.

    This is a conservative evidence gate, not automatic masthead analysis.
    Keep unsupported reviews in the output so a person can improve them.
    """
    return review_gap(review) is None


def separate_recipes(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    """Prove filename sets disjoint from incompatible literal glob prefixes.

    Merely different patterns (Anne*.pdf and *.pdf) are insufficient. Uncertain
    patterns remain blocked; content-supported peer review is also required by
    the caller. Accounts and unconstrained homepage discovery are not selectors.
    """
    prefixes = []
    for row in (left, right):
        if row.get("bulletin_provider") not in PROVIDERS_TAKING_RECIPE:
            return False
        try:
            recipe = Recipe.parse(str(row.get("provider_id") or ""),
                                  website=str(row.get("website") or ""))
        except ValueError:
            return False
        if recipe.collector not in {"page-pdfs", "page-images"} or not recipe.filename:
            return False
        prefix = re.split(r"[*?\[]", recipe.filename.casefold(), maxsplit=1)[0]
        if not prefix:
            return False
        prefixes.append(prefix)
    a, b = prefixes
    return not (a.startswith(b) or b.startswith(a))
