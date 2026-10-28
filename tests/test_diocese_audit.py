"""Publication audit tests use recorded rows and fake probes; no network is needed."""

from __future__ import annotations

from collections import Counter

import pytest

from pdf_extract.dioceses import audit, records, report, web


@pytest.fixture
def dataset(monkeypatch):
    def load(rows, *, churches=None):
        d = records.Diocese("test", {"parish": {
            slug: {"slug": slug, "website": f"https://{slug}.org", "bulletin_provider": "other",
                   **row} for slug, row in rows.items()
        }, "church": churches or {}})
        monkeypatch.setattr(records, "load", lambda _: d)
        monkeypatch.setattr(report, "_aliases", lambda _: {})
        monkeypatch.setattr(report, "roster_names", lambda _: [])
        return d

    return load


def review(peer="b", decision="separate", text=None):
    return {"parish": peer, "decision": decision, "evidence": [{
        "url": "https://family.org/bulletin.pdf", "seen": "2026-10-20",
        "note": text or "Ann's masthead lists Ann alone; Bede's masthead lists Bede alone.",
    }]}


def pair(result):
    assert len(result["candidate_pairs"]) == 1
    return result["candidate_pairs"][0]


def successful_probe(url, *, links=(), publications=(), **extra):
    return {"url": url, "verdict": "ok", "bulletin_links": list(links),
            "publications": list(publications), **extra}


def pdf(url, body=b"%PDF-1.7\nexample bulletin", **extra):
    return web.Response(url, 200, url, "application/pdf", body, **extra)


def test_different_url_ids_on_shared_host_are_candidates_offline(dataset, monkeypatch):
    dataset({
        "a": {"website": "https://WWW.Family.org/ann", "publication": ["url:https://family.org/a"]},
        "b": {"website": "http://family.org/bede", "publication": ["url:https://family.org/b"]},
    })
    monkeypatch.setattr(web, "probe_urls", lambda _: pytest.fail("offline audit fetched sites"))
    monkeypatch.setattr(web, "fetch", lambda *a, **k: pytest.fail("offline audit fetched PDF"))
    result = report.audit("test")
    candidate = pair(result)
    assert candidate["parishes"] == ["a", "b"]
    assert candidate["status"] == "unresolved"
    assert "host: family.org" in candidate["reasons"]
    assert result["needs_a_look"]
    assert result["scope"]["rows_considered"] == 2
    assert result["scope"]["candidate_pairs"] == 1
    assert result["scope"]["site_probes"]["fetched"] == 0
    assert all(p["reason"] == "offline" for p in result["scope"]["site_probes"]["skipped"])


@pytest.mark.parametrize("host", ["files.ecatholic.com", "drive.google.com", "facebook.com",
                                  "parishesonline.com", "container.parishesonline.com"])
def test_generic_host_alone_does_not_create_candidates(dataset, host):
    dataset({"a": {"website": f"https://{host}/ann"},
             "b": {"website": f"https://www.{host}/bede"}})
    assert report.audit("test")["candidate_pairs"] == []


def test_tenant_subdomains_are_kept_distinct(dataset):
    dataset({"a": {"website": "https://ann.wordpress.com/"},
             "b": {"website": "https://bede.wordpress.com/"},
             "c": {"website": "https://ann.wordpress.com/bulletins"}})
    assert pair(report.audit("test"))["parishes"] == ["a", "c"]


@pytest.mark.parametrize("fields,reason", [
    ({"publication": ["ecatholic:1234"]}, "publication: ecatholic:1234"),
    ({"bulletin_provider": "parishes_online", "provider_id": "family"},
     "provider/account: parishes_online:family"),
    ({"provider_id": "page-pdfs https://family.org/bulletins"},
     "recipe: page-pdfs https://family.org/bulletins filename=*"),
])
def test_ungrouped_recorded_publication_account_and_recipe_leads(dataset, fields, reason):
    dataset({"a": fields, "b": fields})
    candidate = pair(report.audit("test"))
    assert reason in candidate["reasons"]
    assert candidate["status"] == "unresolved"


def test_collector_name_without_shared_page_is_not_a_shared_recipe(dataset):
    dataset({"a": {"provider_id": "page-pdfs"}, "b": {"provider_id": "page-pdfs"}})
    assert report.audit("test")["candidate_pairs"] == []


def test_roster_group_still_discovers_pairs(dataset, monkeypatch):
    dataset({"a": {}, "b": {}}, churches={
        "ann": {"parish": "a", "roster": ["official:ann"]},
        "bede": {"parish": "b", "roster": ["official:bede"]},
    })
    monkeypatch.setattr(report, "roster_names", lambda _: ["official"])
    monkeypatch.setattr(report, "load_roster", lambda *a: {"entries": [
        {"id": "ann", "group": "Family 1"}, {"id": "bede", "group": "Family 1"},
    ]})
    assert pair(report.audit("test"))["reasons"] == ["official: Family 1"]


@pytest.mark.parametrize("decision", ["separate", "shared"])
def test_content_supported_review_settles_offline_and_keeps_evidence(dataset, decision):
    evidence = review(decision=decision, text=(
        "The masthead names Ann and Bede as members of this shared bulletin."
        if decision == "shared" else None))
    dataset({"a": {"publication_reviews": [evidence]}, "b": {}})
    result = report.audit("test")
    candidate = pair(result)
    assert candidate["status"] == decision
    assert candidate["reviews"][0]["evidence"] == evidence["evidence"]
    assert candidate["reviews"][0]["content_supported"]
    assert bool(result["needs_a_look"]) == (decision == "shared")


@pytest.mark.parametrize("text", [
    "Different native publication IDs and URL locations are recorded.",
    "Different native publication IDs establish separate bulletins.",
    "Different URL identifiers for each parish's bulletin; mastheads were not inspected.",
    "Both mastheads are unread, but each parish has its own bulletin URL.",
    "We need to inspect the mastheads to see which members each one lists.",
])
def test_url_and_native_id_differences_do_not_support_a_separate_review(dataset, text):
    dataset({"a": {"publication_reviews": [review(text=text)]}, "b": {}})
    candidate = pair(report.audit("test"))
    assert candidate["status"] == "unresolved"
    assert not candidate["reviews"][0]["content_supported"]


@pytest.mark.parametrize("text", [
    # Wilmington: a "not" in one sentence and "Checked" in the next were read as unobserved.
    "Running head '310', not Holy Family's 308. Checked 2026-10-27: each masthead names its "
    "own parish only.",
    "Ann's masthead names St. Ann alone, not St. Bede; St. Bede's lists Bede alone.",
])
def test_negation_in_another_sentence_does_not_unsay_an_observed_review(dataset, text):
    dataset({"a": {"publication_reviews": [review(text=text)]}, "b": {}})
    assert pair(report.audit("test"))["reviews"][0]["content_supported"]


@pytest.mark.parametrize("text,gap", [
    ("Different native publication IDs establish separate bulletins.", "only ids"),
    ("Own masthead, Mass schedule and intentions.", "whose bulletin"),
    ("The masthead names St. Ann but was not yet checked against St. Bede's.",
     "not yet observed"),
    ("Masthead names Ann.", "under 5 words"),
])
def test_review_gap_says_why_a_review_is_turned_down(text, gap):
    from pdf_extract.dioceses.publications import review_gap

    assert gap in review_gap(review(text=text))
    assert review_gap(review()) is None


def test_conflicting_reviews_remain_unresolved(dataset):
    dataset({"a": {"publication_reviews": [review()]},
             "b": {"publication_reviews": [review("a", "shared", text=(
                 "The masthead names both Ann and Bede on one shared bulletin."))]}})
    candidate = pair(report.audit("test"))
    assert candidate["status"] == "unresolved"
    assert "Conflicting" in candidate["notes"][0]


def test_review_can_explain_publication_membership_without_masthead_keyword(dataset):
    dataset({"a": {"publication_reviews": [review(decision="shared", text=(
        "The publisher's membership list includes both Ann and Bede."))]}, "b": {}})
    assert pair(report.audit("test"))["status"] == "shared"


def test_one_review_does_not_settle_other_members_of_a_group(dataset):
    dataset({"a": {"group": "Family", "publication_reviews": [review()]},
             "b": {"group": "Family"}, "c": {"group": "Family"}})
    result = report.audit("test")
    group = next(g for g in result["groups_spanning_rows"] if g["group"] == "group: Family")
    assert group["status"] == "unresolved"
    assert sum(p["status"] == "separate" for p in result["candidate_pairs"]) == 1


def test_fetch_does_not_skip_different_url_ids_and_reuses_shared_document(dataset, monkeypatch):
    dataset({
        "a": {"website": "https://family.org/ann", "publication": ["url:https://family.org/ann"]},
        "b": {"website": "https://family.org/bede", "publication": ["url:https://family.org/bede"]},
    })
    site_calls, downloads = [], []
    doc = "https://family.org/weekly.pdf"

    def probes(urls):
        site_calls.extend(urls)
        return [successful_probe(u, links=[doc], publications=["ecatholic:1234"]) for u in urls]

    def fetch(url, **kwargs):
        downloads.append(url)
        return pdf(url)

    monkeypatch.setattr(web, "probe_urls", probes)
    monkeypatch.setattr(web, "fetch", fetch)
    result = report.audit("test", fetch=True)
    candidate = pair(result)
    assert Counter(site_calls) == Counter({"https://family.org/ann": 1,
                                           "https://family.org/bede": 1})
    assert downloads == [doc]
    assert candidate["status"] == "unresolved"
    assert f"document URL: {doc}" in candidate["reasons"]
    assert any(r.startswith("document sha256:") for r in candidate["reasons"])
    group = next(g for g in result["groups_spanning_rows"] if g["group"] == "host: family.org")
    assert group["lead"] == {"ecatholic:1234": ["a", "b"]}
    assert all(r["found_on_site"] == ["ecatholic:1234"] for r in group["rows"])
    assert result["scope"]["document_probes"]["fetched"] == 1


def test_equal_document_bytes_create_lead_across_unrelated_sites(dataset, monkeypatch):
    dataset({"a": {}, "b": {}})
    monkeypatch.setattr(web, "probe_urls", lambda urls: [
        successful_probe(u, links=[u + "weekly.pdf"]) for u in urls])
    monkeypatch.setattr(web, "fetch", lambda u, **kw: pdf(u))
    result = report.audit("test", fetch=True)
    candidate = pair(result)
    assert candidate["status"] == "unresolved"
    assert len(candidate["reasons"]) == 1
    assert candidate["reasons"][0].startswith("document sha256:")


def test_different_document_bytes_and_urls_never_prove_separate(dataset, monkeypatch):
    dataset({"a": {"group": "Family"}, "b": {"group": "Family"}})
    monkeypatch.setattr(web, "probe_urls", lambda urls: [
        successful_probe(u, links=[u + "weekly.pdf"]) for u in urls])
    monkeypatch.setattr(web, "fetch", lambda u, **kw: pdf(u, b"%PDF-" + u.encode()))
    result = report.audit("test", fetch=True)
    assert pair(result)["status"] == "unresolved"
    assert result["scope"]["document_probes"]["fetched"] == 2


def test_followed_pages_and_resolved_document_urls_create_leads(dataset, monkeypatch):
    dataset({"a": {}, "b": {}})
    site_calls = []

    def probes(urls):
        site_calls.extend(urls)
        return [successful_probe(u, links=[u + ("issue.pdf" if "bulletins" in u
                                                else "bulletins/")]) for u in urls]

    monkeypatch.setattr(web, "probe_urls", probes)
    monkeypatch.setattr(web, "fetch", lambda u, **kw: web.Response(
        u, 200, "https://cdn.example.org/latest.pdf", "application/pdf", b"%PDF-" + u.encode()))
    candidate = pair(report.audit("test", fetch=True))
    assert "resolved document URL: https://cdn.example.org/latest.pdf" in candidate["reasons"]
    assert len(site_calls) == len(set(site_calls)) == 4
    assert candidate["status"] == "unresolved"


def test_failed_sites_and_documents_report_errors_without_settling_candidates(dataset, monkeypatch):
    dataset({"a": {"group": "Family"}, "b": {"group": "Family"}})
    monkeypatch.setattr(web, "probe_urls", lambda urls: [
        {"url": u, "verdict": "UNREACHABLE", "detail": "timeout"} if u == "https://a.org/"
        else successful_probe(u, links=["https://b.org/issue.pdf"]) for u in urls])
    monkeypatch.setattr(web, "fetch", lambda u, **kw: web.Response(u, error="timeout"))
    result = report.audit("test", fetch=True)
    assert pair(result)["status"] == "unresolved"
    assert result["scope"]["site_probes"]["errors"] == [
        {"url": "https://a.org/", "error": "timeout"}]
    assert result["scope"]["document_probes"]["errors"] == [
        {"url": "https://b.org/issue.pdf", "error": "timeout"}]


def test_probe_exception_is_reported_as_unresolved(dataset, monkeypatch):
    dataset({"a": {"group": "Family"}, "b": {"group": "Family"}})

    def fail(urls):
        raise OSError("network unavailable")

    monkeypatch.setattr(web, "probe_urls", fail)
    result = report.audit("test", fetch=True)
    assert pair(result)["status"] == "unresolved"
    assert len(result["scope"]["site_probes"]["errors"]) == 2


@pytest.mark.parametrize("response", [
    web.Response("", 200, body=b"<html>blocked</html>", content_type="text/html"),
    web.Response("", 200, body=b"%PDF-incomplete", truncated=True),
])
def test_failed_pdf_content_is_never_hashed(dataset, monkeypatch, response):
    dataset({"a": {"website": "https://a.org/issue.pdf"},
             "b": {"website": "https://b.org/issue.pdf"}})
    monkeypatch.setattr(web, "fetch", lambda *a, **kw: response)
    result = report.audit("test", fetch=True)
    assert not result["candidate_pairs"]
    assert len(result["scope"]["document_probes"]["errors"]) == 2


def test_scope_reports_probe_limits_excluded_and_unreadable_rows(dataset, monkeypatch):
    d = dataset({"a": {"group": "Family"}, "b": {"group": "Family"},
                 "c": {"group": "Family", "bulletin_provider": "no_bulletin"}})
    d.unreadable.append("parishes/broken.md: invalid YAML")
    monkeypatch.setattr(audit, "MAX_SITE_PROBES", 1)
    monkeypatch.setattr(audit, "MAX_DOCUMENT_PROBES", 0)
    monkeypatch.setattr(web, "probe_urls", lambda urls: [
        successful_probe(u, links=[u + "issue.pdf"]) for u in urls])
    result = report.audit("test", fetch=True)
    scope = result["scope"]
    assert scope["rows_total"] == 3
    assert scope["rows_considered"] == 2
    assert scope["rows_skipped"] == [{"parish": "c", "reason": "no_bulletin"}]
    assert scope["unreadable_records"] == d.unreadable
    assert scope["site_probes"]["fetched"] == 1
    assert scope["site_probes"]["skipped"] == [
        {"url": "https://b.org/", "reason": "site probe limit reached"}]
    assert scope["document_probes"]["fetched"] == 0
    assert scope["document_probes"]["skipped"] == [
        {"url": "https://a.org/issue.pdf", "reason": "document probe limit reached"}]
    assert pair(result)["status"] == "unresolved"


def test_results_are_not_cached_between_invocations(dataset, monkeypatch):
    dataset({"a": {}, "b": {}})
    calls = []

    def probes(urls):
        calls.extend(urls)
        return [successful_probe(u, links=["https://family.org/issue.pdf"]) for u in urls]

    monkeypatch.setattr(web, "probe_urls", probes)
    monkeypatch.setattr(web, "fetch", lambda u, **kw: pdf(u))
    report.audit("test", fetch=True)
    report.audit("test", fetch=True)
    assert Counter(calls) == Counter({"https://a.org/": 2, "https://b.org/": 2})


def test_scope_explains_rows_without_valid_probe_sources(dataset, monkeypatch):
    dataset({"a": {"website": "", "provider_id": "page-pdfs"},
             "b": {"website": "mailto:office@b.org", "provider_id": "page-pdfs"}})
    monkeypatch.setattr(web, "probe_urls", lambda _: pytest.fail("no HTTP sources to fetch"))
    result = report.audit("test", fetch=True)
    assert result["candidate_pairs"] == []
    assert result["scope"]["rows_considered"] == 2
    assert result["scope"]["site_probes"]["fetched"] == 0
    assert {p["parish"] for p in result["scope"]["site_probes"]["skipped"]} == {"a", "b"}
