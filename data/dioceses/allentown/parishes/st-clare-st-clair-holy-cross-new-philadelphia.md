---
name: St. Clare of Assisi, St. Clair and Holy Cross, New Philadelphia
website: https://stclareassisi.weebly.com/
bulletin_provider: other
provider_id: ''
publication: ['url:https://stclareassisi.weebly.com/2026_weekly-bulletin.html', 'po-org:st-clare-of-assisi-parish-17970',
  'lpi:001C000001CRr1pIAD', 'po-org:holy-cross-', 'lpi:0018000000QxAkZAAV']
group: ''
evidence:
- url: https://stclareassisi.weebly.com/uploads/5/6/4/5/56457441/137b_2026_10_11.pdf
  seen: 2026-10-18
  quote: The Parish Family of SAINT CLARE OF ASSISI PASTOR
  note: 'Page 1 masthead of the 11 October 2026 issue (the newest posted on 18 October): Rev. Msgr. William
    F. Glosser, V.F., pastor; 250 E. Hancock Street, Saint Clair.'
- url: https://stclareassisi.weebly.com/uploads/5/6/4/5/56457441/137b_2026_10_11.pdf
  seen: 2026-10-18
  quote: 'Saturdays: 4:00 PM @ St. Clare 5:30 PM @ Holy Cross Sundays: 8:30 AM @ St. Clare 10:45 AM @
    Holy Cross'
  note: 'Page 1 "MASS TIMES": also Tuesdays 6:00 PM and Wednesdays 8:30AM @ Holy Cross, Thursdays and
    Fridays 8:00 AM @ St. Clare. No other church is named.'
- url: https://stclareassisi.weebly.com/2026_weekly-bulletin.html
  seen: 2026-10-18
  note: The "2026_Weekly Bulletin" page lists one PDF per Sunday, 137b_2026_MM_DD.pdf, newest 11 October
    2026 (probe url). Earlier years are on 2025_weekly-bulletin.html and 2024_weekly-bulletin.html.
- url: https://www.allentowndiocese.org/places/holy-cross
  seen: 2026-10-18
  quote: 'Pastor: | Rev. Msgr. William F. Glosser, V.F.'
  note: 'Holy Cross''s own map page: the same pastor as St. Clare (whose page also names Msgr. Glosser);
    website "https://parishesonline.com/organization/holy-cross-".'
- url: https://parishesonline.com/organization/holy-cross-
  seen: 2026-10-18
  note: 'probe po: Holy Cross''s ParishesOnline org (lpi 0018000000QxAkZAAV, 99 Valley Street) has no
    publications; the website it gives, theholycrosschurch.com, does not resolve (probe url DEAD-DNS).
    St. Clare''s own org, st-clare-of-assisi-parish-17970 (lpi 001C000001CRr1pIAD), has no publications
    either.'
revisit: 'Run the fetch check again: the resolver should move from 2026_weekly-bulletin.html to the 2027
  page; if it does not, pin a recipe for the 2027 page.'
revisit_after: 2027-01-17
promoted: 2026-10-19
---

## Publisher

St. Clare of Assisi, St. Clair, publishes a weekly bulletin on its Weebly site. Holy Cross,
New Philadelphia, shares the same pastor (Msgr. William F. Glosser on both diocesan map
pages) and appears only in that bulletin. I read the 11 October 2026 issue, the newest
posted on 18 October. Its page-1 masthead is "The Parish Family of SAINT CLARE OF ASSISI",
and its "MASS TIMES" box covers both churches: Saturdays 4:00 PM @ St. Clare and 5:30 PM @
Holy Cross; Sundays 8:30 AM @ St. Clare and 10:45 AM @ Holy Cross; weekdays at one or the
other. Holy Cross has no channel of its own. The diocese's map points it to a ParishesOnline
org with no publications, and that org's website, theholycrosschurch.com, doesn't resolve.
So one bulletin, one row, two churches. A Google result for an allentowndiocese.org page
titled "St. Clare of Assisi, St. Clair and Holy Cross, New Philadelphia" (node/1147, now
404) suggests the diocese has paired them before. The row's name follows it.

St. Stephen, Port Carbon was merged into St. Clare in 2020 (`excluded/st-stephen-port-carbon`).

## Worship sites

- St. Clare of Assisi, 250 E. Hancock St., St. Clair (`st-clare-st-clair`).
- Holy Cross, Valley St., New Philadelphia (`holy-cross-new-philadelphia`).

Ruled out: St. Stephen, Port Carbon (GCatholic): merged into St. Clare in 2020 and later sold
(`excluded/st-stephen-port-carbon`). The Ruthenian St. Mary and the Ukrainian St. Nicholas
in St. Clair are Eastern Catholic (`other-jurisdiction`). ParishesOnline's church search also
shows an old "Immaculate Conception Church, Caroline Ave Diener's Hill, Saint Clair" account
with no publications. No roster lists it and the bulletin doesn't mention it, so it has no
record.

## Website and bulletin provider

`other`: the bulletin is self-hosted on stclareassisi.weebly.com, and the homepage links a
yearly page, "2026_Weekly Bulletin" (`2026_weekly-bulletin.html`), which lists one PDF per
Sunday (`/uploads/5/6/4/5/56457441/137b_2026_10_11.pdf`). The website is the homepage, not
the yearly page, because that page's name changes every January. Issues go up about a week
late: on Sunday 18 October the newest was 11 October. Pages 2 and 3 of the PDFs use an
embedded font that extracts as glyph codes (`/0 /1 /2`), so only pages 1 and 4–6 read as
text. The publication ids include both parishes' empty ParishesOnline orgs so that no other
row claims them.

Fetch check (2026-10-18, `fetch_check_rows.py`): from the homepage, the resolver chose
the 2026 yearly page and picked `137b_2026_10_11.pdf` ("page-pdfs on
.../2026_weekly-bulletin.html: first-listed", recipe `page-pdfs
https://stclareassisi.weebly.com/2026_weekly-bulletin.html`). That is the newest issue
posted (18 October wasn't up yet), so the pick is right. The resolver gave it no date.
`provider_id` is left empty on purpose: the printed recipe names the 2026 page and would
stop finding new issues in January 2027. Without it, the resolver finds the current year's
page from the homepage.

## Not yet confirmed

Whether the resolver moves to `2027_weekly-bulletin.html` once St. Clare starts it in
January (see `revisit`).
