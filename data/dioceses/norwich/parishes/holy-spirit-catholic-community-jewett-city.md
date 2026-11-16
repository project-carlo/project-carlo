---
name: Holy Spirit Catholic Community
website: https://parishesonline.com/organization/st-catherine-of-siena-06365
bulletin_provider: parishes_online
provider_id: st-catherine-of-siena-06365
publication: ['po-org:st-catherine-of-siena-06365', 'lpi:0018000000QxAEgAAN', 'po-container:03/0945']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/0945/20261115B.pdf
  seen: 2026-11-14
  quote: Holy Spirit Catholic Community - St. Mary St. Catherine SS Thomas & Anne  |  03-0945
  note: Footer of pages 7-8 of the November 15, 2026 issue (8 pages). Page 1's masthead lists St. Catherine
    (243 Route 164, Preston), St. Mary (34 North Main Street, Jewett City) and SS. Thomas and Anne (61
    Preston City Rd, Voluntown), with one pastor (Rev. Tom Griffin) and one church office at 34 North
    Main Street, Jewett City.
- url: https://container.parishesonline.com/bulletins/03/0945/20261115B.pdf
  seen: 2026-11-14
  quote: 11:45am St. Catherine-Mass
  note: 'Page 2 of the November 15, 2026 issue gives one Mass schedule for the three churches: St. Mary
    Saturday 4:00pm and Sunday 8:00am, St. Thomas Sunday 10:00, St. Catherine Sunday 11:45am, with weekday
    Masses at each.'
- url: https://parishesonline.com/organization/st-catherine-of-siena-06365
  seen: 2026-11-14
  note: 'probe po: ''St. Catherine of Siena'', 243 Route 164, Preston, website www.saintcatherineofsienapreston.org,
    lpi 0018000000QxAEgAAN, container 03/0945, weekly issues to 2026-11-15. The diocese''s locator map
    links this org (parishesonline.com/find/st-catherine-of-siena-06365).'
- url: https://stmaryjc.weconnect.com/
  seen: 2026-11-14
  note: The website the diocese's list gives for St. Mary (www.stmaryjc.weconnect.com) answers 'Temporarily
    Unavailable' (bare host) or fails TLS (www.); www.saintcatherineofsienapreston.org timed out at DNS;
    www.stthomasvoluntown.org doesn't resolve; www.stmaryjc.4lpi.com (GCatholic) didn't load in the browser.
promoted: 2026-11-14
research:
- method: probe url and visit.py of the parish sites given by the diocese and GCatholic
  url: https://stmaryjc.weconnect.com/
  checked: '2026-11-14'
  outcome: access-blocked
  next_action: Re-open stmaryjc.weconnect.com and saintcatherineofsienapreston.org; if one links the 03/0945
    bulletin, set it as website
  retry_when: stmaryjc.weconnect.com no longer shows 'Temporarily Unavailable'
  revisit_after: 2027-02-01
bulletin_status: available
---

## Publisher

The three yoked parishes under Rev. Thomas P. Griffin (St. Mary, Jewett City; St. Catherine of Siena, Preston; Saints Thomas & Anne, Voluntown; the diocese's List of Parishes, March 6, 2026, gives each as yoked with the other two) publish one LPi bulletin, container 03/0945, as "Holy Spirit Catholic Community". The November 15, 2026 issue (read 2026-11-14) has the footer "Holy Spirit Catholic Community - St. Mary St. Catherine SS Thomas & Anne | 03-0945", and page 1 gives the three churches, one pastoral leadership and one church office (34 North Main Street, Jewett City).

## Worship sites

Three churches, from the November 15, 2026 issue. Page 2's schedule: St. Mary Saturday 4:00pm and Sunday 8:00am, Tuesday 8:00am; St. Thomas Sunday 10:00, Friday 8:00am; St. Catherine Sunday 11:45am, Thursday 9:00am.

Ruled out: St. Anne, Route 201, Glasgo, which the diocese's list marks 'Closed – For inquiries or records, contact St. Thomas & St. Anne, Voluntown'. The bulletin doesn't name Glasgo (grep: no match). It has its own excluded record, st-anne-glasgo. The Marian Friary of Our Lady of Guadalupe in Griswold (Franciscan Friars of the Immaculate) holds public Mass but isn't in this bulletin; it has its own excluded record (no-bulletin), our-lady-of-guadalupe-friary-griswold.

## Website and bulletin provider

ParishesOnline, read by `provider_id`. `website` is the ParishesOnline organization page: none of the parishes' own sites answered on 2026-11-14 (see evidence). The bulletin's masthead gives the website as 'stmaryjc@weconnect.com' and the Facebook page facebook.com/stmaryschurchjewettcity.

## Not yet confirmed

No parish website could be read. When stmaryjc.weconnect.com answers again, check whether it links this bulletin and whether it should be the `website`.
