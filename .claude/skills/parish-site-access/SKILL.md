---
name: parish-site-access
description: See parish websites and bulletins that `pnpm diocese probe url` can't, while exploring a new diocese from a Claude Code cloud sandbox. A real Chrome (the pipeline's stealth browser, headed under xvfb) that gets past Cloudflare most of the time, renders JavaScript sites and iframe widgets, follows a site's bulletin links, and reports the same verdicts and publication ids `probe url` does, plus a `probe container` equivalent for eCatholic and Discover Mass bulletins, and a reader that turns a diocese's eCatholic parish-finder map into a roster, and a renderer for bulletin pages that are only images. Use when probe url says HTTP4XX or NO-PARISH-WORDS, or finds no publications, or when WebFetch/curl get a 403 "Just a moment..." page.
---

# Seeing parish sites the probes can't

This skill works alongside `explore-diocese`, whose `probe url` fetches pages without a
browser. On Syracuse's 75 parish websites, `probe url` found the bulletin publisher for only
7. It couldn't read these:

- **HTTP4XX (6):** Cloudflare's "Just a moment..." page (every eCatholic-hosted site is
  behind it), or a bot-block.
- **NO-PARISH-WORDS (6):** pages built in JavaScript, or "Redirecting..." shells.
- **`ok` with no publications (most of the rest):** the bulletin sits in an iframe widget,
  or on a "Bulletins" page one click away.

WebFetch hits the same walls. These tools fill the gaps, and they report ids in the
`scheme:value` form that `publication` takes.

## Setup, once per sandbox (~1 min)

```bash
.claude/skills/parish-site-access/scripts/setup_browser.sh
```

This installs Google Chrome and trusts the agent proxy's TLS certificate in Chrome's store.
Before it runs, no browser starts at all:

- The venv's Playwright wants a newer Chromium than the image ships, and
  `playwright install` is blocked.
- The proxy re-terminates TLS, so every page fails with `ERR_CERT_AUTHORITY_INVALID`.

## `visit.py`: probe url in a real browser

```bash
V=".claude/skills/parish-site-access/scripts/visit.py"
uv run python $V --bulletin https://www.stmarys-clinton.com http://saintlouisgonzaga.org   # like probe url
uv run python $V https://stleohilton.org --follow /bulletins --links --match files.ecatholic
uv run python $V https://example-parish.org --text --chars 3000 --screenshot /tmp/p.png   # Read the PNG
```

It prints JSON with `probe url`'s fields for the site's own page, judged on the **rendered**
HTML of the page and its iframes:

- **`verdict`:** `probe url`'s checks (SPAM-SQUAT, REDIRECT-OFFSITE, HTTP4XX, HTTP5XX,
  NO-PARISH-WORDS, ok) applied to the rendered HTML, plus two of its own. `BLOCKED` means
  Cloudflare challenged every load. `ERROR` means the browser couldn't load the page at all:
  for example, one Syracuse site answers HTTP 445, which Chrome refuses. A domain that
  doesn't resolve is also `ERROR`; run `probe url` for the DEAD-DNS diagnosis.
- **`publications`:** from the CLI's own `find_publications`, so the ids match `probe url`'s.
- **`bulletin_links`**, and **`pdf_links`** listed separately: `bulletin_links` stops at 15,
  and WordPress pages use those up on feeds before reaching the PDF.
- **`--bulletin`:** when the page embeds no id, it opens the site's bulletin pages (up to 5)
  until one does. The result goes in `bulletin_search.found`. Bulletin PDFs with no
  publisher are reported as self-hosted, with `url:<the page that lists them>`. That page
  may be an index linking one post per issue, or the home page itself.
- **`--follow TEXT`** clicks through to the first link whose text or href contains TEXT
  (repeatable, one URL only). The page it lands on goes under `followed`; the top-level
  fields still describe the site. Prefer a path (`/bulletins`) to a word: "bulletin" also
  matches "Publish in our Bulletin".
- **`--text` (`--chars N`), `--links` (`--match REGEX`), `--html PATH` and
  `--screenshot PATH`** read the final page. With several URLs, the file names get `-0`,
  `-1` and so on.

What it found on the 21 Syracuse sites `probe url` couldn't read (2026-09-25):

- **Behind Cloudflare:** eCatholic ids for two (`ecatholic:35905`, `ecatholic:33641`).
- **In "Bulletins" pages or widgets:** ParishesOnline ids for three (`po-org:…`, `lpi:…`,
  `po-container:…`).
- **Self-hosted:** three bulletins.
- **Dead or hijacked domains:** a parked domain, a for-sale page, and a site taken over by a
  Chinese movie-streaming page. None of these contain parish words, so they get a non-`ok`
  verdict.
- **Never loaded:** two sites stayed BLOCKED through every run (see the next section).

## When a site stays BLOCKED: find the bulletin elsewhere

Most Cloudflare sites load within a few tries, but some challenge nearly every visitor.
holyfamilyendwell.com loaded 0 times in ~25 loads over half an hour. When that happens,
don't keep hammering it. The bulletin is usually published somewhere that isn't blocked:

1. **Search the web** for the parish name, the town and "bulletin". Discover Mass,
   ParishesOnline and the eCatholic file host all show up in results. For Holy Family,
   Endwell, a search turned up `discovermass.com/church/church-of-the-holy-family-endwell-ny/`,
   and `issues.py discovermass` then read its 27 September issue.
2. **Check the diocese directory, GCatholic and Facebook** for a second website, such as a
   family or cluster site. It may be blocked too, but it's worth one try.
3. **Try `visit.py` again later.** Blocked streaks pass.

## `issues.py`: probe container for eCatholic and Discover Mass

`probe container` walks a ParishesOnline container back week by week, and `issues.py` does
the same for the other two publishers. Their files live on hosts with no Cloudflare, so no
browser is needed even when the parish's own site is blocked:

```bash
I=".claude/skills/parish-site-access/scripts/issues.py"
uv run python $I ecatholic ecatholic:20434 [--weeks 12 --from 2026-06-01 --step 4 --all --pages 3 --grep "St. Anne"]
uv run python $I discovermass discovermass:st-patrick-victor-ny [--issues 6 --pages 3]
```

- **eCatholic:** issues are at `files.ecatholic.com/{site id}/bulletins/{YYYYMMDD}.pdf`, one
  per Sunday. The coming Sunday's issue is usually up by mid-week. As with ParishesOnline,
  **a missing issue answers 403, not 404**, and there's no directory listing. The site id
  comes from `visit.py` on the parish's eCatholic site. Without `--from`, it starts at the
  coming Sunday. With `--from`, it starts at the Sunday on or before that date, as
  `probe container --from` does. Some parishes date the file by another weekday: Holy
  Spirit, Hamilton posts the 27 September issue as `20260925.pdf`, the Friday before. Pass
  `--day fri` (or `sat`, ...) for those.
- **`ecatholic:31250` is the Diocese of Syracuse's own site**, not a parish. `visit.py` and
  `probe url` report it on any parish page that links a diocesan PDF. Don't record it.
- **Discover Mass:** the church page is server-rendered and lists about 12 issues.
- **Staleness:** for both publishers, `issues.py` flags a newest issue older than 45 days,
  as `probe po` does.
- **`--pages` and `--grep`** work as in `probe pdf`. Mastheads are often on page 2 or 3.
  `--grep` alone reads 3 pages.

## `render.py`: read a bulletin page that is only an image

Many bulletins are scanned images, in whole or in part: in Syracuse, about one in five
(ParishesOnline, Discover Mass and self-hosted alike). `probe pdf` lists those pages under
`pages_without_text`. The sandbox has no pdftoppm, PIL or tesseract, so `render.py` draws
the pages with pdf.js in Chrome and writes PNGs you can look at with the Read tool:

```bash
uv run python .claude/skills/parish-site-access/scripts/render.py \
    https://container.parishesonline.com/bulletins/03/1424/20260920B.pdf /tmp/ccsssp --pages 1-2
```

`--pages` takes numbers and ranges (`1,3-5`); without it every page is drawn.

Cite the PDF's URL as usual, and say in the evidence `note` that the page is an image, so
the auditor knows `recheck` can't find the quote in its text. Record in the parish's
*Website and bulletin provider* that the bulletin is image-only: the pipeline will need to
read it as an image too.

## `finder.py`: an eCatholic parish finder as a roster

A diocese whose site runs on eCatholic usually has a "parish finder" map (Syracuse:
`syracusediocese.org/parishfinder`). It is behind Cloudflare and isn't WP Store Locator, so
`roster fetch wpsl` can't read it. `finder.py` loads it in the browser and writes the list
`roster import` takes: one entry per site on the map, with the finder's site id, name,
address, coordinates, website and phone. Closed parishes stay on these maps as
"<Name> (Closed)" with no address, and get `kind: closed`.

```bash
F=".claude/skills/parish-site-access/scripts/finder.py"
uv run python $F https://www.syracusediocese.org/parishfinder --out /tmp/directory.json
uv run python $F --html saved-finder.html --out /tmp/directory.json   # from visit.py --html
pnpm diocese roster import <d> directory /tmp/directory.json --title "..." --url <finder URL> --notes "..."
```

The map pins are the diocese's, so churches made `--from directory:<id>` get
`coordinates_from: diocese-directory`. Put a GCatholic entry first in `--from` when there is
one: its Plus Code is on the building.

## Other bulletin hosts seen in Syracuse

- **John Patrick Publishing / church-bulletin.org:** `jppc.net/onlinebulletins/<id>template.pdf`
  and `church-bulletin.org/<id>` redirect to `church-bulletin.org/<slug>`, which lists one
  PDF per Sunday at `church-bulletin.org/bulletin/<slug>/<YYYY-MM-DD>.pdf`, fetchable
  without a browser. Record it as `bulletin_provider: other` with
  `url:<church-bulletin.org page>` as the publication.
- **Discover Mass archive widgets:** `bulletins.discovermass.com/archives/<n>`, embedded on
  parish sites, is a plain HTML list of past issues with no Cloudflare in front.
- **Diocesan documents:** a `syracusediocese.org/documents/...` PDF answers 403, but the same
  file is at `files.ecatholic.com/31250/documents/<same path>` with no Cloudflare.
- **LPi generic inserts:** a ParishesOnline page that lists only
  `.../generic-publications/pol/<date>GB.pdf` files is LPi's generic insert, not the
  parish's bulletin.

## Other bulletin hosts seen in Albany

- **SiteGround's "Robot Challenge Screen"** (`/.well-known/sgcaptcha/`): `visit.py` waits up
  to 20 s for it to clear, which it usually does on the first load in headed Chrome (St.
  John the Baptist, Walton). Plain curl gets only the challenge.
- **Google Drive file links:** some parishes link one `drive.google.com/file/d/<id>/view`
  per Sunday instead of a folder (Altamont, Walton). The PDF downloads without a browser
  from `drive.google.com/uc?export=download&id=<id>`. Record these as `other`: its resolver
  reads Drive file links, and Concrete CMS `download_file/view/<n>` links, as PDFs.
- **parishes.rcda.org/<Name>/**: the diocese's hosted parish sites. `bulletin.php` lists
  `bulletins/<YYYY>/<Month>_<DD>.pdf`. HTTPS resets about one request in three; retry.
- **eCatholic bulletins uploaded as documents:** Holy Family, Little Falls posts its PDFs
  under `files.ecatholic.com/<id>/documents/<y>/<m>/` with free-form names, linked from a
  yearly `/2026-bulletins` page, so `issues.py ecatholic` finds nothing there.
- **A spam word on a parish page is not a squat:** `probe url` and `visit.py` say
  SPAM-SQUAT only for two spam terms, three hits, or a page without parish vocabulary. A
  Schenectady parish's news mentioned "Rivers Casino".

## Other bulletin hosts seen in Ogdensburg

- **Weekly-overwritten PDFs:** `cvrchparish.org/files/bulletin.pdf`,
  `mwcatholics.org/files/bulletin.pdf`, and the diocese's own
  `rcdony.org/images/<parish>bulletin.pdf`. Record the PDF (or the page linking it) as the
  `other` website. `fetch` downloads a known address again each week and keeps a new
  issue, told apart by its content. A PDF evidence quote from one of these is only good
  until the next Sunday, so say which issue in the `note`.
- **church-bulletin.org linked directly** (`church-bulletin.org/?id=4047`, "recent
  bulletins"), not through a jppc.net template. The resolver follows it when the page's own
  PDFs are something else.
- **nny360.com (Watertown Daily Times):** paywalled articles keep their text ROT47-scrambled
  in the served HTML. `visit.py --text` shows it, but `recheck` can't, so quote the headline
  or subhead where you can.

## Evidence from blocked pages

`pnpm diocese recheck` re-fetches every evidence URL without a browser, so a quote taken from
a Cloudflare-blocked page will come back `unreachable`. Prefer quoting the bulletin PDF:
issues on `files.ecatholic.com` and `container.parishesonline.com` fetch without a browser,
and a dated issue at a dated URL never changes. Discover Mass issues fetch without a browser
too, but their `download.php?bulletin=` link is a token that changes on every page load.
Old tokens kept working, including one fetched five days earlier, but nobody has checked
whether they last. So cite a Discover Mass issue by the church page plus the issue date in
the `note`, and quote from its text: `recheck` reads every issue the church page lists
along with the page, so the quote is checked until the issue drops off the list (about
twelve weeks). When a quote can only come from a blocked
page, say so in the item's `note`, e.g. "behind Cloudflare; read in a browser
(parish-site-access visit.py)", so the auditor knows to open it the same way.

## How Cloudflare behaves in the sandbox (measured 2026-09-25)

- **The challenge can't be solved here.** Its "Verify you are human" step needs
  `brunhild.challenges.cloudflare.com`, which the environment's egress policy denies
  (`connect_rejected` in `curl -sS "$HTTPS_PROXY/__agentproxy/status"`). Don't route around
  it. The user can add that host in the environment's network settings.
- **Cloudflare decides per request, so retrying works for most sites.** Headed Chrome
  sometimes gets the real page with no challenge at all. No clearance cookie is ever set, so
  every load rolls again. `visit.py` reloads with backoff (2s, 4s, 8s, then 15s, up to
  `--retries`, default 8).
- **How often it gets through varies by site:**
  - **Rochester:** 15 of 15 Cloudflare homepages loaded in one batch (1–6 loads each).
  - **Syracuse:** `stjohnsnh.com` loaded in 2. `stmarys-clinton.com` loaded in half its
    runs. `holyfamilyendwell.com` never loaded.
- **Headless never passes:** 0 of 23 loads. Keep the browser headed: `visit.py` re-runs
  itself under `xvfb-run`, so don't set `PLAYWRIGHT_HEADLESS=1`.
- The egress IP rotates across a pool, and the IP doesn't predict the outcome.
- **`probe url`'s DEAD-DNS is real here.** The domains it flagged don't resolve, and the
  proxy can't reach them either.
