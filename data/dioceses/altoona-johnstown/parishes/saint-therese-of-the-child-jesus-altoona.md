---
name: Saint Therese of the Child Jesus Parish, Altoona
website: https://sainttheresealtoona.org
bulletin_provider: ecatholic
provider_id: '37141'
publication: ['ecatholic:37141']
group: ''
evidence:
- url: https://files.ecatholic.com/37141/bulletins/20261017.pdf
  seen: 2026-10-21
  quote: Father Brian Norris, Pastor
  note: 'Page 1 of the issue for Sunday 18 October 2026 (listed as "October 17, 2026" in the site archive;
    4 pages, text layer). Masthead "Saint Therese of the Child Jesus", parish office 417 25th Avenue,
    Altoona PA 16601-3842; "Weekend Mass Schedule  Saturday Evening: ... 5:00 PM  Sunday Morning: ...
    8:00 AM & 10:30 AM". The issue names no other parish or church as part of this bulletin.'
- url: https://sainttheresealtoona.org/bulletins
  seen: 2026-10-21
  quote: October 17, 2026
  note: 'eCatholic bulletin archive (headed Chrome; curl gets a Cloudflare 403). Links are files.ecatholic.com/37141/bulletins/<YYYYMMDD>.pdf,
    dated by the Saturday before the Sunday (20261017.pdf, 20261010.pdf, 20261003.pdf, ...), weekly back
    to 3 January 2026. Footer: "St. Thérèse of the Child Jesus 411 Wopsononock Avenue, Altoona, PA 16601
    Parish Office: 417 25th Ave".'
- url: https://discovermass.com/church/st-therese-of-the-child-jesus-altoona-pa/
  seen: 2026-10-21
  quote: no bulletins available for St. Therese of the Child Jesus.
  note: 'The Discover Mass page exists (its Visit Website link is https://sainttheresealtoona.org/) but
    carries no bulletin: not a live channel.'
promoted: 2026-10-21
---

## Publisher

St. Therese of the Child Jesus Parish, Altoona (pastor Fr. Brian Norris, with Fr. Ashok Kumar
Alphonse as parochial vicar and Deacon Thomas McFee) publishes its own weekly bulletin on its
eCatholic site, sainttheresealtoona.org (eCatholic site id 37141). The newest issue read on
2026-10-21 is `https://files.ecatholic.com/37141/bulletins/20261017.pdf`, the issue for Sunday
18 October 2026 (the file is named for the Saturday): masthead "Saint Therese of the Child
Jesus", "Weekend Mass Schedule: Saturday Evening 5:00 PM, Sunday Morning 8:00 AM & 10:30 AM",
Father Brian Norris, Pastor. It names no other parish as a co-publisher.

St. Mark / Holy Rosary: the lead said their youth group meets with St. Therese's. The issue's
only mention of St. Mark is an announcement ("St. Mark's Catholic Church, 416 6th Avenue,
Altoona, will be holding their annual Triduum to St. Jude ... Mass will be at 5:30 pm each
night", 26-28 October). The bulletin carries no St. Mark or Holy Rosary Mass schedule, so it
does not cover their Masses; nothing joint to report for saint-mark-holy-rosary-altoona.

## Worship sites

One church, St. Therese of the Child Jesus (churches/saint-therese-of-the-child-jesus-altoona).
The Johnstown parish of the same name (536 Decker Ave) is a different parish with its own
roster entries.

## Website and bulletin provider

`bulletin_provider: ecatholic`, `provider_id: 37141`, `publication: ecatholic:37141`. The
directory's homepage `http://sttheresealtoona.com/` does not resolve (probe url: DEAD-DNS
twice, 2026-10-21); the working site is `https://sainttheresealtoona.org/`, which is the
"Visit Website" link on the Discover Mass page. It answers 403 to curl (Cloudflare) and loads
in headed Chrome; the PDFs on files.ecatholic.com fetch without a browser. `issues.py
ecatholic` probing Sundays finds nothing, because this parish dates files by the Saturday: use
`--day sat`.

## Not yet confirmed

Nothing about the bulletin. `pnpm fetch:check --diocese altoona-johnstown --parish saint-therese-of-the-child-jesus-altoona` on 2026-10-21 resolved the eCatholic site and fetched `files.ecatholic.com/37141/bulletins/20261017.pdf` (status ok, 915,002 bytes, url_date 2026-10-17), this week's issue. The church's street address is unsettled (see churches/saint-therese-of-the-child-jesus-altoona).
