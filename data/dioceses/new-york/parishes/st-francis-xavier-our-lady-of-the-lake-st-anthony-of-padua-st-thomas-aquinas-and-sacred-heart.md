---
name: St. Francis Xavier, Our Lady of the Lake, St. Anthony of Padua, St. Thomas Aquinas and Sacred Heart
website: https://sfx-sap.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:11769']
group: ''
evidence:
- url: https://files.ecatholic.com/11769/bulletins/20261011.pdf
  seen: 2026-10-08
  quote: Saint Francis Xavier-Our Lady of the Lake-St. Anthony of Padua-
  note: Actual two-page issue downloaded and read October 8. Page 1 names all five dedications and gives Mass schedules at Narrowsburg, Lake Huntington and Yulan. Future-dated October 11 issue was already posted.
- url: https://files.ecatholic.com/11769/bulletins/20261003.pdf
  seen: 2026-10-07
  quote: Saint Francis Xavier-Our Lady of the Lake-St. Anthony of Padua-
  note: 'October 4, 2026 masthead is 20261003.pdf page 1: one publisher with five dedications. Yulan St.
    Anthony/St. Thomas Aquinas, 25 Beaver Brook Road: Saturday 4 PM; Sunday 11:30 AM; Tuesday/Thursday
    9 AM. 20261004.pdf is a supplement, not another publisher. Narrowsburg/Lake Huntington are cross-slice.'
revisit: Resolve the mixed full-issue/supplement archive with a reviewed content-aware reader or a stable
  full-issue-only channel. Regression-test both October 3/4 and October 10/11 pairs; their filename order
  reverses and the latest full issue and supplement both have two pages. Keep fetch disabled meanwhile.
revisit_after: 2026-10-15
---

## Publisher

The October 4 and already-posted October 11, 2026 mastheads identify one publisher with five dedications, but three physical worship buildings: St. Francis Xavier in Narrowsburg, Our Lady of the Lake in Lake Huntington, and the combined St. Anthony of Padua/St. Thomas Aquinas church at 25 Beaver Brook Road in Yulan. The latest full issue was downloaded and read October 8 and retains all three schedules. A supplement is part of this publication, not another publisher.

## Channel and grouping

Official parish site links the inspected current issue. Current masthead, not administrative merger or account name, determines one publisher. Linked external eCatholic sites are not automatically its publication IDs.

## Worship sites and scope

Linked worship-site records for St. Francis Xavier, Our Lady of the Lake, St. Anthony of Padua, St. Thomas Aquinas and Sacred Heart: [Our Lady of the Lake Church](../churches/our-lady-of-the-lake-lake-huntington.md), [St. Anthony of Padua](../churches/st-anthony-of-padua-yulan.md), [St. Francis Xavier](../churches/st-francis-xavier-narrowsburg.md). Each church record retains its building-specific Mass evidence.

[The automatic fetch connector](../open/st-francis-xavier-our-lady-of-the-lake-st-anthony-of-padua-st-thomas-aquinas-and-sacred-heart-fetch-connector.md) remains an implementation question because full-issue/supplement filename order reverses between the two inspected weeks. The publisher and its three public-Mass sites are established; the archive must not be enabled with an unsafe date, weekday or page-count heuristic.

## Automatic fetch safeguard

Follow-up on October 8 read both newly posted PDFs: `20261011.pdf` is the two-page full issue, while `20261010.pdf` is its two-page prayer/advertiser supplement. This reverses the full-issue/supplement filename order observed for October 4. Newest date, weekday, filename parity and page count therefore do not safely distinguish the full publication. The latest full issue confirms all three existing worship-site records, but a correct default pick for one week does not resolve this reproducible ingestion hazard. See the connector record for the exact regression pairs and fail-closed selection requirements.

Automatic fetching stays disabled pending the reviewed full-issue selection rule or a separate safe archive. The October 4 newest-date pick would ingest a supplement; the October 11 newest-date pick currently selects the full issue, but that one correct pick does not establish a safe rule for subsequent weeks.

The `no_bulletin` provider keeps this publisher and its three established public-Mass venues out of the live CSVs and site under the October 7 policy, pending safe full-issue selection. It is not a statement that this publisher has no publication. Its actual publication identity, current issue evidence and church records are preserved without promoted stamps.
