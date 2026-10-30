---
name: Co-Cathedral of St. Robert Bellarmine
website: https://www.strobert.cc/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/co-cathedral-of-saint-robert-bellarmine-freehold-nj-07728
publication: ['url:https://www.church-bulletin.org/co-cathedral-of-saint-robert-bellarmine-freehold-nj-07728']
group: Cohort 12 (Freehold, Manalapan, Millstone)
evidence:
- url: https://www.church-bulletin.org/bulletin/co-cathedral-of-saint-robert-bellarmine-freehold-nj-07728/2026-11-01.pdf
  seen: 2026-10-30
  quote: 61 Georgia Road - Freehold, New Jersey 07728
  note: 'Page 2 of the 1 November 2026 issue (12 pages; pages 1, 2, 6-9 are images, read from a render).
    Its masthead block is headed ''Co-Cathedral of St. Robert Bellarmine, Roman Catholic Diocese of Trenton''
    and gives ''Daily Masses: (Mon.-Fri.) 7AM & 9AM- (Sat.) 9AM'' and ''Weekend Masses: Sat. 4:30PM– Sun.
    8AM, (10AM Livestreamed) & 12PM'', with Rev. Msgr. Sam A. Sirianni as Rector. Names the Co-Cathedral
    alone. Page 3''s Mass intentions text layer matches those times.'
- url: https://www.church-bulletin.org/co-cathedral-of-saint-robert-bellarmine-freehold-nj-07728
  seen: 2026-10-30
  quote: October 25, 2026
  note: 'John Patrick Publishing listing 558 (Co-Cathedral of Saint Robert Bellarmine, Freehold, NJ 07728):
    dated PDFs 2026-10-04, 10-11, 10-18, 10-25 and 11-01.'
- url: https://www.strobert.cc/
  seen: 2026-10-30
  quote: Saturday - 4:30pm (Vigil)
  note: Read with the browser (plain probe url gets HTTP 403). Homepage lists the same Mass times as the
    bulletin; its Bulletin button goes to https://www.strobert.cc/bulletin, whose only link is 'Most Current
    Bulletins' (strobert.cc/bulletin/53-bulletin/file), which the sandbox could not read.
research:
- method: probe pdf on https://www.strobert.cc/bulletin/53-bulletin/file (the site's 'Most Current Bulletins'
    link)
  url: https://www.strobert.cc/bulletin/53-bulletin/file
  checked: '2026-10-30'
  outcome: access-blocked
  next_action: Compare this file's issue date with John Patrick listing 558 if the site starts answering
    probe get; until then read listing 558, which fetch:check selects as the 1 November 2026 issue
  retry_when: strobert.cc stops answering HTTP 403 to probe get, or listing 558 falls behind the site
bulletin_status: available
---

## Publisher

The Co-Cathedral publishes its own weekly bulletin through John Patrick Publishing (listing 558 on church-bulletin.org, latest edition 1 November 2026 on 2026-10-30). Page 2 of that issue, an image read from a render, is headed "Co-Cathedral of St. Robert Bellarmine, Roman Catholic Diocese of Trenton, 61 Georgia Road - Freehold, New Jersey 07728" and gives the schedule of Masses (daily Monday to Friday 7AM and 9AM, Saturday 9AM; weekend Saturday 4:30PM, Sunday 8AM, 10AM and 12PM). It names the Co-Cathedral alone; no other Cohort 12 parish is in it. Rev. Leo Bagenda is an adjunct priest here and at St. Rose of Lima: shared clergy, not a shared bulletin.

## Worship sites

One church, 61 Georgia Rd, Freehold (see `co-cathedral-of-st-robert-bellarmine-freehold`). GCatholic omits it entirely (diocese.md); the diocese's finder lists it as directory:14624.

## Website and bulletin provider

The parish site strobert.cc refuses plain probe url (HTTP 403) but loads in the browser. Its /bulletin page offers one "Most Current Bulletins" file (`/bulletin/53-bulletin/file`), which probe pdf could not read (no PDF returned). The John Patrick listing is read instead, as the playbook says for sites that block: `page-pdfs` on the church-bulletin.org listing.

## Not yet confirmed

Whether the site's `/bulletin/53-bulletin/file` ever carries an issue newer than the John Patrick listing. Both carry the same bulletin, so the listing's id is the publication; see `research`.
