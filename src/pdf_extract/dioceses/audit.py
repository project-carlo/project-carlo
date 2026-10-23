"""Duplicate-publication leads, with explicit limits and no automatic merges.

Publication IDs, provider accounts, pages and even identical documents are
discovery evidence. Only a recorded review explaining the publication's
masthead or membership settles whether two rows share a bulletin.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable, Mapping
from itertools import combinations
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from pdf_extract.dioceses import records, web
from pdf_extract.dioceses.records import PARISH, Diocese
from pdf_extract.fetch import PROVIDERS_TAKING_RECIPE
from pdf_extract.parish_sites import Recipe
from pdf_extract.parish_sites.links import document_download_url, is_pdf_url, unwrap_pdf_viewer_url

# An invocation has fixed, visible bounds; nothing is persisted between runs.
MAX_SITE_PROBES = 80
MAX_DOCUMENT_PROBES = 20
MAX_DOCUMENT_BYTES = 8_000_000

# These hosts serve unrelated publishers. Tenant subdomains (ann.wordpress.com)
# remain useful; do not collapse them to their registrable domain.
GENERIC_HOSTS = frozenset({
    "parishesonline.com", "container.parishesonline.com", "discovermass.com",
    "files.ecatholic.com", "ecatholic.com", "ecatholicchurches.com",
    "drive.google.com", "docs.google.com", "google.com", "storage.googleapis.com",
    "facebook.com", "m.facebook.com", "youtube.com", "youtu.be", "instagram.com",
    "wordpress.com", "weebly.com", "wixsite.com", "squarespace.com",
    "jppc.net", "church-bulletin.org", "thebostonpilot.com", "s3.amazonaws.com",
    "nebula.wsimg.com", "uploads.weconnect.com", "liturgicalpublications.com",
})
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
_FAILED_SITES = frozenset({
    "BAD-URL", "DEAD-DNS", "UNREACHABLE", "HTTP4XX", "HTTP5XX", "SPAM-SQUAT",
})


def _url(value: str) -> str:
    """Canonical HTTP address, preserving paths, queries and transport identity."""
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
            return ""
        return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(),
                           parsed.path or "/", parsed.query, ""))
    except ValueError:
        return ""


def _host(url: str) -> str:
    normalized = _url(url)
    if not normalized:
        return ""
    host = (urlsplit(normalized).hostname or "").rstrip(".").removeprefix("www.")
    return "" if host in GENERIC_HOSTS else host


def _document(url: str) -> str:
    url = unwrap_pdf_viewer_url(url)
    return _url(document_download_url(url) or (url if is_pdf_url(url) else ""))


def _supported(review: Mapping[str, Any]) -> bool:
    """Require a content explanation, not just URL/account differences.

    This is a conservative evidence gate, not automatic masthead analysis.
    Keep unsupported reviews in the output so a person can improve them.
    """
    for evidence in review.get("evidence") or []:
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
        if (_url(str(evidence.get("url") or "")) and evidence.get("seen")
                and len(text.split()) >= 5 and content):
            return True
    return False


def _verdict(status: str) -> str:
    return {
        "separate": "separate bulletins: content-supported review recorded",
        "shared": "shared bulletin: content-supported review recorded; inspect before merging",
        "unresolved": "unknown: candidate remains unresolved; read mastheads and member coverage",
    }[status]


def audit_rows(d: Diocese, groups: Mapping[str, set[str]], *, fetch: bool = False
               ) -> dict[str, Any]:
    """Audit all active readable parish rows, retaining the report's group fields.

    `candidate_pairs` is the deduplicated list to review. Groups explain how
    pairs were discovered and can overlap. `scope` reports rows and bounded
    probe coverage, including failures and work skipped offline or at a limit.
    """
    all_rows = d.of(PARISH)
    rows = {s: r for s, r in sorted(all_rows.items())
            if r.get("bulletin_provider") != records.NO_BULLETIN}
    buckets = {label: set(slugs) & rows.keys() for label, slugs in groups.items()}
    sources: dict[str, list[str]] = {}
    recipes: dict[str, Recipe] = {}
    reviews: dict[tuple[str, str], list[dict[str, Any]]] = {}
    row_output = {s: {"parish": s, "website": r.get("website", ""),
                      "publication": list(r.get("publication") or [])} for s, r in rows.items()}
    scope: dict[str, Any] = {
        "mode": "fetch" if fetch else "offline", "rows_total": len(all_rows),
        "rows_considered": len(rows), "considered_parishes": list(rows),
        "rows_skipped": [{"parish": s, "reason": "no_bulletin"}
                         for s in sorted(all_rows.keys() - rows.keys())],
        "unreadable_records": list(d.unreadable),
        "possible_pairs": len(rows) * (len(rows) - 1) // 2,
        "site_probes": {"limit": MAX_SITE_PROBES, "fetched": 0, "skipped": [], "errors": []},
        "document_probes": {"limit": MAX_DOCUMENT_PROBES, "fetched": 0,
                            "max_bytes": MAX_DOCUMENT_BYTES, "skipped": [], "errors": []},
        "limitations": [
            "Candidates follow recorded or probed evidence; absence of a candidate is not "
            "proof of separate publications.",
            "Matching URLs, accounts and document hashes are leads; differing values do not "
            "prove separate bulletins. Only content-supported recorded reviews settle pairs.",
            "Site probes read HTML, follow at most one bulletin page per row, and compare "
            "at most one document per row; they do not render JavaScript or walk archives.",
        ],
    }

    def add(kind: str, value: str, slug: str) -> None:
        if value:
            buckets.setdefault(f"{kind}: {value}", set()).add(slug)

    for slug, row in rows.items():
        urls = [str(row.get("website") or "")]
        for publication in row.get("publication") or []:
            add("publication", str(publication), slug)
            if str(publication).startswith("url:"):
                urls.append(str(publication)[4:])
        provider, provider_id = row.get("bulletin_provider"), str(row.get("provider_id") or "")
        if provider_id and provider in PROVIDERS_TAKING_RECIPE:
            try:
                recipe = Recipe.parse(provider_id, website=urls[0])
                recipes[slug] = recipe
                if recipe.page:
                    urls.append(recipe.page)
                    if page := _url(recipe.page):
                        add("recipe", f"{recipe.collector or '*'} {page} "
                            f"filename={recipe.filename or '*'}", slug)
            except ValueError as exc:
                row_output[slug]["recipe_error"] = str(exc)
        elif provider_id:
            add("provider/account", f"{provider}:{provider_id.strip()}", slug)
        sources[slug] = list(dict.fromkeys(u for url in urls if (u := _url(url))))
        for url in dict.fromkeys(urls):
            if url and not _url(url):
                scope["site_probes"]["skipped"].append(
                    {"parish": slug, "url": url, "reason": "not a valid HTTP source"})
        if not sources[slug]:
            scope["site_probes"]["skipped"].append(
                {"parish": slug, "reason": "no valid HTTP source recorded"})
        for url in sources[slug]:
            add("host", _host(url), slug)
            add("document URL", _document(url), slug)
        for review in row.get("publication_reviews") or []:
            if not isinstance(review, Mapping):
                continue
            peer = review.get("parish")
            if peer not in rows or peer == slug:
                continue
            pair = tuple(sorted((slug, peer)))
            reviews.setdefault(pair, []).append({**review, "recorded_by": slug,
                                                 "content_supported": _supported(review)})
            add("review", " / ".join(pair), slug)
            add("review", " / ".join(pair), peer)

    if fetch:
        _probe(rows, sources, recipes, row_output, scope, add)
    else:
        scope["site_probes"]["skipped"].extend([
            {"url": url, "reason": "offline"} for url in sorted(
                {u for urls in sources.values() for u in urls if not _document(u)})
        ])
        recorded_docs = {_document(u) for urls in sources.values() for u in urls} - {""}
        scope["document_probes"]["skipped"] = [
            {"url": url, "reason": "offline"} for url in sorted(recorded_docs)
        ]

    pair_reasons: dict[tuple[str, str], list[str]] = {}
    for label, slugs in sorted(buckets.items()):
        for pair in combinations(sorted(slugs), 2):
            pair_reasons.setdefault(pair, []).append(label)
    pairs = {}
    for pair, reasons in sorted(pair_reasons.items()):
        pair_reviews = reviews.get(pair, [])
        decisions = {r["decision"] for r in pair_reviews if r["content_supported"]
                     and r.get("decision") in {"shared", "separate"}}
        status = next(iter(decisions)) if len(decisions) == 1 else "unresolved"
        explanation = []
        if len(decisions) > 1:
            explanation.append("Conflicting content-supported reviews; resolve them by hand.")
        if any(not r["content_supported"] for r in pair_reviews):
            explanation.append("A recorded review lacks a masthead/member explanation.")
        if status == "unresolved":
            explanation.append("Recorded IDs and fetched locations/content cannot settle this pair.")
        pairs[pair] = {"parishes": list(pair), "status": status, "verdict": _verdict(status),
                       "reasons": reasons, "reviews": pair_reviews, "notes": explanation}

    out_groups = []
    for label, slugs in sorted(buckets.items()):
        if len(slugs) < 2:
            continue
        members = sorted(slugs)
        statuses = {pairs[pair]["status"] for pair in combinations(members, 2)}
        status = next(iter(statuses)) if len(statuses) == 1 else "unresolved"
        group = {"group": label, "status": status, "verdict": _verdict(status),
                 "rows": [row_output[s] for s in members],
                 "candidate_pairs": [list(p) for p in combinations(members, 2)]}
        # Retain the existing embedded-publication lead field for consumers.
        seen: dict[str, list[str]] = {}
        for slug in members:
            for pub in row_output[slug].get("found_on_site", []):
                seen.setdefault(pub, []).append(slug)
        if shared := {pub: owners for pub, owners in seen.items() if len(owners) > 1}:
            group["lead"] = shared
        out_groups.append(group)
    scope["candidate_pairs"] = len(pairs)
    return {
        "diocese": d.slug, "scope": scope, "candidate_pairs": list(pairs.values()),
        "groups_spanning_rows": out_groups,
        "needs_a_look": [g["group"] for g in out_groups if g["status"] != "separate"],
        "parishes_without_publication_id": [s for s, r in rows.items() if not r.get("publication")],
    }


def _probe(rows: Mapping[str, Mapping[str, Any]], sources: Mapping[str, list[str]],
           recipes: Mapping[str, Recipe], row_output: dict[str, dict[str, Any]],
           scope: dict[str, Any], add: Callable[[str, str, str], None]) -> None:
    """One invocation's site and document results, shared across overlapping leads."""
    sites: dict[str, dict[str, Any]] = {}
    site_scope, doc_scope = scope["site_probes"], scope["document_probes"]
    documents: dict[str, set[str]] = {}

    def document(url: str, slug: str) -> bool:
        doc = _document(url)
        if not doc:
            return False
        add("document URL", doc, slug)
        documents.setdefault(doc, set()).add(slug)
        return True

    def probe(urls: list[str]) -> None:
        pending = [u for u in dict.fromkeys(urls) if u not in sites]
        remaining = max(0, MAX_SITE_PROBES - site_scope["fetched"])
        for url in pending[remaining:]:
            sites[url] = {"url": url, "error": "site probe limit reached", "skipped": True}
            site_scope["skipped"].append({"url": url, "reason": "site probe limit reached"})
        targets = pending[:remaining]
        if not targets:
            return
        site_scope["fetched"] += len(targets)
        try:
            found = {_url(p["url"]): p for p in web.probe_urls(targets)}
        except Exception as exc:  # noqa: BLE001 - audit uncertainty survives probe failures
            found = {u: {"url": u, "error": str(exc)} for u in targets}
        for url in targets:
            result = found.get(url) or {"url": url, "error": "probe returned no result"}
            sites[url] = result
            if result.get("error") or result.get("verdict") in _FAILED_SITES:
                site_scope["errors"].append({"url": url, "error": result.get("error")
                                              or result.get("detail") or result["verdict"]})

    # Interleave each row's sources so large dioceses get broad homepage coverage.
    initial = []
    for index in range(max((len(urls) for urls in sources.values()), default=0)):
        for slug, urls in sources.items():
            if index < len(urls) and not document(urls[index], slug):
                initial.append(urls[index])
    probe(initial)

    def consume(slug: str, url: str) -> list[str]:
        result = sites[url]
        row_output[slug].setdefault("site_probes", []).append(result)
        if url == _url(str(rows[slug].get("website") or "")):
            row_output[slug]["found_on_site"] = result.get("publications", [])
            row_output[slug]["site_verdict"] = result.get("verdict")
        if (result.get("error") or result.get("skipped")
                or result.get("verdict") in _FAILED_SITES):
            return []
        if final := _url(result.get("final_url") or ""):
            add("host", _host(final), slug)
            document(final, slug)
        for pub in result.get("publications", []):
            # Same bucket as recorded IDs, so recorded/probed evidence can meet.
            add("publication", pub, slug)
        pages = []
        for link in result.get("bulletin_links", []):
            if not (link := _url(link)):
                continue
            if not document(link, slug):
                pages.append(link)
        return pages

    follow: dict[str, str] = {}
    for slug, urls in sources.items():
        pages = [link for url in urls if url in sites for link in consume(slug, url)]
        if next_page := next((p for p in pages if p not in urls), None):
            follow[slug] = next_page
    probe(list(follow.values()))
    for slug, url in follow.items():
        consume(slug, url)

    # Record every exact link lead, but compare only one document per row.
    selected: set[str] = set()
    for slug in rows:
        eligible = [url for url, owners in documents.items() if slug in owners
                    and (slug not in recipes or recipes[slug].matches(url))]
        if eligible:
            selected.add(eligible[0])
    fetched = 0
    for url, owners in documents.items():
        if url not in selected or fetched >= MAX_DOCUMENT_PROBES:
            doc_scope["skipped"].append({"url": url, "reason": "document probe limit reached"
                                         if url in selected else "one document per row"})
            continue
        fetched += 1
        doc_scope["fetched"] = fetched
        try:
            response = web.fetch(url, timeout=10, max_bytes=MAX_DOCUMENT_BYTES)
            if not response.ok:
                raise ValueError(response.error or f"HTTP {response.status}")
            if response.truncated:
                raise ValueError("document exceeds byte limit; content not compared")
            if not response.body.startswith(b"%PDF-"):
                raise ValueError("response is not a PDF; content not compared")
            digest = hashlib.sha256(response.body).hexdigest()
            final = _url(response.final_url or url)
            for slug in sorted(owners):
                add("document URL", final, slug)
                add("resolved document URL", final, slug)
                add("document sha256", digest, slug)
                row_output[slug].setdefault("documents", []).append(
                    {"url": url, "final_url": final, "sha256": digest, "bytes": len(response.body)})
        except Exception as exc:  # noqa: BLE001 - never turn a fetch failure into a verdict
            doc_scope["errors"].append({"url": url, "error": str(exc)})
