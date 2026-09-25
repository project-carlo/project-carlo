from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pdf_extract.blobstore import CachedBlobStore, LocalBlobStore, set_store  # noqa: E402

R2_ENV_VARS = (
    "R2_ACCOUNT_ID",
    "R2_ACCESS_KEY_ID",
    "R2_SECRET_ACCESS_KEY",
    "R2_BUCKET",
    "R2_ENDPOINT_URL",
    "CARLO_REMOTE_WRITE",
)

PARISH_FIELDS = ["slug", "name", "website", "bulletin_provider", "provider_id"]
CHURCH_FIELDS = [
    "parish_id", "slug", "name", "line1", "line2", "city", "state", "postal_code",
    "latitude", "longitude", "name_verified", "address_verified",
]


@pytest.fixture(autouse=True)
def _isolated_blob_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Every test gets a private, local-only blob store and no R2 credentials."""
    for var in R2_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    store = CachedBlobStore(LocalBlobStore(tmp_path / "blobs"))
    set_store(store)
    yield store
    set_store(None)


@pytest.fixture
def blob_store(_isolated_blob_store: CachedBlobStore) -> CachedBlobStore:
    return _isolated_blob_store


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


@pytest.fixture
def pipeline_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Run the test from an empty directory, so data/ paths resolve inside it.

    Seeds one parish (`test-parish`) with one church (`test-church`).
    """
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    write_csv(
        work / "data" / "parishes.csv",
        PARISH_FIELDS,
        [{"slug": "test-parish", "name": "Test Parish", "website": "https://example.org"}],
    )
    write_csv(
        work / "data" / "churches.csv",
        CHURCH_FIELDS,
        [{
            "parish_id": "test-parish", "slug": "test-church", "name": "Test Church",
            "line1": "1 Main St", "city": "Rochester", "state": "NY", "postal_code": "14620",
        }],
    )
    return work
