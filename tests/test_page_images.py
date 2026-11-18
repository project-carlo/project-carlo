"""`seed pages`' renders: sized for Read, cropped where asked, tiled into labelled sheets;
and the images with no text layer that `seed text` flags and `seed pages --images` packs."""

from __future__ import annotations

import io
import random
import zlib
from pathlib import Path

import pypdfium2 as pdfium
import pytest
from PIL import Image, ImageStat
from pypdf import PdfReader, PdfWriter

from pdf_extract.seeding import cli as seed_cli
from pdf_extract.seeding import page_images as pi
from pdf_extract.seeding import textless

LETTER = (612, 792)


def _pdf(pages: int = 1, *, size: tuple[int, int] = LETTER, rotate: int = 0) -> bytes:
    """Pages at 72 dpi, white with a black square in the bottom-right quarter."""
    images = []
    for _ in range(pages):
        im = Image.new("RGB", size, "white")
        w, h = size
        im.paste((0, 0, 0), (int(w * 0.6), int(h * 0.6), int(w * 0.95), int(h * 0.95)))
        images.append(im)
    buf = io.BytesIO()
    images[0].save(buf, format="PDF", resolution=72, save_all=True, append_images=images[1:])
    if not rotate:
        return buf.getvalue()
    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(buf.getvalue())))
    for page in writer.pages:
        page.rotate(rotate)
    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()


def _darkness(path: str) -> float:
    return 1 - ImageStat.Stat(Image.open(path).convert("L")).mean[0] / 255


def test_token_cost_and_the_size_read_passes_on():
    assert pi.image_tokens(1275, 1650) == 46 * 59
    assert pi.fits(1545, 2000) and not pi.fits(1545, 2001)
    assert not pi.fits(2000, 2000)  # under the edge, over the token cap
    assert pi.fit_dpi(*LETTER, 100) == 100
    dpi = pi.fit_dpi(*LETTER, 300)
    assert 175 <= dpi < 182 and pi.fits(-(-612 * dpi // 72), -(-792 * dpi // 72))


def test_pages_and_regions_parse_and_are_checked():
    assert pi.parse_pages(None, 3) == [1, 2, 3]
    assert pi.parse_pages(2, 3) == [2]
    assert pi.parse_pages("2,4-6", 8) == [2, 4, 5, 6]
    with pytest.raises(pi.PageImageError, match="pages 1 to 3"):
        pi.parse_pages("2-4", 3)
    with pytest.raises(pi.PageImageError, match="a number, a range or a list"):
        pi.parse_pages("first", 3)
    assert pi.parse_region("top-left") == ("top-left", (0, 0, 0.55, 0.55))
    assert pi.parse_region("0.4,0.6,1,1") == ("r40-60-100-100", (0.4, 0.6, 1, 1))
    for bad in ("middle", "0.5,0.5,0.4,1", "0,0,1"):
        with pytest.raises(pi.PageImageError):
            pi.parse_region(bad)


def test_a_page_renders_at_100_dpi_and_reports_its_cost(tmp_path: Path):
    r = pi.render(_pdf(2), tmp_path, "abc", page=1)
    [im] = r["images"]
    assert (im["width"], im["height"], im["dpi"]) == (850, 1100, 100)
    assert im["tokens"] == r["tokens"] == 1240 and im["lowered_from"] is None
    assert Path(im["path"]).name == "abc-p1-100dpi.png" and r["paths"] == [im["path"]]


def test_a_dpi_read_would_shrink_is_lowered(tmp_path: Path):
    [im] = pi.render(_pdf(), tmp_path, "abc", page=1, dpi=300)["images"]
    assert im["lowered_from"] == 300 and im["dpi"] < 182
    assert pi.fits(im["width"], im["height"])
    with pytest.raises(pi.PageImageError, match="between 36 and 600"):
        pi.render(_pdf(), tmp_path, "abc", dpi=20)


def test_a_region_zooms_into_the_part_of_the_page_as_shown(tmp_path: Path):
    [im] = pi.render(_pdf(), tmp_path, "abc", page=1, region="bottom-right")["images"]
    assert max(im["width"], im["height"]) <= pi.ZOOM_LONG_EDGE and im["dpi"] > 200
    assert Path(im["path"]).name == f"abc-p1-bottom-right-{im['dpi']}dpi.png"
    assert _darkness(im["path"]) > 0.35  # the square fills 0.35² of the 0.55² region
    [blank] = pi.render(_pdf(), tmp_path, "abc", page=1, region="top-left")["images"]
    assert _darkness(blank["path"]) < 0.01
    # Turned a quarter clockwise, the square shows at the bottom left.
    rotated = _pdf(rotate=90)
    [im] = pi.render(rotated, tmp_path, "rot", page=1, region="bottom-left")["images"]
    assert im["width"] > im["height"] and _darkness(im["path"]) > 0.35
    # A zoom of every page would cost more than the pages: it takes the pages it zooms.
    with pytest.raises(pi.PageImageError, match="add --page N"):
        pi.render(_pdf(3), tmp_path, "abc", region="top")


def test_a_sheet_tiles_labelled_pages_into_one_image_read_takes_whole(tmp_path: Path):
    r = pi.render(_pdf(10), tmp_path, "abc", sheet=True)
    [im] = r["images"]
    assert im["pages"] == list(range(1, 11)) and im["dpi"] >= pi.SHEET_MIN_DPI
    assert pi.fits(im["width"], im["height"])
    assert Path(im["path"]).name == f"abc-sheet-p1-10-{im['dpi']}dpi.png"
    [im] = pi.render(_pdf(10), tmp_path, "abc", page="2,4-6", sheet=True)["images"]
    assert im["pages"] == [2, 4, 5, 6] and "-sheet-p2_4-6-" in im["path"]
    assert im["dpi"] <= pi.PAGE_DPI


def test_too_many_pages_for_one_sharp_sheet_make_several(tmp_path: Path):
    r = pi.render(_pdf(16), tmp_path, "abc", sheet=True)
    assert [im["pages"] for im in r["images"]] == [list(range(1, 9)), list(range(9, 17))]
    assert all(im["dpi"] >= pi.SHEET_MIN_DPI for im in r["images"])
    with pytest.raises(pi.PageImageError, match="--sheet tiles whole pages"):
        pi.render(_pdf(2), tmp_path, "abc", sheet=True, region="top")


# ── Images with no text layer ────────────────────────────────────────────────
NEWS = "Parish news for the week ahead, set in the PDF's text layer."


def _picture(width: int, height: int, seed: int, *, border: int = 0) -> Image.Image:
    """A white picture with dark blocks placed by `seed` (inside a white `border`)."""
    im = Image.new("RGB", (width, height), "white")
    rng = random.Random(seed)
    for _ in range(6):
        x0 = rng.randrange(border, width - border - 10)
        y0 = rng.randrange(border, height - border - 10)
        x1 = rng.randrange(x0 + 8, width - border + 1)
        y1 = rng.randrange(y0 + 8, height - border + 1)
        im.paste(tuple(rng.randrange(0, 120) for _ in range(3)), (x0, y0, x1, y1))
    return im


def _layout_pdf(pages: list[list[tuple]]) -> bytes:
    """US Letter pages of Helvetica text and images, placed in points from the top left:
    ("text", x, y, size, text); ("image", (x0, y0, x1, y1), picture); and
    ("form", scale, [image items]), images drawn in a form XObject scaled by `scale`."""
    objects: list[bytes] = [b"", b"", b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]

    def add(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    def stream(head: str, data: bytes) -> bytes:
        return f"<< {head} /Length {len(data)} >>\nstream\n".encode() + data + b"\nendstream"

    def images(items: list[tuple], height: float, scale: float = 1) -> tuple[str, list[str]]:
        names, ops = [], []
        for _, (x0, y0, x1, y1), picture in items:
            rgb = picture.convert("RGB")
            ref = add(stream(f"/Type /XObject /Subtype /Image /Width {rgb.width} /Height "
                             f"{rgb.height} /ColorSpace /DeviceRGB /BitsPerComponent 8 "
                             "/Filter /FlateDecode", zlib.compress(rgb.tobytes())))
            name = f"Im{ref}"
            names.append(f"/{name} {ref} 0 R")
            x0, y0, x1, y1 = (v / scale for v in (x0, y0, x1, y1))
            ops.append(f"q {x1 - x0:g} 0 0 {y1 - y0:g} {x0:g} {height / scale - y1:g} cm "
                       f"/{name} Do Q")
        return " ".join(names), ops

    page_ids = []
    for items in pages:
        xobjects, ops = images([i for i in items if i[0] == "image"], 792)
        for _, scale, inner in (i for i in items if i[0] == "form"):
            names, inner_ops = images(inner, 792, scale)
            ref = add(stream(f"/Type /XObject /Subtype /Form /BBox [0 0 {612 / scale:g} "
                             f"{792 / scale:g}] /Resources << /XObject << {names} >> >>",
                             "\n".join(inner_ops).encode()))
            xobjects += f" /Fm{ref} {ref} 0 R"
            ops.append(f"q {scale:g} 0 0 {scale:g} 0 0 cm /Fm{ref} Do Q")
        for _, x, y, size, text in (i for i in items if i[0] == "text"):
            ops.append(f"BT /F1 {size:g} Tf {x:g} {792 - y - size:g} Td ({text}) Tj ET")
        content = add(stream("", "\n".join(ops).encode("latin-1")))
        page_ids.append(add(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font "
            f"<< /F1 3 0 R >> /XObject << {xobjects} >> >> /Contents {content} 0 R >>"
            .encode()))
    objects[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{i} 0 R" for i in page_ids)
    objects[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode()
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objects) + 1, xref)
    return bytes(out)


def _captioned(box: tuple[float, float, float, float], seed: int) -> list[tuple]:
    """An image with three lines of the text layer over it (a schedule box's text)."""
    x0, y0, _, _ = box
    return [("image", box, _picture(200, 200, seed)),
            *(("text", x0 + 10, y0 + 20 + 15 * i, 9, f"Saturday {i + 4}:00 PM Vigil Mass, "
               "Main Church") for i in range(3))]


# Page 1: a schedule set as a picture (two touching images), a captioned image with a
# textless one touching it, an icon and a sliver. Page 2: a picture in a scaled form.
# Page 3: only an image.
SCHEDULE, SCHEDULE_FOOT = (50, 100, 300, 350), (50, 352, 300, 450)
CAPTIONED, BESIDE_IT = (320, 100, 560, 350), (320, 352, 560, 450)
DETECTION_PDF = [
    [("text", 50, 40, 10, NEWS),
     ("image", SCHEDULE, _picture(250, 250, 1)), ("image", SCHEDULE_FOOT, _picture(250, 98, 2)),
     *_captioned(CAPTIONED, 3), ("image", BESIDE_IT, _picture(240, 98, 4)),
     ("image", (50, 600, 60, 610), _picture(20, 20, 5)),        # an icon
     ("image", (575, 100, 595, 700), _picture(20, 600, 6))],    # a column's edge
    [("text", 50, 40, 10, NEWS), ("form", 0.5, [("image", (50, 50, 250, 250),
                                                 _picture(200, 200, 7))])],
    [("text", 50, 40, 10, "Page 3"), ("image", (0, 0, 612, 792), _picture(300, 400, 8))],
]


def _fractions(box: tuple[float, float, float, float]) -> tuple[float, ...]:
    x0, y0, x1, y1 = box
    return (x0 / 612, y0 / 792, x1 / 612, y1 / 792)


def _found(data: bytes) -> tuple[list[int], list[textless.TextlessImage]]:
    pdf = pdfium.PdfDocument(data)
    pages = {n: pdf[n - 1] for n in range(1, len(pdf) + 1)}
    try:
        return textless.find(pages)
    finally:
        for page in pages.values():
            page.close()
        pdf.close()


def test_images_the_text_layer_doesnt_cover_are_found_then_merged():
    image_only, found = _found(_layout_pdf(DETECTION_PDF))
    assert image_only == [3]
    boxes = [(a.page, pytest.approx(a.box, abs=0.002)) for a in found]
    # The schedule's two images are one; the captioned image is left out, but not the
    # textless one touching it (merged first, they would hold its text and both go); the
    # icon and the sliver are left out.
    assert boxes == [
        (1, _fractions((50, 100, 300, 450))),
        (1, _fractions(BESIDE_IT)),
        (2, _fractions((50, 50, 250, 250))),  # in the form's space, twice that
    ]
    assert found[0].where == "left" and found[2].where == "top left"
    assert found[0].share == pytest.approx(250 * 350 / (612 * 792), abs=0.001)


def test_images_are_trimmed_tagged_and_listed_once_with_every_page(tmp_path: Path):
    logo = _picture(200, 100, 11)
    framed = _picture(300, 300, 12, border=60)   # a white frame around it, trimmed off
    data = _layout_pdf([
        [("text", 50, 40, 10, NEWS), ("image", (50, 100, 250, 200), logo),
         ("image", (300, 300, 550, 550), framed),
         ("image", (50, 600, 250, 750), Image.new("RGB", (40, 30), "white"))],  # blank
        [("text", 50, 40, 10, NEWS), ("image", (300, 600, 500, 700), logo)],
        [("text", 50, 40, 10, "Page 3"), ("image", (0, 0, 612, 792), _picture(30, 40, 13))],
    ])
    r = pi.render(data, tmp_path, "abc", images=True)
    assert r["image_only"] == [3] and r["searched"] == [1, 2, 3]
    [im] = r["images"]
    assert pi.fits(im["width"], im["height"]) and im["dpi"] == pi.IMAGES_MAX_DPI
    assert Path(im["path"]).name == "abc-images-p1-2-110dpi.png" and im["pages"] == [1, 2]
    assert r["tokens"] == im["tokens"] == pi.image_tokens(im["width"], im["height"])
    by_page = {(t["page"], tuple(t["also_on"])): t for t in im["tiles"]}
    assert set(by_page) == {(1, (2,)), (1, ())}  # the logo once, with both pages
    region = [float(v) for v in by_page[1, ()]["region"].split(",")]
    x0, y0, x1, y1 = _fractions((300, 300, 550, 550))
    inset = 50 / 612  # the frame: 60 of 300 px across 250 pt
    assert x0 + inset - 0.02 <= region[0] and region[2] <= x1 - inset + 0.02
    assert region[0] > x0 and region[2] < x1 and region[1] > y0 and region[3] < y1
    tile = Image.open(im["path"]).convert("RGB")
    assert tile.getpixel((2, 2)) == (200, 0, 0)  # a tile's red tag
    # Only the page that is only an image: nothing to pack.
    assert pi.render(data, tmp_path, "abc", images=True, page=3)["images"] == []
    with pytest.raises(pi.PageImageError, match="--images packs"):
        pi.render(data, tmp_path, "abc", images=True, dpi=80)
    text = seed_cli._text_pages({**r, "parish": "st-x", "bulletin": "ab" * 32})
    assert "--page 1 --region" in text and "(also on p2)" in text
    assert "Only an image, so not tiled: p3" in text


def test_packing_stays_within_what_read_takes_whole():
    rng = random.Random(4)
    sizes = [(rng.randrange(60, 700), rng.randrange(60, 700)) for _ in range(14)]
    positions = pi.pack(sizes)
    assert positions is not None
    width, height = pi._used(sizes, positions)
    assert pi.fits(width, height)
    rects = [(x, y, x + w, y + h) for (w, h), (x, y) in zip(sizes, positions)]
    for i, a in enumerate(rects):
        for b in rects[i + 1:]:
            assert a[2] + pi.TILE_GUTTER_PX <= b[0] or b[2] + pi.TILE_GUTTER_PX <= a[0] \
                or a[3] + pi.TILE_GUTTER_PX <= b[1] or b[3] + pi.TILE_GUTTER_PX <= a[1]
    assert pi.pack([(1500, 1500), (1500, 1500)]) is None


def test_tiles_take_the_sharpest_dpi_that_fits_one_image_else_several():
    def tiles(count: int, size_pt: tuple[float, float]) -> list:
        return [pi._Tile(1, (0, 0, 1, 1), size_pt, []) for _ in range(count)]

    assert pi._plan(tiles(3, (200, 150)))[0] == pi.IMAGES_MAX_DPI
    dpi, sheets = pi._plan(tiles(16, (340, 340)))
    assert pi.IMAGES_MIN_DPI <= dpi < pi.IMAGES_MAX_DPI and len(sheets) == 1
    # A full-page flyer is shrunk to TILE_MAX_EDGE, not everything with it.
    assert max(pi._Tile(1, (0, 0, 1, 1), (612, 792), []).size(110)) == pi.TILE_MAX_EDGE
    dpi, sheets = pi._plan(tiles(30, (600, 780)))
    assert dpi == pi.IMAGES_MIN_DPI and len(sheets) > 1
    assert sorted(k for group, _ in sheets for k in group) == list(range(30))
    for group, positions in sheets:
        size = pi._Tile(1, (0, 0, 1, 1), (600, 780), []).size(dpi)
        assert pi.fits(*pi._used([size] * len(group), positions))
