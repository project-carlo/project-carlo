"""Filesystem locations shared by every module.

Kept apart from storage.py so low-level modules (the blob store) can import
them without pulling in the SQLite helpers.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Relative on purpose: commands run from the repo root, and tests chdir into a
# temporary directory to get an isolated data/ tree.
DATA_DIR = Path("data")
