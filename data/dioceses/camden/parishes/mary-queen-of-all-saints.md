---
name: Mary, Queen of All Saints Parish
website: http://www.maryqueenofallsaints.org
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:http://www.maryqueenofallsaints.org/currbulletin3.pdf']
group: ''
evidence:
- url: http://www.maryqueenofallsaints.org/currbulletin3.pdf
  seen: 2026-10-29
  quote: Families must be registered in Mary, Queen of All Saints Parish.
  note: 'Current bulletin (text layer, 3 pages): Mass intentions for Saturday 31 October to Sunday 8 November
    2026 with Saturday 6:30pm, Sunday 8:30am and 10:30am, weekday 8:00am Masses, then parish notices (rectory,
    religious education, food pantry). It has no masthead page; the parish is named in the religious education
    notice. Names this parish alone.'
- url: http://www.maryqueenofallsaints.org/currbulletin2.pdf
  seen: 2026-10-29
  quote: SATURDAY, OCTOBER 24th
  note: 'The site''s ''Previous Week''s Weekly Bulletin'' link: the issue before currbulletin3, Mass intentions
    for 24 October onward. So currbulletin3.pdf is the current week and currbulletin2.pdf the previous.'
- url: http://www.maryqueenofallsaints.org
  seen: 2026-10-29
  quote: 4824 Camden Avenue, Pennsauken, NJ 08110
  note: Parish site (a static page), footer 'Copyright © 2026, Mary Queen of All Saints Parish, Pennsauken,
    NJ'; links currbulletin3.pdf as the weekly bulletin and currbulletin2.pdf as the previous week's.
- url: http://www.stceciliapennsauken.org
  seen: 2026-10-29
  note: The directory's website for this parish is the old St. Cecilia domain; probe url (200) shows the
    same page, linking maryqueenofallsaints.org/currbulletin3.pdf and currbulletin2.pdf.
promoted: 2026-10-30
research:
- method: fetch:check --diocese camden --parish mary-queen-of-all-saints (2026-10-29)
  url: http://www.maryqueenofallsaints.org/currbulletin3.pdf
  checked: '2026-10-29'
  outcome: found
  next_action: Re-run fetch:check if the site's bulletin links change; the pick is the first-listed PDF
    (currbulletin3), which the page labels the current week.
---

## Publisher

The parish publishes its own bulletin as a fixed-name PDF on its own site: `http://www.maryqueenofallsaints.org/currbulletin3.pdf` is the link labelled 'Weekly Bulletin' and `currbulletin2.pdf` the 'Previous Week's Weekly Bulletin' (home page and `probe url`, 2026-10-29). On that date currbulletin3 held the week of Saturday 31 October to Sunday 8 November 2026 and currbulletin2 the week of 24 October. The file is a three-page text PDF with no masthead page: Mass intentions with times, then notices for the parish (rectory, religious education 'registered in Mary, Queen of All Saints Parish', food pantry, Joseph's House). No other publisher prints it, and nothing links a John Patrick id.

The pastor is not named in the bulletin or the site pages read; the directory's 'Father Ed Friel' dates from 2015 and the bulletin's Marylin Angelotti Kelly 'R/B Friel Family' proves nothing, so no pastor is recorded and no shared pastor with St. Stephen or St. Peter is claimed.

## Worship sites

One: Mary, Queen of All Saints, 4824 Camden Avenue (church record `mary-queen-of-all-saints`). The site's Mass Schedule gives Saturday 6:30pm (Spanish), Sunday 8:30am and 10:30am, Monday, Tuesday, Wednesday and Friday 8:00am, which matches the bulletin's intentions. The bulletin names no other church.

## Website and bulletin provider

The directory lists `stceciliapennsauken.org` (the former St. Cecilia parish's domain), which serves the same page as `maryqueenofallsaints.org`, GCatholic's website. The site is `maryqueenofallsaints.org`. `other`: the pipeline finds the PDF from the site's links. The site still shows a 2021 Holy Week schedule on its home page, so its notices are not all current, but the bulletin link is.

## Not yet confirmed

The bulletin is the same URL each week (overwritten), so freshness depends on the parish updating it; the week of 31 October to 8 November was posted on 29 October. `fetch:check` (2026-10-29) picked currbulletin3.pdf (first-listed on the home page, the current week): transport ok, PDF, but issue date and freshness 'unknown', because the file has no masthead or dated filename (only the weekday dates of the Mass intentions). That is a format limit, not a stale pick. Nothing blocking.
