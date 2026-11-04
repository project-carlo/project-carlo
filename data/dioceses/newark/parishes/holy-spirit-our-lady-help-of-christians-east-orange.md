---
name: Holy Spirit and Our Lady Help of Christians, East Orange
website: https://www.holyspiritandolhc.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Planning Area H
evidence:
- url: https://www.holyspiritandolhc.org/
  seen: 2026-11-04
  note: 'Down: probe url on https://www.holyspiritandolhc.org/ failed the TLS handshake (UNREACHABLE)
    and visit.py reported ERROR; http://holyspiritandolhc.org answered Cloudflare ''Error 1001 DNS resolution
    error'' (HTTP 409).'
- url: http://web.archive.org/web/20240912141110/https://www.holyspiritandolhc.org/
  seen: 2026-11-04
  quote: Corner of N. Clinton St and MLK Blvd., East Orange, NJ 07017
  note: 'The 12 September 2024 Wayback copy (quick_snap.py): menu Home, Calendar of Activities, Sacraments,
    Ministries, Gallery, Contact Us; Mass Saturday 6:00 pm (Creole), Sunday 9:00 am (English) and 11:30
    am (Creole), Monday-Saturday 7:00 am; pastor Rev. Jean Max Osias. No bulletin link or publisher.'
- url: https://rcan.org/sacramental-records/
  seen: 2026-11-03
  note: The closed-or-merged parishes table (scratch/newark-map-1/tools/rcan-closed-merged-2025-05.tsv)
    lists 'Our Lady Help of Christians, East Orange, Merged' and 'Holy Spirit, Orange, Merged', records
    at 'Holy Spirit-Help of Christians, East Orange'.
revisit: Reload https://www.holyspiritandolhc.org/ (down 2026-11-04) for a bulletin and a current Mass
  schedule.
revisit_after: 2027-02-04
research:
- method: 'probe url, visit.py and the Wayback copy of the parish site; ParishesOnline slug guesses (holy-spirit-church-07017,
    our-lady-help-of-christians-church-07017, holy-spirit-our-lady-help-of-christians-07017 and two more:
    none exist); John Patrick scans grepped for East Orange and 07017'
  url: https://www.holyspiritandolhc.org/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Reload the parish site and look for a bulletin page; otherwise check the archdiocese directory
    card for a new website
  retry_when: holyspiritandolhc.org loads again or the directory gives a website
  revisit_after: 2027-02-04
- method: Rosters and the 2024 site read for the merged parishes' second church
  url: https://rcan.org/sacramental-records/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Find which building (Holy Spirit's in Orange or Our Lady Help of Christians') the merged
    parish still uses besides 17 North Clinton Street, and record the other as excluded closed with a
    dated source
  retry_when: A parish or archdiocesan source names the former church building and its status
bulletin_status: not-found
---

## Publisher

No bulletin found. The parish's site https://www.holyspiritandolhc.org/ was down on 4 November 2026 (a TLS failure on www, Cloudflare "DNS resolution error" on the bare domain). Its last Wayback copy, 12 September 2024, shows a menu of Home, Calendar of Activities, Sacraments, Ministries, Gallery and Contact Us, Mass times and the pastor, Rev. Jean Max Osias, but no bulletin link or publisher. No ParishesOnline org exists under the slugs I tried, and the Run's John Patrick scans list nothing in East Orange. The archdiocese's directory card gives no website.

## Worship sites

One church, `holy-spirit-our-lady-help-of-christians-east-orange`, at 17 North Clinton Street (the directory's 25 and GCatholic's 18382, the 2024 site's "Corner of N. Clinton St and MLK Blvd."). The 2024 site gives one schedule with no other place. The parish joins Holy Spirit (Orange) and Our Lady Help of Christians (East Orange), both "Merged" in the archdiocese's records table; neither roster lists a second building, and I found no source on the other former church, so it has no record yet (see `research`).

## Website and bulletin provider

The website is the parish's own domain, the only one any source gives, though it is down. The provider is `no_bulletin` (Settled policy 4), `bulletin_status: not-found`. No fetch check was run.

## Not yet confirmed

- A bulletin, if the site returns: see `revisit`, from 2027-02-04.
- Which former church the merged parish no longer uses, and whether it still holds Mass: see `research`.
