---
name: St. Junipero Serra Parish
website: https://www.stjuniperoserra.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=4142
publication: ['url:http://sponsors.bonventure.net/?page=4142']
group: Cohort 21 (Bay Head, Lavallette, Seaside)
evidence:
- url: http://sponsors.bonventure.net/pdfs/4142/2026-11-01.pdf
  seen: 2026-10-30
  quote: Dos Templos en una Parroquia UNIDA
  note: 'Page 1 of the 1 November 2026 issue (8 pages, text layer; md5 of the file e3c3c4e2a15a0705ace462adb94938e8):
    header ''50 E Street • Seaside Park, NJ 08752, 732-793-0041 / www.stjuniperoserra.org'', ''Served
    by the Franciscan Friars Conventual'', ''Two Houses of Worship in ONE UNITED Parish'' (the English
    words are font-garbled in the text layer; the Spanish line is readable), then each church''s Sunday
    and daily Masses: Our Lady of Perpetual Help, 100 Grant Avenue, Seaside Heights, and St. Catharine
    of Siena Church, 50 E Street, Seaside Park. It names this parish alone.'
- url: http://sponsors.bonventure.net/?page=4142
  seen: 2026-10-30
  note: Bon Venture sponsor page 4142, linked from the parish's homepage; dated issues are posted weekly
    (pdfs/4142/2026-11-01.pdf is the newest, back to 2018-07-01, the month the parish began).
- url: https://www.stjuniperoserra.org/about-our-parish/
  seen: 2026-10-30
  quote: Saint Junipero Serra Parish began on July 1, 2018 as a union of Our Lady of Perpetual Help Church
    in Seaside Heights and Saint Catharine of Siena Church in Seaside Park.
  note: 'The parish''s About page: ''one united diverse parish with the good fortune of having two churches
    on two different campuses''. The homepage''s only bulletin link is the Bon Venture page; the site
    has no archive of its own. The finder''s pin is directory:14641 ''St. Junipero Serra Parish'', 50
    E St, Seaside Park 08752-1509.'
- url: https://www.stjuniperoserra.org/liturgy-worship/
  seen: 2026-10-30
  note: 'Liturgy page: Saturday Vigil 4:00PM at Our Lady of Perpetual Help, 4:30PM at St. Catharine of
    Siena; Sunday 8:00 AM and 11:00 AM at St. Catharine, 9:30 AM and 7:00 PM Spanish Mass at Our Lady
    of Perpetual Help.'
research:
- method: 'Compared page 1 of the 2 August 2026, 1 February 2026 and 1 November 2026 issues on Bon Venture
    4142 (the barrier island''s seasonal-shore question): both Seaside churches list the same Sunday Masses
    in summer and winter. The cohort neighbours Lavallette and Bay Head print a different bulletin (John
    Patrick 6003).'
  url: http://sponsors.bonventure.net/?page=4142
  checked: '2026-10-30'
  outcome: found
  next_action: None
- method: 'pnpm fetch:check --diocese trenton --parish st-junipero-serra-seaside-park (headed Chrome,
    page-pdfs on the Bon Venture page): picked pdfs/4142/2026-11-01.pdf; transport ok, document_type pdf,
    freshness future (the coming Sunday, posted early), identity unverified by the tool (the English headings
    are font-garbled); identity read from the issue''s page 1 text instead.'
  url: http://sponsors.bonventure.net/?page=4142
  checked: '2026-10-30'
  outcome: found
  next_action: None; the pick is the current bulletin. No `recipe` line was printed (the stored page-pdfs
    provider_id already resolves).
bulletin_status: available
---

## Publisher

St. Junipero Serra Parish, Seaside Park, publishes one weekly bulletin through Bon Venture (sponsor page 4142), carrying both of its churches. The 1 November 2026 issue has a text layer (the English headings are font-garbled; the Mass lines read) and its first page prints one parish address, 50 E Street, with "Dos Templos en una Parroquia UNIDA" and the two churches' Masses side by side, so one row, two churches. The parish was formed on 1 July 2018 by the merger of Our Lady of Perpetual Help, Seaside Heights and St. Catharine of Siena, Seaside Park (the About page), the merger the 2017 decisions planned. GCatholic still lists the two as separate churches under their old names; both are worship sites of this one parish.

## Website and bulletin provider

The finder's site, stjuniperoserra.org, is the parish's own WordPress site and links the Bon Venture page as its only bulletin; the row uses the site as `website` and `page-pdfs` on the Bon Venture page (`http://`, per the playbook: https fails certificate verification). GCatholic's stcatharinesiena.com and ourladyph.com are the old parishes' domains and are not used. The cohort neighbours St. Pio and Sacred Heart print a John Patrick bulletin (listing 6003), so there is no bulletin shared across the cohort; the rest of Cohort 21's shape is in `st-pio-of-pietrelcina-lavallette`.

## Worship sites

Two: St. Catharine of Siena Church, 50 E Street, Seaside Park and Our Lady of Perpetual Help Church, 100 Grant Avenue, Seaside Heights (`st-catharine-of-siena-seaside-park`, `our-lady-of-perpetual-help-seaside-heights`). Both appear with the same Sunday Masses in the 1 February, 2 August and 1 November 2026 issues, so neither is seasonal on this evidence.
