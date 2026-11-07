---
name: Our Lady of the Angels Parish
website: http://www.olanj.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-parish-of-our-lady-of-the-angels-trenton-nj-08611
publication: ['url:https://www.church-bulletin.org/the-parish-of-our-lady-of-the-angels-trenton-nj-08611']
group: Cohort 10
evidence:
- url: https://www.church-bulletin.org/bulletin/the-parish-of-our-lady-of-the-angels-trenton-nj-08611/2026-10-25.pdf
  seen: 2026-10-30
  quote: 11:00AM (SJC)
  note: '25 October 2026 issue, 12 pages, text layer on 2 (pages 1 and 7); the rest are images, rendered
    with render.py. Page 2 (image) is the pastor''s letter under the logo ''The Parish of Our Lady of
    the Angels, Saint Joachim & Immaculate Conception'', signed Rev. Carlos Aguirre, inviting parishioners
    to ''St. Joachim Church''. Page 7 (text) lists Mass intentions by church: weekdays 12:15PM (SJC),
    Saturday 4:00 PM (SJC) and 6:30PM (ICC, Spanish), Sunday 7:30AM (ICC, Spanish), 9:30 AM (ICC), 11:00AM
    (SJC), 12:30PM (ICC, Spanish), Thursday 7:00PM (SJC, Spanish). Footer of page 12: ''594 Our Lady of
    the Angels, Trenton, NJ''.'
- url: https://www.olanj.org/
  seen: 2026-10-30
  quote: 540 Chestnut Ave.
  note: 'Homepage (read in the browser; the quoted lines are also in the plain HTML): ''Immaculate Concept
    Church (ICC)'' and ''Saint Joachim Church (SJC)'' with ''20 Butler St.'' and ''540 Chestnut Ave.''
    (Trenton NJ 08611), office ''21-23 Bayard Street'', phone (609) 695-6089. Mass schedule: weekdays
    Monday-Thursday 12:15 p.m. and Thursday 7:00 p.m. Spanish at St. Joachim; Saturday 4:00 p.m. English
    at St. Joachim, 6:30 p.m. Spanish at Immaculate Conception; Sunday 7:30 a.m. Spanish and 9:30 a.m.
    English at Immaculate Conception, 11:00 a.m. English at St. Joachim, 12:30 p.m. Spanish at Immaculate
    Conception. ''Click for Current Bulletin'' links John Patrick 594 (probe url: jppc.net/onlinebulletins/594template.pdf).'
promoted: 2026-10-30
research:
- method: church-bulletin.org listing 594; probe pdf and render.py on the 25 October 2026 issue; probe
    url and visit.py on olanj.org
  url: https://www.church-bulletin.org/the-parish-of-our-lady-of-the-angels-trenton-nj-08611
  checked: '2026-10-30'
  outcome: found
  next_action: None.
- method: pnpm fetch:check --diocese trenton --parish our-lady-of-the-angels-trenton (headed Chrome);
    page-pdfs on the church-bulletin.org listing
  url: https://www.church-bulletin.org/the-parish-of-our-lady-of-the-angels-trenton-nj-08611
  checked: '2026-10-30'
  outcome: found
  next_action: It picked the 25 October 2026 issue (date read from the text, freshness 'fresh', 5 days);
    document type pdf, mostly image pages; identity 'unverified' by the tool, read by hand from the rendered
    pages. Recipe recorded in provider_id.
bulletin_status: available
publication_reviews:
- parish: st-mary-of-the-assumption-cathedral-trenton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/the-parish-of-our-lady-of-the-angels-trenton-nj-08611/2026-10-25.pdf
    seen: 2026-10-30
    note: The 25 October 2026 issue (rendered page 2) is the bulletin for The Parish of Our Lady of the
      Angels, Saint Joachim and Immaculate Conception (pastor Rev. Carlos Aguirre), with Masses at (SJC)
      and (ICC) only; John Patrick 594.
  - url: https://www.church-bulletin.org/bulletin/cathedral-of-saint-mary-of-the-assumption-trenton-nj-08608/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names the Cathedral of Saint Mary of the Assumption
      (Rector Msgr. Joseph L. Roldán, 151 North Warren Street), with a Mass schedule that includes both
      the Cathedral and Saint Joseph; John Patrick 524.
- parish: st-joseph-trenton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/the-parish-of-our-lady-of-the-angels-trenton-nj-08611/2026-10-25.pdf
    seen: 2026-10-30
    note: The 25 October 2026 issue (rendered page 2) is the bulletin for The Parish of Our Lady of the
      Angels, Saint Joachim and Immaculate Conception (pastor Rev. Carlos Aguirre), with Masses at (SJC)
      and (ICC) only; John Patrick 594.
  - url: https://www.church-bulletin.org/bulletin/saint-joseph-s-parish-roman-catholic-church-trenton-nj-08638/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names St. Joseph's parish alone (Pastor Rev. Msgr. Joseph Roldan,
      540 North Olden Avenue), with its own Mass times; footer '553 St. Joseph, Trenton'; a different
      file from the Cathedral's issue of the same Sunday.
---

## Publisher

The Parish of Our Lady of the Angels, Trenton, Cohort 10: a 2017-era merger of Immaculate Conception and St. Joachim (the logo reads 'Saint Joachim & Immaculate Conception'; pastor Rev. Carlos Aguirre). It publishes its own bulletin through John Patrick Publishing (listing 594); the parish site's 'Current Bulletin' link is the 594 template. The 25 October 2026 issue is the latest on the listing (a week behind the Cathedral's and St. Joseph's 1 November issues; the coming Sunday's is not posted yet). The masthead is an image page (evidence note). GCatholic's website for St. Joachim (olatrenton05.org) is dead.

## Worship sites

Two churches with public Mass, both in the bulletin's Mass intentions and the parish site's schedule: St. Joachim, 20 Butler Street (`st-joachim-trenton`) and Immaculate Conception, 540 Chestnut Avenue (`immaculate-conception-trenton`). The parish office, 21-23 Bayard Street (finder: 19 Bayard St), is next to St. Joachim's Centennial Hall and is no worship site.

## Website and bulletin provider

The row reads the John Patrick listing (`page-pdfs`); `fetch:check` result in research.
