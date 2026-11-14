---
name: St. Philip the Apostle
website: https://saintphilipct.com/category/bulletin/
bulletin_provider: other
provider_id: dated-post https://saintphilipct.com/category/bulletin/
publication: ['url:https://saintphilipct.com/category/bulletin/#st-philip-the-apostle-ashford']
group: ''
evidence:
- url: https://saintphilipct.com/index.php?gf-download=2026%2F11%2FBulletin-11-15-2026.pdf&form-id=4&field-id=7&hash=61b5e9f3111c570e7f63e7b68ac1e2b1b161255876b7bfda5929c2f26889b853
  seen: 2026-11-14
  quote: 64 Pompey Hollow Rd., Ashford, CT 06278
  note: Page 1 masthead of the November 15, 2026 bulletin names 'ST. PHILIP THE APOSTLE CHURCH' alone,
    Father Michael Giannitelli, Pastor, with its own Mass schedule (Saturday 4:30 p.m.; Sunday 9:00 and
    11:00 a.m.).
- url: https://saintphilipct.com/bulletin/bulletin-november-15-2026/
  seen: 2026-11-14
  quote: Bulletin-11-15-2026.pdf
  note: WordPress post 'Bulletin November 15, 2026' (category bulletin, posted 2026-11-13) linking the
    PDF through a Gravity Forms gf-download URL.
bulletin_status: available
---

## Publisher

St. Philip the Apostle, Ashford publishes its own bulletin on its WordPress site, one post per issue. The November 15, 2026 issue (Bulletin-11-15-2026.pdf, read 2026-11-14) is headed "ST. PHILIP THE APOSTLE CHURCH, 64 Pompey Hollow Rd., Ashford, CT 06278", Father Michael Giannitelli, Pastor, on page 1.

## Worship sites

The page 1 weekend schedule (Saturday 4:30 p.m.; Sunday 9:00 and 11:00 a.m.; daily Tuesday-Friday 8:00 a.m.) and the page 3 Mass intentions name no other church. St. Jude, Willington, which the diocese's list marks closed with records at St. Philip, appears in the issue only in the parish email address stphilipstjude@gmail.com (grep of the text pages for "Jude" and "Willington"; image page 2 is a craft fair flyer; image pages 6, 9, 11, 12 not read). It has its own `excluded/` record. The locator map's pastor (Rev. P. Grzegorz Jednaki) is older than the bulletin and the diocese's list.

## Website and bulletin provider

The diocese gives www.saintphilipct.com (redirects to saintphilipct.com). Each issue is a post in `/category/bulletin/` (`/bulletin/bulletin-<month>-<d>-<yyyy>/`), whose PDF is linked as `index.php?gf-download=<yyyy>/<mm>/Bulletin-<mm>-<dd>-<yyyy>.pdf&form-id=4&field-id=7&hash=...`, a Gravity Forms download that serves the PDF. GCatholic's saintphilipsaintjude.org answers 403. Pages 2, 6, 9, 11 and 12 of the November 15 issue are images.

fetch:check (2026-11-14) without a recipe picked the November 15 PDF but proposed pinning that week's post page; the pinned recipe `dated-post https://saintphilipct.com/category/bulletin/` reads the newest post from the category listing and picks the same November 15 issue ("dated-post ...: current").

## Not yet confirmed

Nothing open.
