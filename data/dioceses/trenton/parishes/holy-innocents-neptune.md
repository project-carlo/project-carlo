---
name: Holy Innocents Church
website: https://holyinnocentschurch.net/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/holy-innocents-church-neptune-nj-07753
publication: ['url:https://www.church-bulletin.org/holy-innocents-church-neptune-nj-07753']
group: Cohort 18 (Asbury Park, Neptune)
evidence:
- url: https://www.church-bulletin.org/bulletin/holy-innocents-church-neptune-nj-07753/2026-11-01.pdf
  seen: 2026-10-30
  note: '8-page issue dated 1 November 2026 (All Saints), image-only (probe pdf: no extractable text),
    so pages 1-2 were read from renders. Page 1 masthead: ''Holy Innocents Church, 3455 West Bangs Avenue,
    Neptune, NJ 07753, Parish Office 732 922-4242''. Page 2, ''Parish Served By'': Fr. H. Todd Carter,
    Pastor; Fr. Aleksander Bialas, Hospital Chaplain; Deacons John G. Klincewicz and Chris Ellis Jr.;
    footer ''Page 2 - 608''. Mass Schedule: Monday thru Saturday 9:00 AM (except some holidays); Saturday
    Vigil 4:00 PM; Sunday 8:00 AM, 10:00 AM, 12:00 Noon, 5:30 PM; Traditional Latin Mass 9:00 AM every
    first Saturday and 3:00 PM every third Sunday. It names this parish alone.'
- url: https://www.church-bulletin.org/holy-innocents-church-neptune-nj-07753
  seen: 2026-10-30
  note: John Patrick Publishing listing 608, 'Holy Innocents Church, Neptune, NJ 07753'; latest edition
    1 November 2026, with 25 and 18 October below it.
- url: https://holyinnocentschurch.net/
  seen: 2026-10-30
  note: 'probe url: HTTP 200 (the finder''s http://www.holyinnocentschurch.net/ redirects here); its bulletin
    links are https://www.jppc.net/onlinebulletins/608template.pdf, /bulletin/ and /bulletins-archive/.
    The /bulletin/ page links the same 608 template.'
research:
- method: Rendered pages 1-2 of the 1 Nov 2026 issue and read the masthead and Mass block; grep of the
    text layer returned nothing (image-only)
  url: https://www.church-bulletin.org/bulletin/holy-innocents-church-neptune-nj-07753/2026-11-01.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: None
- method: pnpm fetch:check --diocese trenton --parish holy-innocents-neptune (headed Chrome)
  url: https://www.church-bulletin.org/holy-innocents-church-neptune-nj-07753
  checked: '2026-10-30'
  outcome: found
  next_action: 'None; transport ok, document_type pdf, picks the 1 November 2026 issue (freshness future:
    the coming Sunday issue, posted early); publication identity unverified because no expected identity
    is supplied'
bulletin_status: available
publication_reviews:
- parish: mother-of-mercy-asbury-park
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/holy-innocents-church-neptune-nj-07753/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Holy Innocents Church alone, with Fr. H. Todd Carter as pastor
      and its own Mass schedule; Mother of Mercy's bulletin (ParishesOnline 04/0324) has a different pastoral
      team.
---

## Publisher

Holy Innocents Church, Neptune publishes its own weekly bulletin through John Patrick Publishing (listing 608). The 1 November 2026 issue is image-only; its rendered page 1 masthead names Holy Innocents Church at 3455 West Bangs Avenue alone, and page 2 gives Fr. H. Todd Carter as pastor with one Mass schedule for one church. It doesn't mention Mother of Mercy, Asbury Park, the other Cohort 18 parish, whose bulletin (ParishesOnline 04/0324) has a different pastoral team and masthead, so the two are separate rows.

## Worship sites

One church, 3455 West Bangs Avenue (`holy-innocents-neptune`). The bulletin lists no mission or chapel.

## Website and bulletin provider

The parish's live site is holyinnocentschurch.net (the finder's .net address; GCatholic's holyinnocentschurch.com has no DNS). Its bulletin page links the John Patrick 608 template, so the row is `other` with `page-pdfs` on the listing.

## Not yet confirmed

Nothing outstanding. The issue pages are images, so the words quoted come from renders and are recorded as notes.
