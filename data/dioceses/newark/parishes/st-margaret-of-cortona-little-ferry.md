---
name: St. Margaret of Cortona, Little Ferry
website: https://www.stmargaretlfnj.org/
bulletin_provider: other
provider_id: page-pdfs https://www.stmargaretlfnj.org/bulletins
publication: ['url:https://www.stmargaretlfnj.org/bulletins']
group: Planning Area D
evidence:
- url: https://www.stmargaretlfnj.org/_files/ugd/1b4306_9553c92555884ef786650c5a4289b60f.pdf
  seen: 2026-11-03
  quote: Serving the Catholic Communities of
  note: 'Newest issue on the Bulletins page (4 pages, text layer, parish-produced, no publisher footer).
    Page 1: ''St. Margaret of Cortona Parish, Serving the Catholic Communities of Little Ferry and Moonachie'',
    Pastor Rev. Kevin E. Carter, dated ''September 13, 2026''.'
- url: https://www.stmargaretlfnj.org/_files/ugd/1b4306_9553c92555884ef786650c5a4289b60f.pdf
  seen: 2026-11-03
  quote: 'Saturday Vigil: 5:30 p.m.'
  note: 'Page 1 Mass Schedule: Saturday Vigil 5:30 p.m., Sunday 9:00 a.m. & 11:30 a.m., Monday to Friday
    12:00 p.m.; no other worship site named.'
- url: https://www.stmargaretlfnj.org/bulletins
  seen: 2026-11-03
  note: The Wix Bulletins page (probe get and visit.py) lists 'Past Bulletins … September 13, 2026, September
    6, 2026, August 30, 2026, August 23, 2026, August 9, 2026 …' newest first, each a _files/ugd/1b4306_<hash>.pdf
    with no date in its name.
- url: https://parishesonline.com/organization/st-margaret-of-cortona-church-07643
  seen: 2026-11-03
  note: 'probe po: org ''St. Margaret of Cortona Church'', 31 Chamberlain Ave, Little Ferry, lpi 0018000000QxABvAAN,
    website stmargaretlfnj.org, but no publications (''does not publish a bulletin here now''). Not recorded
    in publication.'
revisit: Check whether https://www.stmargaretlfnj.org/bulletins lists an issue newer than 13 September
  2026, and rerun fetch:check.
revisit_after: 2026-11-17
research:
- method: probe get and visit.py on the parish Bulletins page and homepage; probe pdf on each linked PDF;
    probe po on st-margaret-of-cortona-church-07643
  url: https://www.stmargaretlfnj.org/bulletins
  checked: '2026-11-03'
  outcome: not-found
  next_action: Reread the Bulletins page for an issue after 13 September 2026 and rerun fetch:check; if
    none by mid-December, ask whether the parish has moved its bulletin elsewhere
  retry_when: The Bulletins page lists a newer issue, or 2026-11-17 arrives
  revisit_after: 2026-11-17
bulletin_status: available
---

## Publisher

The parish produces its own 4-page bulletin and posts it on its Wix site; no publisher's footer appears. The newest issue on the Bulletins page on 3 November 2026 is dated 13 September 2026: page 1 "St. Margaret of Cortona Parish, Serving the Catholic Communities of Little Ferry and Moonachie", Pastor Rev. Kevin E. Carter. The homepage (read the same day) has current news (a Mass of Remembrance on 2 November 2026), so the parish is active; only the bulletin uploads stopped.

## Worship sites

One church, `st-margaret-of-cortona-little-ferry`. The 13 September Mass Schedule gives Saturday Vigil 5:30 PM, Sunday 9:00 and 11:30 AM and Monday-Friday 12:00 noon, naming no other site. Moonachie's own parish, St. Anthony, is listed as Closed on the archdiocese's table of closed or merged parishes (scratch/newark-map-1/tools/rcan-closed-merged-2025-05.tsv) and is in neither roster. The archdiocese directory (103) and GCatholic (18467) list only this church.

## Website and bulletin provider

The website is the directory's https://www.stmargaretlfnj.org/. Provider `other`, pinned to `page-pdfs https://www.stmargaretlfnj.org/bulletins`, which lists the issues newest first; the homepage links only brochures and forms, so it must not be the page read. A ParishesOnline org (st-margaret-of-cortona-church-07643) exists but has no issues, so it is left out of `publication`.

Fetch check (2026-11-03, headed): transport ok, PDF; resolved `page-pdfs on https://www.stmargaretlfnj.org/bulletins: first-listed, dated 2026-09-13`, the issue read above, so the recipe picks the right document but freshness is `stale` and overall `failed`. The recipe is the one in `provider_id`; it needs no change once a newer issue is posted.

## Not yet confirmed

Whether the bulletin is still published weekly: the site's newest issue is 13 September 2026, seven weeks old (the archive also skips 16 August). The research item and `revisit_after` 2026-11-17 cover rechecking it.
