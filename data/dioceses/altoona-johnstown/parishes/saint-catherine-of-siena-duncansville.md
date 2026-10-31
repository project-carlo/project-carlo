---
name: Saint Catherine of Siena Parish, Duncansville
website: https://www.duncansvillecatholic.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:37641']
group: ''
evidence:
- url: https://files.ecatholic.com/37641/bulletins/20261018.pdf
  seen: 2026-10-21
  quote: 'Church Address: 308 Old Route 22, Duncansville, PA 16635'
  note: Page 2 of the 18 October 2026 issue (2 pages). Page 1 headed "St. Catherine of Siena Church UPCOMING
    MASS & EVENTS SCHEDULE"; page 2 headed "Saint Catherine of Siena Parish ... Pastor - Reverend Jeremy
    J. Mohler". Names this parish alone.
- url: https://www.duncansvillecatholic.org/bulletins
  seen: 2026-10-21
  note: The eCatholic site (id 37641, found by visit.py on the home page) links the current bulletin;
    fetch:check followed it to files.ecatholic.com/37641/bulletins/20261018.pdf. The site answers 403
    to curl and probe url (Cloudflare) but opens in headed Chrome.
promoted: 2026-10-21
---

## Publisher

St. Catherine of Siena, Duncansville publishes its own weekly bulletin through eCatholic (site id
37641). `issues.py ecatholic ecatholic:37641` on 2026-10-21 found the 18 October 2026 issue
(`files.ecatholic.com/37641/bulletins/20261018.pdf`, 2 pages, text layer readable; the 25 October
file is not up yet, 403). Page 1 is the Mass and intentions schedule for "St. Catherine of Siena
Church", page 2 the masthead "Saint Catherine of Siena Parish ... Church Address: 308 Old Route
22, Duncansville, PA 16635 ... Pastor - Reverend Jeremy J. Mohler". It names this church alone.
The diocese directory lists the parish with one church and no linked parish.

## Worship sites

One church, St. Catherine of Siena (churches/saint-catherine-of-siena-duncansville). The page 2
list of Masses is "Sunday: 5:00PM (Saturday Vigil) 8:00 AM & 11:00 AM; Daily: M-F 7:00 AM; First
Saturday: 8:30 AM", which matches the directory's times. The office is at 332 Howard Dr but holds
no Mass.

## Website and bulletin provider

`https://www.duncansvillecatholic.org` is the eCatholic-hosted site, so `fetch` reads it from the
website (`provider_id` empty). `pnpm fetch:check --diocese altoona-johnstown --parish
saint-catherine-of-siena-duncansville` on 2026-10-21 returned status ok:
`https://files.ecatholic.com/37641/bulletins/20261018.pdf` (url date 2026-10-18, 506,527 bytes).

## Not yet confirmed

Nothing.
