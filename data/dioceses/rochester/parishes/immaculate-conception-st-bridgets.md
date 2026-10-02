---
name: Immaculate Conception/St. Bridget's
website: https://www.immaculateconceptionrochester.org
bulletin_provider: other
provider_id: ''
publication:
- url:https://www.immaculateconceptionrochester.org/bulletin-news
group: St. Monica / Immaculate Conception-St. Bridget's cluster
evidence:
- url: https://www.immaculateconceptionrochester.org/_files/ugd/309cee_8abae253aa794d1382e0a22d6872d95a.pdf
  seen: '2026-10-02'
  quote: Immaculate Conception / St. Bridget’s Church
  note: 'Page 1 of the 27 September 2026 issue (dated "09-27-2026" on the bulletin page): masthead and
    "Sunday Mass ~ 9:00 a.m."; it names this parish only.'
- url: https://www.immaculateconceptionrochester.org/_files/ugd/309cee_8abae253aa794d1382e0a22d6872d95a.pdf
  seen: '2026-10-02'
  quote: 445 Frederick Douglass Street, Rochester, NY 14608
  note: 'Page 1; the same page gives "Office located at: 34 Monica Street, Rochester, NY 14619" (shared
    with St. Monica).'
- url: https://www.immaculateconceptionrochester.org/bulletin-news
  seen: '2026-10-02'
  note: Wix page. After 2020-22 issues it lists one PDF per Sunday labelled with the date ("01-11-2026"
    ... "09-27-2026", "10-04-2026" and further Sundays to 12-27-2026); read in a browser (visit.py --links).
- url: https://ps.dor.org/directory/immaculate-conception-st-bridgets/
  seen: '2026-10-02'
  quote: Mass Schedule Sunday ~ 9:00 am
  note: 'Diocesan directory listing: "Cluster (St. Monica/Emmanuel Church of the Deaf)".'
promoted: 2026-10-02
---

## Publisher

Immaculate Conception / St. Bridget's publishes its own weekly bulletin (4 pages) on its Wix site. The 27 September 2026 issue masthead is "Immaculate Conception / St. Bridget's Church, A Roman Catholic Community of African American Tradition", with "Sunday Mass ~ 9:00 a.m." and the church address 445 Frederick Douglass Street. It does not mention St. Monica. It is a separate bulletin from St. Monica's (`st-monica-emmanuel`), although the pastor (Fr. Raymond Fleming), the office (34 Monica Street) and the diocesan "cluster" are shared; the rows share a `group`.

## Worship sites

One: `churches/immaculate-conception-st-bridgets.md`. The parish was formed from Immaculate Conception, St. Bridget's and St. Lucy's (the sacramental index lists St. Bridget, Immaculate Conception and St. Lucy as records now held here); only 445 Frederick Douglass Street holds Mass per the bulletin, the directory and GCatholic. The locator's "Immaculate Conception" entry (`directory:14-immaculate-conception`, no address) is this church.

## Website and bulletin provider

`immaculateconceptionrochester.org` is alive. It is Wix, which rate-limits plain fetches (429 to `probe url` and `probe pdf`; curl and a browser work); the browser-based fetch should be fine. The bulletin page lists date-labelled PDFs, so provider `other` reading the website is right.

## Not yet confirmed

That the pipeline's fetch is not blocked by the Wix 429s; `recheck` of these quotes may come back unreachable for the same reason.
