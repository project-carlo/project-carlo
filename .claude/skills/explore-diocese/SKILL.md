---
name: explore-diocese
description: Record parishes, churches and ruled-out places for a diocese the pipeline does not cover yet, in data/dioceses/<diocese>/, using the `pnpm diocese` CLI. Use when asked to explore, research or add a new diocese, or to add, edit, look up or exclude parishes or churches outside the live data/*.csv files.
---

# Exploring a diocese

Full reference: `data/dioceses/README.md`. Read it before your first write.

Each diocese folder holds `parishes.json`, `churches.json` (the live CSV
columns, plus `explanation` and `sources`), `not-parishes.md` and
`not-churches.md`. Make every change through `pnpm diocese ...`, not by
editing the files. Every command prints JSON (use `pnpm -s` to
drop pnpm's banner when piping to `jq`). The CLI checks slug and website uniqueness against every
diocese and the live CSVs, and refuses any write that would add an error.

Loop:

1. `pnpm diocese list`. For a new diocese:
   `pnpm diocese init <slug> --name "..." --state XX --website URL --directory-url URL`.
2. Before adding anything, run `pnpm diocese search <words>`. It covers
   live data, every diocese and the exclusions. St./Saint and Sts./Ss. match
   each other.
3. Add the parish, then each of its churches. Missions count as churches;
   closed or merged buildings go in `not-church`:
   - `pnpm diocese parish add <d> --name ... --website ... --explanation "..." --source URL`
   - `pnpm diocese church add <d> --parish <parish-slug> --name ... --line1 ... --city ... --state ... --postal-code ... --explanation "..." --source URL`
4. Record what you ruled out, and why:
   `pnpm diocese not-parish add <d> --name ... --explanation "..."`
   (or `not-church`). Examples: campus ministries, chapels, shrines,
   non-Catholic churches with the same name, closed churches.
5. As you learn more, use `pnpm diocese <kind> edit <d> <slug> --append-explanation "..." --source URL`.
6. Before committing, run `pnpm diocese validate` and `uv run pytest tests/test_dioceses.py`.
   Update the diocese's `--notes` (`pnpm diocese edit <d> --notes ...`) with
   what has been covered and what hasn't.

Every explanation should say what the place is, how you know (which source
gave which fact), and what is still unconfirmed. Keep `name_verified` and
`address_verified` false until a bulletin or the parish's own site confirms
them. Never invent coordinates: leave them null for `geocode`.
