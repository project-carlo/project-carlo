---
name: St. Mark's Catholic Church
website: https://stmarkseagirt.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-mark-s-catholic-church-sea-girt-nj-08750
publication: ['url:https://www.church-bulletin.org/saint-mark-s-catholic-church-sea-girt-nj-08750']
group: Cohort 29 (Spring Lake, Sea Girt, Manasquan)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-mark-s-catholic-church-sea-girt-nj-08750/2026-11-01.pdf
  seen: 2026-10-30
  note: '16-page issue dated 1 November 2026 (All Saints Day), image-only (probe pdf: no extractable text),
    so pages 1-2 were read from renders. Page 1 masthead: "St. Mark''s Catholic Church, Fr. Miguel Virella,
    SVD, Pastor, Dr. Joseph V. Stillo, Deacon, Michael Keary, Deacon"; Weekend Masses Saturday 4:30 PM,
    Sunday 8 AM, 10 AM and 12 Noon, 5PM in Spanish; Daily Masses Monday-Friday 7:30 AM and 11 AM, Saturday
    7:30 AM only; footer ''215 Crescent Pkwy, Sea Girt, NJ 08750 - Phone 732-449-6364 - www.stmarkseagirt.com''.
    It names St. Mark alone.'
- url: https://www.church-bulletin.org/saint-mark-s-catholic-church-sea-girt-nj-08750
  seen: 2026-10-30
  note: John Patrick Publishing listing 613 ('Saint Mark's Catholic Church, Sea Girt, NJ 08750'); latest
    edition 1 November 2026, with the 2026-10-25 issue below it.
- url: https://stmarkseagirt.com/
  seen: 2026-10-30
  note: The parish's homepage (read with the browser; probe url answers 403) links https://church-bulletin.org/?id=613
    as its bulletin and https://stmarkseagirt.com/whats-happening/mass-schedule; no second channel.
promoted: 2026-10-30
research:
- method: pnpm fetch:check --diocese trenton --parish st-mark-sea-girt (headed Chrome); page-pdfs on the
    John Patrick listing
  url: https://www.church-bulletin.org/saint-mark-s-catholic-church-sea-girt-nj-08750
  checked: '2026-10-30'
  outcome: found
  next_action: 'None; transport ok, document_type pdf, picks the current issue (freshness future: the
    coming Sunday issue, posted early)'
bulletin_status: available
---

## Publisher

St. Mark's Catholic Church, Sea Girt publishes its own weekly bulletin through John Patrick Publishing (listing 613). The 1 November 2026 issue is image-only; its rendered page 1 names Fr. Miguel Virella, SVD as pastor with two deacons and gives the Mass schedule of one church. It does not mention St. Catharine-St. Margaret or St. Denis (the other Cohort 29 parishes), whose bulletins have different mastheads and pastors, so it is a single-parish row.

## Worship sites

One church, 215 Crescent Parkway (see `st-mark-sea-girt`). The Mass schedule on page 1 lists weekend and daily Masses without naming another building.

## Website and bulletin provider

stmarkseagirt.com blocks `probe url` (403) but loads in the browser; its homepage links the John Patrick listing as the bulletin, so the row is `other` with `page-pdfs` on the listing.

## Not yet confirmed

Nothing outstanding.
