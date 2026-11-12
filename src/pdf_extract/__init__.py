"""Fetch parish bulletins and keep each parish's schedule up to date from them."""

from pdf_extract.fetch import fetch_bulletins
from pdf_extract.process import process_bulletins

__all__ = [
    "fetch_bulletins",
    "process_bulletins",
]
