# Corrections

Reviewed hand corrections to live parishes' believed schedules, one file per
correction: `<parish-slug>/<YYYY-MM-DD>-<short-name>.json`. Pipeline commands
load each file once, as a `human` revision, and skip and report one that no
longer fits the schedule.

Write one with `pnpm schedule add|modify|delete|apply|wrong-bulletin ...
--write-correction NAME`. The format, the guards and when a correction goes
live are in [docs/believed-schedules.md](../../docs/believed-schedules.md#corrections).
