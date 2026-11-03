---
name: St. Ann
website: https://saintann1859.org/
bulletin_provider: other
provider_id: page-pdfs https://saintann1859.org/ filename=Bulletin*.pdf
publication: ['url:https://saintann1859.org/']
group: ''
evidence:
- url: https://saintann1859.org/wp-content/uploads/2026/10/BulletinNovember1.pdf
  seen: 2026-11-02
  quote: G60649 (JR) - St. Ann, Hampton, NJ
  note: '1 November 2026 issue (6 pages, text layer; the quote is the Bon Venture code line on the ad
    page). Page 1 masthead: ''ROMAN CATHOLIC The Church of Saint Ann SUNDAY BULLETIN 6 CHURCH STREET,
    HAMPTON, NEW JERSEY''; ''Rev. Fr. Michael C. Saharic, KCHS Pastor''; parish office mailing address
    ''32 Main Street P.O. Box 405 Hampton, NJ 08827''; ''MASS SCHEDULE Weekend Saturday Vigil Mass at
    4:00pm Sunday at 8:00, 9:30 & 11:00am Daily Monday – Friday at 8:00 am Holy Days as published''; page
    2 dated ''November 1, 2026''. Names no other church.'
- url: https://saintann1859.org/wp-content/uploads/2026/10/BulletinOctober4.pdf
  seen: 2026-11-02
  note: 'The home page''s ''Last Week'' link: despite the file name, the issue inside is dated ''October
    25, 2026'' (page 2), with the same masthead and code line G60649.'
- url: https://saintann1859.org/
  seen: 2026-11-02
  quote: Online Bulletin available on the
  note: 'Parish WordPress site. Menu ''Bulletin'' with ''This Week'' (BulletinNovember1.pdf) and ''Last
    Week'' (BulletinOctober4.pdf); ''Mass Schedule: Vigil Mass: Saturdays at 4:00 PM; Sunday Mass: 8:00
    AM, 9:30 AM, and 11:00 AM; Daily Mass: 8:00 AM Monday through Friday''. Title ''The Church of Saint
    Ann – Rev. Fr. Michael C. Saharic, Pastor''.'
research:
- method: Searched DuckDuckGo (via visit.py) for St. Ann Hampton bulletin Bon Venture and for sponsors.bonventure.net
    'Hampton, NJ'; then fetched sponsors.bonventure.net/?page=<n> for n in 1450-1600, 2100-2260 and 6480-6560
    (the ranges holding this diocese's known listings) with tools/bonventure_scan.sh, matching 'Hampton'
  url: http://sponsors.bonventure.net/
  checked: '2026-11-02'
  outcome: not-found
  next_action: Scan other sponsors.bonventure.net page ranges, or look for a listing link on the parish
    site or in a later bulletin, and add url:http://sponsors.bonventure.net/?page=<n> as a second publication
    id
  retry_when: Another batch finds how Bon Venture numbers its listings, or the parish site links a listing
bulletin_status: available
---

## Publisher

The Church of Saint Ann, Hampton, publishes its own weekly bulletin, printed by Bon Venture Services (code line 'G60649 (JR) - St. Ann, Hampton, NJ' on the ad page) and posted on the parish's WordPress site. I read the 1 November 2026 issue (2026-11-02): its masthead is 'The Church of Saint Ann, SUNDAY BULLETIN, 6 CHURCH STREET, HAMPTON, NEW JERSEY', pastor 'Rev. Fr. Michael C. Saharic, KCHS' (as in the finder), Masses Saturday 4 pm, Sunday 8, 9:30 and 11 am, Monday-Friday 8 am. It names no other church.

## Worship sites

One church (directory:24493, gcatholic:18635). The bulletin's masthead gives the church at 6 Church Street and the parish office at 32 Main Street; the finder and GCatholic give 32 Main Street for the parish. Saint Ann's Cemetery is listed (gates open dawn to dusk) but has no Mass.

## Website and bulletin provider

Website https://saintann1859.org/, whose 'Bulletin' menu links 'This Week' and 'Last Week' PDFs under `/wp-content/uploads/<yyyy>/<mm>/Bulletin<Month><Day>.pdf`. The file names are not reliable dates: 'BulletinOctober4.pdf' holds the 25 October 2026 issue, so the parish evidently reuses old names. Provider `other` with recipe `page-pdfs` on the home page filtered to `Bulletin*.pdf` (the menu also links a 'November-2026.pdf' calendar and forms). The finder lists no website for this parish; GCatholic gives saintann1859.org. The survey's `probe url` said DEAD-DNS, but `probe get` loaded it.

Publication id `url:https://saintann1859.org/`, the bulletin's only page, as for other self-hosted rows here. I found no Bon Venture `sponsors.bonventure.net/?page=<n>` listing for code G60649 (see research); if one turns up, add it as a second id.

## Not yet confirmed

Whether Bon Venture keeps a sponsors listing for this parish; see research. The parish site keeps only 'This Week' and 'Last Week', so there is no archive.

## Fetch check

`pnpm fetch:check` on 2026-11-02 resolved 'page-pdfs on https://saintann1859.org/: first-listed' and picked `BulletinNovember1.pdf`, the 'This Week' link and the 1 November 2026 issue (read above): transport ok, PDF, but issue date and freshness `unknown` ('No unambiguous issue date in inspected masthead or selected URL filename'), since the file name holds a month name and the masthead no date. The pick is right because the menu lists 'This Week' first; the file names alone can't date an issue (the 'Last Week' file is named October4 but holds 25 October).
