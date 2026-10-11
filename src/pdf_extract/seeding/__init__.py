"""Seeding believed schedules: an agent drafts each parish's seed, a person approves it.

The design is docs/seeding-plan.md. A seed file (`data/seeds/<parish>.json`)
holds every slot the agent drafted, its sources, decision and rationale, and
the questions it left for a reviewer. The labeler's Seeds mode settles those,
and pipeline commands load the approved files as `seed` revisions, which
switches a parish to update mode (docs/schedule-state-plan.md).

- `files`: the file format: reading, writing and checking its shape.
- `checks`: a file against the database (`seed check`).
- `queries`: what the agent reads: bulletins, PDFs, extract mode's history,
  the batch to seed, and test runs on the labeled parishes.
- `calls`: second opinions from external models (`seed extract`, `seed ask`).
- `loader`: approved files into the database.
- `score`: a test run's drafts against the labels.
- `cli`: `pnpm seed`.
"""
