---
name: St. Teresa of Calcutta Parish
website: https://stteresaofcalcuttanj.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-teresa-of-calcutta-parish-collingswood-nj-08108
publication: ['url:https://www.church-bulletin.org/saint-teresa-of-calcutta-parish-collingswood-nj-08108#john-patrick']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-teresa-of-calcutta-parish-collingswood-nj-08108/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (16 pages, image-only: read from rendered pages 1-2). Page 1 is headed
    ''Saint Teresa of Calcutta Parish'' with the parish mission statement; page 2 ''Parish Information''
    lists Rev. Steven Bertonazzi, Pastor, and the ''Mass & Sacrament Schedule'' for St. John Church (SJ),
    809 Park Ave., Collingswood and Holy Saviour Church (HS), 50 Emerald Ave., Haddon Township.'
- url: https://stteresaofcalcuttanj.org/
  seen: 2026-10-29
  quote: Serving the Communities of Collingswood & Haddon Township, New Jersey
  note: 'Read in the browser (probe url answers 403). Mass Schedule: Holy Saviour Saturday 4:00 PM, Sunday
    8:00 AM and 11:00 AM (American Sign Language); St. John Sunday 9:30 AM and 11:00 AM; daily Mass Mon,
    Tue, Wed, Fri 9:00 am St. John and Thursday 9:00 AM Holy Saviour.'
- url: https://stteresaofcalcuttanj.org/bulletin
  seen: 2026-10-29
  note: 'Browser read: the site''s own Bulletin folder lists ''October 25, 2026'' down to June 2026, each
    linking /bulletin/<n>-<date>/file (extension-less; the pipeline finds no PDF links there and the sandbox
    gets 403 on them). The church-bulletin.org listing has the same weekly issues.'
- url: https://www.church-bulletin.org/saint-teresa-of-calcutta-parish-collingswood-nj-08108
  seen: 2026-10-29
  note: Listing 'Saint Teresa of Calcutta Parish Bulletin', hosted by John Patrick Publishing Company;
    dated weekly PDFs, latest 2026-10-25.
research:
- method: probe get / render.py / fetch:check on the parish site's own /bulletin/<n>-<date>/file links
  url: https://stteresaofcalcuttanj.org/bulletin
  checked: '2026-10-29'
  outcome: unsupported-format
  next_action: Use the church-bulletin.org listing (pinned). Only if that stops posting issues, teach
    a collector the site's extension-less /file links
  retry_when: church-bulletin.org stops listing this parish's weekly issues
bulletin_status: available
---

## Publisher

John Patrick Publishing prints the bulletin, and the church-bulletin.org listing serves it (checked 2026-10-29: dated weekly PDFs, latest 2026-10-25, the same issue the parish site's Bulletin folder lists). The listing's 25 October 2026 issue is image-only; its pages 1 and 2 (rendered and read) are headed 'Saint Teresa of Calcutta Parish' with Rev. Steven Bertonazzi as pastor, and its Mass & Sacrament Schedule covers St. John Church, 809 Park Ave., Collingswood and Holy Saviour Church, 50 Emerald Ave., Haddon Township, and no other church. The John Patrick id was not found (the listing doesn't print it), so the `publication` id is the listing's URL.

## Worship sites

Two, both read from the parish site's Mass Schedule and the bulletin's page 2: St. John, Collingswood (`st-john-collingswood`) and Holy Saviour, Haddon Township/Westmont (`holy-saviour-westmont`). GCatholic still lists both under 'Blessed Teresa of Calcutta Parish'; the bulletin and site say 'Saint Teresa of Calcutta'.

## Website and bulletin provider

The directory's `stteresaofcalcuttanj.org` is the live site (it answers 403 to `probe url` but loads in the browser); GCatholic's `blessedteresanj.org` has no DNS. The site's own Bulletin folder links each issue as `/bulletin/<n>-<date>/file`, with no `.pdf`, so fetch:check finds no PDF links there (tried page-pdfs, redirected-pdf, linked-issue-page and dated-post, all `NoBulletin`) and probe get and render.py get 403 on the files. The church-bulletin.org listing serves the same issues as plain PDFs, so the recipe is pinned to it.

## Not yet confirmed

No shared bulletin with Most Precious Blood or St. Joseph the Worker: each masthead names its own parish.
