import pytest

from pdf_extract.dioceses import web


@pytest.mark.parametrize(
    "url",
    ["stmary.org", "https:/stmary.org", "javascript:void(0)", "mailto:office@stmary.org",
     "localhost:8080"],
)
def test_probe_url_calls_an_address_without_a_host_part_bad(monkeypatch, url: str) -> None:
    monkeypatch.setattr(web, "_resolves", lambda host: pytest.fail(f"looked up {host}"))
    assert web.probe_url(url)["verdict"] == "BAD-URL"


def test_probe_url_looks_up_the_host_of_a_full_address(monkeypatch) -> None:
    looked_up: list[str] = []
    monkeypatch.setattr(web, "_resolves", lambda host: looked_up.append(host) or False)
    assert web.probe_url("https://www.StMary.org/bulletins")["verdict"] == "DEAD-DNS"
    assert looked_up[0] == "www.stmary.org"
