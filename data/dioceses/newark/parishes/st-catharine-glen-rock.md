---
name: St. Catharine, Glen Rock
website: https://www.stcatharinechurch.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:14116']
group: ''
evidence:
- url: https://files.ecatholic.com/14116/bulletins/20261101.pdf
  seen: 2026-11-03
  note: 'Page 1 of the 1 November 2026 issue (8 pages, image only, no text layer; read rendered with parish-site-access
    render.py). Masthead shows St. Catharine Roman Catholic Church, 905 South Maple Avenue, Glen Rock,
    New Jersey 07452, www.stcatharinechurch.org, Sunday, November 1, 2026. Eucharist - Weekend Masses:
    Saturday 5 pm; Sunday 8 am, 10am, 12 pm. Daily Mass: Monday-Friday 8 am in the Ministry Center Chapel;
    Saturday 9 am in the Ministry Center Chapel.'
- url: https://www.stcatharinechurch.org/
  seen: 2026-11-03
  note: Parish eCatholic site (probe get answers 403; loaded with parish-site-access visit.py). Embeds
    ecatholic:14116 and links /current-bulletin and /bulletins.
- url: https://www.stcatharinechurch.org/mass-schedules
  seen: 2026-11-03
  quote: 'Daily Mass: Monday through Friday at 8am and Saturday at 9am in the MINISTRY CENTER CHAPEL.'
  note: Read with visit.py (Cloudflare 403 to probe get).
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. Catharine, 905 South Maple Avenue, Glen Rock, publishes its own weekly bulletin through eCatholic (site 14116). I read page 1 of the 1 November 2026 issue (image only, rendered): the masthead names "St. Catharine Roman Catholic Church, 905 South Maple Avenue, Glen Rock" alone, with its own Mass schedule. The 8 November issue was not yet posted on 3 November (403).

## Worship sites

- St. Catharine Church, 905 South Maple Avenue (`st-catharine-glen-rock`): the weekend Masses (Saturday 5 pm; Sunday 8, 10 am, 12 pm).
- Ministry Center Chapel (`ministry-center-chapel-glen-rock`): the bulletin and the site's Mass Schedules page put every weekday Mass there (Monday–Friday 8 am, Saturday 9 am). A chapel with its own public daily schedule, so its own church row, as Holy Trinity, Hackensack's Parish Center Chapel is.

The directory (53) and GCatholic (18413) list only the church.

## Website and bulletin provider

The directory's stcatharinechurch.org is the parish's eCatholic site (ecatholic:14116), behind Cloudflare: `probe get` answers 403, `visit.py` loaded it on the first try. Provider `ecatholic`, read from the website. The bulletin is image-only (no text on any of the 8 pages of the 1 November issue), so the pipeline has to read it as images.

Fetch check (2026-11-03): ok, resolved the latest anchor link on the site to `files.ecatholic.com/14116/bulletins/20261101.pdf` (1 November 2026, `fresh`).

## Not yet confirmed

Where the Ministry Center stands on the campus (see its church record).
