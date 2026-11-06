---
name: Our Lady of the Snows (Floral Park)
website: https://olsnows.org/
bulletin_provider: other
provider_id: page-pdfs https://olsnows.org/bulletin/
publication: []
group: Deanery Q5 (Queens East)
evidence:
- url: https://olsnows.org/wp-content/uploads/sites/7/2026/10/11-1-26-1.pdf
  seen: 2026-11-06
  quote: We the people of Our Lady of the Snows
  note: '1 November 2026 issue (14 pages, Microsoft Publisher; ''MASS INTENTIONS FOR THE WEEK, SUNDAY,
    NOVEMBER 1, 2026''). Page 1 is the parish''s staff and schedule page (Pastor Rev. Fred Marano): Masses
    Saturday 5:00 PM; Sunday 8:00 AM, 9:30 AM, 11:00 AM, 12:30 PM and 5:30 PM Mass in Malayalam; Weekdays
    9:00 AM and 12:00 Noon; Saturday Mornings 9:00 AM. No publisher footer.'
- url: https://olsnows.org/bulletin/
  seen: 2026-11-06
  note: 'probe url: UNREACHABLE (RemoteDisconnected); visit.py loads it. WordPress multisite (uploads
    under /wp-content/uploads/sites/7/). The Bulletin page lists flyers and weekly bulletins together:
    11-1-26-1.pdf, FIL-AM-Mission.pdf, YM-NOVEMBER-1.pdf, FORMED-11-1-26.pdf ..., October-25-2026.pdf,
    October-18-2026.pdf, 10-11-26-1.pdf, October-4-2026.pdf, September-27-2026.pdf.'
revisit: Check fetch still picks the weekly bulletin and not a dated flyer (e.g. FORMED-11-1-26.pdf) from
  the mixed /bulletin/ page; bulletin file names vary (11-1-26-1.pdf vs October-25-2026.pdf), so no filename
  filter is pinned
revisit_after: 2026-12-01
---

## Publisher

Our Lady of the Snows publishes its own weekly bulletin (Microsoft Publisher, no publisher footer) on its parish site. The 1 November 2026 issue (`11-1-26-1.pdf`, 14 pages, read 2026-11-06) opens with the parish's mission statement ("We the people of Our Lady of the Snows Parish…"), staff (Pastor Rev. Fred Marano) and schedule, and its intentions page is headed "SUNDAY, NOVEMBER 1, 2026". The page-1 photo panel is captioned "Our Lady of the Snows Church" (rendered image).

## Worship sites

One church. Page 1 gives Saturday 5:00 PM; Sunday 8:00 AM, 9:30 AM, 11:00 AM, 12:30 PM and 5:30 PM Mass in Malayalam ("Latin Rite Catholic Mass in Malayalam: Each Sunday at 5:30 PM in Church"); weekdays 9:00 AM and 12:00 Noon; Saturday mornings 9:00 AM. No other building is named. The diocese directory, deanery list (Q5), GCatholic 16647 and Mass finder 1141 list only this church.

## Website and bulletin provider

`other`, recipe `page-pdfs https://olsnows.org/bulletin/`. olsnows.org is on the same WordPress multisite as olschurch-corona.org (uploads under `/wp-content/uploads/sites/7/`): `probe url` gets RemoteDisconnected, but visit.py, `tools/fetch-pdf.py` and `fetch` load it. `fetch:check` on 2026-11-06 picked `11-1-26-1.pdf`, the 1 November 2026 issue, freshness `fresh`.

## Not yet confirmed

The /bulletin/ page mixes flyers with the bulletins, and the bulletin file names vary (`11-1-26-1.pdf`, `October-25-2026.pdf`), so no filename filter is pinned. A dated flyer (`FORMED-11-1-26.pdf`) could be picked in a later week; recheck the pick on the revisit date.
