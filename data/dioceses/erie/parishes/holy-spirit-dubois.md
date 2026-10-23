---
name: Holy Spirit Parish
website: https://www.weareholyspirit.com/bulletin
bulletin_provider: other
provider_id: page-pdfs https://www.weareholyspirit.com/bulletin
publication: ['ecatholic:35653', 'discovermass:holy-spirit-parish-dubois-pa']
group: Holy Spirit Parish (DuBois; five parishes merged 2023)
evidence:
- url: https://files.ecatholic.com/35653/documents/2026/10/2026-10-18.pdf
  seen: 2026-10-23
  quote: View this bulletin online at www.DiscoverMass.com
  note: 'Issue dated 18 October 2026 (8 pages; the page-1 masthead text extracts with spaces dropped:
    ''Holy SpiritParish'', Administrative Office 118 S. State Street, DuBois; Pastor Fr. John Malthaner,
    Parochial Vicar Fr. Michael Scanga, Deacon Dan Satterlee). Weekly schedule on page 1: weekday Masses
    at St. Catherine; Saturday 4:00 p.m. St. Catherine and 5:30 p.m. A.B.V.M., Sykesville; Sunday 8:00
    a.m. A.B.V.M. and 7:30, 9:00, 11:00 a.m. St. Catherine. Names this one parish alone. fetch:check (publication
    identity ''Malthaner'' matched, freshness fresh) picked this file.'
- url: https://www.weareholyspirit.com/bulletin
  seen: 2026-10-23
  quote: Weekly Bulletins
  note: 'eCatholic site 35653, read in headed Chrome (weareholyspirit.com 403s probe url and curl). Page
    ''Weekly Bulletins'' lists 27 dated PDFs, newest first: 10-18-2026, 10-11-2026, 10-04-2026, ... 04-19-2026,
    under files.ecatholic.com/35653/documents/<yyyy>/<m>/<date>.pdf (free-form names, so `issues.py ecatholic`
    finds nothing). The 25 October issue is not posted yet.'
- url: https://www.weareholyspirit.com/
  seen: 2026-10-23
  quote: 5:30 PM Sykesville, ABVM
  note: 'Home page Mass Times box: Saturday 4:00 PM DuBois St. Catherine, 5:30 PM Sykesville ABVM; Sunday
    7:30, 9:00, 11:00 AM St. Catherine, 8:00 AM Sykesville ABVM; weekday Masses at St. Catherine. Footer:
    Holy Spirit Parish, 123 S State Street, DuBois.'
- url: https://discovermass.com/church/holy-spirit-parish-dubois-pa/
  seen: 2026-10-23
  note: 'Discover Mass page for Holy Spirit Parish, DuBois: current bulletin cover class ''bulletin-cover
    X-|2026-10-25|1792780901|3163'' (bulletin number 3163, issue 25 October 2026, already posted two days
    early). The sister pages for Assumption (Sykesville), St. Mary (Reynoldsville) and St. Bernard (Falls
    Creek) all say ''no bulletins available''; no Discover Mass page was found for St. Catherine or St.
    Michael.'
- url: https://www.eriercd.org/Parish20824-Holy-Spirit.html
  seen: 2026-10-23
  note: Diocese directory record 20824, Holy Spirit Parish (established 2023), 123 S. State St.; Pastor
    per clergy PDF 'Rev. John Malthaner' (the locator's 'Rev. Msgr. Richard R. Siefer, E.V.' is stale;
    he petitioned as pastor in the August 2023 decree). The four other records (20805 St. Catherine, 20809
    St. Michael, 20804 St. Bernard, 20808 St. Mary) and 20801 Assumption all give this website.
- url: https://www.eriercd.org/images/sections/bishop/pdf/DECREE%20-%20Merging%20St.%20Catherine%20of%20Siena%20St.%20Michael%20the%20Archangel%20St.%20Bernard%20St.%20Mary%20and%20Assumption%20of%20the%20Blessed%20Virgin%20Mary%20and%20erecting%20Holy%20Spirit.pdf
  seen: 2026-10-23
  quote: be designated as secondary churches of the new parish
  note: 'Merger decree: five parishes (St. Catherine of Siena, St. Michael the Archangel, St. Bernard,
    St. Mary, Assumption of the BVM) merged by extinctive union into Holy Spirit Parish; St. Catherine
    is the parish church and the other four are secondary churches. The decree closes no building.'
promoted: 2026-10-23
research:
- method: probe url weareholyspirit.com; visit.py --bulletin in headed Chrome; the Bulletin page's PDF
    list; pdftotext of all 27 issues
  url: https://www.weareholyspirit.com/bulletin
  checked: '2026-10-23'
  outcome: found
  next_action: 'None: the Bulletin page is the channel and the recipe page-pdfs https://www.weareholyspirit.com/bulletin
    passes fetch:check (18 October 2026 issue).'
  retry_when: If the fetch picks a stale file, compare with the Discover Mass page (number 3163 was the
    25 October issue).
- method: pnpm fetch:check --diocese erie --parish holy-spirit-dubois with provider ecatholic (resolver
    visits /bulletins)
  url: https://www.weareholyspirit.com/bulletins
  checked: '2026-10-23'
  outcome: not-found
  next_action: 'Use the recorded `other` recipe (page-pdfs on /bulletin) instead: the eCatholic resolver
    looks for files.ecatholic.com anchors on /bulletins, which does not exist on this site, and the PDFs
    sit under /documents/ not /bulletins/.'
  retry_when: The eCatholic resolver learns the /bulletin path or documents/ file names
---

## Publisher

Holy Spirit Parish, DuBois (erected 2023 by merging St. Catherine of Siena, St. Michael the Archangel, St. Bernard, St. Mary and Assumption of the BVM) publishes one weekly bulletin on its eCatholic site, weareholyspirit.com (site id 35653). The issue dated 18 October 2026, read 2026-10-23, is headed Holy Spirit Parish with the office at 118 S. State Street and pastor Fr. John Malthaner, and its Mass schedule and intentions cover St. Catherine and Assumption (Sykesville) together: one bulletin for the whole merged parish, so one row. The merger is a fact, not a plan: the bulletin, the web site, the directory and the decree all use the one name, and none of the five former parishes has a bulletin of its own (the former sites stmikestjoe.com, stbernardfallscreek.org and saintcatherinedubois.com no longer resolve (DEAD-DNS, 2026-10-23)).

## Worship sites

Two buildings hold Mass: St. Catherine of Siena, DuBois (parish church; all weekday Masses, Saturday 4:00 p.m., Sunday 7:30/9:00/11:00 a.m.) and Assumption of the BVM, Sykesville (Saturday 5:30 p.m., Sunday 8:00 a.m.). Both are church rows under this parish.

Three other buildings are secondary churches with no regular Mass: St. Michael the Archangel (DuBois), St. Bernard (Falls Creek), St. Mary (Reynoldsville). Each had only its patronal-feast Mass in the 27 bulletins of 19 April to 18 October 2026 (St. Mary 8 September, St. Michael 29 September, St. Bernard 20 August), so each is `excluded/` with reason `no-public-mass`: see `st-michael-the-archangel-dubois`, `st-bernard-falls-creek`, `st-mary-reynoldsville`. St. Joseph, DuBois (relegated 2019-12-01) is `excluded/st-joseph-dubois`. The Byzantine Catholic Holy Trinity church in Sykesville belongs to the eastern-Catholic batch and is not linked here.

## Website and bulletin provider

weareholyspirit.com answers 403 to `probe url` and curl but opens in headed Chrome. The Bulletin page (`/bulletin`, not `/bulletins`) lists 27 PDFs newest first under `files.ecatholic.com/35653/documents/`. The built-in eCatholic resolver asks for `/bulletins` and found no match, so the row is `other` with provider_id `page-pdfs https://www.weareholyspirit.com/bulletin`; `fetch:check` (headed Chrome, expected identity Malthaner) fetched `2026-10-18.pdf`, 2.2 MB, PDF, identity matched, date inferred from the file name, fresh (5 days old). Overall status is 'unverified' only because the date is inferred from the file name. The same bulletin is on Discover Mass (`holy-spirit-parish-dubois-pa`, cover number 3163, which on 2026-10-23 was already the 25 October issue); the page lags by a week, but Discover Mass downloads are capped per IP, so the site is the better source.

## Not yet confirmed

Whether the Discover Mass 25 October issue is the same document as the parish site's (not downloaded; the file is not yet on the site). The parish's `publication` ids list both channels as the same bulletin on the strength of the bulletin's own line 'View this bulletin online at www.DiscoverMass.com'.
