---
name: St. Anne
website: https://stannebrentwood.org/index.php/bulletins
bulletin_provider: other
provider_id: page-pdfs https://stannebrentwood.org/index.php/bulletins
publication: ['url:https://stannebrentwood.org/index.php/bulletins']
group: ''
evidence:
- url: http://stannebrentwood.org/images/bulletins/2026/AnneBrent11-15r.pdf
  seen: 2026-11-13
  quote: 'Wednesday: 7:00pm (French Creole) (Chapel)'
  note: 'November 15th, 2026 issue (Canva, 12 pages). Page 1 masthead ''St. Anne''s R.C. Church'', 88
    Second Ave., Brentwood, New York 11717, with one MASS SCHEDULE: Monday-Friday 12:00 noon (English);
    Monday-Wednesday and Friday 5:00pm (Spanish); Wednesday 7:00pm (French Creole) (Chapel); Thursday
    5:00pm (English), 7:00pm (Spanish); Saturday 9:00am; weekends Saturday 5:00pm, 7:00pm (Spanish); Sunday
    7:30am, 9:00am (Spanish), 11:00am, 12:30pm (French Creole), 3:00pm (Spanish), 5:00pm, 6:00pm (Spanish).
    Back page ''#169 FOR ADVERTISING: THE CHURCH BULLETIN INC.'''
- url: https://stannebrentwood.org/index.php/bulletins
  seen: 2026-11-13
  note: Joomla bulletin page (probe get) links /images/bulletins/2026/AnneBrent<m>-<d>R.pdf for 8-2 through
    11-15.
revisit: Run fetch:check after the first January 2027 issue to confirm the yearless filenames still date
  correctly
revisit_after: 2027-01-10
promoted: 2026-11-13
bulletin_status: available
---

## Publisher

St. Anne, 88 Second Avenue, Brentwood publishes its own weekly bulletin, made in Canva and printed with advertising by The Church Bulletin Inc. of West Babylon (#169), which posts nothing online. The November 15th, 2026 issue (`http://stannebrentwood.org/images/bulletins/2026/AnneBrent11-15r.pdf`, read 2026-11-13) has the page 1 masthead "St. Anne's R.C. Church" and one Mass schedule: weekdays 12:00 noon (English) and 5:00pm (Spanish, Thursday English with 7:00pm Spanish), Wednesday 7:00pm French Creole in the Chapel, Saturday 9:00am; Saturday 5:00pm and 7:00pm (Spanish); Sunday 7:30am, 9:00am (Spanish), 11:00am, 12:30pm (French Creole), 3:00pm (Spanish), 5:00pm and 6:00pm (Spanish). This matches the diocese's Mass-times page.

## Worship sites

One: the church at 88 Second Avenue (`st-anne-brentwood-church`); the Chapel used for the Wednesday Creole Mass is part of the parish, with no other address given. The diocesan locator (directory:97), GCatholic (16816) and the Mass-times page list only this building. St. Anne's Gardens, 80 2nd Avenue, named in the bulletin, is a lunch program site, not a worship site.

## Website and bulletin provider

stannebrentwood.org is a Joomla site whose `/index.php/bulletins` page links the issues as `/images/bulletins/2026/AnneBrent<m>-<d>R.pdf`, so the row is `other` pinned to `page-pdfs` on that page. fetch:check on 2026-11-13 picked `AnneBrent11-15r.pdf` and dated it 2026-11-15, the current issue. The filenames carry no year; the year comes from the `/2026/` folder.

## Not yet confirmed

Nothing about the parish or church. In January 2027 check that fetch still dates the issues right when the folder changes to `/2027/`.
