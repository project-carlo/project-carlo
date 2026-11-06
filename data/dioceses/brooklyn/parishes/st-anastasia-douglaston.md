---
name: St. Anastasia (Douglaston)
website: https://sta.nyc/
bulletin_provider: other
provider_id: redirected-pdf https://sta.nyc/bulletin
publication: []
group: Deanery Q5 (Queens East)
evidence:
- url: https://sta.nyc/files/bulletin.pdf
  seen: 2026-11-06
  quote: Solemnity of All Saints
  note: 'The 1 November 2026 issue (7 pages, created 28 Oct 2026), page 1 masthead: ''Good News! Saint
    Anastasia Church, Douglaston/Little Neck, New York'', 45-14 245th St. (Rev. John J. Gribbon Way),
    Douglaston, NY 11362-1135, www.sta.nyc. Weekend Masses: 5:00 p.m. Vigil on Saturday; Sunday 8:00 AM,
    10:00 AM and 12 noon; weekdays Monday thru Saturday 8:30 AM.'
- url: https://sta.nyc/
  seen: 2026-11-06
  note: 'probe url: WordPress site ''Saint Anastasia Church'', bulletin link https://sta.nyc/bulletin,
    which redirects to the fixed file https://sta.nyc/files/bulletin.pdf (overwritten each week). No ParishesOnline,
    eCatholic or Discover Mass ids embedded.'
revisit: Confirm sta.nyc/files/bulletin.pdf has moved on to the 8 November 2026 issue (fixed file name,
  so fetch:check reports freshness unknown)
revisit_after: 2026-11-10
---

## Publisher

St. Anastasia publishes its own bulletin, laid out in-house (PDF metadata: Affinity, author Ralph Iskaros), as one fixed file `https://sta.nyc/files/bulletin.pdf` that the site's /bulletin link redirects to. The issue read on 2026-11-06 is dated "Solemnity of All Saints … November 1, 2026"; page 1 reads "Saint Anastasia Church, Douglaston/Little Neck, New York", 45-14 245th St., Douglaston, NY 11362-1135. No publisher footer or LPi container number appears.

## Worship sites

One church. Page 1's Liturgies box gives Saturday 5:00 p.m. Vigil, Sunday 8:00 AM, 10:00 AM and 12 noon, and Monday thru Saturday 8:30 AM, with confession "Saturdays from 4:00 - 4:30 PM in the Church"; no other building is named. The diocese directory, the deanery list (Q5), GCatholic 16674 and Mass finder 1196 list only this church.

## Website and bulletin provider

`other`, recipe `redirected-pdf https://sta.nyc/bulletin`. The directory's homepage https://www.sta.nyc/ redirects to sta.nyc (WordPress). GCatholic's website (stanastasia.info) is an older domain. `fetch:check` on 2026-11-06 resolved the homepage's /bulletin link to the redirected file and downloaded `https://sta.nyc/files/bulletin.pdf`, which was the 1 November 2026 issue (the latest Sunday); it reports the issue date unknown because the file name carries none.

## Not yet confirmed

That the fixed file is replaced every week: on 2026-11-06 (a Friday) it was still the 1 November issue, as expected before the weekend. Recheck after 8 November (revisit).
