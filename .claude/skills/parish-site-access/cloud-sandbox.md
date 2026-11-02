# parish-site-access in a Claude Code cloud sandbox

Only for a cloud sandbox. The factory's host already has Chrome, and its workers don't
read this page.

## Setup, once per sandbox (~1 min)

```bash
.claude/skills/parish-site-access/scripts/setup_browser.sh
```

This installs Google Chrome and trusts the agent proxy's TLS certificate in Chrome's store.
Before it runs, no browser starts at all:

- The venv's Playwright wants a newer Chromium than the image ships, and
  `playwright install` is blocked.
- The proxy re-terminates TLS, so every page fails with `ERR_CERT_AUTHORITY_INVALID`.

## What the sandbox's network changes (measured 2026-09-25)

- **The Cloudflare challenge can't be solved here.** Its "Verify you are human" step needs
  `brunhild.challenges.cloudflare.com`, which the environment's egress policy denies
  (`connect_rejected` in `curl -sS "$HTTPS_PROXY/__agentproxy/status"`). Don't route around
  it. The user can add that host in the environment's network settings.
- The egress IP rotates across a pool, and the IP doesn't predict the outcome.
- **`probe url`'s DEAD-DNS is real here.** The domains it flagged don't resolve, and the
  proxy can't reach them either.
