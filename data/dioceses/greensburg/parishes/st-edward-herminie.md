---
name: St. Edward Parish, Herminie
website: https://www.saint-edward.org
bulletin_provider: other
provider_id: dated-post https://www.saint-edward.org/bulletin/read-our-weekly-bulletins/ filename=[0-9]*.pdf
publication: ['url:https://www.saint-edward.org/bulletin/read-our-weekly-bulletins/']
group: ''
evidence:
- url: https://www.saint-edward.org/wp-content/uploads/2026/10/1018189.pdf
  seen: 2026-10-22
  quote: 'St. Edward Catholic Church'
  note: 'Page 1 masthead of the 18 Oct 2026 issue (5 pages; linked from the post https://www.saint-edward.org/october-18-2026/):
    "St. Edward Catholic Church", "120 St. Edwards Lane, Herminie, PA 15637", "Rev. David J. Nazimek, Pastor";
    MASS SCHEDULE "Saturday Vigil 6:00 p.m.", "Sunday 9:00 a.m.", "Weekdays - Tues & Thurs 9:00 a.m.".
    Page 2 header "ST. EDWARD PARISH, A Pennsylvania Charitable Trust OCTOBER 18, 2026". Names St. Edward alone.'
- url: https://www.saint-edward.org/wp-content/uploads/2026/10/1018189.pdf
  seen: 2026-10-22
  quote: 'Mass at Seven Dolors ~ 9:00am'
  note: 'Page 2 intentions: Monday and Wednesday weekday Masses are at Seven Dolors, Yukon (the pastor''s other
    parish); St. Edward''s own Masses are Sat 6:00 pm, Sun 9:00 am, Tue and Thu 9:00 am.'
- url: https://www.saint-edward.org/bulletin/read-our-weekly-bulletins/
  seen: 2026-10-22
  note: 'Diocese-template WordPress page listing one post per issue: October 18, October 11, October 4, September 27 ...
    2026 (curl with a browser User-Agent; probe url reads it too). Each post embeds one dFlip PDF named MMDD189.pdf
    (1018189, 1011189, 1004189, 0927189, 0830189). The sidebar on every page also links Calendar.pdf and ministry schedules.'
- url: https://www.sevendolors.org/wp-content/uploads/2026/10/101826.pdf
  seen: 2026-10-22
  quote: 'Seven Dolors Catholic Church'
  note: 'The same pastor''s other parish, Seven Dolors, Yukon, publishes its own separate 18 Oct 2026 issue on its own
    site (row seven-dolors-yukon); its contact block lists "St. Edward Office: 724-446-5197" but the masthead and Mass
    schedule are Seven Dolors'' alone.'
- url: https://parishesonline.com/organization/st-edward-church-15637
  seen: 2026-10-22
  note: 'probe po: LPi org "St. Edward Church", 120 St Edwards Ln, Herminie (LPi 0018000000QxBzxAAF) has no
    publications and no container: not a live channel, not recorded as a publication.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=129
  seen: 2026-10-22
  note: 'Directory: St. Edward Parish, 120 Saint Edward Lane, Herminie; pastor Father David J. Nazimek (also pastor of
    Seven Dolors, LocationID 311); "Saturday: 6:00 p.m.; Sunday: 9:00 a.m."; no Partner Parishes listed.'
---

## Publisher

St. Edward Parish, Herminie publishes its own weekly bulletin and posts it on its diocese-template
WordPress site. The 18 October 2026 issue (read 2026-10-22, `1018189.pdf`) has the masthead "St. Edward
Catholic Church, 120 St. Edwards Lane, Herminie" with Fr. David J. Nazimek as pastor, and a Mass schedule
for St. Edward alone (Saturday Vigil 6:00 p.m., Sunday 9:00 a.m., Tuesday and Thursday 9:00 a.m.).

Fr. Nazimek is also pastor of Seven Dolors, Yukon, and the two share staff (the same secretary, deacon and
music director) and a weekday rota: St. Edward's intentions say "Mass at Seven Dolors ~ 9:00am" on Monday
and Wednesday. But Seven Dolors publishes its own issue, with its own masthead and schedule, on its own site
(sevendolors.org, `101826.pdf` for 18 October). Two live channels, so two rows (seven-dolors-yukon).

## Worship sites

One: St. Edward church, 120 St. Edward Lane, Herminie, the only St. Edward building in the bulletin's
schedule. The weekday Masses "at Seven Dolors" belong to the Seven Dolors row. GCatholic's St. Mary,
5 2nd St., Herminie (17291) is a Byzantine Catholic church (other jurisdiction), not part of this parish.

## Website and bulletin provider

`website` is the parish's own site. Provider `other` with the recipe `dated-post
https://www.saint-edward.org/bulletin/read-our-weekly-bulletins/ filename=[0-9]*.pdf`: the page lists one
post per issue and each post embeds the issue's PDF (named `MMDD189.pdf`). The filename filter is needed
because every page's sidebar also links `Calendar.pdf`: without it `fetch:check` (2026-10-22) picked
`wp-content/uploads/2023/03/Calendar.pdf`; with it, `1018189.pdf` (the 18 October issue). The LPi
organization `st-edward-church-15637` exists but is empty and is not recorded.

## Not yet confirmed

The issue PDFs follow a `MMDD189.pdf` pattern for now; if the parish changes how it names files so that
they no longer start with a digit, the filename filter will make the fetch fail loudly and needs updating.
