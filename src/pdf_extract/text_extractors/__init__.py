"""Registry of PDF → text extractors used by the text-based classifiers.

Extractors are registered by module and class name and imported only when
used: their dependencies (OCR engines, layout models) are heavy and live in
the optional `bench` dependency group (`uv sync --group bench`), which the
production pipeline does not install.
"""

from __future__ import annotations

import importlib

from pdf_extract.text_extractors.base import TextExtractor, page_header

# name -> (module under pdf_extract.text_extractors, class name)
REGISTRY: dict[str, tuple[str, str]] = {
    "pymupdf-layout": ("pymupdf_layout", "PyMuPDFLayoutExtractor"),
    "docling": ("docling_md", "DoclingExtractor"),
    "ocr-layout": ("ocr_layout", "OCRLayoutExtractor"),
}


def get_text_extractor(name: str) -> TextExtractor:
    if name not in REGISTRY:
        available = ", ".join(sorted(REGISTRY)) or "(none)"
        raise KeyError(f"Unknown text extractor {name!r}. Available: {available}")
    module_name, class_name = REGISTRY[name]
    try:
        module = importlib.import_module(f"pdf_extract.text_extractors.{module_name}")
    except ImportError as exc:
        raise ImportError(
            f"Text extractor {name!r} needs the bench dependencies: "
            f"run `uv sync --group bench` ({exc})"
        ) from exc
    return getattr(module, class_name)()


def available_text_extractors() -> list[str]:
    return sorted(REGISTRY)


__all__ = [
    "REGISTRY",
    "TextExtractor",
    "available_text_extractors",
    "get_text_extractor",
    "page_header",
]
