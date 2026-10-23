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
_NOT_OBSERVED = re.compile(
    r"\b(?:not|never|haven't|hasn't|didn't|without)\b.{0,60}"
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


def supported_review(review: Mapping[str, Any]) -> bool:
    """Require a content explanation, not just URL/account differences.

    This is a conservative evidence gate, not automatic masthead analysis.
    Keep unsupported reviews in the output so a person can improve them.
    """
    evidence_items = review.get("evidence")
    if not isinstance(evidence_items, list):
        return False
    for evidence in evidence_items:
        if not isinstance(evidence, Mapping):
            continue
        text = " ".join(str(evidence.get(k) or "") for k in ("quote", "note"))
        if _NOT_OBSERVED.search(text):
            continue
        content = _CONTENT.search(text) or (
            re.search(r"\b(mastheads?|members?|membership)\b", text, re.I)
            and _MEMBER_DETAIL.search(text)
        )
        # Calling ID differences "separate bulletins" is still only ID evidence.
        if (re.search(r"\b(ids?|identifiers?|urls?|accounts?|containers?)\b", text, re.I)
                and not re.search(r"\b(mastheads?|members?|membership|serves|serving|"
                                  r"published|publishes|coverage)\b", text, re.I)):
            content = False
        if (_http_url(str(evidence.get("url") or "")) and evidence.get("seen")
                and len(text.split()) >= 5 and content):
            return True
    return False


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
