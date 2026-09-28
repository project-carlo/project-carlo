---
name: St. Thomas the Apostle Catholic Church
website: https://www.stthomas-church.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:16575', 'po-container:04/0246']
group: ''
evidence:
- url: https://files.ecatholic.com/16575/bulletins/20260927.pdf
  seen: 2026-09-28
  quote: St. Thomas, Delmar, NY 04-0246
  note: 'LPi footer on the advertising pages (11-12) of the 27 September 2026 issue. Pages 1-10 are images
    with no text layer; page 1 (rendered with render.py and read) is the masthead: "St. Thomas the Apostle
    Catholic Church, Delmar, New York, September 27, 2026", "Church 35 Adams Place Delmar, NY 12054",
    "Masses Saturday (Vigil): 5:00pm Sunday: 7:30am, 10:30am, 5:00pm".'
- url: https://container.parishesonline.com/bulletins/04/0246/20260927B.pdf
  seen: 2026-09-28
  quote: St. Thomas, Delmar, NY 04-0246
  note: The same issue in LPi's ParishesOnline container 04/0246; its file has the same MD5 as the eCatholic
    one (4465c19a…), i.e. one bulletin in two places.
- url: https://www.stthomas-church.org/bulletins
  seen: 2026-09-28
  note: The parish's eCatholic site, behind Cloudflare; visit.py (2026-09-28) found ecatholic:16575 on
    it.
promoted: 2026-09-28
---

## Publisher

St. Thomas the Apostle, Delmar, publishes its own weekly bulletin, printed by LPi and
posted both on its eCatholic site (files.ecatholic.com/16575/bulletins/YYYYMMDD.pdf) and in
ParishesOnline container 04/0246; the two 27 September 2026 files are byte-identical. The
cover (an image) is "St. Thomas the Apostle Catholic Church, Delmar, New York", with one
church (35 Adams Place) and its schedule. Page 2 is "A Message from Fr. Matt" (Fr. Matthew
Duclos, also pastor of St. Lucy/St. Bernadette, Altamont, which publishes its own
bulletin).

## Worship sites

One: `st-thomas-the-apostle-delmar`. The school at 42 Adams Place is not a worship site.

## Website and bulletin provider

stthomas-church.org is the parish's eCatholic site (site id 16575), named on the cover and
by the diocese and GCatholic; `fetch` reads eCatholic from the website. The ParishesOnline
container is recorded too; no ParishesOnline organization slug was looked up because the
eCatholic channel is the one fetched.

**Image-only bulletin:** pages 1-10 have no text layer; the pipeline will need to read it
as images.

## Not yet confirmed

Nothing.
