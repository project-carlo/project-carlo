---
name: parish-site-access
description: Use before trying to open, scrape, or debug any parish website or bulletin provider (parishesonline.com, files.ecatholic.com, discovermass.com, Google Drive) from an agent session — including running `pnpm run fetch` / `pnpm detect`, checking why a parish's bulletin is stale, or verifying a URL in data/parishes.csv. Explains what blocks access from a Claude Code cloud container (the session's egress policy, not the sites), what does and does not work, how to get unblocked, and the container-specific Playwright/TLS fixes needed once hosts are allowed.
---

# Reaching parish sites from an agent session

## Short version

In a Claude Code **cloud** session, every parish site and bulletin provider
is blocked by the **session's network egress policy**. The sites themselves
aren't blocking you. Whether you use WebFetch, curl, Python `urllib`, or
Playwright (stealth or not, headed or headless), the connection is refused
at the agent proxy before it reaches the site.
A browser, different headers, or a different user agent can't fix that.

**Do not try to route around it** (third-party fetch/cache/proxy services,
triggering the GitHub Actions workflow to fetch pages for you, archive
mirrors, etc.). The policy is the user's setting. Tell them which hosts are
denied and let them change it (see "Getting unblocked").

Last verified 2026-09-24: all 62 parish websites in `data/parishes.csv`
plus the 6 provider hosts were `egress-blocked` over both plain HTTP and
Playwright.

## How each tool fails

| Tool | Symptom | Meaning |
|---|---|---|
| WebFetch | `EGRESS_BLOCKED ... blocked by the network egress proxy` | policy denial |
| curl / urllib | HTTP `000`, or `Tunnel connection failed: 403 Forbidden` | proxy answered 403 to CONNECT |
| Playwright / Chromium | `net::ERR_TUNNEL_CONNECTION_FAILED` | same 403, as Chromium reports it |
| WebSearch | **works** (runs server-side) | but see caveats below |

Confirm with the proxy's own log. Each denied host shows up as
`connect_rejected` / `gateway answered 403 to CONNECT`:

```bash
curl -sS "$HTTPS_PROXY/__agentproxy/status" | python3 -c \
  "import json,sys; [print(f['host'], f['detail']) for f in json.load(sys.stdin)['recentRelayFailures']]"
```

If even `https://example.com` is refused, the environment is on the
**Trusted** level (or Custom/None). That was the case when these findings
were recorded. See "Getting unblocked" before blaming the sites or the
user's claude.ai settings.

## Run the probe first

```bash
uv run python .claude/skills/parish-site-access/probe.py            # every parish + provider host
uv run python .claude/skills/parish-site-access/probe.py --slug st-jerome --slug peace-of-christ
uv run python .claude/skills/parish-site-access/probe.py --http-only  # skip Playwright
xvfb-run -a uv run python .claude/skills/parish-site-access/probe.py # headed, like production
```

For each target it gives one status for plain HTTP and one for Playwright:
`ok` (with a count of "bulletin" links, as a rough navigability check),
`egress-blocked`, `bot-challenge` (Cloudflare/WAF page), `http-<code>`, or
`error`. Takes about 30 s when everything is blocked.

- `egress-blocked` anywhere: stop and ask the user to allow the hosts.
- `bot-challenge`: this is the site's own protection. See "Site-side bot
  protection".

## Getting unblocked (the user has to do this)

**Two different settings, and only one of them matters here.** claude.ai
**Settings → Capabilities → Domain allowlist = "All domains"** controls
the claude.ai chat / Cowork code-execution sandbox. It does **not** apply to
Claude Code cloud sessions. The user set that one to "All domains" and every
parish host was still refused. (Separately, anthropics/claude-code#93562
reports that even that setting has been ignored since 2026-09-11 on the
surfaces it does govern.)

What controls this container is the cloud **environment's Network access
level**. Check it with the `list_environments` tool: this repo's sessions
ran in `Default` with the description "Default - trusted network access".
The levels, per https://code.claude.com/docs/en/cloud-environments:

| Level | Reaches |
|---|---|
| None | nothing (GitHub, MCP connectors and the Anthropic API still work) |
| **Trusted** (default) | package registries, GitHub, cloud SDKs, and nothing else. No parish sites. |
| **Full** | any domain |
| **Custom** | your own list, optionally plus the Trusted defaults |

To change it: at claude.ai/code, click the cloud icon with the environment
name in the row above the message box, hover the environment, click the
gear, then set **Network access** to **Full**, or to **Custom** with the
hosts below and "Also include default list of common package managers"
ticked. There's no settings page or URL for this. Then **start a new
session**: resuming this one after the Capabilities change made no
difference, and the docs say sessions read environment config at startup.

Hosts the pipeline needs. The first block covers most fetches: from
`data/metadata.json`, 613 of 1279 bulletins came from parishesonline.com,
199 from files.ecatholic.com and 86 from bulletins.discovermass.com.

```
parishesonline.com
container.parishesonline.com
files.ecatholic.com
discovermass.com
bulletins.discovermass.com
drive.google.com
# PDF hosts some "other" parishes link to
media.thechurchcoassets.com
s3-us-west-2.amazonaws.com
# every parish website: the `website` column of data/parishes.csv, e.g.
#   python3 -c "import csv;from urllib.parse import urlparse;[print(urlparse(r['website']).netloc) for r in csv.DictReader(open('data/parishes.csv'))]"
# add both the bare and www. form, since several sites redirect between them
```

Only the provider block is needed for `parishes_online` / `ecatholic` /
`discover_mass` parishes. The fetch stage goes straight to the provider,
not the parish site. `other` parishes and `pnpm detect` need the parish
websites themselves. Re-run the probe after the change and before doing
anything else.

## What WebSearch can and can't do here

WebSearch still works, but it only returns titles and URLs, and its index is
**stale**. The newest parish bulletin PDFs it returned were from mid-2025.
Don't use it to find "this week's bulletin", and don't use it to change a
parish's `bulletin_provider`. Example: searching for St. Jerome returns
old `container.parishesonline.com` PDFs, but the parish has been on
eCatholic (`files.ecatholic.com/22370/...`) through September 2026.

It *is* useful for discovery, e.g. learning a provider's URL shape:
Parishes Online PDFs live at
`container.parishesonline.com/bulletins/<region>/<org>/<YYYYMMDD>B.pdf`,
and eCatholic PDFs at `files.ecatholic.com/<site-id>/bulletins/<YYYYMMDD>.pdf`.
You still can't download them until the hosts are allowed.

## Once hosts are allowed: container gotchas

Even with the network open, the pipeline as written will not run unmodified
in a cloud container. `probe.py` already handles all four of these. Copy its
approach if you drive Playwright yourself:

1. **Playwright can't find its browser.** The Python `playwright` pin
   (1.58) wants `chromium_headless_shell-1208`. The image ships build 1194
   at `/opt/pw-browsers`. Don't run `playwright install`, because
   cdn.playwright.dev is blocked. Instead launch with
   `executable_path="/opt/pw-browsers/chromium"`.
2. **Chromium doesn't trust the agent proxy's CA**, so allowed hosts fail
   with `ERR_CERT_AUTHORITY_INVALID`. Trust only that key. Do not use
   `--ignore-certificate-errors` or `ignore_https_errors`:
   ```bash
   SPKI=$(openssl x509 -in /root/.ccr/agent-proxy-ca.crt -pubkey -noout \
     | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | base64)
   # launch(args=[f"--ignore-certificate-errors-spki-list={SPKI}"])
   ```
   Chromium picks up `HTTPS_PROXY` from the environment on its own, so no
   `proxy=` argument is needed.
3. **Python 3.13 urllib rejects the proxy CA** with
   `CA cert does not include key usage extension`, because of the
   `VERIFY_X509_STRICT` default. This breaks the pipeline's PDF downloads
   (`fetch._http_get_bytes`). Clear just that flag on a default context:
   `ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT`. The chain is still
   verified.
4. **No display.** `DISPLAY` is unset and `launch_stealth_browser`
   defaults to headed. Either wrap the command in `xvfb-run -a` (installed),
   which matches the Docker/CI setup, or set `PLAYWRIGHT_HEADLESS=1`.
   `pnpm detect` asks for `channel="chrome"`, and real Chrome is not
   installed here. Set `PLAYWRIGHT_BROWSER_CHANNEL` to something that
   exists, or expect `detect` to fail.

Items 2 and 3 only apply behind the Claude Code agent proxy
(`/root/.ccr/agent-proxy-ca.crt` exists). Keep them out of
`src/pdf_extract` unless the user wants cloud-session support in the
pipeline itself.

## Site-side bot protection (for when you can actually reach the sites)

None of this could be tested from the cloud container, because egress
blocks everything first. It is what the pipeline already does, and it
works on GitHub-hosted runners every week (`.github/workflows/weekly-docker.yml`):

- `pdf_extract/browser.py` applies `playwright-stealth` and runs **headed**
  (under `xvfb` in Docker/CI), because true headless is more often flagged.
- `pdf_extract/detect.py` uses the **real Chrome channel** for parish home
  pages because bundled Chromium fails some Cloudflare checks. It also
  waits up to 15 s for a `Just a moment...` challenge title to clear.
- PDF downloads use plain `urllib` with a desktop Chrome User-Agent and the
  bulletin page as `Referer`.
- eCatholic hides PDF links in a collapsed archive panel. Wait for
  `state="attached"`, not visible, and reload once if the panel is empty.
- The Parishes Online widget is an iframe. Look for `publication-page` /
  `selectedPublication=` links inside the `parishesonline` frame.

If the probe reports `bot-challenge` for a site after egress is open, try
the same URL headed under `xvfb-run -a` with stealth before anything else.
That combination is the one known to work.

To see how the real sites behaved recently without network access, read the
logs of the latest scheduled "weekly" workflow run (GitHub MCP
`actions_list` / `get_job_logs`). Fetch warnings like `Skipping parish` or
`has no bulletin newer than 14 days` name the problem parishes. Reading
existing logs is fine. Don't dispatch the workflow just to fetch pages for
yourself.
