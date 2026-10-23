---
name: Beloved Disciple Parish
website: https://www.beloveddiscipleparish.org/bulletins
bulletin_provider: parishes_online
provider_id: beloved-disciple-parish
publication: ['po-org:beloved-disciple-parish', 'lpi:0018000000QxBjkAAF', 'po-container:14/1463']
group: Merged with St. Michael the Archangel, Emlenton (decree 2023); Grove City and Emlenton share one
  bulletin
evidence:
- url: https://container.parishesonline.com/bulletins/14/1463/20261025B.pdf
  seen: 2026-10-23
  quote: Very Rev. V. David Foradori, E.V., Pastor, ext. 111
  note: 'Page 1 of the 25 Oct 2026 issue (8 pages), left column of the masthead. The right column, ''Liturgical
    Schedule'', reads: ''Weekend Masses  Beloved Disciple, Grove City PA  4:30pm Saturday Evening  11:00am
    Sunday Morning  St. Michael, Emlenton PA  9:00am Sunday Morning  Daily Masses: Beloved Disciple  Monday,
    Tuesday, Wednesday, Friday - 8:00am  Thursday - 6:00pm''. Page 7 footer: ''Church of the Beloved Disciple,
    Grove City, PA 14-1463''. The bulletin covers both churches; the 13 Sept, 27 Sept, 4, 11 and 18 Oct
    2026 issues I downloaded print the same ''St. Michael, Emlenton PA / 9:00am Sunday Morning'' line.'
- url: https://www.beloveddiscipleparish.org/bulletins
  seen: 2026-10-23
  quote: St. Michael the Archangel 807 Chestnut Street, PO Box 117, Emlenton, PA 16373 724-867-2422
  note: 'Parish site (WeConnect/LPi). Footer lists both churches. The Bulletins page embeds two ParishesOnline
    widgets: id 0018000000QxBjkAAF (Beloved Disciple Parish, latest issue 25 Oct 2026, container 14/1463)
    and id 0018000000QxBkCAAV (St. Michael the Archangel, container 14/1658, latest issue 31 May 2026,
    i.e. stopped). The nav has ''St. Michael''s Bulletins'' and ''About St. Michael the Archangel'' pages.'
- url: https://container.parishesonline.com/bulletins/14/1658/20260531B.pdf
  seen: 2026-10-23
  quote: Beloved Disciple –Grove City
  note: 'Last St. Michael container issue, 31 May 2026, page 1: ''SUNDAY MASS Sunday.......9:00 am'',
    ''Beloved Disciple -Grove City Saturday 4:30 pm, Sunday 11:00am'', ''Website: BelovedDiscipleparish.org''.
    Container 14/1658 has no issue after that date (probe po, 2026-10-23); the parish''s bulletin since
    is 14/1463 alone. It is a stopped channel, not a second live bulletin.'
- url: https://www.eriercd.org/Parish31101-Beloved-Disciple.html
  seen: 2026-10-23
  note: 'Directory record 31101: 1310 S. Center St. Ext., Grove City PA 16127; clergy ''Pastor: Very Rev.
    V. David Foradori, EV; Permanent Deacon: Deacon Owen Wagner''; Saturday 4:30 p.m., Sunday 11 a.m.,
    Monday, Tuesday, Wednesday, Friday 8 a.m., Thursday 6 p.m. (the locator''s pastor field names Kujawinski,
    the detail page Foradori; the bulletin agrees with the detail page). Mission record 30909 (St. Michael
    the Archangel, Emlenton) is ''secondary mission church'' under it.'
research:
- method: pnpm fetch:check --diocese erie --parish beloved-disciple-grove-city --expected-identity Beloved
    --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://parishesonline.com/publication-page/beloved-disciple-parish
  checked: '2026-10-23'
  outcome: found
  next_action: 'None for the pick: transport ok, PDF (7,167,839 bytes), identity matched in first-page
    text, and it resolved the 25 Oct 2026 file (container 14/1463/20261025B.pdf). The check reported ''conflicting
    dates'' (overall unverified) only because the bulletin''s own page 1 prints ''October 25, 2006'' (a
    typo for 2026, thrice in the page-1 text layer) while the file name and the liturgical day, ''October
    25, 2026 Thirtieth Sunday in Ordinary Time'' on page 2, say 2026. Not a staleness signal; re-run on
    a later week to confirm the pick follows the newest issue.'
---

## Publisher

Beloved Disciple, Grove City publishes its weekly bulletin through ParishesOnline (org `beloved-disciple-parish`, LPi id 0018000000QxBjkAAF, container 14/1463; latest issue 25 October 2026, read 2026-10-23). Its masthead block names Very Rev. V. David Foradori, E.V., as pastor and prints one 'Liturgical Schedule' for two churches: Beloved Disciple, Grove City and St. Michael, Emlenton (Sunday 9:00am). Weekday Masses are Beloved Disciple's.

**St. Michael, Emlenton is not a second row.** The decree 'Merging St. Michael the Archangel into Beloved Disciple Parish' (2023; diocese decrees page) merged the parishes, and St. Michael's old ParishesOnline org (`st-michael-the-archangel-parish-16373`, LPi 0018000000QxBkCAAV, container 14/1658) still exists but its last issue is 31 May 2026, whose own page 1 lists the Grove City Masses and Beloved Disciple's website. Since then only 14/1463 is live, and it covers Emlenton. St. Michael's own site, stmichaelrcchurch.org, still lists 'Saturday Vigil Mass, Grove City 4:30PM; Sunday Mass, Emlenton, 9:00am, Grove City, 11:00am' and links 'Click HERE for Beloved Disciple'. I did not read the 2023-2026 St. Michael issues, so I do not know when its separate bulletin began carrying the joint schedule or whether it was distinct before 31 May 2026; the stopped container is recorded as evidence and not as a `publication` id.

## Worship sites

- Beloved Disciple, 1310 S. Center St. Ext., Grove City: Saturday 4:30pm, Sunday 11:00am, weekdays as above.
- St. Michael the Archangel, 807 Chestnut St., Emlenton: Sunday 9:00am (the diocese's 'secondary mission church').

No campus Mass: in the 25 Oct 2026 issue (grepped for 'College' and 'Campus') the only 'Campus' is the faith-formation 'Grove City Campus' and 'College' does not appear. Grove City College is not a roster entry here.

## Website and bulletin provider

`parishes_online` with the org slug; the parish site embeds the widget on /bulletins. `probe po beloved-disciple-parish` returned the 25 Oct 2026 issue.

## Not yet confirmed

St. Michael's Emlenton Sunday Mass has no intention line in the 25 Oct Mass Intentions page (only the Grove City Masses); its existence rests on the Liturgical Schedule in the six issues read (13 Sept, 27 Sept, 4, 11, 18, 25 Oct), the diocese directory ('Sunday: in-person and online 9 a.m.') and St. Michael's own site.
