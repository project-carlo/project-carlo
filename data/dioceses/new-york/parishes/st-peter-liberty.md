---
name: St. Peter
website: https://stpetersliberty.com/bulletins-1
bulletin_provider: other
provider_id: page-pdfs https://stpetersliberty.com/bulletins-1 filename=Bulletin?St?Peter*.pdf
publication: ['url:https://stpetersliberty.com/bulletins-1#st-peter']
group: St. Peter - St. Aloysius - Immaculate Conception
evidence:
- url: https://files.ecatholic.com/14200/documents/2026/10/Bulletin%20St%20Peter-4.pdf
  seen: 2026-10-31
  quote: Liberty, NY  12754
  note: The November 1, 2026 (All Saints) issue, newest St. Peter file on the archive. Page 1 masthead
    names St. Peter's Church, 262 North Main St., Liberty alone, with its own collection ($5351) and Liberty
    Mass intentions; its weekend schedule covers Woodbourne, Liberty, Livingston Manor and the Bethlehem
    monastery.
- url: https://stpetersliberty.com/bulletins-1
  seen: 2026-10-31
  note: 'Rendered in headed Chrome (probe url gets HTTP 403). Newest first: Bulletin St Peter-4.pdf, STALOYSIUS-4.pdf
    and the Immaculate Conception October 31/November 1 file, then the -3, -2, -1 and unsuffixed October
    sets. eCatholic site 14200 hosts all three publishers'' files under /documents/2026/10/.'
- url: https://files.ecatholic.com/14200/documents/2026/11/Bulletin%20St%20Peter.pdf
  seen: 2026-11-08
  note: November 8, 2026 issue, the newest for this publisher on the shared archive and the file fetch:check
    picked on 2026-11-08. The St. Peter bulletin, published for St. Peter's Church, 262 North Main St.,
    Liberty. The November 8, 2026 issue (read 2026-11-08) has that masthead, 'NOVEMBER 8, 2026', a $5764
    collection and Liberty weekday and Sunday intentions.
revisit: Re-run fetch:check after the next upload; if St. Peter's file stops being named Bulletin St Peter*.pdf,
  update the filename glob.
revisit_after: 2026-11-22
promoted: 2026-11-09
research:
- method: Headed-Chrome visit of the shared archive and probe pdf of the newest file per publisher
  url: https://stpetersliberty.com/bulletins-1
  checked: '2026-10-31'
  outcome: found
  next_action: Re-run fetch:check if the archive's file naming changes
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check with the pinned page-pdfs recipe
  url: https://stpetersliberty.com/bulletins-1
  checked: '2026-11-08'
  outcome: found
  next_action: Re-run fetch:check if a week picks the wrong file or none
bulletin_status: available
publication_reviews:
- parish: st-aloysius-livingston-manor
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/14200/documents/2026/10/STALOYSIUS-4.pdf
    seen: 2026-10-31
    note: The November 1, 2026 St. Aloysius masthead names St. Aloysius, 22 Church Street, Livingston
      Manor alone, with its own collection ($902) and its own page 2; the St. Peter issue of the same
      week names St. Peter's Church, Liberty, with a $5351 collection and different page 2 content.
- parish: immaculate-conception-woodbourne
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/14200/documents/2026/10/Church%20of%20the%20Immaculate%20Conception%20Bulletin%20October%2031%20%20November%201%202026.docx.pdf
    seen: 2026-10-31
    note: The October 31/November 1, 2026 Woodbourne masthead names Church of the Immaculate Conception,
      6317 State Route 42, Woodbourne alone, with its own Mass schedule, collection ($1,502) and announcements;
      the St. Peter issue of the same week names St. Peter's Church, Liberty.
---

## Publisher

The St. Peter bulletin, published for St. Peter's Church, 262 North Main St., Liberty. The November 8, 2026 issue (read 2026-11-08) has that masthead, 'NOVEMBER 8, 2026', a $5764 collection and Liberty weekday and Sunday intentions.

## Worship sites

[St. Peter, Liberty](../churches/st-peter-liberty.md): Saturday 7:00pm Spanish, Sunday 10:30am and 4:00pm. Its shared weekend panel also prints Woodbourne, Livingston Manor and the Bethlehem monastery, which are churches of the other two rows (each has its own bulletin). The archdiocese's directory groups the three as St. Peter - St. Aloysius - Immaculate Conception.

## Website and bulletin provider

The archive at https://stpetersliberty.com/bulletins-1 (eCatholic site 14200; probe url gets HTTP 403, headed Chrome reads it) lists, newest first, three separately headed weekly bulletins: Bulletin St Peter*.pdf, STALOYSIUS*.pdf and Church of the Immaculate Conception Bulletin <dates>.pdf, plus occasional other documents (an Archbishop Hicks letter in November). The three share reflections and one office phone, but each has its own masthead, collection figure, intentions and page 2. The October 2026 session found this too but the collector then had no filename filter; main now has one, so each publisher is its own row with a pinned `page-pdfs` recipe whose `filename=` glob has a distinct literal prefix (`bulletin`, `staloysius`, `church`), and peer `publication_reviews` for every pair. `?` in the globs stands for the spaces in the file names. File names for St. Peter and St. Aloysius carry no date (they gain -1, -2 ... within a month folder), so the pick relies on the page listing newest first.

fetch:check on 2026-11-08 resolved `page-pdfs on https://stpetersliberty.com/bulletins-1: current` and downloaded `Bulletin St Peter.pdf` (the November 8 issue), verification ok. The recipe in `provider_id` is the pinned form.

## Not yet confirmed

Nothing open. If the parish renames its files, the glob stops matching and fetch fails loudly; update the glob then.
