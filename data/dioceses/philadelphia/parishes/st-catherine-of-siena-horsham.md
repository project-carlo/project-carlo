---
name: St. Catherine of Siena Parish
website: https://stcatherineschurch.org
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://stcatherineschurch.org/news/bulletin']
group: ''
evidence:
- url: https://stcatherineschurch.org/news/bulletin/200-october-25-2026/file
  seen: 2026-10-28
  note: 'The 25 October 2026 issue (7 pages, image-only; fetched inside the browser page, rendered and
    read): cover "Saint Catherine of Siena Parish / 321 Witmer Rd. Horsham, PA 19044 ~ 215-672-2881",
    "Father Joseph F. Rymdeika, Pastor"; Mass Schedule "Saturday Vigil: 5pm, Sunday: 7:00, 9:00, and 11:15am.
    Daily: 9:00am Mon.-Sat."; page 2 "30th Sunday in Ordinary Time". It names no other church.'
- url: https://stcatherineschurch.org/news/bulletin
  seen: 2026-10-28
  note: The parish site (HTTP 403 to probe url and probe get; read with the browser) has a News > Bulletin
    page listing issues as /news/bulletin/<n>-<month>-<d>-<yyyy>/file, newest "200-october-25-2026", then
    "199-october-18-2026".
- url: https://www.church-bulletin.org/saint-catherine-of-siena-parish-horsham-pa-19044
  seen: 2026-10-28
  note: 'John Patrick Publishing listing id 117, "Saint Catherine of Siena Parish", Horsham, PA 19044,
    shows daily readings and no bulletin editions: not the parish''s channel.'
- url: https://archphila.org/parish/st-catherine-of-siena-horsham/
  seen: 2026-10-28
  note: 'Directory entry: Rev. Joseph F. Rymdeika; 321 Witmer Rd.; website stcatherineschurch.org; Mass
    times Saturday vigil 5 PM, Sunday 7, 9, 11:15 AM, weekdays 9 AM.'
revisit: Retry fetch:check when the resolver can read Squarespace /file links (or the site stops answering
  403 to plain downloads); the row then becomes `other` with a page-pdfs recipe on https://stcatherineschurch.org/news/bulletin.
revisit_after: 2026-12-01
research:
- method: fetch:check with page-pdfs, dated-post, linked-issue-page and redirected-pdf recipes, and with
    no recipe, on https://stcatherineschurch.org/news/bulletin
  url: https://stcatherineschurch.org/news/bulletin
  checked: '2026-10-28'
  outcome: access-blocked
  next_action: Add a collector for Squarespace issue links ending in /file whose target is a PDF that
    only a browser session can download (plain probe get answers 403; in-page fetch() in Chrome returns
    the PDF)
  retry_when: The resolver reads /file links or the site stops blocking plain downloads
- method: 'Searched for another channel: John Patrick listing 117 (readings only, no editions); parish
    site links (only /news/bulletin); no ParishesOnline or eCatholic id on the site'
  url: https://www.church-bulletin.org/saint-catherine-of-siena-parish-horsham-pa-19044
  checked: '2026-10-28'
  outcome: not-found
  next_action: Look again if the parish moves its bulletin to a listing or provider
  retry_when: The John Patrick listing 117 shows an edition or the site changes provider
bulletin_status: access-blocked
---

## Publisher

St. Catherine of Siena publishes its own weekly bulletin on its own site (stcatherineschurch.org, Squarespace), News > Bulletin, newest issue "200-october-25-2026". The 25 October 2026 issue (image-only) was downloaded with an in-browser fetch, rendered and read: its cover reads "Saint Catherine of Siena Parish, 321 Witmer Rd. Horsham, PA 19044" with Father Joseph F. Rymdeika, Pastor, and gives the Mass Schedule. The old John Patrick listing (117) has never carried an edition, so it is not the channel.

## Worship sites

One church, 321 Witmer Rd. The cover's Mass box names one location; the directory and GCatholic list no other.

## Website and bulletin provider

The bulletin is real and current, but the pipeline can't fetch it. The site answers HTTP 403 to `probe url` and `probe get`, including for the `/file` issue links; `fetch:check` found no PDF links on the bulletin page or the post pages under any recipe tried (page-pdfs, dated-post, linked-issue-page, redirected-pdf, none). Chrome opens the `/file` URL and an in-page `fetch()` returns the PDF (200, application/pdf), so a collector for Squarespace `/file` links could read it. Until then the row is `no_bulletin` (Settled policy 4: kept in the records, left off the site) with `bulletin_status: access-blocked`.

## Not yet confirmed

Whether the resolver can be made to read the `/file` links. See `research` and `revisit`.
