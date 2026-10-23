---
name: Catholic Community of Sharon (St. Joseph and St. Anthony of Padua)
website: https://www.sharoncatholic.org/weekly-bulletin
bulletin_provider: discover_mass
provider_id: st-joseph-sharon-pa
publication: ['discovermass:st-joseph-sharon-pa', 'discovermass:st-anthony-of-padua-sharon-pa']
group: 'Sharon: St. Joseph (31113) and St. Anthony of Padua (31110), one pastor, Rev. James Power'
evidence:
- url: https://discovermass.com/church/st-joseph-sharon-pa/
  seen: 2026-10-23
  quote: 79 Case Ave., Sharon, PA 16146
  note: 'Current-bulletin download from this Discover Mass church page (cover image class ''bulletin-cover
    X-|2026-10-25|1792785980|3537'': bulletin number 3537, dated 25 October 2026; 6 pages). Page 1 masthead:
    ''THE CATHOLIC COMMUNITY OF SHARON'', ''St Joseph Roman Catholic Church'', ''79 Case Ave. Sharon,
    PA 16146'', ''PASTOR Fr. James Power'', then two Mass-time boxes: ''ST. JOSEPH PARISH ... Saturday
    Vigil 5:15 pm; Sunday 11:00 am; Monday, Tuesday, Thursday, Friday 8:00 am; Wednesday 12:10 pm'' and
    ''ST. ANTHONY PARISH ... Sunday 8:30 am''. The footer says ''View this bulletin online at www.DiscoverMass.com''.'
- url: https://discovermass.com/church/st-anthony-of-padua-sharon-pa/
  seen: 2026-10-23
  quote: 804 Idaho St., Sharon, PA 16146
  note: 'The St. Anthony of Padua church page carries the same current issue: cover image class ''bulletin-cover
    X-|2026-10-25|1792785981|3537'', the same bulletin number 3537 as the St. Joseph page (timestamp differs
    by 1 second). Two slugs, one bulletin.'
- url: https://www.sharoncatholic.org/weekly-bulletin
  seen: 2026-10-23
  quote: Current Bulletin
  note: 'Wix page read in headed Chrome (visit.py): ''Catholic Community of Sharon'' header with ''St.
    Joseph and St. Anthony'' sub-nav and one ''Current Bulletin'' list (October 25, 18, 11 and 4, 2026)
    whose links are bulletins.discovermass.com download URLs; ''Archive Bulletins'' goes to /more-bulletins.
    Footer: ''St. Joseph Parish 79 Case Avenue ... Pastor: Fr. James Power''. Plain curl returns the Wix
    shell without the links.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: 1) St. Joseph; 2) St. Anthony, Sharon
  note: 'Clergy list updated 8/7/2026 (survey, diocese.md): Rev. James Power is pastor of St. Joseph and
    St. Anthony of Padua, Sharon. Diocese directory records 31113 and 31110 both give ''Pastor: Rev. James
    Power'' and the same phone, 724-981-3232; St. Anthony''s mailing address is ''c/o St. Joseph Parish
    79 Case Ave.''.'
research:
- method: grep of the 25 Oct 2026 bulletin text layer (pdftotext, 6 pages) for Fatima, Farrell, Good Shepherd,
    Middlesex, Whitman, Adalbert
  url: https://discovermass.com/church/st-joseph-sharon-pa/
  checked: '2026-10-23'
  outcome: not-found
  next_action: 'None needed: the issue carries only St. Joseph and St. Anthony Mass times, so Our Lady
    of Fatima, Farrell is not covered by it (see st-... fatima row).'
  retry_when: A later issue prints Fatima's Saturday 4:00 pm Mass in the masthead or Mass box
- method: pnpm fetch:check --diocese erie --parish st-joseph-st-anthony-sharon --expected-identity Sharon
    (headed Chrome); second run, the first hit Discover Mass's per-IP download cap (not_pdf) after the
    manual download
  url: https://discovermass.com/church/st-joseph-sharon-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: 'None: transport ok, document a 1,884,050-byte PDF (same size as the manual download),
    identity matched (''the catholic community of sharon 30th sunday in ordinary time sunday october 25
    2026''); issue date reported unknown because the masthead date is split by the layout, which is expected
    here.'
---

## Publisher

St. Joseph and St. Anthony of Padua, Sharon, are one bulletin. The Discover Mass pages for both churches (`st-joseph-sharon-pa`, `st-anthony-of-padua-sharon-pa`) serve the same issue, bulletin number 3537, dated Sunday 25 October 2026 (read 2026-10-23). Its page 1 masthead reads 'THE CATHOLIC COMMUNITY OF SHARON / St Joseph Roman Catholic Church / 79 Case Ave.' with 'PASTOR Fr. James Power' and a Mass-times box for each church. The parish website, sharoncatholic.org (Wix), has one 'Bulletin' page for both churches and its issue links are Discover Mass downloads.

The diocese's clergy list names Rev. James Power pastor of both parishes. The two canonical parishes are St. Joseph (directory 31113, gcatholic 24520) and St. Anthony of Padua (directory 31110, gcatholic 24481); St. Anthony's directory mailing address is 'c/o St. Joseph Parish'. There is no separate St. Anthony bulletin: the one page and one issue serve both, so this is one row.

## Worship sites

Two churches with Mass in the 25 October 2026 bulletin: St. Joseph (79 Case Ave.: Saturday 5:15 pm, Sunday 11:00 am, weekdays) and St. Anthony of Padua (804 Idaho St.: Sunday 8:30 am). Left out, each with its own record: Sacred Heart, Sharon (relegated 2018-03-25), St. Stanislaus Kostka-Holy Trinity, Sharon (relegated 2019-06-09) and St. Adalbert, Farrell (relegated 2020-09-20), all former parishes merged into St. Joseph or St. Anthony in 2017 and closed by decree.

**Our Lady of Fatima, Farrell is not on this bulletin.** The web city list says Fatima is 'partnered with St. Anthony of Padua Parish, Sharon', but the clergy list names Rev. Glenn Whitman, not Fr. Power, as Fatima's pastor, and Fatima posts its own bulletin (see its row). A grep of this issue for Fatima, Farrell, Good Shepherd, Middlesex and Whitman found nothing.

## Website and bulletin provider

Provider `discover_mass`, church slug `st-joseph-sharon-pa`; the issue is mirrored under the St. Anthony slug (both recorded in `publication`). Website is the parish's Bulletin page because the Wix home page does not link the issues in static HTML. Discover Mass downloads are capped per IP per day; see diocese.md.

## Not yet confirmed

Whether weekday Masses continue as printed: the intentions column prints 'No Daily Mass' under each weekday that week (probably 'no intention listed'), while the Mass-time box lists 8:00 am and 12:10 pm; the schedule box is followed here.
