---
name: Our Lady of Victories, Harrington Park
website: https://olvhp.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:12991', 'po-container:03/4002']
group: Planning Area B
evidence:
- url: https://files.ecatholic.com/12991/bulletins/20261101.pdf
  seen: 2026-11-03
  quote: Our Lady of Victories Church  |  03-4002
  note: '1 November 2026 issue (6 pages; pages 1-5 image-only, rendered with render.py). Page 1 masthead:
    ''Our Lady of Victories Church (serving Harrington Park, River Vale and the Pascack/Northern Valley)
    150 Harriot Avenue, Harrington Park, New Jersey''; Rev. Edmond P. Ilg, Administrator; MASS SCHEDULE
    Saturday 4pm & 5pm, Sunday 7am, 8am Latin, 9:30am, 10:45am, 12pm, 1pm Spanish, 6pm; OLV Rectory 81
    Lynn Street. The quote is the LPi ad-page footer on page 6.'
- url: https://container.parishesonline.com/bulletins/03/4002/20261101B.pdf
  seen: 2026-11-03
  note: 'probe container 03/4002: the same 1 November 2026 issue (6 pages, page 6 footer ''Our Lady of
    Victories Church | 03-4002''); 8 November not yet posted.'
- url: https://olvhp.org/bulletins
  seen: 2026-11-03
  note: 'eCatholic bulletin page (probe get 403; read with visit.py): weekly files.ecatholic.com/12991/bulletins/YYYYMMDD.pdf
    issues from 2016 to 20261101.pdf.'
bulletin_status: available
---

## Publisher

Our Lady of Victories, Harrington Park, publishes a weekly LPi-printed bulletin (container 03/4002) and posts it on its eCatholic site (ecatholic:12991). I read the 1 November 2026 issue, whose pages 1–5 are images (rendered with render.py): the page 1 masthead names Our Lady of Victories Church alone, 'serving Harrington Park, River Vale and the Pascack/Northern Valley', at 150 Harriot Avenue, with its own Mass schedule (Rev. Edmond P. Ilg, Administrator). The eCatholic copy and container 03/4002 carry the same page 6 footer, 'Our Lady of Victories Church | 03-4002', so both ids are recorded for this one bulletin.

## Worship sites

- Our Lady of Victories Church, 150 Harriot Avenue (`our-lady-of-victories-harrington-park`): Saturday 4pm and 5pm; Sunday 7am, 8am (Latin), 9:30am, 10:45am, 12pm, 1pm (Spanish), 6pm.

The directory (58) and GCatholic (18419) list only this church. Page 2 of the issue mentions a lower church and a CCD 'Family Mass 9:30 in the gym', both on the parish campus; no other building is named. River Vale has no church of this parish in the issue.

## Website and bulletin provider

The directory gives https://olvhp.org/contact-us; the site root https://olvhp.org/ is an eCatholic site behind Cloudflare (`probe get` 403; `visit.py` loads it). GCatholic's geocities.com address is long dead. Provider `ecatholic`, read from the site's Sunday-dated files.

Fetch check (2026-11-03, headed): transport ok, PDF, picked `files.ecatholic.com/12991/bulletins/20261101.pdf`, the 1 November 2026 issue read above; freshness fresh (2 days). Publication identity `unverified` in the check; the rendered masthead confirms it.

## Not yet confirmed

Nothing open. The issue is image-only, so `recheck` can find only the page 6 footer quote; the masthead is cited by note.
