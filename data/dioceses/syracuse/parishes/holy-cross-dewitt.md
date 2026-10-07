---
name: Holy Cross Church
website: https://www.holycrossdewitt.org
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.holycrossdewitt.org/bulletins']
group: 'Fr. Kurgan: Holy Cross, St. Daniel, St. Anthony of Padua'
evidence:
- url: https://www.holycrossdewitt.org/s/2026-09-06-Holy-Cross-Bulletin.pdf
  seen: 2026-09-26
  quote: 4 112 EAST GENESEE STREET | DEWITT, NY 1 32 1 4
  note: Masthead, page 1 of the 6 September 2026 issue (the newest on the bulletins page on 2026-09-26).
    The PDF's text layer splits digits ("4 112" = 4112).
- url: https://www.holycrossdewitt.org/s/2026-09-06-Holy-Cross-Bulletin.pdf
  seen: 2026-09-26
  quote: WEEKLY MASS SCHEDULE Weekdays 7:45 am Saturdays 9:00 am 4:00 pm vigil Sundays 7:30 am 10:30 am
    5:00 pm
  note: Page 5. Every Mass in the week's calendar is at "Church", i.e. Holy Cross.
- url: https://www.holycrossdewitt.org/s/2026-08-16-Holy-Cross-Bulletin.pdf
  seen: 2026-09-26
  quote: There will be a Holy Hour at St. Mary’s Church in James- ville
  note: The parish's St. Mary's Oratory in Jamesville appears in the bulletin only for occasional services.
- url: https://www.holycrossdewitt.org/bulletins
  seen: 2026-09-26
  note: The parish's bulletin page, weekly PDFs named <date>-Holy-Cross-Bulletin.pdf back to at least
    31 May 2026 (visit.py --bulletin).
revisit: Check holycrossdewitt.org/bulletins has issues after 6 September 2026.
revisit_after: 2026-10-20
promoted: 2026-09-26
---

## Publisher

Holy Cross publishes its own weekly bulletin on its Squarespace site. I read the 6
September 2026 issue, the newest on the bulletins page on 2026-09-26 (no 13 or 20
September file exists at the same naming pattern, so it may post irregularly): the page-1
masthead is Holy Cross alone, 4112 East Genesee Street, DeWitt, and the page-5 weekly Mass
schedule (weekdays 7:45 am; Saturday 9 am and 4 pm vigil; Sunday 7:30, 10:30 am and 5 pm)
is all at the church.

Rev. John Kurgan is also pastor of St. Daniel and administrator of St. Anthony of Padua
(diocese page for St. Mary's Oratory, 2026-09-26), and St. Anthony's bulletin gives its
office as "Located @ Holy Cross Church". Both publish their own bulletins (ParishesOnline
06/0145 and a self-hosted PDF), so they are separate rows in the same `group`.

## Worship sites

One: Holy Cross itself (`holy-cross-dewitt`). St. Mary's Oratory, 6443 East Seneca
Turnpike, Jamesville, has its office and sacramental records at Holy Cross (diocese page)
and is used for Holy Hours; its last Mass found was 9 October 2025, so on 2026-10-07 it was
moved to `open/st-marys-oratory-jamesville` (see that file).

## Website and bulletin provider

holycrossdewitt.org's "Bulletins" page lists the PDFs; provider `other`, publication
`url:` of that page. No ParishesOnline, eCatholic or Discover Mass id was found on the site.

## Not yet confirmed

Whether the gap after 6 September is a posting lag or a change of schedule; check the
bulletins page again in October.
