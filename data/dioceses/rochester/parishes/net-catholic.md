---
name: N.E.T. Catholic
website: https://netcatholic.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:20434']
group: All Saints/Holy Cross/St. Anthony
evidence:
- {url: 'https://files.ecatholic.com/20434/bulletins/20260927.pdf', seen: 2026-10-02, quote: N.E.T. CATHOLIC
    DEACON, note: 'Page 1 of the 27 September 2026 issue, the bulletin of "North East Tompkins County
    (NET) Catholic": Fr. John Gagnier, Parochial Administrator, with the three churches All Saints (Lansing),
    Holy Cross (Freeville) and St. Anthony (Groton).'}
- {url: 'https://files.ecatholic.com/20434/bulletins/20260927.pdf', seen: 2026-10-02, quote: Mass @ Holy
    Cross, note: 'Page 2: that weekend’s Masses at all three churches.'}
- {url: 'https://netcatholic.org/bulletins', seen: 2026-10-02, quote: 'September 27, 2026', note: 'Bulletins
    page of the eCatholic site (site id 20434, behind Cloudflare; read with visit.py): one PDF per Sunday
    at files.ecatholic.com/20434/bulletins/YYYYMMDD.pdf, newest 20260927 on 2026-10-02.'}
- {url: 'https://ps.dor.org/directory/holy-cross-parish/', seen: 2026-10-02, quote: 'Weekly Bulletin Website:
    http://www.netcatholic.org', note: 'The Directory of Parishes lists the three churches as three parishes
    (All Saints, Holy Cross, Saint Anthony), all pointing at netcatholic.org.'}
promoted: 2026-10-02
---

## Publisher

N.E.T. (North East Tompkins) Catholic publishes one bulletin for All Saints (Lansing), Holy Cross (Freeville)
and St. Anthony (Groton). The 27 September 2026 issue lists all three with their addresses and a combined
Mass schedule ("6:30PM at All Saints", "8:30am at Holy Cross", "4:30pm at Saint Anthony"). Fr. John F.
Gagnier is Parochial Administrator of all three. The Parish Locator groups them as
"All Saints/Holy Cross/St. Anthony".

## Worship sites

`churches/all-saints.md`, `churches/holy-cross-freeville.md`, `churches/st-anthonys.md`. The George Jr.
Republic Chapel (Freeville) hosted a single 12:30 pm Mass on 4 October 2026 (bulletin page 2-3: "Mass &
Picnic at the George Jr. Republic Chapel"); it is a one-off, not a worship site, and is not in any roster.

## Website and bulletin provider

`netcatholic.org` is an eCatholic site (site id 20434; probe url gets a 403 from Cloudflare, so use
visit.py). The fetch stage reads the bulletins page from `website`, and `/bulletins` lists the PDFs. The
provider has no provider_id by design.

## Not yet confirmed

Nothing. (The 4 October issue was not up on 2026-10-02: eCatholic answers 403 for a missing issue.)
