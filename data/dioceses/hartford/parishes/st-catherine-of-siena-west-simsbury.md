---
name: St. Catherine of Siena Parish
website: https://stcatherine.info/bulletins/
bulletin_provider: other
provider_id: page-pdfs
publication: []
group: ''
evidence:
- url: https://stcatherine.info/wp-content/uploads/2026/10/STC-Bulletin-11126.pdf
  seen: 2026-11-13
  quote: 267 Stratton Brook Road, Box 184
  note: 'Page 1 masthead of the 1 November 2026 (All Saints) issue: Saint Catherine of Siena Roman Catholic
    Church, West Simsbury, Connecticut 06092; Pastor Reverend Michael Whyte. Mass/Liturgy Schedule: Saturday
    Vigil 5:00 p.m.; Sunday 8:00 a.m. and 11:00 a.m.; daily 8:30 a.m. Monday through Wednesday and Friday.
    No other church named.'
- url: https://stcatherine.info/bulletins/
  seen: 2026-11-13
  note: Bulletins page links two self-uploaded PDFs (STC-Bulletin-11126.pdf and STC-Bulletin-102526-_2_.pdf,
    both in /2026/10/) and parishesonline.com/organization/st-catherine-of-siena-roman-catholic-church-6092.
- url: https://parishesonline.com/organization/st-catherine-of-siena-roman-catholic-church-6092
  seen: 2026-11-13
  note: 'probe po: org exists (LPi id 0018000000Qc1G0AAJ, 264 Stratton Brook Rd) but lists no publications.'
research:
- method: probe get of the Bulletins page; newest linked issue
  url: https://stcatherine.info/bulletins/
  checked: '2026-11-13'
  outcome: found
  next_action: Confirm the 8 and 15 November issues get posted (the newest on 2026-11-13 was 1 November)
  retry_when: Next map or reconcile pass
  revisit_after: 2026-11-20
bulletin_status: available
---

## Publisher

St. Catherine of Siena Parish, West Simsbury publishes its own bulletin as PDFs uploaded to its WordPress site (stcatherine.info, not on cdn.diocesanweb.org). The 1 November 2026 issue (`STC-Bulletin-11126.pdf`, 6 pages, text layer) has the masthead on page 1: "Saint Catherine of Siena Roman Catholic Church", "267 Stratton Brook Road, Box 184 West Simsbury, Connecticut 06092", Pastor Reverend Michael Whyte. The site also links a ParishesOnline org (`st-catherine-of-siena-roman-catholic-church-6092`, LPi 0018000000Qc1G0AAJ) that `probe po` found with no publications on 2026-11-13; since nothing is published there, its ids are kept in evidence, not in `publication`.

## Worship sites

One: St. Catherine of Siena Church, 265 Stratton Brook Rd (`st-catherine-of-siena-west-simsbury`). Page 1's schedule (Saturday vigil 5:00 p.m.; Sunday 8:00 and 11:00 a.m.; daily 8:30 a.m. Monday to Wednesday and Friday) names no other place. The directory (2) and GCatholic (22233) list this church.

## Website and bulletin provider

`other`, recipe `page-pdfs` (printed by `fetch:check` on 2026-11-13). stcatherine.info/bulletins/ links the two newest issues. On Friday 13 November 2026 the newest was 1 November (the 8 November issue was not posted), so `fetch:check` picked it as first-listed rather than current: the right document, but two weeks old.

## Not yet confirmed

How regularly the issues are posted: check after 2026-11-20 that the 8 and 15 November issues appeared.
