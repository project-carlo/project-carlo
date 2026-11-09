---
name: Holy Trinity
revisit: Grep the St. Vito-Most Holy Trinity eCatholic issues (files.ecatholic.com/6764/bulletins/) for
  a Mass at Holy Trinity or 320 East Boston Post Road, especially the Christmas 2026 and Trinity Sunday
  (23 May 2027) issues. A dated public Mass there makes it a church under that parish; an explicit closure
  or relegation source makes it an exclusion.
revisit_after: 2027-05-24
roster: ['gcatholic:16520']
evidence:
- url: https://gcatholic.org/churches/usa-02/16520
  seen: 2026-10-07
  quote: "Church of the Most Holy Trinity, Mamaroneck, New York, USA Church of the Most Holy Trinity\n\
    Mamaroneck, New York , USA\nℹ️ Info \U0001F4CD Nearby\nJurisdiction: Metropolitan Archdiocese of New\
    \ York\nMission of: Church of St. Vito , Mamaroneck\nType: Church\nRite: Roman (Latin)\nHistory: parish\
    \ merged with St. Vito "
  note: 'Research snapshot: HTTP 200. A failed access attempt or missing listing is not evidence of closure
    or no bulletin.'
- url: https://stvitomhtchurch.com/bulletins
  seen: 2026-10-07
  quote: Just a moment...
  note: 'Research snapshot: HTTP 403. A failed access attempt or missing listing is not evidence of closure
    or no bulletin.'
- url: https://files.ecatholic.com/6764/bulletins/20261004.pdf
  seen: 2026-10-07
  quote: "Parish Staff \n•WELCOME/ BIENVENIDO \nTo register in the parish, please come to the office.\
    \ \nPara registrarse en la parroquia, por favor acérquese a\nla oficina. \nSponsor Certificates are\
    \ ONLY given to qualified\nregistered parishioners. *Priest approval needed. \nPastor: REV. JOSEPH\
    \ P. TIERNEY \nParochia"
  note: Saved issue is a research lead, not a settled current building/publication decision; inspect its
    masthead and building-labelled Mass schedule.
- url: https://files.ecatholic.com/6764/bulletins/20261011.pdf
  seen: 2026-10-10
  quote: Saint Vito - Most Holy Trinity
  note: Complete October 11, 2026 issue downloaded and read October 10. Combined masthead and ordinary
    Mass schedule do not identify a liturgy at 320 East Boston Post Road.
- url: https://files.ecatholic.com/6764/bulletins/20260531.pdf
  seen: 2026-10-10
  note: May 31, 2026 Trinity Sunday issue downloaded October 10; first three pages rendered and pages
    2-3 visually inspected. Page 2 Trinity Sunday reflection is not a building-labelled Holy Trinity Mass
    notice; page 3 Festa is expressly at 816 Underhill Avenue.
- url: https://stvitomhtchurch.com/mass-times
  seen: 2026-10-10
  note: Official current weekly schedule fetched October 10; services are generically labelled Church,
    not 320 East Boston Post Road. Parish office number is 914-698-2648 on the May 31 Festa/registration
    notice.
- url: https://files.ecatholic.com/6764/bulletins/20261108.pdf
  seen: 2026-11-08
  quote: ST. VITO - MOST HOLY TRINITY CHURCH NOVEMBER 8, 2026
  note: Current issue, 6 pages. Mass schedule (Mon-Fri 8:00 AM, Tue/Thu 8:00 PM Spanish, Saturday 9:00
    AM and 4:00 PM Vigil, Sunday 8:00, 9:00, 11:30 AM Spanish) with the rectory at 826 Underhill Ave;
    'Boston Post Road' appears only in two advertisers' addresses. No Mass at Holy Trinity.
- url: https://stvitomhtchurch.com/mass-times
  seen: 2026-11-08
  note: Every Mass is labelled '(Church)'; no mention of Holy Trinity or 320 East Boston Post Road.
- url: https://www.foxnews.com/faith-values/new-york-catholic-church-vatican-save-mamaroneck
  seen: 2026-11-08
  quote: Dolan last month rescinded his decree shuttering the house of worship
  note: 'Published 13 August 2020 (from the New York Post): the 2018 decree closing Holy Trinity Church
    was rescinded in July 2020 after a Vatican appeal. So the building is not canonically closed; the
    article gives no Mass schedule.'
- url: https://en.wikipedia.org/wiki/Most_Holy_Trinity_Church,_Mamaroneck
  seen: 2026-11-08
  quote: Special-occasion use
  note: Infobox functional status; the text says that since the August 2015 merger there have been 'no
    regularly scheduled masses' at Most Holy Trinity Church. Undated and unsourced for current use.
parish: st-vito-and-most-holy-trinity-mamaroneck
line1: 320 East Boston Post Rd.
city: Mamaroneck
state: NY
postal_code: '10543'
research:
- method: issues.py ecatholic ecatholic:6764 --grep 'Boston Post' --grep 'Holy Trinity Church' --grep
    320 (8 November 2026 issue)
  url: https://files.ecatholic.com/6764/bulletins/20261108.pdf
  checked: '2026-11-08'
  outcome: not-found
  next_action: Grep the Christmas 2026 and Trinity Sunday 2027 issues the same way
  retry_when: The 20261220-20261227 or 20270523 issue is posted
  revisit_after: 2027-05-24
- method: web search and news (Fox News/New York Post 2020, Wikipedia) for the building's status
  url: https://www.foxnews.com/faith-values/new-york-catholic-church-vatican-save-mamaroneck
  checked: '2026-11-08'
  outcome: not-found
  next_action: Look for a dated special-occasion Mass notice (parish site, bulletin, Knights of Columbus
    Council 2247)
  retry_when: A news item or parish notice about Holy Trinity Church appears
---

## What is known

Most Holy Trinity Church, 320 East Boston Post Road, Mamaroneck, belongs to the parish of [St. Vito-Most Holy Trinity](../parishes/st-vito-and-most-holy-trinity-mamaroneck.md), whose eCatholic bulletin is read weekly. Since the August 2015 merger the parish's regular Masses are at St. Vito, 816-826 Underhill Avenue. The 2018 decree closing Holy Trinity was rescinded in July 2020 after a Vatican appeal (New York Post via Fox News, 13 August 2020), so the building is not canonically closed. Wikipedia describes it as in "special-occasion use" with no regularly scheduled Masses, without a date or source.

Checked on 8 November 2026: the 8 November bulletin's Mass schedule and text name no Mass at Holy Trinity or 320 East Boston Post Road (the only Boston Post Road addresses are advertisers'), and the parish's Mass-times page labels every Mass "(Church)". On October 10 the 31 May 2026 Trinity Sunday issue was read: its Festa was at Underhill Avenue, and it announced no Mass at Holy Trinity.

## Why it is not decided

No source dates a public Mass at Holy Trinity now, and none says it is closed (the closure was rescinded). Occasional Masses (a feast day, a funeral) would not show in the regular schedule. The next check is the parish's own bulletins around Christmas 2026 and Trinity Sunday 2027 (23 May), when a special-occasion Mass there would be announced.
