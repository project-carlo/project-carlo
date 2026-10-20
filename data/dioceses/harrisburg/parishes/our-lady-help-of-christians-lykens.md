---
name: Our Lady Help of Christians
website: https://www.ourlady-lykens.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:29061']
group: Rev. Michael Opoki, AJ, pastor of Our Lady Help of Christians (Lykens) and Queen of Peace (Millersburg)
evidence:
- url: https://files.ecatholic.com/29061/bulletins/20261015.pdf
  seen: 2026-10-20
  quote: 'Tuesday Oct 20 11.00am @ OL Funeral : Evelyn Koppenhaver'
  note: 'The 18 October 2026 issue (5 pages), filed under Thursday''s date (20261015.pdf), found by the
    fetch check. Page 1 masthead as in the 11 October issue ("October 18, 2026 Our Lady Help of Christians
    Parish, Parish Office: 732 East Main Street, Lykens"); page 2: Saturday Oct 17 4:00pm and Sunday Oct
    18 8:00am @ OL; Wednesday''s noon Mass at QP cancelled. No ''Williamstown''.'
- url: https://files.ecatholic.com/29061/bulletins/20261011.pdf
  seen: 2026-10-19
  quote: 4:00 p.m. Our Lady Help of Christians Church, Lykens
  note: 'Page 1 of the 11 October 2026 issue (4 pages). Masthead: Our Lady Help of Christians Parish,
    732 East Main Street, Lykens; Rev. Michael Opoki, AJ. Saturday Vigil 4:00 p.m. and Sunday 8:00 a.m.
    at Lykens; it also lists the 10:30 a.m. Sunday Mass at Queen of Peace, the pastor''s other parish.'
- url: https://files.ecatholic.com/29061/bulletins/20261011.pdf
  seen: 2026-10-19
  quote: Parish Websites•ourlady-lykens.org and queenofpeace-millersburg.org
  note: 'Same page: the two parishes keep two websites.'
- url: https://www.ourlady-lykens.org/
  seen: 2026-10-19
  note: Behind Cloudflare (probe url HTTP4XX; visit.py got through on a retry). The rendered page embeds
    ecatholic:29061, links /bulletins, and gives Mass times SAT 4:00 PM, SUN 8:00 AM, daily Mon/Tue/Fri
    8:30 AM. Read in a browser (parish-site-access visit.py).
- url: https://www.hbgdiocese.org/parishes/closed-parishes-and-records-locations/
  seen: 2026-10-19
  quote: Our Lady Help of Christian, Lykens
  note: The diocese's 'Closed Parishes and Records Locations' (as of November 21, 2024) lists Sacred Heart
    of Jesus, Williamstown under this parish, i.e. merged into it with its records here. The diocese's
    site sometimes drops scripted connections (recheck on 2026-10-19 got 'Remote end closed connection');
    plain curl and a browser (visit.py) loaded it the same day.
promoted: 2026-10-20
---

## Publisher

Our Lady Help of Christians, Lykens publishes its own weekly bulletin on its eCatholic site
(site 29061). I read the 11 October and 18 October 2026 issues: the page-1 masthead is "Our Lady Help of Christians Parish,
Parish Office: 732 East Main Street, Lykens", with Rev. Michael Opoki, AJ, and its schedule lists
Saturday Vigil 4:00 p.m. and Sunday 8:00 a.m. at Lykens and weekday Mass Monday, Tuesday and
Friday 8:30 a.m.

Fr. Opoki is also pastor of Queen of Peace, Millersburg, and this bulletin's schedule box also
lists Queen of Peace's 10:30 a.m. Sunday and Wednesday noon Masses. But Queen of Peace prints its
own two-page bulletin on its own eCatholic site (29106), with its own masthead, so the two are
separate rows (`queen-of-peace-millersburg`).

## Worship sites

- Our Lady Help of Christians, 732 East Main St., Lykens (`our-lady-help-of-christians-lykens`).

Sacred Heart of Jesus, 140 E. Market St., Williamstown (GCatholic 23794, not in the diocesan
directory) was a separate parish. The diocese's closed-parishes page lists it under this parish,
and this bulletin's schedule does not mention it (no "Williamstown" in the 11 or 18 October issues). No
source I found says the church closed or when, so it is in `open/sacred-heart-of-jesus-williamstown`.

## Website and bulletin provider

The website is the parish's eCatholic site (Cloudflare-protected; the eCatholic id came from
`visit.py`); its PDFs are at `files.ecatholic.com/29061/bulletins/<YYYYMMDD>.pdf` and fetch
without a browser. The file is not always dated by the Sunday: the 11 October issue is
`20261011.pdf`, but the 18 October issue is `20261015.pdf` (the Thursday before), so
`issues.py ecatholic` needs `--day thu` for some weeks. The fetch check (2026-10-20) found the 18
October issue (`20261015.pdf`) on its own. `ecatholic`.

The diocesan directory's map pin for Lykens repeats New Oxford's coordinates (39.8646,
-77.0570); the church row uses GCatholic's Plus Code instead.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows, under xvfb-run with Chrome): ok, picked the 18 October 2026 issue (20261015.pdf).

## Not yet confirmed

The directory's weekend times
(Vigil 4:15 p.m., Sunday 8:15 a.m.) are 15 minutes later than the bulletin's and the parish
site's 4:00 and 8:00; the bulletin is followed.
