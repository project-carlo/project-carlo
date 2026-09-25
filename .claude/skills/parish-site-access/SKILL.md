---
name: parish-site-access
description: How to reach parish websites and bulletin providers (eCatholic, Parishes Online, Discover Mass, WordPress/Wix sites) from this repo's data/parishes.csv when WebFetch or curl gets a 403 / Cloudflare "Just a moment..." page or an empty JavaScript app. Use when checking a parish's bulletin, debugging `pnpm run fetch` for one parish, adding a parish, or browsing a parish site from a Claude Code sandbox.
---

# Reaching parish sites and bulletins

Tested 2026-09-25 against all 62 rows of `data/parishes.csv` from a Claude Code
cloud sandbox. Summary: **don't fight the Cloudflare challenges. Each provider
has an unchallenged route to its PDFs.**

## Quick answer: latest bulletin for any parish

```bash
python .claude/skills/parish-site-access/scripts/bulletin_url.py <slug> [<slug> ...]   # or --all
```

It prints `slug<TAB>publish date<TAB>pdf url` and needs only the standard library, with no browser.
It covers every `parishes_online`, `ecatholic` and `discover_mass` parish (40 of 62).
Those routes often show next Sunday's bulletin a few days before the parish
website does. For `other`, `google_drive` and `no_bulletin` it only prints the website to check yourself.

To read a PDF, WebFetch it or `curl -o` it. WebFetch can't read the text, but it
saves the file under `tool-results/…pdf`, and the `Read` tool opens that file with `pages:`.

## What blocks what

| Provider (count) | WebFetch / curl on the site | Unblocked route |
|---|---|---|
| `ecatholic` (11) | **403 Cloudflare managed challenge** on the whole domain (`cf-mitigated: challenge`, title "Just a moment...") | `https://files.ecatholic.com/{site_id}/bulletins/{YYYYMMDD}.pdf` is not challenged. `YYYYMMDD` is always the Sunday. `?t=` is optional. A missing date returns **403 AccessDenied** (S3), not 404. Directory listing is denied. `site_id` comes from past rows in `data/metadata.json`. |
| `parishes_online` (26) | `parishesonline.com/organization/*` returns a 1 KB React shell ("Online Directory", no links). Some parish homepages also get a Cloudflare 403. | JSON API, no auth: `GET https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/organizations/slug/{provider_id}` → `data.salesforce_id`, then `GET …/organizations/{salesforce_id}/publications?limit=12&type=Church` → `data[].fileUrl` / `publishDate`. The PDFs on `container.parishesonline.com` download directly. |
| `discover_mass` (3) | The church page is server-rendered and works with WebFetch and curl. **Python `urllib`'s default User-Agent gets 403**, so send a browser UA. | The first `download.php?bulletin=` link is the current bulletin. Its cover `<img class="bulletin-cover X-\|YYYY-MM-DD\|…">` holds the date. Old `download.php` links keep working. |
| `other` / `google_drive` (21) | Mostly fine (WordPress, Wix/"Pepyaka", Vercel). WebFetch reads them. | Fetch the site directly. `cabriniroc.org` (Cloudflare) and `stmonicaofrochester.org` (429 when hit quickly) are the exceptions. |

Also Cloudflare-challenged for plain HTTP, whatever the provider: `stlouischurch.org`,
`holyspirit-saintjoseph.org`, `cabriniroc.org`, `stjohnschurchspencerport.org`.
`allsaintsparish.org` only rejects curl's default UA, so pass `-A` with a browser string.

## Why a browser doesn't reliably fix it here

The eCatholic and Cloudflare-protected sites sometimes answer with an interactive
Turnstile ("Performing security verification / Verify you are human"). Solving it
needs `brunhild.challenges.cloudflare.com`, and **the sandbox egress policy denies
that host.** It shows up as `connect_rejected` in
`curl -sS "$HTTPS_PROXY/__agentproxy/status"`. Don't try to route around that
denial or click through the CAPTCHA; use the routes above.

Measured with `scripts/probe_browser.py` on 6 challenged URLs:

- **Headless** Chromium, with or without playwright-stealth: blocked 12/12.
- **Headed under xvfb** with stealth (what the pipeline does): 5/12 loaded.
  When it works, Cloudflare returns 200 with no challenge at all; when it doesn't,
  waiting longer never helps. It varies from run to run.

The weekly GitHub Actions job (headed, xvfb, stealth) does get eCatholic pages
most weeks. Still, `data/metadata.json` shows `net-catholic` stuck on 2026-09-06
while its 09-20 PDF existed on `files.ecatholic.com`, so the pipeline misses some too.

## Running Playwright in the cloud sandbox

Two things break Chromium here before any site gets a chance to block it:

1. **Browser build mismatch.** The venv's Playwright (1.58) wants `chromium-1208`, but
   the image ships `chromium-1194`, and `playwright install` is blocked. Pass
   `executable_path="/opt/pw-browsers/chromium"`.
2. **`ERR_CERT_AUTHORITY_INVALID`.** The agent proxy re-terminates TLS, and Chromium's
   NSS store (`~/.pki/nssdb`) does not have its CA (no `certutil` to add it). Trust
   exactly that CA by its public-key hash. TLS is still verified for everything else:

   ```bash
   SPKI=$(openssl x509 -in /root/.ccr/agent-proxy-ca.crt -pubkey -noout \
     | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | base64)
   # launch(..., args=[f"--ignore-certificate-errors-spki-list={SPKI}"])
   ```

`scripts/probe_browser.py` does both. It mirrors `src/pdf_extract/browser.py`
(stealth, headed by default) and reports OK/BLOCKED, the bulletin links it found,
and optional screenshots:

```bash
xvfb-run -a uv run python .claude/skills/parish-site-access/scripts/probe_browser.py \
  https://parishesonline.com/organization/all-saints-parish --screenshot /tmp/shots
```

`src/pdf_extract/browser.py` sets neither option, so `pnpm run fetch` fails to
launch Chromium in this sandbox. It works in Docker and CI, which install their own
matching browser and have no TLS-intercepting proxy.

Page timing: parishesonline.com loads its data from the API after
`domcontentloaded`, so wait for `a[href*='selectedPublication=']` (the pipeline
does) rather than scraping right away.
