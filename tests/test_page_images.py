"""`seed pages`' renders: sized for Read, cropped where asked, tiled into labelled sheets."""

from __future__ import annotations

import io
from pathlib import Path

import pytest
from PIL import Image, ImageStat
from pypdf import PdfReader, PdfWriter

from pdf_extract.seeding import page_images as pi

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
