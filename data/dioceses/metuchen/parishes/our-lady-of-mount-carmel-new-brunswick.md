---
name: Our Lady of Mount Carmel
website: https://www.olmtcarmelonline.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://www.olmtcarmelonline.com/
  seen: 2026-11-03
  quote: Fotos de la Fiesta de Ntra. Señora del Carmen 2026
  note: 'The parish''s Spanish-language WordPress site (ChurchDev.com theme), read with probe get and
    visit.py: menu items La Parroquia, Personal, Album de Fotos, Grupos, Voluntariados, Catequesis, Sacramentos,
    Calendario, Lista de Eventos, Contactos, Donaciones; no Bulletin/Boletín item, no PDF links, no Mass
    schedule. The WordPress pages API lists 20 pages, none a bulletin or Mass-times page, and the media
    API returns no PDF.'
- url: https://www.parishesonline.com/organization/our-lady-of-mount-carmel-church-08901
  seen: 2026-11-03
  note: 'probe po: organization ''Our Lady of Mount Carmel Church'', 75 Morris St, New Brunswick, lpi:0018000000QxA3rAAF,
    website olmtcarmelonline.com; ''no publications: this organization does not publish a bulletin here
    now''.'
- url: https://discovermass.com/church/our-lady-of-mt-carmel-spanish-new-brunswick-nj/
  seen: 2026-11-03
  quote: There are currently no bulletins available for Our Lady of Mt. Carmel [Spanish].
  note: Discover Mass church page, 75 Morris St.; lists Mass times (Saturday 8:00am, Sunday 8:00am, weekdays
    7:00am, all Spanish) under an old COVID-19 notice, so not used as the schedule.
- url: https://diometuchen.org/parishfinder
  seen: 2026-11-03
  note: 'Parish finder: Our Lady of Mount Carmel, 75 Morris Street, New Brunswick, NJ 08901-2549, website
    olmtcarmelonline.com; ''Pastor: Rev. Raymond L. Nacarino | Parochial Vicars: Rev. Bonfilio Enriquez,
    SJCP; Rev. Manuel Lorente … Reconciliation: One half hour before every Mass''. No Mass times and no
    worship-site list.'
revisit: 'Look again for a bulletin: the parish site''s menu, the ParishesOnline org our-lady-of-mount-carmel-church-08901
  and the Discover Mass church page; if one appears, set the provider and read its masthead and Mass schedule.'
revisit_after: 2027-05-01
research:
- method: Parish site (probe get, visit.py --links/--text, WordPress pages and media APIs) for a bulletin
    page or PDF
  url: https://www.olmtcarmelonline.com/
  checked: '2026-11-03'
  outcome: not-found
  next_action: Re-read the site's menu for a Boletín/Bulletin item or PDF links
  retry_when: The site adds a bulletin or Mass-times page, or after 2027-05-01
- method: probe po on the ParishesOnline org slug; Discover Mass church page
  url: https://www.parishesonline.com/organization/our-lady-of-mount-carmel-church-08901
  checked: '2026-11-03'
  outcome: not-found
  next_action: probe po our-lady-of-mount-carmel-church-08901 and reload the Discover Mass church page
  retry_when: After 2027-05-01
- method: DuckDuckGo searches (via visit.py) in English and Spanish for the parish's bulletin; church-bulletin.org
    and Bon Venture hits were other parishes (Jersey City, Joliet container 01/0686, Nutley)
  checked: '2026-11-03'
  outcome: not-found
  next_action: Search 'Our Lady of Mount Carmel New Brunswick boletín' again and ask whether the parish's
    Facebook page posts a bulletin
  retry_when: After 2027-05-01
bulletin_status: not-found
---

## Publisher

No bulletin found. Our Lady of Mount Carmel, 75 Morris Street, New Brunswick, is a Spanish-language parish with an active website (2026 content: 'Fotos de la Fiesta de Ntra. Señora del Carmen 2026', the 2026 Bishop's Annual Appeal, 2026-2027 catechesis registration), but on 2026-11-03 the site had no bulletin item, no PDF and no Mass schedule; its ParishesOnline organization has no publications; its Discover Mass page says 'There are currently no bulletins available'. Searches found only other Mount Carmel parishes' bulletins. The row is `no_bulletin` (kept in the records, off the site) until a bulletin turns up. Pastor per the finder: Rev. Raymond L. Nacarino (no masthead to check it against).

## Worship sites

One church, Our Lady of Mount Carmel, 75 Morris Street (directory:24512, gcatholic:18621). The finder gives no other worship site and GCatholic lists no other church for the parish.

## Website and bulletin provider

Website https://www.olmtcarmelonline.com/ (WordPress, ChurchDev.com; `probe url` reported DEAD-DNS, but `probe get` and the browser load it). Provider `no_bulletin`, `bulletin_status` not-found; see `research`.

## Not yet confirmed

Whether the parish prints a paper bulletin that is not posted online, or posts one on Facebook. Mass times are not published by the parish online; the Discover Mass times are stale-looking. Revisit after 2027-05-01.
