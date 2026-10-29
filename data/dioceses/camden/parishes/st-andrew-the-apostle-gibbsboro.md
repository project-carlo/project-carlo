---
name: St. Andrew the Apostle Parish
website: https://www.churchofsaintandrews.org/bulletin
bulletin_provider: other
provider_id: page-pdfs https://www.churchofsaintandrews.org/bulletin
publication: ['url:https://www.churchofsaintandrews.org/bulletin#st-andrew-gibbsboro']
group: ''
evidence:
- url: https://irp.cdn-website.com/3adbeedb/files/uploaded/40284_2026_11_01.pdf
  seen: 2026-10-29
  note: 'Issue for Thirty-First Sunday in Ordinary Time, 1 November 2026 (posted ahead). The PDF''s text
    layer is garbled (a substituted font encoding), so page 1 was rendered with render.py and read: ''Welcome
    to the Church of St. Andrew the Apostle'', ''November 1, 2026'', Mass schedule Weekend Saturday Vigil
    4:00 PM, Sunday 8:00 AM, 10:00 AM & 6:00 PM, weekday Monday - Saturday 8:00 AM, ''All Souls'' Day
    Mass: Monday, November 2, 2026 at 7 PM'', 27 Kresson-Gibbsboro Road, Gibbsboro, NJ 08026, (856) 784-3878.
    Names this parish alone. recheck can''t find the words as text.'
- url: https://www.churchofsaintandrews.org/bulletin
  seen: 2026-10-29
  quote: Thirtieth Sunday of Ordinary Time (Ministry Guide) 10-25-2026
  note: The parish's Bulletin page lists the issues (11-1-2026, 10-25-2026 'Ministry Guide', 10-18-26,
    10-11-26, 10-04-26), each linking irp.cdn-website.com/3adbeedb/files/uploaded/40284_<date>.pdf. The
    10-25 issue's page 1 is the 2026-2027 Ministry Guide cover (rendered and read), with the same Mass
    schedule.
---

## Publisher

St. Andrew the Apostle publishes its own weekly bulletin on its Duda site's Bulletin page (https://www.churchofsaintandrews.org/bulletin, read 2026-10-29): a list of dated PDFs at `irp.cdn-website.com/3adbeedb/files/uploaded/40284_YYYY_MM_DD.pdf`, newest first by title, latest 1 November 2026. Page 1 of the 1 November issue (rendered and read; the text layer is garbled) is headed 'Welcome to the Church of St. Andrew the Apostle' with the Mass schedule and the Gibbsboro address. The page also names Rev. Msgr. Louis A. Marucci as pastor and Rev. Anthony Infanti as parochial vicar.

## Worship sites

One: 27 Kresson-Gibbsboro Road, Gibbsboro (church record `st-andrew-the-apostle-gibbsboro`). The bulletin names no other church. The parish site also lists Little Angels Academy (a preschool) and mentions Our Lady of Mt. Carmel School, which is St. Simon Stock's school: schools, not Mass sites.

## Website and bulletin provider

The directory (http://churchofsaintandrews.org/) and GCatholic (churchofstandrews.org) both resolve to https://www.churchofsaintandrews.org (200). `other` with a `page-pdfs` recipe on /bulletin. The PDFs have a garbled text layer, so the pipeline will probably need to read them as images. The 25 October issue is the Ministry Guide cover, not an ordinary issue; the newest file is the pick.

`fetch:check` (2026-10-29): the recipe picks `40284_2026_11_01.pdf` (transport ok, PDF, issue date and freshness unknown because the filename date format and the garbled text give the tool nothing to read; the date was read from the rendered page 1). That is the newest issue on the page, so the pick is right.

## Not yet confirmed

Nothing blocking. No shared bulletin with Berlin (St. Simon Stock publishes through Bon Venture, a different pastor).
