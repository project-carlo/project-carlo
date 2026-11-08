---
name: St. Mary of the Assumption Cathedral
website: http://saintmaryscathedral-trenton.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/cathedral-of-saint-mary-of-the-assumption-trenton-nj-08608
publication: ['url:https://www.church-bulletin.org/cathedral-of-saint-mary-of-the-assumption-trenton-nj-08608']
group: Cohort 10
evidence:
- url: https://www.church-bulletin.org/bulletin/cathedral-of-saint-mary-of-the-assumption-trenton-nj-08608/2026-11-01.pdf
  seen: 2026-10-30
  note: '1 November 2026 issue, 6 pages, image-only (no text layer; rendered page 1 with render.py, so
    recheck cannot find a quote). Page 1 masthead: ''Cathedral of Saint Mary of the Assumption / Catedral
    Santa María de la Asunción''; clergy ''Rev. Msgr. Joseph L. Roldán, Rector'', ''Rev. Erwin Candelaria'';
    parish office 149 North Warren Street; footer ''151 North Warren Street | Trenton, New Jersey 08608
    | P: 609-396-8447''. Its one Mass schedule lists both churches: Cathedral (Mon-Thu 12:10 PM English,
    7:00 PM Spanish; Fri 12:10 PM; Sat 5:30 PM Spanish; Sun 8:30 AM Spanish, 10:30 AM English, 12:30 PM
    Spanish) and Saint Joseph (Mon-Thu 9:00 AM Spanish; Fri 7:00 PM; Sat 4:00 PM English; Sun 9:30 AM
    and 11:30 AM Spanish). Weekly adoration Thursday 7:30 PM Cathedral, Friday 6:00 PM Saint Joseph.'
- url: https://saintmaryscathedral-trenton.org/
  seen: 2026-10-30
  quote: Cathedral of Saint Mary of the Assumption
  note: 'probe url: the parish site''s bulletin link is http://www.jppc.net/onlinebulletins/524template.pdf,
    which redirects to the John Patrick listing above (524).'
promoted: 2026-10-30
research:
- method: 'church-bulletin.org listing 524 and its 1 November 2026 PDF (probe pdf: no text; render.py
    pages 1-2)'
  url: https://www.church-bulletin.org/cathedral-of-saint-mary-of-the-assumption-trenton-nj-08608
  checked: '2026-10-30'
  outcome: found
  next_action: None.
- method: pnpm fetch:check --diocese trenton --parish st-mary-of-the-assumption-cathedral-trenton (headed
    Chrome); page-pdfs on the church-bulletin.org listing
  url: https://www.church-bulletin.org/cathedral-of-saint-mary-of-the-assumption-trenton-nj-08608
  checked: '2026-10-30'
  outcome: found
  next_action: It picked the 1 November 2026 issue (the coming Sunday's, freshness 'future'); document
    type pdf with no text on page 1 (image-only), identity 'unverified' by the tool, read by hand from
    the rendered masthead. Recipe recorded in provider_id.
bulletin_status: available
publication_reviews:
- parish: st-joseph-trenton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/cathedral-of-saint-mary-of-the-assumption-trenton-nj-08608/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names the Cathedral of Saint Mary of the Assumption
      (Rector Msgr. Joseph L. Roldán, 151 North Warren Street), with a Mass schedule that includes both
      the Cathedral and Saint Joseph; John Patrick 524.
  - url: https://www.church-bulletin.org/bulletin/saint-joseph-s-parish-roman-catholic-church-trenton-nj-08638/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names St. Joseph's parish alone (Pastor Rev. Msgr. Joseph Roldan,
      540 North Olden Avenue), with its own Mass times; footer '553 St. Joseph, Trenton'; a different
      file from the Cathedral's issue of the same Sunday.
- parish: our-lady-of-the-angels-trenton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/cathedral-of-saint-mary-of-the-assumption-trenton-nj-08608/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names the Cathedral of Saint Mary of the Assumption
      (Rector Msgr. Joseph L. Roldán, 151 North Warren Street), with a Mass schedule that includes both
      the Cathedral and Saint Joseph; John Patrick 524.
  - url: https://www.church-bulletin.org/bulletin/the-parish-of-our-lady-of-the-angels-trenton-nj-08611/2026-10-25.pdf
    seen: 2026-10-30
    note: The 25 October 2026 issue (rendered page 2) is the bulletin for The Parish of Our Lady of the
      Angels, Saint Joachim and Immaculate Conception (pastor Rev. Carlos Aguirre), with Masses at (SJC)
      and (ICC) only; John Patrick 594.
---

## Publisher

St. Mary of the Assumption Cathedral, Trenton, is Cohort 10 in the July 2024 cohort list (with St. Joseph and Our Lady of the Angels) and the seat of the Bishop (His Excellency David M. O'Connell, CM, on the bulletin). It publishes through John Patrick Publishing (listing 524); the parish site links `jppc.net/onlinebulletins/524template.pdf`. The latest issue, 1 November 2026, is image-only: the masthead is page 1 as rendered (evidence note).

The 2017 *Faith in Our Future* decisions (https://dioceseoftrenton.org/decisions, read 2026-10-30) set a Linkage Model for the Cathedral and St. Joseph: one pastor, distinct parishes. The mastheads agree: the Cathedral's names Rev. Msgr. Joseph L. Roldán as Rector, and St. Joseph's (`st-joseph-trenton`) names Rev. Msgr. Joseph Roldan as Pastor. They are nonetheless two bulletins: two John Patrick listings (524, 553), two different files for the same Sunday (different md5), and different mastheads, offices and phone numbers (609-396-8447 against 609-394-5757). So two rows (Rules settled: a linkage is not a shared bulletin).

## Worship sites

One church row: the Cathedral, 151 North Warren Street (`st-mary-of-the-assumption-cathedral-trenton`). The Cathedral's Mass schedule also lists Masses at Saint Joseph as part of one combined parish-pair schedule (Spanish weekday and Sunday Masses and the Saturday 4:00 PM English Mass), which the Saint Joseph bulletin repeats as its own. St. Joseph keeps its own church row under its own bulletin (`st-joseph-trenton`); a church belongs to one parish row, and I did not add it here. The combined schedule means a reader of this bulletin will see St. Joseph's times too: see the flag in the handoff.

The Cathedral's own Mass times are the ones marked 'Cathedral'. GCatholic omits the Cathedral entirely; the finder pins it.

## Website and bulletin provider

The row reads the John Patrick listing (`page-pdfs`); `fetch:check` result is in research. Nothing else is published: the parish site only links the listing.

## Not yet confirmed

Issues are image-only: the pipeline would need to read them as images.
