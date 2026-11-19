---
name: St. Aloysius
website: https://stpetersliberty.com/bulletins-1
bulletin_provider: other
provider_id: page-pdfs https://stpetersliberty.com/bulletins-1 filename=STALOYSIUS*.pdf
publication: ['url:https://stpetersliberty.com/bulletins-1#st-aloysius']
group: St. Peter - St. Aloysius - Immaculate Conception
evidence:
- url: https://files.ecatholic.com/14200/documents/2026/10/STALOYSIUS-4.pdf
  seen: 2026-10-31
  quote: 22 Church Street, P.O. Box. 206
  note: The November 1, 2026 (All Saints) issue, newest St. Aloysius file on the shared archive. Page
    1 masthead names St. Aloysius, Livingston Manor alone, with its own collection ($902). Its weekend
    schedule gives Sunday 8:30am Livingston Manor and 9:30am at the Monastery of Sisters of Bethlehem,
    Livingston Manor, 'All are welcome.'
- url: https://files.ecatholic.com/14200/documents/2026/10/STALOYSIUS.pdf
  seen: 2026-10-31
  quote: October 4, 2026
  note: The dated October 4 issue has the same St. Aloysius masthead; the -2 and -3 files are dated October
    18 and 25. The November 1 file carries no date line but has the All Saints readings.
- url: https://stpetersliberty.com/bulletins-1
  seen: 2026-10-31
  note: Rendered in headed Chrome (probe url gets HTTP 403). Newest first; each week posts Bulletin St
    Peter-N.pdf, STALOYSIUS-N.pdf and a dated Immaculate Conception file on eCatholic site 14200.
- url: https://files.ecatholic.com/14200/documents/2026/11/STALOYSIUS.pdf
  seen: 2026-11-08
  note: November 8, 2026 issue, the newest for this publisher on the shared archive and the file fetch:check
    picked on 2026-11-08. The St. Aloysius bulletin, published for St. Aloysius, 22 Church Street, Livingston
    Manor. The November 8, 2026 issue (read 2026-11-08) has that masthead, 'NOVEMBER 8, 2026' and a $919
    collection.
revisit: Re-run fetch:check after the next upload; if St. Aloysius's file stops being named STALOYSIUS*.pdf,
  update the filename glob.
revisit_after: 2026-11-22
promoted: 2026-11-09
research:
- method: Headed-Chrome visit of the shared archive and probe pdf of the October and November St. Aloysius
    files
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
- parish: st-peter-liberty
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/14200/documents/2026/10/Bulletin%20St%20Peter-4.pdf
    seen: 2026-10-31
    note: The November 1, 2026 St. Peter masthead names St. Peter's Church, 262 North Main St., Liberty
      alone, with a $5351 collection and Liberty intentions; the St. Aloysius issue of the same week names
      St. Aloysius, Livingston Manor, with a $902 collection and different page 2 content.
- parish: immaculate-conception-woodbourne
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/14200/documents/2026/10/Church%20of%20the%20Immaculate%20Conception%20Bulletin%20October%2031%20%20November%201%202026.docx.pdf
    seen: 2026-10-31
    note: The October 31/November 1, 2026 Woodbourne masthead names Church of the Immaculate Conception,
      6317 State Route 42, Woodbourne alone, with its own collection ($1,502) and announcements; the St.
      Aloysius issue of the same week names St. Aloysius, Livingston Manor.
---

## Publisher

The St. Aloysius bulletin, published for St. Aloysius, 22 Church Street, Livingston Manor. The November 8, 2026 issue (read 2026-11-08) has that masthead, 'NOVEMBER 8, 2026' and a $919 collection.

## Worship sites

[St. Aloysius, Livingston Manor](../churches/st-aloysius-livingston-manor.md): Sunday 8:30am. [Monastery of Bethlehem](../churches/monastery-of-bethlehem-livingston-manor.md): Sunday 9:30am, 'All are welcome', in this bulletin's schedule; filed here as the Livingston Manor publisher. Liberty and Woodbourne in the shared panel belong to the other two rows.

## Website and bulletin provider

The archive at https://stpetersliberty.com/bulletins-1 (eCatholic site 14200; probe url gets HTTP 403, headed Chrome reads it) lists, newest first, three separately headed weekly bulletins: Bulletin St Peter*.pdf, STALOYSIUS*.pdf and Church of the Immaculate Conception Bulletin <dates>.pdf, plus occasional other documents (an Archbishop Hicks letter in November). The three share reflections and one office phone, but each has its own masthead, collection figure, intentions and page 2. The October 2026 session found this too but the collector then had no filename filter; main now has one, so each publisher is its own row with a pinned `page-pdfs` recipe whose `filename=` glob has a distinct literal prefix (`bulletin`, `staloysius`, `church`), and peer `publication_reviews` for every pair. `?` in the globs stands for the spaces in the file names. File names for St. Peter and St. Aloysius carry no date (they gain -1, -2 ... within a month folder), so the pick relies on the page listing newest first.

fetch:check on 2026-11-08 resolved `page-pdfs on https://stpetersliberty.com/bulletins-1: current` and downloaded `STALOYSIUS.pdf` (the November 8 issue), verification ok. The recipe in `provider_id` is the pinned form.

## Not yet confirmed

Nothing open. If the parish renames its files, the glob stops matching and fetch fails loudly; update the glob then.
