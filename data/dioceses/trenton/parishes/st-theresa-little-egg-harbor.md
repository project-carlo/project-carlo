---
name: St. Theresa Catholic Parish
website: https://sttheresa450.org/
bulletin_provider: other
provider_id: page-pdfs https://sttheresa450.org/weekly-parish-bulletins
publication: ['url:https://sttheresa450.org/weekly-parish-bulletins', 'ecatholic:5085']
group: Cohort 30 (Barnegat, Long Beach Island, Little Egg Harbor)
evidence:
- url: https://files.ecatholic.com/5085/documents/2026/10/C84880_2026_11_01.pdf
  seen: 2026-10-30
  quote: 450 Radio Road • Little Egg Harbor, New Jersey 08087
  note: 'Page 1 of the 1 November 2026 issue (12 pages, text layer): ''The Parish of St. Theresa'', pastor
    Rev. Selvam J. Asirvatham, ''MASS SCHEDULE Monday - Friday: 8:00 am (Daily Chapel); Saturday Vigil:
    4:00 pm & Sunday: 7:30 am, 9:00 am & 11:30 am''. Pages 10-12 are Bon Venture Services advertising
    pages (''C84880 (CK) • St. Theresa - Little Egg Harbor, NJ''). Names this parish alone.'
- url: https://sttheresa450.org/weekly-parish-bulletins
  seen: 2026-10-30
  quote: Weekly Parish Bulletins
  note: 'Parish eCatholic site (id 5085, plain fetch reads it). Its Weekly Parish Bulletins page links
    dated PDFs under files.ecatholic.com/5085/documents/2026/<m>/ (newest ''November 1, 2026'', then October
    25, 17 (file C84880_2026_10_18), 11, 4 ...), read with visit.py --links. These are /documents/ uploads,
    not /bulletins/ files: issues.py ecatholic 5085 finds none (403 for every Sunday 11 Oct-1 Nov).'
- url: https://www.church-bulletin.org/saint-theresa-parish-little-egg-harbor-nj-08087
  seen: 2026-10-30
  note: 'John Patrick Publishing listing 545 for ''Saint Theresa Parish, Little Egg Harbor, NJ 08087''
    has no edition (tools/jppc-trenton.tsv): not this parish''s channel.'
- url: https://dioceseoftrenton.org/parishfinder
  seen: 2026-10-30
  note: Finder pin directory:14658 'St. Theresa Catholic Parish', 450 Radio Rd, Little Egg Harbor Township
    08087-1882, (609) 296-2504, website sttheresa450.org. GCatholic's sttheresa-littleeggharbor.com has
    no DNS.
research:
- method: issues.py ecatholic 5085 (weeks 11 Oct-1 Nov) and fetch:check with the ecatholic provider
  url: https://files.ecatholic.com/5085/bulletins/20140119.pdf
  checked: '2026-10-30'
  outcome: not-found
  next_action: 'Use the `other` row on the Weekly Parish Bulletins page: the eCatholic resolver picks
    /bulletins/20140119.pdf (2014) because the current issues are /documents/ uploads.'
  retry_when: The parish starts posting to /bulletins/<yyyymmdd>.pdf
- method: fetch:check on the row (page-pdfs sttheresa450.org/weekly-parish-bulletins), run 2026-10-30
  url: https://files.ecatholic.com/5085/documents/2026/10/C84880_2026_11_01.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: 'The pick is the correct current issue (1 November 2026, 12 pages, 5.8 MB). Identity is
    unverified and the issue date unknown only because the first 2000 characters of page 1 are the staff
    list: ''The Parish of St. Theresa'' and ''NOVEMBER 1, 2026'' come after the Mass schedule on the same
    page. Run with --expected-identity Theresa fails for that reason.'
  retry_when: The pick stops being the newest dated PDF on the page
bulletin_status: available
publication_reviews:
- parish: st-mary-barnegat
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/5085/documents/2026/10/C84880_2026_11_01.pdf
    seen: 2026-10-30
    quote: 450 Radio Road
    note: The 1 November 2026 masthead of St. Theresa's bulletin names the Parish of St. Theresa, 450
      Radio Road alone, with its own pastor and Mass schedule.
- parish: st-francis-of-assisi-long-beach-island
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/5085/documents/2026/10/C84880_2026_11_01.pdf
    seen: 2026-10-30
    quote: 450 Radio Road
    note: The 1 November 2026 masthead of St. Theresa's bulletin names the Parish of St. Theresa, 450
      Radio Road alone, with its own pastor and Mass schedule.
---

## Publisher

St. Theresa Parish (Little Egg Harbor) publishes its own weekly bulletin, printed by Bon Venture Services (advertising pages carry the account code C84880) and posted on the parish's eCatholic site (id 5085). The 1 November 2026 issue has a text layer and names this parish alone, with one Mass schedule for one church.

## Worship sites

One church, St. Theresa, 450 Radio Road (`st-theresa-little-egg-harbor`). The schedule's "Daily Chapel" (weekday 8:00 am Mass; adoration Fridays) is inside the church campus and has no street address of its own, so it is not a second church (*Rules settled*, jackson-lakehurst-whiting). GCatholic lists St. Theresa only.

## Website and bulletin provider

eCatholic id 5085, `ecatholic` row on sttheresa450.org. The bulletins are `/documents/` uploads on the parish's Weekly Parish Bulletins page rather than `/bulletins/<yyyymmdd>.pdf` files; see the fetch check in *Not yet confirmed*. The John Patrick listing 545 is empty and is not this parish's channel.

## Not yet confirmed

The `fetch:check` run on 2026-10-30 picks the right file (the 1 November 2026 issue) but cannot verify identity or date from the first 2000 characters of page 1, which are the staff list; the parish name and "NOVEMBER 1, 2026" come later on the same page (see research).
