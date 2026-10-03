# Exploring a diocese

`data/dioceses/<diocese>/` is where a diocese the pipeline does not cover yet gets worked
out: which bulletins it publishes, which buildings hold Mass, which places were looked at
and ruled out, and the evidence for every one of those calls. `pnpm diocese promote` then
writes the rows into `data/parishes.csv` and `data/churches.csv`.

The files are kept after promotion. They are the record of **why each live row is what it
is**, and that is what they are written for: someone auditing a row a year from now, human
or agent, should be able to open its file, follow the evidence, and confirm or overturn it
in a few minutes.

This guide comes out of the Diocese of Buffalo expansion (PR #14): 72 parishes and 151
churches, reworked several times. Most of its mistakes were in **structure** (which rows are
one bulletin), not coverage, and most of its time went on re-deriving things that were
never written down. The rules and the file layout below are there to avoid both.

- [The model](#the-model): what a parish row and a church row are
- [Files](#files): layout and fields
- [The explanation](#the-explanation): what to write, and what an auditor needs
- [Sources](#sources): what to look for, and how far to trust each
- [Method](#method): the order to work in, cheapest first
- [Traps](#traps): the things that produced confident wrong answers in Buffalo
- [Commands](#commands)

## The model

**One parish row = one bulletin.** A `parish` row is a bulletin publisher, because the
pipeline reads bulletins: its `website` is where that bulletin can be found, and its churches
are the worship sites the bulletin's Mass schedule covers. The diocese's own units do not
decide this:

- A *family*, *cluster* or *pastorate* of several canonical parishes that publishes one
  bulletin is **one** row with several churches.
- A family whose members each publish their own bulletin is **several** rows.
- A canonical merger does not merge rows, and a rescinded one does not split them. Buffalo
  had both: Holy Cross and Our Lady of Hope share Family #23 but are separate rows, while
  St. John and St. Mary of the Angels in Olean had their merger rescinded and still publish
  one bulletin (one row). Bulletins change too: Fourteen Holy Helpers kept its own bulletin
  after merging into Queen of Heaven, but by September 2026 it shared the Blessed Family #7
  bulletin with Queen of Heaven and St. John Vianney (one row).
- A family's size tells you nothing. Buffalo's families went every way: some single
  bulletins over four parishes, some with every member separate.

Record the grouping in `group` anyway: `audit` uses it to find rows that may be one bulletin.

**One church row = one place where Mass is celebrated publicly now.** Missions, oratories,
chapels, shrines and campus chapels count, and so does a building with Mass four times a
year. What the place is called doesn't matter; whether Mass happens there does. A building
whose parish closed can still be a worship site. In Buffalo, every closure source said
St. George (West Falls) had closed, but the family's own schedule still listed a Saturday
Mass there.

**Everything else goes in `excluded/`, with a reason** (`pnpm diocese new excluded --help`
lists them):

| reason | use it for |
|---|---|
| `closed` | no Mass any more: closed, merged away, sold, demolished. Put the date in `last_mass` when a source gives it |
| `no-bulletin` | **open**, with public Mass, but nothing the pipeline could read. Don't file these under `closed`; that list has to stay a record of what actually shut down |
| `no-public-mass` | offices, schools, pregnancy centers, cemeteries, private convent or hospital chapels |
| `not-catholic` | a same-named Orthodox, Episcopal, Lutheran... church |
| `other-jurisdiction` | another diocese or an Eastern Catholic eparchy (GCatholic lists these in the territory) |
| `other` | none of the above; the explanation says what |

An exclusion states a fact about a place, so it needs a source that states it. If
everything points to closed but nothing says so, it goes in `open/`, not `excluded/`.

**Settled policy** (the data owner decided these during the Buffalo work; apply them rather
than reopening them):

1. A social-media page can be a parish `website` if the bulletin is actually posted there.
   A page that merely exists is not enough.
2. A closed church is removed from `churches.csv` (promote does this for a promoted church
   moved to `excluded/`), and its page on the site is allowed to 404. There is no `closed`
   column.
3. The dataset tracks real worship sites, not a diocesan list. A place with solid evidence
   goes in whether or not the diocese's directory lists it.

## Files

```
data/dioceses/<diocese>/
  diocese.md            sources, their quirks, rules settled for this diocese, a dated log
  parishes/<slug>.md    one per bulletin publisher      -> a data/parishes.csv row
  churches/<slug>.md    one per worship site            -> a data/churches.csv row
  excluded/<slug>.md    looked at and ruled out, with a reason
  open/<slug>.md        found, not decided: what is known and what would settle it
  rosters/<name>.json   outside lists the diocese is measured against (written by tools)
```

Every record is YAML frontmatter plus a Markdown body. The slug is the file name. Edit the
files directly: create them with `pnpm diocese new ...` (which fills in the frontmatter and
an explanation template), write the explanation and evidence, and run `pnpm diocese
validate`. Use the commands for anything that touches several files: `merge`, `rename`,
`exclude`, `coverage --link`, `promote`. Those are refused, with nothing written, if they
would add a validation error.

```markdown
---
name: Cathedral of the Immaculate Conception
website: https://cathedralsyracuse.org
bulletin_provider: parishes_online
provider_id: cathedral-of-the-immaculate-conception-13202
publication: [po-org:cathedral-of-the-immaculate-conception-13202, lpi:0018000000Qbz9eAAB, po-container:06/0091]
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/06/0091/20260920B.pdf
  seen: 2026-09-25
  quote: 'Weekend: Sat. 5:10 pm … Sun. 7:30 am, 9:45 am, 5:10 pm'
  note: Masthead of the 20 September 2026 issue, page 1. Names the cathedral alone.
---

## Publisher

The cathedral publishes its own weekly bulletin through ParishesOnline...
```

`syracuse/` is a complete worked example: a whole diocese explored in one pass by eight
parallel agents, one per region, including exclusions of every kind, parishes folded into
shared bulletins, and a canonical merger dated from the news rather than a guess.

### Fields

Every kind has `name`, `evidence`, and optionally `revisit` (the next thing to check) with
`revisit_after` (a date). `todo` lists revisits that are due.

**parish**
- `website`: where the bulletin can be found (required, unique across the dataset).
- `bulletin_provider`: `parishes_online`, `ecatholic`, `discover_mass`, `other`,
  `google_drive` or `no_bulletin`. `fetch` reads ParishesOnline and DiscoverMass by
  `provider_id` (the org slug from `parishesonline.com/organization/<slug>`, the church slug
  from `discovermass.com/church/<slug>/`). It reads eCatholic, `other` and `google_drive`
  from `website`, so for eCatholic the website has to be the eCatholic-hosted site, and for
  `google_drive` it has to link the shared folder. For `other` and `google_drive`,
  `provider_id` may pin how to read the site, as a recipe: a collector, the bulletin page,
  or both (`page-pdfs https://example.org/bulletins`). Run
  `pnpm fetch:check -- --parish <slug>` and record the `recipe` it prints once its pick is
  this week's bulletin (see "How the `other` resolver reads a site" in the main README).
- `publication`: ids of the bulletin itself, as `scheme:value`. **Two parish rows may never
  share one**, and `validate` enforces that across every diocese: it catches "one bulletin
  carried as several rows", a mistake that shows up in no other check. Record every form
  you find: `po-container:14/0434`, `po-org:<slug>`, `lpi:<18-character id>` (all three are
  one ParishesOnline bulletin), `ecatholic:<site id>`, `discovermass:<slug>`, or
  `url:<page>` for a self-hosted bulletin.
- `group`: the diocese's grouping, e.g. `Family #31`.
- `replaces`: slugs of rows merged or renamed into this one. Maintained by `merge` and
  `rename`; `promote` deletes those live rows.

**church**
- `parish`, the address fields, `latitude`/`longitude` (or `null`, and `pnpm geocode` fills
  them after promotion).
- `coordinates_from`: `gcatholic-plus-code` (building-precise), `osm-node`,
  `diocese-directory`, `parishes-online-org`, `nominatim`, `geocode-stage` or `manual`.
- `name_verified` / `address_verified`: true only when two independent sources agree (the
  parish's bulletin and its own site are one source; OSM, GCatholic and the diocese are
  others). **When sources disagree, leave the flag false and write down the disagreement.**
  Don't pick a favourite without saying so.
- `roster`: the roster entries this place is, as `<roster>:<id>`. Written by
  `coverage --link` or by hand.

**excluded**: `reason`, address fields, `parish` (related parish, if any), `last_mass`,
`decided`, `roster`.

**open**: address fields, `parish`, `roster`, and a required `revisit`.

**evidence** items: `url`, `seen` (the date you read it), and `quote` and/or `note`. A
`quote` is copied **verbatim** from the page (`…` marks a gap). `pnpm diocese recheck`
fetches each URL and checks the quote is still there, so write quotes that can be found.

## The explanation

The body of the file is for the person who has to check the row later. They have the file
and a browser, and the diocese has moved on since you wrote it. Write so they can re-check
each claim and see where your judgement came in.

**Every claim has a source, a date and the words.** "The 20 September 2026 masthead (page 1)
names the cathedral alone" can be checked. "Single-church parish per the diocese" can't be.
Bulletin PDFs at dated URLs never change, which makes them the best evidence there is; a
homepage will be different next month.

**Say what you read, not what you concluded from.** "The family's Mass schedule lists five
buildings and not this one" is evidence. "Not listed" is only absence, and absence is weak:
Buffalo's diocesan pages, its masterlist and GCatholic all omitted an open oratory at once.
When your evidence is absence, list what you checked.

**When sources disagree, write down all of them.** Give each version, which source says it,
which one you followed and why, and what would settle it (for example, "the office next
door is probably number 24"). Buffalo's disputed rows were only defensible because this was
written down.

**Separate what you checked from what you inferred.** "One bulletin for all four churches"
is a claim. "Inferred from the merger; no bulletin read" is a different claim, and the reader
needs to know which one they're looking at. Put anything you couldn't check under *Not yet
confirmed*, with the step that would settle it. If it has a date ("the parish says it closes
after Labor Day"), put it in `revisit_after`. A deferral with a date and a next step gets
done. "Someone should look at this" doesn't.

**Record what you ruled out.** If a directory still lists a building this parish no longer
uses, say so in the parish's *Worship sites* and give that building its own `excluded/`
record. Otherwise the next person spends an hour rediscovering it.

The templates `new` writes give each kind its headings:

- **parish:** *Publisher* (who publishes, which issue you read, quoted), *Worship sites*
  (why these churches, and what the diocese lists that is not here), *Website and bulletin
  provider*, *Not yet confirmed*.
- **church:** *Holds Mass* (current, dated), *Name and address* (sources, agreement,
  coordinates).
- **excluded:** *Why it is excluded* (the claim, quoted and dated), *What would change
  this*.
- **open:** *What is known*, *Why it is not decided*.

Validation treats a leftover `TODO` or an empty explanation as incomplete, and `promote`
refuses until none are left.

A good exclusion, from Buffalo:

> **St. Thomas Aquinas, 450 Abbott Rd, Buffalo — closed, last Mass 2024-11-09.** The 13 Oct
> 2024 issue of the Catholic Family of South Buffalo bulletin (container 14/0940) still names
> it in the masthead and announces "the closing Mass at St. Thomas Aquinas: Saturday,
> November 9th at 11:30 AM"; the 10 Nov masthead has dropped it; the 17 Nov issue says "Now
> that St. Thomas Aquinas has been closed".

A bad one: *"Closed. Part of the Road to Renewal consolidation."* That was a plan, and in
Buffalo the plan was wrong about several churches still holding Mass two years later.

## Sources

Look for these for every diocese and record in `diocese.md` what you found, where it is, and
how far it can be trusted there. Diocese-wide lists answer most questions in a few fetches.
Buffalo went from 62% to 79% coverage in one session by reading two diocesan pages nobody
had opened.

| source | good for | lags on |
|---|---|---|
| **A current bulletin** | who publishes, which buildings have Mass, closures dated to the week | nothing, **so it wins every disagreement** |
| The parish or family's own site | Mass schedule, "our churches" page (often lists closures with dates) | old domains live on after a merger |
| The diocese's parish directory / finder | addresses, coordinates, homepages, often the canonical structure in the names | closures (Buffalo's listed a church **demolished in 2023** and one closed in **2008**), dead homepages |
| The diocese's family/cluster list | which parishes are grouped, and their worship sites | closures; and a group is not a bulletin |
| The diocese's Mass-times pages | finding places no directory lists (Buffalo found a shrine with eleven weekend Masses) | a closed church was still listed thirteen days after its last Mass |
| Closed-parish / sacramental-records index | which parishes ended and where their records went | says a *corporation* ended, never that a building is shut |
| Pastoral plans, closure announcements | leads for what to check | they're plans; several of Buffalo's never happened |
| GCatholic | a second independent address, a Plus Code on the building, Eastern churches flagged | closures; may omit the cathedral |
| ParishesOnline / eCatholic / DiscoverMass | the bulletin itself, when the parish site blocks you | account names accumulate old members |
| OpenStreetMap | whether a building exists, independent coordinates | street numbers sometimes |
| News, Mass Mob sites | dating a closure, reasons | whatever they don't cover |

For structure, a current bulletin beats the family list, which beats the directory. The
plan says what the diocese intended; the bulletin says what happened.

## Method

Work in this order and only fall through when a step can't answer. Commit as you go.

1. **Set up.** `pnpm diocese init <slug> --name ... --state XX --gcatholic <key>`. Fill in
   `diocese.md` *Sources* as you find each list.
2. **Get rosters.** `pnpm diocese roster fetch <d> gcatholic`, and the diocese's own
   directory: `roster fetch <d> wpsl <finder URL>` if it runs WP Store Locator, otherwise
   scrape it with a throwaway script and `roster import <d> directory list.json`. Import the
   family list and Mass-times pages the same way (`group` = the family). Rosters are what you
   measure against. They aren't evidence on their own, and none of them is the diocese.
3. **Read structure before researching parishes.** From the family list and the directory,
   sketch which parishes might share a bulletin. For each group, find its bulletin (step 4)
   before creating rows. It's cheaper than creating four rows and merging them later.
4. **Find each bulletin.** Two or three requests usually settle a publisher:
   - `pnpm diocese probe url <site>` shows whether the site is alive, where it redirects,
     whether it has been taken by a squatter, and which publication ids it embeds.
   - `probe po <org slug or LPi id>` returns a ParishesOnline organization's address, its
     publication ids and its latest issues. An LPi site's `publicationWidget?id=` is the
     organization id, so a widget found on a parish site leads straight to its container.
   - `probe container 14/0434 --pages 3` walks back through the Sundays and prints the
     latest masthead. `--all --step 4` gives one issue a month: **read one masthead and you
     have a snapshot; read two and you have a changelog** of who joined and who left.
   - `probe pdf <url> --grep "<church or code>"` gets the text of any bulletin. Grep a
     family bulletin's Mass-schedule codes across monthly issues to date a closure to the
     week, then look for the issue that announces it.
   - When a parish site blocks every fetcher, DiscoverMass often serves the same PDF, one
     listing per church.
5. **Decide one bulletin or several.** Merge only when the family's own bulletin is current
   **and** each member's own old channel (container, widget, bulletin page) has gone silent,
   or the member says itself that it has folded in ("St. Philomena Parish is now part of the
   ... Family of Parishes ... Check Bulletin"). **One live member channel means no merge.**
   If you can't find a member's bulletin, that isn't evidence that it shares someone else's,
   so keep its row and say so. Record `publication` ids on every row you settle.
6. **Add churches under their publisher** with `new church <d> --parish <p> --from
   gcatholic:<id> --from directory:<id>`. This prefills the address and Plus Code
   coordinates, links both entries, and adds them as evidence. Confirm Mass against the
   current bulletin or schedule before writing *Holds Mass*.
7. **Account for the rest.** `pnpm diocese coverage <d>` lists every roster entry that is
   not yet a church, an exclusion or an open question. `--link` saves the automatic matches
   on their records. For each one left, link it by hand (add `<roster>:<id>` to the record's
   `roster`), or create the church, exclusion or open question. Expect most unmatched entries
   to be naming noise (hamlet vs town, parish name vs building name, "St. Jude" vs "St. Jude
   Chapel"). Add hamlet spellings to `city_aliases` in `diocese.md`. Once linked, an entry
   stays resolved, so the next run only shows new ones.
8. **Audit structure.** `pnpm diocese audit <d> [--fetch]` lists groups whose churches span
   several parish rows, and which ones have no `publication` ids to tell them apart. **Run it
   every session.** It is the only check for Buffalo's most persistent mistake. "Every
   family has been read" was declared twice while four families that each publish one
   bulletin sat in the data as fourteen rows. Collapsing them changed no church row and no
   coverage number, which is why nothing else noticed.
9. **Close the session.** `pnpm diocese validate <d>`, `pnpm diocese todo <d>`, a dated line
   in `diocese.md`'s *Log* with the coverage numbers, and a commit.

**Promotion:** when `todo` shows no errors or incomplete records, run `pnpm diocese promote
<d> --dry-run`, read it, then `pnpm diocese promote <d>` and `pnpm test`. The next pipeline
command seeds the new rows into the database.
Promotion appends new rows, updates promoted ones, and deletes live rows the diocese has
retired (merged, renamed or excluded). Retiring a church deletes its events, and retiring a
parish deletes its bulletins and the events read from them, even for churches moved to another
parish. The dry run lists the churches that would lose events (`removed_rows_with_events`).
Removals don't go live on merge: deploys keep serving the published data, and the next weekly
run is held for review. Publishing that run is what applies them. It also keeps coordinates and flags that `geocode` and
`verify` filled in. Keep editing the records after promotion and promote again. Don't delete
a promoted record: exclude it or merge it, or its live row will be orphaned.

`pnpm diocese recheck <d>` re-fetches every quoted source. Run it when auditing, or before
promoting a diocese that was researched a while ago.

## Traps

Each of these produced a confident wrong answer in Buffalo at least once.

- **A publisher's account name is not a membership list of the present.** LPi footers and
  ParishesOnline org names build up over time: one container's footer still named two
  parishes it served under a previous owner and left out one it serves now. Read the
  masthead.
- **LPi ids are 18 characters** (`0018000000Qbyz4AAB`). Matched as digits, every id in a
  diocese truncates to `00180000` and unrelated parishes look like one bulletin.
  `validate` rejects the truncated form.
- **Comparing files doesn't answer "same bulletin?"**. A parish that hosts its family's
  bulletin itself serves a file with a different size, hash and even page count. Compare
  mastheads.
- **A missing ParishesOnline issue answers 403, not 404.** "403 every week" means the
  container is dead only if the same probe finds issues in a container you know is live.
- **A silent container means a fold-in only if a live one exists to fold into.** Otherwise
  the publisher just changed.
- **The masthead is often not on page 1.** LPi puts a generic cover reflection first. A
  container that looks anonymous is usually just a page short.
- **Lapsed parish domains get squatted.** Two Buffalo domains were taken by one
  online-slots network; one redirect was first read as a merger into a family site. `probe url` checks for the
  vocabulary; read any redirect target before acting on it.
- **A DNS failure can be transient**, and a bare domain can fail where `www.` works.
  `probe url` retries both before reporting DEAD-DNS.
- **The diocese's own homepage for a parish can be dead**, and so can the directory's. Check
  the URL before you store it.
- **Directory street numbers are sometimes PO boxes** ("1154 Lower College Dr" was
  "PO Box 1154"), and one building can have an address on two streets.
- **A summarizing fetch tool is not a source.** For a quote, read the page itself (`probe
  pdf`, `curl`, the recheck tool). One summary moved a 2020 merger to 2026. The article's
  weekdays gave the real year.
- **A hand-written `quote:` or `note:` containing ": " breaks the YAML.** Quote the value
  (`note: 'Page 1: the masthead'`). `validate` catches it, but only after the whole file is
  unreadable, which in Albany briefly left three churches pointing at a "missing" parish.
- **Coverage measures the roster.** A place the roster doesn't list moves no number, and an
  oratory with no weekend Mass can be missing from every list and still be open. `coverage`
  lists your churches that are in no roster; each needs an explanation, not deletion.

## Commands

`pnpm diocese <command> --help` gives every flag. Output is JSON (`pnpm -s` drops pnpm's
banner for `jq`). Without pnpm: `uv run python -m pdf_extract diocese ...`.

```bash
pnpm diocese list | show <d> | todo <d> | validate [<d>]
pnpm diocese init <d> --name "..." --state NY [--website URL] [--gcatholic key]
pnpm diocese search <words> [--diocese d|live] [--kind parish|church|excluded|open]

pnpm diocese new parish   <d> --name ... --website ... [--bulletin-provider p --provider-id id --publication x:y --group g]
pnpm diocese new church   <d> --parish <p> [--from roster:id ...] [--name ... --line1 ... --city ... ...]
pnpm diocese new excluded <d> --reason <r> [--from roster:id] [--name ... --city ... --last-mass date]
pnpm diocese new open     <d> --name ... --revisit "next step" [--revisit-after date] [--from roster:id]
pnpm diocese merge   <d> <parish>... --into <parish> [--note "why"]
pnpm diocese rename  <d> <kind> <old> <new>
pnpm diocese exclude <d> <church> --reason <r> [--last-mass date]

pnpm diocese roster fetch  <d> gcatholic [key] | wpsl <finder URL>
pnpm diocese roster import <d> <name> <file.json|csv> [--title --url --notes]
pnpm diocese roster list <d> | show <d> <roster:id>
pnpm diocese coverage <d> [--roster name] [--link] [--show-matched]
pnpm diocese audit <d> [--fetch]

pnpm diocese probe url <url>...
pnpm diocese probe sites <d> [--all]
pnpm diocese probe po <org slug | LPi id>... [--issues N]
pnpm diocese probe container <a/b> [--weeks N --from date --step N --all --pages N]
pnpm diocese probe pdf <url> [--pages N] [--grep text ...]
pnpm diocese recheck <d> [slug ...] [--kind k] [--all]

pnpm diocese export  <d> --out-dir DIR
pnpm diocese promote <d> [--dry-run]
```

`validate` separates **errors** (block every write), **incomplete** (block export and
promote: TODOs, missing evidence, missing address, unknown provider) and **warnings**. `pytest`
runs it over the committed dioceses, so a bad hand edit fails CI.
