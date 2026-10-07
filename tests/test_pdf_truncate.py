from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_extract.pdf_truncate import ensure_truncated_pdf


def _make_pdf(path: Path, pages: int) -> None:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=72, height=72)
    with path.open("wb") as fh:
        writer.write(fh)


def _page_count(path: Path) -> int:
    return len(PdfReader(str(path)).pages)


def test_truncates_when_over_limit(tmp_path: Path) -> None:
    original = tmp_path / "bulletin.pdf"
    _make_pdf(original, pages=12)

    result = ensure_truncated_pdf(original)

    expected = tmp_path / "bulletin-truncated.pdf"
    assert result == expected
    assert expected.exists()
    assert _page_count(expected) == 10
    assert _page_count(original) == 12


def test_returns_original_when_at_or_under_limit(tmp_path: Path) -> None:
    original = tmp_path / "bulletin.pdf"
    _make_pdf(original, pages=8)

    result = ensure_truncated_pdf(original)

    assert result == original
    assert not (tmp_path / "bulletin-truncated.pdf").exists()


def test_is_idempotent_on_subsequent_calls(tmp_path: Path) -> None:
    original = tmp_path / "bulletin.pdf"
    _make_pdf(original, pages=15)

    first = ensure_truncated_pdf(original)
    first_mtime = first.stat().st_mtime_ns

    second = ensure_truncated_pdf(original)

    assert second == first
    assert second.stat().st_mtime_ns == first_mtime
    assert _page_count(second) == 10


def test_custom_max_pages(tmp_path: Path) -> None:
    original = tmp_path / "bulletin.pdf"
    _make_pdf(original, pages=6)

    result = ensure_truncated_pdf(original, max_pages=3)

    expected = tmp_path / "bulletin-truncated.pdf"
    assert result == expected
    assert _page_count(expected) == 3


def test_page_limits_override_per_parish(tmp_path: Path, monkeypatch) -> None:
    from pdf_extract import pdf_truncate

    limits = tmp_path / "bulletin_page_limits.csv"
    limits.write_text("parish_slug,max_pages,why\nlong-parish,12,schedule on page 11\n",
                      encoding="utf-8")
    monkeypatch.setattr(pdf_truncate, "PAGE_LIMITS_CSV_PATH", limits)
    assert pdf_truncate.max_pages_for("long-parish") == 12
    assert pdf_truncate.max_pages_for("other-parish") == pdf_truncate.MAX_BULLETIN_PAGES

    original = tmp_path / "bulletin.pdf"
    _make_pdf(original, pages=16)
    assert _page_count(ensure_truncated_pdf(original, max_pages=10)) == 10
    # A raised limit replaces a truncated copy made under the old one.
    assert _page_count(ensure_truncated_pdf(original, max_pages=12)) == 12

    monkeypatch.setattr(pdf_truncate, "PAGE_LIMITS_CSV_PATH", tmp_path / "missing.csv")
    assert pdf_truncate.max_pages_for("long-parish") == pdf_truncate.MAX_BULLETIN_PAGES


def test_page_limits_name_live_parishes_and_raise_the_limit() -> None:
    import csv

    from pdf_extract.pdf_truncate import MAX_BULLETIN_PAGES, read_page_limits

    root = Path(__file__).parents[1] / "data"
    limits = read_page_limits(root / "bulletin_page_limits.csv")
    with (root / "parishes.csv").open(encoding="utf-8") as fh:
        live = {row["slug"] for row in csv.DictReader(fh)}
    assert sorted(set(limits) - live) == []
    assert all(n > MAX_BULLETIN_PAGES for n in limits.values())
