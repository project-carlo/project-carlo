---
name: St. Augustine - Our Lady of Victory, Bronx
website: https://www.saolv.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: St. Augustine - Our Lady of Victory
evidence:
- url: https://www.saolv.org/
  seen: 2026-11-08
  quote: 'Sunday​ English : 9:45 AM Spanish : 12:30 PM'
  note: 'Parish (Wix) home page read in headed Chrome: Mass schedule and the address 1512 Webster Ave.
    Bronx, NY 10457. No bulletin link anywhere in its menu (Home, About, Sacraments, Ministries, Staff,
    News & Events, Offerings, Contact).'
- url: https://www.saolv.org/news-and-events
  seen: 2026-11-08
  quote: Pilgrimage to Our Lady of La Salette Shrine
  note: News & Events carries two event posts and no bulletin or PDF.
research:
- method: visit.py --bulletin and --links on saolv.org and its News & Events page
  url: https://www.saolv.org/
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-read the site menu for a Bulletin page
  retry_when: The site adds a bulletin page or PDF link
  revisit_after: 2027-02-01
- method: 'probe po our-lady-of-victory-church-10457 (ParishesOnline org exists: ''Our Lady of Victory
    Church, 1512 Webster Ave'')'
  url: https://parishesonline.com/organization/our-lady-of-victory-church-10457
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-run probe po; a publication there would be the bulletin
  retry_when: The org lists publications
- method: Discover Mass church slug our-lady-of-victory-bronx-ny
  url: https://discovermass.com/church/our-lady-of-victory-bronx-ny/
  checked: '2026-11-08'
  outcome: not-found
  next_action: None
  retry_when: The parish site links Discover Mass
bulletin_status: not-found
---

## Publisher

St. Augustine - Our Lady of Victory worships at 1512 Webster Avenue. No bulletin was found on 8 November 2026: the parish's Wix site has no bulletin page or PDF, ParishesOnline has a directory org for the church with no publications, and Discover Mass has no listing. The row is `no_bulletin` and kept off the site (Settled policy 4); see `research` for what would change that.

## Worship sites

One church, Our Lady of Victory, 1512 Webster Ave, with Sunday 9:45 AM (English) and 12:30 PM (Spanish) and daily Masses per the home page. The old St. Augustine church (1183 Franklin Ave) is excluded as closed (`excluded/st-augustine-bronx-16150`).

## Website and bulletin provider

`no_bulletin`; website is the parish home page.

## Not yet confirmed

Whether the parish prints a paper bulletin that is not posted online.
