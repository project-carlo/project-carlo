---
name: St. Margaret of Scotland
website: https://www.margaretofscotland.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-margaret-of-scotland-roman-catholic-church-newark-de-19702
publication: ['url:https://www.church-bulletin.org/saint-margaret-of-scotland-roman-catholic-church-newark-de-19702']
group: Iron Hill Deanery
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-margaret-of-scotland-roman-catholic-church-newark-de-19702/2026-10-25.pdf
  seen: 2026-10-27
  note: 'Pages 1-3 of the 25 October 2026 issue (8 pages, scanned images with no extractable text, so
    read as rendered images): cover ''St. Margaret of Scotland Roman Catholic Church, 2431 Frazer Road,
    Newark, Delaware 19702, 302-834-0225''; page 2 ''Pastor: Rev. Ed Ogden, OSFS'', ''Pastoral Associate
    Deacon Tommy Watts''; page 3 ''Mass Schedule Saturday: 5:00 pm Sunday: 8:30 am & 10:30 am Weekday:
    Mon., Wed., & Fri. 8:30 am''. This parish alone.'
- url: https://www.margaretofscotland.org/
  seen: 2026-10-27
  quote: jppc.net/onlinebulletins/306template.pdf
  note: 'probe url: the site''s bulletin link is https://www.jppc.net/onlinebulletins/306template.pdf,
    which redirects to the church-bulletin.org listing above (306, John Patrick). The eCatholic site (id
    28410) also posts the issues as documents on https://www.margaretofscotland.org/bulletins-archived
    (for example 2026-10-18-1.pdf, 8 pages, also image-only), which look like the same bulletin.'
---

## Publisher

St. Margaret of Scotland publishes its own weekly bulletin, printed by John Patrick Publishing (no. 306). The 25 October 2026 cover names this parish alone, with Rev. Ed Ogden, OSFS as pastor. The bulletin is scanned images: the pipeline will need to read it as an image.

## Worship sites

One church, 2431 Frazer Road, Newark (the Glasgow area; the logo reads 'Glasgow, Delaware'). Mass: Saturday 5:00 pm, Sunday 8:30 and 10:30 am, Monday, Wednesday and Friday 8:30 am. The jppc.net John Patrick listing the survey found is this same bulletin, not a second publisher.

## Website and bulletin provider

`other`, pinned to the church-bulletin.org listing. The eCatholic site (28410) hosts the website and mirrors issues as uploaded documents, not as `files.ecatholic.com/28410/bulletins/` files, so `ecatholic` doesn't read them. The mirrored 18 October file and the listing's 18 October issue are both 8 pages of images; I did not compare them page by page.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-margaret-of-scotland-newark` (2026-10-27): picked church-bulletin.org 2026-10-25.pdf (6.1 MB); transport ok, document type PDF, freshness fresh (2 days). The tool leaves identity 'unverified'; the masthead read above settles it. The pinned recipe is already in `provider_id`, so no new recipe is recorded.

## Not yet confirmed

Whether the eCatholic copy differs from the John Patrick issue (assumed the same bulletin).
