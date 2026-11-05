---
name: St. Gerard Majella
website: https://stgerardmajella.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:16550']
group: ''
evidence:
- url: https://files.ecatholic.com/16550/bulletins/20261101.pdf
  seen: 2026-11-04
  quote: ST. GERARD MAJELLA CATHOLIC CHURCH
  note: 'Page 1 of the 1 November 2026 issue (''Solemnity of All Saints - November 1, 2026''), read with
    probe pdf: ''ST. GERARD MAJELLA CATHOLIC CHURCH 501 WEST BROADWAY, PATERSON, NJ 07522'', www.stgerardmajella.org;
    weekend Masses Saturday 5:00PM (English), Sunday 9:00AM, 11:00AM (English), 1:00PM (Spanish); daily
    Monday - Saturday 8:15 AM, Thursday 7:00 PM (Español).'
- url: https://stgerardmajella.org/bulletins
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403; eCatholic site 16550). Lists files.ecatholic.com/16550/bulletins/<YYYYMMDD>.pdf
    issues, newest 'November 1, 2026' (20261101.pdf), then 25, 18, 11, 4 October, 27 September 2026.
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: 'Diocese of Paterson parish finder (directory:16550): ''St. Gerard Majella, Paterson'', 501 West
    Broadway, website https://stgerardmajella.org/; a second pin, directory:30898 ''St. Gerard Majella
    School'', has no address, no Mass times and website https://stgerardschool.org/.'
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. Gerard Majella, Paterson publishes a weekly bilingual bulletin on its eCatholic site, site id 16550 (the finder pin id). The 1 November 2026 issue (`https://files.ecatholic.com/16550/bulletins/20261101.pdf`, read 2026-11-04 with probe pdf) has on page 1 "ST. GERARD MAJELLA CATHOLIC CHURCH 501 WEST BROADWAY, PATERSON, NJ 07522", "Solemnity of All Saints - November 1, 2026" and the Mass schedule.

## Worship sites

One church, `st-gerard-majella-paterson`. The 1 November page 1 schedule names no other place, and a text search of all 8 pages for chapel, capilla, school, escuela and academy found only the staff line "St. Gerard Majella School Principal: Sr. Jo-Ann Pompa, M.P.F.". The parish school (finder pin directory:30898) is excluded as `st-gerard-majella-school-paterson` (no-public-mass). GCatholic lists the one church (19004).

## Website and bulletin provider

`https://stgerardmajella.org/` (the finder's website) is an eCatholic site behind Cloudflare: probe url gets 403, and visit.py on the home page hung twice on 2026-11-04 (no output in 110 s and 500 s), while visit.py on `/bulletins` loaded at once. That page lists weekly `files.ecatholic.com/16550/bulletins/<YYYYMMDD>.pdf` files, newest 20261101.pdf; `issues.py ecatholic` found 8 November not yet posted (403). Provider `ecatholic`, publication `ecatholic:16550`.

`fetch:check` on 2026-11-04 (headed Chrome) picked `https://files.ecatholic.com/16550/bulletins/20261101.pdf` (the 1 November 2026 issue, 3 days old, fresh); identity is reported unverified (no expected identity supplied) and was checked by hand on page 1 above.

## Not yet confirmed

Nothing open.
