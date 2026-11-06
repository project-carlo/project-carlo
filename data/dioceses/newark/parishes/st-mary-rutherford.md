---
name: St. Mary, Rutherford
website: https://www.stmaryrutherford.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1558
publication: ['url:http://sponsors.bonventure.net/?page=1558']
group: ''
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
- url: http://web.archive.org/web/20260513220016id_/https://www.stmaryrutherford.org/
  seen: 2026-11-05
  note: The 13 May 2026 Wayback capture of the parish homepage (probe get) has a menu item 'Bulletin'
    linking http://sponsors.bonventure.net/?page=1558.
- url: http://sponsors.bonventure.net/?page=1558
  seen: 2026-11-05
  note: Bon Venture sponsors page headed '91 Home Avenue • Rutherford, NJ 07070', listing pdfs/1558/2026-11-08.pdf
    as the newest issue.
- url: http://sponsors.bonventure.net/pdfs/1558/2026-11-08.pdf
  seen: 2026-11-05
  quote: CHURCH OF SAINT MARY
  note: '8 November 2026 bulletin (12 pages, text layer). Pages 1-3 are an All Souls remembrance list
    headed ''The Church of Saint Mary, Rutherford, New Jersey''. Page 4 masthead: ''CHURCH OF SAINT MARY
    91 HOME AVENUE RUTHERFORD, NEW JERSEY 07070''; Saturday 5:00 pm, Sunday 8:00, 10:00 & 12:00 noon,
    Monday-Friday 8:30 am; ''Rev. Charles Pinyan ... Pastor''; footer ''002D (CK) - St. Mary''s, Rutherford
    ... BON VENTURE SERVICES, LLC''.'
promoted: 2026-11-05
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
- method: probe get and parish-site-access visit.py --bulletin on the parish site
  url: https://www.stmaryrutherford.org/
  checked: '2026-11-05'
  outcome: access-blocked
  next_action: None needed for the bulletin, which is read from Bon Venture; open the site with visit.py
    only to check for a second worship site or a new bulletin link
  retry_when: fetch:check stops finding new issues on Bon Venture page 1558
- method: Wayback snapshot of the homepage (web.archive.org/web/20260513220016id_/https://www.stmaryrutherford.org/)
  url: http://web.archive.org/web/20260513220016id_/https://www.stmaryrutherford.org/
  checked: '2026-11-05'
  outcome: found
- method: probe po guesses (st-mary-church-07070 found, empty; st-mary-07070, st-mary-parish-07070, st-marys-church-07070
    none); John Patrick church-bulletin.org/<id> listings 500-720 and 6000-6120 scanned for a Rutherford
    slug; Discover Mass slugs st-mary-rutherford-nj and st-mary-church-rutherford-nj (404)
  checked: '2026-11-05'
  outcome: found
bulletin_status: available
---

## Publisher

The parish's bulletin is printed by Bon Venture Services and posted on its sponsors page http://sponsors.bonventure.net/?page=1558 (headed '91 Home Avenue • Rutherford, NJ 07070'), which the 13 May 2026 Wayback capture of the parish homepage links as 'Bulletin'. I read the 8 November 2026 issue (pdfs/1558/2026-11-08.pdf, 12 pages, text layer) on 2026-11-05: page 4 masthead 'CHURCH OF SAINT MARY 91 HOME AVENUE RUTHERFORD, NEW JERSEY 07070', one Mass schedule, 'Rev. Charles Pinyan ... Pastor', footer '002D (CK) - St. Mary's, Rutherford ... BON VENTURE SERVICES, LLC'. A ParishesOnline org (st-mary-church-07070, lpi 0018000000QxAALAA3) exists for this address but carries no publications, so it is an old account, not this bulletin; its ids are left out of `publication`.

## Worship sites

One church, `st-mary-rutherford`. The 8 November 2026 schedule (page 4) gives Saturday 5:00 pm, Sunday 8:00, 10:00 and 12:00 noon and Monday-Friday 8:30 am, naming no other place. The archdiocese directory (182) and GCatholic (18550) list only this church.

## Website and bulletin provider

The website is the directory's (and GCatholic's) https://www.stmaryrutherford.org/, a WordPress site behind Cloudflare that refused every load on 2026-11-03 and again on 2026-11-05 (visit.py BLOCKED). The bulletin is read from Bon Venture: provider `other`, `page-pdfs` on the sponsors page over http (its https certificate doesn't verify), as for the archdiocese's other Bon Venture parishes.

Fetch check (2026-11-05, headed): ok, `page-pdfs on http://sponsors.bonventure.net/?page=1558: current`, picked pdfs/1558/2026-11-08.pdf, the 8 November 2026 issue read above.

## Not yet confirmed

The parish site itself has not been read live (research); the Wayback capture of 13 May 2026 and the bulletin are the sources.
