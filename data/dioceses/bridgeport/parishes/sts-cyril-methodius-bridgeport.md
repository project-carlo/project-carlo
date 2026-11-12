---
name: Sts. Cyril & Methodius
website: https://institute-christ-king.org/bridgeport-bulletins
bulletin_provider: other
provider_id: page-pdfs https://institute-christ-king.org/bridgeport-bulletins filename=b*.pdf
publication: ['url:https://institute-christ-king.org/bridgeport-bulletins#sts-cyril-methodius-icksp']
group: ''
evidence:
- url: https://institute-christ-king.org/images/b11.8.2026_Resumed_Epiphany_V.pdf
  seen: 2026-11-12
  quote: 79 Church Street - Bridgeport, Connecticut 06608
  note: 'Page 1 masthead of the 8 November 2026 issue: ''Institute of Christ the King Sovereign Priest'',
    ''Church of Saints Cyril & Methodius'', Reverend Canon Francis X. Altiere IV, Pastor & Rector. Mass
    Times: Sunday 8:30 a.m. Low Mass, 10:15 a.m. High Mass; Monday-Friday 7:45 a.m.; Saturday 8:30 a.m.
    Names no other church; ''Mary'' does not occur on pages 1-2.'
- url: https://institute-christ-king.org/bridgeport-bulletins
  seen: 2026-11-12
  note: The Institute's Bridgeport bulletins page lists weekly PDFs newest first under /images/ (b11.8.2026_Resumed_Epiphany_V.pdf,
    b11.1.2026_All_Saints.pdf, b10.25.2026_Christ_the_King.pdf ...), with occasional flyers (/images/Holy_Week_2026_flyer.pdf).
bulletin_status: available
publication_reviews:
- parish: st-mary-bridgeport
  decision: separate
  evidence:
  - url: https://institute-christ-king.org/images/b11.8.2026_Resumed_Epiphany_V.pdf
    seen: 2026-11-12
    note: The 8 November 2026 masthead names the Church of Saints Cyril & Methodius alone, with Canon
      Altiere as rector and its own Latin Mass times.
  - url: https://stmarychurchbridgeport.org/wp-content/uploads/2026/11/11.08.2026-32th-Sunday-in-Ordinary-Time.pdf
    seen: 2026-11-12
    note: 'The 8 November 2026 St. Mary sheet is the bulletin for St. Mary: Fr. Rolando, Saturday 4:00pm
      and Sunday 8:30, 10:00, 11:30am Masses; it does not mention Sts. Cyril & Methodius.'
---

## Publisher

Sts. Cyril & Methodius, Bridgeport is an oratory of the Institute of Christ the King Sovereign Priest (ICKSP); the diocese lists it as a parish with Canon Francis Altiere as rector (directory:1329). It publishes its own weekly bulletin, posted on the Institute's site. The 8 November 2026 issue (`https://institute-christ-king.org/images/b11.8.2026_Resumed_Epiphany_V.pdf`, read 2026-11-12, text layer readable) has the masthead "Church of Saints Cyril & Methodius, 79 Church Street - Bridgeport, Connecticut 06608", names Canon Altiere as "Pastor & Rector", and gives Sunday 8:30 Low Mass and 10:15 High Mass, Monday-Friday 7:45 and Saturday 8:30.

## Worship sites

- `sts-cyril-methodius-bridgeport`: the church at 79 Church Street (directory:1329, GCatholic 21998), the only church in the masthead.

The directory also puts St. Mary (directory:1331) at 79 Church Street. That is not a shared site or bulletin: St. Mary's own site and GCatholic give 25 Sherman St., it has its own pastor (Fr. Rolando Torres) and its own bulletin with other Mass times, and this bulletin doesn't mention it (see `publication_reviews`). The directory's address for St. Mary is the error.

## Website and bulletin provider

Provider `other`, read from the Institute's Bridgeport bulletins page (`https://institute-christ-king.org/bridgeport-bulletins`), which lists the weekly PDFs newest first under `/images/b<m>.<d>.<yyyy>_<feast>.pdf`, mixed with occasional flyers. The publication id is that page in the `url:` form, as the Institute's site hosts other houses' pages too.

`fetch:check` on 2026-11-12 without a recipe failed: it followed the page's Facebook share link ("No PDF links found on bulletin page: https://www.facebook.com/sharer.php?u=..."). With the pinned recipe `page-pdfs https://institute-christ-king.org/bridgeport-bulletins filename=b*.pdf` (the filter skips the flyers, whose names don't start with `b`), it picked `https://institute-christ-king.org/images/b11.8.2026_Resumed_Epiphany_V.pdf`, the 8 November 2026 issue and the newest posted (age 4 days; identity unverified as reported, masthead checked by hand above).

## Not yet confirmed

Nothing open.
