# The fetch stage

`fetch` finds each parish's current bulletin and stores it. How it stores bulletins
is in the README's [How data is stored](../README.md#how-data-is-stored).

## Parallel fetching

`fetch` works on several parishes at once (`pnpm run fetch --workers N`,
default 6, each with its own browser), but never has two workers fetching
from one site: all ParishesOnline parishes count as one site, as do all
eCatholic and all Discover Mass parishes, and any other site counts by its
domain (so `parishes.rcda.org` and `www.rcda.org` are one). A worker holds one
site at a time: its parish's while its browser finds the bulletin, then the
PDF's while it downloads it, and lets go before compacting the PDF, so the
next parish on a site starts then. Requests a page makes to other sites, and
redirects, are not held back; with only a few workers, no site gets more than
a few at once. A worker whose browser will not launch, or stops answering,
gets a new one; the fetch fails only when no worker can.

## Skipping what it already has

`fetch` skips a parish whose newest bulletin is already this weekend's, by
the issue date the extractor read off it (and only when that bulletin was
fetched within a few days of the date). Otherwise it downloads the bulletin,
asking the server first whether the copy it has from that address is still
current (`ETag` / `Last-Modified`), and keeps it only if it is new: not the
same bytes as any of the parish's bulletins (`src/pdf_extract/duplicates.py`).
A bulletin seen again is recorded on its row (`last_seen_at`), not stored twice.
The address is never taken to mean the bulletin is unchanged: Discover Mass
serves the same PDF from a new address each time, and some sites put each
week's bulletin at the same one.

**A download that is neither a PDF nor an image is not stored.** A server can
answer 200 with a page in place of the file: Discover Mass sends a 134-byte
"Maximum number of files downloaded today" page once its daily cap is hit, and
some hosts send a bot check. The parish is reported as `download_failed`, with
the page's size and opening text in the detail, and counts as a failure like
any other; its last bulletin stays its last. Before this check, the October 25,
2026 run stored the Discover Mass page as 66 parishes' bulletin, and every run
after matched it by hash and reported them `unchanged`. Migration 13 deleted
those rows.

## Compacted copies

`fetch` stores a compacted copy of each bulletin: the first 10 pages, which is
all the classifiers read, with images downsampled to 150 dpi by Ghostscript.
`data/bulletin_page_limits.csv` raises the page limit, with the reason, for a
parish whose schedule runs past page 10. The storage key's hash is of the PDF as
downloaded. Without `gs` installed, long bulletins are only truncated.

Compaction takes as many steps as a bulletin needs (`src/pdf_extract/pdf_compact.py`):

1. Ghostscript, with a 180-second limit. Time goes on converting colours rather
   than on file size, so a 39 MB bulletin can take longer than a 515 MB one.
2. If that fails, Ghostscript again without converting colours. It takes seconds
   on the same files; the result can be larger, since CMYK images stay CMYK.
3. If what is left is still over 20 MB, Ghostscript at 110 dpi.

**A bulletin over 20 MB after all of that is not stored** (`too_large` in the run
report, which counts it as a failure). Nothing is recorded for it, so the parish
keeps its last bulletin and the next run tries again. Under 20 MB a failure is
harmless: when compaction fails or saves nothing, the smallest copy available is
stored, which may be the PDF as downloaded. A download over 1 GB is stopped and
reported the same way.

When a parish shows up as `too_large`, the file itself is the place to start:
page through it, and work out what makes it big. `pnpm data:recompact` shrinks
bulletins already in the bucket. It lists what it would change, and `--apply`
(with `CARLO_REMOTE_WRITE=1` and write credentials) replaces them under the same
keys, so no bulletin row, label or cached result changes.

## Checking the fetch stage

Most parishes publish through ParishesOnline, eCatholic or Discover Mass, but
the `other` provider has to find the bulletin on the parish's own website, and
every site is laid out differently. `pnpm fetch:check` runs the resolvers in the
browser without touching the database, downloads what each one picks, and
prints one row per parish (`ok`, `resolve_failed`, `download_failed`,
`not_pdf`, or `blocked` when Cloudflare challenged the browser instead).

That status only says whether a PDF was found and downloaded. Each row also
has a `verification` block (totals in `verification_counts`) that checks five
things separately: the download, whether the file is a valid PDF, whether it is
the expected parish's bulletin, its issue date, and whether that date is recent.
For one parish:

```bash
pnpm --silent fetch:check --parish saint-joseph-renovo \
  --expected-identity "Saint Joseph" --expected-issue-date 2026-10-18 \
  --reference-date 2026-10-21 --max-issue-age-days 14
```

The `--expected-*` flags apply to every parish selected.

- **Identity**: `--expected-identity` is looked for as a literal phrase (ignoring
  case and punctuation) in the first 2,000 characters of the first page's text.
  It is `matched` or `not_matched`, or `unknown` when the PDF has no text (a scan).
  A match only means the phrase is there, not that the parish published it.
- **Issue date**: a date printed on its own line in that text is `observed`. A
  date found only in the file name is `inferred`. Dates that disagree are a
  `conflict`. `--expected-issue-date` is compared with the date found.
- **Freshness**: an issue is `fresh` when it is at most `--max-issue-age-days`
  old (default 14) on `--reference-date` (default today), `stale` when older,
  and `future` when dated later.

`verification.overall` is `verified` only when the PDF parses, the identity
matches and an observed issue date is fresh, so a date from the URL alone never
verifies an issue. It is `failed` when any check fails, and `unverified`
otherwise. Only PDFs up to 25 MB are inspected, and there is no OCR.
`--no-download` skips the document checks. The status column and the command's
exit code ignore verification, so read the two separately.

### How the `other` resolver reads a site

`src/pdf_extract/parish_sites/` reads a parish's own site in three stages:

1. **Locate** the bulletin page by following the homepage's "bulletin" links
   (`locate.py`).
2. **Collect** the PDFs it offers (`collectors.py`). Each collector handles one
   way a site offers them: `drive-folder`, `redirected-pdf` (the bulletin link
   is the PDF), `page-pdfs` (links, or addresses in the page's markup),
   `linked-issue-page` (an embedded flipbook or a publisher's listing) and
   `dated-post` (a weekly post that wraps the PDF). They run in that order
   until one finds a convincing set. `page-pdfs` also reads PDF addresses a
   viewer plugin keeps in base64 JSON (PDF Embedder's `pdfemb-data`, 3D
   FlipBook's `FB3D_CLIENT_DATA`), and takes Google Drive files, Google Docs
   (exported as PDF), Concrete CMS and DotNetNuke (`LinkClick.aspx`) downloads
   as PDFs. One more collector runs only when a recipe names it:
   `page-images`, for a parish that posts each issue as an image (a JPEG per
   weekend); `fetch` stores the image as a one-page PDF.
3. **Choose** this week's issue among them (`choose.py`), and say why:
   `current` (dated this week), or a fallback (`newest-recent`, `titled`,
   `first-listed`). `newest-recent` is the newest issue dated in the last 45
   days, taken when the first listed is plainly old, or when it is neither
   dated nor labelled "bulletin" and the page lists a dated series.

Each fetch result records how its bulletin was found ("page-pdfs on
https://…/bulletins: current"), and the run report lists any new bulletin the
site dated, but not this week.

A parish can pin the first two stages with a **recipe** in its `provider_id`:
a collector, a bulletin page, or both (`page-pdfs https://example.org/bulletins`;
a collector alone reads `website` as the bulletin page). A pinned parish skips
the homepage and runs only its collector, so it fails loudly when its site
changes rather than guessing, and no change made for another site can change
what it picks. `fetch:check` prints the recipe that reproduces each pick it
guessed; pin it once the pick is right.

A shared page can be restricted to one parish's PDFs with a filename glob:
`page-pdfs https://example.org/bulletins filename=St-Annes-Bulletin*.pdf`.
The filter matches the decoded file name, ignores case and query parameters,
and runs before choosing an issue. Patterns cannot contain whitespace. If
no file matches, the fetch fails. Use a page that lists the newest issue first
so the fallback also keeps the latest matching bulletin when uploads are late.

When a site needs something new, add a collector rather than a branch inside
an existing one, and record the site (below). The parishes waiting on one are
`bulletin_provider: unsupported` with a `fetch_gap` (`pnpm diocese gaps` lists
them by kind). A new collector doesn't put them live: set each one's provider,
check it with `fetch:check`, then clear its gap (data/dioceses/README.md).

### Recorded sites

To keep a resolver change from fixing one site and breaking another, the pages
each resolver read on every parish's real site are recorded in
`tests/fixtures/fetch/<slug>.json.gz`, and `tests/test_fetch_replay.py` replays
them offline against the bulletin in `expected.json`, using each parish's
recipe in `data/parishes.csv` as it is now. After changing `fetch.py` or
`parish_sites/`, or pinning a recipe:

1. Run `pnpm test`. A changed pick on any recorded site fails the replay test.
   A site that now opens a page the old resolver never did fails with "re-record
   this parish".
2. Re-record the sites whose result should change, then check them by hand:
   `pnpm fetch:check --parish SLUG --record tests/fixtures/fetch`.
3. Update their entries in `tests/fixtures/fetch/expected.json`. That diff is the
   coverage change.

Run `fetch:check` in a headed browser (under `xvfb-run` on a server); Cloudflare
turns headless browsers away. Set `PLAYWRIGHT_BROWSER_CHANNEL=chrome` to use the
installed Chrome.
