---
name: Seven Dolors Parish, Yukon
website: https://www.sevendolors.org
bulletin_provider: other
provider_id: dated-post https://www.sevendolors.org/bulletins/ filename=[0-9]*.pdf
publication: ['url:https://www.sevendolors.org/bulletins/']
group: ''
evidence:
- url: https://www.sevendolors.org/wp-content/uploads/2026/10/101826.pdf
  seen: 2026-10-22
  quote: Seven Dolors Catholic Church
  note: 'Page 1 masthead of the 18 Oct 2026 issue (5 pages; linked from https://www.sevendolors.org/october-18-2026/;
    the PDF answers 403 to probe pdf but downloads with curl and a browser User-Agent): "Seven Dolors
    Catholic Church", "102 Center St., PO Box 308, Yukon, PA 15698", "Year A - Twenty-Ninth Sunday in
    Ordinary Time October 18, 2026"; MASS SCHEDULE "Saturday Vigil 4:00 PM", "Sunday 11:00 AM", "Weekday
    Mass - Mon & Wed 9:00 a.m."; pastoral staff "Rev. David J. Nazimek Pastor". Names Seven Dolors alone.'
- url: https://www.sevendolors.org/wp-content/uploads/2026/10/101826.pdf
  seen: 2026-10-22
  quote: Mass at St. Edward ~ 9:00am
  note: 'Page 2 intentions: Tuesday and Thursday weekday Masses are at St. Edward, Herminie (same pastor,
    its own bulletin: row st-edward-herminie).'
- url: https://www.sevendolors.org/bulletins/
  seen: 2026-10-22
  note: 'Diocese-template WordPress page (403 to probe url; curl with a browser User-Agent reads it) listing
    one post per issue: October 18, October 11, October 4, September 27 ... 2026. Each post embeds one
    dFlip PDF named MMDDYY.pdf (101826, 101126, 092726, 083026). The sidebar also links an altar-ministry
    schedule PDF.'
- url: https://parishesonline.com/organization/seven-dolors-church-15698
  seen: 2026-10-22
  note: 'probe po: LPi org "Seven Dolors Church", 102 Center St, Yukon (LPi 0018000000QxC0kAAF) has no
    publications and no container: not a live channel, not recorded.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=311
  seen: 2026-10-22
  note: 'Directory: Seven Dolors Parish, 102 Center Street, Yukon; pastor Father David J. Nazimek (also
    pastor of St. Edward, Herminie, LocationID 129); "Saturday: 4:00 p.m.; Sunday: 11:00 a.m."; no Partner
    Parishes listed.'
promoted: 2026-10-23
---

## Publisher

Seven Dolors Parish, Yukon publishes its own weekly bulletin on its diocese-template WordPress site. The
18 October 2026 issue (read 2026-10-22, `101826.pdf`) has the masthead "Seven Dolors Catholic Church, 102 Center
St., PO Box 308, Yukon" and a Mass schedule for Seven Dolors alone (Saturday Vigil 4:00 p.m., Sunday 11:00 a.m.,
Monday and Wednesday 9:00 a.m.).

Its pastor, Fr. David J. Nazimek, also leads St. Edward, Herminie; the two share staff and alternate weekday
Masses (the intentions say "Mass at St. Edward ~ 9:00am" on Tuesday and Thursday), and the contact block gives
the St. Edward office number. St. Edward nevertheless posts its own separately mastheaded issue each week
(`1018189.pdf` on saint-edward.org), so the two are separate rows (st-edward-herminie).

## Worship sites

One: Seven Dolors church, 102 Center Street, Yukon, the only Seven Dolors building in the schedule. The
Tuesday/Thursday Masses "at St. Edward" belong to the St. Edward row. No other building is listed by the
diocese or GCatholic for this parish.

## Website and bulletin provider

`website` is the parish's own site. Provider `other`, recipe `dated-post https://www.sevendolors.org/bulletins/
filename=[0-9]*.pdf`: the page lists one post per issue, each embedding the issue PDF (`MMDDYY.pdf`); the filter
keeps the sidebar's ministry-schedule PDF out (same template as saint-edward.org, where the unfiltered pick was a
sidebar calendar). `fetch:check` on 2026-10-22 picked `wp-content/uploads/2026/10/101826.pdf`, the 18 October
issue. The LPi organization `seven-dolors-church-15698` is empty and not recorded.

## Not yet confirmed

Nothing. (The site's PDFs answer 403 to `probe pdf`, but `fetch`, `recheck` (2026-10-22: all quotes found)
and curl with a browser User-Agent read them.)
