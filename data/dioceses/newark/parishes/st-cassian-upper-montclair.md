---
name: St. Cassian Parish, Upper Montclair
website: https://stcassianchurchuppermontclair.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/616
publication: ['url:https://www.church-bulletin.org/saint-cassian-parish-upper-montclair-nj-07043']
group: Planning Area G
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-cassian-parish-upper-montclair-nj-07043/2026-11-01.pdf
  seen: 2026-11-03
  note: 1 November 2026 issue, 16 pages, image only (read with render.py; recheck can't find quotes).
    Page 1 cover 'All Saints Day / St. Cassian Church'. Page 2 masthead 'Saint Cassian Parish, 187 Bellevue
    Avenue Upper Montclair, NJ 07043 • (973) 744-2850 • stcassianchurch.org', 'All Saints Day November
    1, 2026'; Mass schedule Saturday 5:30PM; Sunday 7:30AM, 9:00AM, 11:30AM; weekdays Tuesday through
    Saturday 8:15AM; pastor Rev. Fr. Steven D'Andrea. Page 16 footer '616 St Cassian, Upper Montclair,
    NJ (back) … John Patrick Publishing Company'.
- url: https://church-bulletin.org/616
  seen: 2026-11-03
  note: 'Redirects to church-bulletin.org/saint-cassian-parish-upper-montclair-nj-07043: dated issues
    2026-11-01, 10-25, 10-18, 10-11 and earlier.'
- url: https://stcassianchurchuppermontclair.org/
  seen: 2026-11-03
  note: Parish site (the masthead's stcassianchurch.org redirects here); probe url lists its bulletin
    link https://www.jppc.net/onlinebulletins/616template.pdf.
bulletin_status: available
publication_reviews:
- parish: st-teresa-of-calcutta-montclair
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-cassian-parish-upper-montclair-nj-07043/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead (page 2) names Saint Cassian Parish, 187 Bellevue Avenue, Upper
      Montclair, alone, with its own Mass schedule; John Patrick id 616.
  - url: https://www.church-bulletin.org/bulletin/immaculate-conception-church-saint-teresa-of-calcutta-parish-montclair-nj-07042/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Immaculate Conception Church, St Teresa of Calcutta Parish,
      with a Mass schedule for Immaculate Conception alone; John Patrick id 6037.
- parish: our-lady-of-mount-carmel-oratory-montclair
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-cassian-parish-upper-montclair-nj-07043/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead (page 2) names Saint Cassian Parish, 187 Bellevue Avenue, Upper
      Montclair, alone, with its own Mass schedule; John Patrick id 616.
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-mount-carmel-oratory-montclair-nj-07042/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Our Lady of Mount Carmel, Montclair, an oratory at 94 Pine
      Street, alone, with its own Mass schedule; John Patrick id 6030.
---

## Publisher

St. Cassian Parish, Upper Montclair, publishes a weekly bulletin printed by John Patrick Publishing (id 616). I read the 1 November 2026 issue (16 pages, image only, rendered): page 2 masthead 'Saint Cassian Parish, 187 Bellevue Avenue Upper Montclair, NJ 07043', one Mass schedule for the church; page 16 footer '616 St Cassian, Upper Montclair, NJ (back) … John Patrick Publishing Company'.

## Worship sites

- St. Cassian, 187 Bellevue Avenue (`st-cassian-upper-montclair`): Saturday 5:30 pm; Sunday 7:30, 9:00, 11:30 am; Tuesday-Saturday 8:15 am (page 2).

The directory (202) and GCatholic (18570) list this one church; the parish also runs St. Cassian School (not a worship site).

## Website and bulletin provider

https://stcassianchurchuppermontclair.org/ (stcassianchurch.org, the masthead's address, redirects to it) links jppc.net/onlinebulletins/616template.pdf. Provider `other`, read with `page-pdfs https://church-bulletin.org/616` (the playbook's John Patrick pin). The issues are image only: the pipeline will need to read them as images.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/616: current` and picked church-bulletin.org/bulletin/saint-cassian-parish-upper-montclair-nj-07043/2026-11-01.pdf, the 1 November 2026 issue read above; freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied; the rendered masthead confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open for the row.
