"""Images on a bulletin's text pages with no text layer over them.

`seed text` reads a PDF's text layer, so print that is only pixels (a schedule set as a
picture, a flyer pasted in) is invisible to it. A page with almost no text is only an
image; this finds, on the other pages, the images that hold next to none of the page's
text, which `seed pages --images` packs into one image (`page_images`).

On the newest bulletin of 250 parishes (1,789 pages), 45% of text pages had such an image
over 15% of the page. Most were cover art, photos and ads, but some held Mass, Confession
or Adoration times found nowhere in the text: one parish's whole weekly schedule.

An image counts as textless before images are merged: merging first joined a textless
schedule to a captioned photo beside it and lost it.
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass

import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c

# Fewer characters than this on a page: it is only an image (`seed text`).
MIN_PAGE_TEXT_CHARS = 40
# An image with at most this many text-layer characters inside it (a caption) is textless.
MAX_CHARS_INSIDE = 30
MIN_OBJECT_SHARE = 0.004    # smaller images (bullets, icons) are left out...
MIN_SHARE = 0.02            # ...as are textless areas, once merged, under this share of a page
MIN_SIDE_PT = 36            # ...or narrower than this (half an inch: a column's edge)
MERGE_SLACK_PT = 4          # images this close are one area (a collage, a sliced picture)
FORM_DEPTH = 5              # how deep into nested forms to look for images

_SPACES = {0, 9, 10, 13, 32, 0xA0, 0xFFFE, 0xFFFF}

Box = tuple[float, float, float, float]


@dataclass(frozen=True)
class TextlessImage:
    """An area of a page that is images with no text layer: x0, y0, x1, y1 as fractions
    of the page as shown, from its top left (what `seed pages --region` takes)."""

    page: int
    box: Box

    @property
    def share(self) -> float:
        x0, y0, x1, y1 = self.box
        return (x1 - x0) * (y1 - y0)


def page_text(textpage: pdfium.PdfTextPage) -> str:
    """A page's text layer, as `seed text` prints it."""
    return textpage.get_text_range().replace("\r\n", "\n").strip()


def is_image_only(text: str) -> bool:
    return len(text) < MIN_PAGE_TEXT_CHARS


def textless_images(page: pdfium.PdfPage, textpage: pdfium.PdfTextPage,
                    number: int) -> list[TextlessImage]:
    """The areas of page `number` that are images with no text layer, largest first."""
    width, height = page.get_size()
    centers = []
    for i in range(textpage.count_chars()):
        if pdfium_c.FPDFText_GetUnicode(textpage, i) in _SPACES:
            continue
        left, bottom, right, top = textpage.get_charbox(i)
        centers.append(((left + right) / 2, (bottom + top) / 2))
    found: list[list[float]] = []
    for obj in page.get_objects(filter=[pdfium_c.FPDF_PAGEOBJ_IMAGE], max_depth=FORM_DEPTH):
        left, bottom, right, top = _page_bounds(obj)
        x0, y0, x1, y1 = _shown(page, width, height, (left, bottom, right, top))
        if (x1 - x0) * (y1 - y0) < MIN_OBJECT_SHARE * width * height:
            continue
        inside = 0
        for cx, cy in centers:
            if left <= cx <= right and bottom <= cy <= top:
                inside += 1
                if inside > MAX_CHARS_INSIDE:
                    break
        if inside <= MAX_CHARS_INSIDE:
            found.append([x0, y0, x1, y1])
    areas = [TextlessImage(number, (x0 / width, y0 / height, x1 / width, y1 / height))
             for x0, y0, x1, y1 in _merge(found)
             if (x1 - x0) * (y1 - y0) >= MIN_SHARE * width * height
             and min(x1 - x0, y1 - y0) >= MIN_SIDE_PT]
    return sorted(areas, key=lambda a: -a.share)


def _page_bounds(obj: pdfium.PdfObject) -> Box:
    """An object's bounds on the page: inside a form, they are in the form's space."""
    left, bottom, right, top = obj.get_bounds()
    corners = [(left, bottom), (left, top), (right, bottom), (right, top)]
    form = obj.container
    while form is not None:
        matrix = form.get_matrix()
        corners = [matrix.on_point(x, y) for x, y in corners]
        form = form.container
    xs, ys = [x for x, _ in corners], [y for _, y in corners]
    return min(xs), min(ys), max(xs), max(ys)


_PRECISION = 10  # device units per point when mapping to the page as shown


def _shown(page: pdfium.PdfPage, width: float, height: float, box: Box) -> Box:
    """A box in PDF page space as x0, y0, x1, y1 points on the page as shown (rotation
    and crop box applied, from the top left), clipped to the page."""
    size_x, size_y = round(width * _PRECISION), round(height * _PRECISION)
    dx, dy = ctypes.c_int(), ctypes.c_int()
    xs, ys = [], []
    left, bottom, right, top = box
    for x, y in ((left, bottom), (left, top), (right, bottom), (right, top)):
        pdfium_c.FPDF_PageToDevice(page, 0, 0, size_x, size_y, 0, x, y,
                                   ctypes.byref(dx), ctypes.byref(dy))
        xs.append(dx.value / _PRECISION)
        ys.append(dy.value / _PRECISION)
    return (max(0.0, min(xs)), max(0.0, min(ys)),
            min(width, max(xs)), min(height, max(ys)))


def _merge(boxes: list[list[float]]) -> list[list[float]]:
    """Boxes that touch or overlap (within MERGE_SLACK_PT), joined into their bounds."""
    boxes = [b for b in boxes if b[2] > b[0] and b[3] > b[1]]
    merged = True
    while merged:
        merged = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if (a[0] - MERGE_SLACK_PT <= b[2] and b[0] - MERGE_SLACK_PT <= a[2]
                        and a[1] - MERGE_SLACK_PT <= b[3] and b[1] - MERGE_SLACK_PT <= a[3]):
                    boxes[i] = [min(a[0], b[0]), min(a[1], b[1]),
                                max(a[2], b[2]), max(a[3], b[3])]
                    del boxes[j]
                    merged = True
                    break
            if merged:
                break
    return boxes


def find(pages: dict[int, pdfium.PdfPage]) -> tuple[list[int], list[TextlessImage]]:
    """Of `pages` (by number): those only an image, and the others' textless images."""
    image_only, found = [], []
    for number, page in pages.items():
        textpage = page.get_textpage()
        try:
            if is_image_only(page_text(textpage)):
                image_only.append(number)
            else:
                found += textless_images(page, textpage, number)
        finally:
            textpage.close()
    return image_only, found
