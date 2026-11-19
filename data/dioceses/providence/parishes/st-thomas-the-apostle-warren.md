---
name: St. Thomas the Apostle
website: https://parishesonline.com/organization/st-thomas-the-apostle-church-02885
bulletin_provider: parishes_online
provider_id: st-thomas-the-apostle-church-02885
publication: ['po-org:st-thomas-the-apostle-church-02885', 'lpi:0018000000Qc2WcAAJ', 'po-container:03/0224']
group: St. Mary of the Bay, Warren (with St. Thomas the Apostle mission)
evidence:
- url: https://container.parishesonline.com/bulletins/03/0224/20261025B.pdf
  seen: 2026-11-15
  quote: 'PLEASE NOTE: There will be no bulletin until the'
  note: '25 October 2026 issue, 4 pages. Page 1 (rendered; its text layer is an old September 2023 page)
    masthead ''St. Thomas the Apostle / 500 METACOM AVENUE • WARREN, RHODE ISLAND 02885 / A MISSION OF
    SAINT MARY OF THE BAY PARISH''; ''MASSES: Saturday – Sábado: 4:00 PM - Vigil Mass / Sunday – Domingo:
    10:30 AM / Daily Mass and Holy Days: Visit stmaryofthebay.org''; ''Father Joseph R. Upton, Ph.D.,
    Pastor''. Page 2 ''Thirtieth Sunday in Ordinary Time October 25, 2026'', Mass intentions Saturday
    4pm and Sunday 10:30am through Sunday 15 November, and the notice ''...no bulletin until the weekend
    of November 21 & 22 due to the Parish Pilgrimage to Greece. In the meantime, please consult the Saint
    Mary of the Bay Parish bulletin''.'
- url: https://parishesonline.com/organization/st-thomas-the-apostle-church-02885
  seen: 2026-11-15
  note: 'probe po: ''St. Thomas the Apostle Church'', 500 Metacom Ave, Warren, Rhode Island, 02885-2808,
    LPi 0018000000Qc2WcAAJ, container 03/0224, issues weekly to 2026-10-25. probe container 03/0224 on
    2026-11-15: 1, 8 and 15 November answer 403 while St. Mary of the Bay''s 03/0705 has its 15 November
    issue.'
revisit: Check container 03/0224 for the 22 November 2026 issue (the 25 October issue announced no bulletin
  until the weekend of November 21 & 22); if it never resumes, read the St. Mary of the Bay bulletin for
  St. Thomas's Masses and merge.
revisit_after: 2026-11-24
promoted: 2026-11-16
research:
- method: probe container 03/0224 --weeks 4 (and probe po st-thomas-the-apostle-church-02885)
  url: https://parishesonline.com/organization/st-thomas-the-apostle-church-02885
  checked: '2026-11-15'
  outcome: not-published
  next_action: Probe container 03/0224 for 20261122B.pdf; read its masthead and schedule, then rerun fetch:check
  retry_when: After the weekend of 21-22 November 2026, when the 25 October issue says the bulletin resumes
  revisit_after: 2026-11-24
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --diocese providence --parish
    st-thomas-the-apostle-warren
  url: https://container.parishesonline.com/bulletins/03/0224/20261025B.pdf
  checked: '2026-11-15'
  outcome: not-found
  next_action: Rerun fetch:check once the 22 November 2026 issue is in container 03/0224 and confirm it
    picks it (page 1's text layer is a stale September 2023 page, so expect a date conflict to be reported
    unless the issue is rebuilt)
  retry_when: The 22 November 2026 issue appears in container 03/0224
  revisit_after: 2026-11-24
bulletin_status: available
publication_reviews:
- parish: st-mary-of-the-bay-warren
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/0224/20261025B.pdf
    seen: 2026-11-15
    note: The 25 October 2026 masthead names St. Thomas the Apostle alone, 500 Metacom Avenue, 'A MISSION
      OF SAINT MARY OF THE BAY PARISH', with its own Mass schedule (Saturday 4:00 PM, Sunday 10:30 AM)
      and intentions.
  - url: https://container.parishesonline.com/bulletins/03/0705/20261115B.pdf
    seen: 2026-11-15
    note: The 15 November 2026 St. Mary of the Bay bulletin lists Masses at St. Mary of the Bay and Saint
      Alexander only; its schedule does not include St. Thomas.
---

## Publisher

St. Thomas the Apostle merged into St. Mary of the Bay on 11 May 2026 (finder 12227: "Saint Thomas the Apostle Parish will merge into Saint Mary of the Bay Parish"), but the church keeps its own weekly ParishesOnline bulletin, container 03/0224. The latest issue, 25 October 2026 (https://container.parishesonline.com/bulletins/03/0224/20261025B.pdf), page 1 (image; its text layer is a stale 2023 page), is headed "St. Thomas the Apostle / 500 METACOM AVENUE • WARREN, RHODE ISLAND 02885 / A MISSION OF SAINT MARY OF THE BAY PARISH", with "MASSES: Saturday – Sábado: 4:00 PM - Vigil Mass / Sunday – Domingo: 10:30 AM" and Father Joseph R. Upton, Ph.D., Pastor. Page 2 is dated October 25, 2026 and gives intentions for the Saturday 4pm and Sunday 10:30am Masses through 15 November.

The St. Mary of the Bay bulletin (container 03/0705) does not list these Masses, so the two are separate bulletins and separate rows, grouped as one parish (see `publication_reviews`).

## Worship sites

One church: St. Thomas the Apostle, 500 Metacom Ave., Warren (Saturday 4:00 PM, Sunday 10:30 AM). The finder (12227) and GCatholic (22445) list it. Daily Mass and holy days are at St. Mary of the Bay ("Visit stmaryofthebay.org").

## Website and bulletin provider

`parishes_online` on org `st-thomas-the-apostle-church-02885`. The parish has no website of its own; the finder points to stmaryofthebay.org.

## Not yet confirmed

Whether the bulletin resumes. The 25 October 2026 issue says "There will be no bulletin until the weekend of November 21 & 22 due to the Parish Pilgrimage to Greece", so on 2026-11-15 the newest issue is three weeks old and `fetch:check` can't pick a current one. Check container 03/0224 for the 22 November issue after 2026-11-24 (see `research`). If it does not resume and St. Mary of the Bay's bulletin starts listing St. Thomas's Masses, merge this row into st-mary-of-the-bay-warren.

fetch:check on 2026-11-15 downloaded the 25 October 2026 issue (transport ok, PDF) but reported its date as a conflict: page 1's text layer is an old 'September 17, 2023' page under the current image, while page 2 says October 25, 2026.
