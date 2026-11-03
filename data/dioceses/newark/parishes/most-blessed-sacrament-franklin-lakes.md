---
name: Most Blessed Sacrament, Franklin Lakes
website: https://mostblessedsacrament.ws/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:14258']
group: Planning Area A
evidence:
- url: https://files.ecatholic.com/14258/bulletins/20261101.pdf
  seen: 2026-11-03
  note: '1 November 2026 issue, 16 pages, image-only (no text layer; read pages 1-2 rendered with parish-site-access
    render.py). Page 1 masthead: ''Most Blessed Sacrament Roman Catholic Church, Franklin Lakes, New Jersey'',
    The Solemnity of All Saints, November 1, 2026. Page 2: parish office 787 Franklin Lake Road, Franklin
    Lakes, New Jersey 07417; Rev. John R. Job, Pastor; MASS SCHEDULE: Saturday 5:30 pm; Sunday 8:00 am,
    10:00 am, 12:00 pm; Weekdays Monday and Saturday 9:00 am, Tuesday-Friday 7:30 am. No other church
    named. Footer ''0697 - Page 2'' (John Patrick Publishing layout number).'
- url: https://mostblessedsacrament.ws/
  seen: 2026-11-03
  note: eCatholic site 'Church of the Most Blessed Sacrament - Franklin Lakes, NJ' embedding ecatholic:14258
    and linking /bulletins; behind Cloudflare (probe get 403), read in a browser (parish-site-access visit.py).
bulletin_status: available
---

## Publisher

Most Blessed Sacrament, 787 Franklin Lake Road, Franklin Lakes, publishes its own weekly bulletin on its eCatholic site (site id 14258). I read pages 1-2 of the 1 November 2026 issue, rendered as images because the PDF has no text layer: page 1's masthead reads "Most Blessed Sacrament Roman Catholic Church, Franklin Lakes, New Jersey", November 1, 2026; page 2 gives the parish office at 787 Franklin Lake Road, Rev. John R. Job as pastor, and one Mass schedule (Saturday 5:30 pm; Sunday 8:00 am, 10:00 am, 12:00 pm; Monday and Saturday 9:00 am, Tuesday-Friday 7:30 am). The page footer "0697 - Page 2" is a John Patrick Publishing layout number; the parish posts the issue to its own eCatholic site.

## Worship sites

- Most Blessed Sacrament Church, 787 Franklin Lake Road (`most-blessed-sacrament-franklin-lakes`): the only church the bulletin names.

The archdiocese directory (48) and GCatholic (18407, "Blessed Sacrament") list only this church.

## Website and bulletin provider

mostblessedsacrament.ws is an eCatholic site behind Cloudflare (`probe get` 403; `visit.py` loaded it and reported `ecatholic:14258`). Issues fetch directly from files.ecatholic.com/14258/bulletins/YYYYMMDD.pdf. Provider `ecatholic`, read from the website.

Fetch check (2026-11-03): transport ok, PDF, picked `files.ecatholic.com/14258/bulletins/20261101.pdf` (`fresh`), the 1 November issue read above.

## Not yet confirmed

Nothing open. The issues are image-only, so the text the pipeline extracts depends on OCR.
