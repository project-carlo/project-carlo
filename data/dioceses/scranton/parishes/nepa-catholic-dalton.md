---
name: Our Lady of the Abingtons, Saint Mary of the Lake & Saint Patrick (NEPA Catholic)
website: https://nepacatholic.com/
bulletin_provider: other
provider_id: page-pdfs https://nepacatholic.com/bulletin
publication: ['url:https://nepacatholic.com/bulletin']
group: Our Lady of the Abingtons Parish; Saint Mary of the Lake Parish; Saint Patrick Parish Nicholson
evidence:
- url: https://img1.wsimg.com/blobby/go/e126fb61-2499-4188-a27d-56245bc4d6a9/10-11-2026%20bulletin.pdf
  seen: 2026-10-16
  quote: Our three Parishes continue to celebrate the SML
  note: 'Page 1 of the 11 October 2026 issue (2 pages, text). Page 2 lists one schedule for the three
    parishes, coded OLA (Our Lady of the Abingtons), SML (Saint Mary of the Lake) and SP (Saint Patrick):
    Saturday 4 pm (OLA), Sunday 9:00am (SML) and 11 am (SP); weekdays Tuesday 8:00am (OLA), Wednesday
    8:00am (SP), Thursday 8:00 am (SML).'
- url: https://img1.wsimg.com/blobby/go/e126fb61-2499-4188-a27d-56245bc4d6a9/10-11-2026%20bulletin.pdf
  seen: 2026-10-16
  quote: 4 pm (OLA) Michele Zajac
  note: Page 2, liturgical ministers for 17-18 October, one list for OLA, SML and SP.
- url: https://nepacatholic.com/bulletin
  seen: 2026-10-16
  note: 'The shared site''s Bulletin page (GoDaddy Websites; the sandbox cannot connect to nepacatholic.com,
    so it was read with a fetch tool, not quoted): "Weekly Bulletin" linking img1.wsimg.com/blobby/go/e126fb61-2499-4188-a27d-56245bc4d6a9/10-11-2026
    bulletin.pdf, and "Past Bulletins" back to 7-19-2026. The homepage links pages for /our-lady-of-the-abingtons,
    /saint-mary-of-the-lake and /saint-patricks.'
promoted: 2026-10-17
---

## Publisher

Three canonical parishes under one pastor, Our Lady of the Abingtons (Dalton), Saint Mary of
the Lake (Lake Winola) and Saint Patrick (Nicholson), publish one weekly bulletin on their
shared site nepacatholic.com. The diocesan finder gives nepacatholic.com as the website of
all three. I read the 11 October 2026 issue (a two-page PDF): it speaks of "Our three
Parishes", and page 2 has one ministers' schedule and one Mass-intention list for all three,
coded OLA, SML and SP: Saturday 4 pm OLA, Sunday 9 am SML and 11 am SP, Tuesday 8 am OLA,
Wednesday 8 am SP, Thursday 8 am SML. So one row.

## Worship sites

- Our Lady of the Abingtons, Dalton (`our-lady-of-the-abingtons-dalton`); its street address
  is disputed between sources, see that file.
- St. Mary of the Lake, 1872 Dalton Road, Lake Winola (`st-mary-of-the-lake-lake-winola`).
- St. Patrick, 205 Main Street, Nicholson (`st-patrick-nicholson`).

One church per canonical parish, as the finder and GCatholic list them. Nothing ruled out.

## Website and bulletin provider

nepacatholic.com is the three parishes' own site; its /bulletin page links the current
PDF ("Weekly Bulletin") and a list of past issues, each a dated file on GoDaddy's
img1.wsimg.com host (e.g. "10-11-2026 bulletin.pdf"). Provider `other` with the recipe
`page-pdfs https://nepacatholic.com/bulletin`, which is a guess from the page's shape:
from this sandbox nepacatholic.com refuses every connection (curl, probe url and the
browser all got "connection reset"; the img1.wsimg.com PDFs download fine), so the page was
read with a fetch tool and neither probe url nor fetch:check has run on it. GCatholic gives
an older site for St. Mary of the Lake (bvm-sml.org), not checked. St. Patrick's
ParishesOnline organization `st-patrick-church-18446` has no publications.

## Not yet confirmed

Whether the pipeline can reach nepacatholic.com and whether the recipe picks the current
issue: run `pnpm fetch:check -- --parish nepa-catholic-dalton` after promotion, from a
network that can reach the site.
