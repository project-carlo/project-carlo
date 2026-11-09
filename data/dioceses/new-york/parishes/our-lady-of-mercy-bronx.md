---
name: Our Lady of Mercy, Bronx
website: https://ourladyofmercyny.org/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://ourladyofmercyny.org/bulletin/
publication: ['url:https://ourladyofmercyny.org/bulletin/']
group: Our Lady of Mercy, Bronx
evidence:
- url: https://ourladyofmercyny.org/wp-content/uploads/sites/109/2026/09/sept27_2026_olmercyny_compressed.pdf
  seen: 2026-10-07
  quote: Our Lady of Mercy
  note: Latest linked issue inspected October 7, 2026; masthead visually read on rendered page 1 where
    the text layer omits it.
- url: https://ourladyofmercyny.org/wp-content/uploads/sites/109/2026/09/sept27_2026_olmercyny_compressed.pdf
  seen: 2026-10-07
  quote: |-
    SUNDAY
    9:30 am  English

    11:00 am  Spanish

    1:00 pm  Spanish
  note: Printed recurring Sunday timetable in the saved actual issue text; it has no closure meaning.
promoted: 2026-10-08
research:
- method: fetch:check on 2026-11-08 and 2026-11-09; the parish homepage read in Chrome (visit.py --links)
    for another bulletin link; web search of discovermass.com, parishesonline.com, church-bulletin.org
    and bonventure.net for the parish; ParishesOnline org our-lady-of-mercy-church-10458 has no issues
  url: https://ourladyofmercyny.org/bulletin/
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-run fetch:check; the parish's own archive lags (newest September 27, 2026 on 2026-11-09)
    and no other current channel was found. If it stays over two weeks behind, look again for a publisher
    listing (church-bulletin.org, ParishesOnline).
  retry_when: The archive posts an issue dated after September 27, 2026
  revisit_after: 2026-11-16
---

## Publisher

The September 27, 2026 image masthead identifies Our Lady of Mercy, 2496 Marion Avenue. The printed recurring Sunday timetable gives 9:30 am English, 11:00 am Spanish and 1:00 pm Spanish; these are ordinary weekly Masses, not a final/closing Mass.

## Worship sites

Our Lady of Mercy alone is identified; Saturday 6 pm, Sunday 9:30 am English/11 am Spanish/1 pm Spanish.

## Website and bulletin provider

The parish bulletin page was inspected October 7, 2026. Publication identifiers come from the actual linked bulletin channel, not unrelated links or a historical parish merger. Saved actual rendered HTML and a live headed-browser resolver check both select the inspected September 27 PDF with the pinned page-pdfs recipe. The current listing returns an HTTP URL; the equivalent HTTPS URL was downloaded and read. Resolver results are in scratch/bronx1-resolver-check.json and scratch/bronx1-live-resolver-check.json; full production downloading remains separate.

## Not yet confirmed

Run fetch:check for the page-pdfs collector and look for a newer October bulletin.
