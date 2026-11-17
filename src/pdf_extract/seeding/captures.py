"""`seed capture`: store a page of a parish's website or Facebook page for a source seed.

A bulletin seed's evidence is the stored PDF; a source seed's is the page it was
read from (docs/source-schedules-plan.md), which can change or disappear. So a
drafter captures each page it relies on, and the source seed cites the capture:

- The page is rendered in the pipeline's stealth browser (`browser.launch_stealth_browser`;
  run it under xvfb-run, as `seed site` and fetch are) and its visible text kept
  as `seed site` reads it. The text is committed beside the seed files,
  `data/seeds/captures/<parish>/<sha256 of the text>.txt`, so `seed check` can
  confirm each quote anywhere, and a reviewer can read it in the pull request.
- A full-page screenshot is stored in the blob store as
  `captures/<parish>/<sha256>.png` (it reaches R2 only where `CARLO_REMOTE_WRITE` is
  set, as fetched bulletins do) and split into tiles in `data/seed-work/<parish>/`
  that Claude Code's Read passes on unshrunk (`page_images.fits`): a Facebook
  schedule is often a picture, and its text is only in the screenshot.
- The capture is added to the file's `captures`, named by its text's hash, so
  capturing an unchanged page again adds nothing. The first capture is the
  primary one (the page the website links as the times' source) unless another
  is made primary.

A page that comes back empty, or as a challenge page, is refused rather than
stored. A Facebook page that asks the visitor to log in is stored with a
warning, since its posts may still be there.
"""

from __future__ import annotations

import hashlib
import io
import os
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from PIL import Image

from pdf_extract.blobstore import get_store
from pdf_extract.dioceses.web import html_text
from pdf_extract.model import FACEBOOK, sha256_text, source_platform
from pdf_extract.seeding.files import (
    APPROVED,
    SEEDS_DIR,
    WORK_DIR,
    capture_text_path,
    captures,
    is_source_seed,
    read_capture_text,
    resolve_capture,
    short_capture,
)
from pdf_extract.seeding.page_images import MAX_IMAGE_EDGE, fits, image_tokens
from pdf_extract.seeding.queries import SeedError

# Less text than this, with no screenshot to read instead, is not a page.
MIN_TEXT_CHARS = 40
BLOCKED_MARKERS = ("just a moment", "enable javascript and cookies", "attention required",
                   "checking your browser")
LOGIN_MARKERS = ("log in to facebook", "you must log in", "log into facebook",
                 "see more on facebook")
# How long the browser waits for a script to draw the page, and how tall a screenshot
# is kept (a Facebook page grows as it is scrolled; the newest posts are at the top).
SETTLE_MS = 6000
MAX_SCREENSHOT_PX = 16000
# Screenshot tiles overlap by this much, so a line on a boundary is whole in one.
TILE_OVERLAP_PX = 120

# What grabbing a page returns: its rendered HTML, the address it ended at, and a
# full-page PNG screenshot (None when none could be taken).
Grab = Callable[[str], tuple[str, str, bytes | None]]


def screenshot_key(parish_slug: str, png_hash: str) -> str:
    return f"captures/{parish_slug}/{png_hash}.png"


def _blocked(text: str) -> bool:
    head = text[:2000].lower()
    return any(marker in head for marker in BLOCKED_MARKERS)


def browser_grab(url: str) -> tuple[str, str, bytes | None]:
    """The page in the stealth browser: Chrome, which Cloudflare passes more often, or
    Playwright's Chromium without it."""
    from pdf_extract.browser import goto_with_retry, launch_stealth_browser

    for channel in ("chrome", None):
        try:
            with launch_stealth_browser(channel=channel) as page:
                goto_with_retry(page=page, page_url=url)
                for _ in range(3):
                    page.wait_for_timeout(SETTLE_MS)
                    if not _blocked(html_text(page.content())):
                        break
                png = page.screenshot(full_page=True)  # type: ignore[attr-defined]
                return page.content(), page.url, png
        except Exception as exc:
            if channel is None or "is not found" not in str(exc):
                raise
    raise AssertionError("unreachable")


def _tiles(png: bytes) -> list[Image.Image]:
    """The screenshot cut into tiles Read passes on unshrunk, top to bottom."""
    image = Image.open(io.BytesIO(png)).convert("RGB")
    if image.width > MAX_IMAGE_EDGE:
        image = image.resize((MAX_IMAGE_EDGE, round(image.height * MAX_IMAGE_EDGE / image.width)))
    if image.height > MAX_SCREENSHOT_PX:
        image = image.crop((0, 0, image.width, MAX_SCREENSHOT_PX))
    height = MAX_IMAGE_EDGE
    while height > TILE_OVERLAP_PX * 2 and not fits(image.width, height):
        height -= 28
    tiles, top = [], 0
    while True:
        bottom = min(top + height, image.height)
        tiles.append(image.crop((0, top, image.width, bottom)))
        if bottom >= image.height:
            return tiles
        top = bottom - TILE_OVERLAP_PX


def write_tiles(parish_slug: str, png_hash: str, png: bytes, work_dir: Path = WORK_DIR,
                ) -> list[dict[str, Any]]:
    """The screenshot's tiles as PNGs in the parish's work folder, with their cost."""
    folder = work_dir / parish_slug / "captures"
    folder.mkdir(parents=True, exist_ok=True)
    out = []
    for i, tile in enumerate(_tiles(png), 1):
        path = folder / f"{png_hash[:12]}-{i}.png"
        tile.save(path, format="PNG", optimize=True)
        out.append({"path": Path(os.path.relpath(path)).as_posix(), "width": tile.width,
                    "height": tile.height, "tokens": image_tokens(tile.width, tile.height)})
    return out


def capture_page(
    seed: dict[str, Any], url: str, *, primary: bool = False, grab: Grab | None = None,
    seeds_dir: Path = SEEDS_DIR, work_dir: Path = WORK_DIR, now: datetime | None = None,
) -> dict[str, Any]:
    """Capture `url` into the source seed `seed` (changed in place; the caller writes it).

    Returns the capture, its text, the screenshot's tiles and any warnings.
    """
    if not is_source_seed(seed):
        raise SeedError("Only a source seed captures pages: this parish is seeded from its "
                        "bulletins (`seed site` reads a page for a bulletin seed)")
    if seed.get("status") == APPROVED:
        raise SeedError("An approved seed belongs to its reviewer; it cannot be changed")
    if not url.startswith(("https://", "http://")):
        raise SeedError(f"Capture a full http(s) address, not {url!r}")
    slug = seed["parish_slug"]
    page, final, png = (grab or browser_grab)(url)
    text = html_text(page) if page else ""
    if _blocked(text) or (len(text) < MIN_TEXT_CHARS and png is None):
        raise SeedError(f"Could not read {url}: " + ("a challenge page" if _blocked(text)
                                                     else "no text and no screenshot")
                        + ". Run it under xvfb-run, or try again later")
    warnings = []
    platform = source_platform(url)
    if platform == FACEBOOK and any(m in text.lower() for m in LOGIN_MARKERS):
        warnings.append("Facebook asked to log in: check the screenshot shows the posts you "
                        "quote, and quote nothing hidden behind the prompt")
    if len(text) < MIN_TEXT_CHARS:
        warnings.append("almost no text: the schedule may be a picture; read the screenshot "
                        "and mark what you quote from it from_image")
    text = text.rstrip("\n") + "\n"
    content_hash = sha256_text(text)
    path = capture_text_path(slug, content_hash, seeds_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    if read_capture_text(slug, content_hash, seeds_dir) is None:
        path.write_text(text, encoding="utf-8", newline="\n")

    png_hash = None
    tiles: list[dict[str, Any]] = []
    if png is not None:
        png_hash = hashlib.sha256(png).hexdigest()
        get_store().put(screenshot_key(slug, png_hash), png, content_type="image/png")
        tiles = write_tiles(slug, png_hash, png, work_dir)

    captured_at = (now or datetime.now(UTC)).isoformat(timespec="seconds")
    listed = resolve_capture(seed, content_hash)
    if listed is None or listed["content_hash"] != content_hash:
        listed = {
            "content_hash": content_hash, "url": url,
            "final_url": final if final and final != url else None, "platform": platform,
            "captured_at": captured_at, "screenshot_hash": png_hash, "primary": False,
        }
        seed["captures"].append(listed)
        new = True
    else:
        # The same text: the same capture, read again now. Its screenshot is replaced,
        # since a picture on the page (a Facebook schedule) can change under the same text.
        new = False
        warnings.append(f"the page's text is unchanged since {listed['captured_at']}: that "
                        "capture is kept, with this screenshot and time")
        listed["captured_at"] = captured_at
        if png_hash is not None:
            listed["screenshot_hash"] = png_hash
    if primary or not any(c.get("primary") for c in captures(seed)):
        for c in captures(seed):
            c["primary"] = c is listed
    return {
        "parish": slug,
        "capture": {**listed, "short": short_capture(seed, content_hash)},
        "new": new,
        "text_path": Path(os.path.relpath(path)).as_posix(),
        "tiles": tiles,
        "warnings": warnings,
        "text": text,
    }


def capture_text(seed: dict[str, Any], ref: str, seeds_dir: Path = SEEDS_DIR) -> dict[str, Any]:
    """`seed capture-text`: a capture's stored text, to quote from."""
    found = resolve_capture(seed, ref)
    if found is None:
        listed = ", ".join(c["content_hash"][:8] for c in captures(seed)) or "none"
        raise SeedError(f"{ref!r} names none of the file's captures ({listed})")
    text = read_capture_text(seed["parish_slug"], found["content_hash"], seeds_dir)
    if text is None:
        raise SeedError(f"capture {found['content_hash'][:12]}'s text is not in "
                        f"{capture_text_path(seed['parish_slug'], found['content_hash'], seeds_dir)}")
    return {"parish": seed["parish_slug"],
            "capture": {**found, "short": short_capture(seed, found["content_hash"])},
            "text": text}
