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
from pdf_extract.dioceses.publications import supported_review
from pdf_extract.dioceses.records import PARISH, Diocese
from pdf_extract.fetch import PROVIDERS_TAKING_RECIPE
from pdf_extract.parish_sites import Recipe
from pdf_extract.parish_sites.links import document_download_url, is_pdf_url, unwrap_pdf_viewer_url

# An invocation has fixed, visible bounds; nothing is persisted between runs.
MAX_SITE_PROBES = 80
MAX_DOCUMENT_PROBES = 20
MAX_DOCUMENT_BYTES = 8_000_000

# Bulletin publishers' hosts: every parish they print is on them, so a host alone pairs
# every such row with every other. Their account ids (`publisher_account`) are the lead.
PUBLISHER_HOSTS = frozenset({
    "parishesonline.com", "container.parishesonline.com", "discovermass.com",
    "files.ecatholic.com", "jppc.net", "church-bulletin.org", "liturgicalpublications.com",
    "sponsors.bonventure.net", "bonventure.net", "e-churchbulletins.com",
    "cdn.diocesanweb.org",
})
# These hosts serve unrelated publishers. Tenant subdomains (ann.wordpress.com)
# remain useful; do not collapse them to their registrable domain.
GENERIC_HOSTS = PUBLISHER_HOSTS | frozenset({
    "ecatholic.com", "ecatholicchurches.com",
    "drive.google.com", "docs.google.com", "google.com", "storage.googleapis.com",
    "facebook.com", "m.facebook.com", "youtube.com", "youtu.be", "instagram.com",
    "wordpress.com", "weebly.com", "wixsite.com", "squarespace.com",
    "thebostonpilot.com", "s3.amazonaws.com", "nebula.wsimg.com", "uploads.weconnect.com",
})
_FAILED_SITES = frozenset({
    "BAD-URL", "DEAD-DNS", "UNREACHABLE", "PROXY-REFUSED", "HTTP4XX", "HTTP5XX", "SPAM-SQUAT",
})
# A publisher account in a URL on its host: Bon Venture's `?page=2141` and
# `/pdfs/2141/<date>.pdf`, John Patrick's `/onlinebulletins/<n>template.pdf`,
# church-bulletin.org's `?id=4047`, `/227`, `/<slug>` and `/bulletin/<slug>/<date>.pdf`.
_ACCOUNT_PATTERNS = {
    "bonventure.net": ("bonventure", r"(?:[?&]page=|^/pdfs/)(\d+)"),
    "jppc.net": ("jppc", r"^/onlinebulletins/(\d+)template"),
    "church-bulletin.org": ("church-bulletin",
                            r"[?&]id=(\d+)|^/(?:bulletin/)?(?!bulletin/?$)([a-z0-9][\w-]*)"),
}


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


def publisher_account(url: str) -> str:
    """The publisher account a URL on a bulletin publisher's host belongs to, or "".

    The same account on two rows is a lead, like a shared page. Two different accounts
    aren't a lead, but they don't prove separate bulletins either.
    """
    normalized = _url(url)
    if not normalized:
        return ""
    parts = urlsplit(normalized)
    host = (parts.hostname or "").rstrip(".").removeprefix("www.")
    domain = next((d for d in _ACCOUNT_PATTERNS if host == d or host.endswith(f".{d}")), "")
    if not domain:
        return ""
    name, pattern = _ACCOUNT_PATTERNS[domain]
    where = parts.path + (f"?{parts.query}" if parts.query else "")
    m = re.search(pattern, where, flags=re.IGNORECASE)
    value = next((g for g in m.groups() if g), "") if m else ""
    return f"{name}:{value.lower()}" if value else ""


def _publisher_host(url: str) -> str:
    host = (urlsplit(_url(url)).hostname or "").rstrip(".").removeprefix("www.")
    return host if host in PUBLISHER_HOSTS else ""


def _document(url: str) -> str:
    url = unwrap_pdf_viewer_url(url)
    return _url(document_download_url(url) or (url if is_pdf_url(url) else ""))


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
    publisher_hosts: dict[str, set[str]] = {}
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
            "A bulletin publisher's host (publisher_hosts) serves many parishes, so rows on "
            "it are paired only by a shared publisher account, page, document, id or group, "
            "never by the host alone; different accounts don't prove separate bulletins.",
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
            add("publisher account", publisher_account(url), slug)
            add("document URL", _document(url), slug)
            if (host := _publisher_host(url)):
                publisher_hosts.setdefault(host, set()).add(slug)
        for review in row.get("publication_reviews") or []:
            if not isinstance(review, Mapping):
                continue
            peer = review.get("parish")
            if peer not in rows or peer == slug:
                continue
            pair = tuple(sorted((slug, peer)))
            reviews.setdefault(pair, []).append({**review, "recorded_by": slug,
                                                 "content_supported": supported_review(review)})
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
    scope["publisher_hosts"] = {host: sorted(slugs) for host, slugs in sorted(
        publisher_hosts.items()) if len(slugs) > 1}
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
            add("publisher account", publisher_account(final), slug)
            document(final, slug)
        for pub in result.get("publications", []):
            # Same bucket as recorded IDs, so recorded/probed evidence can meet.
            add("publication", pub, slug)
        pages = []
        for link in result.get("bulletin_links", []):
            if not (link := _url(link)):
                continue
            add("publisher account", publisher_account(link), slug)
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
