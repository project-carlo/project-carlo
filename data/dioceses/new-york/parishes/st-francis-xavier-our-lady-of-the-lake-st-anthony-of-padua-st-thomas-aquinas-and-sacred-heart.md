---
name: St. Francis Xavier, Our Lady of the Lake, St. Anthony of Padua, St. Thomas Aquinas and Sacred Heart
website: https://sfx-sap.org/
bulletin_provider: unsupported
provider_id: ''
publication: ['ecatholic:11769']
group: ''
evidence:
- url: https://files.ecatholic.com/11769/bulletins/20261011.pdf
  seen: 2026-10-08
  quote: Saint Francis Xavier-Our Lady of the Lake-St. Anthony of Padua-
  note: Actual two-page issue downloaded and read October 8. Page 1 names all five dedications and gives
    Mass schedules at Narrowsburg, Lake Huntington and Yulan. Future-dated October 11 issue was already
    posted.
- url: https://files.ecatholic.com/11769/bulletins/20261003.pdf
  seen: 2026-10-07
  quote: Saint Francis Xavier-Our Lady of the Lake-St. Anthony of Padua-
  note: 'October 4, 2026 masthead is 20261003.pdf page 1: one publisher with five dedications. Yulan St.
    Anthony/St. Thomas Aquinas, 25 Beaver Brook Road: Saturday 4 PM; Sunday 11:30 AM; Tuesday/Thursday
    9 AM. 20261004.pdf is a supplement, not another publisher. Narrowsburg/Lake Huntington are cross-slice.'
- url: https://files.ecatholic.com/11769/bulletins/20261108.pdf
  seen: 2026-11-08
  quote: 151 Bridge
  note: 'November 8, 2026 full issue: masthead and schedules for the three churches (151 Bridge Street
    Narrowsburg, State Route 52, Beaver Brook Road). 20261107.pdf the same week is the two-page advertiser
    supplement (''ADVERTIS...''). The same Sunday-full / Saturday-supplement pattern holds for October
    17/18, 24/25 and October 31/November 1.'
revisit: When a content-aware eCatholic pick lands (pnpm diocese gaps, kind dated-supplement-beside-issue),
  set the provider to ecatholic, run fetch:check, and clear fetch_gap.
revisit_after: 2026-12-06
research:
- method: headed-Chrome visit of https://sfx-sap.org/bulletins; probe pdf of every November and late-October
    file; fetch:check with provider ecatholic
  url: https://sfx-sap.org/bulletins
  checked: '2026-11-08'
  outcome: found
  next_action: Set bulletin_provider back to ecatholic once a collector can skip the supplement by content,
    or if the owner accepts the newest-date pick (right every week since October 11)
  revisit_after: 2026-12-06
bulletin_status: available
fetch_gap:
  kind: dated-supplement-beside-issue
  seen: 2026-11-08
  url: https://sfx-sap.org/bulletins
  note: 'Each week the eCatholic 11769 archive posts two two-page PDFs a day apart: the full issue (masthead
    and Mass schedules for 151 Bridge Street, 6590 State Route 52 and 25 Beaver Brook Road) and an advertiser/prayer
    supplement. Since October 11 the full issue has the Sunday date (20261108.pdf) and the supplement
    the Saturday date (20261107.pdf), so the eCatholic reader''s newest pick is right (fetch:check 2026-11-08
    picked 20261108.pdf); but on October 4 the order was reversed (full 20261003.pdf, supplement 20261004.pdf),
    when it would have picked the supplement. No filename glob separates them; a reader would need to
    check the content (masthead) and skip the supplement.'
---

## Publisher

The October 4 and already-posted October 11, 2026 mastheads identify one publisher with five dedications, but three physical worship buildings: St. Francis Xavier in Narrowsburg, Our Lady of the Lake in Lake Huntington, and the combined St. Anthony of Padua/St. Thomas Aquinas church at 25 Beaver Brook Road in Yulan. The latest full issue was downloaded and read October 8 and retains all three schedules. A supplement is part of this publication, not another publisher.

## Channel and grouping

Official parish site links the inspected current issue. Current masthead, not administrative merger or account name, determines one publisher. Linked external eCatholic sites are not automatically its publication IDs.

## Worship sites and scope

Linked worship-site records: [Our Lady of the Lake Church](../churches/our-lady-of-the-lake-lake-huntington.md), [St. Anthony of Padua](../churches/st-anthony-of-padua-yulan.md), [St. Francis Xavier](../churches/st-francis-xavier-narrowsburg.md). The November 8, 2026 full issue still gives schedules for all three buildings.

The October 2026 connector question (open/...-fetch-connector) is closed and deleted: its finding now lives in this row's `fetch_gap`.

## Automatic fetch safeguard

The archive mixes each week's full issue with a two-page advertiser/prayer supplement dated a day apart. On October 4 the supplement had the later date (20261004.pdf, full issue 20261003.pdf); from October 11 to November 8 the full issue has the Sunday date and the supplement the Saturday before (checked 2026-11-08 for October 17/18, 24/25, October 31/November 1 and November 7/8). The eCatholic reader takes the newest date, so it picks the full issue now (fetch:check 2026-11-08: 20261108.pdf) but would have picked the supplement on October 4.

Under main's November rules this is `bulletin_provider: unsupported` with a `fetch_gap` (kind `dated-supplement-beside-issue`), not `no_bulletin`: the bulletin exists and is current. The row and its three churches stay off the site until a reader skips the supplement by content, or the owner accepts the newest-date pick.
