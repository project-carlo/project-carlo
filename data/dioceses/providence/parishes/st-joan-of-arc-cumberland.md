---
name: St. Joan of Arc
website: https://www.church-bulletin.org/saint-joan-of-arc-parish-cumberland-ri-02864
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://www.church-bulletin.org/saint-joan-of-arc-parish-cumberland-ri-02864']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-joan-of-arc-parish-cumberland-ri-02864/2026-11-15.pdf
  seen: 2026-11-14
  quote: 3357 Mendon Road Cumberland, Rhode Island 02864-2112
  note: '15 November 2026 issue (6 pages), page 1 masthead: ''Saint Joan of Arc Parish'', Rev. Michael
    J. McMahon, Pastor; Holy Mass Schedule Saturday Vigil 4:00 PM, Sunday 7:30, 9:30 & 11:30 AM. Back-page
    footer: ''923 St. Joan of Arc, Cumberland, RI (B) John Patrick Publishing Company''.'
- url: https://stjoanschurchri.org/bulletin-and-links/
  seen: 2026-11-14
  note: Parish WordPress site's bulletin page links https://www.jppc.net/onlinebulletins/923template.pdf,
    which redirects to the church-bulletin.org page. probe url could not reach stjoanschurchri.org (egress
    proxy EOF); read in a browser (parish-site-access visit.py).
- url: https://www.church-bulletin.org/923
  seen: 2026-11-14
  note: Redirects to church-bulletin.org/saint-joan-of-arc-parish-cumberland-ri-02864, which lists one
    PDF per Sunday back to 2024-11-17, newest 2026-11-15.
promoted: 2026-11-16
bulletin_status: available
---

## Publisher

St. Joan of Arc, Cumberland publishes its own weekly bulletin through John Patrick Publishing (bulletin 923). The 15 November 2026 issue (https://www.church-bulletin.org/bulletin/saint-joan-of-arc-parish-cumberland-ri-02864/2026-11-15.pdf, 6 pages; page 5 is an image) has the masthead on page 1: "Saint Joan of Arc Parish", "3357 Mendon Road Cumberland, Rhode Island 02864-2112", "Established 1929", "The Reverend Michael J. McMahon ~ Pastor", and the Holy Mass Schedule: Saturday Vigil 4:00 PM, Sunday 7:30, 9:30 & 11:30 AM, daily Monday - Friday 7:30 AM, Saturdays and legal holidays 8:00 AM. The footer reads "923 St. Joan of Arc, Cumberland, RI (B)".

The finder (12139) gives the Saturday Vigil as 5:00 PM; the bulletin's 4:00 PM is current and is what the pipeline will read.

## Worship sites

One church: St. Joan of Arc, 3357 Mendon Rd. The bulletin, the finder (12139) and GCatholic (22354) name only this building.

## Website and bulletin provider

`other`, on the church-bulletin.org page that lists the issues. The parish site http://www.stjoanschurchri.org (finder and GCatholic) links the bulletin through `jppc.net/onlinebulletins/923template.pdf` on its /bulletin-and-links/ page, but `probe url` could not reach that host, so the website is the publisher's page, which needs no browser.

`fetch:check` on 2026-11-14 resolved "page-pdfs on https://www.church-bulletin.org/saint-joan-of-arc-parish-cumberland-ri-02864: current" and picked the 2026-11-15 issue read above; recipe `page-pdfs`.

## Not yet confirmed

Nothing open.
