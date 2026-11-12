---
name: St. Patrick & Assumption/All Saints, Jersey City
website: https://stpaasjc.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://stpaasjc.org/']
group: ''
evidence:
- url: https://stpaasjc.org/wp-content/uploads/2026/04/April-5-2025.pdf
  seen: 2026-11-03
  note: 'Newest bulletin on the parish site (file named April-5-2025 but dated inside ''SUNDAY, APRIL
    5, 2026 | THE RESURRECTION OF THE LORD | YEAR A''), 3 pages, self-produced, no publisher footer; read
    as screenshots in Chrome (parish-site-access visit.py; the host refuses the probe proxy). Page 1 masthead
    ''SAINT PATRICK AND ASSUMPTION/ALL SAINTS''; Liturgical schedule: weekday Masses Monday through Saturday
    9:00 AM at Assumption/All Saints Church; Sunday Masses at Saint Patrick''s Church from 7 December
    2025 to 31 May 2026, 9:30 AM English, 11:30 AM Spanish, 1:00 PM French/Creole, 10:00 AM last Sunday
    Swahili. Contact: St. Patrick / Rectory 492 Bramhall Avenue; Assumption All Saints 344 Pacific Avenue.
    Page 2: pastor Rev. Marc-Arthur Francois.'
- url: https://stpaasjc.org/
  seen: 2026-11-03
  note: 'WordPress site (My Town Website Development), read with visit.py: ''Eucharist is celebrated at
    St. Patrick and Assumption churches.'' Bulletins are posts titled by Sunday with a PDF download; the
    newest is ''Sunday, April 6, 2026'' (stpaasjc.org/sunday-april-6-2026/), the others January-March
    2026.'
- url: https://discovermass.com/church/st-patrick-jersey-city-nj/
  seen: 2026-11-03
  quote: There are currently no bulletins available for St. Patrick.
  note: Discover Mass listing gives https://stpaasjc.org as the parish website; no bulletins.
revisit: Look for a bulletin post newer than 'Sunday, April 6, 2026' on stpaasjc.org (visit.py; the proxy
  can't reach the host) or another channel; if one appears, record provider other with page-pdfs on the
  post list and run fetch:check headed
revisit_after: 2027-01-15
research:
- method: 'Parish website stpaasjc.org read with visit.py (probe get and probe url get ''Remote end closed
    connection'' through the proxy): bulletin posts list and the newest PDF'
  url: https://stpaasjc.org/sunday-april-6-2026/
  checked: '2026-11-03'
  outcome: not-found
  next_action: Check the post list for a new bulletin with visit.py; ask the parish ((201) 332-8600) where
    the weekly bulletin is posted now
  retry_when: A bulletin post newer than 6 April 2026 appears, or a parish social page posting bulletins
    is found
  revisit_after: 2027-01-15
- method: 'Publisher listings: probe po on seven guessed ParishesOnline slugs (st-patrick-church-07304,
    st-patrick-assumption-all-saints-07304 and variants: no org); John Patrick church-bulletin.org ids
    1-1100 and 6000-6400 (scans in scratch/newark-map-1/*-map/jp-*.tsv: no 07304 listing for this parish);
    Discover Mass st-patrick-jersey-city-nj (no bulletins)'
  checked: '2026-11-03'
  outcome: not-found
  next_action: Read the publisher from a current bulletin once one is found, then set the provider and
    run fetch:check
  retry_when: A current bulletin is found
bulletin_status: not-found
---

## Publisher

St. Patrick & Assumption/All Saints, Jersey City produces its own bulletin (no publisher footer) and posts it on its WordPress site stpaasjc.org as one post per Sunday with a PDF download. The newest post is 'Sunday, April 6, 2026', whose PDF (named April-5-2025.pdf) is dated inside 'SUNDAY, APRIL 5, 2026 | THE RESURRECTION OF THE LORD | YEAR A'; I read it as screenshots in Chrome (visit.py), since the host refuses the probe proxy. Its masthead is 'SAINT PATRICK AND ASSUMPTION/ALL SAINTS', with Rev. Marc-Arthur Francois as pastor, and one schedule covering both churches. No issue after Easter 2026 was found, so the row is `no_bulletin` (Settled policy 4) until a current one turns up.

## Worship sites

- St. Patrick, 492 Bramhall Avenue (`st-patrick-jersey-city`): Sunday 9:30 AM English, 11:30 AM Spanish, 1:00 PM French/Creole, 10:00 AM last Sunday Swahili (schedule for 7 December 2025 to 31 May 2026).
- Assumption/All Saints, 344 Pacific Avenue (`assumption-all-saints-jersey-city`): Monday to Saturday 9:00 AM.

Both from the 5 April 2026 bulletin; the site's home page says 'Eucharist is celebrated at St. Patrick and Assumption churches.' The directory (81) lists the parish at 492 Bramhall Ave.; GCatholic lists both churches (18455, 18436). The archdiocese's records table lists Assumption of the Blessed Virgin Mary (Slovak) as merged into All Saints and All Saints as merged into Assumption/All Saints: those are parish mergers, and the Assumption building still holds the weekday Masses.

## Website and bulletin provider

The directory's card for this parish has a broken website link (its href is the parish's name). GCatholic's link stpats-school.org/parish/ is now a parked domain (a script redirecting to /lander). Discover Mass gives https://stpaasjc.org, the site in use. `probe url` and `probe get` report 'Remote end closed connection' for it through the proxy; visit.py loads it. Provider `no_bulletin`: the newest bulletin is seven months old. If a current one appears, the post list on the home page would read with `page-pdfs`, but the host may refuse the fetcher too, which would need a `fetch_gap`.

Fetch check (2026-11-03): not run on a bulletin; it answers 'no_bulletin, so there is nothing to fetch'.

## Not yet confirmed

Whether the parish still publishes a weekly bulletin anywhere after Easter 2026, and the Sunday schedule after 31 May 2026 (the site's Liturgical Schedule page still gives the 2024-25 winter and a June-November summer schedule: 9:00 AM English, 11:00 AM Spanish, 12:30 PM French/Creole). See `research`.
