---
name: Our Lady of Fatima Parish
website: https://fatimafarrell.org
bulletin_provider: other
provider_id: page-pdfs https://fatimafarrell.org/weeklybulletin.php
publication: ['url:https://fatimafarrell.org/weeklybulletin.php#our-lady-of-fatima-farrell']
group: Pastor Rev. Glenn Whitman also serves Good Shepherd, West Middlesex (clergy list, 8/7/2026); the
  web city list's 'partnered with St. Anthony of Padua Parish, Sharon' is not borne out
evidence:
- url: https://fatimafarrell.org/images/weeklybulletin/5a3b66993337424d1d415f427d08c6d1.pdf
  seen: 2026-10-23
  quote: Our Lady of Fatima Parish
  note: 'Issue titled ''October 24, 2026'' on the parish''s weeklybulletin.php (4 pages, text layer).
    Page 1: ''Our Lady of Fatima Parish / 601 Roemer Blvd. / Farrell, Pa. 16121 / Mass time Saturday 4:00
    PM'', ''Pastor: Fr. Glenn Whitman'', ''Weekend Assistance: Fr. Frank DiCristina''. Page 2 footer:
    ''OUR LADY OF FATIMA PARISH, FARRELL, PA "THIRTIETH SUNDAY IN ORDINARY TIME, OCT 24, 2026''; intentions
    for ''SATURDAY OCT 24 4:00PM MASS'' and ''Saturday Oct 31 at 4:00pm MASS ALL SAINTS MASS''; Monday
    to Friday ''Prayer Service'' at 6:30 am. The only Mass printed is Saturday 4:00 pm.'
- url: https://fatimafarrell.org/weeklybulletin.php
  seen: 2026-10-23
  quote: October 24, 2026
  note: Diocese-hosted template page (footer 'Diocese of Erie'); 12 dated issues from August 1 to October
    24, 2026, newest-first-ish (October 10, 24, 17, 3, ...). tools/weeklybulletin_issues.sh lists them.
    The October 24 issue is the one dated for the coming weekend.
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Our Lady of Fatima
  note: 'Clergy list updated 8/7/2026 (read for the survey, diocese.md): Whitman, Rev. Glenn: pastor of
    Good Shepherd, West Middlesex and Our Lady of Fatima, Farrell. Rev. James Power''s assignments are
    St. Joseph and St. Anthony, Sharon only.'
- url: https://www.eriercd.org/Parish31116-Our-Lady-of-Fatima.html
  seen: 2026-10-23
  quote: Our Lady of Fatima
  note: 'Directory record 31116: 601 Roemer Blvd., Farrell; clergy ''Pastor: Rev. Glenn Whitman''; Saturday
    4:00 p.m., prayer service Monday to Friday 6:30 a.m. Its locator pastor field says ''Rev. Matthew
    J. Ruyechan'' and its city-list note says ''partnered with St. Anthony of Padua Parish, Sharon'' while
    its locator GroupID is Good Shepherd (31102): the directory disagrees with itself.'
research:
- method: pnpm fetch:check --diocese erie --parish our-lady-of-fatima-farrell --expected-identity Fatima
    (headed Chrome)
  url: https://fatimafarrell.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None: it picked the October 24, 2026 issue (the newest), a 7,111,067-byte PDF; identity
    matched on page 1 (''our lady of fatima parish 601 roemer blvd farrell pa 16121 mass time saturday
    4''); issue date reported unknown (not parsed from the masthead), as for other diocese-hosted sites.
    provider_id pins the page-pdfs recipe; no separate recipe line was printed.'
publication_reviews:
- parish: st-joseph-st-anthony-sharon
  decision: separate
  evidence:
  - url: https://fatimafarrell.org/images/weeklybulletin/5a3b66993337424d1d415f427d08c6d1.pdf
    seen: 2026-10-23
    quote: Our Lady of Fatima Parish
    note: Fatima's 24 Oct 2026 issue is its own four-page bulletin (Fatima pastor, ministry schedule,
      Saturday 4:00 pm Mass) with no Sharon Mass times.
  - url: https://discovermass.com/church/st-joseph-sharon-pa/
    seen: 2026-10-23
    quote: 79 Case Ave., Sharon, PA 16146
    note: 'The Catholic Community of Sharon issue 3537 (25 Oct 2026) was grepped for Fatima, Farrell,
      Whitman: no hit.'
- parish: good-shepherd-west-middlesex
  decision: separate
  evidence:
  - url: https://www.goodshepherdwm.org/bulletins
    seen: 2026-10-23
    note: Good Shepherd's 25 Oct 2026 issue (Wix, image-only pages) is headed 'Church of the Good Shepherd'
      with its own Mass intention table (Saturday 6:00 pm, Sunday 9:00 and 11:30 am) and no Fatima Mass;
      Fatima's issue is a separate file on a separate site. Fatima's calendar mentions 'Making Fatima
      Cavatelli In the Good Shepherd Social Hall', a shared venue, not a shared bulletin.
---

## Publisher

Our Lady of Fatima, Farrell publishes its own weekly bulletin on its diocese-hosted site, fatimafarrell.org (`weeklybulletin.php`, one hash-named PDF per issue with the date in the link title). The 24 October 2026 issue (read 2026-10-23) is a four-page bulletin headed 'Our Lady of Fatima Parish, 601 Roemer Blvd., Farrell, Pa. 16121, Mass time Saturday 4:00 PM', pastor 'Fr. Glenn Whitman'.

**The pastor conflict, settled by the bulletins.** The task started from two sources that disagree: the clergy list (8/7/2026) names Rev. Glenn Whitman pastor of Good Shepherd (West Middlesex) and Our Lady of Fatima, while the directory's web city list says Fatima is 'partnered with St. Anthony of Padua Parish, Sharon' (whose pastor is Rev. James Power). I read the three current bulletins: Fatima's own issue names Fr. Whitman as pastor; the Sharon issue (Discover Mass 3537, 25 Oct 2026) names Fr. Power and carries only St. Joseph and St. Anthony Mass times (no hit for Fatima, Farrell or Whitman); Good Shepherd's issue names Fr. Whitman as pastor. Fatima therefore shares a pastor with Good Shepherd, not with Sharon, and its bulletin is distinct from both. The partnership decree was not read; the city-list note may be stale (Fatima partnered with Sharon's parishes earlier, as St. Adalbert, Farrell was merged into St. Anthony in 2017). Two peer reviews record the separation.

## Worship sites

One church: Fatima's own church at 601 Roemer Blvd. (Saturday 4:00 pm). GCatholic names it 'Our Lady of Fatima-St. Ann' (history 2008): the 2008 combination of two Farrell parishes. Discover Mass also has a separate page `st-ann-farrell-pa` at '601 Fruit Ave., Farrell' with no Mass times and no bulletin; no roster lists it, the Fatima bulletin does not mention St. Ann, and I did not confirm that a St. Ann building exists or holds Mass. Not created as a church or open record (it is outside this batch's rosters and found only on a Discover Mass listing); see *Not yet confirmed*. St. Adalbert, Farrell (the other Farrell church in this batch) closed by decree in 2020; see its record.

## Website and bulletin provider

Provider `other` with `page-pdfs https://fatimafarrell.org/weeklybulletin.php`, as for the other diocese-hosted sites here. The Discover Mass page `our-lady-of-fatima-farrell-pa` says 'no bulletins available': it is not a channel.

## Not yet confirmed

- Whether 'St. Ann' (Discover Mass `st-ann-farrell-pa`, 601 Fruit Ave.) is a distinct open building. Next step: search Farrell obituaries or the diocese decrees for St. Ann; retry if Fatima's bulletin starts listing a second building.
- The partnering decree for Fatima was not read; the bulletins settle which bulletin covers it.
