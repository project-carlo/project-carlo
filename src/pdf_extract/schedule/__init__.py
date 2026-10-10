"""Believed schedules: each parish's schedule kept as a log of changes.

The design is docs/schedule-state-plan.md. A parish with a `seed` revision is
in update mode: each of its new bulletins is shown to the model together with
the schedule we believe (the view), the model answers with the changes it
thinks the bulletin calls for, and code decides each one. A parish without a
seed stays in extract mode (`pdf_extract.process`), unchanged.

- `qualifiers`: weeks of the month and seasons, between the labels' forms and
  the database columns.
- `entries`: one schedule entry's content, its checks, identity and hash.
- `store`: the tables: entries, revisions, the change log and the fold into
  `current_schedule`, views, seeds and sightings.
- `policy`: the decision policy that applies or rejects each proposal.
- `history`: which week each of a parish's calls is for, and its high-water mark.
- `update`: the update-mode process stage.
- `edits`: hand edits (`human` revisions).
"""
