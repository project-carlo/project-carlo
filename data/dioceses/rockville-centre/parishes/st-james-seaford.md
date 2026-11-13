---
name: St. James
website: https://stjamesrcchurch.org/
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://stjamesrcchurch.org/#st-james-seaford']
group: ''
evidence:
- url: https://html.duckduckgo.com/html/?q=%22St.+James%22+Seaford+NY+church+bulletin
  seen: 2026-11-13
  note: Search result (read with visit.py) links https://stjamesrcchurch.org/wp-content/uploads/2024/10/10-20-24-St.-James.pdf,
    a bulletin PDF named by date and hosted on the parish's WordPress site. The file itself answers 403
    (Cloudflare); not read.
- url: https://stjamesrcchurch.org/
  seen: 2026-11-13
  note: 'Cloudflare ''Just a moment...'' on every load: probe url HTTP 403; visit.py verdict BLOCKED on
    five runs (8 loads each).'
research:
- method: visit.py --bulletin on stjamesrcchurch.org (https, http, /bulletin), 5 runs; probe get on guessed
    2026 PDF names and the WordPress media API; ParishesOnline slugs st-james-church-11783, st-james-rc-church-11783,
    st-james-11783; DuckDuckGo searches; Wayback CDX (archive offline)
  url: https://stjamesrcchurch.org/
  checked: '2026-11-13'
  outcome: access-blocked
  next_action: Load stjamesrcchurch.org with visit.py --bulletin again; if it loads, read the newest issue's
    masthead and Mass schedule, set bulletin_provider other with a pinned page-pdfs recipe, run fetch:check
    and clear fetch_gap. Otherwise try the Wayback CDX for stjamesrcchurch.org/wp-content/uploads/2026/*
    to confirm current issues.
  retry_when: Cloudflare stops challenging the browser, or web.archive.org is back online
  revisit_after: 2026-12-01
bulletin_status: access-blocked
fetch_gap:
  kind: cloudflare-challenge
  seen: 2026-11-13
  note: 'stjamesrcchurch.org answers every load with Cloudflare''s ''Just a moment...'' challenge: probe
    url and probe get 403 (home page, /wp-content/uploads PDFs, /wp-json), visit.py BLOCKED on 5 runs
    of up to 8 loads each, and fetch:check ''blocked NoBulletin: No bulletin page link found for other
    provider at https://stjamesrcchurch.org/''. A search engine indexes self-hosted bulletin PDFs on the
    site (wp-content/uploads/2024/10/10-20-24-St.-James.pdf).'
  url: https://stjamesrcchurch.org/
---

## Publisher

Not read. St. James, 80 Hicksville Road, Seaford appears to post its own bulletin as dated PDFs on its WordPress site: a search engine indexes `https://stjamesrcchurch.org/wp-content/uploads/2024/10/10-20-24-St.-James.pdf` (20 October 2024). No 2026 issue could be read, because the site answers every request with Cloudflare's challenge (see *Website and bulletin provider*). Inferred, not checked: that the parish still publishes weekly and on its own.

## Worship sites

One: the church at 80 Hicksville Road (`st-james-seaford-church`), on the diocese's word. The diocesan locator (directory:48), GCatholic (16914) and the drvc.org Mass-times page list only this church; the Mass-times page gives Saturday 4:00 PM, Sunday 8:00 AM, 10:00 AM and Noon, Monday-Saturday 8:00 AM. No bulletin was read to confirm it.

## Website and bulletin provider

stjamesrcchurch.org (the address every list gives) is behind Cloudflare. On 2026-11-13 `probe url` and `probe get` answered 403 for the home page, guessed PDFs and `/wp-json`; `visit.py --bulletin` was BLOCKED on five runs (https, http and `/bulletin`); `fetch:check` reported "blocked NoBulletin: No bulletin page link found for other provider". ParishesOnline has no org under the usual slugs, and searches found no copy on another host. The row is `unsupported` with `fetch_gap` `cloudflare-challenge` until the site can be read.

## Not yet confirmed

The current bulletin, its masthead and Mass schedule, and that it covers only this church. See `research`: retry `visit.py` on the site after 2026-12-01, or the Wayback CDX once the archive is back.
