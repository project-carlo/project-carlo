---
name: Immaculate Conception
website: https://www.iccannandale.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:22614', 'po-container:04/0852']
group: ''
evidence:
- url: https://files.ecatholic.com/22614/bulletins/20261101.pdf
  seen: 2026-11-02
  quote: 316 Old Allerton Road
  note: 'Page 1 of the 1 November 2026 issue (12 text pages): ''IMMACULATE CONCEPTION CATHOLIC CHURCH'',
    ''Annandale, NJ 08801'', ''www.iccannandale.org''; weekend Masses ''Saturday: 9:00am, 4:30pm Vigil'',
    ''Sunday: 8:00am, 10:00am, 12:00pm, 5:00pm''; weekday Masses 7:00am and 9:00am Monday-Friday. Page
    2 ''PARISH CLERGY'': ''Pastor Rev. Keith M. Cervine'', ''Parochial Vicar Rev. Jose Lim''. Ad pages:
    ''For ad info. call 1-800-950-9952 • www.4lpi.com … Immaculate Conception, Annadale, NJ 04-0852''.
    No other church is named.'
- url: https://container.parishesonline.com/bulletins/04/0852/20261101B.pdf
  seen: 2026-11-02
  quote: 316 Old Allerton Road
  note: 'ParishesOnline container 04/0852 (the code printed on the ad pages), probe container on 2026-11-02:
    newest issue 1 November 2026 (8 November answered 403). Its 20261101B.pdf is byte-identical to the
    eCatholic 20261101.pdf (39,212,969 bytes each, MD5 577abd9a870a05f07080dbd917b9fe5a), so they are
    one publication.'
- url: https://www.iccannandale.org/bulletins
  seen: 2026-11-02
  quote: November 1, 2026
  note: eCatholic site 22614, read with visit.py (probe url said DEAD-DNS for every host on 2026-11-02;
    the survey's probe url loaded it on 2026-10-30). The Bulletins page lists files.ecatholic.com/22614/bulletins/<YYYYMMDD>.pdf
    weekly from 24 May to 1 November 2026 and links no other publisher.
promoted: 2026-11-03
bulletin_status: available
---

## Publisher

Immaculate Conception, Annandale publishes its own weekly bulletin, printed by LPi (ad-page code 04-0852). The parish posts each issue on its eCatholic site (22614), and ParishesOnline container 04/0852 carries the same file. The 1 November 2026 issue (read 2026-11-02) is headed 'IMMACULATE CONCEPTION CATHOLIC CHURCH', '316 Old Allerton Road Annandale, NJ 08801', and page 2 names 'Pastor Rev. Keith M. Cervine' and 'Parochial Vicar Rev. Jose Lim'. The parish finder (2026-10-30) calls Fr. Cervine Administrator and gives Rev. Ariel Bautista, Jr. as parochial vicar; the masthead is the newer source. It names no other church.

## Worship sites

One church (directory:24464, gcatholic:18605). The page 1 schedule (Saturday 9:00am and 4:30pm Vigil; Sunday 8:00am, 10:00am, 12:00pm and 5:00pm; weekdays 7:00am and 9:00am) gives no other location, and the finder lists no other worship site.

## Website and bulletin provider

Website https://www.iccannandale.org (finder, GCatholic and masthead), eCatholic site 22614. The eCatholic 20261101.pdf and container 04/0852's 20261101B.pdf are byte-identical (39,212,969 bytes, same MD5), and both had 1 November 2026 as their newest issue on 2026-11-02 (container 8 November answered 403). Under the diocese's rule for a bulletin carried both on the parish site and by a publisher, I recorded the parish-hosted copy (`ecatholic`) and listed both ids. No ParishesOnline org slug was found (`probe po` knows no org for the container).

## Fetch check

`PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check` on 2026-11-02 picked https://files.ecatholic.com/22614/bulletins/20261101.pdf (the 1 November 2026 issue): transport ok, document type `pdf_signature` (the 39 MB file exceeds the tool's 25,000,000-byte inspection limit, so it checked only the PDF signature), issue date inferred 2026-11-01, freshness fresh (2 days), identity unverified by the tool; I read that issue myself (evidence above).

## Not yet confirmed

Nothing open for this row.
