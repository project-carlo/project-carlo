"""Shared Playwright browser launcher and page/anchor Protocol types."""

from __future__ import annotations

import logging
import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Protocol
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

LOGGER = logging.getLogger(__name__)

# Playwright waits for a matching selector to appear on a page before we scrape
# anchor hrefs from it.
PLAYWRIGHT_SELECTOR_TIMEOUT_MS = 15000
# Short delay between retries when Playwright aborts a navigation because the
# page initiated another one while we were waiting.
PLAYWRIGHT_NAV_RETRY_DELAY_MS = 250


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


class AnchorLike(Protocol):
    def get_attribute(self, name: str) -> str | None: ...
    def inner_text(self) -> str: ...
    def text_content(self) -> str | None: ...


class ResponseLike(Protocol):
    def text(self) -> str: ...


class RequestLike(Protocol):
    """Playwright's `page.request`: HTTP with the page's cookies, no rendering."""

    def get(self, url: str) -> ResponseLike: ...


class PageLike(Protocol):
    def goto(self, url: str, wait_until: str = ..., timeout: float = ...) -> None: ...
    def wait_for_selector(
        self, selector: str, timeout: int, state: str | None = None,
    ) -> None: ...
    def query_selector_all(self, selector: str) -> list[AnchorLike]: ...
    def content(self) -> str: ...
    def wait_for_timeout(self, timeout: int) -> None: ...

    @property
    def url(self) -> str: ...

    @property
    def request(self) -> RequestLike: ...


def proxy_from_env() -> dict[str, str] | None:
    """Playwright's `proxy=` from HTTPS_PROXY (or HTTP_PROXY), or None when neither is set.

    Chrome doesn't read those itself. A factory worker's sandbox reaches the web only
    through its egress proxy (docs/factory-sandbox-plan.md §3.6).
    """
    names = ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy")
    raw = next((os.environ[n] for n in names if os.environ.get(n)), None)
    if raw is None:
        return None
    url = urlsplit(raw if "://" in raw else f"http://{raw}")
    proxy = {"server": f"{url.scheme}://{url.hostname}" + (f":{url.port}" if url.port else "")}
    if url.username:
        proxy |= {"username": unquote(url.username), "password": unquote(url.password or "")}
    bypass = os.environ.get("NO_PROXY") or os.environ.get("no_proxy")
    if bypass:
        proxy["bypass"] = bypass
    return proxy


@contextmanager
def launch_stealth_browser(*, channel: str | None = None) -> Iterator[PageLike]:
    """Yield a stealth-patched page. PLAYWRIGHT_HEADLESS and
    PLAYWRIGHT_BROWSER_CHANNEL override the defaults; `channel` is the
    caller's default when the env var is unset (e.g. "chrome" for sites
    whose bot checks reject bundled Chromium)."""
    launch_kwargs: dict[str, object] = {
        "headless": _env_bool("PLAYWRIGHT_HEADLESS", False),
    }
    channel = os.getenv("PLAYWRIGHT_BROWSER_CHANNEL") or channel
    if channel:
        launch_kwargs["channel"] = channel
    proxy = proxy_from_env()
    if proxy:
        launch_kwargs["proxy"] = proxy

    with sync_playwright() as pw:
        browser = pw.chromium.launch(**launch_kwargs)
        try:
            context = browser.new_context()
            Stealth().apply_stealth_sync(context)
            yield context.new_page()
        finally:
            browser.close()


def goto_with_retry(*, page: PageLike, page_url: str, max_attempts: int = 3) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            page.goto(page_url, wait_until="domcontentloaded")
            return
        except Exception as exc:
            error_text = str(exc).lower()
            interrupted = "interrupted by another navigation" in error_text
            is_last_attempt = attempt == max_attempts
            if not interrupted or is_last_attempt:
                raise
            LOGGER.warning(
                "Navigation interrupted for %s (attempt %d/%d), retrying",
                page_url, attempt, max_attempts,
            )
            page.wait_for_timeout(PLAYWRIGHT_NAV_RETRY_DELAY_MS)


def wait_for_selector_quietly(
    *, page: PageLike, selector: str, state: str | None, source_label: str,
) -> None:
    """Wait for `selector`, treating the wait itself as best-effort.

    The wait only lets a fast page resolve in a second instead of blocking for
    the full timeout. When it expires we still scrape whatever the DOM holds,
    so a hidden or late link produces a real "nothing found" error (or a link)
    rather than a Playwright timeout that hides why the parish was skipped.
    """
    try:
        if state is None:
            page.wait_for_selector(selector, timeout=PLAYWRIGHT_SELECTOR_TIMEOUT_MS)
        else:
            page.wait_for_selector(
                selector, timeout=PLAYWRIGHT_SELECTOR_TIMEOUT_MS, state=state,
            )
    except Exception as exc:
        LOGGER.warning(
            "Selector %s did not settle for %s (%s); scraping the page anyway",
            selector, source_label, type(exc).__name__,
        )


def anchor_text(anchor: AnchorLike) -> str:
    try:
        return anchor.inner_text().strip()
    except Exception:
        pass
    try:
        return (anchor.text_content() or "").strip()
    except Exception:
        return ""
