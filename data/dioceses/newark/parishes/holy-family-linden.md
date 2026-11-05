---
name: Holy Family, Linden
website: https://holyfamilylinden.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Planning Area K
evidence:
- url: https://holyfamilylinden.org/
  seen: 2026-11-05
  note: 'Found by guessing the domain (neither the directory nor GCatholic gives a website). Title ''Holy
    Family Church – A Slovak – American Catholic Parish in Linden, New Jersey''; phone 908-862-1060 (the
    GCatholic number). probe url and visit.py: no bulletin link, no PDF and no publisher; menu only Mass
    and Confession, Gallery, About, Contact.'
- url: https://holyfamilylinden.org/mass-confession/
  seen: 2026-11-05
  note: 'Mass & Confession Schedule: Monday 7:00 PM Slovak; Tuesday and Wednesday 7:00 PM English; Thursday
    no Mass; Friday 7:00 PM Slovak; Saturday 4:00 PM (Vigil Mass) English; Sunday 9:30 AM Slovak, 11:30
    AM English; all ''at Holy Family Church''.'
- url: https://holyfamilylinden.org/wp-json/wp/v2/media?mime_type=application/pdf&per_page=20
  seen: 2026-11-05
  note: 'WordPress media API: [] (no PDF uploads).'
- url: http://web.archive.org/cdx/search/cdx?url=holyfamilylinden.org&matchType=prefix
  seen: 2026-11-05
  note: 76 captures, all from 2026-09-22 onward; none is a bulletin or a PDF.
- url: https://parishesonline.com/organization/holy-family-church-7036
  seen: 2026-11-05
  note: 'probe po: Holy Family Church, 210 Monroe St, Linden, New Jersey, 07036; lpi 0018000000Qbz1CAAR;
    no website; ''no publications: this organization does not publish a bulletin here now''. (holy-family-church-07036
    does not exist.)'
research:
- method: probe po on holy-family-church-7036 and -07036; John Patrick scans (029-map/jp-*.tsv, ids 1-1100
    and 6000-6400) grepped for Linden and 07036; parish site, its WordPress media API and Wayback CDX;
    domain guesses
  url: https://holyfamilylinden.org/
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reopen holyfamilylinden.org for a bulletin page and probe po holy-family-church-7036 for
    issues; ask whether the parish posts a bulletin on Facebook
  retry_when: The site adds a bulletin or news page, or the ParishesOnline org lists a publication
  revisit_after: 2027-02-01
bulletin_status: not-found
---

## Publisher

No bulletin found. Holy Family is a Slovak-American parish in Linden. Its site, holyfamilylinden.org (live since September 2026, by the Wayback CDX), has a Mass schedule but no bulletin, PDF or publisher link (probe url, visit.py and the WordPress media API, 2026-11-05). The ParishesOnline org `holy-family-church-7036` (LPi 0018000000Qbz1CAAR, 210 Monroe St) exists but lists no publications, and no John Patrick listing in the saved scans is in Linden or 07036. The LPi id stays in evidence, not `publication`, because the org carries no bulletin now.

## Worship sites

- Holy Family Church (`holy-family-linden`): Saturday 4:00 PM vigil (English); Sunday 9:30 AM (Slovak), 11:30 AM (English); Monday and Friday 7:00 PM (Slovak), Tuesday and Wednesday 7:00 PM (English) (parish site, 2026-11-05).

The directory (100) and GCatholic (18463) list only this church. The archdiocese's closed-parish records table places St. Joseph's (Slovak), Elizabeth's records here; that parish is not this batch's to record.

## Website and bulletin provider

`no_bulletin`, with the parish site as `website`, so the row and its church stay in the records but off the site (Settled policy 4). Its Facebook and Instagram links point at the bare facebook.com and instagram.com, so no social page was checked.

## Not yet confirmed

Whether the parish prints a paper bulletin it does not post. Research holds the recheck.
