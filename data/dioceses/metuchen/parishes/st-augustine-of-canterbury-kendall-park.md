---
name: St. Augustine of Canterbury
website: https://parish.staugustinenj.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:22672', 'po-container:03/4080']
group: ''
evidence:
- url: https://files.ecatholic.com/22672/bulletins/20261101.pdf
  seen: 2026-11-02
  quote: “Churchweek” - November 01, 2026 –All Saints Day
  note: 'The parish-hosted copy of the 1 November 2026 issue (20 pages, pages 2, 6, 9, 16 and 17 images).
    Page 1 is a cover image reading ''St. Augustine of Canterbury Church, 45 Henderson Road, Kendall Park,
    NJ 08824'' (read from a render of the identical container copy; the text layer only has the ''Churchweek''
    line); page 18 gives ''OUR PARISH IS SERVED BY REVEREND CANON ROBERT G. LYNAM, KCHS, PASTOR'' and
    ''MASS SCHEDULE SUNDAY MASSES: SAT—5PM | SUN—8AM, 10AM, 12NOON, 5PM; WEEKDAY MASSES: MON-FRI—9AM''.
    Names no other church.'
- url: https://container.parishesonline.com/bulletins/03/4080/20261101B.pdf
  seen: 2026-11-02
  quote: “Churchweek” - November 01, 2026 –All Saints Day
  note: 'The same issue on ParishesOnline container 03/4080: pdftotext of all 20 pages is byte-identical
    to the eCatholic file (same five image pages; I rendered pages 1 and 2 of this copy, not of the eCatholic
    one). One bulletin on two hosts, so only the parish-hosted eCatholic copy is the provider; the container
    id is recorded as an alias of the same publication.'
- url: https://parish.staugustinenj.org/mass-times
  seen: 2026-11-02
  quote: 'SATURDAY: 5:00 PM SUNDAY: 8:00 AM 10:00 AM 12:00 PM 5:00 PM MONFRI 9:00 AM'
  note: Mass Times page of the parish's eCatholic site (id 22672; read in the browser, 403 to probe get);
    its Bulletin page (parish.staugustinenj.org/bulletins) lists files.ecatholic.com/22672/bulletins/20261101.pdf
    and earlier Sundays back to 20260802.
promoted: 2026-11-03
bulletin_status: available
---

## Publisher

St. Augustine of Canterbury, 45 Henderson Road, Kendall Park, publishes its own weekly bulletin, 'Churchweek', on its eCatholic site (id 22672) at files.ecatholic.com/22672/bulletins/<YYYYMMDD>.pdf. The 1 November 2026 issue (read 2026-11-02) has a cover reading 'St. Augustine of Canterbury Church, 45 Henderson Road, Kendall Park, NJ 08824' and, on page 18, 'REVEREND CANON ROBERT G. LYNAM, KCHS, PASTOR', matching the finder's pastor line. It names no other church or parish.

The same issue is also on ParishesOnline container 03/4080 (found through a web search, not through the parish site): same page count and byte-identical extracted text. That is one publication, not two, so the parish row uses the parish-hosted eCatholic copy and lists the container id as an alias in `publication`.

## Worship sites

One church, 45 Henderson Road (directory:24501, gcatholic:18639). The bulletin's Mass schedule gives one site, and mentions a 'Chapel of the Saints' for confession and weekday use that is inside the same campus (page 18: 'CONFESSION SAT—11:30AM IN THE CHAPEL OF THE SAINTS'), which isn't a separate place with its own Mass times.

## Website and bulletin provider

Website: https://parish.staugustinenj.org (eCatholic 22672). The finder and GCatholic give http://www.staugustinenj.org, and the bulletin's own contact block still prints 'HTTP://WWW.STAUGUSTINENJ.ORG', but that domain no longer resolves to the parish: `probe get` on 2026-11-02 returned a Flash-era page headed 'Welcome to St. Augustine's Church' with replica-goods spam text, and the parish's current site is parish.staugustinenj.org (found by search: ddg.sh, 'St. Augustine of Canterbury Kendall Park NJ bulletin'; its footer gives 45 Henderson Rd., (732) 297-3000, matching the finder). `probe url` reports DEAD-DNS for both hosts and `probe get` 403 for the new one; visit.py loads it. Provider `ecatholic` with the parish site as website, as `fetch` reads eCatholic from `website`.

## Not yet confirmed

Nothing about identity or the Mass schedule.

## Fetch check

`pnpm fetch:check` on 2026-11-02 with provider `ecatholic` (read from the website) picked `files.ecatholic.com/22672/bulletins/20261101.pdf`: transport ok, PDF, issue date 2026-11-01 inferred from the file name, freshness `fresh` (1 day), identity unverified by the tool (I read the cover myself, above). No `recipe` is needed for an eCatholic row.
