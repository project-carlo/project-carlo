"""Render a bulletin's pages to PNGs sized for an OpenAI image `detail` level.

The pdf stack can send the bulletin as one image per page instead of the PDF
(`pnpm bench --pdf-input images`). OpenAI resizes every image to fit its
detail level before reading it, so each page is rendered straight at the size
the model will see, never larger (a bigger upload buys nothing) and never
smaller (it would throw away legibility the level pays for).

Limits (https://platform.openai.com/docs/guides/images-vision), images are
tokenised in 32 × 32 px patches:

- `low`: fits within 512 × 512 px (gpt-5.5 and later; gpt-5.4 reads `low`
  at up to 2,048 px, so there this level sends less than the model takes).
- `high`: at most 2,500 patches and 2,048 px a side (gpt-5.4 through
  gpt-5.6): about 165 dpi for a letter page.
- `original`: sent as is. The tightest documented cap is gpt-5.4/5.5's
  10,000 patches and 6,000 px a side (larger images are scaled down, and
  gpt-5.6 rejects anything over 30,000 patches), so pages render at 300 dpi
  (what the OCR stack reads, 8,320 patches for letter) and shrink only when a
  large page would pass that cap.

Rendering needs PyMuPDF, from the optional `bench` dependency group; it is
imported only to render, so the sizing and the version are there without it.
"""

from __future__ import annotations

import importlib.util
import math
import threading
from dataclasses import dataclass

PATCH = 32
POINTS_PER_INCH = 72


@dataclass(frozen=True)
class RenderLimit:
    dpi: int
    """Resolution a page renders at when it fits the other limits."""
    max_side: int
    """Longest side in pixels."""
    max_patches: int | None
    """32 × 32 px patches, rounding each side up."""


LIMITS: dict[str, RenderLimit] = {
    "low": RenderLimit(dpi=300, max_side=512, max_patches=None),
    "high": RenderLimit(dpi=300, max_side=2048, max_patches=2500),
    "original": RenderLimit(dpi=300, max_side=6000, max_patches=10_000),
}

RENDER_VERSION = "png-v1-" + "-".join(
    f"{detail}{lim.dpi}dpi{lim.max_side}px{lim.max_patches or ''}"
    for detail, lim in LIMITS.items()
)
"""Moves when the rendering does, so cached results are re-extracted."""

# PyMuPDF documents are not safe to share across threads; the bench extracts
# several bulletins at once.
_LOCK = threading.Lock()


def _patches(width: int, height: int) -> int:
    return math.ceil(width / PATCH) * math.ceil(height / PATCH)


def render_scale(width_pt: float, height_pt: float, detail: str) -> float:
    """Pixels per PDF point for a page of this size (points are 1/72 inch)."""
    limit = LIMITS[detail]
    scale = min(limit.dpi / POINTS_PER_INCH, limit.max_side / max(width_pt, height_pt))
    if limit.max_patches:
        # Area bound first, then step down for the patches' rounding up.
        scale = min(scale, math.sqrt(limit.max_patches * PATCH * PATCH / (width_pt * height_pt)))
        while _patches(math.ceil(width_pt * scale), math.ceil(height_pt * scale)) > limit.max_patches:
            scale *= 0.99
    return scale


def require_renderer() -> None:
    """Raise ImportError now, rather than per bulletin, when PyMuPDF is missing."""
    if importlib.util.find_spec("pymupdf") is None:
        raise ImportError(
            "Sending PDF pages as images needs PyMuPDF: run `uv sync --group bench`"
        )


def render_pages(pdf_bytes: bytes, detail: str) -> list[bytes]:
    """Every page of the PDF as a PNG, in page order."""
    import pymupdf

    with _LOCK:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        try:
            images = []
            for page in doc:
                rect = page.rect  # after the page's rotation
                scale = render_scale(rect.width, rect.height, detail)
                pixmap = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
                images.append(pixmap.tobytes("png"))
            return images
        finally:
            doc.close()
