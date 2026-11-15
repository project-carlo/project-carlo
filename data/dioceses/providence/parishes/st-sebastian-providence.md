---
name: St. Sebastian, Providence
website: https://www.stsebastianri.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:21143']
group: ''
evidence:
- url: https://files.ecatholic.com/21143/bulletins/20261115.pdf
  seen: 2026-11-15
  quote: 67 Cole Ave., Providence, RI 02906
  note: 15 November 2026 issue (5 pages, text layer). Page 1 masthead 'CHURCH OF SAINT SEBASTIAN', Rev.
    Edward A. Sousa, Jr., Pastor, and 'Parochial Administrator St. Joseph Parish, 92 Hope St., Providence';
    Mass Schedule Saturday Vigil 4:00 p.m., Sunday 9:00 a.m. & 11:00 a.m., Daily Monday - Wednesday 8:00
    a.m. (Our Lady of Perpetual Help Chapel). No St. Joseph Mass times anywhere in the issue (grep 'Joseph'
    finds only the masthead line and a Mass intention).
- url: https://www.stsebastianri.org
  seen: 2026-11-15
  note: Parish site answers 403 to probe url (Cloudflare); in parish-site-access visit.py it is an eCatholic
    site embedding ecatholic:21143, with a Bulletins page at /bulletins.
- url: https://dioceseofprovidence.org/parishfinder
  seen: 2026-11-14
  note: Finder entry 12214 St. Sebastian, 67 Cole Ave., Pastor Rev. Edward A. Sousa, Jr.; entry 12208
    St. Joseph names him 'Administrator pro tem'.
bulletin_status: available
---

## Publisher

St. Sebastian publishes its own weekly bulletin on eCatholic (site id 21143). The 15 November 2026 issue (https://files.ecatholic.com/21143/bulletins/20261115.pdf), page 1, is headed "CHURCH OF SAINT SEBASTIAN", "67 Cole Ave., Providence, RI 02906", dated November 15, 2026, with Rev. Edward A. Sousa, Jr., Pastor.

## Worship sites

One church. The page-1 schedule lists Saturday Vigil 4:00 p.m., Sunday 9:00 and 11:00 a.m., and daily Mass Monday-Wednesday 8:00 a.m. in the Our Lady of Perpetual Help Chapel, which this row treats as a chapel of the same building, not a separate site. The finder (12214) and GCatholic (22431) list only this church.

The same priest administers St. Joseph, 92 Hope St., and the masthead names him "Parochial Administrator St. Joseph Parish, 92 Hope St., Providence". But the issue gives no St. Joseph Mass times, intentions or schedule: a search for "Joseph" finds only that masthead line and one intention. So the bulletin is St. Sebastian's alone, and St. Joseph is a separate row (st-joseph-providence).

## Website and bulletin provider

`ecatholic` on the parish's eCatholic site, which `probe url` can't read (403, Cloudflare) but visit.py can; issues are at `files.ecatholic.com/21143/bulletins/YYYYMMDD.pdf`.

## Not yet confirmed

The daily schedule (Mon-Wed 8:00 a.m.) differs from the finder's (Mon-Fri 7:00 AM); the bulletin is the newer source.
