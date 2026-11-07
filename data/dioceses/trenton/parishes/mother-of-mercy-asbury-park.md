---
name: Mother of Mercy Parish
website: https://parishesonline.com/organization/mother-of-mercy-parish
bulletin_provider: parishes_online
provider_id: mother-of-mercy-parish
publication: ['po-org:mother-of-mercy-parish', 'lpi:0018000000Qbzz7AAB', 'po-container:04/0324']
group: Cohort 18 (Asbury Park, Neptune)
evidence:
- url: https://container.parishesonline.com/bulletins/04/0324/20261101B.pdf
  seen: 2026-10-30
  quote: Fr. Stephen Michael, SVD, Pastor
  note: 'Page 1 of the 1 November 2026 issue (8 pages, text layer): ''PASTORAL TEAM'' (Fr. Stephen Michael,
    SVD, Pastor; Fr. Paul Janvier and Fr. Francis Xavier Rayappan, SVD, Parochial Vicars; Fr. Enel Almeus,
    CSSp, Chaplain), ''Parish Office Address: 1212 First Avenue, Asbury Park'', the Mass schedule (Daily
    Monday-Friday 9:00 AM; Saturday 4:00 PM English, 7:00 PM Spanish; Sunday 7:30, 9:00, 10:30, 12:00
    Noon, 2:00 PM Creole, 4:00 PM) and ''The Church of Mother of Mercy / Worship Site: / Our Lady of Mt.
    Carmel Church / 1201 Asbury Avenue, Asbury Park, NJ 07712''. The footer of pages 7-8 reads ''Mother
    of Mercy Parish | 04-0324''. It names this parish alone, with one worship site.'
- url: https://parishesonline.com/organization/mother-of-mercy-parish
  seen: 2026-10-30
  note: 'probe po mother-of-mercy-parish: org ''Mother of Mercy Parish'', lpi 0018000000Qbzz7AAB, container
    04/0324, address 805 Pine St, Asbury Park 07712-5793, website https://www.momapnj.org/, latest issue
    2026-11-01 (the 25 October issue is below it).'
- url: https://trentonmonitor.com/2020/12/04/holy-spirit-church-closure-to-help-ensure-catholic/
  seen: 2026-10-30
  quote: Holy Spirit Church, one of two worship sites of Mother of Mercy Parish, will be closing
  note: 'The Monitor, 2020-12-04: the parish formed in 2014 from Our Lady of Mount Carmel and Holy Spirit
    (with St. Peter Claver and Our Lady of Providence earlier); after the sale of Holy Spirit it plans
    to hold its Masses at Mount Carmel Church. See excluded/holy-spirit-asbury-park.'
- url: https://trentonmonitor.com/2023/04/29/priest-personnel-changes-2023/
  seen: 2026-10-30
  quote: Father Stephen Michael, S.V.D, from parochial vicar to administrator, Mother of Mercy Parish,
    Asbury Park
  note: The Monitor's Priest Personnel Changes 2023 (assignments effective 1 July 2023) moves Fr. Stephen
    Michael to administrator of Mother of Mercy and Fr. Miguel Virella from its pastor to pastor of St.
    Mark, Sea Girt, with Fr. Francis Xavier Rayappan, SVD as parochial vicar. The 1 November 2026 bulletin
    styles Fr. Michael 'Pastor'; the post gives the title it gave in 2023.
- url: https://trentonmonitor.com/2026/08/17/clergy-appointments-8/
  seen: 2026-10-30
  quote: with residence in Mother of Mercy Parish, Asbury Park, effective Sept. 1, 2026
  note: 'The Monitor''s Clergy Appointments of 2026-08-17 gives Rev. Enel Almeus, chaplain at Jersey Shore
    Medical Center, residence in Mother of Mercy Parish: the bulletin''s ''Fr. Enel Almeus, CSSp, Chaplain''.'
promoted: 2026-10-30
research:
- method: pnpm diocese probe url and parish-site-access visit.py on https://www.momapnj.org/ and https://momapnj.org/
  url: https://momapnj.org/
  checked: '2026-10-30'
  outcome: not-found
  next_action: 'None for the bulletin: the row reads ParishesOnline. If the parish reconnects a site,
    read its homepage for a second bulletin channel and a Mass-times page.'
  retry_when: momapnj.org stops showing Wix's 'Reconnect Your Domain' page
  revisit_after: 2027-04-30
- method: Wayback Machine snapshot of the old site, read with visit.py
  url: http://web.archive.org/web/20260421103907/https://www.momapnj.org/
  checked: '2026-10-30'
  outcome: found
  next_action: None. The 21 April 2026 snapshot was a Wix site whose '↓↓ BULLETIN ↓↓' button links parishesonline.com/publicationWidget.js;
    it gives the address '1212 First Ave, Asbury Park, NJ, 07712. Tel 732-775-1056' and has a Mass Schedule
    page that renders no text in the archive.
- method: pnpm fetch:check --diocese trenton --parish mother-of-mercy-asbury-park (headed Chrome)
  url: https://parishesonline.com/organization/mother-of-mercy-parish
  checked: '2026-10-30'
  outcome: found
  next_action: 'None; transport ok, document_type pdf, picks the 1 November 2026 issue (freshness future:
    the coming Sunday issue, posted early); publication identity unverified because no expected identity
    is supplied'
bulletin_status: available
publication_reviews:
- parish: holy-innocents-neptune
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/04/0324/20261101B.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Mother of Mercy Parish alone, with Fr. Stephen Michael as
      pastor and Our Lady of Mt. Carmel as its one worship site; Holy Innocents' own bulletin (John Patrick
      608) has Fr. H. Todd Carter as pastor and a different Mass schedule.
---

## Publisher

Mother of Mercy Parish ("The Church of Mother of Mercy", Asbury Park) publishes its own weekly bulletin through ParishesOnline: org `mother-of-mercy-parish`, container 04/0324. The 1 November 2026 issue (page 1, text layer) lists the pastoral team and the parish office at 1212 First Avenue, a Mass schedule of a weekday Mass, two Saturday Masses and six Sunday Masses in English, Spanish, Creole and bilingual, and one worship site: "Our Lady of Mt. Carmel Church, 1201 Asbury Avenue". Nothing in it names Holy Innocents, Neptune, the other Cohort 18 parish, or any other parish; Holy Innocents has its own John Patrick listing and masthead, so this is a single-parish row.

I found this container through a web search for the parish's bulletin (`probe po mother-of-mercy-parish` confirms the org and its container); the printer's footer 'Mother of Mercy Parish | 04-0324' is what ties the issue to the parish. John Patrick's scan has no Asbury Park listing.

## Worship sites

One: Our Lady of Mount Carmel Church (`our-lady-of-mount-carmel-asbury-park`). Holy Spirit Church, 705 2nd Ave, the parish's second site until 2021, closed (its closing Mass was on 6 June 2021) and is excluded (`holy-spirit-asbury-park`); GCatholic still lists it under Mother of Mercy. The bulletin's Mass schedule and its single 'Worship Site' line don't mention it.

## Website and bulletin provider

The finder, GCatholic and ParishesOnline all give momapnj.org, which is now a disconnected Wix domain (probe url and the browser both reach Wix's 'Reconnect Your Domain' 404 on 2026-10-30; the lead's 'refused' reading was this). The parish's Facebook page (facebook.com/motherofmercyap, 1.1K followers, last post July 2024) still points to it. The row therefore uses the ParishesOnline organization page as its website and reads the bulletin by org slug. The bulletin still prints 'Parish website: http://www.momapnj.org'.

## Not yet confirmed

Whether the parish has a working website; no second bulletin channel was found. The Monitor's 2023 appointment called Fr. Stephen Michael 'administrator' while the 2026 bulletin styles him 'Pastor'; it doesn't affect the row.
