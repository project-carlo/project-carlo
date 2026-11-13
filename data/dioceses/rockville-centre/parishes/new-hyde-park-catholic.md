---
name: New Hyde Park Catholic (Notre Dame and Holy Spirit)
website: https://newhydeparkcatholic.com/bulletins/
bulletin_provider: other
provider_id: page-pdfs https://newhydeparkcatholic.com/bulletins/
publication: ['url:https://newhydeparkcatholic.com/bulletins/#new-hyde-park-catholic']
group: New Hyde Park Catholic
evidence:
- url: https://newhydeparkcatholic.com/wp-content/uploads/2026/11/Bulletin-1115.pdf
  seen: 2026-11-13
  quote: NHP Catholic Mass Schedule
  note: Issue for November 15, 2026 (24 pages, Canva). Cover masthead 'New Hyde Park Catholic'. Page 2
    (image, rendered) names Notre Dame Church (5 Mayfair Road) and Holy Spirit Church (16 South 6th Street),
    Rev. John J. McCartney Pastor, Rev. John Crozier and Rev. Augustine Aka Parochial Vicars. Page 3 (image)
    lists Notre Dame Mass Times (Sunday 7:00, 9:00, 10:30am, 12:00pm, 7:00pm Spanish; Saturday 8:30am,
    5:00pm Vigil; Mon-Fri 8:30am, 12:05pm) and Holy Spirit Mass Times (Sunday 8:00, 11:30am; Saturday
    4:00pm Vigil; Mon-Thu 8:00am; Syro-Malabar Sunday 5:00pm, Tuesday 6:00pm, Friday 9:30am). Downloaded
    through Chrome (tools/browser_get.py); probe pdf was disconnected.
- url: https://newhydeparkcatholic.com/bulletins/
  seen: 2026-11-13
  note: 'Bulletins page, read with parish-site-access visit.py: CURRENT ISSUE November 15, 2026 (Bulletin-1115.pdf),
    then past issues newest first; links to Past Notre Dame Bulletins and Past Holy Spirit Bulletins (the
    older separate archives).'
promoted: 2026-11-13
bulletin_status: available
---

## Publisher

Notre Dame and Holy Spirit, the two parishes of New Hyde Park, publish one weekly bulletin as "New Hyde Park Catholic". The issue for November 15, 2026 (`https://newhydeparkcatholic.com/wp-content/uploads/2026/11/Bulletin-1115.pdf`, 24 pages, made in Canva, read 2026-11-13) has the cover "New Hyde Park Catholic, The Thirty-third Sunday in Ordinary Time, November 15, 2026". Page 2 (an image, rendered) heads "Welcome to New Hyde Park Catholic" and names Notre Dame Church, 5 Mayfair Road, and Holy Spirit Church, 16 South 6th Street, with one clergy list: Rev. John J. McCartney, Pastor; Rev. John Crozier and Rev. Augustine Aka, Parochial Vicars; Msgr. Charles R. Fink, in residence. Page 3 (image) is the "NHP Catholic Mass Schedule" with a Notre Dame and a Holy Spirit section. The Mass intentions (text) list both churches.

## Worship sites

Two: Notre Dame Church, 45 Mayfair Road (`notre-dame-new-hyde-park-church`) and Holy Spirit Church, 16 South 6th Street (`holy-spirit-new-hyde-park-church`), the two sections of the bulletin's Mass schedule. The diocesan locator (directory:13, directory:10), GCatholic (16891, 16890) and the drvc.org Mass-times page list the same two churches. Holy Spirit also hosts Syro-Malabar Masses (Sunday 5:00pm, Tuesday 6:00pm, Friday 9:30am, per page 3); they are another jurisdiction's services in the same building, not a separate worship site here. Notre Dame Catholic School (25 Mayfair Road) and the Parish Center (5 Mayfair Road) are not Mass sites.

## Website and bulletin provider

newhydeparkcatholic.com (WordPress, "Design by Startup Catholic") is the locator's link for Holy Spirit. Its `/bulletins/` page lists the current joint issue first, then past issues newest first, as `wp-content/uploads/<yyyy>/<mm>/Bulletin-<mmdd>.pdf` (older ones `Bulletin-<Month>-<d>.pdf`). `probe url` and `probe pdf` could not connect; the site loads in the browser. Holy Spirit's former domain holyspiritnhp.com (the Mass-times page's link) is now a casino spam squat (visit.py, 2026-11-13); notredamenhp.org shows a Squarespace "Coming Soon" page. GCatholic's holyspiritchurch.com was not used. The bulletin's Mass schedule is an image (page 3), so the pipeline needs OCR for times.

`fetch:check` (2026-11-13) with page-pdfs on `/bulletins/` picked `Bulletin-1115.pdf`, the November 15, 2026 issue, the newest posted; it skipped the old per-parish archive pages (last issues 2025-03-30).

## Not yet confirmed

Nothing open.
