---
name: St. John the Baptist Parish
website: https://www.stjohnromancatholic.org/sjrc/
bulletin_provider: other
provider_id: page-pdfs https://www.stjohnromancatholic.org/sjrc/News%20%26%20Bulletins
publication: ['url:https://www.stjohnromancatholic.org/sjrc/News%20%26%20Bulletins#st-john-the-baptist-allentown']
group: Cohort 27 (Yardville, Allentown; linkage delayed)
evidence:
- url: https://www.stjohnromancatholic.org/sjrc/News%20%26%20Bulletins/October%2025%2C%202026%20Bulletin.pdf
  seen: 2026-10-30
  quote: Very Rev. Michael Wallack, Pastor
  note: '20-page issue of 25 October 2026 (text layer). Page 1-2: ''Saint John the Baptist Roman Catholic
    Church, 1282 Yardville-Allentown Road, Allentown, N.J. 08501''; pastor Very Rev. Michael Wallack,
    deacons Paul DeGrazia, Joseph Hepp, Michael Scannella; ''Holy Mass Schedule and Intentions'': Sunday
    9:00 AM, 11:00 AM, 12:30 PM; weekdays 7:00 PM Monday, 8:00 AM Tuesday-Friday, 7:00 PM Wednesday; Saturday
    8:00 AM and 5:15 PM. No mention of St. Vincent de Paul (grep over all 20 pages).'
- url: https://www.stjohnromancatholic.org/sjrc/News%20%26%20Bulletins
  seen: 2026-10-30
  quote: News & Bulletins
  note: The parish's own News & Bulletins page, dated PDFs ('October 25, 2026 Bulletin.pdf' newest, back
    to 26 July 2026 on the homepage); 1 November 2026's PDF is not posted yet (the filename answers an
    HTML page).
- url: https://www.church-bulletin.org/saint-john-the-baptist-allentown-nj-08501
  seen: 2026-10-30
  note: John Patrick listing 548 for the parish has no latest edition (dead or unused); the parish posts
    its own PDFs, so it is not the publisher.
research:
- method: pnpm fetch:check --diocese trenton --parish st-john-the-baptist-allentown-nj (headed Chrome);
    page-pdfs on https://www.stjohnromancatholic.org/sjrc/News%20%26%20Bulletins
  url: https://www.stjohnromancatholic.org/sjrc/News%20%26%20Bulletins
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: it picked the 25 October 2026 issue (fresh, 5 days old).'
bulletin_status: available
publication_reviews:
- parish: st-vincent-de-paul-yardville
  decision: separate
  evidence:
  - url: https://www.stjohnromancatholic.org/sjrc/News%20%26%20Bulletins/October%2025%2C%202026%20Bulletin.pdf
    seen: 2026-10-30
    note: The 25 October 2026 masthead names Saint John the Baptist Roman Catholic Church, Allentown alone
      (pastor Very Rev. Michael Wallack, 1282 Yardville-Allentown Road), with its own Holy Mass schedule.
  - url: https://www.church-bulletin.org/bulletin/saint-vincent-de-paul-parish-yardville-nj-08620/2026-10-25.pdf
    seen: 2026-10-30
    note: The 25 October 2026 masthead names St. Vincent de Paul Parish alone (pastor Rev. Stanley Krzyston,
      555 Yardville Allentown Road), with its own Mass times. (John Patrick 6044)
---

## Publisher

St. John the Baptist Roman Catholic Parish, Allentown (Cohort 27, "*linkage delayed", with St. Vincent de Paul, Yardville). It posts its own dated PDFs on its News & Bulletins page; the John Patrick listing 548 under its name is empty. The 25 October 2026 issue names the parish alone, with pastor Very Rev. Michael Wallack. The planned linkage with St. Vincent de Paul (2017 decisions: "no later than July 1, 2019") has not produced one pastor or one bulletin: St. Vincent's pastor is Rev. Stanley Krzyston.

## Worship sites

One church, 1282 Yardville-Allentown Road (the finder and GCatholic add "Ste 1"). The parish also keeps a cemetery (staff list), which is not a Mass site.

## Website and bulletin provider

Self-hosted PDFs under `/sjrc/News & Bulletins/`; the filename is the Sunday's date.
