---
name: St. Joseph's Church
website: https://stjosephscamillus.org
bulletin_provider: other
provider_id: linked-issue-page https://stjosephscamillus.org/bulletins/
publication: ['url:https://www.church-bulletin.org/saint-joseph-s-church-camillus-ny-13031']
group: Rev. Robert Hyde (Camillus, Jordan)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-joseph-s-church-camillus-ny-13031/2026-09-27.pdf
  seen: 2026-09-26
  quote: 'Saturday: 4:30pm'
  note: 'Page 1 of the 27 September 2026 bulletin: "St. Joseph’s Church 5600 West Genesee Street Camillus,
    NY 13031", Rev. Robert Hyde pastor, "Eucharistic Liturgies are celebrated on Monday, Wednesday and
    Friday: 9:00am Saturday: 4:30pm Sunday: 8:00am & 10:45am". Page 2 notes Thursday "No Liturgy (Mass
    at St. Patrick’s in Jordan)".'
- url: https://stjosephscamillus.org/bulletins/
  seen: 2026-09-26
  quote: This Week's Bulletin
  note: The parish's Bulletins page. Its one button links https://www.jppc.net/onlinebulletins/4038template.pdf,
    which redirects (301, then 302) to the publisher's listing https://www.church-bulletin.org/saint-joseph-s-church-camillus-ny-13031.
- url: https://www.church-bulletin.org/saint-joseph-s-church-camillus-ny-13031
  seen: 2026-09-26
  note: John Patrick Publishing's listing for the parish, one PDF per Sunday at /bulletin/saint-joseph-s-church-camillus-ny-13031/YYYY-MM-DD.pdf,
    from 2024-09-29 through 2026-09-27.
- url: https://www.syracusediocese.org/st-joseph-camillus
  seen: 2026-09-26
  quote: Sacramental Records for Our Lady of Good Counsel, Warners; and St. John, Camillus are retained
    here.
  note: 'The diocese''s page (behind Cloudflare; read with visit.py). Clergy: "Hyde, Rev. Robert P., Jr.,
    J.C.L. PASTOR, ST. JOSEPH, CAMILLUS; ST. PATRICK, JORDAN".'
promoted: 2026-09-26
---

## Publisher

St. Joseph's, Camillus publishes its own weekly bulletin through John Patrick Publishing
(church-bulletin.org / jppc.net). I read the 27 September 2026 issue: page 1 is St. Joseph's
alone, with its mission statement, staff under Rev. Robert Hyde, its office and "St. Joseph’s
Church 5600 West Genesee Street Camillus", and its Mass times (Monday, Wednesday and Friday
9:00am; Saturday 4:30pm; Sunday 8:00am and 10:45am). Page 2's liturgy schedule covers only
St. Joseph's.

Fr. Hyde is also pastor of St. Patrick, Jordan (the diocese's page names him "PASTOR, ST.
JOSEPH, CAMILLUS; ST. PATRICK, JORDAN"), and the two parishes send weekday Mass-goers to each
other, but St. Patrick's publishes its own bulletin on its own site (masthead "St. Patrick Roman
Catholic Church, Jordan"). Both channels are current, so they are two rows, grouped as "Rev.
Robert Hyde (Camillus, Jordan)".

## Worship sites

One: St. Joseph's, 5600 West Genesee Street (`churches/st-joseph-camillus.md`).

The diocese's list sends two other places here. "Our Lady of Good Counsel, Warners (CLOSED - See
St. Joseph, Camillus)" is in another region's batch; St. Joseph's bulletin has no Mass in
Warners. "St. John, Camillus (See St. Joseph, Camillus)" is not marked closed and appears in
neither roster; its sacramental records are kept at St. Joseph's, and St. Joseph's bulletin has
no Mass at a St. John's, so it is no worship site of this parish. No building or address for it
was found, so it has no record.

## Website and bulletin provider

stjosephscamillus.org is the parish's own site; its Bulletins page's "This Week's Bulletin"
button is the stable jppc.net link that redirects to the publisher's listing page, where each
Sunday's issue is a dated PDF. The provider is `other`, from the website; the listing page is
the `publication`.

**Fetch gap:** a test run of the pipeline's `other` fetcher on 2026-09-26 on
https://stjosephscamillus.org returned jppc.net/onlinebulletins/4038template.pdf, which is not a
PDF but a redirect to the HTML listing, so the download will not get the bulletin. Pointed at the
listing page instead, the fetcher found no "bulletin" page link. A church-bulletin.org builder
(latest = /bulletin/<slug>/<Sunday>.pdf) would fix both. Reported to the orchestrator.

Fetch recipe `linked-issue-page https://stjosephscamillus.org/bulletins/`, pinned
2026-10-03: on the pages recorded 2026-09-27
(`tests/fixtures/fetch/st-joseph-camillus.json.gz`) the resolver found
https://www.church-bulletin.org/bulletin/saint-joseph-s-church-camillus-ny-13031/2026-09-27.pdf
this way, dated that week.

## Not yet confirmed

Whether the pipeline can fetch this bulletin (see the gap above).
