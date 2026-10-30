---
name: St. Joseph Parish
website: https://www.church-bulletin.org/saint-joseph-s-parish-roman-catholic-church-trenton-nj-08638
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-joseph-s-parish-roman-catholic-church-trenton-nj-08638
publication: ['url:https://www.church-bulletin.org/saint-joseph-s-parish-roman-catholic-church-trenton-nj-08638']
group: Cohort 10
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-joseph-s-parish-roman-catholic-church-trenton-nj-08638/2026-11-01.pdf
  seen: 2026-10-30
  quote: 540 North Olden Avenue
  note: '1 November 2026 issue, 4 pages, text layer (the masthead''s title glyphs are garbled, the rest
    reads). Page 1: 540 North Olden Avenue, Trenton 08638, phone (609) 394-5757, e-mail elena@sjctrenton.com;
    ''Pastor ... Rev. Msgr. Joseph Roldan'', parochial vicar Rev. Erwin Candelaria; ''ENGLISH MASSES Saturday:
    4:00 PM'', ''MISAS EN ESPAÑOL Domingo: 9:30 am y 11:30 am''. Page 2 footer ''553 St. Joseph, Trenton''.
    A different file from the Cathedral''s 1 November issue (md5 a3f2b475... against ff9963cd...).'
research:
- method: church-bulletin.org listing 553 and its 1 November 2026 PDF (probe pdf --pages 2)
  url: https://www.church-bulletin.org/saint-joseph-s-parish-roman-catholic-church-trenton-nj-08638
  checked: '2026-10-30'
  outcome: found
  next_action: None.
- method: 'Looked for the parish''s own website: the finder pin has none; the bulletin prints e-mail elena@sjctrenton.com;
    visit.py on sjctrenton.com'
  url: https://sjctrenton.com
  checked: '2026-10-30'
  outcome: not-found
  next_action: 'None: the domain is parked (GoDaddy lander), so the row''s website is the printer''s listing.'
  retry_when: The finder or the Cathedral's site links a St. Joseph website.
- method: pnpm fetch:check --diocese trenton --parish st-joseph-trenton (headed Chrome); page-pdfs on
    the church-bulletin.org listing
  url: https://www.church-bulletin.org/saint-joseph-s-parish-roman-catholic-church-trenton-nj-08638
  checked: '2026-10-30'
  outcome: found
  next_action: It picked the 1 November 2026 issue (the coming Sunday's, freshness 'future'); document
    type pdf; identity 'unverified' by the tool (no expected identity), read by hand from page 1. Recipe
    recorded in provider_id.
bulletin_status: available
publication_reviews:
- parish: st-mary-of-the-assumption-cathedral-trenton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-joseph-s-parish-roman-catholic-church-trenton-nj-08638/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names St. Joseph's parish alone (Pastor Rev. Msgr. Joseph Roldan,
      540 North Olden Avenue), with its own Mass times; footer '553 St. Joseph, Trenton'; a different
      file from the Cathedral's issue of the same Sunday.
  - url: https://www.church-bulletin.org/bulletin/cathedral-of-saint-mary-of-the-assumption-trenton-nj-08608/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names the Cathedral of Saint Mary of the Assumption
      (Rector Msgr. Joseph L. Roldán, 151 North Warren Street), with a Mass schedule that includes both
      the Cathedral and Saint Joseph; John Patrick 524.
- parish: our-lady-of-the-angels-trenton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-joseph-s-parish-roman-catholic-church-trenton-nj-08638/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names St. Joseph's parish alone (Pastor Rev. Msgr. Joseph Roldan,
      540 North Olden Avenue), with its own Mass times; footer '553 St. Joseph, Trenton'; a different
      file from the Cathedral's issue of the same Sunday.
  - url: https://www.church-bulletin.org/bulletin/the-parish-of-our-lady-of-the-angels-trenton-nj-08611/2026-10-25.pdf
    seen: 2026-10-30
    note: The 25 October 2026 issue (rendered page 2) is the bulletin for The Parish of Our Lady of the
      Angels, Saint Joachim and Immaculate Conception (pastor Rev. Carlos Aguirre), with Masses at (SJC)
      and (ICC) only; John Patrick 594.
---

## Publisher

St. Joseph Parish, Trenton (540 North Olden Avenue), Cohort 10, linked with the Cathedral under one pastor by the 2017 decisions (https://dioceseoftrenton.org/decisions, read 2026-10-30). It publishes its own bilingual bulletin through John Patrick Publishing (listing 553; footer '553 St. Joseph, Trenton'). Its 1 November 2026 masthead names the pastor Rev. Msgr. Joseph Roldan, the same priest the Cathedral's bulletin names as Rector, but it is a different file with its own contact details and a Mass schedule for St. Joseph alone (quoted in the evidence). The Cathedral's bulletin also prints St. Joseph's Masses in its combined schedule; see `st-mary-of-the-assumption-cathedral-trenton`. Two rows (Rules settled: a linkage is not a shared bulletin).

## Worship sites

One church: St. Joseph, 540 North Olden Avenue (`st-joseph-trenton`). The bulletin also announces Divine Mercy Chaplet 'En la capilla' Sundays at 3:00 PM: a chapel within the same campus with no address of its own, not a second row.

## Website and bulletin provider

The finder pin has no website. The e-mail domain sjctrenton.com is a parked GoDaddy page (visit.py, 2026-10-30). The row therefore uses the printer's listing as its website.
