---
name: Resurrection
website: https://www.resurrectionde.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/resurrection-parish-wilmington-de-19808
publication: ['url:https://www.church-bulletin.org/resurrection-parish-wilmington-de-19808']
group: Iron Hill Deanery
evidence:
- url: https://www.church-bulletin.org/bulletin/resurrection-parish-wilmington-de-19808/2026-10-25.pdf
  seen: 2026-10-27
  note: 'Page 1 of the 25 October 2026 issue (6 pages), read as a rendered image (the cover has no extractable
    text beyond the running head): ''Resurrection Parish, A Catholic Christian Community'', 3000 Videre
    Dr., Wilmington, DE 19808; ''Rev. Msgr. David F. Kelley, Pastor'', ''Rev. Francis I. Okorie, CMF,
    Associate''; ''Mass Times Saturday 5:00 p.m. Sunday 9:30 a.m. Monday & Thursday 8:30 a.m.''. This
    parish alone.'
- url: https://www.church-bulletin.org/bulletin/resurrection-parish-wilmington-de-19808/2026-10-25.pdf
  seen: 2026-10-27
  quote: www.resurrectionde.org
  note: 'Running head of every page: ''310  www.resurrectionde.org  https://ironhilldeanery.com/''; 310
    is the John Patrick Publishing number.'
- url: https://www.resurrectionde.org/
  seen: 2026-10-27
  note: 'Browser read of the parish''s eCatholic site (id 5398): its ''Bulletins'' and ''PARISH BULLETIN''
    links go to https://church-bulletin.org/?id=310 and https://church-bulletin.org/310, which redirect
    to the listing above. `issues.py ecatholic ecatholic:5398` found no files.ecatholic.com bulletins
    (403 for 11, 18 and 25 October).'
promoted: 2026-10-27
publication_reviews:
- parish: holy-family-newark
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/resurrection-parish-wilmington-de-19808/2026-10-25.pdf
    seen: 2026-10-27
    note: 'Resurrection''s 25 October 2026 cover (rendered image): own title and address (3000 Videre
      Dr.), same pastor and associate (Okorie), Mass Saturday 5:00pm, Sunday 9:30am, Monday and Thursday
      8:30am; running head ''310'', not Holy Family''s 308. On 2026-10-27 each cover masthead names one
      parish with its own address and Mass schedule; Resurrection''s text names Holy Family only for a
      ''Holy Family Raise Right program'' (p.4).'
  - url: https://www.church-bulletin.org/bulletin/holy-family-catholic-church-newark-de-19713/2026-10-25.pdf
    seen: 2026-10-27
    note: 'Holy Family''s 25 October 2026 cover (rendered image): own banner and address (15 Gender Road),
      Msgr. Kelley pastor, Rev. Francis Okorie associate pastor, Mass Saturday 5:00pm, Sunday 8:00, 10:00,
      noon.'
---

## Publisher

Resurrection publishes its own weekly bulletin through John Patrick Publishing (no. 310). The parish's eCatholic site links to the church-bulletin.org listing as its bulletin, and carries no eCatholic bulletin files. The 25 October 2026 cover names Resurrection alone: Msgr. David F. Kelley as pastor and Rev. Francis I. Okorie, CMF as associate.

## Worship sites

One church, 3000 Videre Drive, Wilmington (Pike Creek). The cover lists Saturday 5:00 p.m., Sunday 9:30 a.m. and Monday and Thursday 8:30 a.m.; no other building. The directory gives the same times.

## Shared associate check

The Dialog (2024-05-19) paired Resurrection and Holy Family under one associate. The 25 October 2026 covers of both still list Rev. Francis Okorie, but Resurrection's bulletin (310) has its own cover, schedule and parish staff, and Holy Family prints 308. Page 4 mentions Holy Family only in a 'Raise Right program' line. Separate rows. See holy-family-newark.

## Website and bulletin provider

`other`, pinned to the church-bulletin.org listing. The eCatholic site id 5398 is not recorded as a publication: it hosts the website, not the bulletin. resurrectionde.org answers `probe url` with a 200 but the earlier survey saw HTTP 4xx, so use the browser if it blocks.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish resurrection-wilmington` (2026-10-27): picked church-bulletin.org 2026-10-25.pdf (2.9 MB); transport ok, document type PDF, freshness fresh (2 days). The tool leaves identity 'unverified'; the masthead read above settles it. The pinned recipe is already in `provider_id`, so no new recipe is recorded.

## Not yet confirmed

Nothing outstanding.
