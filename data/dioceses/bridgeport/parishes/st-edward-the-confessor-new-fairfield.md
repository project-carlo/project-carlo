---
name: St. Edward the Confessor
website: https://www.stedwardchurch.org/
bulletin_provider: parishes_online
provider_id: st-edward-the-confessor-church-06812
publication: ['po-org:st-edward-the-confessor-church-06812', 'lpi:0018000000Qc1JNAAZ', 'po-container:04/0718']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0718/20261115B.pdf
  seen: 2026-11-12
  quote: Holy Trinity Chapel | 10 AM
  note: 'Page 1 of the 15 November 2026 issue (8 pages): ''33rd Sunday in Ordinary Time, November 15,
    2026, 21 BRUSH HILL ROAD | NEW FAIRFIELD, CT 06812, WWW.STEDWARDCHURCH.ORG''. Page 2 ''WELCOME TO
    ST. EDWARD THE CONFESSOR'', Pastor Fr. Robert Wolfe; Mass times Daily Mon.-Fri. 9 AM, Saturday 4 PM
    Vigil, Sunday 7:30, 9, 11 AM, 5:15 PM, ''Holy Trinity Chapel | 10 AM''. Page 3 offertory ''St. Edward''
    and ''Holy Trinity'', and intentions incl. Sunday 22 November ''10:00 am Holy Trinity Chapel''.'
- url: https://parishesonline.com/organization/st-edward-the-confessor-church-06812
  seen: 2026-11-12
  note: 'probe po: org ''St. Edward the Confessor Parish'', 21 Brush Hill Rd, New Fairfield, CT 06812,
    LPi id 0018000000Qc1JNAAZ, container 04/0718; issues weekly to 22 November 2026.'
- url: https://www.stedwardchurch.org/bulletins
  seen: 2026-11-12
  note: eCatholic site (ecatholic:2335 in the page, 'powered by eCatholic'), behind Cloudflare (probe
    url HTTP 403; read with visit.py). Its Bulletins page links https://www.parishesonline.com/find/st-edward-the-confessor-church-06812;
    no eCatholic bulletin files were linked.
- url: https://files.ecatholic.com/2335/documents/2025/7/Notes%20on%20Merger.docx.pdf
  seen: 2026-11-12
  quote: As of July 1st, the parish of Holy Trinity was merged into St. Edward the Confessor
  note: 'Fr. Wolfe''s letter of 10 September 2022, linked from the parish''s Holy Trinity page: two campuses,
    St. Edward the Confessor Campus (New Fairfield) and Holy Trinity Campus (Sherman).'
bulletin_status: available
---

## Publisher

LPi publishes St. Edward the Confessor's weekly bulletin on ParishesOnline (org `st-edward-the-confessor-church-06812`, LPi id 0018000000Qc1JNAAZ, container 04/0718). The 15 November 2026 issue (`https://container.parishesonline.com/bulletins/04/0718/20261115B.pdf`, read 2026-11-12) has on page 1 "33rd Sunday in Ordinary Time, November 15, 2026, 21 BRUSH HILL ROAD | NEW FAIRFIELD, CT 06812", and on page 2 "WELCOME TO ST. EDWARD THE CONFESSOR" with Fr. Robert Wolfe as pastor and the parish's Mass times.

## Worship sites

Page 2 of the 15 November 2026 issue lists "Daily| Mon. - Fri. 9 AM, Saturday| 4 PM, Vigil Mass, Sunday | 7:30 AM, 9 AM, 11 AM, 5:15 PM, Holy Trinity Chapel | 10 AM"; page 3 reports the offertory for "St. Edward" and "Holy Trinity" separately and lists the intention for "10:00 am Holy Trinity Chapel" on Sunday 22 November.

- `st-edward-the-confessor-new-fairfield`: the parish church, 21 Brush Hill Road (directory:1400, GCatholic 22030).
- `holy-trinity-chapel-sherman`: Holy Trinity Chapel, Sherman (GCatholic 22031, not in the diocese's directory). Fr. Wolfe's letters on the parish site say Holy Trinity parish, Sherman "was merged into St. Edward the Confessor" on 1 July 2022 (letter of 10 September 2022), the old church building's condition led to a new chapel on the Sherman property (letter of 2 July 2022), and the new chapel's dedication Mass was set for Sunday 21 December 2025 (update of 14 December 2025). This settles the earlier jobs' lead: Holy Trinity is a church of this parish, open, not closed.

## Website and bulletin provider

`stedwardchurch.org` is an eCatholic site (site 2335) behind Cloudflare: `probe url` got HTTP 403 and `visit.py` read it. Its Bulletins page links the ParishesOnline org rather than hosting issues, so the provider is `parishes_online` with the org slug. The eCatholic site id is the site's hosting account, not the bulletin, so it is kept in evidence, not `publication`. See the fetch check below.

`fetch:check` on 2026-11-12 (headed Chrome) fetched the ParishesOnline org's newest issue, `https://container.parishesonline.com/bulletins/04/0718/20261122B.pdf` (22 November 2026, posted ahead; freshness reported `future`, -10 days), from the same container as the 15 November issue read above.

## Not yet confirmed

Nothing open for the parish row.
