---
name: Church of Christ the King
website: https://churchofchristtheking.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:12066']
group: ''
evidence:
- url: https://files.ecatholic.com/12066/bulletins/20261101.pdf
  seen: 2026-11-04
  quote: Church of Christ the King
  note: 'Page 1 masthead: The Solemnity of All Saints, November 1, 2026; 16 Blue Mill Road, PO Box 368,
    New Vernon, NJ 07976; www.churchofchristtheking.org; MASS SCHEDULE Saturday (Vigil) 5pm, Sunday 7,
    9, 11am, 5:30pm* (*September - May), Weekdays Monday - Saturday 9am. Eight pages; pages 7-8 footer
    123C (PK) - Church of Christ the King, Bon Venture Services (ad sales). A grep for Chapel finds only
    Our Lady''s Chapel, a chapel in the church (p3 votive list, p5 lectors).'
- url: https://churchofchristtheking.org/bulletins
  seen: 2026-11-04
  note: Bulletins page (read with parish-site-access visit.py; probe url gets 403) lists files.ecatholic.com/12066/bulletins/<YYYYMMDD>.pdf
    weekly, newest November 1, 2026; it also links an eBULLETIN Mailchimp archive (us1.campaign-archive.com),
    not used.
bulletin_status: available
---

## Publisher

Church of Christ the King, New Vernon publishes its own weekly bulletin on eCatholic (site id 12066, the diocese finder's pin id). The 1 November 2026 issue (`https://files.ecatholic.com/12066/bulletins/20261101.pdf`, read 2026-11-04) has on page 1 "Church of Christ the King ... The Solemnity of All Saints November 1, 2026 16 Blue Mill Road PO Box 368 New Vernon, NJ 07976". Bon Venture sells its ads (footer "123C (PK) - Church of Christ the King"), but the parish posts the PDF to eCatholic.

## Worship sites

- `christ-the-king-new-vernon`: the only church. Page 1's "MASS SCHEDULE" (Saturday Vigil 5pm; Sunday 7, 9, 11am, 5:30pm September-May; Monday-Saturday 9am) names no other place. A grep of all 8 pages for Chapel found only "Our Lady's Chapel", which is inside the church (a votive list and a lectors' notice), not a separate site.

The diocese's finder (directory:12066) and GCatholic (19008) list this one church.

## Website and bulletin provider

`churchofchristtheking.org` is the parish's eCatholic site (the finder's link; GCatholic gives the same domain with www). It answers `probe url` with 403 (Cloudflare); `visit.py` loaded it on 2026-11-04 and found `ecatholic:12066` (and the diocese's own `ecatholic:5303`, not recorded). Its /bulletins page lists the standard `bulletins/<YYYYMMDD>.pdf` files. Provider `ecatholic`; `fetch:check` on 2026-11-04 resolved the latest bulletin link on https://churchofchristtheking.org/ to `files.ecatholic.com/12066/bulletins/20261101.pdf` (1 November 2026, 3 days old).

## Not yet confirmed

Nothing open.
