"""`seed capture`: store a page of a parish's website or Facebook page for a source seed.

A bulletin seed's evidence is the stored PDF; a source seed's is the page it was
read from (docs/source-schedules-plan.md), which can change or disappear. So a
drafter captures each page it relies on, and the source seed cites the capture:

- The page is rendered in the pipeline's stealth browser (`site.browser_page`; run
  it under xvfb-run, as `seed site` and fetch are) and its visible text kept as
  `seed site` reads it. The text is committed beside the seed files,
  `data/seeds/captures/<parish>/<sha256>.txt`, so `seed check` can confirm each
  quote anywhere, and a reviewer can read it in the pull request. It opens with a
  short header (`files.capture_document`): the page's address, where it ended, and
  the Facebook pages it links, which is how `seed check` knows a Facebook page is
  the parish's own. The hash covers the header, so two pages with the same text
  (two pages that are only a picture) are two captures.
- A full-page screenshot, as a WebP no wider than Read takes and cut off at
  MAX_SCREENSHOT_PX, is stored in the blob store as `captures/<parish>/<sha256>.webp`
  and split into PNG tiles in `data/seed-work/<parish>/` that Claude Code's Read
  passes on unshrunk (`page_images.fits`): a Facebook schedule is often a picture,
  and its text is only in the screenshot. A quote read from it names the
  screenshot (`from_image`), and `seed finalize` commits each screenshot a quote
  names beside the text (`keep_quoted_screenshots`), since the blob store reaches
  R2 only from a machine that writes there and a reviewer must see it.
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
import html
import io
import os
import re
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from PIL import Image

from pdf_extract.blobstore import get_store
from pdf_extract.dioceses.web import html_text
from pdf_extract.model import FACEBOOK, WEBSITE, facebook_page, sha256_text, source_platform
from pdf_extract.seeding.files import (
    APPROVED,
    CAPTURES_DIRNAME,
    SEEDS_DIR,
    WORK_DIR,
    capture_document,
    capture_text_path,
    captures,
    is_source_seed,
    read_capture_text,
    resolve_capture,
    screenshot_path,
    short_capture,
)
from pdf_extract.seeding.page_images import MAX_IMAGE_EDGE, fits, image_tokens
from pdf_extract.seeding.queries import SeedError
from pdf_extract.seeding.site import blocked, browser_page

# Less text than this, with no screenshot to read instead, is not a page.
MIN_TEXT_CHARS = 40
LOGIN_MARKERS = ("log in to facebook", "you must log in", "log into facebook",
                 "see more on facebook")
# How tall a screenshot is kept (a Facebook page grows as it is scrolled; the newest
# posts are at the top), and its WebP quality: legible text, a tenth of a PNG's size.
MAX_SCREENSHOT_PX = 16000
SCREENSHOT_QUALITY = 85
# Screenshot tiles overlap by this much, so a line on a boundary is whole in one.
TILE_OVERLAP_PX = 120
_LINK = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)

# What grabbing a page returns: its rendered HTML, the address it ended at, and a
# full-page PNG screenshot (None when none could be taken).
Grab = Callable[[str], tuple[str, str, bytes | None]]


def screenshot_key(parish_slug: str, screenshot_hash: str) -> str:
    return f"captures/{parish_slug}/{screenshot_hash}.webp"


def browser_grab(url: str) -> tuple[str, str, bytes | None]:
    """The page in the stealth browser, with a full-page screenshot."""
    return browser_page(url, screenshot=True)


def screenshot_image(png: bytes) -> bytes:
    """The screenshot as it is kept: a WebP no wider than Read takes, cut off at
    MAX_SCREENSHOT_PX (a WebP is at most 16383 pixels each way)."""
    image = Image.open(io.BytesIO(png)).convert("RGB")
    if image.width > MAX_IMAGE_EDGE:
        image = image.resize((MAX_IMAGE_EDGE, round(image.height * MAX_IMAGE_EDGE / image.width)))
    if image.height > MAX_SCREENSHOT_PX:
        image = image.crop((0, 0, image.width, MAX_SCREENSHOT_PX))
    out = io.BytesIO()
    image.save(out, format="WEBP", quality=SCREENSHOT_QUALITY)
    return out.getvalue()


def linked_facebook_pages(page: str, base: str) -> list[str]:
    """The Facebook pages `page` links or embeds, as `model.facebook_page` names them."""
    found = {facebook_page(urljoin(base, html.unescape(link.strip())))
             for link in _LINK.findall(page)}
    return sorted(p for p in found if p)


def _tiles(screenshot: bytes) -> list[Image.Image]:
    """The kept screenshot (`screenshot_image`) cut into tiles Read passes on unshrunk,
    top to bottom."""
    image = Image.open(io.BytesIO(screenshot)).convert("RGB")
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


def write_tiles(parish_slug: str, screenshot_hash: str, screenshot: bytes,
                work_dir: Path = WORK_DIR) -> list[dict[str, Any]]:
    """The screenshot's tiles as PNGs in the parish's work folder, with their cost."""
    folder = work_dir / parish_slug / "captures"
    folder.mkdir(parents=True, exist_ok=True)
    out = []
    for i, tile in enumerate(_tiles(screenshot), 1):
        path = folder / f"{screenshot_hash[:12]}-{i}.png"
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
    if blocked(text) or (len(text) < MIN_TEXT_CHARS and png is None):
        raise SeedError(f"Could not read {url}: " + ("a challenge page" if blocked(text)
                                                     else "no text and no screenshot")
                        + ". Run it under xvfb-run, or try again later")
    warnings = []
    platform = source_platform(url)
    if platform == FACEBOOK and any(m in text.lower() for m in LOGIN_MARKERS):
        warnings.append("Facebook asked to log in: check the screenshot shows the posts you "
                        "quote, and quote nothing hidden behind the prompt")
    if len(text) < MIN_TEXT_CHARS:
        warnings.append("almost no text: the schedule may be a picture; read the screenshot "
                        "and cite what you quote from it as `cap <capture> image: …`")
    final_url = final if final and final != url else None
    linked = linked_facebook_pages(page, final or url) if platform == WEBSITE and page else []
    document = capture_document(url, final_url, linked, text)
    content_hash = sha256_text(document)
    path = capture_text_path(slug, content_hash, seeds_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    if read_capture_text(slug, content_hash, seeds_dir) is None:
        path.write_text(document, encoding="utf-8", newline="\n")

    shot_hash = None
    tiles: list[dict[str, Any]] = []
    if png is not None:
        shot = screenshot_image(png)
        shot_hash = hashlib.sha256(shot).hexdigest()
        get_store().put(screenshot_key(slug, shot_hash), shot, content_type="image/webp")
        tiles = write_tiles(slug, shot_hash, shot, work_dir)

    captured_at = (now or datetime.now(UTC)).isoformat(timespec="seconds")
    listed = resolve_capture(seed, content_hash)
    if listed is None or listed["content_hash"] != content_hash:
        listed = {
            "content_hash": content_hash, "url": url, "final_url": final_url,
            "platform": platform, "captured_at": captured_at, "screenshot_hash": shot_hash,
            "primary": False,
        }
        seed["captures"].append(listed)
        new = True
    else:
        # The same page and text: the same capture, read again now. Its screenshot is
        # replaced, since a picture on the page (a Facebook schedule) can change under
        # the same text; a quote read from the old one names it, and `seed check` asks
        # for it to be read again from this one.
        new = False
        warnings.append(f"the page's text is unchanged since {listed['captured_at']}: that "
                        "capture is kept, with this screenshot and time")
        old_shot = listed["screenshot_hash"]
        listed["captured_at"] = captured_at
        if shot_hash is not None:
            listed["screenshot_hash"] = shot_hash
        replaced = shot_hash is not None and old_shot not in (None, shot_hash)
        stale = [slot["id"] for slot in seed["slots"] for src in slot.get("sources") or []
                 if replaced and isinstance(src, dict) and src.get("from_image") == old_shot
                 and resolve_capture(seed, src.get("capture")) is listed]
        if stale:
            warnings.append(f"the screenshot has changed: {', '.join(dict.fromkeys(stale))} "
                            "quote the old one. Read the new tiles and write their image "
                            "sources again")
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
        "text": document,
    }


def quoted_screenshots(seed: dict[str, Any]) -> set[str]:
    """The screenshots the file's sources quote (their `from_image`)."""
    return {src["from_image"] for slot in seed.get("slots") or [] if isinstance(slot, dict)
            for src in slot.get("sources") or []
            if isinstance(src, dict) and isinstance(src.get("from_image"), str)}


def keep_quoted_screenshots(seed: dict[str, Any], seeds_dir: Path = SEEDS_DIR) -> list[str]:
    """Commit each screenshot a source quotes beside the capture texts, from this
    machine's blob store, and remove committed screenshots no source quotes any more.
    Returns the quoted screenshots that couldn't be found (`seed check` reports them)."""
    slug = seed["parish_slug"]
    quoted = quoted_screenshots(seed)
    missing = []
    for shot_hash in sorted(quoted):
        try:
            path = screenshot_path(slug, shot_hash, seeds_dir)
        except ValueError:
            continue  # validate_seed reports a malformed hash
        if path.is_file():
            continue
        data = get_store().get(screenshot_key(slug, shot_hash))
        if data is None or hashlib.sha256(data).hexdigest() != shot_hash:
            missing.append(shot_hash)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    folder = seeds_dir / CAPTURES_DIRNAME / slug
    for kept in folder.glob("*.webp") if folder.is_dir() else []:
        if kept.stem not in quoted:
            kept.unlink()
    return missing


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
