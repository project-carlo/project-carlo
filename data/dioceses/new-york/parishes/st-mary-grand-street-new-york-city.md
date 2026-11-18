---
name: St. Mary (Grand Street)
website: https://www.saintmarygrand.org/
bulletin_provider: other
provider_id: dated-post https://www.saintmarygrand.org/category/bulletins/
publication: ['url:https://www.saintmarygrand.org/category/bulletins/']
group: ''
evidence:
- url: https://www.saintmarygrand.org/wp-content/uploads/2026/10/10.11.26-Saint-Mary-bulletin.pdf
  seen: 2026-11-08
  quote: 'MASS SCHEDULE October 10 - 17, 2026 SATURDAY: 5 P.M.'
  note: Page 1 of the two-page 11 October 2026 issue; masthead '10.11.26 28TH SUNDAY IN ORDINARY TIME',
    'First Church in NYC Dedicated to Mary', saintmarygrand.org, (212) 674-3266. Sunday 9 A.M. and 11
    A.M. follow.
- url: https://www.saintmarygrand.org/category/bulletins/
  seen: 2026-11-08
  quote: 10.11.26 Bulletin
  note: Newest post in the Bulletins category on 2026-11-08, above 10.4.26, 9.27.26, 9.20.26 and 9.13.26;
    on 2026-10-08 the newest was 8.23.26, so these five were posted together after October 8.
- url: https://www.saintmarygrand.org/
  seen: 2026-10-08
  quote: |-
    Church address:
    440 Grand Street
    New York, NY 10002

    Parish Office address:
    213 Stanton St.
  note: Homepage separates the church (440 Grand Street) from the office (213 Stanton Street).
revisit: Check that the bulletin category has caught up past the 11 October 2026 issue (it posts in batches);
  if it stays more than a month behind, consider no_bulletin.
revisit_after: 2026-11-29
promoted: 2026-11-09
research:
- method: check_fetch on a hypothetical row (provider other, no recipe) and fetch:check on the written
    row
  url: https://www.saintmarygrand.org/category/bulletins/
  checked: '2026-11-08'
  outcome: found
bulletin_status: available
---

## Publisher

St. Mary on Grand Street publishes its own two-page weekly bulletin as a WordPress post per issue in the Bulletins category of https://www.saintmarygrand.org/, each with a PDF (`wp-content/uploads/2026/10/10.11.26-Saint-Mary-bulletin.pdf`). The 11 October 2026 issue, read November 8, is headed "10.11.26 28th Sunday in Ordinary Time" and "First Church in NYC Dedicated to Mary", with saintmarygrand.org and (212) 674-3266, and prints the "Mass Schedule October 10 - 17, 2026". No other church appears.

## Worship sites

One: St. Mary, 440 Grand Street (`churches/st-mary-grand-street-new-york-city.md`). The 11 October issue gives Saturday 5 P.M. and Sunday 9 A.M. and 11 A.M. with intentions, and says the church is now open daily 8:15 a.m. to 3 p.m. The homepage (October 8) separates the church at 440 Grand Street from the parish office at 213 Stanton Street. This is the Latin parish, not the Ruthenian St. Mary on East 15th Street.

## Website and bulletin provider

The recipe `dated-post https://www.saintmarygrand.org/category/bulletins/` picked the 11 October issue on November 8, the newest one posted. The archive lags and is filled in batches: on October 8 it ended at August 23 and its embedded archive document said "Contact the rectory for the latest"; by November 8 the September 13 to October 11 issues had been added. So the pick is the newest issue the parish has posted, not this week's; the row goes live on that basis.

## Not yet confirmed

Whether the archive keeps catching up (see revisit). The weekday schedule in the 11 October issue was not separately read; the homepage on October 8 gave daily 9 AM bilingual.
