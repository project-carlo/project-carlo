---
name: Our Lady of Peace Parish
website: https://www.olpphazleton.org
bulletin_provider: other
provider_id: page-pdfs https://www.olpphazleton.org/bulletin
publication: ['url:https://www.olpphazleton.org/bulletin']
group: Our Lady of Peace Parish
evidence:
- url: https://irp.cdn-website.com/110e99de/files/uploaded/10.4.26.pdf
  seen: 2026-10-16
  quote: October 4, 2026 VIEW THIS BULLETIN ONLINE AT https://www.olpphazleton.org 2 OUR LADY OF PEACE
    PARISH 27th Sunday in Ordinary Time
  note: Running header of page 2 of the 4 October 2026 issue (the newest on the bulletin page on 2026-10-16).
- url: https://irp.cdn-website.com/110e99de/files/uploaded/10.4.26.pdf
  seen: 2026-10-16
  note: 'Page 1 is an image (rendered and read): "Our Lady of Peace Parish ... Most Precious Blood Church
    ... Fourth & Seybert Streets, Hazleton, PA 18201. Saturday Evening Mass: 5:30 p.m. Sunday Mass: 8:30
    a.m. & 11:00 a.m. Daily Mass: 8:00 a.m. Thursday & Friday". recheck cannot find this text.'
- url: https://irp.cdn-website.com/110e99de/files/uploaded/August+2-+2026.pdf
  seen: 2026-10-16
  quote: The final Mass at Our Lady of Grace church will be celebrated on Sunday, Au…gust 2, 2026, beginning
    at 1:30 pm.
- url: https://www.olpphazleton.org/bulletin
  seen: 2026-10-16
  note: 'The bulletin page links one PDF per week on the Duda CDN (irp.cdn-website.com/110e99de/...),
    with irregular file names: "Bulletin+for+July+5.pdf", "August+2-+2026.pdf", "9.20.26+bulletin.pdf",
    "10.4.26.pdf". Newest on 2026-10-16: 4 October 2026.'
revisit: fetch:check picks 'Parish Consolidation' PDF instead of the bulletin (undated file names like
  10.4.26.pdf); re-run after a chooser fix.
revisit_after: 2026-11-15
promoted: 2026-10-17
---

## Publisher

Our Lady of Peace Parish publishes its own weekly bulletin, posted as PDFs on its site.
The 4 October 2026 issue's masthead (page 1, an image) names one church, Most Precious
Blood, Fourth & Seybert Streets, with Saturday 5:30 pm, Sunday 8:30 and 11 am, and
Thursday and Friday 8 am Masses; every page header reads "OUR LADY OF PEACE PARISH". It is
not shared with another Hazleton parish: the Hazleton clergy's June 2026 city-wide Mass
schedule lists Our Lady of Peace beside Saint Pius, SSCM and Holy Rosary, each of which
has its own bulletin.

## Worship sites

One since August 2026: Most Precious Blood Church (`precious-blood-hazleton`). The parish's
second church, Our Lady of Grace (750 N. Vine Street, GCatholic's "Queen of Heaven Parish"
group), closed with a final Mass on 2 August 2026, announced in the 26 July and 2 August
bulletins and in the clergy's June letter ("Our Lady of Grace Church will close effective
August 2, 2026"): `excluded/our-lady-of-grace-hazleton.md`. The diocese's consolidated-
parishes list also gives the former National Shrine of the Sacred Heart, Harleigh
"(closed 8/8/2011)" with records here; it is in neither roster and has no record.

## Website and bulletin provider

olpphazleton.org (the finder's link and the bulletin's own "VIEW THIS BULLETIN ONLINE AT").
Its /bulletin page lists the PDFs, which embed no publisher id, so provider `other` with
`url:` the bulletin page as the publication. Recipe `page-pdfs
https://www.olpphazleton.org/bulletin` is pinned by inspection (the page links the PDFs
directly). `fetch:check` (run on 2026-10-17 against a temporary parishes.csv holding this
row) picked the wrong file: "Parish+Consolidation-1bcc83bd.pdf" ("first-listed"), a
document linked on the same page, because it cannot date the irregular file names
("10.4.26.pdf", "9.20.26+bulletin.pdf", "August+2-+2026.pdf"). **Until the chooser can date
these names (or skip non-bulletin PDFs), the row fetches the wrong PDF.** Page 1 (masthead
and Mass times) is an image; inner pages have text.

## Not yet confirmed

The 11 October issue was not yet posted on 2026-10-16 (newest 4 October), so the parish
posts a week or two late at times. The resolver's wrong pick (above) needs a fix in the
`other` chooser before this row yields bulletins.
