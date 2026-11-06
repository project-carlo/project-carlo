---
name: Our Lady of Mount Carmel Oratory, Montclair
website: https://olmcmontclair.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6030
publication: ['url:https://www.church-bulletin.org/our-lady-of-mount-carmel-oratory-montclair-nj-07042']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-of-mount-carmel-oratory-montclair-nj-07042/2026-11-01.pdf
  seen: 2026-11-03
  note: '1 November 2026 issue, 8 pages, image only (read with render.py; recheck can''t find quotes).
    Page 1 masthead: ''A Catholic Oratory of the Archdiocese of Newark / Our Lady of Mount Carmel / Montclair
    / Celebrating Our 120th Anniversary'', ''94 Pine Street • Montclair, NJ 07042'', ''Bulletin for the
    Feast of All Saints November 1st, 2026'', with the Mass schedule (weekday 08:30 AM M, W, Th, F; Saturday
    04:30 PM vigil in English, 06:30 PM Neocatechumenal Mass in Church Hall; Sunday 11:00 AM English,
    06:00 PM Spanish). Page 8 footer: ''6030 Our Lady of Mount Carmel Oratory, Montclair, NJ (B) … John
    Patrick Publishing Co.'''
- url: https://church-bulletin.org/6030
  seen: 2026-11-03
  note: 'Redirects to church-bulletin.org/our-lady-of-mount-carmel-oratory-montclair-nj-07042: dated issues
    2026-11-01, 10-25, 10-18, 10-11 and earlier. Found with jp_scan.sh output from earlier batches; the
    oratory''s site does not link it.'
- url: https://olmcmontclair.org/wp-content/uploads/2026/10/59-November-1-OLMC-Final.pdf
  seen: 2026-11-03
  note: 'The oratory''s own copy of the 1 November 2026 issue: the same pages 1-7 as the John Patrick
    issue, without the ad page (image only).'
- url: https://olmcmontclair.org/feast-of-all-saints-november-1-2026/
  seen: 2026-11-03
  quote: Feast of All Saints
  note: WordPress post in category Bulletin linking wp-content/uploads/2026/10/59-November-1-OLMC-Final.pdf;
    earlier posts weekly back to 30 August 2026 (22nd Sunday in Ordinary Time).
- url: https://olmcmontclair.org/mass-times/
  seen: 2026-11-03
  quote: 'Neocatechumenal Mass: Saturday 8:00 PM (Church Hall)'
  note: 'Weekend: Saturday (English) 4:30 PM; Sunday (English) 11:00 AM; Sunday (Spanish) 6:00 PM; weekdays
    Monday, Wednesday, Thursday, Friday 8:30 AM. Footer: ''An Oratory of the Archdiocese of Newark … 94
    Pine Street, Montclair, NJ 07042''.'
bulletin_status: available
publication_reviews:
- parish: st-teresa-of-calcutta-montclair
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-mount-carmel-oratory-montclair-nj-07042/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Our Lady of Mount Carmel, Montclair, an oratory at 94 Pine
      Street, alone, with its own Mass schedule; John Patrick id 6030.
  - url: https://www.church-bulletin.org/bulletin/immaculate-conception-church-saint-teresa-of-calcutta-parish-montclair-nj-07042/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Immaculate Conception Church, St Teresa of Calcutta Parish,
      with a Mass schedule for Immaculate Conception alone; John Patrick id 6037.
---

## Publisher

Our Lady of Mount Carmel Oratory, Montclair, publishes a weekly bulletin printed by John Patrick Publishing (id 6030). I read the 1 November 2026 issue (image only, rendered): page 1 masthead 'A Catholic Oratory of the Archdiocese of Newark / Our Lady of Mount Carmel / Montclair', '94 Pine Street • Montclair, NJ 07042', with its own Mass schedule; page 8 footer '6030 Our Lady of Mount Carmel Oratory, Montclair, NJ (B) … John Patrick Publishing Co.'. The oratory also posts each issue (without the ad page) as a WordPress post in the Bulletin category of olmcmontclair.org.

## Worship sites

- Our Lady of Mount Carmel, 94 Pine Street (`our-lady-of-mount-carmel-montclair`): Saturday 4:30 pm (English); Sunday 11:00 am (English), 6:00 pm (Spanish); Monday, Wednesday, Thursday, Friday 8:30 am; a Saturday Neocatechumenal Mass in the church hall (6:30 pm in the bulletin, 8:00 pm on the Mass Times page).

The parish of Our Lady of Mount Carmel (Italian) was merged into St. Teresa of Calcutta (rcan.org closed/merged records table, May 2025), and the archdiocese lists the church as an oratory (directory 118; planning area list: 'Our Lady of Mt. Carmel Oratory-St. Teresa of Calcutta'). Its bulletin is separate from St. Teresa of Calcutta's (John Patrick 6037), whose 1 November 2026 issue gives a Mass schedule for Immaculate Conception alone, so the oratory is its own row (`publication_reviews`).

## Website and bulletin provider

https://olmcmontclair.org/ is WordPress; its Bulletin category (/category/bulletin/) has one post per week wrapping the PDF (wp-content/uploads/2026/10/59-November-1-OLMC-Final.pdf for 1 November), and a first fetch:check with no pin read it with `dated-post https://olmcmontclair.org/category/bulletin/`. The site doesn't link John Patrick, but the publisher's listing has dated file names and the complete issue, so the row is pinned to `page-pdfs https://church-bulletin.org/6030` (the playbook's John Patrick pin); the dated-post recipe is the fallback if the listing stops. The issues are image only: the pipeline will need to read them as images.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/6030: current` and picked church-bulletin.org/bulletin/our-lady-of-mount-carmel-oratory-montclair-nj-07042/2026-11-01.pdf, the 1 November 2026 issue read above; freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

The Saturday Neocatechumenal Mass time differs between the bulletin (6:30 pm) and the Mass Times page (8:00 pm); it does not affect the row.
