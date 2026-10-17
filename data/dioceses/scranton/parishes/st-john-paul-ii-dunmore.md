---
name: St. John Paul II Parish
website: https://www.sjp2parish.com
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=9249
publication: ['url:http://sponsors.bonventure.net/?page=9249']
group: Saint John Paul II Parish
evidence:
- url: http://sponsors.bonventure.net/pdfs/9249/2026-10-11.pdf
  seen: 2026-10-16
  quote: MONDAY - FRIDAY 8:00 AM (St. Anthony’s Church) 12:00 NOON (St. Mary’s Church) SATURDAY 4:00 PM
    (St. Mary’s Church) 5:15 PM (St. Anthony’s Church)
  note: 'Page 1 (cover) of the 11 October 2026 issue: the parish Mass schedule, then the three church
    addresses (St. Anthony of Padua, 208 Smith St.; St. Mary of Mount Carmel, 322 Chestnut St.; St. Rocco,
    118 Kurtz St.). Sunday: 8:30 and 11:15 am St. Anthony''s, 10 am St. Mary''s. No Mass is scheduled
    at St. Rocco.'
- url: http://sponsors.bonventure.net/pdfs/9249/2026-10-11.pdf
  seen: 2026-10-16
  quote: St. Rocco Church 118 Kurtz Street Dunmore, PA 18510
  note: Page 1 lists St. Rocco among the parish's churches, after the Mass schedule, which names only
    St. Anthony's and St. Mary's.
- url: http://sponsors.bonventure.net/?page=9249
  seen: 2026-10-16
  quote: St. John Paul II Parish 303 Smith Street • Dunmore, PA 18512-2919
  note: 'Bon Venture Services'' "Our Sponsors" page for the parish: "Click to View Current Bulletin" links
    pdfs/9249/2026-10-11.pdf, and a drop-down lists weekly issues back through 2025. Reached from the
    "Bulletins" item in sjp2parish.com''s menu (a Google redirect to this page).'
- url: https://www.sjp2parish.com
  seen: 2026-10-16
  quote: 'Daily Mass: 8:00 a.m. Monday-Friday Daily Mass: 12 Noon Monday - Frida y Saturday: 5:15 p.m.
    Saturday : 4:00 p.m. Sunday: 8:30 a.m. and 11:15 a.m. Sunday: 10:00 a.m.'
  note: 'The parish''s Google Sites homepage: a two-column Mass schedule headed "St. Anthony of Padua
    Church" and "St. Mary of Mount Carmel Church" (columns run together in the text), the same times as
    the bulletin.'
promoted: 2026-10-17
---

## Publisher

St. John Paul II Parish in Dunmore publishes one weekly bulletin, printed by Bon Venture
Services and posted on Bon Venture's sponsors site (page id 9249). The 11 October 2026
issue's cover (page 1) gives one Mass schedule for the parish: weekdays 8 am at St.
Anthony's and noon at St. Mary's; Saturday 4 pm St. Mary's and 5:15 pm St. Anthony's;
Sunday 8:30 am and 11:15 am St. Anthony's and 10 am St. Mary's. It then lists three
churches: St. Anthony of Padua (208 Smith St.), St. Mary of Mount Carmel (322 Chestnut St.)
and St. Rocco (118 Kurtz St.). The parish was formed from Sts. Anthony & Rocco and Our Lady
of Mount Carmel ("This year, we gather as St. John Paul II parish —one truly united Catholic
community of Dunmore", pastor's column, 2 August 2026 issue); the finder lists it as one
canonical parish, and no other parish shares this bulletin.

## Worship sites

- `saint-anthony-of-padua-dunmore`: weekday 8 am, Saturday 5:15 pm, Sunday 8:30 and
  11:15 am.
- `saint-mary-of-mt-carmel-dunmore`: weekday noon, Saturday 4 pm, Sunday 10 am.

St. Rocco Church (122 Kurtz St. in the finder and GCatholic, 118 Kurtz St. in the bulletin)
is still listed as a parish church, but no Mass is scheduled there: the bulletin's schedule
names only St. Anthony's and St. Mary's, and the diocesan finder gives it no Mass times. The
parish holds one outdoor "Festival Mass (St. Rocco's Grounds)" a year during the Italian
festival (2 August 2026 issue, page 4), and the parish hall is used for meetings. It is
`excluded/saint-rocco-dunmore.md` (`no-public-mass`).

## Website and bulletin provider

sjp2parish.com is the parish's site (named in the bulletin and the diocesan finder). Its
"Bulletins" menu item is a Google redirect to http://sponsors.bonventure.net/?page=9249, Bon
Venture's page for the parish, where "Click to View Current Bulletin" links
`pdfs/9249/<YYYY-MM-DD>.pdf` (the Sunday's date) and a drop-down lists the past issues. The
issues are text PDFs (page 2's header is in an embedded font that extracts as garbage, the
rest reads). `bulletin_provider: other` with the recipe `page-pdfs
http://sponsors.bonventure.net/?page=9249` pins the collector to that page, whose only PDF
link is the current issue, dated in its file name. The recipe was written by hand from the
page's markup; `fetch:check` reads only promoted rows, so it has not been run on it yet.

## Not yet confirmed

Whether `fetch:check` picks the current issue with this recipe once the row is promoted (it
should: one dated PDF link). Bon Venture posts the issue on the Sunday's date; on Friday 16
October the newest was 11 October.
