---
name: St. Patrick's Church, Rouses Point
website: https://www.stpatricksrpny.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:15896']
group: ''
evidence:
- url: https://files.ecatholic.com/15896/bulletins/20260927.pdf
  seen: 2026-09-30
  quote: FR. NICOLAS REVILLA, PASTOR
  note: 'Page 1 of the 27 September 2026 issue (2 pages, text layer): "September 27, 2026 FR. NICOLAS
    REVILLA, PASTOR / Sr. Rani Selvaraj, SCC - Pastoral Associate", "Many thanks to all who continue to
    support St. Patrick’s Church with their offertory gifts" and a weekly-collection report for St. Patrick’s
    alone.'
- url: https://files.ecatholic.com/15896/bulletins/20260927.pdf
  seen: 2026-09-30
  quote: Sun. 27 Twenty-Sixth Sunday in Ordinary Time
  note: 'Page 1 Mass intentions: Saturday 26 September "4:00PM (St. Mary’s)", Sunday 27 September "8:00AM
    (St. Patrick’s)" and "10:00AM (St. Patrick’s)", weekdays 9:00AM (St. Patrick’s) Monday to Wednesday
    and 9:00AM (St. Mary’s) Thursday 1 and Friday 2 October, Saturday 3 October 4:00PM (St. Mary’s), Sunday
    4 October 8:00AM and 10:00AM (St. Patrick’s). Two Sunday Masses carry "Parishioners of St. Mary’s
    & St. Patrick’s (pro populo)". So this bulletin schedules both churches.'
- url: https://www.stpatricksrpny.org/
  seen: 2026-09-30
  quote: St. Mary’s and St. Patrick’s Faith Formation Program begins this Sunday, September 27
  note: Parish home page (eCatholic, behind Cloudflare; BLOCKED for several loads and read in a browser
    with visit.py on 2026-09-30, so `recheck` reports it unreachable). The page links "St. Mary's Church,
    Champlain" (stmaryschamplain.org) and two bulletin pages, /bulletins and /bulletins-events; `visit.py`
    reports `ecatholic:15896`.
- url: https://www.stpatricksrpny.org/mass-times
  seen: 2026-09-30
  quote: 'SUNDAY: 8:00 AM 10:00 AM MONWED 9:00 AM Check bulletin to confirm'
  note: Parish Mass Times page (same caveat).
- url: https://www.rcdony.org/parish/rouses-point
  seen: 2026-09-30
  note: 'Directory: directory:rouses-point, St. Patrick''s Church, 140 Lake Street, Rouses Point, website
    https://www.stpatricksrpny.org, phone 518-297-7361, pastor Rev. Nicolas J. Revilla. directory:champlain
    (St. Mary''s Church, 90 Church Street, Champlain, phone 518-298-8244, no website, pastor Reverend
    Nicolas J. Revilla) names the same pastor.'
promoted: 2026-09-30
---

## Publisher

St. Patrick's, Rouses Point publishes its own weekly eCatholic bulletin, site 15896 (files.ecatholic.com/15896/bulletins/YYYYMMDD.pdf; newest 27 September 2026, read 2026-09-30). Its page 1 names Fr. Nicolas Revilla, Pastor, and St. Patrick's own finances, and its Mass-intentions list runs both churches' Masses: St. Patrick's, Rouses Point (Sunday 8:00 and 10:00, weekdays 9:00) and St. Mary's, Champlain (Saturday 4:00, Thursday and Friday 9:00). The pastor and a shared faith-formation program tie St. Patrick's to St. Mary's, Champlain ("OUR BROTHER PARISH" on St. Mary's website).

**This row is kept separate from `st-mary-champlain`.** St. Mary's publishes its own eCatholic bulletin (site 15646; issues weekly through at least 20 September 2026, which reads as a double issue for 20 and 27 September with St. Mary's own Sanctuary Lamp and Stewardship report), so each church has a live bulletin of its own. The README rule is that one live member channel means no merge; the two bulletins' Mass lists overlap, and the audit may flag the pair. The St. Patrick's bulletin alone would supply events for both churches if St. Mary's bulletin ever stopped.

## Worship sites

- `st-patrick-rouses-point` (140 Lake St.): Sunday 8:00 AM and 10:00 AM, Monday to Wednesday 9:00 AM.

Not here: St. Mary's, Champlain has its own row. St. Joseph's, Champlain (GCatholic 18267, 74 Mason Rd) is St. Joseph's Cemetery, which this parish owns (`excluded/st-joseph-cemetery-champlain`). St. Joseph's Oratory, Coopersville, named on the parish's cemeteries page, is in no roster (`open/st-joseph-oratory-coopersville`).

## Website and bulletin provider

`www.stpatricksrpny.org` is the directory's website, an eCatholic site behind Cloudflare (`probe url` HTTP4XX; `visit.py` BLOCKED on one run, then loaded on the fifth load and reported `ecatholic:15896`). Issues fetch without a browser: `issues.py ecatholic ecatholic:15896` read the 27 September 2026 issue (the 4 October one answers 403, not yet posted). Provider id empty; `website` is the eCatholic-hosted site. The old `saintpatricks.ws` (GCatholic's link) answered 503.

## Not yet confirmed

- Whether St. Mary's own bulletin continues after the 20/27 September double issue (the 27 September file was a 403, i.e. not posted, on 2026-09-30).
