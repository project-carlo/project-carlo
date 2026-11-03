---
name: St. Joseph, Demarest
website: https://www.stjosephdemarest.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Planning Area B
evidence:
- url: https://www.stjosephdemarest.com/images/pdf/bulletin.pdf
  seen: 2026-11-03
  quote: Twenty-sixth Sunday in Ordinary Time
  note: 'The only bulletin the site links (''Sunday Bulletin'' menu item, bulletin.pdf?refresh=yes) is
    the 28 September 2025 issue: page 1 ''PARISH OF ST. JOSEPH, 573 PIERMONT ROAD - DEMAREST, NEW JERSEY
    07627'', ''September 28, 2025'', Rev. Raphael Lee, Pastor; Mass schedule weekdays 8:00 am, Saturdays
    9:00 am, Vigil Saturday 5:00 pm, Sundays 9:30 am, 12:30 pm, Korean Masses Vigil Saturday 8:00 pm and
    Sundays 8:00 & 11:00 am. Page 6 footer: ''126A (PK) - St. Joseph’s - Demarest, NJ … BON VENTURE SERVICES,
    LLC''.'
- url: https://www.stjosephdemarest.com/about-our-parish/liturgical-schedules
  seen: 2026-11-03
  quote: KOREAN MASS SCHEDULE
  note: 'Site''s schedule page (probe get): Mass weekdays 8 AM, Saturdays 9 AM, Saturday Vigil 5 PM, Sundays
    9:30 AM & 12:30 PM; Korean Mass schedule Mon/Thu 6:30 AM, Tue/Fri 8:30 PM, Wed 10:00 AM, Sat 11:00
    AM, Saturday Vigil 8:00 PM, Sundays 8:00 AM and 11:00 AM. Footer ''© 2026 St. Joseph Church, Demarest''.'
- url: https://www.stjosephdemarest.com/
  seen: 2026-11-03
  note: 'Homepage (probe get and visit.py, Trinity Publishing site): menu links ''Sunday Bulletin'' to
    /images/pdf/bulletin.pdf?refresh=yes and ''korean.sjdnj.org''; no publisher id, no sponsors.bonventure.net
    link.'
revisit: Check whether the site's 'Sunday Bulletin' link (images/pdf/bulletin.pdf) carries a current issue,
  and whether korean.sjdnj.org loads and posts a bulletin; if current, set provider other with page-pdfs
  on the homepage and run fetch:check.
revisit_after: 2026-12-01
research:
- method: probe get / probe pdf of the site's Sunday Bulletin link, with and without ?refresh=yes; visit.py
    --bulletin on the homepage
  url: https://www.stjosephdemarest.com/images/pdf/bulletin.pdf
  checked: '2026-11-03'
  outcome: not-found
  next_action: Re-read the Sunday Bulletin link; if it carries an issue from the last two weeks, set provider
    other with page-pdfs https://www.stjosephdemarest.com/ and run fetch:check
  retry_when: The site's bulletin.pdf is updated past 28 September 2025
  revisit_after: 2026-12-01
- method: visit.py (headed, --retries 5) on the Korean community site the parish menu links
  url: https://korean.sjdnj.org/
  checked: '2026-11-03'
  outcome: access-blocked
  next_action: Open korean.sjdnj.org with visit.py again; look for a weekly bulletin (주보) and whether
    it covers the whole parish or only the Korean community
  retry_when: A later visit.py run gets past the 'Checking your browser...' page
- method: 'Looked for this parish''s Bon Venture listing (code 126A): no sponsors.bonventure.net link
    on the parish site, and sponsors.bonventure.net has no parish search'
  url: http://sponsors.bonventure.net/
  checked: '2026-11-03'
  outcome: not-found
  next_action: Check the parish site and its Korean site for a sponsors.bonventure.net link
  retry_when: The parish site or another source links a sponsors.bonventure.net/?page=<id> listing
bulletin_status: not-found
---

## Publisher

The Parish of St. Joseph, Demarest, prints a weekly bulletin with Bon Venture Services (footer '126A (PK) - St. Joseph’s - Demarest, NJ'), but the only issue it posts online is the 28 September 2025 one: the site's 'Sunday Bulletin' link (/images/pdf/bulletin.pdf?refresh=yes) served that issue on 2026-11-03, with and without the refresh parameter. Its page 1 masthead names 'PARISH OF ST. JOSEPH, 573 PIERMONT ROAD - DEMAREST' alone, with one Mass schedule that includes the Korean community's Masses. No current issue was found, so the row is `no_bulletin` (kept in the records, off the site) until one is.

## Worship sites

- St. Joseph Church (`st-joseph-demarest`): English Masses Saturday 5:00 PM, Sunday 9:30 AM and 12:30 PM, weekdays 8:00 AM, Saturday 9:00 AM; Korean Masses Saturday 8:00 PM, Sunday 8:00 and 11:00 AM and on weekdays (site's Liturgical Schedules page, 2026-11-03; the same in the September 2025 bulletin).

The directory lists one parish (21). GCatholic lists St. Joseph twice: 18377 at 280 County Rd. (website stjosephdemarest.com) and 18378 at 274 County Rd. (website stjosephkcc.org, the St. Joseph Korean Catholic Community; it answered HTTP 502 to visit.py). Both carry the same Plus Code 87G8X26Q+28, and the parish's own schedule lists the Korean Masses as its own, with no other building named. I read them as one church with an English and a Korean community and linked both entries to it; that the Korean Masses are in the same building is inferred from the shared Plus Code and the single schedule, not stated.

## Website and bulletin provider

https://www.stjosephdemarest.com/ (the directory's http:// address redirects there) is a Trinity Publishing site that answers `probe get`. It embeds no publisher id and links no sponsors.bonventure.net listing. The Korean community's site, korean.sjdnj.org (linked from the parish menu), answered 'Checking your browser...' (403) to visit.py on every load; sjdnj.org itself is a bare page with no parish words.

No publication id is recorded: the Bon Venture code 126A identifies the printed bulletin, but there is no scheme for it and no listing was found.

Fetch check (2026-11-03): refused, 'no_bulletin, so there is nothing to fetch'. Run it again once a current issue is found and the provider is set.

## Not yet confirmed

- A current bulletin: see `research` (site bulletin link stale since September 2025; Korean site blocked; no Bon Venture listing found). Revisit after 2026-12-01.
- Whether the Korean community publishes its own bulletin (it would be a separate row if it does).
