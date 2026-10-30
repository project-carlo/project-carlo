---
name: St. Ann Parish
website: https://www.stannschurch.org/
bulletin_provider: other
provider_id: page-pdfs https://www.stannschurch.org/bulletin
publication: ['url:https://www.stannschurch.org/bulletin']
group: Cohort 4 (Hainesport, Mount Holly, Browns Mills, New Egypt)
evidence:
- url: https://irp.cdn-website.com/0b085e54/files/uploaded/10.25.26.pdf
  seen: 2026-10-30
  quote: Rev. Andrew Thu Pham, SVD
  note: '7-page issue of 25 October 2026 (Thirtieth Sunday in Ordinary Time), pages 1-3 and 7 with a text
    layer, pages 4-6 images. Page 1 (the cover): ''MASS SCHEDULE: SATURDAY: 5:15PM (English) SUNDAY: 8:00
    (Eng) 10:30AM (Eng) 12:00 N (Spanish) WEEKLY: MON., WED., FRI. 9:00AM TUES. & THURS.: 7:00PM''; ''Rev.
    Pierre C. Lunimbu, SVD (Fr. Fleury) Pastor''; ''PARISH OFFICE: (609) 893-3246''; website www.stannschurch.org.
    It names St. Ann''s alone; the ''Masses for the Week'' on page 2 are all at the one church.'
- url: https://www.stannschurch.org/bulletin
  seen: 2026-10-30
  note: The parish's Duda site (probe get reads it) has a Bulletin page with two entries, 'Bulletin Oct
    25, 2026' and 'Bulletin Oct 18, 2026', linking https://irp.cdn-website.com/0b085e54/files/uploaded/10.25.26.pdf
    and .../10.18.26.pdf (page HTML, newest first). The footer shows '22 Trenton Road Browns Mills, NJ'.
    No 1 November issue yet; the 11.1.26 filename was not posted when tried.
- url: https://www.church-bulletin.org/
  seen: 2026-10-30
  note: 'Absence only: the John Patrick scans of ids 1-1300 and 6000-6110 (tools/jppc-nj-1-1300.jsonl,
    jppc-6000-6110.jsonl) hold no Browns Mills (08015) listing, so no printer''s listing was found for
    St. Ann.'
research:
- method: probe url stannschurch.org; probe get /bulletin; probe pdf of the 25 October issue
  url: https://www.stannschurch.org/bulletin
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: the Duda bulletin page is the row''s channel.'
- method: pnpm fetch:check --diocese trenton --parish st-ann-browns-mills (headed Chrome); page-pdfs on
    the bulletin page
  url: https://www.stannschurch.org/bulletin
  checked: '2026-10-30'
  outcome: found
  next_action: None. Picked 10.25.26.pdf (6.4 MB, pdf, issue date 25 October 2026 observed in the text
    and URL, freshness fresh).
bulletin_status: available
publication_reviews:
- parish: our-lady-queen-of-peace-hainesport
  decision: separate
  evidence:
  - url: https://irp.cdn-website.com/0b085e54/files/uploaded/10.25.26.pdf
    seen: 2026-10-30
    note: The 25 October 2026 cover names St. Ann's, Browns Mills alone (pastor Rev. Pierre C. Lunimbu,
      SVD; parish office (609) 893-3246), with its own Mass times.
  - url: https://www.church-bulletin.org/bulletin/our-lady-queen-of-peace-church-hainesport-nj-08036/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Our Lady Queen of Peace Church, Hainesport alone (1603 Marne
      Highway), with its own Mass times.
- parish: sacred-heart-mount-holly
  decision: separate
  evidence:
  - url: https://irp.cdn-website.com/0b085e54/files/uploaded/10.25.26.pdf
    seen: 2026-10-30
    note: The 25 October 2026 cover names St. Ann's, Browns Mills alone (pastor Rev. Pierre C. Lunimbu,
      SVD; parish office (609) 893-3246), with its own Mass times.
  - url: https://www.church-bulletin.org/bulletin/sacred-heart-church-mt-holly-nj-08060/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Sacred Heart Church, Mount Holly alone (pastor Rev. John
      P. Czahur, 260 High Street), with its own Mass times.
- parish: st-isidore-the-farmer-new-egypt
  decision: separate
  evidence:
  - url: https://irp.cdn-website.com/0b085e54/files/uploaded/10.25.26.pdf
    seen: 2026-10-30
    note: The 25 October 2026 cover names St. Ann's, Browns Mills alone (pastor Rev. Pierre C. Lunimbu,
      SVD; parish office (609) 893-3246), with its own Mass times.
  - url: https://www.church-bulletin.org/bulletin/parish-of-saint-isidore-the-farmer-new-egypt-nj-08533/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1, image-only issue) names the Parish of St. Isidore
      the Farmer alone, with Mass at its St. Andrew and Assumption worship sites and Assumption Chapel.
---

## Publisher

St. Ann, Browns Mills publishes its own weekly bulletin on its Duda site, https://www.stannschurch.org/bulletin: a page of dated PDFs under `irp.cdn-website.com/0b085e54/files/uploaded/` named `<m>.<d>.<yy>.pdf` (10.18.26.pdf, 10.25.26.pdf), newest first. The 25 October 2026 issue's cover gives the Mass schedule (Saturday 5:15pm English; Sunday 8:00 and 10:30am English, 12:00 noon Spanish; weekdays), the pastor Rev. Pierre C. Lunimbu, SVD and the office number (609) 893-3246. It names St. Ann alone. The parish is staffed by the Divine Word Missionaries (SVD).

It is Cohort 4 with Hainesport, Mount Holly and New Egypt; a cohort is not a shared bulletin, and each of the four publishes its own. The 2017 decisions also designated St. Ann a Center for Hispanic Ministry, which fits the Spanish noon Mass.

## Worship sites

One church, St. Ann, 22 Trenton Road (see `st-ann-browns-mills`). The bulletin's calendar mentions a 'Capilla' (Spanish prayer group meetings) and rooms named for saints and apparitions; the Mass schedule lists one church, so these are campus rooms, not a second worship site.

## Website and bulletin provider

The finder's website, www.stannschurch.org, is current. The bulletin page is a Duda page whose PDFs are `irp.cdn-website.com` files, so the row is `other` with `page-pdfs https://www.stannschurch.org/bulletin`. No printer's listing was found.

## Not yet confirmed

Nothing outstanding. `fetch:check` (2026-10-30) picks the 25 October 2026 issue (pdf, date observed, fresh).
