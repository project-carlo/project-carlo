---
name: St. Patrick
website: https://stpatricksmithtown.org/bulletins/
bulletin_provider: other
provider_id: page-pdfs https://stpatricksmithtown.org/bulletins/ filename=*Bulletin*.pdf
publication: ['url:https://stpatricksmithtown.org/bulletins/']
group: ''
evidence:
- url: https://stpatricksmithtown.org/wp-content/uploads/2026/11/St.-Patrick-Smithtown-Bulletin-for-11-15-26.pdf
  seen: 2026-11-13
  note: 'Issue for November 15, 2026 (20 pages, Producer ''Microsoft: Print To PDF'', image-only; downloaded
    with browser_get.py and rendered). Page 1 masthead ''St. Patrick R.C. Church / 280 East Main Street,
    Smithtown, New York 11787 / November 15, 2026 - Thirty-third Sunday in Ordinary Time''. Page 3 ''Masses
    for the Week'' lists Sat 5:00 PM; Sun 7:30, 9:00, 10:30 AM, 12:00, 5:00 PM; weekdays 6:45 AM, 9:00
    AM, 12:10 PM, Mon 7:30 PM, all with no other place named; pastor Rev. Msgr. Brian McNamara. No printer
    named.'
- url: https://stpatricksmithtown.org/bulletins/
  seen: 2026-11-13
  note: 'WordPress bulletin page read with parish-site-access visit.py (probe url could not connect: egress
    proxy EOF). Lists St.-Patrick-Smithtown-Bulletin-for-11-15-26.pdf, ...-for-11-8-26.pdf, 11-1-26-St.-Patrick-Smithtown-Bulletin.pdf
    under /wp-content/uploads/.'
promoted: 2026-11-13
bulletin_status: available
---

## Publisher

St. Patrick, Smithtown, publishes its own weekly bulletin on its WordPress site. The 15 November 2026 issue (`https://stpatricksmithtown.org/wp-content/uploads/2026/11/St.-Patrick-Smithtown-Bulletin-for-11-15-26.pdf`, 20 pages, image-only 'Microsoft: Print To PDF'; read by rendering pages 1-3 on 2026-11-13) has the page-1 masthead "St. Patrick R.C. Church / 280 East Main Street, Smithtown, New York 11787" and "November 15, 2026 - Thirty-third Sunday in Ordinary Time". No printer is named.

## Worship sites

One: St. Patrick church, 280 East Main Street (`st-patrick-smithtown-church`). Page 3's "Masses for the Week" (Sat 5:00 PM; Sun 7:30, 9:00, 10:30 AM, 12:00, 5:00 PM; weekdays 6:45 AM, 9:00 AM, 12:10 PM, Mon 7:30 PM) names no other place, and the diocesan locator, GCatholic and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

`stpatricksmithtown.org/bulletins/` lists the issues as PDFs under `/wp-content/uploads/<yyyy>/<mm>/`, newest first. `probe url` and `probe pdf` could not connect (egress proxy EOF / RemoteDisconnected); visit.py and browser_get.py read them. Provider `other` reading that page; see the fetch:check result in `provider_id`.

## Not yet confirmed

Nothing open. The issue's text layer is empty, so the Mass schedule was read from rendered pages.
