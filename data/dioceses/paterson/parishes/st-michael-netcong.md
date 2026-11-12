---
name: St. Michael
website: https://stmichaelnetcong.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:10927']
group: ''
evidence:
- url: https://files.ecatholic.com/10927/bulletins/20261025.pdf
  seen: 2026-11-04
  quote: Schedule of Masses
  note: 'Page 1 masthead of the 25 October 2026 issue: SAINT MICHAEL, 4 CHURCH STREET, NETCONG, NJ 07857,
    ROMAN CATHOLIC CHURCH, October 25, 2026; Saturday 5:00 pm; Sunday 7:00, 9:30, 11:30 am; Misa en Español
    1:30 pm; Weekdays 10:00 am.'
- url: https://files.ecatholic.com/10927/bulletins/20261101.pdf
  seen: 2026-11-04
  quote: The Church of Saint Michael
  note: 'Page 1 cover reads ''St. Michael Netcong, New Jersey''; page 2 masthead ''The Church of Saint
    Michael November 1, 2026 All Saints'', Fr. Enrique Corona-Pastor, with Mass intentions Saturday 10am
    and 5pm; Sunday 7am, 9:30am, 11:30am and 1:30pm (Spanish); weekdays 10am. Page 12 ad footer: ''049A
    (MV) - St. Michael, Netcong''.'
- url: https://stmichaelnetcong.org/bulletins
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403). eCatholic site id 10927; the page
    lists weekly files.ecatholic.com/10927/bulletins/ PDFs, newest 'November 1, 2026' (20261101.pdf),
    back to 26 July 2026.
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. Michael, Netcong publishes its own weekly bulletin on its eCatholic site (site id 10927). The 1 November 2026 issue (`https://files.ecatholic.com/10927/bulletins/20261101.pdf`, read 2026-11-04 with probe pdf; pages 9-11 have no text layer) has a page 1 cover "St. Michael Netcong, New Jersey" and on page 2 "The Church of Saint Michael November 1, 2026 All Saints", with "Fr. Enrique Corona-Pastor" and stmichaelnetcong.org addresses. Its ad page carries a Bon Venture footer ("049A (MV) - St. Michael, Netcong"), but the issue is posted on eCatholic, which is where the site links it.

## Worship sites

- `st-michael-netcong`: the only church. The 25 October 2026 issue's page 1 masthead reads "SAINT MICHAEL 4 CHURCH STREET • NETCONG, NJ 07857 ROMAN CATHOLIC CHURCH" with a "Schedule of Masses" (Saturday 5:00 pm; Sunday 7:00, 9:30, 11:30 am in English; Misa en Español todos los Domingos 1:30 pm; Weekdays 10:00 am) and no other place. Page 2's "Mass Intentions for the Week" lists Saturday 10am and 5pm; Sunday 7am, 9:30am, 11:30am and 1:30pm ("Día de Todos los Santos", the Spanish Mass); weekdays 10am, at no named place other than the church. Page 4 announces a prayer service (not a Mass) at the old St. Michael cemetery on Old Ledgewood Road on 1 November; a grep of the issue for chapel and mission found no other worship site.

The diocese's finder (directory:10927) and GCatholic (19041) both list this one church. GCatholic's website for it, `www.st-michael-1880.com`, no longer resolves (probe url 2026-11-04: DEAD-DNS); the parish's site is stmichaelnetcong.org.

## Website and bulletin provider

`stmichaelnetcong.org` is the parish's eCatholic site, behind Cloudflare (probe url: 403). visit.py read its /bulletins page on 2026-11-04: weekly `files.ecatholic.com/10927/bulletins/<YYYYMMDD>.pdf` files, newest 1 November 2026. The home page also reports `ecatholic:5303`, the diocese's own site, which is not recorded. Provider `ecatholic`, publication `ecatholic:10927`. `fetch:check` on 2026-11-04 resolved the /bulletins page to `https://files.ecatholic.com/10927/bulletins/20261101.pdf` (the 1 November 2026 issue, 3 days old). It reports an issue-date conflict and freshness unknown because that issue's page 1 is a one-off cover for the pastor's birthday, "Father Enrique November 5, 2026" (page 2's intentions have "Thursday, November 5 ... Happy Birthday Fr. Enrique"); page 2 is dated "November 1, 2026", and the usual page 1 masthead (25 and 18 October 2026 issues) carries the Sunday date. The pick is the current issue; identity is unverified (no expected identity supplied) and was checked by hand above.

## Not yet confirmed

Nothing open.
