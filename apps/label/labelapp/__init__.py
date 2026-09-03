"""Ground-truth labeling for bulletin event extraction.

Pure logic behind the labeling app in ``apps/label``: turning classifier runs
into review candidates, grouping model disagreements into single decisions,
persisting human labels, and scoring runs against them.

The HTTP server (``apps/label/server.py``) is a thin shell over this package,
so everything here is importable and testable on its own.
"""

from __future__ import annotations

__all__ = ["candidates", "corpus", "events", "score", "store"]
