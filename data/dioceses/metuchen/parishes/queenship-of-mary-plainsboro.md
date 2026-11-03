---
name: Queenship of Mary
website: https://www.qomchurch.org
bulletin_provider: unsupported
provider_id: page-pdfs https://www.qomchurch.org/about-us/bulletin
publication: ['url:https://www.qomchurch.org/about-us/bulletin']
group: ''
evidence:
- url: https://www.qomchurch.org/about-us/bulletin/154-solemnity-of-all-saints/file
  seen: 2026-11-02
  quote: Queenship of Mary Church
  note: 'Page 1 of the Solemnity of All Saints, 1 November 2026 issue (10 pages, PDF created 28 Oct 2026;
    read from a browser download, since the host answers 403 to non-browser clients): masthead ''Queenship
    of Mary Church, 16 Dey Road, Plainsboro, NJ 08536''; ''Weekend Celebration Saturday 5:00pm Sunday
    8:30am and 10:30am; Weekday Celebration Monday 7:00pm, Tuesday - Saturday 8:00am''; page 5 lists ''Rev.
    Gerry Paderon, Pastor'' and ''Deacon Hugo P. Simão''. Names no other church.'
- url: https://www.qomchurch.org/about-us/bulletin
  seen: 2026-11-02
  note: The parish site's Bulletin page (Joomla; read in the browser) lists issues newest first as 154
    Solemnity of All Saints, 153 30th Sunday October 25 2026, 152 ... down to 142 16th Sunday July 19
    2026, each linked as /about-us/bulletin/<n>-<title>/file.
research:
- method: probe url, probe get, visit.py --bulletin, then a fetch() inside the browser page for the newest
    /file link
  url: https://www.qomchurch.org/about-us/bulletin
  checked: '2026-11-02'
  outcome: found
  next_action: Clear fetch_gap if fetch:check ever picks an issue from this page
  retry_when: A collector reads Joomla /file endpoints, or the site stops answering 403
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-02
  note: Bulletin issues are links of the form /about-us/bulletin/<n>-<title>/file (no .pdf name) on a
    host that answers 403 to probe get; fetch:check finds 'No PDF links found'. A real browser fetch of
    /154-solemnity-of-all-saints/file returned application/pdf (11 MB, 10 pages), so the bulletin exists
    and is current.
  url: https://www.qomchurch.org/about-us/bulletin
---

## Publisher

Queenship of Mary, 16 Dey Road, Plainsboro, publishes its own weekly bulletin on its own Joomla site, at https://www.qomchurch.org/about-us/bulletin. The 1 November 2026 issue (read 2026-11-02 from a browser download) is headed 'Queenship of Mary Church, 16 Dey Road, Plainsboro, NJ 08536' and gives the Mass schedule below; it names no other church or parish. The pastor line on page 5 is 'Rev. Gerry Paderon, Pastor'; the finder lists 'Administrator: Rev. Gerardo Paderon', the same person under a different title, so I took the title from the parish's own bulletin.

## Worship sites

One church, 16 Dey Road (directory:24531, gcatholic:18629). The bulletin's Mass schedule gives one site and no mission or chapel; the finder's Mass list for this entry is empty.

## Website and bulletin provider

Website: https://www.qomchurch.org (the finder gives http://www.qomchurch.org). `probe url` reports DEAD-DNS and `probe get` HTTP 403; the browser (visit.py) loads it. Provider `other`: the Bulletin page links `/about-us/bulletin/<n>-<title>/file`, not `.pdf` names. `fetch` can't collect it (*Fetch check*).

## Not yet confirmed

Nothing about the parish's identity or Mass schedule. Collection by `fetch` is blocked; see below.

## Fetch check

`pnpm fetch:check` on 2026-11-02 with the pinned recipe `page-pdfs https://www.qomchurch.org/about-us/bulletin` reported `resolve_failed`: 'No PDF links found on bulletin page'. Transport and document type were not checked. I confirmed by hand that the newest link, `/about-us/bulletin/154-solemnity-of-all-saints/file`, returns a 10-page PDF dated 1 November 2026 headed 'Queenship of Mary Church' when fetched inside a browser page; `probe get` gets 403. So the row has `fetch_gap` kind `joomla-file-endpoint` and the recipe above is a best guess that doesn't work yet.
