---
name: Basilica of the Sacred Heart of Jesus
website: https://sacredheartbasilicasyr.org
bulletin_provider: parishes_online
provider_id: basilica-of-the-sacred-heart-of-jesus
publication: ['po-org:basilica-of-the-sacred-heart-of-jesus', 'lpi:0018000000Qc0EfAAJ', 'po-container:06/0194']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/06/0194/20260927B.pdf
  seen: 2026-09-26
  quote: THE BASILICA OF THE SACRED HEART OF JESUS 927 Park Avenue, Syracuse, NY 13204
  note: Masthead, page 1 of the 27 September 2026 issue. The basilica alone.
- url: https://container.parishesonline.com/bulletins/06/0194/20260927B.pdf
  seen: 2026-09-26
  quote: SUNDAY WORSHIP Saturday Vigil– 4:00 p.m. Sunday– 9:00 a.m. 11:00 a.m. (Bi-Lingual)
- url: https://parishesonline.com/organization/basilica-of-the-sacred-heart-of-jesus
  seen: 2026-09-26
  note: '`probe po`: 927 Park Avenue, LPi id 0018000000Qc0EfAAJ, container 06/0194, weekly issues through
    2026-09-27. Found by web search (site:parishesonline.com).'
---

## Publisher

The basilica publishes its own weekly bulletin through ParishesOnline (container 06/0194).
The 27 September 2026 issue's masthead is the basilica's alone, 927 Park Avenue, with
Saturday 4 pm and Sunday 9 am and 11 am (bilingual) Masses.

## Worship sites

One: the basilica (`basilica-sacred-heart-syracuse`). The diocese lists St. Stephen,
Syracuse as closed with its records here; that building is
`excluded/st-stephen-syracuse.md`.

## Website and bulletin provider

sacredheartbasilicasyr.org is the parish's site (named in the bulletin and on the diocese
page), but on 2026-09-26 it did not load: `probe url` got a connection reset and visit.py
and curl got HTTP 502 through the proxy on every try. The bulletin was found instead by a
web search of parishesonline.com, and `probe po` gives the organization, LPi id and
container. Since the provider is `parishes_online`, fetching goes by `provider_id` and does
not depend on the site.

## Not yet confirmed

Whether the parish site links this organization (it could not be loaded).
