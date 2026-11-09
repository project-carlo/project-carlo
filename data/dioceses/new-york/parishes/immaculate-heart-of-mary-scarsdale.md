---
name: Immaculate Heart of Mary, Scarsdale
website: https://www.ihm-parish.org/online-bulletins
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.ihm-parish.org/online-bulletins']
group: ''
evidence:
- url: https://ihmscarsdale.flocknote.com/note/39251992
  seen: 2026-11-08
  quote: IHM CHURCH - November 8 Bulletin
  note: Newest issue linked from the bulletins page on 8 November. HTML; Mass intentions list Sunday 8
    November 5:30PM (vigil), 7:30AM, 9:00AM, 10:30AM, 12:00PM and weekdays 6:45AM and 9:00AM. No bulletin
    PDF.
- url: https://www.ihm-parish.org/online-bulletins
  seen: 2026-11-08
  note: Bulletins page (eCatholic site 21502) rendered in headed Chrome; its three newest links are Flocknote
    notes 39251992, 39167002, 39096026.
- url: https://ihmscarsdale.flocknote.com/note/38697627
  seen: 2026-10-08
  quote: IHM CHURCH - October 4 Bulletin
  note: October 4 issue inspected October 8; its three PDF attachments are flyers (Baby/Maternity Items
    For Gianna, Items for Sisters for Life, AIA Westchester Mass and Dinner Dance), not the weekly issue.
research:
- method: fetch-check resolver from main (provider other, automatic) on the bulletins page
  url: https://www.ihm-parish.org/online-bulletins
  checked: '2026-10-31'
  outcome: unsupported-format
  next_action: Re-run fetch:check with a Flocknote collector once one exists
  retry_when: A collector for Flocknote HTML notes lands on main
- method: issues.py ecatholic ecatholic:21502, eight Sundays 13 September to 1 November
  url: https://files.ecatholic.com/21502/bulletins/
  checked: '2026-10-31'
  outcome: not-found
  next_action: None; the bulletin is the Flocknote note
  retry_when: The bulletins page links a full-issue PDF
- method: headed browser on the bulletins page and newest note
  url: https://ihmscarsdale.flocknote.com/note/39251992
  checked: '2026-11-08'
  outcome: found
bulletin_status: unsupported-format
fetch_gap:
  kind: flocknote-html-note
  seen: 2026-11-08
  url: https://ihmscarsdale.flocknote.com/note/39251992
  note: The weekly bulletin is the HTML text of a Flocknote note, linked newest-first from https://www.ihm-parish.org/online-bulletins.
    Notes sometimes attach flyer PDFs, and fetch:check with provider other (2026-10-31) picked one (babymaternityitemsforgiannashouse.pdf),
    the wrong document. The 8 November 2026 issue was current on 2026-11-08.
---

## Publisher

Immaculate Heart of Mary, Scarsdale publishes its own weekly bulletin as a Flocknote note (HTML), linked newest-first from https://www.ihm-parish.org/online-bulletins (eCatholic site 21502). On 8 November 2026 the newest entry was note 39251992, "IHM CHURCH - November 8 Bulletin", which carries the pastor's letter, parish notices and the week's Mass intentions: Saturday 5:30 PM vigil; Sunday 7:30, 9:00, 10:30 AM and 12:00 PM; weekdays 6:45 and 9:00 AM. Earlier issues read: 4 October (note 38697627), 1 November (note 39167002). It names one church.

## Worship sites

[Immaculate Heart of Mary](../churches/immaculate-heart-of-mary-scarsdale.md), 8 Carman Road. The bulletin names no other place; its "lower church" is part of the same building.

## Website and bulletin provider

`unsupported`, with `fetch_gap` `flocknote-html-note`. The issue is the note's HTML text and images; the PDFs some notes attach are flyers (the October 4 note: baby/maternity items for Gianna's House, Sisters for Life, an AIA dinner dance), not the bulletin. Main's resolver, run on 31 October with provider `other` against the bulletins page, chose one of those flyers, `.../note/39096026/file/624360/babymaternityitemsforgiannashouse.pdf` (recipe `page-pdfs https://new.flocknote.com/note/39096026`), so a PDF recipe would collect the wrong document. No other channel was found: the eCatholic file host has no `bulletins/` PDFs for site 21502 over the eight Sundays to 1 November (all 403); Discover Mass lists no issues; the parish's sponsors page links no printer; a web search found no PDF host.

A Flocknote collector (read the newest dated note linked from the index, keep its HTML text) would make this row fetchable; Resurrection, Rye uses the same platform.

## Not yet confirmed

Nothing about the church is in doubt; only the collector is missing.
