---
name: Holy Spirit Parish
website: https://holyspiritrcparish.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:39636']
group: ''
evidence:
- url: https://www.romesentinel.com/news/route-20-catholic-churches-holy-spirit-parish-merger/article_66a992b3-2d7e-4d30-b659-9116c53bb9c1.html
  seen: 2026-09-25
  quote: The Most Rev. Douglas J. Lucia, bishop of Syracuse, issued a decree on Tuesday, June 16, ordering
    the merger. It became effective today, Wednesday, July 1, and the church of St. Mary will be the principal
    church, with parish offices at St. Bernard’s
  note: Names all four churches with addresses. The page's datePublished is 2026-06-18 (16 June and
    1 July fall on a Tuesday and a Wednesday in 2026, and also in 2020, which an earlier version of this
    record wrongly read the weekdays as). The same article says "The decree does not close any of the churches".
- url: https://www.wktv.com/news/local/multiple-catholic-parishes-merge-in-mohawk-valley/article_8af8d0af-8069-41b4-96b5-cf293c2ef26a.html
  seen: 2026-09-26
  quote: The churches of Saint Bernard, Saint Joseph, and Saint Joan of Arc will remain open as auxiliary
    churches for public worship.
  note: WKTV, published 2026-06-19 (datePublished). Reports the decree forming Holy Spirit parish
    "effective July 1", with its principal church at Saint Mary, 16 Wylie St., Hamilton.
- url: https://route20catholic.org
  seen: 2026-09-25
  note: '`probe url`: redirects to http://holyspiritrcparish.org/, i.e. the old shared site of the four
    churches now points at the merged parish.'
- url: https://parishesonline.com/organization/st-marys-church-13346
  seen: 2026-09-25
  note: '`probe po st-marys-church-13346`: a ParishesOnline organization for St. Mary''s, Hamilton (LPi
    id 0018000000Qx7RGAAZ, website route20catholic.org) that lists no issues, so the bulletin is not published
    there.'
- url: https://files.ecatholic.com/39636/bulletins/20260925.pdf
  seen: 2026-09-26
  quote: St. Bernard’s,    St. Joan of Arc,        St. Joseph,          St. Mary’s
  note: 'Bulletin for the 26th Sunday of Ordinary Time, 27 September 2026 (file dated Friday 25 September),
    page 1: masthead ''Waterville Morrisville Oriskany Falls Hamilton & The Newman Ministries of Colgate
    and Morrisville''; Mass schedule 4:00 pm Vigil St. Joan of Arc, 6:00 pm Vigil St. Joseph''s, 8:30
    am Sunday St. Bernard''s, 11:00 am Sunday St. Mary''s, 8:30 pm Sunday Colgate Chapel when in session.'
- url: https://holyspiritrcparish.org/bulletins
  seen: 2026-09-26
  note: behind Cloudflare; read in a browser (parish-site-access visit.py). The Bulletins page lists weekly
    PDFs on files.ecatholic.com/39636/bulletins/, newest 'September 25, 2026' (20260925.pdf), then 20260918,
    20260911, 20260904, 20260828... Files are named by the Friday before the Sunday. `visit.py --bulletin
    https://holyspiritrcparish.org` reported ecatholic:39636.
---

## Publisher

Holy Spirit is one canonical parish formed on 1 July 2026 by merging the four "Route 20" churches:
St. Mary's (Hamilton, the principal church), St. Bernard's (Waterville, parish offices),
St. Joseph's (Oriskany Falls) and St. Joan of Arc Mission (Morrisville), under a decree of
16 June 2026 (Rome Sentinel, 18 June 2026; WKTV, 19 June 2026: the other three "remain open as
auxiliary churches for public worship"). An earlier version of this record dated the merger to
2020 from the article's weekdays, which fit both years; both articles' publication dates say 2026. It publishes one weekly bulletin through eCatholic. I read the
issue for the 26th Sunday of Ordinary Time, 27 September 2026 (file 20260925.pdf): its page-1
masthead names the four churches "& The Newman Ministries of Colgate and Morrisville", and its Mass
schedule covers the four churches plus a Sunday-evening Mass in Colgate's chapel during term.

## Worship sites

Five, from the 27 September 2026 schedule:

- St. Joan of Arc, Morrisville (`churches/st-joan-of-arc-morrisville.md`): Sat 4:00 pm.
- St. Joseph's, Oriskany Falls (`churches/st-joseph-oriskany-falls.md`): Sat 6:00 pm.
- St. Bernard's, Waterville (`churches/st-bernard-waterville.md`): Sun 8:30 am, Mon/Wed 7:30 am.
- St. Mary's, Hamilton (`churches/st-mary-hamilton.md`): Sun 11:00 am, Tue/Thu 7:30 am.
- Colgate Memorial Chapel, Hamilton (`churches/colgate-memorial-chapel-hamilton.md`): Sun 8:30 pm
  when the university is in session. Not in either roster.

The diocese's page keeps the records of four closed parishes here: Immaculate Conception
(Hamilton), St. Ann Mission (Brookfield), St. Anthony Mission (Morrisville) and St. Mary Mission
(North Brookfield). Only North Brookfield is in a roster; it is `excluded/st-mary-north-brookfield.md`.
None of the four appears in the bulletin.

## Website and bulletin provider

holyspiritrcparish.org is an eCatholic site behind Cloudflare (route20catholic.org, the four
churches' earlier shared site, redirects to it). A real browser (parish-site-access `visit.py`,
2026-09-26) got through on the third load and reported eCatholic site id 39636; the Bulletins
page lists weekly PDFs at files.ecatholic.com/39636/bulletins/, which fetch without a browser.
So the provider is `ecatholic` with the site as `website`. The issues are named by the **Friday**
before the Sunday (20260925.pdf for 27 September), so `issues.py ecatholic ecatholic:39636`,
which probes Sunday dates, finds nothing; the pipeline's eCatholic reader should be checked
against this naming. The empty ParishesOnline organization for St. Mary's (`st-marys-church-13346`,
no issues) is not a channel.

## Not yet confirmed

Nothing. (The earlier revisit, read a current bulletin, is done.)
