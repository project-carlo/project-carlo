---
name: St. Francis of Assisi Parish
website: https://discovermass.com/church/st-francis-of-assisi-clearfield-pa/
bulletin_provider: discover_mass
provider_id: st-francis-of-assisi-clearfield-pa
publication: ['discovermass:st-francis-of-assisi-clearfield-pa']
group: ''
evidence:
- url: https://discovermass.com/church/st-francis-of-assisi-clearfield-pa/
  seen: 2026-10-23
  quote: Fr. Robert Horgas, Pastor
  note: 'Current-bulletin download from the Discover Mass church page (cover image class ''bulletin-cover
    X-|2026-10-25|1792773797|3101'': bulletin number 3101, dated 25 October 2026; 8 pages). Page 1: ''October
    25, 2026 30th Sunday in Ordinary Time'', ''St. Francis of Assisi Church 212 South Front Street, Clearfield,
    PA 16830'', ''Fr. Robert Horgas, Pastor'', ''Weekend Mass Times Saturday Vigil 4:15pm Sunday 7:15am
    & 9:45am''. No hit for Timothy, Bonaventure, Curwensville or Grampian in the text layer.'
- url: https://www.eriercd.org/Parish20708-St-Francis-of-Assisi.html
  seen: 2026-10-23
  note: 'Diocese directory record 20708: no website field; 211 S. Second St. (mailing 212 S. Front St.),
    (814) 765-9671; Sat 4:15 p.m.; Sun 7:15, 9:45 a.m. The locator''s pastor field says Rev. Brandon M.
    Kleckner and the detail page says Rev. Robert Horgas; the bulletin and the clergy list agree with
    Horgas.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor .................................................................................... St.
    Francis of Assisi, Clearfield
  note: 'Clergy list updated 8/7/2026, Horgas, Rev. Robert: pastor, one assignment.'
- url: https://parishesonline.com/organization/st-francis-church-16830
  seen: 2026-10-23
  note: 'probe po st-francis-church-16830 (LPi 0018000000QxBkuAAF, 212 S Front St; website field http://www.stfrancisclearfield.com):
    ''no publications: this organization does not publish a bulletin here now''. probe url on stfrancisclearfield.com:
    DEAD-DNS. So the old domain is dead and the Discover Mass page is the channel.'
research:
- method: pnpm fetch:check --diocese erie --parish st-francis-of-assisi-clearfield --expected-identity
    Horgas (headed Chrome)
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, document type pdf, identity matched on the pastor's surname. Issue
    date and freshness read 'unknown' because the masthead date layout is not parsed; I confirmed by reading
    the downloaded PDF (25 October 2026, bulletin number 3101) and the cover class on the church page.
    Not a failure.
---

## Publisher

St. Francis of Assisi Parish, Clearfield (church 211 S. Second St., rectory 212 S. Front St., 16830) publishes its own weekly bulletin on Discover Mass (church page `st-francis-of-assisi-clearfield-pa`). The diocese directory gives it no website, and the ParishesOnline organization's website, stfrancisclearfield.com, no longer resolves, so the `website` field here is the Discover Mass church page. I downloaded the current issue on 2026-10-23: bulletin number 3101, dated 25 October 2026, 8 pages, masthead 'St. Francis of Assisi Church', pastor Fr. Robert Horgas (clergy list 8/7/2026 agrees). Content is this parish's alone.

## Worship sites

One church. Weekend Masses in the issue: Saturday vigil 4:15pm, Sunday 7:15am and 9:45am; weekday intentions Tuesday 12:10pm, Wednesday 9am, Thursday 10am, Friday 9am (27-30 October). The directory lists no mission or secondary church under it. Historically St. Timothy (Curwensville) and St. Bonaventure (Grampian) were its missions, but they have been separate parishes since 1904 and 1914 (merger decree of 2023); nothing in this bulletin ties them to it.

## Website and bulletin provider

`fetch` reads Discover Mass by `provider_id`. The download cap is per IP per day, so the page was read once.

## Not yet confirmed

Nothing affecting the row.
