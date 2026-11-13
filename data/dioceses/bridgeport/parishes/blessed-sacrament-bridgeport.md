---
name: Blessed Sacrament
website: https://www.blessedsacramentbpt.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://www.blessedsacramentbpt.org/
  seen: 2026-11-12
  quote: 4:00pm Spanish, 5:30pm English
  note: 'Home page (OSV / Duda site) Mass times: Saturday Vigil 4:00 pm Spanish, 5:30 pm English; Sunday
    8:30 am English, 10:00 am Spanish, 11:30 am English; Tuesday-Thursday 6:30 pm Spanish. The menu (Home,
    Parish Life, Financial Reports, Ministries, Religious Education, Summer Camp, Giving, About, Contact,
    Food Pantry, Mass Times, Location, Virtus) has no bulletin page.'
- url: https://www.blessedsacramentbpt.org/parish-life
  seen: 2026-11-12
  quote: you'll want to stay informed by regularly reading the weekly bulletin
  note: Template text from the OSV site; the page links no bulletin.
- url: https://discovermass.com/church/blessed-sacrament-bridgeport-ct/
  seen: 2026-11-12
  quote: There are currently no bulletins available for Blessed Sacrament.
  note: Discover Mass listing for Blessed Sacrament, 275 Union Ave., Bridgeport, CT 06607.
revisit: Look for a bulletin link on blessedsacramentbpt.org or a Discover Mass / ParishesOnline listing;
  if one appears, set the provider and run fetch:check.
revisit_after: 2027-05-01
research:
- method: probe get and parish-site-access visit.py --bulletin on the parish site; /bulletin and /bulletins
    tried
  url: https://www.blessedsacramentbpt.org/
  checked: '2026-11-12'
  outcome: not-found
  next_action: Re-read the site's menu for a bulletin page
  retry_when: The site adds a bulletin link, or by the revisit date
- method: probe po on guessed ParishesOnline slugs (blessed-sacrament-church-06607, blessed-sacrament-06607,
    blessed-sacrament-parish-06607, blessed-sacrament-catholic-church-06607, blessed-sacrament-roman-catholic-church-06607,
    church-of-the-blessed-sacrament-06607, blessed-sacrament-parish-bridgeport, blessed-sacrament-church-bridgeport)
  checked: '2026-11-12'
  outcome: not-found
  next_action: Search ParishesOnline for the parish by name in a browser
  retry_when: A ParishesOnline or LPi id appears on the parish site or another source
- method: Discover Mass church page bulletins tab
  url: https://discovermass.com/church/blessed-sacrament-bridgeport-ct/
  checked: '2026-11-12'
  outcome: not-found
  next_action: Re-check the Bulletins tab
  retry_when: By the revisit date
bulletin_status: not-found
---

## Publisher

No bulletin found. The parish's own site (`blessedsacramentbpt.org`, an OSV-built Duda site) gives Mass times on its home page but links no bulletin; its Parish Life page carries template text about "the weekly bulletin" with no link (read 2026-11-12). The Discover Mass listing says "There are currently no bulletins available for Blessed Sacrament." No ParishesOnline org matched the slugs tried, and the diocese's parish page links no bulletin. See research.

## Worship sites

- `blessed-sacrament-bridgeport`: the one church, 275 Union Avenue (directory:1316, GCatholic 21990). The site, the directory and GCatholic name no other church.

## Website and bulletin provider

`no_bulletin`: kept in the records, off the site (Settled policy 4), until a bulletin turns up. The website is kept as the parish's own site.

## Not yet confirmed

Whether the parish posts a bulletin anywhere else, such as Facebook (`facebook.com/BlessedSacramentChurchRC`, not read: it needs a login). Revisit after 2027-05-01.
