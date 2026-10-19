---
name: St. John XXIII and St. Richard Parishes
website: https://www.sj23tamaqua.org/
bulletin_provider: other
provider_id: page-pdfs https://www.sj23tamaqua.org/bulletin
publication: ['url:https://www.sj23tamaqua.org/bulletin']
group: St. John XXIII Parish
evidence:
- url: https://irp.cdn-website.com/4af99d44/files/uploaded/10+Oct+18+2026.pdf
  seen: 2026-10-18
  quote: Church of St. John XXIII 307 Pine Street, Tamaqua, PA 18252
  note: Page 1 of the 18 October 2026 issue; the same page later has "Church of St. Richard 799 Barnesville
    Drive, Barnesville, PA 18214".
- url: https://irp.cdn-website.com/4af99d44/files/uploaded/10+Oct+18+2026.pdf
  seen: 2026-10-18
  quote: SJ = St. John XXIII SR = St. Richard
  note: 'Page 2: Saturday 4:00PM Mass SJ, 5:30PM Mass SR; Sunday 9:00AM Mass SJ, 10:30AM Mass SR; Wednesday
    and Thursday 9:00AM SJ.'
- url: https://irp.cdn-website.com/4af99d44/files/uploaded/10+Oct+18+2026.pdf
  seen: 2026-10-18
  quote: PRAYER LIST FOR BOTH PARISHES
  note: 'Page 3: devotional candles, religious education and second collections for both churches.'
- url: https://www.sj23tamaqua.org/bulletin
  seen: 2026-10-18
  quote: Download Current Bulletin
  note: Links https://irp.cdn-website.com/4af99d44/files/uploaded/10+Oct+18+2026.pdf; the page lists every
    2024–2026 issue with the date in the file name.
- url: https://www.sj23tamaqua.org/parish-tour
  seen: 2026-10-18
  quote: In 2021, St. John XXIII parish was "twinned" with St. Richard's Parish in Barnesville, and Father
    Robert Finlan assumed the responsibilities of pastor for both parishes.
- url: https://strichard.org/
  seen: 2026-10-18
  note: 'St. Richard''s own site (the diocese map''s website): http redirects to https://strichard.org/,
    which resets the connection (probe url: UNREACHABLE; visit.py: ERROR) from the sandbox.'
revisit: Retry https://strichard.org (connection reset from the sandbox on 2026-10-18) and check whether
  St. Richard posts the same joint bulletin or one of its own; split the row only if it has its own.
revisit_after: 2026-11-15
promoted: 2026-10-19
---

## Publisher

St. John XXIII Parish, Tamaqua and St. Richard Parish, Barnesville, twinned since 2021 under
one pastor, publish **one** weekly bulletin. The 18 October 2026 issue (5 pages; pages 1–4
text) names both churches on page 1 ("Church of St. John XXIII, 307 Pine Street, Tamaqua" and
"Church of St. Richard, 799 Barnesville Drive, Barnesville"), gives one Mass schedule coded
"SJ = St. John XXIII, SR = St. Richard" (Saturday 4:00 pm SJ, 5:30 pm SR; Sunday 9:00 am SJ,
10:30 am SR; Wednesday and Thursday 9:00 am SJ), and has a "Prayer list for both parishes",
candles and religious education for each.

## Worship sites

- `st-john-xxiii-tamaqua`: the former SS. Peter and Paul church, 307 Pine Street, the
  parish's only church since Pentecost 2018.
- `st-richard-barnesville`: 799 Barnesville Drive.

Ruled out: the former St. Jerome church, 266 W. Broad St. (`excluded/`, closed May 2018,
sold January 2022). The diocese's map still gives St. Jerome's address for St. John XXIII.

## Website and bulletin provider

`other`: sj23tamaqua.org/bulletin (an Our Sunday Visitor site) lists every issue at
`irp.cdn-website.com/4af99d44/files/uploaded/<MM> <Mon> <D> <YYYY>.pdf`. `fetch_check_rows.py`
on 2026-10-18 picked the 18 October file ("page-pdfs on https://www.sj23tamaqua.org/bulletin:
current"), so its recipe is pinned. Text PDF.

St. Richard's own site could not be read (connection reset), so it is **not confirmed** that
St. Richard has no channel of its own; the joint bulletin's coverage of St. Richard (its
Masses, candles, CCD and collections) is why it is one row rather than two.

## Not yet confirmed

What strichard.org posts (see `revisit`).
