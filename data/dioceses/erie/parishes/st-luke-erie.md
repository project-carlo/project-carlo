---
name: St. Luke and Our Lady of Mount Carmel Parishes
website: https://www.stlukeolmc.org
bulletin_provider: parishes_online
provider_id: st-luke-church-16504
publication: ['po-org:st-luke-church-16504', 'po-org:our-lady-of-mount-carmel-church-16510', 'lpi:0018000000Qc27IAAR',
  'lpi:0018000000QxBkiAAF', 'po-container:14/1178']
group: 'Erie partnership: St. Luke, Our Lady of Mount Carmel; pastor Rev. Lawrence R. Richards'
evidence:
- url: https://container.parishesonline.com/bulletins/14/1178/20261025B.pdf
  seen: 2026-10-23
  quote: Our Lady
  note: 'Page 1 masthead of the 25 October 2026 issue (8 pages; the probe reads 4): ''Saint Luke and Our
    Lady of Mt. Carmel Parishes'', ''421 East 38th Street Erie, PA 16504'' and ''1531 East Grandview Blvd
    Erie, PA 16510'', ''The Thirtieth Sunday in Ordinary Time October 25, 2026''. Page 3 footer ''ST LUKE
    & OUR LADY OF MT CARMEL PARISHES ERIE, PA''.'
- url: https://container.parishesonline.com/bulletins/14/1178/20261025B.pdf
  seen: 2026-10-23
  quote: MASS SCHEDULE
  note: 'Pages 7-8 (pdftotext -layout) have two Mass-intention columns: ''OUR LADY OF MT. CARMEL MASS
    SCHEDULE'' (Sat Oct 24 4:00, Sun Oct 25 8:00, Tue Oct 27 7:30, Thu Oct 29 7:30, Sat Oct 31 4:00, Sun
    Nov 1 8:00) and ''ST. LUKE MASS SCHEDULE'' (Sat 5:00, Sun 9:00 and 11:30, Mon 7:30, Wed 7:30, Fri
    7:30, Sat Oct 31 5:00, Sun Nov 1 9:00 and 11:30). ''UP COMING MASSES November 1: 4:00pm vigil at OLMC
    with Fr. Larry; 5:00pm vigil at St. Luke with Fr. Joe; 8:00am at OLMC with Fr. Cas; 9:00 am at St.
    Luke with Fr. Larry; 11:30 at St. Luke with Fr. Larry''. Signed by the pastor as ''Fr. Larry''.'
- url: https://www.stlukeolmc.org/bulletin
  seen: 2026-10-23
  note: 'Wix site (visit.py, headed Chrome): the Bulletin page embeds ParishesOnline publication links
    for container 14/1178 (issues 20261025B, 20261018B, 20261011B, 20261004B) under the publication page
    st-luke-church-16504; header ''Office Address: 421 East 38th St'' and ''Church Hours: St. Luke: ...
    OLMC: Varies''. probe url sees LPi 0018000000Qc27IAAR.'
- url: https://parishesonline.com/organization/our-lady-of-mount-carmel-church-16510
  seen: 2026-10-23
  note: 'probe po: a second ParishesOnline organization ''Our Lady of Mount Carmel Church'' (LPi 0018000000QxBkiAAF,
    website olmc-erie.org, 1531 East Grandview Blvd.) lists container 14/1178 and the same issue URLs
    (2026-10-25, 10-18, 10-11) as st-luke-church-16504 (''St. Luke Church'', 421 E 38th St, website https://www.stlukeolmc.org/).
    Two organization records, one bulletin.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor ................................................................1) Our Lady of Mt. Carmel;
    2) St. Luke, Erie
  note: Clergy list 'Updated 8/7/2026', entry Richards, Rev. Lawrence R. (the dotted leader is longer
    in the PDF).
- url: https://www.eriercd.org/images/directoryparishchurch.pdf
  seen: 2026-10-23
  quote: Partnered with Our Lady of Mount Carmel Parish
  note: 'Printable directory (Oct. 6, 2026): St. Luke Parish ''Partnered with Our Lady of Mount Carmel
    Parish'', pastor Reverend Lawrence R. Richards; Our Lady of Mount Carmel Parish ''Partnered with St.
    Luke Parish, Erie'', mailing ''c/o St. Luke Parish''. Both give website https://www.stlukeolmc.org.'
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese erie --parish st-luke-erie --expected-identity "Mt. Carmel" --expected-issue-date
    2026-10-25 (headed Chrome)
  url: https://parishesonline.com/publication-page/st-luke-church-16504
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF (container 14/1178, 20261025B.pdf), identity matched, issue date
    observed 2026-10-25; freshness reads future only because the Sunday issue is posted two days early
    on 2026-10-23.
- method: probe url on lukealive.org and olmc-erie.org (GCatholic websites for St. Luke and OLMC) and
    stlukeolmc.org
  url: http://www.olmc-erie.org
  checked: '2026-10-23'
  outcome: access-blocked
  next_action: 'None needed for the bulletin: the stlukeolmc.org /bulletin page and both ParishesOnline
    organizations carry container 14/1178. Open olmc-erie.org in the browser only if its content is wanted
    as extra evidence.'
  retry_when: stlukeolmc.org stops posting the ParishesOnline bulletin
publication_reviews:
- parish: st-john-the-baptist-erie
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/14/1178/20261025B.pdf
    seen: 2026-10-23
    quote: Our Lady
    note: Container 14/1178, 25 Oct 2026 masthead 'Saint Luke and Our Lady of Mt. Carmel Parishes' (421
      East 38th St and 1531 East Grandview Blvd); content (pastor's desk by Fr. Larry, finances for OLMC
      and St. Luke, Mass schedules at OLMC and St. Luke) concerns those two parishes only.
  - url: https://container.parishesonline.com/bulletins/14/0962/20261025B.pdf
    seen: 2026-10-23
    quote: Holy Rosary Mission Church
    note: 'Container 14/0962, same date: masthead for St. John the Baptist, Holy Trinity and Holy Rosary
      under Rev. James Piszker. Different container, masthead, pastor and content: two bulletins.'
---

## Publisher

St. Luke and Our Lady of Mount Carmel (OLMC), Erie, share one weekly bulletin through ParishesOnline (container 14/1178). I read the 25 October 2026 issue on 2026-10-23: the page 1 masthead is 'Saint Luke and Our Lady of Mt. Carmel Parishes' with both addresses, page 3 is financials for both parishes, and the last pages carry two Mass-intention columns, 'OUR LADY OF MT. CARMEL' and 'ST. LUKE'. The pastor's column is signed 'Fr. Larry' (Rev. Lawrence R. Richards, pastor of both per the clergy list 'Updated 8/7/2026'). One row, per the one-bulletin rule.

Peer decision (shared): OLMC (directory 10205, GCatholic 24455) is folded into this row; it has its own ParishesOnline organization record (our-lady-of-mount-carmel-church-16510, LPi 0018000000QxBkiAAF) but that record serves the same container and issues, so it is the same bulletin, not a second channel. No shared review is recorded for OLMC because a review needs a peer parish row. Peer decision (separate): the neighbouring St. John the Baptist / Holy Trinity / Holy Rosary row prints a different bulletin (container 14/0962); see `publication_reviews`.

## Worship sites

Two churches, both with Mass in the 25 October bulletin: St. Luke (421 E 38th St; Saturday 5:00, Sunday 9:00 and 11:30, weekdays Mon/Wed/Fri 7:30) and OLMC (1531 E Grandview Blvd; Saturday 4:00, Sunday 8:00, Tuesday and Thursday 7:30). The diocese directory's weekday times differ from the bulletin (printable directory: St. Luke Mon/Tue/Thu/Fri 8 a.m. with a Wednesday student liturgy 8:30; OLMC Monday through Friday 7 a.m.; web record: St. Luke daily 7:30 with Tue/Thu at OLMC); the bulletin's Mass-intention columns are the current source and are what I followed.

## Website and bulletin provider

Website https://www.stlukeolmc.org (Wix; the /bulletin page embeds the ParishesOnline publications, `probe url` on the bare site finds none). Provider: parishes_online, organization st-luke-church-16504 (LPi 0018000000Qc27IAAR, container 14/1178). The OLMC organization record is the same container. The GCatholic websites olmc-erie.org (403 to probe url) and lukealive.org (dead DNS) are old.

## Not yet confirmed

The probe reads only the first four of the bulletin's eight pages; the Mass-intention columns are on pages 7-8 and came from the saved PDF, not from `probe pdf`.
