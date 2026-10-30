---
name: Our Lady of Fatima Parish
website: https://www.fatimakeyport.org/
bulletin_provider: parishes_online
provider_id: parish-of-our-lady-of-fatima
publication: ['po-org:parish-of-our-lady-of-fatima', 'lpi:0018000000Qx8o9AAB', 'po-container:04/0792']
group: Cohort 14 (Keyport, Matawan, Union Beach, Holmdel)
evidence:
- url: https://container.parishesonline.com/bulletins/04/0792/20261101B.pdf
  seen: 2026-10-30
  quote: 118 Broad Street
  note: '1 November 2026 issue (12 pages, 10 with text), page 1 cover: "SAINT JOSEPH CATHOLIC CHURCH 376
    Maple Place Keyport, NJ. 07735" and "JESUS THE LORD CATHOLIC CHURCH 118 Broad Street Keyport, NJ.
    07735", parish office 376 Maple Place 732-264-0322, www.fatimakeyport.org, dated "November 1st, 2026"
    (a stray "May 17th, 2026" template line sits above). Page 2: Mass intentions Saturday 4:00 pm, Sunday
    9:00 am, 10:30 am and 12:00 pm, Tuesday and Thursday 12:00 pm, Wednesday 7:00 pm. The 27 September,
    4 and 18 October and 25 October issues carry the same masthead.'
- url: https://www.fatimakeyport.org/
  seen: 2026-10-30
  quote: Merged Parish of St. Joseph Church and Jesus the Lord Church
  note: 'Homepage (Wix): "Our Lady of Fatima Parish ... 376 Maple Place, Keyport NJ"; Weekly Bulletin
    page embeds the ParishesOnline organization parish-of-our-lady-of-fatima.'
- url: https://www.fatimakeyport.org/mass-schedule
  seen: 2026-10-30
  quote: 10:30 Mass (Live streamed)
  note: 'Mass Schedule page: Tuesday and Thursday 12pm; Wednesday adoration 6:30pm then Spanish Mass 7pm;
    Saturday confessions 3:15-3:45 then 4pm Mass; Sunday 9am Children''s Mass, 10:30 Mass, 12pm Spanish
    Mass. It names no church for any Mass.'
- url: https://trentonmonitor.com/2026/06/14/keyport-church-marks-golden-jubilee/
  seen: 2026-10-30
  quote: have formed Our Lady of Fatima Parish
  note: 'The Monitor, 14 June 2026: "Since 2019, St. Joseph Church and Jesus the Lord Church - both in
    Keyport - have formed Our Lady of Fatima Parish, one bilingual, multicultural faith community"; pastor
    Father Rene Pulgarin; Anniversary Mass for St. Joseph Church on 13 June 2026.'
- url: https://files.ecatholic.com/14277/documents/2024/7/2024%20July%20-%20Updated%20%20Parish%20Cohorts%20and%20Deaneries.pdf
  seen: 2026-10-30
  quote: Keyport
  note: July 2024 cohort list, Cohort 14, lists Our Lady of Fatima (Keyport) as one parish.
research:
- method: Grepped the 27 Sept, 4, 18, 25 Oct and 1 Nov 2026 issues for "Jesus the Lord", "Jesus el Senor"
    and "Broad"; read the site Mass Schedule and Parish Life pages; searched The Monitor for "Jesus the
    Lord Keyport"
  url: https://www.fatimakeyport.org/mass-schedule
  checked: '2026-10-30'
  outcome: not-found
  next_action: 'Find a source that says which church holds the weekday and weekend Masses: the parish
    office (732-264-0322), a Mass-time sheet at the church, or an issue with a per-church schedule.'
  retry_when: A bulletin or the site lists a Mass at Jesus the Lord Church, or says it has closed.
  revisit_after: 2027-01-31
- method: pnpm fetch:check --diocese trenton --parish our-lady-of-fatima-keyport (headed Chrome)
  url: https://container.parishesonline.com/bulletins/04/0792/
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: it picked the 1 November 2026 issue; the date conflict comes from a stale "May 17th,
    2026" template line on the cover.'
bulletin_status: available
---

## Publisher

Our Lady of Fatima Parish, Keyport (Cohort 14), the 2017 merger of St. Joseph and Jesus the Lord, in effect since 2019 (The Monitor, 14 June 2026). It publishes one weekly bulletin through ParishesOnline (org `parish-of-our-lady-of-fatima`, container 04/0792, latest 1 November 2026), linked from the Weekly Bulletin page of fatimakeyport.org. The cover names both churches, St. Joseph (376 Maple Place) and Jesus the Lord (118 Broad Street), with the parish office at 376 Maple Place. Pastor Rev. Rene Pulgarin (Monitor; site staff page). Holy Family, Union Beach, the "potential linkage" in the 2017 plan, has a different pastor and its own Bon Venture bulletin and is a separate row.

## Worship sites

St. Joseph Church, 376 Maple Place, is a church row: the site and bulletin print its address as the parish's, and the Monitor reports its 13 June 2026 Anniversary Mass and a 22 February 2026 Sunday Mass there. GCatholic's separate "St. Joseph" (18768) and the finder's pin (14616) are the same place (376 Maple Pl.).

Jesus the Lord Church (GCatholic 18710, 123 Broad St.; the bulletin prints 118 Broad Street) is named in every masthead read and the bulletin lists a prayer group at "Iglesia Jesús el Señor" and a Cursillo at "Casa Parroquial Jesús el Señor", but **no source read says Mass is held there**: the bulletin and site Mass schedules name no church. It is kept in `open/` rather than excluded, since nothing says it closed. See `open/jesus-the-lord-keyport`.

## Website and bulletin provider

fatimakeyport.org is a Wix site (reads with `probe url`); the bulletin is ParishesOnline, so the row is `parishes_online` with the org slug. GCatholic's St. Joseph website stjosephkeyport.com has no DNS.

`fetch:check` (2026-10-30, headed Chrome) picked the 1 November 2026 issue from the publication page (container 04/0792, `20261101B.pdf`): transport ok, PDF. Its issue-date check reports a **conflict**, not a stale issue: the cover prints "May 17th, 2026" (a template line the parish has left in every issue since at least 27 September) beside "November 1st, 2026", and the file name and the ParishesOnline list both date it 1 November. Freshness is therefore "unknown" to the check; the issue is the current one.
