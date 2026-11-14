---
name: Holy Family Roman Catholic Church
website: https://holyfamilyparishny.org
bulletin_provider: ecatholic
provider_id: '36423'
publication: ['ecatholic:36423']
group: ''
evidence:
- url: https://files.ecatholic.com/36423/bulletins/20261101.pdf
  seen: 2026-11-12
  note: 'Page 1 (image only, no text layer; read rendered with parish-site-access render.py) of the 1
    November 2026 issue: masthead "HOLY FAMILY ROMAN CATHOLIC CHURCH", "17 Fordham Ave Hicksville, New
    York 11801"; Mass schedule Saturday 9:00am, 5:00pm Vigil; Sunday 7:30am, 9:00am, 10:30am, 12:00pm,
    5:00pm; weekdays Monday-Friday 7:00am, 9:00am. One church only.'
- url: https://holyfamilyparishny.org/bulletins
  seen: 2026-11-12
  note: The parish's eCatholic site (read with visit.py). Its Bulletin page lists weekly issues files.ecatholic.com/36423/bulletins/20260726.pdf
    through 20261101.pdf; the 8 November issue was not yet there (homepage showed a PNG of it).
promoted: 2026-11-13
research:
- method: Reconcile fetch:check of the whole diocese; probe get on files.ecatholic.com/36423/bulletins/20261108.pdf
    and 20261115.pdf; visit.py on the home page
  url: https://holyfamilyparishny.org/
  checked: '2026-11-13'
  outcome: not-found
  next_action: fetch:check picked the 1 November issue (20261101.pdf, HTTP 200, 12 days old); 20261108.pdf
    and 20261115.pdf answer 403 (not posted), while the home page shows the 8 November issue only as an
    image (documents/2026/11/November%208%20Holy%20Family%20Bulletin.png). Rerun fetch:check; if the PDF
    archive stays two or more weeks behind, consider an unsupported row with a gap for image-only current
    issues.
  retry_when: After Sunday 15 November 2026, once the parish posts 20261108.pdf or a later PDF
bulletin_status: available
---

## Publisher

Holy Family, 17 Fordham Avenue, Hicksville publishes its own weekly bulletin on eCatholic (site id 36423). Page 1 of the 1 November 2026 issue (`https://files.ecatholic.com/36423/bulletins/20261101.pdf`, 16 pages) has the masthead "HOLY FAMILY ROMAN CATHOLIC CHURCH" with the Fordham Ave address and a Mass schedule for this one church: Saturday 9:00am and 5:00pm Vigil; Sunday 7:30am, 9:00am, 10:30am, 12:00pm and 5:00pm; Monday-Friday 7:00am and 9:00am. This agrees with the diocese's Mass-times page (roster `mass-times:church-of-holy-family-hicksville`).

## Worship sites

One: the church at 17 Fordham Avenue (`holy-family-hicksville-church`). The diocesan locator (directory:7), GCatholic (16860) and the Mass-times page list only this building, and the bulletin's schedule names no other place.

## Website and bulletin provider

holyfamilyparishny.org is the directory's and GCatholic's link and is hosted on eCatholic (visit.py found `ecatholic:36423`; `probe url` reached it too). Issues are at `files.ecatholic.com/36423/bulletins/<YYYYMMDD>.pdf`, dated by the Sunday. The issues of 18 October, 25 October and 1 November 2026 have no text layer (all 16 pages are images), so the pipeline has to read them as images; the quotes above come from a rendered page and `recheck` can't find them in the text.

## Not yet confirmed

Nothing open for the row. The 8 November file (20261108) answered 403 on 2026-11-12, i.e. not yet posted; the site shows it as a PNG on the homepage.
