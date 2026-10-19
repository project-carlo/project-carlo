---
name: Roman Catholic Churches of Easton (St. Anthony of Padua and Our Lady of Mercy)
website: https://rccofeaston.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/207
publication: ['url:https://www.church-bulletin.org/saint-anthony-of-padua-our-lady-of-mercy-easton-pa-18042']
group: 'Twin parishes: St. Anthony of Padua and Our Lady of Mercy, Easton'
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-anthony-of-padua-our-lady-of-mercy-easton-pa-18042/2026-10-18.pdf
  seen: 2026-10-18
  note: 'Page 1 of the 18 October 2026 issue (all 8 pages are images with no text layer; read rendered
    with parish-site-access render.py). One masthead: "OUR LADY OF MERCY, 132 S. 5th Street, Easton, PA
    18042" and "SAINT ANTHONY OF PADUA, 900 Washington Street, Easton, PA 18042", "www.rccofeaston.org",
    clergy Rev. Mark Searles, Parochial Administrator. Two MASS & LITURGY SCHEDULE boxes: Our Lady of
    Mercy "Sunday @ 8:00 am English & 12:00 pm Spanish", Monday & Friday 8:00 am, Wednesday 12:10 pm &
    7:00 pm Spanish; St. Anthony "Saturday @ 4:30pm, Sunday @ 10:30am", Tuesday & Thursday 8:00am.'
- url: https://www.church-bulletin.org/saint-anthony-of-padua-our-lady-of-mercy-easton-pa-18042
  seen: 2026-10-18
  quote: Easton
  note: John Patrick Publishing's listing (church-bulletin.org/?id=207 lands here), one PDF per Sunday,
    newest 2026-10-18.
- url: https://rccofeaston.org/
  seen: 2026-10-18
  quote: Roman Catholic Churches of Easton
  note: The joint parish site (title "Roman Catholic Churches of Easton"); probe url found its bulletin
    link https://church-bulletin.org/?id=207.
promoted: 2026-10-19
---

## Publisher

St. Anthony of Padua and Our Lady of Mercy, the two Easton city parishes, are "twin parishes"
under one priest (the diocesan directory: "also pastor of twin parish ..."; the 18 October
2026 bulletin names Rev. Mark Searles as parochial administrator) with one website,
rccofeaston.org, and **one weekly bulletin** through John Patrick Publishing. I read the 18
October 2026 issue (image-only; rendered): its page-1 masthead pairs the two churches, each
with its own address and Mass box.

## Worship sites

- St. Anthony of Padua, 900 Washington Street, Easton (`st-anthony-of-padua-easton`):
  Saturday 4:30 pm, Sunday 10:30 am.
- Our Lady of Mercy, Easton (`our-lady-of-mercy-easton`): Sunday 8:00 am (English) and
  12:00 pm (Spanish).

## Website and bulletin provider

rccofeaston.org is the site both directory entries give; it links the bulletin as
church-bulletin.org/?id=207, which lands on the listing recorded in `publication`. Provider
`other`, recipe `page-pdfs https://church-bulletin.org/207`. The whole bulletin is scanned
images (18 October issue: no text on any of its 8 pages), so the pipeline will have to read it
as images. Empty ParishesOnline orgs exist for each church (`our-lady-of-mercy-church-18042`,
`st-anthony-of-padua-church-18042`) with no publications; not recorded.

Fetch check (2026-10-19, `fetch_check` on a temporary CSV of the unpromoted rows): resolved, `page-pdfs on https://church-bulletin.org/207: current`, the 18 October 2026 PDF (image-only).

## Not yet confirmed

The directory still names Rev. Keith R. Laskowski as pastor; the bulletin names Rev. Mark
Searles as parochial administrator. This doesn't affect the row.
