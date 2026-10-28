---
name: Holy Family
website: https://www.holyfamilynewark.org/bulletin.php
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/holy-family-catholic-church-newark-de-19713
publication: ['url:https://www.church-bulletin.org/holy-family-catholic-church-newark-de-19713']
group: Iron Hill Deanery
evidence:
- url: https://www.church-bulletin.org/bulletin/holy-family-catholic-church-newark-de-19713/2026-10-25.pdf
  seen: 2026-10-27
  note: 'Page 1 of the 25 October 2026 issue (12 pages), read as a rendered image because the PDF has
    no extractable text: banner ''Holy Family Catholic Church, 15 Gender Road, Newark, DE 19713''; ''Rev.
    Msgr. David Kelley, Pastor'', ''Rev. Francis Okorie, Associate Pastor''; Mass schedule ''Saturday
    Evenings: 5:00pm. Sundays: 8:00am, 10:00am & 12:00pm (noon). Daily Mass: Monday - Friday 8:30am''.
    This parish alone; Resurrection is not named.'
- url: https://www.holyfamilynewark.org/bulletin.php
  seen: 2026-10-27
  note: 'Parish site (browser, visit.py --bulletin): the Bulletin page lists self-hosted PDFs named ''308
    Holy Family <Month day, 2026>.pdf'' (newest 18 October on 27 October) and links https://church-bulletin.org/?id=308,
    which redirects to the church-bulletin.org listing of the same issues (newest 2026-10-25). 308 is
    the John Patrick Publishing number.'
publication_reviews:
- parish: resurrection-wilmington
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/holy-family-catholic-church-newark-de-19713/2026-10-25.pdf
    seen: 2026-10-27
    note: 'Holy Family''s 25 October 2026 cover (rendered image): own banner and address (15 Gender Road),
      Msgr. Kelley pastor, Rev. Francis Okorie associate pastor, Mass Saturday 5:00pm, Sunday 8:00, 10:00,
      noon. Checked 2026-10-27: each cover masthead names one parish with its own address and Mass schedule;
      Resurrection''s text names Holy Family only for a ''Holy Family Raise Right program'' (p.4).'
  - url: https://www.church-bulletin.org/bulletin/resurrection-parish-wilmington-de-19808/2026-10-25.pdf
    seen: 2026-10-27
    note: 'Resurrection''s 25 October 2026 cover (rendered image): own title and address (3000 Videre
      Dr.), same pastor and associate (Okorie), Mass Saturday 5:00pm, Sunday 9:30am, Monday and Thursday
      8:30am; running head ''310'', not Holy Family''s 308.'
---

## Publisher

Holy Family publishes its own weekly bulletin, printed by John Patrick Publishing (no. 308). The parish site's Bulletin page hosts the PDFs itself and links the church-bulletin.org listing, which was a week ahead on 27 October 2026 (2026-10-25 against 18 October on the site). The 25 October 2026 cover names Holy Family alone, with Msgr. David Kelley as pastor and Rev. Francis Okorie as associate pastor.

## Worship sites

One church, 15 Gender Road, Newark. The cover's Mass schedule (Saturday 5:00pm; Sunday 8:00am, 10:00am, noon; Monday to Friday 8:30am; Friday adoration 9:00am) lists no other building.

## Shared associate check

The Dialog's clergy appointments (2024-05-19, via diocese.md) gave Holy Family and Resurrection a shared associate from June 2024. The 25 October 2026 covers of both bulletins still list Rev. Francis Okorie as associate, but each prints its own cover, schedule, staff and number (Holy Family 308, Resurrection 310). Shared priest, separate bulletins: separate rows. See resurrection-wilmington.

## Website and bulletin provider

`other`, pinned to the church-bulletin.org listing (newest first, as for the other John Patrick parishes here). The parish site's own PDFs could not be read from the probe tooling (`probe pdf` got RemoteDisconnected for holyfamilynewark.org), which is another reason to prefer the listing; the listing's 25 October issue downloads.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish holy-family-newark` (2026-10-27): picked church-bulletin.org 2026-10-25.pdf (8.9 MB); transport ok, document type PDF, freshness fresh (2 days). The tool leaves identity 'unverified'; the masthead read above settles it. The pinned recipe is already in `provider_id`, so no new recipe is recorded.

## Not yet confirmed

Nothing outstanding.
