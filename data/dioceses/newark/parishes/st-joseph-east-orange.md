---
name: St. Joseph, East Orange
website: https://stjosepheo.weconnect.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:st-joseph-church-07018', 'lpi:0018000000Qc1URAAZ']
group: ''
evidence:
- url: https://stjosepheo.weconnect.com/
  seen: 2026-11-04
  quote: Unfortunately, this site is temporarily unavailable.
  note: probe url and visit.py both got only this page (verdict NO-PARISH-WORDS). The Wayback CDX shows
    the site answering ~930-byte pages (this message) from 2024-06-27 on; the last full snapshot is 2023-06-09.
- url: http://web.archive.org/web/20230609103748/https://stjosepheo.weconnect.com/
  seen: 2026-11-04
  quote: 'Sunday: 8:00am, 9:30am (Spanish)'
  note: The June 2023 copy of the parish's LPi WeConnect site has Mass times, news and a link to the school,
    and no bulletin link or publication widget.
- url: https://parishesonline.com/organization/st-joseph-church-07018
  seen: 2026-11-04
  note: 'probe po: org ''St. Joseph Church'', 110 Telford St, East Orange, NJ 07018-1896, website stjosepheo.weconnect.com,
    lpi 0018000000Qc1URAAZ, no publications (''this organization does not publish a bulletin here now'').'
- url: https://stjosepheo.com/
  seen: 2026-11-04
  note: The parish school's eCatholic site (files.ecatholic.com/26621) links the parish only as https://stjosepheo.weconnect.com/;
    it posts no parish bulletin.
revisit: 'Look for a current St. Joseph, East Orange website or bulletin: the archdiocese directory''s
  card (no website on 2026-11-03), the school site stjosepheo.com, or a ParishesOnline issue under st-joseph-church-07018.'
revisit_after: 2027-02-04
research:
- method: probe url and visit.py on the parish's WeConnect site; Wayback CDX and the 2023-06-09 snapshot
  url: https://stjosepheo.weconnect.com/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Look for a new parish domain (rcan.org parish card, the school site's Parish link, a current
    bulletin's masthead) and read its bulletin page
  retry_when: The archdiocese directory or the school site links a new parish website
  revisit_after: 2027-02-04
- method: probe po on the ParishesOnline org; John Patrick scans (029-map jp-*.tsv) grepped for East Orange
    and 07018; domain guesses stjosepheastorange.org/.com, stjosepheo.org, saintjosepheastorange.org (DEAD-DNS)
  url: https://parishesonline.com/organization/st-joseph-church-07018
  checked: '2026-11-04'
  outcome: not-found
  next_action: Recheck only with a new lead to a publisher or site
  retry_when: A source names the parish's current website or printer
bulletin_status: not-found
---

## Publisher

No bulletin found. The parish's website, the LPi WeConnect site https://stjosepheo.weconnect.com/ that ParishesOnline and the parish school's site both link, answered only "Unfortunately, this site is temporarily unavailable." on 4 November 2026 (probe url and visit.py). The Wayback CDX shows it answering that page since 27 June 2024; its last full copy (9 June 2023) shows Mass times and news but no bulletin link or publication widget. The ParishesOnline org st-joseph-church-07018 exists with no publications, the Run's John Patrick scans list nothing in East Orange, and the domains I guessed don't resolve. The archdiocese's directory card gives no website. stjosepheo.com is the parish school's eCatholic site, not the parish's.

## Worship sites

One church, `st-joseph-east-orange`. The directory (24, English and Spanish) and GCatholic (18383) each list only this church at 110 Telford Street, and the 2023 site gave one schedule with no other place.

## Website and bulletin provider

The website is the WeConnect address the parish's own accounts still give, though it is down; there is no live alternative. The provider is `no_bulletin` (Settled policy 4), `bulletin_status: not-found`. No fetch check was run.

## Not yet confirmed

- A current website or bulletin and a current Mass schedule: see `revisit` and `research`, from 2027-02-04.
