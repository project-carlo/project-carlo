---
name: St. Patrick Parish
website: http://www.saintpatrickparisherie.org
bulletin_provider: parishes_online
provider_id: st-patrick-parish-16507
publication: ['po-org:st-patrick-parish-16507', 'lpi:0018000000QxBkcAAF', 'po-container:14/1195']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/1195/20261025B.pdf
  seen: 2026-10-23
  quote: St. Patrick Parish - Erie, PA 14-1195
  note: 'Footer of page 4 of the 25 October 2026 issue (4 pages, text layer). Page 1 masthead: ''SAINT
    PATRICK PARISH, 130 EAST 4TH STREET, ERIE, PA 16507, Serving the East Bayfront since 1837'', ''* OCTOBER
    25, 2026 * 30TH SUNDAY IN ORDINARY TIME''; ''MASS SCHEDULE Saturday: 5:00 pm; Sunday: 8:00 am & 10:30
    am; Holy Day Mass: 12:00 pm''; ''Pastor: Fr. Mike DeMartinis ... In residence: Fr. Denny Veltri''.'
- url: https://container.parishesonline.com/bulletins/14/1195/20261025B.pdf
  seen: 2026-10-23
  quote: We have only one Priest, our Pastor, Fr. Mike DeMartinis, who celebrates three Masses total each
    week.
  note: Page 2. Consistent with the three weekend Masses (Sat 5:00 pm, Sun 8:00 am and 10:30 am). Page
    3 lists weekday Mass intentions at '7:45am Cathedral PREP Chapel - Parishioners of St. Patrick', which
    is Cathedral Prep's school chapel, not a St. Patrick worship site.
- url: http://www.saintpatrickparisherie.org/bulletin.html
  seen: 2026-10-23
  quote: Get the latest published bulletins
  note: The parish's own Bulletins page (plain curl, HTTP 200; probe url answered 200 on the bare host,
    so the connection reset the directory scout saw did not recur) links 'PARISHES ONLINE ... from St.
    Patrick Parish!' to https://www.parishesonline.com/find/st-patrick-parish-16507, plus yearly archive
    pages for 2017-2020. It hosts no current PDFs itself.
- url: https://parishesonline.com/organization/st-patrick-parish-16507
  seen: 2026-10-23
  note: 'probe po: ''St. Patrick Parish'', 130 E 4th St, Erie PA 16507, website http://www.saintpatrickparisherie.org/,
    LPi 0018000000QxBkcAAF, container 14/1195, latest issue 2026-10-25.'
- url: https://www.eriercd.org/Parish10219-St-Patrick.html
  seen: 2026-10-23
  note: 'Diocese directory record 10219 (GCatholic 24547): one parish record, no mission or partner; Sat
    5 p.m.; Sun 8, 10:30 a.m. (livestream 10:30); holy day 12 p.m.; no daily Mass. Pastor Rev. Michael
    DeMartinis, priest in residence Rev. Dennis Veltri.'
research:
- method: pnpm fetch:check --diocese erie --parish st-patrick-erie --expected-identity 'SAINT PATRICK'
    --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://parishesonline.com/organization/st-patrick-parish-16507
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF (container 14/1195, 20261025B.pdf), identity matched on page 1,
    issue date 2026-10-25 inferred from the URL and read from the masthead; freshness 'future' only because
    it posts two days early.
---

## Publisher

St. Patrick Parish, Erie (130 E. 4th St., 16507; the downtown/East Bayfront parish founded 1837) publishes its own weekly bulletin through ParishesOnline (organization `st-patrick-parish-16507`, container 14/1195). I read the 25 October 2026 issue on 2026-10-23: the masthead names 'Saint Patrick Parish, 130 East 4th Street, Erie, PA 16507' and the content (Mass schedule, pastor's note, OCIA, novena in the church chapel, St. Patrick Haven drive) is about this parish alone. Pastor: Rev. Michael G. DeMartinis (bulletin; the diocese directory agrees; the clergy list gives his assignment only as faculty at Cathedral Prep, 'Faculty ... Cathedral Prep', with no parish line, so the pastorship comes from the bulletin and directory). Fr. Dennis Veltri is in residence.

The parish is a stand-alone parish: the directory shows one parish record, no mission, partner or secondary church. St. Patrick's own site links the ParishesOnline listing, so the lead that the site resets connections is moot for the bulletin: it answered on 2026-10-23.

## Worship sites

One church, St. Patrick at 130 E. 4th St. Weekend Masses in the 25 Oct issue: Saturday 5:00 pm, Sunday 8:00 am and 10:30 am (livestreamed), holy day 12:00 pm; no weekday Mass at the church. The weekday intentions on page 3 are 'Cathedral PREP Chapel' Masses (7:45 am) offered for St. Patrick parishioners; that chapel is Cathedral Prep school's, in another batch's scope, and not a St. Patrick site. A 'St. Patrick Church Chapel' appears as a room for a novena and a rosary group (6:00 pm), not a separate Mass site.

## Website and bulletin provider

`saintpatrickparisherie.org` is an old Homestead site that links the ParishesOnline listing and hosts no current bulletin PDFs; the listing's three ids are one bulletin. The pipeline reads ParishesOnline by `provider_id`.

## Not yet confirmed

Nothing affecting the row. The 'Cathedral Prep chapel weekday Mass' may merit a check by whoever covers Cathedral Prep (a lead, not a St. Patrick site).
