---
name: Church of St. Paul the Apostle
website: https://stpaulbrookville.org/bulletin-2/
bulletin_provider: other
provider_id: page-pdfs https://stpaulbrookville.org/bulletin-2/
publication: ['url:https://stpaulbrookville.org/bulletin-2/']
group: ''
evidence:
- url: https://stpaulbrookville.org/wp-content/uploads/sites/111/2026/11/nov8_2026_stpaul_compressed.pdf
  seen: 2026-11-13
  note: 'Page 1 masthead of the 8 November 2026 issue (12 pages, PDF Creator Canva; downloaded through
    Chrome with tools/browser_get.py because probe get got RemoteDisconnected): ''Church of St. Paul the
    Apostle'', 2534 Cedar Swamp Road, Brookville, New York 11545; Pastor Rev. Msgr. James F. Pereda, J.C.D.
    MASS SCHEDULE Saturday 5:00pm; Sunday 8:30 and 10:30am; Weekday Monday-Friday, 9am in the Church.'
- url: https://stpaulbrookville.org/bulletin-2/
  seen: 2026-11-13
  note: 'Read with visit.py: ''This Week''s Bulletin: November 8, 2026'' (nov8_2026_stpaul_compressed.pdf)
    and a Bulletin Archive back to May 2026, files under wp-content/uploads/sites/111/<YYYY>/<MM>/.'
- url: https://www.stpaulsbrookville.org/
  seen: 2026-11-13
  note: The locator's link is an old Weebly page giving the parish address and pastor, with no bulletin;
    its logo links https://stpaulbrookville.org/.
promoted: 2026-11-13
bulletin_status: available
---

## Publisher

St. Paul the Apostle, 2534 Cedar Swamp Road, Brookville publishes its own weekly bulletin, laid out by the parish in Canva. The 8 November 2026 issue (`https://stpaulbrookville.org/wp-content/uploads/sites/111/2026/11/nov8_2026_stpaul_compressed.pdf`, 12 pages, read 2026-11-13) has the page-1 masthead "Church of St. Paul the Apostle, 2534 Cedar Swamp Road, Brookville, New York 11545", names "Rev. Msgr. James F. Pereda, J.C.D." as pastor, and gives the MASS SCHEDULE: Saturday 5:00pm; Sunday 8:30 and 10:30am; Weekday Monday-Friday, 9am in the Church.

The Mass-times page (roster entry read 2026-11-12) gives Sunday 8:00, 9:30 and 11:00 AM and weekdays 8:00 AM, an older schedule; the bulletin is followed.

## Worship sites

One: the church at 2534 Cedar Swamp Road (`st-paul-the-apostle-brookville-church`). The bulletin's schedule names no other place. The diocesan locator (directory:60), GCatholic (16819) and the Mass-times page list only this church.

## Website and bulletin provider

The locator and Mass-times page link stpaulsbrookville.org, an old Weebly page with the address and pastor and no bulletin, whose logo links the current site stpaulbrookville.org (no "s"). GCatholic's saintpaulsbrookville.com does not resolve (DNS, 2026-11-13). stpaulbrookville.org is a WordPress multisite member (uploads under `sites/111`) that `probe url` and `probe get` could not reach (UNREACHABLE / RemoteDisconnected) but `visit.py` and Chrome read normally. Its Bulletin page lists "This Week's Bulletin" and an archive, each a PDF named by date (nov8_2026_stpaul_compressed.pdf).

`fetch:check` (2026-11-13) read `page-pdfs` on the Bulletin page and downloaded nov8_2026_stpaul_compressed.pdf, the 8 November 2026 issue; the recipe is recorded in `provider_id`.

## Not yet confirmed

Nothing open.
