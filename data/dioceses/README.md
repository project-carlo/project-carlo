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
For shared-pastor directories, preserve explicit pastor-to-parish associations and their
source. Adjacency in extracted text isn't an association; leave ambiguous links unresolved.

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
| `closed` | no Mass any more: closed, merged away, sold, demolished. Put the date in `last_mass` when a source gives it (`2017` or `2017-06` when it gives no day) |
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
4. The site shows only places it can give a schedule for. A `no_bulletin` parish row and its
   churches stay in the records, with their evidence and a `revisit`, but `promote` leaves
   them out of the live CSVs (and removes them if they were live, which `validate` warns about
   until it is done), and they carry no `promoted` stamp. `coverage` counts their churches as
   accounted for but not in its `modelled` figure. Setting the row to a real provider when a
   bulletin turns up puts it back. (Settled 2026-10-07; until then these rows
   were kept on the map with no Mass times.) A place that was never a parish row of its own
   goes in `excluded/` with `reason: no-bulletin` as before.

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

Every record is YAML frontmatter plus a Markdown body. The slug is the file name. Prefer
`uv run python -m pdf_extract diocese write <d> <kind> <slug> --file record.json` for
structured updates (example below), rather than scratch `fill_record` scripts or hand-built
YAML. `new` still creates templates and can prefill roster fields. Use the commands for
anything that touches several files: `merge`, `rename`, `exclude`, `coverage --link`,
`promote`. Those are refused, with nothing written, if they would add a validation error.

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
`revisit_after` (a date), plus optional structured `research` (below). `todo` exposes
unresolved research alongside due revisits, so the next researcher can inspect prior checks
and retry triggers before making requests. Legacy records need no mass backfill.

**parish**
- `website`: where the bulletin can be found (required). Sharing one URL within a diocese
  requires content-supported `separate` peer reviews for **every pair**, and pinned
  `page-pdfs` or `page-images` recipes with filename filters whose literal prefixes
  cannot overlap (e.g. `Anne-Bulletin*.pdf` and `Therese-Bulletin*.pdf`). Different
  globs alone are insufficient: `Anne*.pdf` and `*.pdf` can select the same file.
  Reviews without observed masthead/member evidence, conflicting reviews, external
  live CSV rows and other-diocese claims still block sharing. The exception survives
  promotion and import; the database identifies parishes by slug, not website.
- `bulletin_provider`: `parishes_online`, `ecatholic`, `discover_mass`, `other`,
  `google_drive` or `no_bulletin` (kept in the records, left off the site: Settled policy
  4). `fetch` reads ParishesOnline and DiscoverMass by
  `provider_id` (the org slug from `parishesonline.com/organization/<slug>`, the church slug
  from `discovermass.com/church/<slug>/`). It reads eCatholic, `other` and `google_drive`
  from `website`, so for eCatholic the website has to be the eCatholic-hosted site, and for
  `google_drive` it has to link the shared folder. For `other` and `google_drive`,
  `provider_id` may pin how to read the site, as a recipe: a collector, the bulletin page,
  or both (`page-pdfs https://example.org/bulletins`). For a page serving several parishes,
  add a filename glob such as `filename=St-Annes-Bulletin*.pdf` to keep only that parish's
  files (case-insensitive; no whitespace). Use a newest-first page so late uploads still
  select the latest matching issue. Run
  `pnpm fetch:check --diocese <d> --parish <slug>` (which reads the rows from these
  records, so it works before promotion) and record the `recipe` it prints once its pick is
  this week's bulletin (see "How the `other` resolver reads a site" in the main README).
- `publication`: ids of the bulletin itself, as `scheme:value`. **Two parish rows may never
  share one**, and `validate` enforces that across every diocese: it catches "one bulletin
  carried as several rows", a mistake that shows up in no other check. Record every form
  you find: `po-container:14/0434`, `po-org:<slug>`, `lpi:<18-character id>` (all three are
  one ParishesOnline bulletin), `ecatholic:<site id>`, `discovermass:<slug>`, or
  `url:<page>#<publisher>` for separate self-hosted bulletins on a shared page. A hosting
  account or shared listing is a discovery lead, not a publication identity: record
  only identifiers that identify this bulletin in `publication`, and keep shared
  account/site evidence in `evidence`. Peer reviews never waive publication-id uniqueness.
- `bulletin_status` (optional): `available`, `not-found`, `access-blocked`,
  `unsupported-format` or `not-published`. This describes research availability independently
  of `bulletin_provider`; legacy `no_bulletin` still controls promotion (Settled policy 4).
- `fetch_gap` (optional): the parish publishes a bulletin that `fetch` can't collect yet
  (*What to flag*, below): `{kind, seen, note, url}`. `kind` is a slug naming the problem,
  the same for every parish that has it (`solutio-file-403`, `joomla-weblink-redirect`);
  reuse one that `pnpm diocese gaps` already lists. `seen` is the date you checked, `note`
  says what fails and where the bulletin is, and the optional `url` is an example issue or
  the bulletin page. It doesn't change promotion. Remove it (`"fetch_gap": null`) once
  `fetch:check` picks this week's issue.
- `publication_reviews` (optional): supported peer decisions, independent of URL ids:
  `[{parish: peer-slug, decision: separate|shared, evidence: [{url, seen, quote?, note?}]}]`.
  Use dated content evidence; different URLs alone don't support `separate`. A `shared`
  review records the finding; use `merge` to change structure after reviewing its effects.
  `audit` counts a review only if one evidence item has an http(s) `url`, a `seen` date and
  a note saying whose bulletin it is, in these words: "serves …", "published by …",
  "bulletin for …", or "masthead" with "names", "lists", "includes" or "shows". For
  example: `note: The 25 October 2026 masthead names St. Ann alone, with its own Mass
  times.` "Own masthead" or "different cover" alone don't count, nor does "not … read" or
  "need to check" in the same sentence. `write` and `validate` warn about a review audit
  won't count, and say why.
- `group`: the diocese's grouping, e.g. `Family #31`.
- `replaces`: slugs of rows merged or renamed into this one. Maintained by `merge` and
  `rename`; `promote` deletes those live rows. A promoted successor retains ownership of
  its retired slugs while their CSV rows await deletion, so merging or renaming a shared-site
  publisher does not create a website collision. Other active publishers still need peer
  reviews, and unrelated live rows and other-diocese claims still block sharing.

**church**
- `parish`, the address fields, `latitude`/`longitude` (or `null`, and `pnpm geocode` fills
  them after promotion).
- `coordinates_from`: `gcatholic-plus-code` (building-precise), `osm-node`,
  `diocese-directory`, `parishes-online-org`, `nominatim`, `geocode-stage` or `manual`.
- `name_verified` / `address_verified`: true only when two independent sources agree on
  the value you recorded (the parish's bulletin and its own site are one source; OSM,
  GCatholic and the diocese are others).
- **When sources disagree on an address, choose; don't flag it.** Record the address most
  likely to be right. Prefer the official sources, the parish's own (bulletin, site) and
  the diocese's (directory, finder), over GCatholic, OSM and listings, unless there's a
  concrete reason not to: the official address is an office, a rectory or a PO box rather
  than the church, gives only cross streets, or is out of date (the church moved, the site
  is an old domain). Most conflicts are a few doors apart, and either would find the
  building. Say in *Name and address* what each source gives and why you chose. Set the
  coordinates on the building at the address you chose: a GCatholic Plus Code or an OSM
  building usually is, while a directory pin can be a geocode of the street. A name works
  the same way: use what the parish calls the building (its masthead, its site), and keep
  the roster's name in the roster link.
- `roster`: the roster entries this place is, as `<roster>:<id>`. Written by
  `coverage --link` or by hand.

**excluded**: `reason`, address fields, `parish` (related parish, if any), `last_mass`,
`decided`, `roster`.

**open**: address fields, `parish`, `roster`, and a required `revisit`.

**evidence** items: `url`, `seen` (the date you read it), and `quote` and/or `note`. A
`quote` is copied **verbatim** from the page (`…` marks a gap). `pnpm diocese recheck`
fetches each URL and checks the quote is still there, so write quotes that can be found.

### Structured writes and bounded research

`write <d> <kind> <slug> --file record.json` accepts flat record fields plus a `body`
string, patches existing fields and replaces each supplied list in full. Preserve prior
items when extending `evidence`, `research` or `publication_reviews`; omitted fields stay
unchanged. It validates and writes atomically, returning slug, path and validation counts.
`--file -` reads stdin. Use `--create` only when explicitly creating a new record; `new`
and `merge` remain supported. Supplying `body` replaces the explanation, so include the
complete intended body. For example, a patch to an existing parish (illustrative only):

```bash
uv run python -m pdf_extract diocese write example parish st-example --file - <<'JSON'
{
  "bulletin_status": "access-blocked",
  "research": [{
    "method": "probe url; publisher page returned HTTP 403",
    "url": "https://example.org/bulletins",
    "checked": "2026-10-22",
    "outcome": "access-blocked",
    "next_action": "Read the bulletin page with the browser access method",
    "retry_when": "Browser access becomes available"
  }],
  "body": "## Not yet confirmed\n\nThe bulletin page blocked this check. Publication and current worship sites remain unconfirmed; see research for the next method.\n"
}
JSON
```

Each optional `research` item on any record kind has `method` (string), optional `url`,
`checked` (`YYYY-MM-DD`), and `outcome`: `found`, `not-found`, `access-blocked`,
`unsupported-format` or `not-published`. `next_action` and `retry_when` are required for
every non-`found` outcome; both are optional for `found`. Optional `revisit_after`
(`YYYY-MM-DD`) additionally schedules a check; a dependency belongs in `retry_when` even
when no date can be known.

`not-found` means the recorded method found nothing in its checked scope; `access-blocked`
means access failed; `unsupported-format` means the material exists but the format can't
be read by the method; `not-published` needs evidence that no bulletin is published.
Record the scope and uncertainty rather than converting a failed search into a fact.
Exhausted checks need no repeat without a changed method, source or satisfied retry trigger.
Use a concrete next action and trigger to bound negative research, not a fixed network
request budget that sacrifices evidence. Parish-specific attempts and decisions stay in
the record; the shared publisher playbook keeps only reusable methods and new lessons.

### What to flag

A factory flag asks the owner for a decision. These need none, so record them instead:

- **A church whose status no source settles.** Nothing shows Mass there now and nothing
  says it closed: an `open/` record, with what would settle it in `revisit` and a date in
  `revisit_after`. The factory's `reconcile` tries once more, and the PR lists every
  `open/` record.
- **A bulletin `fetch` can't collect.** The parish publishes a bulletin, but no recipe
  reads it: the host refuses the fetcher, the links aren't PDFs (`opendoc.asp?b_id=`,
  Joomla `weblink.go`, Squarespace `/file`), it is HTML only (an emailed newsletter, a
  page of announcements), it sits in an embedded viewer (Drive `/preview`), or `fetch`
  picks the right file and misreads it (a date taken from a file name). Set the parish's
  `fetch_gap`. `pnpm diocese gaps` lists them across every diocese by kind, which is the
  work list for new collectors. A bulletin not found at all is `research`, not a gap.
- **A check blocked for now.** A block a retry may clear (a daily download cap, a site
  that is down) is `research` with a retry trigger, not a gap and not a flag.
- **Sources that disagree on an address or a name.** Choose, as above.

Flag what only the owner can decide: a question of policy no rule settles, a structural
call the evidence leaves open (a merge, which row a church belongs to, whether a Mass is
public), or a settled rule the evidence contradicts.

## Batch plans

The factory's survey saves a diocese's reviewable plan in `data/dioceses/<d>/batches.json`,
the source of roster assignments: the factory runs a map job per batch, in
`batches.json`'s order with `first_batch` first. Existing mapped dioceses need no backfill.

```json
{
  "version": 1,
  "diocese": "test",
  "first_batch": "town",
  "batches": [{
    "id": "town",
    "name": "Town and its missions",
    "why": "The directory names one shared pastor; check for a shared bulletin.",
    "entries": ["directory:anne", "gcatholic:123"]
  }],
  "excluded": [{"ref": "gcatholic:999", "reason": "Duplicate of directory:anne"}]
}
```

Run `pnpm --silent diocese batches validate <d>` before any map job starts and whenever
rosters or assignments change. `--file <path>` checks a proposed manifest elsewhere.
The command reads every local roster, fetches nothing and changes no files. It exits
1 on errors and reports `passed`, counts, batch sizes, `missing`, `unknown` and duplicate
reference locations. Every `<roster>:<id>` must occur exactly once, either in a nonempty
batch or as an exclusion with a reason. Batch ids must be unique, names and grouping
reasons nonempty, and `first_batch` must name a batch. Missing/malformed rosters cannot
produce a successful check. Excluding a duplicate roster entry from the batches does not
exclude the church from the diocese; normal coverage must still account for it.

The validator checks assignments, not whether a shared pastor implies a shared bulletin.
`survey-review` still reviews the grouping and the choice of a typical first batch. The
plan is committed with the rosters so future reviewers can reproduce the assignment check.

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
4. **Find each bulletin.** Start with targeted checks; record negative outcomes and retry
   triggers as above rather than repeatedly searching the same exhausted sources:
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
5. **Decide one bulletin or several.** Merge only with a current shared bulletin and
   evidence that it covers each member. Check member channels (container, widget, bulletin
   page): they may carry the same publication, have gone silent, or explicitly direct
   readers to the shared bulletin. A live member channel with **distinct current content**
   means no merge; a different URL serving the same bulletin doesn't.
   If you can't find a member's bulletin, that isn't evidence that it shares someone else's,
   so keep its row and say so. Record `publication` ids on every row you settle and supported
   peer content decisions in `publication_reviews`, with dated evidence.
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
8. **Audit structure.** `pnpm diocese audit <d> [--fetch]` reports candidate rows and the
   scope checked, including incomplete fetches or comparisons. **Run it every session.**
   Inspect scope before interpreting a clean result. Different URLs or ids don't establish
   separate documents; compare current content and record supported peer decisions.
   Coverage alone can't reveal several rows publishing one bulletin.
   Run `pnpm fetch:check --diocese <d> --parish <slug>` before promotion and assess
   transport, document type, parish identity and freshness separately. An HTTP success can
   still be an HTML error page, the wrong parish or an old issue. Record unresolved checks
   and retry triggers; consult command help for supported options.
9. **Close the session.** `pnpm diocese validate <d>`, `pnpm diocese todo <d>`, a dated line
   in `diocese.md`'s *Log* with the coverage numbers, and a commit.

**Promotion:** when `todo` shows no errors or incomplete records, run `pnpm diocese promote
<d> --dry-run`, read it, then `pnpm diocese promote <d>` and `pnpm test`. The next pipeline
command seeds the new rows into the database. New parish rows go in with `fetch_only` set:
the weekly run fetches their bulletins but doesn't process them or show their churches until
the flag is cleared (README, "Fetch-only parishes").
Promotion appends new rows, updates promoted ones, and deletes live rows the diocese has
retired (merged, renamed, excluded, moved to open/, or `no_bulletin`). Retiring a church deletes its events, and retiring a
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
- **Different URLs, sizes, hashes or page counts don't prove separate bulletins.** A parish
  can host a copy of its family's bulletin. Compare mastheads and current content; preserve
  the supported decision in `publication_reviews` rather than treating URL ids as proof.
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
  pdf`, `probe get`, the recheck tool). One summary moved a 2020 merger to 2026. The article's
  weekdays gave the real year.
- **A hand-written `quote:` or `note:` containing ": " breaks the YAML.** Quote the value
  (`note: 'Page 1: the masthead'`). `validate` catches it, but only after the whole file is
  unreadable, which in Albany briefly left three churches pointing at a "missing" parish.
- **Coverage measures the roster.** A place the roster doesn't list moves no number, and an
  oratory with no weekend Mass can be missing from every list and still be open. `coverage`
  lists your churches that are in no roster; each needs an explanation, not deletion.

## Commands

`pnpm diocese <command> --help` gives every flag. CLI stdout is JSON; diagnostics go to
stderr. For `jq`, use `pnpm --silent diocese ...` or direct
`uv run python -m pdf_extract diocese ...`; never merge stderr with `2>&1` into `jq`.

```bash
pnpm diocese list | show <d> | todo <d> | validate [<d>]
pnpm diocese gaps [--diocese d] [--kind k]   # bulletins fetch can't collect yet, by kind
pnpm diocese init <d> --name "..." --state NY [--website URL] [--gcatholic key]
pnpm diocese search <words> [--diocese d|live] [--kind parish|church|excluded|open]
pnpm --silent diocese write <d> <kind> <slug> --file record.json [--create]  # --file -: stdin

pnpm diocese new parish   <d> --name ... --website ... [--bulletin-provider p --provider-id id --publication x:y --group g]
pnpm diocese new church   <d> --parish <p> [--from roster:id ...] [--name ... --line1 ... --city ... ...]
pnpm diocese new excluded <d> --reason <r> [--from roster:id] [--name ... --city ... --last-mass date]
pnpm diocese new open     <d> --name ... --revisit "next step" [--revisit-after date] [--from roster:id]
pnpm diocese merge   <d> <parish>... --into <parish> [--note "why"]
pnpm diocese rename  <d> <kind> <old> <new>
pnpm diocese exclude <d> <church> --reason <r> [--last-mass date]
pnpm diocese question <d> <church> --revisit "next step" [--revisit-after date]

pnpm diocese roster fetch  <d> gcatholic [key] | wpsl <finder URL>
pnpm diocese roster import <d> <name> <file.json|csv> [--title --url --notes]
pnpm diocese roster list <d> | show <d> <roster:id>
pnpm diocese coverage <d> [--roster name] [--link] [--show-matched]
pnpm diocese audit <d> [--fetch]

pnpm diocese probe url <url>...
pnpm diocese probe sites <d> [--all]
pnpm diocese probe po <org slug | LPi id>... [--issues N]
pnpm diocese probe container <a/b> [--weeks N --from date --step N --all --pages N]
pnpm diocese probe pdf <url> [--pages N] [--chars N] [--grep text] [--grep text2 ...]
pnpm diocese probe get <url> [--out file] [--chars N]   # instead of curl: page, PDF or JSON
pnpm diocese recheck <d> [slug ...] [--kind k] [--all]

pnpm diocese export  <d> --out-dir DIR
pnpm diocese promote <d> [--dry-run]
```

`validate` separates **errors** (block every write), **incomplete** (block export and
promote: TODOs, missing evidence, missing address, unknown provider) and **warnings**. `pytest`
runs it over the committed dioceses, so a bad hand edit fails CI.
