---
name: Immaculate Conception Parish (Catholic Churches of Jim Thorpe)
website: https://www.catholicchurchesofjimthorpe.org/Resources/Sunday-Bulletin
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://www.catholicchurchesofjimthorpe.org/Resources/Sunday-Bulletin']
group: ''
evidence:
- url: https://www.catholicchurchesofjimthorpe.org/LinkClick.aspx?fileticket=q5bOa0_NCc8%3d&tabid=8565&portalid=114&mid=16625
  seen: 2026-10-18
  quote: Catholic Churches of Jim Thorpe 11 October 2026 Twenty-Eighth Sunday in Ordinary Time
  note: Page 1 of the 11 October 2026 issue (6 pages, text PDF), the newest posted on 18 October. The
    masthead names "Immaculate Conception Parish 180 W. Broadway, Jim Thorpe" and "Saint Joseph Church
    526 North Street, Jim Thorpe", one office, "Rev. Ronald J. Minner, Pastor".
- url: https://www.catholicchurchesofjimthorpe.org/LinkClick.aspx?fileticket=q5bOa0_NCc8%3d&tabid=8565&portalid=114&mid=16625
  seen: 2026-10-18
  quote: Saturday, October 17 - Vigil … 4:00 pm (SJC) … Sunday, October 18 … 8:30 am (SJC) … 10:45 am
    (ICC)
  note: Page 2, the week's Mass intentions, each marked SJC (St. Joseph Church) or ICC (Immaculate Conception
    Church); weekday Masses alternate between the two. A box on the page reads "Note - Location change
    4:00 pm Mass at Saint Joseph".
- url: https://www.catholicchurchesofjimthorpe.org/Resources/Sunday-Bulletin
  seen: 2026-10-18
  quote: Sunday Bulletins Title October 11, 2026 Download October 4, 2026 Download September 27, 2026
    Download
  note: The site's bulletin page (DotNetNuke Documents module); each title links a /LinkClick.aspx?fileticket=…
    URL that serves the PDF.
- url: https://www.catholicchurchesofjimthorpe.org/Pray-With-Us/Masses
  seen: 2026-10-18
  quote: 'Saturday Vigil: 4:00 PM Immaculate Conception Church Sunday: 8:30 AM Saint Joseph Church 10:45
    AM Immaculate Conception Church'
  note: The site's standing schedule still puts the Saturday vigil at Immaculate Conception; the October
    bulletins move it to St. Joseph.
- url: https://www.tnonline.com/20200622/jim-thorpe-parishes-consolidate/
  seen: 2026-10-18
  quote: On Sunday, the diocese announced that St. Joseph Parish is consolidated into Immaculate Conception
    parish.
  note: Times News, 22 June 2020 (date in the URL), which adds that "Both church buildings will remain
    open and will use the existing Mass schedule".
promoted: 2026-10-19
---

## Publisher

Immaculate Conception Parish, Jim Thorpe, publishes one weekly bulletin as "Catholic Churches
of Jim Thorpe" on its own site. I read the 11 October 2026 issue (the newest posted on 18
October): the page-1 masthead names Immaculate Conception Parish (180 W. Broadway) and
Saint Joseph Church (526 North Street) with one pastor, Rev. Ronald J. Minner, and page 2
lists the week's Masses marked SJC or ICC. St. Joseph Parish was consolidated into
Immaculate Conception in June 2020 with both buildings kept open (Times News, 22 June 2020),
and the old iccjimthorpe.org domain now redirects to the joint site. One row, two churches.

## Worship sites

- `immaculate-conception-jim-thorpe` (178 W. Broadway): Sunday 10:45 am; weekdays Monday and
  Thursday 8 am (the Saturday 4 pm vigil, normally here, is at St. Joseph in October 2026).
- `st-joseph-jim-thorpe` (526 North Street): Saturday 4 pm (for now), Sunday 8:30 am,
  Tuesday and Friday 8 am, Wednesday 6 pm on alternate weeks.

The diocesan map lists the same two, St. Joseph as "Worship Site for Immaculate Conception
Parish"; GCatholic lists both. Nothing ruled out.

## Website and bulletin provider

The site (DotNetNuke, "Connecting Members") lists the last four issues on
/Resources/Sunday-Bulletin, each as a `LinkClick.aspx?fileticket=` link with the Sunday's
date as its title. The fileticket token is not a date, so the resolver has to date issues
by the link text. Recorded as `other` with the bulletin page as website and publication. The
directory's second website value "https://catholicchurchesofjimthorpe" (on St. Joseph's
page) is a typo for the same site. probe url also found a "DMI Parish Template for the
Diocese of Allentown.pdf" link on the home page, which is a diocesan form, not the bulletin.

Fetch check (2026-10-18): resolved; recipe `page-pdfs` on the bulletin page picked the 11 October issue's LinkClick URL ("current": the 18 October issue was not posted yet). Recorded as provider_id.

## Not yet confirmed

Whether the Saturday vigil returns to Immaculate Conception after October (the 11 October
bulletin's note gives no end date). Doesn't affect the rows.
