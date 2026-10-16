---
name: Mary, Mother of God Parish
website: https://www.marymotherofgodparish.org
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1884
publication: ['url:http://sponsors.bonventure.net/?page=1884']
group: Mary, Mother of God Parish
evidence:
- url: http://sponsors.bonventure.net/pdfs/1884/2026-10-18.pdf
  seen: 2026-10-16
  quote: Mary, Mother of God Parish Office 316 William Street, Scranton, PA 18508 Holy Rosary Church 316
    William Street, Scranton, PA 18508 Holy Rosary Center West Market Street, Scranton, PA 18508
  note: 'Page 1 (cover) of the 18 October 2026 issue, after the "Mass Schedule": Saturday 4:00 pm, Sunday
    7:15, 8:30 and 11:00 am, and confession Saturday 3:15 pm. Then two cemeteries. Page 2 lists the week''s
    Masses (weekdays 8:00 am).'
- url: http://sponsors.bonventure.net/?page=1884
  seen: 2026-10-16
  quote: Mary, Mother of God Parish 316 William Street • Scranton, PA 18508
  note: Bon Venture's "Our Sponsors" page for the parish; "Click to View Current Bulletin" links pdfs/1884/2026-10-18.pdf,
    with weekly back issues in a drop-down.
- url: https://www.marymotherofgodparish.org/
  seen: 2026-10-16
  note: 'The parish site answers 403 to curl and to the headless browser (net::ERR_HTTP_RESPONSE_CODE_FAILURE).
    Read through WebFetch only to find links: its "Sunday Bulletin" link is http://sponsors.bonventure.net/?page=1884,
    and it gives "Monday - Friday: 8:00 a.m. Saturday: 4:00 p.m. Sunday: 7:15 a.m. - 8:30 a.m. - 11:00
    a.m." Not quoted, since it was not read directly.'
---

## Publisher

Mary, Mother of God Parish (North Scranton) publishes its own weekly bulletin, printed by Bon
Venture Services and posted on Bon Venture's sponsors site (page id 1884). The 18 October
2026 issue, up on 16 October, is the parish's alone: its cover gives the Mass schedule
(Saturday 4 pm, Sunday 7:15, 8:30 and 11 am) and lists the parish office, Holy Rosary Church
and Holy Rosary Center (a hall on West Market Street) and two cemeteries; page 2 lists Masses
daily at 8 am. No other parish shares it.

## Worship sites

One: Holy Rosary Church, 316 William Street (`holy-rosary-scranton`), the finder's only
worship site for this parish. Holy Rosary Center and the cemeteries are not worship sites.

## Website and bulletin provider

marymotherofgodparish.org is the parish's site (finder, bulletin cover), but it refuses
automated readers (403 to curl and to Chrome here). A WebFetch read showed its "Sunday
Bulletin" link goes to Bon Venture page 1884, which links the current PDF (a text PDF). The
row is `other`, pinned with the recipe `page-pdfs http://sponsors.bonventure.net/?page=1884`
so the fetcher never needs the blocked parish site. The recipe was written by hand;
`fetch:check` reads only promoted rows.

## Not yet confirmed

Whether `fetch:check` picks the current issue with this recipe after promotion.
