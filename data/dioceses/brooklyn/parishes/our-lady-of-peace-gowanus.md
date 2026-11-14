---
name: Our Lady of Peace (Gowanus)
website: https://ourladyofpeace-brooklyn.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://ourladyofpeace-brooklyn.org/bulletins']
group: Deanery B4 (Brooklyn West)
evidence:
- url: https://ourladyofpeace-brooklyn.org/bulletins
  seen: 2026-11-06
  quote: Bulletin for Sunday, Jul 05, 2026
  note: 'Tilma bulletins page, newest card first: ''Bulletin for Sunday, Jul 05, 2026'', then Jun 28,
    Jun 21, Jun 14, Jun 07, May 24 ... No card after 5 July 2026; the homepage''s bulletin teaser shows
    the same four newest cards.'
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMDcvMDEvY3ppcmI2bHl4XzcwMzU3NS4wNzA1MjAyNl8xTlVFVk8ucGRmIl1d/703575.07052026%201NUEVO.pdf
  seen: 2026-11-06
  quote: 522 CARROLL STREET
  note: 'Newest posted issue, 5 July 2026 (2 pages, text, self-made: file named ''703575.07052026 1NUEVO.pdf'',
    no LPi, Paluch, John Patrick or Church Bulletin Inc. mark). Page 1 masthead ''Our Lady of Peace Church'',
    522 Carroll Street, Franciscan Friars & Sisters, pastor Rev. Orlando Ruiz, O.F.M.; MASS SCHEDULE for
    the one church. Page 2 ''Our Lady of Peace Brooklyn, N.Y FOURTEENTH SUNDAY IN ORDINARY TIME JULY 5,
    2026''.'
- url: https://parishesonline.com/organization/our-lady-of-peace-church-11215
  seen: 2026-11-06
  note: 'probe po: org ''Our Lady of Peace Church'', 522 Carroll St, Brooklyn 11215, has no issues (empty
    org, not a publication). Slugs our-lady-of-peace-11215 and our-lady-of-peace-brooklyn don''t exist;
    our-lady-of-peace-church is Minneapolis.'
- url: https://discovermass.com/church/our-lady-of-peace-brooklyn-ny/
  seen: 2026-11-06
  quote: Shucks! There are no bulletins available.
  note: Discover Mass page names ourladyofpeace-brooklyn.org as the parish website and lists no bulletins.
revisit: Check whether the Tilma /bulletins page has posted an issue newer than 5 July 2026 (or the parish's
  Facebook page posts bulletins); if current, set other with page-pdfs https://ourladyofpeace-brooklyn.org/bulletins
  and run fetch:check.
revisit_after: 2026-12-06
research:
- method: Read the Tilma /bulletins page and homepage; probe po our-lady-of-peace-church-11215 and slug
    variants; Discover Mass church page
  url: https://ourladyofpeace-brooklyn.org/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: Reread the /bulletins page for a card newer than 5 July 2026 and the parish Facebook page
    (facebook.com/olpbrooklyn) for posted bulletins; if the Tilma page is current again, set bulletin_provider
    other with recipe page-pdfs https://ourladyofpeace-brooklyn.org/bulletins and run fetch:check.
  retry_when: After 2026-12-06, or when the parish site shows a new bulletin card
  revisit_after: 2026-12-06
bulletin_status: not-found
---

## Publisher

The parish self-publishes a two-page weekly bulletin on its Tilma site, but the newest card on `/bulletins` (read 2026-11-06) is "Bulletin for Sunday, Jul 05, 2026": nothing has been posted for four months. I read that issue: page 1 masthead "Our Lady of Peace Church, 522 CARROLL STREET BROOKLYN, NY 11215-1030, FRANCISCAN FRIARS & SISTERS", pastor Rev. Orlando Ruiz, O.F.M.; page 2 "JULY 5, 2026". The file name prefix `703575` matches no publisher mark in the issue; it is the parish's own layout.

## Worship sites

One church, Our Lady of Peace, 522 Carroll Street; the 5 July issue's MASS SCHEDULE and the site's current Mass Times page name only it. The issue also names the Franciscan sisters' convent at 209 First Street, which is a residence, not a Mass site.

## Website and bulletin provider

`no_bulletin`, following the playbook's lesson for a months-stale Tilma page: `fetch:check` would still pass it (first-listed, freshness unknown) and pick the 5 July issue. Before recording this I checked ParishesOnline (`our-lady-of-peace-church-11215` exists with no issues) and Discover Mass ("no bulletins available"). When an issue is posted again, the row is `other` with recipe `page-pdfs https://ourladyofpeace-brooklyn.org/bulletins` (see research).

## Not yet confirmed

Whether the parish still prints a bulletin it no longer posts, or posts it on Facebook (facebook.com/olpbrooklyn, not read): recheck after 2026-12-06.
