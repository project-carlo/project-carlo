---
name: St. Aloysius (Ridgewood)
website: https://www.saloysius.org/bulletin.html
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery Q11 (Queens West)
evidence:
- url: https://www.saloysius.org/uploads/1/0/3/5/10351126/17_sunday_ota_2026.pdf
  seen: 2026-11-05
  note: 'The only bulletin the site posts: ''Seventeenth Sunday in Ordinary Time, July 26, 2026'', 8 pages;
    page 1 is an image (rendered with render.py) with the masthead ''St. Aloysius Parish / 382 Onderdonk
    Ave., Ridgewood, NY 11385-1399'', Rev. George Poltorak SAC, Pastor, and a Schedule of Masses for this
    church alone. recheck cannot find the image text.'
- url: https://www.saloysius.org/bulletin.html
  seen: 2026-11-05
  note: The Weebly bulletin page links one PDF, 17_sunday_ota_2026.pdf (26 July 2026); no later issue
    is posted as of 2026-11-05.
- url: https://www.saloysius.org/schedule.html
  seen: 2026-11-05
  quote: Saturday - 9.00am - English; 5.30pm - English (Sunday Vigil Mass) Sunday - 8.00am - English;
    9.30am - Polish; 11.00am - English; 12.30pm - Spanish; 7.00pm - Polish
  note: The parish site's schedule page; it agrees with the 26 July bulletin's schedule.
- url: https://parishesonline.com/organization/st-aloysius-church-11385
  seen: 2026-11-05
  note: 'probe po: org ''St. Aloysius Church'', 382 Onderdonk Ave, Ridgewood (lpi 0018000000QxB9mAAF)
    exists but lists no publications; not this parish''s bulletin channel now.'
revisit: Check whether saloysius.org/bulletin.html has resumed weekly posting (last issue 26 July 2026)
revisit_after: 2026-12-06
research:
- method: probe url and probe get of the parish's Weebly bulletin page; probe po of the ParishesOnline
    org st-aloysius-church-11385
  url: https://www.saloysius.org/bulletin.html
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reread https://www.saloysius.org/bulletin.html for an issue newer than 26 July 2026 and
    rerun fetch:check; if one is posted, record the page-pdfs recipe fetch:check prints
  retry_when: The bulletin page links an issue dated within the last two weeks, or the parish's ParishesOnline
    org starts listing issues
  revisit_after: 2026-12-06
bulletin_status: not-found
---

## Publisher

St. Aloysius produces its own bulletin and posts it on its Weebly site. The only issue on `https://www.saloysius.org/bulletin.html` (read 2026-11-05) is `17_sunday_ota_2026.pdf`, the Seventeenth Sunday in Ordinary Time, July 26, 2026. Its page 1 is an image; rendered, the masthead reads "St. Aloysius Parish / 382 Onderdonk Ave., Ridgewood, NY 11385-1399", Rev. George Poltorak SAC, Pastor. A ParishesOnline org for the parish (`st-aloysius-church-11385`, lpi 0018000000QxB9mAAF) exists but lists no issues, so it is not recorded as this bulletin's publication.

## Worship sites

One church. The 26 July bulletin's Schedule of Masses (Saturday 9:00 a.m. and 5:30 p.m. vigil; Sunday 8:00, 9:30 Polish, 11:00, 12:30 Spanish, 7:00 p.m. Polish; weekdays 9:00 a.m. and 7:00 p.m.) names only St. Aloysius, and the site's schedule page gives the same times. The diocese directory, deanery list, GCatholic 16673 and Mass finder 1181 list this one church. The Notre Dame Catholic Academy at 62-22 61st Street named on page 1 is a school, not a worship site.

## Website and bulletin provider

`no_bulletin` for now, with the bulletin page kept as `website`. The page carries one file at a time and has not been updated since the 26 July 2026 issue: `fetch:check` (2026-11-05) resolves `page-pdfs` on the page and picks `17_sunday_ota_2026.pdf` with freshness "unknown", so a promoted row would serve a three-month-old issue as this week's. Set the provider to `other` (recipe `page-pdfs https://www.saloysius.org/bulletin.html`) once the page links a current issue and `fetch:check` picks it. The front page is an image with no text layer.

## Not yet confirmed

Whether the parish still posts its bulletin weekly anywhere: no issue after 26 July 2026 was found on its site or ParishesOnline (see research). Revisit after 2026-12-06.
