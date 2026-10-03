"""Reading bulletins off parishes' own websites (the "other" provider)."""

from pdf_extract.parish_sites.collectors import COLLECTORS
from pdf_extract.parish_sites.resolve import Recipe, Resolution, resolve_parish_site

__all__ = ["COLLECTORS", "Recipe", "Resolution", "resolve_parish_site"]
