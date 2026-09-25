# Dioceses being explored

A staging area for dioceses the pipeline does not cover yet. Record parishes
and churches here as you find them, together with how you know each one is
right. Also record the places that looked like a parish or church but are not,
and why, so the next agent does not have to look into them again.

Nothing here is read by `fetch`, `process` or the web app. When a diocese is
ready, `export` writes it out in the format of `data/parishes.csv` and
`data/churches.csv`, and those rows get appended to the live files.

## Layout

```
data/dioceses/<diocese>/
  diocese.json      name, state, website, parish directory URL, exploration notes
  parishes.json     parishes to add
  churches.json     their churches (worship sites, missions included)
  not-parishes.md   looked like a parish, isn't: why
  not-churches.md   looked like a church, isn't: why
```

### `parishes.json`

These are the columns of `data/parishes.csv`, plus `explanation` and `sources`:

```json
{
  "slug": "holy-spirit-hamilton",
  "name": "Holy Spirit Parish",
  "website": "https://holyspiritrcparish.org",
  "bulletin_provider": "",
  "provider_id": "",
  "explanation": "One parish with four worship sites along Route 20 ...",
  "sources": ["https://holyspiritrcparish.org/"]
}
```

`bulletin_provider` is one of `parishes_online`, `ecatholic`, `discover_mass`,
`other`, `google_drive` or `no_bulletin`, or `""` while it is unknown.
`parishes_online` and `discover_mass` also need a `provider_id`.

### `churches.json`

These are the columns of `data/churches.csv`, plus `explanation` and `sources`.
`parish_id` is the parish's slug. The verified flags are booleans and the
coordinates are numbers or `null`:

```json
{
  "parish_id": "holy-spirit-hamilton",
  "slug": "st-marys-hamilton",
  "name": "St. Mary's Church",
  "line1": "16 Wylie Street", "line2": "", "city": "Hamilton", "state": "NY", "postal_code": "13346",
  "name_verified": false, "address_verified": false,
  "latitude": null, "longitude": null,
  "explanation": "...",
  "sources": ["https://..."]
}
```

### The explanation

Write it for the next agent, who will want to know:

- **What it is:** a single-church parish, one of several worship sites, a
  mission, a merger of older parishes.
- **How you know:** which page gave you the address and website, and whether
  that was the parish's own site, the diocese's, or a third-party directory.
- **What is still open:** anything unconfirmed, such as a bulletin provider you
  guessed or churches not recorded yet.

Put URLs in `sources`, not only in the text.

### `not-parishes.md` / `not-churches.md`

One section per place. The tool writes these files, but you can also edit them
by hand if you keep this shape:

```markdown
## Alibrandi Catholic Center (St. Thomas More Chapel)
- **Slug:** alibrandi-catholic-center
- **Website:** https://www.sucatholic.org
- **Address:** 110 Walnut Place, Syracuse, NY 13210
- **Parish:** (related parish slug, if any)
- **Source:** https://syracusediocese.org/campus-ministries
- **Added:** 2026-09-25

Why it is excluded, in as many paragraphs as it takes.
```

Typical entries: campus ministries, hospital or convent chapels, shrines
without a parish, non-Catholic churches with the same name, closed or merged
churches that old directories still list, and a diocese office that shows up
in searches.

## The `diocese` command

Use it for every common operation. Every command prints JSON. Writes are
checked first and refused, with nothing written, if they would add a
validation error. A change is not blocked by an error that was already there,
but `validate` still reports it.

```bash
pnpm diocese list                                  # dioceses and record counts
pnpm diocese init buffalo --name "..." --state NY --website URL --directory-url URL
pnpm diocese edit <diocese> --notes "..."          # change diocese.json
pnpm diocese show <diocese>                        # parishes > churches, plus exclusions

pnpm diocese search st marys hamilton              # every diocese + live CSVs + exclusions
pnpm diocese search "our lady" --diocese syracuse --kind church

pnpm diocese parish add <diocese> --name "..." --website URL \
  [--slug s] [--bulletin-provider p] [--provider-id id] \
  --explanation "..." --source URL [--source URL ...]
pnpm diocese church add <diocese> --parish <parish-slug> --name "..." \
  --line1 "..." --city "..." --state NY --postal-code 12345 \
  [--latitude N --longitude N] [--name-verified true] [--address-verified true] \
  --explanation "..." --source URL
pnpm diocese not-parish add <diocese> --name "..." --explanation "..." [--website URL] [--address "..."] [--source URL]
pnpm diocese not-church add <diocese> --name "..." --explanation "..." [--parish slug] [--address "..."] [--source URL]

pnpm diocese <kind> list   <diocese> [--parish slug]
pnpm diocese <kind> get    <diocese> <slug>        # a parish comes with its churches
pnpm diocese <kind> edit   <diocese> <slug> [--field value ...] \
  [--append-explanation "..."] [--source URL] [--clear-sources] [--new-slug s]
pnpm diocese <kind> remove <diocese> <slug>        # parish: --cascade removes its churches

pnpm diocese validate [<diocese>]                  # exits 1 on errors
pnpm diocese export <diocese> --out-dir <dir>      # parishes.csv + churches.csv, live format
```

`<kind>` is `parish`, `church`, `not-parish` or `not-church`. On `edit`, flags
you leave out keep their values, and `--field ""` clears a field. `--slug` on
`add` defaults to the name, slugified. Add `--help` to any command for its
full flag list. pnpm prints a banner before the JSON, so use `pnpm -s diocese ...`
when piping into `jq`. Without pnpm, run `uv run python -m pdf_extract diocese ...`.

### What `validate` checks

Errors, which block writes and `export`:

- Slugs are lowercase and hyphenated, and unique within the file.
- Parish slugs, church slugs and parish websites are unique across every
  diocese **and** the live CSVs, because the database requires it.
- Every church's `parish_id` is a parish in the same diocese.
- Name and explanation are present, and a parish has a website.
- Known `bulletin_provider`; two-letter state; five-digit ZIP; coordinates in
  range and set together.
- No slug is both kept and excluded.

Warnings: no sources; no churches for a parish; missing address parts; unknown
bulletin provider or missing `provider_id`; and, on `add`, a name that matches
something already excluded.

## Workflow for a new diocese

1. Run `pnpm diocese list`. If the diocese is new, run `init` with the
   diocese's parish directory URL, and record in `--notes` how far you got.
2. For each parish you find, run `search` first. It covers the live data and
   the exclusions, so it catches duplicates and places already ruled out.
3. Add the parish, then its churches. Include missions and every worship
   site, and leave out closed buildings: those go in `not-churches.md`.
4. Anything you rule out goes in `not-parish` / `not-church` with the reason.
5. Run `pnpm diocese validate` before committing. `pytest` runs it over
   everything in `data/dioceses/` too.

When a diocese is complete, run `export` and review the CSVs. Then append the
rows to `data/parishes.csv` / `data/churches.csv` and run `pnpm db:create` to
confirm the constraints hold.
