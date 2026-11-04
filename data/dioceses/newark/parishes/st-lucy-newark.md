---
name: St. Lucy's Church, Newark (National Shrine of St. Gerard)
website: https://parishesonline.com/organization/st-lucy-church-07104
bulletin_provider: parishes_online
provider_id: st-lucy-church-07104
publication: ['po-org:st-lucy-church-07104', 'lpi:0018000000QxAAqAAN', 'po-container:04/1246']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/1246/20261101B.pdf
  seen: 2026-11-04
  quote: 118 Seventh Ave, Newark, NJ 07104
  note: '1 November 2026 issue (6 pages, text). Page 1 masthead: ''St. Lucy''s Church'', ''The National
    Shrine of St. Gerard'', ''Sunday, November 1st, 2026''. Mass Schedule: Sunday Vigil 6:00pm; Sunday
    8:00am (Ita), 9:00am (Spa), 11:00am, 12:30pm & 5:30pm (Eng); weekdays 7:00 am, 9:00am and (Mon-Thu)
    5:30pm. One church.'
- url: https://parishesonline.com/organization/st-lucy-church-07104
  seen: 2026-11-04
  note: 'probe po: St. Lucy Church, 118 7th Ave, Newark, NJ, 07104; lpi 0018000000QxAAqAAN; container
    04/1246; latest issue 2026-11-01, then 10-25, 10-18. The org''s website field is empty.'
- url: https://www.saintlucy.net/
  seen: 2026-11-04
  note: 'Directory and GCatholic website. probe url: HTTP 404; visit.py: page title ''Reconnect Your Domain
    | Wix.com'', status 404: the Wix site''s domain is disconnected.'
research:
- method: probe url and visit.py on the directory/GCatholic website; Wayback availability API
  url: https://www.saintlucy.net/
  checked: '2026-11-04'
  outcome: not-found
  next_action: If the bulletin masthead or ParishesOnline org starts naming a website, record it as the
    parish website
  retry_when: A later bulletin or the PO org lists a working parish website
bulletin_status: available
---

## Publisher

St. Lucy's Church, the National Shrine of St. Gerard, publishes a weekly bulletin with LPi (ParishesOnline org `st-lucy-church-07104`, container 04/1246). I read the 1 November 2026 issue (6 pages, text): page 1 masthead 'St. Lucy's Church / The National Shrine of St. Gerard', '118 Seventh Ave, Newark, NJ 07104', with one Mass schedule in English and Spanish. No other church is named.

## Worship sites

- St. Lucy's Church, 118 Seventh Avenue (`st-lucy-newark`): Sunday vigil 6:00 pm; Sunday 8:00 am (Italian), 9:00 am (Spanish), 11:00 am, 12:30 pm and 5:30 pm (English); weekdays 7:00 am and 9:00 am, Monday-Thursday also 5:30 pm (page 1, 1 November 2026).

The directory (135) and GCatholic (18508) list only this church.

## Website and bulletin provider

The website the directory and GCatholic give, https://www.saintlucy.net/, answers 404 with Wix's 'Reconnect Your Domain' page (visit.py, 2026-11-04): the domain is disconnected. The bulletin is on ParishesOnline, so `website` is the PO org page and the provider is `parishes_online` with the org slug as `provider_id`. The org's own website field is empty, and the Wayback availability API answered 429.

Fetch check (2026-11-04, headed): transport ok, PDF, picked container 04/1246's `20261101B.pdf`, the 1 November 2026 issue read above; issue date 2026-11-01, freshness fresh. Identity `unverified` only because no expected identity is supplied.

## Not yet confirmed

Whether the parish has a new website (structured research holds the retry trigger). It does not affect the bulletin.
