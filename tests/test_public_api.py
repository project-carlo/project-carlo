from pdf_extract import fetch_bulletins, process_bulletins


def test_public_exports_are_callable() -> None:
    assert callable(fetch_bulletins)
    assert callable(process_bulletins)
