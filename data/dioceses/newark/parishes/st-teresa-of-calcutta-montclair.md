---
name: St. Teresa of Calcutta Parish, Montclair
website: https://www.iccmontclair.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6037
publication: ['url:https://www.church-bulletin.org/immaculate-conception-church-saint-teresa-of-calcutta-parish-montclair-nj-07042']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/immaculate-conception-church-saint-teresa-of-calcutta-parish-montclair-nj-07042/2026-11-01.pdf
  seen: 2026-11-03
  note: '1 November 2026 issue, 6 pages, image only (read with render.py; recheck can''t find quotes).
    Page 1 masthead: ''Immaculate Conception Church / St Teresa of Calcutta Parish'', ''November 1, 2026
    | Solemnity of All Saints''. Page 2: ''www.montclaircatholics.org'', parish center 1 Munn Street,
    pastor Rev. A. Benny Prado; ''Immaculate Conception Church 30 North Fullerton Avenue Montclair NJ
    07042'': Saturday 5:00 pm; Sunday 8:00 am, 10:30 am, 6:00 pm; weekdays Monday-Friday 12:00 pm in Pope
    Francis Hall. Page 6 footer: ''6037 St. Teresa of Calcutta, Montclair, NJ … John Patrick Publishing
    Company''.'
- url: https://church-bulletin.org/6037
  seen: 2026-11-03
  note: 'Redirects to church-bulletin.org/immaculate-conception-church-saint-teresa-of-calcutta-parish-montclair-nj-07042,
    ''Immaculate Conception Church - Saint Teresa of Calcutta Parish Bulletin'': dated issues 2026-11-01,
    10-25, 10-18, 10-11, 10-04 and earlier.'
- url: https://www.iccmontclair.org/
  seen: 2026-11-03
  note: Wix site 'Immaculate Conception Church | Montclair, NJ' (montclaircatholics.org redirects here);
    probe url lists its bulletin link https://church-bulletin.org/?id=6037.
promoted: 2026-11-05
bulletin_status: available
publication_reviews:
- parish: our-lady-of-mount-carmel-oratory-montclair
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/immaculate-conception-church-saint-teresa-of-calcutta-parish-montclair-nj-07042/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Immaculate Conception Church, St Teresa of Calcutta Parish,
      with a Mass schedule for Immaculate Conception alone; John Patrick id 6037.
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-mount-carmel-oratory-montclair-nj-07042/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Our Lady of Mount Carmel, Montclair, an oratory at 94 Pine
      Street, alone, with its own Mass schedule; John Patrick id 6030.
---

## Publisher

St. Teresa of Calcutta Parish, Montclair, publishes a weekly bulletin under the masthead 'Immaculate Conception Church / St Teresa of Calcutta Parish', printed by John Patrick Publishing (id 6037). I read the 1 November 2026 issue (image only, rendered): page 2 gives the parish center at 1 Munn Street, pastor Rev. A. Benny Prado, and one Mass schedule for Immaculate Conception Church, 30 North Fullerton Avenue; the page 6 footer reads '6037 St. Teresa of Calcutta, Montclair, NJ … John Patrick Publishing Company'.

## Worship sites

- Immaculate Conception Church, 30 North Fullerton Avenue (`immaculate-conception-montclair`): Saturday 5:00 pm; Sunday 8:00 am, 10:30 am, 6:00 pm; Monday-Friday 12:00 pm in Pope Francis Hall (1 November 2026 issue, page 2).

The archdiocese's closed/merged records table (rcan.org/sacramental-records, May 2025) lists Immaculate Conception and Our Lady of Mount Carmel (Italian), Montclair, as merged into St. Theresa of Calcutta. Our Lady of Mount Carmel at 94 Pine Street is now an oratory (directory 118) and publishes its own bulletin (John Patrick 6030, 1 November 2026 issue) with its own Mass schedule, so it is a separate row (`our-lady-of-mount-carmel-oratory-montclair`); this bulletin's Mass schedule names only Immaculate Conception.

## Website and bulletin provider

https://www.iccmontclair.org/ (Wix; the masthead's www.montclaircatholics.org redirects to it) links https://church-bulletin.org/?id=6037. Provider `other`, read with `page-pdfs https://church-bulletin.org/6037` (the playbook's John Patrick pin). The issues are image only: the pipeline will need to read them as images.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/6037: current` and picked church-bulletin.org/bulletin/immaculate-conception-church-saint-teresa-of-calcutta-parish-montclair-nj-07042/2026-11-01.pdf, the 1 November 2026 issue read above (date from the file name, as the issue has no text layer); freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied; the rendered masthead confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open for the row.
