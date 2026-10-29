---
name: Our Lady of the Rosary Catholic Church
website: https://www.olrcc.org
bulletin_provider: ecatholic
provider_id: '30876'
publication: ['ecatholic:30876', 'url:https://www.church-bulletin.org/our-lady-of-the-rosary-catholic-church-coatesville-pa-19320']
group: ''
evidence:
- url: https://files.ecatholic.com/30876/bulletins/20261025.pdf
  seen: 2026-10-28
  note: 'The 25 October 2026 issue (6 pages; page 1 an image, rendered and read; page 2 text): masthead
    ''Our Lady of the Rosary Catholic Church'', Rev. Daniel Gnangba, FM, 80 South 17th Avenue, Coatesville,
    PA 19320, www.olrcc.org, Thirtieth Sunday in Ordinary Time; Mass Times: Saturday Vigil 5:00 PM; Sunday
    8:30 AM, 10:30 AM, 6:00 PM; Mon & Wed 6:00 PM; Tues, Thurs, Fri & Saturday 8:00 AM. Names the parish
    alone; no other site. Page 2 is headed ''This Week at Our Lady of the Rosary Church''.'
- url: https://www.olrcc.org/bulletins
  seen: 2026-10-28
  quote: '20261101'
  note: 'The parish''s own eCatholic Bulletins page (site 30876): newest linked file files.ecatholic.com/30876/bulletins/20261101.pdf
    (1 November, posted ahead), then 20261025 and 20261018.'
- url: https://www.church-bulletin.org/bulletin/our-lady-of-the-rosary-catholic-church-coatesville-pa-19320/2026-10-25.pdf
  seen: 2026-10-28
  note: 'John Patrick Publishing listing id 206, ''Our Lady of the Rosary Catholic Church'', Coatesville,
    PA 19320, latest October 25, 2026 (image only; page 1 rendered): identical cover and Mass Times to
    the eCatholic 25 October file. Not byte-identical (4,846,120 vs 1,506,362 bytes), same page 1 content;
    recorded as a second publication id.'
promoted: 2026-10-29
publication_reviews:
- parish: st-joseph-coatesville
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/30876/bulletins/20261025.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, an image, rendered) names Our Lady of the Rosary Catholic
      Church alone, 80 South 17th Avenue, with its own Mass Times.
  - url: https://files.ecatholic.com/37050/bulletins/20261025.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead names St. Joseph Parish alone, 404 Charles St., with its own Mass
      Schedule. Same Parochial Administrator, different bulletin.
---

## Publisher

Our Lady of the Rosary, Coatesville, publishes through eCatholic (site 30876): its own `/bulletins` page lists dated PDFs, the newest 1 November 2026 (posted before the date) and 25 October 2026 behind it. John Patrick Publishing's listing 206 (the survey's lead) carries the 25 October issue with the same page 1; the files differ byte for byte, so the listing is a second publication id. The eCatholic archive is at least as current as the listing, so it is the channel.

The directory names Rev. Komlan D. Gnangba, F.M. as pastor of this parish and St. Joseph; the bulletins are separate (see `publication_reviews`).

## Worship sites

One: the church at 80 S. 17th Ave. The directory calls St. Cecilia (6th and Chestnut Sts.) a worship site of this parish, but the 25 October 2026 bulletin's Mass Times lists only the parish church, the church was relegated to profane use effective 16 September 2016, and no bulletin read lists Mass there (see `excluded/st-cecilia-coatesville`). Directory times (Saturday 5 PM, Sunday 8:30 and 10:45 AM) differ from the bulletin (Sunday 10:30 AM and 6:00 PM); the bulletin wins.

## Website and bulletin provider

`www.olrcc.org` is eCatholic-hosted (`probe url`: ecatholic:30876, links /bulletins); files are under `/bulletins/`. Page 1 of each issue is an image, so the pipeline will read it as an image.

## Not yet confirmed

`fetch:check` (2026-10-28) picks the eCatholic file 20261101.pdf, posted four days before its date, and reports freshness `future` (issue date inferred from the file name; page 1 is an image). The parish posts a week ahead of the John Patrick listing, whose newest is 25 October (fresh). If the pipeline rejects future-dated issues, switch this row to `other` with `page-pdfs https://www.church-bulletin.org/our-lady-of-the-rosary-catholic-church-coatesville-pa-19320`; its ecatholic id and the listing id are already both recorded in `publication`.
