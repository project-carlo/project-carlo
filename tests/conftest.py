from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# The labeling side app in apps/label is not part of the pdf_extract package, so
# its `labelapp` module has to be put on the path the same way the app itself
# does when cli.py is run directly.
LABEL_APP = ROOT / "apps" / "label"
if str(LABEL_APP) not in sys.path:
    sys.path.insert(0, str(LABEL_APP))
