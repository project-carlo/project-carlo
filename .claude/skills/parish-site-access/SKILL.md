---
name: parish-site-access
description: See parish websites and bulletins that `pnpm diocese probe url` can't, while exploring a new diocese from a Claude Code cloud sandbox. A real Chrome (the pipeline's stealth browser, headed under xvfb) that gets past Cloudflare most of the time, renders JavaScript sites and iframe widgets, follows a site's bulletin links, and reports the same verdicts and publication ids `probe url` does, plus a `probe container` equivalent for eCatholic and Discover Mass bulletins. Use when probe url says HTTP4XX or NO-PARISH-WORDS, or finds no publications, or when WebFetch/curl get a 403 "Just a moment..." page.
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
uv run python $V https://stleohilton.org --follow /bulletins --links files.ecatholic
uv run python $V https://example-parish.org --text 3000 --screenshot /tmp/p.png           # Read the PNG
```

It prints JSON with `probe url`'s fields, judged on the **rendered** page and its iframes:

- **`verdict`:** the same rules `probe url` uses (SPAM-SQUAT, REDIRECT-OFFSITE, HTTP4XX,
  HTTP5XX, NO-PARISH-WORDS, ok), plus two of its own. `BLOCKED` means Cloudflare challenged
  every load. `ERROR` means the browser couldn't load the page at all (for example, one
  Syracuse site answers HTTP 445, which Chrome refuses).
- **`publications`:** from the CLI's own `find_publications`. It also reads ParishesOnline's
  `parishesonline.com/find/<slug>/bulletin/file/03-1424-<date>B.pdf` links as
  `po-container:03/1424`, which `find_publications` misses.
- **`bulletin_links`**, and **`pdf_links`** listed separately: `bulletin_links` stops at 15,
  and WordPress pages use those up on feeds before reaching the PDF.
- **`--bulletin`:** when the page embeds no id, it opens the site's bulletin pages (up to 5)
  until one does. The result goes in `bulletin_search.found`. A bulletin page with PDFs and
  no publisher is reported as self-hosted, with `url:<listing page>`.
- **`--follow TEXT`** clicks through to the first link whose text or href contains TEXT
  (repeatable). Prefer a path (`/bulletins`) to a word: "bulletin" also matches "Publish in
  our Bulletin".
- **`--text [N]`, `--links [REGEX]`, `--html PATH` and `--screenshot PATH`** let you read the
  page itself.

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
uv run python $I ecatholic ecatholic:20434 [--weeks 12 --step 4 --all --pages 3 --grep "St. Anne"]
uv run python $I discovermass discovermass:st-patrick-victor-ny [--issues 6 --pages 3]
```

- **eCatholic:** issues are at `files.ecatholic.com/{site id}/bulletins/{YYYYMMDD}.pdf`, one
  per Sunday. The coming Sunday's issue is usually up by mid-week. As with ParishesOnline,
  **a missing issue answers 403, not 404**, and there's no directory listing. The site id
  comes from `visit.py` on the parish's eCatholic site.
- **Discover Mass:** the church page is server-rendered and lists about 12 issues.
  `issues.py` flags a newest issue older than 45 days, as `probe po` does.
- **`--pages` and `--grep`** work as in `probe pdf`. Mastheads are often on page 2 or 3.

## Evidence from blocked pages

`pnpm diocese recheck` re-fetches every evidence URL without a browser, so a quote taken from
a Cloudflare-blocked page will come back `unreachable`. Prefer quoting the bulletin PDF:
issues on `files.ecatholic.com`, `container.parishesonline.com` and Discover Mass all fetch
without a browser, and a dated issue never changes. When a quote can only come from a blocked
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
