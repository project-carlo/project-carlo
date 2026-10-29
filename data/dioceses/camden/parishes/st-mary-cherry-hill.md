---
name: St. Mary, The Catholic Church of
website: https://www.stmarycherryhill.org
bulletin_provider: other
provider_id: page-pdfs https://www.stmarycherryhill.org/site/cpage.asp?sec_id=180021590&cpage_id=180113937
publication: ['po-container:04/0346']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0346/20261101B.pdf
  seen: 2026-10-29
  note: 'Image-only PDF (8 pages; only the ''St. Mary Church | 04-0346'' LPi footer has text). Page 1
    rendered with render.py and read: masthead ''Catholic Church of St. Mary, 2001 Springdale Rd., Cherry
    Hill, NJ 08003'', ''November 1, 2026''; Mass Schedule Weekends Saturday 5:00pm, Sunday 8:30am & 10:30am*,
    Weekdays Monday-Friday 8:00am (Chapel); ''Rev. Michael Matveenko, Pastor''. No Korean Mass listed
    on pages 1-2 (page 2 Mass intentions are all English-language Masses at 8:00am, 5:00pm, 8:30am, 10:30am).
    Recheck can''t find the words as text.'
- url: https://www.stmarycherryhill.org/page/180021590/180114532/Mass-Schedule-2
  seen: 2026-10-29
  quote: 'Saturday: 5:00pm'
  note: 'Parish Mass Schedule page: Weekend Masses Saturday 5:00pm, Sunday 8:30am and 10:30am; Weekday
    Mass 8:00am (Monday-Friday); Confession Saturday 8:30am. No Korean-language Mass or second church
    is listed.'
- url: http://www.stmarycherryhill.org/site/cpage.asp?sec_id=180021590&cpage_id=180113937
  seen: 2026-10-29
  note: '''Parish Bulletins'' page of the Finalweb site: links PDFs under /home/180021590/180021590/Images/
    (''11.1.2026 revised with ads.pdf'', ''October 25 2026 REVISED with ads.pdf'', ''10.11.2026 revisedwith
    ads.pdf'', ...), which carry the same ''St. Mary Church | 04-0346'' footer as the ParishesOnline container
    issue.'
---

## Publisher

LPi (ParishesOnline) prints the bulletin: its pages carry the footer 'St. Mary Church | 04-0346' and the ParishesOnline container `04/0346` serves the 1 November 2026 issue (`container.parishesonline.com/bulletins/04/0346/20261101B.pdf`, 200 on 2026-10-29). The parish posts the same issues on its own Finalweb site's 'Parish Bulletins' page, as files under `/home/180021590/180021590/Images/` with a footer-matching 04-0346 imprint. The ParishesOnline organization slug could not be found (`probe po` of 04/0346 and five guessed slugs failed), so the row reads the parish's page, not the container. The issue is image-only; page 1 (rendered and read) is headed 'Catholic Church of St. Mary, 2001 Springdale Rd., Cherry Hill, NJ 08003' with Rev. Michael Matveenko as pastor, and lists Saturday 5:00pm, Sunday 8:30am and 10:30am, weekdays 8:00am (Chapel). It names no other church and no Korean-language Mass.

## Worship sites

One: 2001 Springdale Road (church record `st-mary-cherry-hill`). Not a church of this parish: the Korean mission of St. Yi Yun Il John, which GCatholic places at this address and whose own site says it meets in this building (see `excluded/st-yi-yun-il-john-korean-mission`). Neither the bulletin's page 1 and 2 nor the parish Mass Schedule page lists its Sunday 1:00 pm Mass.

## Website and bulletin provider

`other` with a `page-pdfs` recipe on the Parish Bulletins page. `fetch:check` (2026-10-29) picked `11.1.2026 revised with ads.pdf` (dated 2026-11-01, `current`, pdf, 8 pages); the file list on the page is not in date order (10.11, 10.4, 11.1, 9.27, October 18, October 25), and the resolver chose the newest by date. The PDF exceeds the 25 MB inspection limit, so `document_type` reports only the signature. The directory's `http://www.stmarycherryhill.org` redirects to the Finalweb site `www.stmarycherryhill.org/default.asp?sec_id=180021590`.

## Shared pastor

Rev. Michael J. Matveenko is Pastor here and Administrator of St. Thomas More, Cherry Hill (its 25 October 2026 masthead). The two publish separate bulletins (this one is LPi 04/0346, St. Thomas More's is John Patrick 632), so the rows stay separate; see `st-thomas-more-cherry-hill`.

## Not yet confirmed

The ParishesOnline organization slug. Retry by reading the footer links on a text-layer issue, or a ParishesOnline search for the parish; if found, set `bulletin_provider: parishes_online` with that slug.
