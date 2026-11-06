---
name: St. John, Orange
website: http://stjohnscatholicchurch.net/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:st-john-church-07050', 'lpi:0018000000QxAACAA3']
group: ''
evidence:
- url: http://stjohnscatholicchurch.net/bulletins/
  seen: 2026-11-04
  quote: 94 Ridge Street | Orange, NJ 07050
  note: 'The site''s Bulletins page holds only a heading and the contact line, no file or embed: probe
    get, the WordPress pages API (content of slug ''bulletins'') and visit.py --bulletin (rendered, no
    pdf_links) all agree.'
- url: http://stjohnscatholicchurch.net/wp-json/wp/v2/media?per_page=30
  seen: 2026-11-04
  note: The media library holds only images uploaded in May 2020; the PDF filter returns an empty list.
- url: https://parishesonline.com/organization/st-john-church-07050
  seen: 2026-11-04
  note: 'probe po: org ''St. John Church'', 94 Ridge St, Orange, NJ 07050, website stjohnscatholicchurch.net,
    lpi 0018000000QxAACAA3, no publications (''this organization does not publish a bulletin here now'').'
revisit: Reread http://stjohnscatholicchurch.net/bulletins/ (empty on 2026-11-04) for posted issues.
revisit_after: 2027-02-04
research:
- method: probe get, WordPress REST (pages, media) and visit.py --bulletin on the parish site
  url: http://stjohnscatholicchurch.net/bulletins/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Reread the Bulletins page and the media list; if issues appear, set the provider from their
    host and run fetch:check
  retry_when: The Bulletins page links a file or a publisher
  revisit_after: 2027-02-04
- method: probe po on the ParishesOnline org; John Patrick scans (029-map jp-*.tsv) grepped for Orange
    and 07050
  url: https://parishesonline.com/organization/st-john-church-07050
  checked: '2026-11-04'
  outcome: not-found
  next_action: Recheck only if the parish names a publisher
  retry_when: The parish site links a publisher
bulletin_status: not-found
---

## Publisher

No bulletin found online. The parish site has a Bulletins page, but on 4 November 2026 it held only the heading and the contact line "St. John Church | 94 Ridge Street | Orange, NJ 07050": no file, link or embed in the served HTML, the WordPress page content or the rendered page (visit.py). The site's media library has only 2020 images. The ParishesOnline org st-john-church-07050 exists with no publications, and the Run's John Patrick scans list nothing in Orange (07050).

The earlier lead asked whether St. John shares a bulletin with Orange's Our Lady of Mount Carmel or Our Lady of the Valley (batch h-orange). Nothing on St. John's site names either; it prints its own Mass schedule for St. John alone and posts no bulletin, so there is nothing to share.

## Worship sites

One church, `st-john-orange`. The Mass and Confession page lists the Masses without naming another place, and the directory (162) and GCatholic (18530) each list only this church. The site's Eucharistic Adoration Chapel page describes adoration sign-ups, not Mass.

## Website and bulletin provider

The website is the parish's own http://stjohnscatholicchurch.net/ (the directory's and ParishesOnline's URL). The provider is `no_bulletin` (Settled policy 4), with `bulletin_status: not-found`. No fetch check was run, since there is no bulletin source.

## Not yet confirmed

- Whether the parish prints a paper bulletin it doesn't post. Next step: `revisit` from 2027-02-04.
