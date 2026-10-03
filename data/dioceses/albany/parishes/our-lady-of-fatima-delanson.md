---
name: Our Lady of Fatima
website: http://parishes.rcda.org/OurLadyOfFatima/
bulletin_provider: other
provider_id: page-pdfs http://parishes.rcda.org/OurLadyOfFatima/bulletin.php
publication: ['url:http://parishes.rcda.org/OurLadyOfFatima/bulletin.php']
group: Schoharie County Cluster
evidence:
- url: http://parishes.rcda.org/OurLadyOfFatima/bulletins/2026/September_20.pdf
  seen: 2026-09-28
  quote: Our Lady Of Fatima P. O. Box 219 (1735 Alexander Road) Delanson, NY 12053
  note: Page 1 of the 20 September 2026 issue (the latest posted on 2026-09-28; September_27.pdf answered
    404). The masthead also carries Our Lady of the Valley, Middleburgh's contact box and Mass times,
    as a cluster courtesy.
- url: http://parishes.rcda.org/OurLadyOfFatima/bulletins/2026/September_20.pdf
  seen: 2026-09-28
  quote: September 27 - 11:15 am
  note: 'Page 2 ''Liturgy Schedule'' lists only Our Lady of Fatima intentions: Sat 4 pm, Sun 11:15 am,
    Tue 9 am.'
- url: http://parishes.rcda.org/olvchurch/bulletins/2026/September_20.pdf
  seen: 2026-09-28
  quote: SCHOHARIE COUNTY CLUSTER LITURGY SCHEDULE
  note: Our Lady of the Valley, Middleburgh publishes its own, different bulletin for the same Sunday
    (masthead 'OUR LADY OF THE VALLEY 111 WELLS AVE.'); same pastor, Fr. Thomas Zelker. So the two are
    separate rows.
- url: http://parishes.rcda.org/OurLadyOfFatima/bulletin.php
  seen: 2026-09-28
  note: The parish's bulletin page lists one PDF per Sunday at bulletins/<year>/<Month>_<DD>.pdf, weekly
    through September_20 on 2026-09-28.
promoted: 2026-09-28
---

## Publisher

Our Lady of Fatima, Delanson publishes its own weekly bulletin as PDFs on its page on the
diocese's parish host (parishes.rcda.org/OurLadyOfFatima). The latest issue posted on
2026-09-28 was 20 September 2026 (the 27 September file was not up yet: 404). Its page 1
names "Our Lady Of Fatima, P. O. Box 219 (1735 Alexander Road), Delanson" and gives Saturday
Vigil 4 pm, Sunday 11:15 am and Tuesday 9 am; page 2's Liturgy Schedule lists only Fatima's
Masses. The masthead also prints a box for Our Lady of the Valley, Middleburgh (same pastor,
Fr. Thomas Zelker; the two form a "Schoharie County Cluster"), but Our Lady of the Valley
publishes its own bulletin with its own masthead (parishes.rcda.org/olvchurch, 20 September
2026 issue read), so the two are separate rows. Our Lady of the Valley is in the
southern-tier region and is not recorded here.

## Worship sites

One: `our-lady-of-fatima-delanson`. The diocese directory gives Sunday 11:00 am; the
bulletin says 11:15 am (the bulletin is followed).

## Website and bulletin provider

The site is the parish's page on parishes.rcda.org, the address the diocese directory gives.
The bulletin is self-hosted: `bulletin_provider: other`, `publication` is the bulletin index
page. File names are `bulletins/<YYYY>/<Monthname>_<DD>.pdf`, not a numeric date.

Fetch recipe `page-pdfs http://parishes.rcda.org/OurLadyOfFatima/bulletin.php`, pinned
2026-10-03: on the pages recorded 2026-10-03
(`tests/fixtures/fetch/our-lady-of-fatima-delanson.json.gz`) the resolver found
http://parishes.rcda.org/OurLadyOfFatima/bulletins/2026/October_04.pdf this way, dated
that week.

## Not yet confirmed

The 27 September 2026 issue had not been posted when read; the index shows weekly issues
without gaps from January to 20 September 2026.
