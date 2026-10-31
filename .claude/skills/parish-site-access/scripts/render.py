"""Render bulletin PDF pages to images, to read the ones with no text layer.

Many bulletins are scanned images: `probe pdf` lists them under
`pages_without_text`, and a masthead or Mass schedule on such a page is
invisible to it. The sandbox has no pdftoppm, PIL or tesseract, so this renders
the pages with pdf.js (from cdn.jsdelivr.net) in the installed Chrome. Look at
the images with the Read tool. What you read off an image is evidence like any
quote: cite the PDF's URL and say in the `note` that the page is an image.

Usage (from the repo root; run setup_browser.sh once first):
  uv run python .claude/skills/parish-site-access/scripts/render.py URL|FILE OUT_PREFIX \
      [--pages 1,3-5] [--scale 1.6] [--png]

Writes OUT_PREFIX-p<N>.jpg for each page (every page without --pages) and
prints JSON: {"pdf", "page_count", "images": [...], "bytes": [...]}. JPEG keeps a
scanned page to a few hundred KB; as PNG one can pass 1 MB, which is slow to read
and once crashed the factory's workers. --png for line art that JPEG blurs.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
JPEG_QUALITY = 80
PDFJS = "https://cdn.jsdelivr.net/npm/pdfjs-dist@4.4.168/build"
PAGE = f"""<html><body style="margin:0;background:#fff"><script type="module">
import * as pdfjs from '{PDFJS}/pdf.min.mjs';
pdfjs.GlobalWorkerOptions.workerSrc = '{PDFJS}/pdf.worker.min.mjs';
let doc = null;
window.load = async (b64) => {{
  const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
  doc = await pdfjs.getDocument({{data: bytes}}).promise;
  return doc.numPages;
}};
window.render = async (scale, n) => {{
  const page = await doc.getPage(n);
  const vp = page.getViewport({{scale}});
  const c = document.createElement('canvas');
  c.width = vp.width; c.height = vp.height; c.id = 'c';
  document.body.innerHTML = ''; document.body.appendChild(c);
  await page.render({{canvasContext: c.getContext('2d'), viewport: vp}}).promise;
  return [Math.ceil(vp.width), Math.ceil(vp.height)];
}};
window.ready = true;
</script></body></html>"""


def _pdf_bytes(source: str) -> bytes:
    if os.path.exists(source):
        return Path(source).read_bytes()
    sys.path.insert(0, str(REPO / "src"))
    from pdf_extract.dioceses import web

    resp = web.fetch(source)
    if not resp.ok:
        raise SystemExit(f"{source}: {resp.error or f'HTTP {resp.status}'}")
    if resp.truncated:
        raise SystemExit(f"{source}: larger than {web.MAX_BYTES // 1_000_000} MB")
    return resp.body


def _page_numbers(spec: str) -> list[int]:
    """'1,3-5' -> [1, 3, 4, 5]."""
    out: list[int] = []
    for part in spec.split(","):
        first, _, last = part.strip().partition("-")
        out.extend(range(int(first), int(last or first) + 1))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("pdf", help="a PDF URL or a local file")
    parser.add_argument("out", type=Path, help="output prefix, e.g. /tmp/bulletin")
    parser.add_argument("--pages", help="page numbers and ranges, e.g. 1,3-5 (default: all)")
    parser.add_argument("--scale", type=float, default=1.6)
    parser.add_argument("--png", action="store_true", help="PNG instead of JPEG")
    args = parser.parse_args()

    data = base64.b64encode(_pdf_bytes(args.pdf)).decode()
    from playwright.sync_api import sync_playwright

    sys.path.insert(0, str(REPO / "src"))
    from pdf_extract.browser import chromium_sandbox_enabled, proxy_from_env

    channel = "chrome" if shutil.which("google-chrome") else None
    args.out.parent.mkdir(parents=True, exist_ok=True)
    images = []
    with sync_playwright() as p:
        # Headless is fine here: the page is local and loads nothing behind Cloudflare.
        # Through the proxy when there is one (a factory sandbox reaches pdf.js only so).
        proxy = proxy_from_env()
        browser = p.chromium.launch(channel=channel, headless=True,
                                    chromium_sandbox=chromium_sandbox_enabled(),
                                    **({"proxy": proxy} if proxy else {}))
        try:
            page = browser.new_page()
            page.set_content(PAGE)
            page.wait_for_function("window.ready === true", timeout=60000)
            count = page.evaluate("b => window.load(b)", data)
            wanted = _page_numbers(args.pages) if args.pages else range(1, count + 1)
            for n in wanted:
                if not 1 <= n <= count:
                    continue
                width, height = page.evaluate("([s, n]) => window.render(s, n)", [args.scale, n])
                page.set_viewport_size({"width": width, "height": height})
                path = f"{args.out}-p{n}.{'png' if args.png else 'jpg'}"
                if args.png:
                    page.locator("#c").screenshot(path=path, type="png")
                else:
                    page.locator("#c").screenshot(path=path, type="jpeg", quality=JPEG_QUALITY)
                images.append(path)
        finally:
            browser.close()
    print(json.dumps({"pdf": args.pdf, "page_count": count, "images": images,
                      "bytes": [os.path.getsize(i) for i in images]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
