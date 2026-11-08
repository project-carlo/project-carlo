---
name: Our Lady of Perpetual Help, Oakland
website: https://www.olphoakland.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:2310']
group: ''
evidence:
- url: https://files.ecatholic.com/2310/bulletins/20261101.pdf
  seen: 2026-11-03
  note: '1 November 2026 issue, 8 pages, image-only (no text layer; page 1 read rendered with render.py).
    Masthead: ''The Catholic Parish of Our Lady of Perpetual Help, 117 Franklin Ave., Oakland, NJ 07436'',
    The Solemnity of All Saints, November 1, 2026; Rev. Dr. Robert P. McLaughlin, Administrator; Mass
    Schedule: Saturday 5:00 pm; Sunday 8:00 am/10:00 am/12pm (Sept.-June); Monday to Saturday 8:30 am;
    Holy Days 7:00 pm. No other church named.'
- url: https://www.olphoakland.org/
  seen: 2026-11-03
  note: eCatholic site 'Our Lady of Perpetual Help Church | Oakland, NJ' embedding ecatholic:2310, footer
    address '117 Franklin Avenue / Oakland, NJ 07436'; behind Cloudflare (probe get 403), read in a browser
    (parish-site-access visit.py).
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

Our Lady of Perpetual Help, Oakland, publishes its own weekly bulletin on its eCatholic site (site id 2310). I read page 1 of the 1 November 2026 issue, rendered because the PDF has no text layer: the masthead reads "The Catholic Parish of Our Lady of Perpetual Help, 117 Franklin Ave., Oakland, NJ 07436", November 1, 2026, with Rev. Dr. Robert P. McLaughlin as administrator and one Mass schedule (Saturday 5:00 pm; Sunday 8:00, 10:00 am and 12 pm, September-June; Monday-Saturday 8:30 am).

## Worship sites

- Our Lady of Perpetual Help Church (`our-lady-of-perpetual-help-oakland`): the only church the bulletin names.

The archdiocese directory (160) and GCatholic (18525) list only this church, at 25 Purdue Avenue; the parish gives 117 Franklin Avenue (see the church record).

## Website and bulletin provider

olphoakland.org is an eCatholic site behind Cloudflare (`probe get` 403; `visit.py` loaded it and reported `ecatholic:2310`). Issues fetch directly from files.ecatholic.com/2310/bulletins/YYYYMMDD.pdf. Provider `ecatholic`, read from the website. GCatholic's old URL olphchurch-oaklandnj.org was not used.

Fetch check (2026-11-03): transport ok, PDF, picked `files.ecatholic.com/2310/bulletins/20261101.pdf` (`fresh`), the 1 November issue read above.

## Not yet confirmed

Nothing open. The issues are image-only, so the text the pipeline extracts depends on OCR.
