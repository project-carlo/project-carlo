---
name: Saints Peter and Paul Parish
website: https://peterandpaulchurch.com/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1572
publication: ['url:http://sponsors.bonventure.net/?page=1572']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/1572/2026-10-18.pdf
  seen: 2026-10-18
  quote: The Catholic Presence in Lehighton since 1850 + Established as a Parish in 1885
  note: 'Page 1 of the 18 October 2026 issue (8 pages, text PDF), under the masthead "SAINTS PETER & PAUL PARISH" (its letters are spaced, so not quoted): "260 NORTH THIRD STREET • LEHIGHTON,
    PENNSYLVANIA 18235", "Saturday Vigil … 4:00 pm Sunday … 7:45 & 10:00 am Daily Mass - M/T/Th/F … 8:00
    am", "Rev. Philip J. Maas … Parochial Administrator". Page 3 lists the intentions, all at one church.'
- url: http://sponsors.bonventure.net/?page=1572
  seen: 2026-10-18
  quote: Saints Peter & Paul Parish 260 North Third Street • Lehighton, PA 18235
  note: Bon Venture Services' sponsor page for the parish; "Click to View Current Bulletin" and "Previous
    bulletins" from October 18, 2026 back to January 2026 at pdfs/1572/YYYY-MM-DD.pdf.
- url: https://peterandpaulchurch.com/
  seen: 2026-10-18
  note: 'Read with a fetch tool (the sandbox gets a connection reset from this GoDaddy-hosted site, in curl
    and in Chrome): the menu item "Bulletins" and the link "Click here for the weekly parish bulletin"
    both go to sponsors.bonventure.net/?page=1572. The home page gives "Saturdays: 4:00 pm Sundays: 7:45
    and 10:00 am".'
---

## Publisher

Saints Peter and Paul Parish, Lehighton, publishes its own weekly bulletin through Bon
Venture Services. I read the 18 October 2026 issue: page 1 is the parish's masthead (260
North Third Street, Lehighton) with one schedule (Saturday 4:00 pm, Sunday 7:45 and 10:00
am, Monday, Tuesday, Thursday, Friday 8:00 am). One church, one bulletin.

## Worship sites

- `sts-peter-and-paul-lehighton`, the only building the bulletin, the diocesan map and
  GCatholic name.

Nothing ruled out.

## Website and bulletin provider

peterandpaulchurch.com (GoDaddy Website Builder) links its bulletin to Bon Venture's sponsor
page 1572, which lists one PDF per Sunday. The sandbox cannot connect to the parish site
(connection reset; the plain-http address answers 308 to https, which then resets), so its
links were read with a fetch tool. The `page-pdfs` recipe pins the Bon Venture page, as for
the Bon Venture parishes in Scranton; it is served over `http://` because Bon Venture's https
certificate chain is broken (Scranton diocese.md).

Fetch check (2026-10-18): resolved; the pinned `page-pdfs` recipe picked `pdfs/1572/2026-10-18.pdf` (current).

## Not yet confirmed

Nothing. The diocesan map still names Rev. Christopher M. Zelonis as pastor; the 18 October
bulletin names Rev. Philip J. Maas as parochial administrator.
