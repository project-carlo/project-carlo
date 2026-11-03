import pytest

from pdf_extract.dioceses import web

PROXY_FOR = web.proxy_for


@pytest.fixture(autouse=True)
def no_proxy(monkeypatch):
    """Tests decide whether a proxy is in the way; the machine's environment doesn't."""
    monkeypatch.setattr(web, "proxy_for", lambda url: None)


@pytest.mark.parametrize(
    "url",
    ["https:/stmary.org", "javascript:void(0)", "mailto:office@stmary.org",
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


class FakeProxy:
    """Answers `proxy_lookup` like smokescreen: a lookup per host, by name."""

    def __init__(self, monkeypatch, answers):
        self.asked: list[tuple[str, int]] = []
        monkeypatch.setattr(web, "proxy_for", lambda url: "http://carlo-egress:4750")
        monkeypatch.setattr(web, "_resolves", lambda host: pytest.fail("local DNS was used"))

        def lookup(host, proxy, *, port=443, timeout=30):
            self.asked.append((host, port))
            return answers.get(host, web.ProxyLookup("ok"))

        monkeypatch.setattr(web, "proxy_lookup", lookup)


PAGE = (b"<html><title>St. Ann Parish</title>Mass times. <a href='https://www.jppc.net/"
        b"onlinebulletins/1234template.pdf'>Bulletin</a> wp-content/themes/x</html>")


def test_behind_a_proxy_probe_url_fetches_instead_of_resolving_locally(monkeypatch) -> None:
    proxy = FakeProxy(monkeypatch, {})
    monkeypatch.setattr(web, "fetch", lambda url, **kw: web.Response(url, 200, url,
                                                                      "text/html", PAGE))
    out = web.probe_url("https://stann.org/")
    assert out["verdict"] == "ok"
    assert out["publishers"] == {"jppc.net": 1} and out["platform"] == "wordpress"
    assert proxy.asked == []  # a site that answers needs no lookup


def test_behind_a_proxy_only_the_proxys_resolver_makes_a_host_dead(monkeypatch) -> None:
    nx = web.ProxyLookup("no-such-host", "Failed to resolve remote hostname: no such host")
    proxy = FakeProxy(monkeypatch, {"gone.org": nx, "www.gone.org": nx})
    monkeypatch.setattr(web, "fetch", lambda url, **kw: web.Response(
        url, error="OSError: Tunnel connection failed: 502 Bad gateway"))
    out = web.probe_url("https://gone.org/")
    assert out["verdict"] == "DEAD-DNS" and "egress proxy's resolver" in out["detail"]
    assert proxy.asked == [("gone.org", 443)] * 2 + [("www.gone.org", 443)] * 2


def test_behind_a_proxy_www_is_tried_when_the_bare_host_does_not_exist(monkeypatch) -> None:
    nx = web.ProxyLookup("no-such-host", "no such host")
    FakeProxy(monkeypatch, {"stann.org": nx})
    monkeypatch.setattr(web, "fetch", lambda url, **kw: (
        web.Response(url, 200, url, "text/html", PAGE) if "www." in url
        else web.Response(url, error="OSError: Tunnel connection failed: 502 Bad gateway")))
    out = web.probe_url("http://stann.org/")
    assert out["verdict"] == "ok" and out["url_tried"] == "http://www.stann.org/"


@pytest.mark.parametrize("state, verdict", [
    ("refused", "PROXY-REFUSED"), ("failed", "UNREACHABLE"),
    ("proxy-unreachable", "UNREACHABLE"), ("ok", "UNREACHABLE"),
])
def test_behind_a_proxy_a_failure_of_the_proxy_is_never_dead(monkeypatch, state, verdict):
    FakeProxy(monkeypatch, {"stann.org": web.ProxyLookup(state, "why")})
    monkeypatch.setattr(web, "fetch", lambda url, **kw: web.Response(url, error="timed out"))
    out = web.probe_url("https://stann.org/")
    assert out["verdict"] == verdict
    if state in ("failed", "proxy-unreachable"):
        assert web.PROXY_NOTES[state] in out["detail"]


def test_a_proxy_refusal_of_an_http_url_is_not_the_sites_status(monkeypatch) -> None:
    from email.message import Message
    from urllib.error import HTTPError

    headers = Message()
    headers[web.PROXY_ERROR_HEADER] = "Failed to resolve remote hostname: no such host"

    def refuse(request, timeout):
        raise HTTPError(request.full_url, 502, "Bad gateway", headers, None)

    monkeypatch.setattr(web, "urlopen", refuse)
    resp = web.fetch("http://gone.org/")
    assert resp.status is None and resp.error.startswith("egress proxy: Failed to resolve")


class _Proxy:
    """A one-shot TCP server that replies to CONNECT with a canned response."""

    def __init__(self, reply: bytes):
        import socket
        import threading

        self.server = socket.socket()
        self.server.bind(("127.0.0.1", 0))
        self.server.listen(1)
        self.url = f"http://127.0.0.1:{self.server.getsockname()[1]}"
        self.request = b""

        def serve():
            conn, _ = self.server.accept()
            with conn:
                while b"\r\n\r\n" not in self.request:
                    self.request += conn.recv(1024)
                conn.sendall(reply)

        threading.Thread(target=serve, daemon=True).start()


@pytest.mark.parametrize("reply, state", [
    (b"HTTP/1.0 200 OK\r\n\r\n", "ok"),
    (b"HTTP/1.1 502 Bad gateway\r\nX-Smokescreen-Error: Failed to resolve remote hostname: "
     b"lookup gone.org on 169.254.1.1:53: no such host\r\n\r\n", "no-such-host"),
    (b"HTTP/1.1 502 Bad gateway\r\nX-Smokescreen-Error: Failed to resolve remote hostname: "
     b"lookup gone.org: server misbehaving\r\n\r\n", "failed"),
    (b"HTTP/1.1 407 Request rejected by proxy\r\nX-Smokescreen-Error: Egress proxying is "
     b"denied to host 'gone.org:443'\r\n\r\n", "refused"),
    (b"garbage\r\n\r\n", "proxy-unreachable"),
])
def test_proxy_lookup_reads_smokescreens_reply(reply: bytes, state: str) -> None:
    proxy = _Proxy(reply)
    lookup = web.proxy_lookup("gone.org", proxy.url, timeout=5)
    assert lookup.state == state
    assert proxy.request.startswith(b"CONNECT gone.org:443 HTTP/1.1\r\n")


def test_proxy_for_follows_the_proxy_environment(monkeypatch) -> None:
    for name in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "NO_PROXY",
                 "no_proxy", "ALL_PROXY", "all_proxy"):
        monkeypatch.delenv(name, raising=False)
    assert PROXY_FOR("https://stann.org/") is None
    monkeypatch.setenv("HTTPS_PROXY", "http://carlo-egress:4750")
    monkeypatch.setenv("NO_PROXY", "localhost")
    assert PROXY_FOR("https://stann.org/") == "http://carlo-egress:4750"
    assert PROXY_FOR("https://localhost/") is None
    assert PROXY_FOR("http://stann.org/") is None  # no HTTP_PROXY


def test_probe_get_explains_a_failed_tunnel(monkeypatch) -> None:
    FakeProxy(monkeypatch, {"gone.org": web.ProxyLookup("no-such-host", "no such host")})
    monkeypatch.setattr(web, "fetch", lambda url, **kw: web.Response(
        url, error="OSError: Tunnel connection failed: 502 Bad gateway"))
    note = web.get("https://gone.org/")["note"]
    assert note.startswith(web.PROXY_NOTES["no-such-host"])
