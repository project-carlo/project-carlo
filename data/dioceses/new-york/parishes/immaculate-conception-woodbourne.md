---
name: Immaculate Conception
website: https://stpetersliberty.com/bulletins-1
bulletin_provider: other
provider_id: page-pdfs https://stpetersliberty.com/bulletins-1 filename=Church?of?the?Immaculate?Conception*.pdf
publication: ['url:https://stpetersliberty.com/bulletins-1#immaculate-conception-woodbourne']
group: St. Peter - St. Aloysius - Immaculate Conception
evidence:
- url: https://files.ecatholic.com/14200/documents/2026/10/Church%20of%20the%20Immaculate%20Conception%20Bulletin%20October%2031%20%20November%201%202026.docx.pdf
  seen: 2026-10-31
  quote: 'Mass Schedule: Saturday Vigil 4:00 PM and Sunday 9:00 AM'
  note: The October 31/November 1, 2026 issue (file name dated; the masthead's date line misprints the
    year as 'November 1st, 2025 All Saints Day', but the readings are this year's All Saints Sunday).
    Page 1 masthead names Church of the Immaculate Conception, 6317 State Route 42, Woodbourne alone,
    with its own schedule, collection ($1,502) and religious-education notices.
- url: https://stpetersliberty.com/bulletins-1
  seen: 2026-10-31
  note: Rendered in headed Chrome (probe url gets HTTP 403). Newest first; each week posts Bulletin St
    Peter-N.pdf, STALOYSIUS-N.pdf and 'Church of the Immaculate Conception Bulletin <dates>.pdf' on eCatholic
    site 14200.
- url: https://files.ecatholic.com/14200/documents/2026/11/Church%20of%20the%20Immaculate%20Conception%20Bulletin%20%20November%207%208%202026.pdf
  seen: 2026-11-08
  note: November 8, 2026 issue, the newest for this publisher on the shared archive and the file fetch:check
    picked on 2026-11-08. The Immaculate Conception bulletin, published for Church of the Immaculate Conception,
    6317 State Route 42, Woodbourne. The November 7/8, 2026 issue (read 2026-11-08) has that masthead,
    its own schedule (Saturday Vigil 4:00 PM, Sunday 9:00 AM), 'November 8th, 2026' and a $1,295.00 collection.
    The November 1 issue's date line misprinted the year as 2025; its file name and readings are 2026.
revisit: Re-run fetch:check after the next upload; if Woodbourne's file stops being named Church of the
  Immaculate Conception*.pdf, update the filename glob.
revisit_after: 2026-11-22
promoted: 2026-11-09
research:
- method: Headed-Chrome visit of the shared archive and probe pdf of the newest Woodbourne file
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
      alone, with a $5351 collection and Liberty intentions; the Woodbourne issue of the same week names
      Church of the Immaculate Conception, Woodbourne, with a $1,502 collection.
- parish: st-aloysius-livingston-manor
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/14200/documents/2026/10/STALOYSIUS-4.pdf
    seen: 2026-10-31
    note: The November 1, 2026 St. Aloysius masthead names St. Aloysius, 22 Church Street, Livingston
      Manor alone, with a $902 collection; the Woodbourne issue of the same week names Church of the Immaculate
      Conception, Woodbourne.
---

## Publisher

The Immaculate Conception bulletin, published for Church of the Immaculate Conception, 6317 State Route 42, Woodbourne. The November 7/8, 2026 issue (read 2026-11-08) has that masthead, its own schedule (Saturday Vigil 4:00 PM, Sunday 9:00 AM), 'November 8th, 2026' and a $1,295.00 collection. The November 1 issue's date line misprinted the year as 2025; its file name and readings are 2026.

## Worship sites

[Immaculate Conception, Woodbourne](../churches/immaculate-conception-woodbourne.md): Saturday Vigil 4:00 PM, Sunday 9:00 AM. Liberty and Livingston Manor in the shared panel belong to the other two rows.

## Website and bulletin provider

The archive at https://stpetersliberty.com/bulletins-1 (eCatholic site 14200; probe url gets HTTP 403, headed Chrome reads it) lists, newest first, three separately headed weekly bulletins: Bulletin St Peter*.pdf, STALOYSIUS*.pdf and Church of the Immaculate Conception Bulletin <dates>.pdf, plus occasional other documents (an Archbishop Hicks letter in November). The three share reflections and one office phone, but each has its own masthead, collection figure, intentions and page 2. The October 2026 session found this too but the collector then had no filename filter; main now has one, so each publisher is its own row with a pinned `page-pdfs` recipe whose `filename=` glob has a distinct literal prefix (`bulletin`, `staloysius`, `church`), and peer `publication_reviews` for every pair. `?` in the globs stands for the spaces in the file names. File names for St. Peter and St. Aloysius carry no date (they gain -1, -2 ... within a month folder), so the pick relies on the page listing newest first.

fetch:check on 2026-11-08 resolved `page-pdfs on https://stpetersliberty.com/bulletins-1: current` and downloaded `Church of the Immaculate Conception Bulletin  November 7 8 2026.pdf` (the November 8 issue), verification ok. The recipe in `provider_id` is the pinned form.

## Not yet confirmed

Nothing open. If the parish renames its files, the glob stops matching and fetch fails loudly; update the glob then.
