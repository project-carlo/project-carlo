---
name: St. Camillus-St. Virgilius (Rockaway Park)
website: https://stcstv.com/
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://stcstv.com/news-events/bulletin#st-camillus-st-virgilius']
group: Deanery Q10 (Queens East)
evidence:
- url: https://stcstv.com/news-events/bulletin/1428-11-08-26/file
  seen: 2026-11-06
  quote: St. Camillus - St. Virgilius
  note: '8 November 2026 issue (DOCman title ''11-08-26'', a Word PDF created 4 November 2026), downloaded
    through the browser with tools/browser-pdf.py. Page 1 masthead ''The Roman Catholic Parish of St.
    Camillus - St. Virgilius / Rockaway Park & Broad Channel'', Very Rev. James Kuroly, Administrator;
    two churches with their own schedules: St. Camillus Church, 99-21 Rockaway Beach Blvd. (Sundays 11:30
    am) and St. Virgilius Church, 14 Noel Road (Saturday Vigil 4 pm, Sundays 10:00 am); parish office
    16 Noel Road, Broad Channel.'
- url: https://stcstv.com/news-events/bulletin
  seen: 2026-11-06
  note: 'Bulletin page (403 to probe url; read with parish-site-access visit.py). Site title ''The Roman
    Catholic Parishes of St. Rose of Lima & St. Camillus - St. Virgilius''. DOCman list newest first:
    11-08-26, 11-01-26, 10-25-26, 10-18-26, 10-11-26 … 08-16-26, each /news-events/bulletin/<id>-<date>/file.'
- url: https://parishesonline.com/organization/st-camillus-church
  seen: 2026-11-06
  note: 'probe po: org ''St. Camillus Church'' (lpi 0018000000QxBKMAA3) exists but lists no issues, so
    it is not this bulletin''s publication id. No org at st-camillus-st-virgilius-church-11694, st-camillus-church-11694,
    st-camillus-st-virgilius-11694, st-camillus-st-virgilius-church-11693 or st-virgilius-church-11693.'
research:
- method: fetch:check unpinned and with page-pdfs https://stcstv.com/news-events/bulletin
  url: https://stcstv.com/news-events/bulletin
  checked: '2026-11-06'
  outcome: unsupported-format
  next_action: Re-run fetch:check when a collector can read Joomla DOCman /file links through the browser
    (pnpm diocese gaps, kind joomla-docman-file-403)
  retry_when: A fetch collector for DOCman /file links behind 403 lands
bulletin_status: available
fetch_gap:
  kind: joomla-docman-file-403
  seen: 2026-11-06
  note: Joomla DOCman list at /news-events/bulletin, newest first ('11-08-26' = /news-events/bulletin/1428-11-08-26/file).
    The page and every /file link answer 403 to probe get and fetch; fetch:check (unpinned and with page-pdfs
    https://stcstv.com/news-events/bulletin) fails 'No PDF links found'. The files open in the browser
    (tools/browser-pdf.py).
  url: https://stcstv.com/news-events/bulletin
---

## Publisher

The parish makes its own bulletin (a Microsoft Word PDF, no publisher footer) and posts it weekly on its Joomla site's DOCman list at `stcstv.com/news-events/bulletin`. The issue read is 8 November 2026 (`/news-events/bulletin/1428-11-08-26/file`, created 4 November, read 2026-11-06 through the browser). Page 1 masthead: "The Roman Catholic Parish of St. Camillus - St. Virgilius / Rockaway Park & Broad Channel", Very Rev. James Kuroly, MA, Ed.D, Administrator, Deacon Michael Pearce; parish office 16 Noel Road, Broad Channel, NY 11693. The issue has no LPi footer, and the ParishesOnline org `st-camillus-church` that exists has no issues.

## Worship sites

Two churches, each with its own Mass schedule on page 1: St. Camillus Church, 99-21 Rockaway Beach Blvd., Rockaway Park (Sundays 11:30 am; first Saturday 12 noon) and St. Virgilius Church, 14 Noel Road, Broad Channel (Saturday Vigil 4 pm; Sundays 10:00 am). The week's Mass intentions list both. So St. Virgilius, which GCatholic lists, is open, not closed. The diocese directory and deanery list (Q10) list the parish once at 99-15 Rockaway Beach Blvd.; the Mass finder's place 1189 'St. Camillus-St. Virgilius (St. Camillus)' gives 16 Noel Road but is pinned on St. Camillus.

The site's title is "The Roman Catholic Parishes of St. Rose of Lima & St. Camillus - St. Virgilius", and the bulletin carries St. Rose of Lima's DRE contact and St. Rose of Lima Catholic Academy news, so the two parishes share leadership. The 8 November masthead names St. Camillus-St. Virgilius alone and its schedule lists no St. Rose of Lima Mass, so this row is this bulletin only; whether St. Rose of Lima (Rockaway Beach, another batch) publishes its own bulletin is left to that batch.

## Website and bulletin provider

`unsupported`, `fetch_gap` `joomla-docman-file-403`. The website is the parish site `stcstv.com` (the directory's URL). The site answers 403 to `probe url` and `probe get` and loads in visit.py; the DOCman `/file` links answer 403 to fetch. `fetch:check` (2026-11-06) failed both unpinned ("No PDF links found on bulletin post page") and with `page-pdfs https://stcstv.com/news-events/bulletin` ("No PDF links found on bulletin page"). No ParishesOnline container carries the issues. The issues are text PDFs once downloaded through the browser (`tools/browser-pdf.py`).

## Not yet confirmed

Whether the bulletin is posted anywhere fetch can read (the parish's Facebook page was not checked). See research.
