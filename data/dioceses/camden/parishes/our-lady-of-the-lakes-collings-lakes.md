---
name: Our Lady of the Lakes Parish
website: https://lakescatholic.com
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-of-the-lakes-church-collings-lakes-nj-08094
publication: ['url:https://www.church-bulletin.org/our-lady-of-the-lakes-church-collings-lakes-nj-08094#john-patrick-6045']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-of-the-lakes-church-collings-lakes-nj-08094/2026-11-01.pdf
  seen: 2026-10-29
  quote: 19 Malaga Road, Collings Lakes, NJ 08094
  note: 'Page 1 of the 1 November 2026 issue (text layer; the file''s title is ''6045-Bulletin''): ''Rev.
    Steven Pinzon, Pastor'', Rectory/Office 609.561.8313. Its Mass intentions list Saturday 5pm, Sunday
    9:30am, Tuesday 7pm, Wednesday-Friday 9:30am; no other church.'
- url: https://www.church-bulletin.org/our-lady-of-the-lakes-church-collings-lakes-nj-08094
  seen: 2026-10-29
  quote: Our Lady of the Lakes Church
  note: John Patrick Publishing listing for 19 Malaga Road, Collings Lakes, NJ 08094, linking https://lakescatholic.com
    as the parish site; dated PDFs weekly, latest 2026-11-01 (posted ahead), then 2026-10-25, 2026-10-18,
    2026-10-11. https://church-bulletin.org/6045 redirects (301, 302) to this listing.
- url: https://lakescatholic.com
  seen: 2026-10-29
  note: 'HTTP 403 to probe url and to the parish-site-access browser on http, https, with and without
    www (3 loads): bot-blocked. The site''s content was not read; the listing carries the bulletin.'
promoted: 2026-10-30
research:
- method: probe url and parish-site-access visit.py --bulletin on lakescatholic.com (http, https, www)
  url: https://lakescatholic.com
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: Read the parish site's Mass-times and bulletin pages if a method gets past the 403; confirm
    it links the same John Patrick listing
  retry_when: the 403 clears, or a different access method is available
---

## Publisher

John Patrick Publishing prints the bulletin (printer code 6045) and posts it on church-bulletin.org: the listing `our-lady-of-the-lakes-church-collings-lakes-nj-08094` has uniform dated PDFs, latest 2026-11-01. The 1 November 2026 issue's page 1 is headed with 19 Malaga Road, Collings Lakes, names Rev. Steven Pinzon as pastor, and its Mass intentions list one church's Masses. Found by a web search for the parish's bulletin; `church-bulletin.org/6045` resolves to the same listing.

## Worship sites

One: 19 Malaga Road (`our-lady-of-the-lakes-collings-lakes`). No other church appears in the bulletin.

## Website and bulletin provider

The parish's own site (`lakescatholic.com`, from the directory) answers 403 to every method tried, so its bulletin page wasn't read; the listing links it, so it is the parish's site. `other` with `page-pdfs` on the listing, as for the other John Patrick parishes here.
