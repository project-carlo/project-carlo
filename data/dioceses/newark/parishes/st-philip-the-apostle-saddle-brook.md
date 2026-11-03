---
name: St. Philip the Apostle, Saddle Brook
website: https://www.stphilipsb.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/518
publication: ['url:https://www.church-bulletin.org/saint-philip-the-apostle-saddle-brook-nj-07662']
group: Planning Area C
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-philip-the-apostle-saddle-brook-nj-07662/2026-11-01.pdf
  seen: 2026-11-03
  quote: 488 Saddle River Road, Saddle Brook, New Jersey 07663
  note: '1 November 2026 issue (12 pages, text layer). Page 1 masthead: ''November 1st, 2026, All Saints,
    St. Philip the Apostle'', 201 843 1888, www.stphilipsb.org.'
- url: https://www.church-bulletin.org/bulletin/saint-philip-the-apostle-saddle-brook-nj-07662/2026-11-01.pdf
  seen: 2026-11-03
  quote: 518 St. Philip the Apostle, Saddle Brook, NJ (b)
  note: The page-12 footer gives John Patrick Publishing id 518.
- url: https://www.church-bulletin.org/bulletin/saint-philip-the-apostle-saddle-brook-nj-07662/2026-11-01.pdf
  seen: 2026-11-03
  quote: Sunday Mass Schedule
  note: 'Page 9: Saturday evening 5:30 PM; Sunday 7:00, 8:30, 10:00 AM and 12:00 PM; weekdays 7:00 and
    8:30 AM; Saturdays 8:30 AM. Page 6 names ''St. Philip''s Daily Mass Chapel''. No other worship site
    is named.'
- url: https://www.stphilipsb.org/bulletin
  seen: 2026-11-03
  note: 'The parish''s eCatholic site (ecatholic:11774), read with visit.py: its Bulletin page says ''Click
    link below for weekly bulletin'' and links http://www.jppc.net/onlinebulletins/518template.pdf. issues.py
    found no files.ecatholic.com bulletins for 11774 (2026-10-25 to 2026-11-08, all 403).'
- url: https://church-bulletin.org/518
  seen: 2026-11-03
  note: The listing is titled 'Saint Philip the Apostle Bulletin' and lists 2026-11-01.pdf first, then
    weekly issues back from 2026-10-25.
bulletin_status: available
---

## Publisher

John Patrick Publishing prints St. Philip's bulletin (id 518). The parish's Bulletin page links jppc.net/onlinebulletins/518template.pdf, and church-bulletin.org/518 lists the issues. I read the 1 November 2026 issue (12 pages, text): the page-1 masthead reads "St. Philip the Apostle, 488 Saddle River Road, Saddle Brook, New Jersey 07663" and the page-12 footer "518 St. Philip the Apostle, Saddle Brook, NJ (b) ... John Patrick Publishing".

## Worship sites

There is one church, `st-philip-the-apostle-saddle-brook`. The page-9 schedule gives Saturday 5:30 PM, Sunday 7:00, 8:30, 10:00 AM and 12:00 PM, weekdays 7:00 and 8:30 AM and Saturday 8:30 AM. Page 6 mentions "St. Philip's Daily Mass Chapel", which I take to be part of the parish buildings (no other address is given). The archdiocese directory (183) and GCatholic (18551) each list only this church. The Church of the Korean Martyrs, 410 m away on the same road, is its own parish row (`korean-martyrs-saddle-brook`); this bulletin doesn't mention it.

## Website and bulletin provider

The website is the parish's eCatholic site https://www.stphilipsb.org/. It is only the website: issues.py found no files.ecatholic.com bulletins for site 11774, and its Bulletin page links John Patrick, so the eCatholic id stays out of `publication`, as the playbook says. The provider is `other`, pinned to `page-pdfs https://church-bulletin.org/518`. The listing's page URL (church-bulletin.org/saint-philip-the-apostle-saddle-brook-nj-07662) is the publication id, as for other John Patrick rows here. The listing's slug says 07662, but the parish's zip is 07663.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/518: current` and picked church-bulletin.org/bulletin/saint-philip-the-apostle-saddle-brook-nj-07662/2026-11-01.pdf, the 1 November 2026 issue read above (date observed in the text); freshness fresh. Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open.
