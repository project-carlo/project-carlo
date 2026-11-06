---
name: St. Joan of Arc (Jackson Heights)
website: https://sjaparish.com/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery Q3 (Queens West)
evidence:
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMDkvMTYvNTUxOW80cTZyd18wM180MDU4XzM4X1NFUFRFTUJFUl8xMy5wZGYiXV0/03-4058%20-%2038%20SEPTEMBER%2013.pdf
  seen: 2026-11-05
  note: Newest bulletin the site posts, '24th Sunday in Ordinary Time ... September 13, 2026', 6 pages,
    all images (rendered page 1 with render.py). Masthead 'ST. JOAN OF ARC CATHOLIC CHURCH / 8200 35th
    Avenue Jackson Heights, NY 11372', Pastor Rev. Christopher R. Heanue, and a Mass Schedule for this
    church alone. The file name '03-4058 - 38' looks like a J.S. Paluch job number. recheck cannot find
    the image text.
- url: https://sjaparish.com/bulletins
  seen: 2026-11-05
  note: 'Tilma bulletins page: the collection lists 10 items, newest ''Sept. 13, 2026''; all the files
    were uploaded 2026/09/16 (path in the resource token). No issue after 13 September is posted as of
    2026-11-05.'
- url: https://joanofarcqueens.org/
  seen: 2026-11-05
  note: 'The directory''s homepage for the parish redirects to https://sjaparish.com/, titled ''St. Joan
    of Arc Parish — Jackson Heights, Queens, NY'', with the parish''s address and phone: the parish''s
    own new domain, not a squat or a fold-in.'
- url: https://discovermass.com/church/st-joan-of-arc-jackson-heights-ny/
  seen: 2026-11-05
  note: 'issues.py discovermass: the Discover Mass church page exists but lists no bulletins.'
revisit: Check whether sjaparish.com/bulletins has resumed posting (newest issue 13 September 2026)
revisit_after: 2026-12-06
research:
- method: probe url of joanofarcqueens.org (redirects to sjaparish.com); probe get of the Tilma bulletins
    page; issues.py discovermass st-joan-of-arc-jackson-heights-ny
  url: https://sjaparish.com/bulletins
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reread https://sjaparish.com/bulletins and the Discover Mass church page for an issue newer
    than 13 September 2026; if one is posted, set provider other (page-pdfs https://sjaparish.com/bulletins)
    or discover_mass and rerun fetch:check
  retry_when: The bulletins page or Discover Mass lists an issue dated within the last two weeks
  revisit_after: 2026-12-06
bulletin_status: not-found
---

## Publisher

St. Joan of Arc produces its own bulletin (the file names, `03-4058 - <week> <DATE>.pdf`, look like a J.S. Paluch job number) and posts it on its Tilma site. The directory's homepage, `joanofarcqueens.org`, redirects to the parish's new domain `sjaparish.com` (read 2026-11-05). The newest issue on `https://sjaparish.com/bulletins` is the 24th Sunday in Ordinary Time, September 13, 2026; its page 1 is an image whose masthead reads "ST. JOAN OF ARC CATHOLIC CHURCH / 8200 35th Avenue Jackson Heights, NY 11372", Rev. Christopher R. Heanue, Pastor. The Discover Mass church page `st-joan-of-arc-jackson-heights-ny` exists but lists no issues.

## Worship sites

One church. The 13 September Mass Schedule (Saturday 12:00 noon, 6:00pm English, 7:30pm Spanish; Sunday 8:00, 10:00, 12:00, 6:00pm English and 9:30, 11:30, 1:30 Spanish, with a Filipino Mass at 1:30pm "LC" on the third Sunday) names no other place; "LC" is read as the lower church of the same building (the site's Mass Times page puts confessions "in the lower church"). The site's Mass Times page (2026-11-05) gives the same weekend schedule. The diocese directory, deanery list, GCatholic 16722 and Mass finder 1144 list this one church.

## Website and bulletin provider

`no_bulletin` for now, with the Tilma bulletins page kept as `website`. The page's newest issue is 13 September 2026 (all ten listed files were uploaded on 16 September), so a `page-pdfs https://sjaparish.com/bulletins` recipe would pick a seven-week-old issue as this week's. The issues are image-only PDFs. Set the provider to `other` with that recipe (or `discover_mass` if issues appear there) once a current issue is posted and `fetch:check` picks it.

## Not yet confirmed

Whether the parish still publishes weekly anywhere: no issue after 13 September 2026 was found on its site or on Discover Mass (see research). Revisit after 2026-12-06.
