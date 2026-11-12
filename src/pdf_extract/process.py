"""Bulletin process stage: read each live parish's new bulletins against its schedule.

A parish is live once its approved seed file is loaded (`pdf_extract.seeding.loader`).
From then on gpt-6-luna reads each of its new bulletins against the schedule
the parish is believed to keep, and the changes it proposes are checked and
applied (`pdf_extract.schedule.update`). A parish without an approved seed has
its bulletins fetched and stored, but no model call is made for it and the
site doesn't show it yet.
"""

from __future__ import annotations

import logging
from collections.abc import Collection

from pdf_extract.classifiers.schedule_update import OpenAIScheduleUpdater
from pdf_extract.schedule.store import unseeded_slugs
from pdf_extract.schedule.update import process_update_mode
from pdf_extract.storage import connect_db, get_parish_by_name, list_parishes

LOGGER = logging.getLogger(__name__)


def process_bulletins(
    *,
    parish_name: str | None = None,
    slugs: Collection[str] | None = None,
    concurrency: int = 5,
    run_id: str | None = None,
) -> dict[str, int]:
    """Update the schedules of the live parishes (all, or `parish_name` or `slugs`) with new bulletins.

    Parishes without an approved seed are left out: their bulletins stay
    unprocessed until the seed is approved, and then the parish's bulletins
    from after the seed are read.
    """
    LOGGER.info(
        "Starting process stage (parish_name=%s, slugs=%s, concurrency=%s)",
        parish_name or "*all*",
        "*all*" if slugs is None else len(slugs),
        concurrency,
    )
    conn = connect_db()
    try:
        scope: Collection[str] | None = slugs
        if parish_name:
            parish_row = get_parish_by_name(conn, parish_name)
            if not parish_row:
                LOGGER.warning("Parish not found: %s", parish_name)
                return {"unseeded_parishes": 0}
            scope = [parish_row["slug"]]
        elif slugs is not None:
            known = {row["slug"] for row in list_parishes(conn)}
            missing = sorted(set(slugs) - known)
            if missing:
                raise ValueError(f"Parish not found: {', '.join(missing)}")

        unseeded = unseeded_slugs(conn)
        if scope is not None:
            unseeded &= set(scope)
        if unseeded and parish_name:
            LOGGER.warning("Parish %s has no approved seed yet; nothing to process", parish_name)
        elif unseeded:
            LOGGER.info("Leaving %d parishes without an approved seed unprocessed", len(unseeded))

        stats = process_update_mode(
            conn, slugs=scope, run_id=run_id,
            updater=OpenAIScheduleUpdater(), concurrency=concurrency,
        )
    finally:
        conn.close()

    result = {"unseeded_parishes": len(unseeded), **stats}
    LOGGER.info("Process stage finished: %s", result)
    return result
