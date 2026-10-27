"""Seeding believed schedules: the onboarding factory drafts and approves each parish's seed.

The design is docs/seeding-plan.md. A seed file (`data/seeds/<parish>.json`)
holds every slot the agent drafted, its sources, decision and rationale, and
the questions it left for a reviewer. The factory's seed-review answers those
(`seed approve`; the owner changes an answer in the labeler's Seeds mode), and
pipeline commands load the approved files as `seed` revisions, which
switches a parish to update mode (docs/schedule-state-plan.md).

- `files`: the file format: reading, writing and checking its shape.
- `checks`: a file against the database (`seed check`).
- `queries`: what the agent reads: bulletins, PDFs and their text, extract
  mode's history and churches.
- `coverage`: a file's slots against extract mode's history (`seed diff`, and
  the history sources `finalize` attaches).
- `calls`: second opinions from external models (`seed extract`, `seed ask`).
- `loader`: approved files into the database.
- `cli`: `pnpm seed`.
"""
