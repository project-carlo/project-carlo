---
name: St. Francis Xavier, Our Lady of the Lake, St. Anthony of Padua, St. Thomas Aquinas and Sacred Heart
  automatic fetch connector
revisit: Obtain a stable full-issue-only archive or implement reviewed content-aware selection. Test both
  October 3/4 and October 10/11 filename pairs, whose full-issue/supplement order reverses; page count and
  weekday also fail. Keep automatic fetching disabled until the selector rejects supplements and fails
  closed when no full issue is found. Publisher and three current public-Mass sites are established.
revisit_after: 2026-10-15
roster: []
evidence:
- url: https://files.ecatholic.com/11769/bulletins/20261011.pdf
  seen: 2026-10-08
  quote: Saint Francis Xavier-Our Lady of the Lake-St. Anthony of Padua-
  note: Downloaded and read both pages. Page 1 is the full October 11 issue masthead and three building-specific Mass schedules; page 2 contains October 10-17 intentions. Already posted on October 8, not a claim that future Masses occurred.
- url: https://files.ecatholic.com/11769/bulletins/20261010.pdf
  seen: 2026-10-08
  quote: PLEASE SUPPORT OUR ADVERTISERS!
  note: Downloaded and read both pages. Prayer list, bazaar notice and advertisers, without the parish masthead or worship-site timetable; this is the companion supplement.
- url: https://files.ecatholic.com/11769/bulletins/20261003.pdf
  seen: 2026-10-07
  quote: Saint Francis Xavier-Our Lady of the Lake-St. Anthony of Padua-
  note: 'October 4, 2026 masthead is 20261003.pdf page 1: one publisher with five dedications. Yulan St.
    Anthony/St. Thomas Aquinas, 25 Beaver Brook Road: Saturday 4 PM; Sunday 11:30 AM; Tuesday/Thursday
    9 AM. 20261004.pdf is a supplement, not another publisher. Narrowsburg/Lake Huntington are cross-slice.'
parish: st-francis-xavier-our-lady-of-the-lake-st-anthony-of-padua-st-thomas-aquinas-and-sacred-heart
---

## What is known

The actual publisher and three current public-Mass sites are established in the October 4 and October 11 issues. Automatic fetching remains disabled because the official archive mixes full issues and supplements, with inconsistent filename order. The October 4 full issue is `20261003.pdf` and its newer-dated supplement is `20261004.pdf`; the October 11 full issue is `20261011.pdf` and its earlier-dated supplement is `20261010.pdf`. A stable full-issue-only channel or reviewed content-aware rule is still required.

## October 8 follow-up: selection cannot be pinned by filename

The rendered official archive at https://sfx-sap.org/bulletins now lists October 11 and October 10 above the October 4/3 pair. Both newer PDFs were downloaded and both have two readable pages. This time `20261011.pdf` is the full issue with the parish masthead and schedules for 151 Bridge Street, 6590 State Route 52 and 25 Beaver Brook Road; `20261010.pdf` is the prayer/advertising supplement. For October 4, the full issue had the earlier filename and the supplement the later one. Thus newest date happens to work for the presently posted issue, but Saturday versus Sunday, odd/even date and page count are not stable full-issue selectors. Reenabling the ordinary eCatholic reader merely because it picks October 11 correctly would leave the demonstrated supplement-ingestion failure unresolved.

The remaining blocker is a reviewed content-aware PDF selector, or a parish-supplied stable full-issue-only archive. A selector must inspect the actual masthead and site-specific Mass timetable, handle either filename order, reject the companion supplement, and fail closed when no complete issue is found. Its regression fixtures must include both October 3/4 and October 10/11 pairs; a page-count or weekday filter is insufficient. The active publisher and three buildings are settled; this is an ingestion implementation blocker rather than unfinished building research.

## Off-site safeguard

Under the October 7 off-site policy, this publisher and its three established public-Mass churches remain in the curated evidence records but are omitted from the live CSVs and site, without promoted stamps, until the connector reliably selects the full issue rather than the newer-dated supplement.

Resolve the format/full-issue selection question and test the resulting connector on the current publication before enabling automatic fetch. This is a pipeline question, not a second physical church or an absence-based exclusion.
