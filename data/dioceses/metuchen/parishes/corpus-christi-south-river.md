---
name: Corpus Christi
website: https://corpuschristisouthriver.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://corpuschristisouthriver.org/bulletins#corpus-christi-south-river']
group: ''
evidence:
- url: https://corpuschristisouthriver.org/bulletins/file/2026-10-25-en.pdf
  seen: 2026-10-30
  quote: Daily Mass – Mon., Thurs. & Fri. - 7:00 a.m.
  note: Page 1 of the 25 October 2026 English bulletin, published by Corpus Christi on its own site. It
    lists Corpus Christi's Masses and no other South River parish's.
- url: https://corpuschristisouthriver.org/bulletins/file/2026-10-25-en.pdf
  seen: 2026-10-30
  quote: Please remember Corpus Christi Parish
  note: Page 1, same issue. Pages 2 and 3 carry Corpus Christi's own giving, religious education and parish
    notices.
- url: https://corpuschristisouthriver.org/mass
  seen: 2026-10-30
  quote: Sunday Portuguese 11:30 am
  note: 'Parish Mass page: English and Portuguese Sunday and weekday Masses at 100 James St.'
revisit: 'Check whether fetch can read the site: the bulletin page links HTML viewer pages (bulletin-view?f=<date>-en.pdf),
  and the PDF is at /bulletins/file/<date>-en.pdf'
revisit_after: 2027-01-15
research:
- method: fetch:check with the guessed recipe, then pinned page-pdfs (filename=*-en.pdf), linked-issue-page,
    dated-post and redirected-pdf on /bulletins
  url: https://corpuschristisouthriver.org/bulletins
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: Add a collector that follows bulletin-view?f=<name> to /bulletins/file/<name>, or pin a
    recipe once one exists; then run fetch:check and set provider to other
  retry_when: The resolver learns viewer-wrapped PDFs, or the site links /bulletins/file/*.pdf directly
bulletin_status: unsupported-format
publication_reviews:
- parish: st-mary-of-ostrabrama-south-river
  decision: separate
  evidence:
  - url: https://corpuschristisouthriver.org/bulletins/file/2026-10-25-en.pdf
    seen: 2026-10-30
    quote: Please remember Corpus Christi Parish
    note: Bulletin for Corpus Christi, published by Corpus Christi on corpuschristisouthriver.org (25
      October 2026, 3 pages); it carries its own Mass intentions and notices.
  - url: https://files.ecatholic.com/11802/bulletins/20261025.pdf
    seen: 2026-10-30
    quote: Saint Mary of Ostrabrama Parish, a Roman Catholic
    note: Bulletin for St. Mary of Ostrabrama, published by that parish through eCatholic 11802 (25 October
      2026, 6 pages), with its own Mass schedule.
- parish: st-stephen-protomartyr-south-river
  decision: separate
  evidence:
  - url: https://corpuschristisouthriver.org/bulletins/file/2026-10-25-en.pdf
    seen: 2026-10-30
    quote: Please remember Corpus Christi Parish
    note: Bulletin for Corpus Christi, published by Corpus Christi on corpuschristisouthriver.org (25
      October 2026, 3 pages); it carries its own Mass intentions and notices.
  - url: https://ststephennj.com/?page_id=17
    seen: 2026-10-30
    quote: Saint Stephen Protomartyr Catholic Church
    note: Bulletin page for St. Stephen Protomartyr, published by that parish on ststephennj.com, with
      its own services for 26 October to 1 November 2026.
---

## Publisher

Corpus Christi publishes its own bulletin on its own website, corpuschristisouthriver.org. The page `/bulletins` (read 2026-10-30) lists every Sunday since 2019, each with an English and a Portuguese edition ("Every bulletin since 2019"). The newest English issue is 25 October 2026; a Portuguese 1 November 2026 edition was already up on 30 October. The viewer page `/bulletin-view?f=2026-10-25-en.pdf` is HTML and embeds the PDF, which is served at `/bulletins/file/2026-10-25-en.pdf`.

The bulletin's text names Corpus Christi Parish and gives its Mass intentions, giving and religious-education notices (3 pages). It does not name St. Mary of Ostrabrama or St. Stephen Protomartyr, so it is not shared with either (see their records).

## Worship sites

The church at 100 James St is the parish's main site (directory:24546, gcatholic:18597). The parish's Traditional Latin Mass on Wednesday 6:15 pm and First Friday 7:00 pm is held in the St. Mark's Christian Academy conference room (former convent), corner of David and Kamm Ave, not in the church; see `open/` for that place. First Saturday and Holy Day Latin Masses are in the church.

## Website and bulletin provider

Self-hosted site (Website by Immaculate Motherhood LLC). The bulletin is a real PDF, English and Portuguese editions, but the site links only HTML viewer pages (`/bulletin-view?f=2026-10-25-en.pdf`). `fetch:check` 2026-10-30 guessed `page-pdfs` and picked `bulletin-view?f=2026-11-01-pt.pdf` (the Portuguese edition, HTML: `not_pdf`). Pinning `page-pdfs … filename=*-en.pdf`, `linked-issue-page`, `dated-post` and `redirected-pdf` on `/bulletins` all failed with "No PDF links". So the row is `no_bulletin` for now (Settled policy 4) with the bulletin itself confirmed readable by hand; the PDF address pattern is `/bulletins/file/<yyyy-mm-dd>-en.pdf`.

## Not yet confirmed

Nothing outstanding on identity. The finder lists Rev. Damian B. Breen as pastor; the bulletin pages read do not name a pastor.
