---
name: St. James the Less
website: https://stjamesthelessrc.org
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/634
publication: ['url:https://www.church-bulletin.org/saint-james-the-less-roman-catholic-church-jamesburg-nj-08831']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-james-the-less-roman-catholic-church-jamesburg-nj-08831/2026-11-01.pdf
  seen: 2026-11-02
  quote: SAINT JAMES THE LESS PARISH
  note: 'Page 1 of the 1 November 2026 issue (8 pages, text): ''All Saints | November 1, 2026'', ''SAINT
    JAMES THE LESS PARISH, 36 Lincoln Avenue, Jamesburg, NJ 08831'', ''Rev. Juan C. Gaviria, Parish Administrator'',
    ''Rev. Peter A. Chakkunny, CMI, In Residence'', parish office 732-521-0100, ''Website: stjamesthelessrc.org'';
    Religious Services: Weekday Masses Monday - Friday 8:30 am; Weekend Masses Saturday 4:00 pm, Sunday
    8:00 am, 10:00 am, 2:00 pm (Spanish), 5:00 pm. A grep of the issue for ''Holy Trinity'' finds nothing
    and for ''Helmetta'' only an advertiser (''Helmetta, NJ Catering'') on page 8; it names no other church.'
- url: https://www.church-bulletin.org/saint-james-the-less-roman-catholic-church-jamesburg-nj-08831
  seen: 2026-11-02
  quote: Latest Edition November 1, 2026
  note: 'John Patrick Publishing listing for the parish (Jamesburg, NJ 08831, phone (732) 521-0100): latest
    edition 1 November 2026, weekly archive back to 2025.'
- url: https://jamestheless.org/bulletins/
  seen: 2026-11-02
  quote: Click Here To Read Current Bulletin
  note: The parish's earlier WordPress.com site (the finder lists no website; `jamestheless.org` is frozen
    at the April 2025 issues) links 'https://www.jppc.net/onlinebulletins/634template.pdf' (the John Patrick
    template id 634, visible in the page's HTML), tying this parish to church-bulletin.org/634. Its page
    lists the two April 2025 PDFs only.
- url: https://stjamesthelessrc.org/bulletins/bulletin.pdf
  seen: 2026-11-02
  quote: Pentecost Sunday | June 8, 2025
  note: 'The current parish site (stjamesthelessrc.org, a GoDaddy page; bulletin.html links only this
    ''This Week'' file) serves a stale copy: page 1 is the 8 June 2025 issue, same ''SAINT JAMES THE LESS
    PARISH, 36 Lincoln Avenue'' masthead. So the live issues are the John Patrick ones, not this file.'
- url: https://stjamesthelessrc.org/masstimes.html
  seen: 2026-11-02
  quote: Saturday 4 pm
  note: 'Parish Mass Times page: Saturday 4 pm; Sunday 8 am, 10 am, 2 pm in Spanish, 5 pm; Monday to Friday
    8:30 am. Matches the 1 November bulletin.'
- url: https://discovermass.com/church/st-james-the-less-jamesburg-nj/
  seen: 2026-11-02
  quote: There are currently no bulletins available for St. James the Less Church.
  note: 'Discover Mass church page: gives the parish site https://stjamesthelessrc.org/, Mass times Saturday
    4:00pm, Sunday 8:00am, 10:00am, 2:00pm (Spanish), 5:00pm, weekdays 8:30am, and no bulletins.'
bulletin_status: available
---

## Publisher

St. James the Less, 36 Lincoln Avenue, Jamesburg, publishes a weekly bulletin that John Patrick Publishing posts at church-bulletin.org (template id 634). The 1 November 2026 issue (page 1, read 2026-11-02) names 'Rev. Juan C. Gaviria, Parish Administrator' (matching the finder's Administrator line) and 'Rev. Peter A. Chakkunny, CMI, In Residence', gives the parish's address and Mass schedule, and names no other church.

## Worship sites

One church, 36 Lincoln Avenue (directory:24500, gcatholic:18655). The St. James cemetery on Mott Avenue is listed in the bulletin; it is not a worship site.

## Shared bulletin with Holy Trinity, Helmetta?

The batch asked whether Jamesburg and Helmetta share a bulletin. They don't: the 1 November St. James issue never names Holy Trinity (grep above), its Mass schedule is St. James's own, and the Helmetta parish (Holy Trinity, pastor Rev. Andrzej Wieliczko per the finder) has a different clergy team and a Polish Mass. See `parishes/holy-trinity-helmetta` for what was found there. Nor does Nativity, Monroe share: its 1 November and 4 October 2026 issues are Nativity's own.

## Website and bulletin provider

The finder lists no website. Discover Mass (`discovermass.com/church/st-james-the-less-jamesburg-nj/`, read 2026-11-02) gives `https://stjamesthelessrc.org/`, which is the parish's current site, so that is recorded as `website`; but its own bulletin file is frozen at June 2025 and `jamestheless.org` at April 2025. The live bulletin is on John Patrick (`other`, `page-pdfs https://church-bulletin.org/634`), as for St. Ambrose, Old Bridge. John Patrick's issue is the only publisher found: Discover Mass's church page for St. James says 'There are no bulletins available'. (`probe url` answered DEAD-DNS for every host in this job, including church-bulletin.org, while `probe get` fetched them; the probe is unreliable from this sandbox.)

## Fetch check

`pnpm fetch:check` on 2026-11-02 resolved `page-pdfs https://church-bulletin.org/634` and picked the 1 November 2026 issue: transport ok, PDF, issue date inferred from the file name, freshness fresh, identity unverified by the tool; I read that issue's page 1 myself (evidence above). No `recipe` line was printed, so the pinned recipe stays as set.

## Not yet confirmed

Nothing open.
