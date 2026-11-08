---
name: Our Lady of Mount Carmel, Tenafly
website: https://olmc.us/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:36339']
group: ''
evidence:
- url: https://files.ecatholic.com/36339/bulletins/20261101.pdf
  seen: 2026-11-03
  quote: Solemnity of All Saints
  note: '1 November 2026 issue (8 pages; the text layer is sparse, pages 1-2 rendered with render.py).
    Page 1 masthead (image): ''the catholic community of OUR LADY OF MOUNT CARMEL'', ''Volume 13, Issue
    44: November 1, 2026'', footer ''10 County Road / Tenafly, NJ 07670 / 201.568.0545 / www.olmc.us''.
    Page 2 (image): ''Masses Daily Monday – Saturday 8:30 AM Weekends Saturday 5:00 PM Sunday 8:00 AM,
    10:00 AM, 12:00 NOON''; Pastor Fr. Richard Supple, O.Carm.'
- url: https://olmc.us/bulletins
  seen: 2026-11-03
  note: 'eCatholic bulletin page (read with parish-site-access visit.py): weekly files.ecatholic.com/36339/bulletins/YYYYMMDD.pdf
    issues, newest ''November 1, 2026'', then October 25, 18, 11.'
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

Our Lady of Mount Carmel, Tenafly, publishes its own weekly bulletin ('Volume 13, Issue 44') on its eCatholic site (ecatholic:36339). I read the 1 November 2026 issue: the page 1 masthead (image) names 'the catholic community of OUR LADY OF MOUNT CARMEL', 10 County Road, Tenafly, and page 2 gives one Mass schedule. No other parish or church is named. No printer's footer (LPi, Bon Venture, John Patrick) appears in the text of any page; it looks parish-produced.

## Worship sites

- Our Lady of Mount Carmel Church, 10 County Road (`our-lady-of-mount-carmel-tenafly`): Saturday 5:00 PM; Sunday 8:00 AM, 10:00 AM, 12:00 noon; Monday-Saturday 8:30 AM (page 2).

The directory (194) and GCatholic (18562) list only this church. The Academy of Our Lady of Mount Carmel (the parish school, page 2 staff list) is not a separate worship site.

## Website and bulletin provider

https://olmc.us/ (the directory's address; GCatholic gives www.olmc.us) is an eCatholic site. `probe get` read the homepage; `visit.py` loaded it and its /bulletins page and reported ecatholic:36339. Provider `ecatholic`, read from the site's Sunday-dated files. The issue's pages are mostly images with fragments of text, so the pipeline needs to read the schedule as an image.

Fetch check (2026-11-03, headed): transport ok, PDF, picked `files.ecatholic.com/36339/bulletins/20261101.pdf`, the 1 November 2026 issue read above; freshness fresh (2 days). Publication identity `unverified` in the check (the masthead is an image); the rendered masthead confirms it.

## Not yet confirmed

Nothing open for this row.
