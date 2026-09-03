"""The labeling session's view of the corpus: queue, ordering, and progress.

Loads the selected classifier runs once and memoizes each bulletin's review, so
paging through the queue does not re-derive candidates on every request. Call
`reload()` after re-running a classifier.
"""

from __future__ import annotations

from typing import Any

from labelapp import corpus, store
from labelapp.candidates import build_review

#: Queue orderings. `disagreement` is the default because a bulletin the models
#: read identically teaches you little per minute spent, and one they split on
#: teaches you a lot.
SORT_DISAGREEMENT = "disagreement"
SORT_QUICKEST = "quickest"
SORT_PARISH = "parish"
SORT_RECENT = "recent"
VALID_SORTS = (SORT_DISAGREEMENT, SORT_QUICKEST, SORT_PARISH, SORT_RECENT)

FILTER_ALL = "all"
FILTER_TODO = "todo"
FILTER_DISPUTED = "disputed"
FILTER_DONE = "done"
VALID_FILTERS = (FILTER_ALL, FILTER_TODO, FILTER_DISPUTED, FILTER_DONE)


class Workspace:
    """One labeling session over a fixed set of classifier runs."""

    def __init__(self, run_names: list[str]) -> None:
        self.run_names = list(run_names)
        self._reviews: dict[str, dict[str, Any]] = {}
        self.reload()

    # ── loading ─────────────────────────────────────────────────────────────
    def reload(self) -> None:
        """Re-read runs, bulletins, names and labels from disk."""
        self.runs = corpus.load_runs(self.run_names)
        self.bulletins = corpus.load_bulletins()
        self.church_names = corpus.load_church_names()
        self.parish_names = corpus.load_parish_names()
        self.churches_by_parish = corpus.churches_by_parish()
        self.labels = store.load_labels()
        self._reviews.clear()

    def reload_labels(self) -> None:
        """Re-read only the labels file; reviews are unaffected by labeling."""
        self.labels = store.load_labels()

    # ── bulletins under review ──────────────────────────────────────────────
    def reviewable_urls(self) -> list[str]:
        """Bulletins at least one selected run produced output for.

        A run only covers the latest bulletin per parish, so this is far smaller
        than metadata.json and is the only set that can be labeled against.
        """
        urls: set[str] = set()
        for run in self.runs.values():
            urls |= run.covered
        return sorted(url for url in urls if url in self.bulletins)

    def review(self, source_url: str) -> dict[str, Any] | None:
        """Memoized candidate breakdown for one bulletin."""
        if source_url in self._reviews:
            return self._reviews[source_url]
        bulletin = self.bulletins.get(source_url)
        if bulletin is None:
            return None
        review = build_review(bulletin, self.runs, self.run_names)
        self._reviews[source_url] = review
        return review

    # ── queue ───────────────────────────────────────────────────────────────
    def summary(self, source_url: str) -> dict[str, Any] | None:
        """Queue-row view of one bulletin: size of the job and how far it got."""
        review = self.review(source_url)
        if review is None:
            return None
        label = self.labels.get(source_url)
        decided = store.decided_ids(label)

        disputed_ids = {row["key_id"] for row in review["singletons"]}
        for conflict in review["conflicts"]:
            disputed_ids |= {row["key_id"] for row in conflict["variants"]}
        undecided = len(disputed_ids - decided)

        return {
            "bulletin_source_url": source_url,
            "parish_slug": review["parish_slug"],
            "parish_name": self.parish_names.get(review["parish_slug"], review["parish_slug"]),
            "published_date": review["published_date"],
            "fetched_at": review["fetched_at"],
            "has_pdf": review["has_pdf"],
            "runs": review["runs"],
            "candidate_count": review["candidate_count"],
            "agreed_count": review["agreed_count"],
            "disputed_count": review["disputed_count"],
            "conflict_count": review["conflict_count"],
            "wrong_bulletin_runs": review["wrong_bulletin_runs"],
            "status": label["status"] if label else None,
            "undecided_count": undecided,
            "labeled_at": label.get("labeled_at") if label else None,
            "accepted_count": len(label.get("events") or []) if label else 0,
        }

    def queue(
        self,
        *,
        sort: str = SORT_DISAGREEMENT,
        which: str = FILTER_ALL,
        parish: str | None = None,
    ) -> list[dict[str, Any]]:
        rows = [
            summary
            for url in self.reviewable_urls()
            if (summary := self.summary(url)) is not None
        ]
        if parish:
            rows = [row for row in rows if row["parish_slug"] == parish]
        rows = [row for row in rows if _passes(row, which)]
        key, reverse = _sort_key(sort)
        rows.sort(key=key, reverse=reverse)
        return rows

    def progress(self) -> dict[str, Any]:
        """Corpus-wide counts for the header."""
        rows = [
            summary
            for url in self.reviewable_urls()
            if (summary := self.summary(url)) is not None
        ]
        complete = [row for row in rows if row["status"] == store.STATUS_COMPLETE]
        started = [row for row in rows if row["status"] == store.STATUS_IN_PROGRESS]
        skipped = [row for row in rows if row["status"] == store.STATUS_SKIPPED]
        return {
            "bulletins": len(rows),
            "complete": len(complete),
            "in_progress": len(started),
            "skipped": len(skipped),
            "unlabeled": len(rows) - len(complete) - len(started) - len(skipped),
            "disputed_total": sum(row["disputed_count"] for row in rows),
            "disputed_undecided": sum(row["undecided_count"] for row in rows),
            "labeled_events": sum(row["accepted_count"] for row in complete),
        }

    def next_url(self, after: str | None, **queue_kwargs: Any) -> str | None:
        """The URL following `after` in the current queue, wrapping to the front."""
        rows = self.queue(**queue_kwargs)
        if not rows:
            return None
        urls = [row["bulletin_source_url"] for row in rows]
        if after in urls:
            index = urls.index(after)
            return urls[(index + 1) % len(urls)]
        return urls[0]


def _passes(row: dict[str, Any], which: str) -> bool:
    if which == FILTER_TODO:
        return row["status"] not in (store.STATUS_COMPLETE, store.STATUS_SKIPPED)
    if which == FILTER_DISPUTED:
        return row["undecided_count"] > 0
    if which == FILTER_DONE:
        return row["status"] == store.STATUS_COMPLETE
    return True


def _sort_key(sort: str) -> tuple[Any, bool]:
    """Return the sort key for a queue ordering, and whether to reverse it."""
    if sort == SORT_QUICKEST:
        # Cheapest unfinished bulletins first: good for building momentum, and
        # for clearing the long tail once the interesting ones are done.
        return (
            lambda row: (
                row["status"] == store.STATUS_COMPLETE,
                row["undecided_count"] == 0,
                row["undecided_count"],
                row["candidate_count"],
                row["bulletin_source_url"],
            ),
            False,
        )
    if sort == SORT_PARISH:
        return (
            lambda row: (
                row["parish_slug"],
                row["published_date"] or "",
                row["bulletin_source_url"],
            ),
            False,
        )
    if sort == SORT_RECENT:
        return (
            lambda row: (
                row["published_date"] or "",
                row["fetched_at"] or "",
                row["bulletin_source_url"],
            ),
            True,
        )
    # SORT_DISAGREEMENT: most unresolved disagreement first, finished last.
    return (
        lambda row: (
            row["status"] == store.STATUS_COMPLETE,
            -row["undecided_count"],
            -row["disputed_count"],
            row["candidate_count"],
            row["bulletin_source_url"],
        ),
        False,
    )
