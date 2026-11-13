---
name: St. Gabriel (East Elmhurst)
website: https://www.saint-gabriel-queens.org/announcements
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery Q3 (Queens West)
evidence:
- url: https://assets.ctfassets.net/1b3qqbmj8u0q/59IXlZrmxSbfzCr9r3q9PD/e19250b7b9c07ab378f32a26a2371df0/090626.pdf
  seen: 2026-11-05
  quote: "Twenty-third Sunday in Ordinary Time// XXIII Domingo Ordinario \nSeptember 6, 2026"
  note: The only bulletin the site links (8 pages, text). Page 1 masthead 'ST. GABRIEL OF THE SORROWFUL
    MOTHER ROMAN CATHOLIC CHURCH / 26-26 98th street & Astoria BLVD, East Elmhurst NY 11369', Pastor Rev.
    Nicholas Apollonio, and a Mass Schedule for this church alone.
- url: https://www.saint-gabriel-queens.org/announcements
  seen: 2026-11-05
  note: The Next.js site's Announcements page embeds one Bulletin PDF, a Contentful asset (090626.pdf)
    created 2026-09-10; no later issue is linked as of 2026-11-05. The homepage and schedule page link
    no bulletin.
- url: https://discovermass.com/church/st-gabriel-east-elmhurst-ny/
  seen: 2026-11-05
  note: 'issues.py discovermass: the Discover Mass church page exists but lists no bulletins.'
revisit: Check whether saint-gabriel-queens.org/announcements links a current bulletin (only issue 6 September
  2026)
revisit_after: 2026-12-06
research:
- method: probe get of the parish site's homepage, schedule and announcements pages; probe pdf of the
    linked bulletin; issues.py discovermass st-gabriel-east-elmhurst-ny
  url: https://www.saint-gabriel-queens.org/announcements
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reread the announcements page for a bulletin newer than 6 September 2026 and the parish
    Facebook page (facebook.com/stgabriel26) for posted bulletins; if the site posts one weekly, try provider
    other on the announcements page with fetch:check
  retry_when: The announcements page links an issue dated within the last two weeks
  revisit_after: 2026-12-06
bulletin_status: not-found
---

## Publisher

St. Gabriel (St. Gabriel of the Sorrowful Mother) produces its own bulletin and posts it on its Next.js/Contentful site. The only issue linked, from the Announcements page (read 2026-11-05), is `090626.pdf`, the Twenty-third Sunday in Ordinary Time, September 6, 2026, with the masthead "ST. GABRIEL OF THE SORROWFUL MOTHER ROMAN CATHOLIC CHURCH / 26-26 98th street & Astoria BLVD, East Elmhurst NY 11369" and Rev. Nicholas Apollonio, Pastor. The Discover Mass church page `st-gabriel-east-elmhurst-ny` exists but lists no issues.

## Worship sites

One church. The 6 September Mass Schedule (Sunday 8:30 English, 10:00 and 12:30 Spanish; Saturday 5:30 pm English and 8:30 pm Neocatechumenal; weekdays 8:30 am) names no other place, and the site's schedule page (2026-11-05) lists Masses at the church only. The diocese directory, deanery list, GCatholic 16714 and Mass finder 785 list this one church.

## Website and bulletin provider

`no_bulletin` for now, with the Announcements page kept as `website`. It embeds one Contentful asset at a time and that asset is the 6 September 2026 issue, two months old; no `fetch` resolver reading it was tried, since the pick could only be a stale issue. When a current issue appears, try `other` on the announcements page and `fetch:check` it (the PDF is on `assets.ctfassets.net`, linked from the page's embedded JSON).

## Not yet confirmed

Whether the parish still publishes weekly anywhere (its Facebook page, facebook.com/stgabriel26, was not read). See research; revisit after 2026-12-06.
