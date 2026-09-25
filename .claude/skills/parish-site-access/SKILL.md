---
name: parish-site-access
description: Open and navigate the parish websites in data/parishes.csv from a Claude Code cloud sandbox the way the pipeline's Playwright code does - real Chrome, headed under xvfb, playwright-stealth - including the Cloudflare-protected ones (all eCatholic sites plus a few others) that WebFetch and curl only see as a 403 "Just a moment..." page. Use when you need to see a parish's homepage, find or follow its bulletin links, screenshot it, debug `pdf_extract fetch`/`detect run` for a parish, check a newly added parish, or when `pnpm diocese probe url` hits a Cloudflare 403.
---

# Visiting parish websites from the cloud sandbox

WebFetch and curl can't see about a quarter of the parish sites. Cloudflare
returns a 403 "Just a moment..." challenge for all 11 `ecatholic` parishes and for
`stlouischurch.org`, `holyspirit-saintjoseph.org`, `cabriniroc.org` and
`stjohnschurchspencerport.org`. `parishesonline.com` pages are a JavaScript app that
arrives empty. The fix is to do what the pipeline does: drive a real browser.

## 1. One-time setup per sandbox (~1 min)

```bash
.claude/skills/parish-site-access/scripts/setup_browser.sh
```

A fresh sandbox can't launch a browser at all until this runs. The script fixes the following:

- **Google Chrome gets installed.** The venv's Playwright expects a newer bundled Chromium than the image
  ships (`/opt/pw-browsers` has build 1194; Playwright 1.58 wants 1208), and
  `playwright install` is blocked. Chrome from `dl.google.com` installs fine.
  It is also what `detect.py` uses, and it passes Cloudflare more often than Chromium.
- **The agent proxy's CA gets trusted.** The proxy re-terminates TLS, and Chrome's NSS store
  (`~/.pki/nssdb`) starts empty, so every page fails with `ERR_CERT_AUTHORITY_INVALID`.
  The script imports `/root/.ccr/agent-proxy-ca.crt` with `certutil`. TLS stays verified.

## 2. Look at a site

```bash
V=".claude/skills/parish-site-access/scripts/visit.py"
uv run python $V st-jerome --text                       # slug or URL; visible text
uv run python $V st-jerome --follow /bulletins --links files.ecatholic
uv run python $V net-catholic --screenshot /tmp/nc.png  # then Read the PNG to see it
uv run python $V https://parishesonline.com/organization/all-saints-parish --links selectedPublication
uv run python $V transfiguration-st-catherine-mendon --frames --links publication-page  # iframe widget
```

- The browser is the pipeline's own `pdf_extract.browser.launch_stealth_browser`
  (stealth-patched, headed) with `channel="chrome"`. The script re-runs itself under
  `xvfb-run` when there's no display.
- `--follow TEXT` clicks through to the first link whose text or href contains TEXT,
  and can be repeated. Prefer a path (`/bulletins`) over a word: `--follow bulletin` on
  netcatholic.org lands on "Publish in our Bulletin".
- `--text [N]`, `--links [REGEX]`, `--html PATH` and `--screenshot PATH` inspect the final page.
  `--frames` adds iframe content.
- It prints `OK`/`BLOCKED`, the HTTP status, the final URL and how many loads it needed.
  It exits 2 if Cloudflare challenged every load. That happens occasionally during a long
  blocked streak; wait a minute or two and run it again.

## 3. Run the pipeline itself

Pipeline code runs unmodified once setup is done. Its env vars pick Chrome:

```bash
uv run python -m pdf_extract db create   # once: no R2 here, so start from an empty DB
PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a uv run python -m pdf_extract fetch --parish "St. John the Evangelist (Greece)"
PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a uv run python -m pdf_extract detect run --dry-run --limit 3
```

`fetch` records bulletins in `data/parish_events.db` and saves PDFs under
`data/bulletins/`. Both are gitignored. The real database lives in R2, and cloud sessions
have no R2 access, so a sandbox run starts from an empty migrated DB. It re-fetches
everything and publishes nothing. The pipeline does not retry Cloudflare challenges (see below), so an
eCatholic parish can fail on one run and succeed on the next.

## How Cloudflare behaves here (measured 2026-09-25)

- **The challenge can't be solved in this sandbox.** When Cloudflare challenges, it's an
  interactive Turnstile ("Verify you are human"), and its endpoint
  `brunhild.challenges.cloudflare.com` is denied by the environment's network policy.
  `challenges.cloudflare.com` itself is allowed. Denials show up as `connect_rejected` in
  `curl -sS "$HTTPS_PROXY/__agentproxy/status"`. Don't try to route around the policy.
  The fix is for the user to add that host to the environment's allowed domains.
- **Cloudflare decides per request, so retrying works.** Headed Chrome gets the real
  page (200, no challenge) about half the time. No clearance cookie is ever set, so
  every navigation rolls again, including a second page on the same site. Blocked
  loads come in streaks lasting tens of seconds. `visit.py` therefore reloads with backoff
  (2s, 4s, 8s, then 15s, up to `--retries`, default 8). The egress IP rotates across
  a pool (160.79.106.x), but the IP doesn't predict the outcome. A batch run of
  `visit.py` over all 15 challenged homepages loaded 15 of 15. Most needed 1–3 loads
  (4–22 s); the worst needed 6 loads (74 s).
- **Headless never passes.** Headless Chrome or Chromium, stealth or not, got the
  real page on 0 of 23 loads. Keep it headed; don't set `PLAYWRIGHT_HEADLESS=1`.
- **WebFetch and curl always get the challenge.** A browser User-Agent doesn't help.
  `allsaintsparish.org` is the exception: it only rejects curl's default UA.

## When you only need the bulletin PDF

The providers serve the PDFs from hosts with no challenge, so no browser is needed:

```bash
python .claude/skills/parish-site-access/scripts/bulletin_url.py <slug> [...] | --all
```

- **eCatholic:** `https://files.ecatholic.com/{site_id}/bulletins/{YYYYMMDD}.pdf`. The date
  is always the Sunday. A missing file returns 403 AccessDenied (S3). `site_id` comes from
  past bulletins in `data/parish_events.db`, or from the script's built-in table
  (as of 2026-09) when the DB hasn't been pulled.
- **Parishes Online:** a JSON API with no auth. `GET https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/organizations/slug/{provider_id}`
  returns `data.salesforce_id`, then `…/organizations/{id}/publications?limit=12&type=Church`
  returns `fileUrl` and `publishDate`.
- **Discover Mass:** the church page is server-rendered, so plain fetches (curl, WebFetch) work. Send a browser
  UA from Python, because `urllib`'s default gets a 403.

These routes often show next Sunday's bulletin before the parish site links it.
WebFetch on a PDF can't read the text, but it saves the file locally, and `Read` with
`pages:` opens it.
