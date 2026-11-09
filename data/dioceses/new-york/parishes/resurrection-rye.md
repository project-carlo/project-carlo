---
name: Resurrection Rye
website: https://resrye.org/churchbulletins
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://resrye.org/churchbulletins']
group: ''
evidence:
- url: https://resrye.org/churchbulletins
  seen: 2026-10-08
  quote: October 4, 2026 Resurrection Church Bulletin
  note: Current official index reopened; three recent issue entries link Flocknote HTML, not a PDF archive.
- url: https://resrye.flocknote.com/note/38786342
  seen: 2026-10-08
  quote: Sunday, October 4th
  note: Full rendered body, outbound anchors and embedded media inspected. Five Sunday Mass intentions
    and October 5-10 weekday intentions remain readable; no PDF rendition is linked.
- url: https://new.flocknote.com/note/38786342
  seen: 2026-10-07
  quote: RESURRECTION CHURCH BULLETIN October 4, 2026
  note: Issue identity and current site-specific Mass schedule; see explanation.
- url: https://new.flocknote.com/note/38786342
  seen: 2026-10-07
  quote: Sunday, October 4th 7:30 am
  note: Issue identity and current site-specific Mass schedule; see explanation.
- url: https://resrye.flocknote.com/note/39343753
  seen: 2026-11-08
  quote: November 8, 2026 Resurrection Church Bulletin
  note: Newest issue linked from the bulletin index on 8 November; HTML text with Mass intentions for
    7 to 14 November (Sunday 7:30, 8:45, 10:00, 11:15 AM, 12:30 PM). No PDF or file link in the note.
- url: https://resrye.flocknote.com/note/39106123
  seen: 2026-10-31
  quote: October 25, 2026 Resurrection Church Bulletin
  note: 25 October issue, HTML only; the note main's resolver reached before reporting no PDF.
- url: https://resrye.org
  seen: 2026-10-31
  quote: Weekly Bulletin
  note: Parish homepage (eCatholic site 16361) rendered in headed Chrome; Mass Times Sunday 7:30, 8:45,
    10:00, 11:15 AM, 12:30 PM; Saturday 5:00 PM Vigil.
research:
- method: fetch-check resolver from main (provider other, automatic) on the bulletin index
  url: https://resrye.org/churchbulletins
  checked: '2026-10-31'
  outcome: unsupported-format
  next_action: Re-run fetch:check with a Flocknote collector once one exists
  retry_when: A collector for Flocknote HTML notes lands on main
- method: issues.py ecatholic ecatholic:16361, eight Sundays 13 September to 1 November
  url: https://files.ecatholic.com/16361/bulletins/
  checked: '2026-10-31'
  outcome: not-found
  next_action: None; the bulletin is the Flocknote note
  retry_when: The bulletin index links a PDF instead of a note
- method: headed browser on the bulletin index and newest note
  url: https://resrye.flocknote.com/note/39343753
  checked: '2026-11-08'
  outcome: found
bulletin_status: unsupported-format
fetch_gap:
  kind: flocknote-html-note
  seen: 2026-11-08
  url: https://resrye.flocknote.com/note/39343753
  note: 'The weekly bulletin is the HTML text of a Flocknote note (no PDF or image), linked newest-first
    from https://resrye.org/churchbulletins; the index links carry no text. fetch:check with provider
    other (2026-10-31) reached the 25 October note and failed: ''No PDF links found on bulletin post page''.
    The 8 November 2026 issue was current on 2026-11-08.'
---

## Publisher

Resurrection, Rye publishes its own weekly bulletin as a Flocknote note (HTML), linked from the parish's bulletin index https://resrye.org/churchbulletins (eCatholic site 16361). On 8 November 2026 the index's newest entry was note 39343753, "November 8, 2026 Resurrection Church Bulletin", whose text gives the weekend Masses Saturday 5:00 PM and Sunday 7:30, 8:45, 10:00, 11:15 AM and 12:30 PM, weekday 8:00 and 9:00 AM, with intentions for 7 to 14 November. Earlier issues read: 4 October (note 38786342) and 25 October (note 39106123), the same pattern. It names one church.

## Worship sites

[Resurrection](../churches/resurrection-rye.md), 910 Boston Post Road. The bulletin and the parish homepage's Mass times name no other place.

## Website and bulletin provider

`unsupported`, with `fetch_gap` `flocknote-html-note`: the bulletin is the text of a Flocknote note, with no PDF or image of the issue. The notes carry no PDF attachment (checked on the 4 October, 25 October and 8 November issues). Main's resolver, run on 31 October with provider `other` against https://resrye.org/churchbulletins, followed the dated-post path to the 25 October note and stopped: "No PDF links found on bulletin post page". No other channel was found: the eCatholic file host has no `bulletins/` PDFs for site 16361 over the eight Sundays to 1 November (all 403), Discover Mass lists no issues, and a web search turned up no PDF host.

A Flocknote collector (read the newest dated note linked from the index, keep its HTML text) would make this row fetchable; St. John the Evangelist, Mahopac and Immaculate Heart of Mary, Scarsdale use the same platform.

## Not yet confirmed

Nothing about the church is in doubt; only the collector is missing.
