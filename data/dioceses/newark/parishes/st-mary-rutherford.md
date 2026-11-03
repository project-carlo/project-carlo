---
name: St. Mary, Rutherford
website: https://www.stmaryrutherford.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Planning Area C
evidence:
- url: https://www.stmaryrutherford.org/
  seen: 2026-11-03
  note: probe get on https://www.stmaryrutherford.org/, http://stmaryrutherford.org/ and two /bulletin(s)
    paths answered HTTP 403; parish-site-access visit.py got Cloudflare's 'Just a moment...' on every
    load in three runs (28 loads, about 15:10-15:35).
- url: https://parishesonline.com/organization/st-mary-church-07070
  seen: 2026-11-03
  note: 'probe po: org ''St. Mary Church'', 91 Home Ave, Rutherford, NJ 07070, website http://www.stmaryrutherford.org/,
    lpi 0018000000QxAALAA3, with no publications (''this organization does not publish a bulletin here
    now''); an old account, so its ids are not recorded as this bulletin''s.'
- url: https://rcan.org/parishes/
  seen: 2026-11-03
  note: The archdiocese directory (entry 182) lists St. Mary Parish, 91 Home Avenue, Rutherford, NJ 07070,
    website https://www.stmaryrutherford.org/.
revisit: Open https://www.stmaryrutherford.org/ with visit.py --bulletin (or its 13 May 2026 Wayback snapshot)
  and find where the weekly bulletin is posted; set the provider and publication ids, read the latest
  masthead and Mass schedule, and run fetch:check.
revisit_after: 2026-11-10
research:
- method: probe get and parish-site-access visit.py --bulletin on the parish site
  url: https://www.stmaryrutherford.org/
  checked: '2026-11-03'
  outcome: access-blocked
  next_action: Run visit.py --bulletin on https://www.stmaryrutherford.org/ again; if it loads, read the
    Bulletin menu for the publisher, set the provider and run fetch:check
  retry_when: A later session (Cloudflare blocks pass between runs)
  revisit_after: 2026-11-10
- method: Wayback snapshot of the homepage (web.archive.org/web/20260513220016id_/https://www.stmaryrutherford.org/)
  url: http://web.archive.org/web/20260513220016id_/https://www.stmaryrutherford.org/
  checked: '2026-11-03'
  outcome: access-blocked
  next_action: Fetch the 13 May 2026 snapshot with probe get and read its bulletin link (the publisher
    or file host)
  retry_when: archive.org stops answering HTTP 429 (four tries over 25 minutes on 2026-11-03)
- method: probe po guesses (st-mary-church-07070 found, empty; st-mary-07070, st-mary-parish-07070, st-marys-church-07070
    none); John Patrick church-bulletin.org/<id> listings 500-720 and 6000-6120 scanned for a Rutherford
    slug; Discover Mass slugs st-mary-rutherford-nj and st-mary-church-rutherford-nj (404)
  checked: '2026-11-03'
  outcome: not-found
  next_action: Read the publisher from the parish site or its Wayback copy rather than guessing further
  retry_when: The parish site or its Wayback snapshot can be read
bulletin_status: access-blocked
---

## Publisher

Not yet known. The parish site https://www.stmaryrutherford.org/ is behind Cloudflare and refused every load on 2026-11-03 (probe get HTTP 403; visit.py BLOCKED in three runs, 28 loads), and archive.org answered HTTP 429 to the Wayback snapshot of 13 May 2026. A ParishesOnline org (st-mary-church-07070, lpi 0018000000QxAALAA3) exists for this address but carries no publications, so it is an old account, not this bulletin; its ids are left out of `publication`. A scan of John Patrick listings (ids 500-720, 6000-6120) and two Discover Mass slugs found nothing for Rutherford. See `research`.

## Worship sites

One church, `st-mary-rutherford`, the only place the archdiocese directory (182) and GCatholic (18550) list for the parish. No Mass schedule was read, so whether the bulletin names other sites is unconfirmed.

## Website and bulletin provider

The website is the directory's (and GCatholic's) https://www.stmaryrutherford.org/. The provider is `no_bulletin` with `bulletin_status: access-blocked` until the bulletin is found: a block, not evidence that none is published.

## Not yet confirmed

The publisher, the current masthead and the Mass schedule. Next step: `revisit` (from 2026-11-10).
