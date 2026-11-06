---
name: St. Andrew, Westwood
website: https://standrewcc.com/
bulletin_provider: parishes_online
provider_id: church-of-st-andrew-07675
publication: ['po-org:church-of-st-andrew-07675', 'lpi:0018000000Qc09qAAB', 'po-container:04/1253']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/1253/20261101B.pdf
  seen: 2026-11-03
  quote: Saturday 5:00 PM (Live streamed on YouTube)
  note: '1 November 2026 issue (8 pages, text layer). Page 1 masthead: CHURCH OF ST. ANDREW, Rev. Diego
    Navarro, Pastor; Parish Office (Parish Center) 120 Washington Ave. Westwood, NJ 07675. Page 2 schedule:
    Saturday 5:00 PM; Sunday 8 AM, 10:30 AM, 12:15 PM and 2 PM in Spanish; Daily Monday-Saturday 9 AM
    and Wednesday 7 PM (Spanish). Ad-page footer ''Church of St. Andrew, Westwood, NJ 04-1253''. No other
    church named.'
- url: https://parishesonline.com/organization/church-of-st-andrew-07675
  seen: 2026-11-03
  note: 'probe po: org ''Church of St. Andrew'', 120 Washington Ave, Westwood, lpi 0018000000Qc09qAAB,
    container 04/1253, weekly issues 27 September to 1 November 2026.'
- url: https://standrewcc.com/
  seen: 2026-11-03
  quote: 120 Washington Ave, Westwood, New Jersey
  note: Parish eCatholic site (ecatholic:13436; answers probe get 403, read with visit.py). Its 'Bulletins'
    menu item links parishesonline.com/organization/church-of-st-andrew-07675; no files.ecatholic.com
    bulletins (issues.py found none for 18 Oct-1 Nov 2026).
bulletin_status: available
---

## Publisher

The Church of St. Andrew, Westwood, publishes a weekly LPi bulletin on ParishesOnline (org `church-of-st-andrew-07675`, container 04/1253). I read the 1 November 2026 issue (Solemnity of All Saints): the page 1 masthead names the Church of St. Andrew alone (Rev. Diego Navarro, Pastor; Parish Center, 120 Washington Ave.), page 2 gives its Mass schedule, and the ad pages carry the footer 'Church of St. Andrew, Westwood, NJ 04-1253'.

## Worship sites

- Church of St. Andrew, 120 Washington Avenue (`st-andrew-westwood`): Saturday 5:00 PM; Sunday 8:00, 10:30 AM, 12:15 PM, 2:00 PM (Spanish); Monday–Saturday 9:00 AM; Wednesday 7:00 PM (Spanish).

The directory (215) and GCatholic (18583) list only this church. The parish site mentions a Parish Center Chapel (Thursday adoration; confession 'After the 9 AM Mass in the Chapel'), on the same campus as the church; see *Not yet confirmed*.

## Website and bulletin provider

The directory's https://standrewcc.com/ is an eCatholic site (ecatholic:13436) behind Cloudflare (`probe get` 403, `visit.py` loads it). It posts no eCatholic bulletins; its Bulletins menu links the ParishesOnline org, which `fetch` reads by `provider_id`. GCatholic's saintandrewswestwood.com was not checked.

Fetch check (2026-11-03, headed): transport ok, PDF, picked container 04/1253 `20261101B.pdf`, the 1 November 2026 issue read above; freshness fresh. The check reports publication identity `unverified`; the masthead read above confirms it is St. Andrew's.

## Not yet confirmed

Whether the weekday 9 AM Mass is said in the Parish Center Chapel rather than the church. Neither the site nor the bulletin says where it is; the chapel shares the 120 Washington Avenue campus, so it would not change which building the map points to. Settle by reading the parish's Mass-times wording in a later bulletin.
