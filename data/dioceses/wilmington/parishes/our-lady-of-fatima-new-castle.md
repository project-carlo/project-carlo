---
name: Our Lady of Fatima
website: https://olfnewcastle.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-of-fatima-church-new-castle-de-19720
publication: ['url:https://www.church-bulletin.org/our-lady-of-fatima-church-new-castle-de-19720']
group: New Castle Deanery
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-of-fatima-church-new-castle-de-19720/2026-10-25.pdf
  seen: 2026-10-27
  quote: Rev. David F. Murphy, Pastor
  note: 'Page 1 of the 25 October 2026 issue: masthead ''Our Lady of Fatima, 801 North DuPont Highway,
    Wilmington Manor, New Castle, Delaware 19720, (302) 328-3431'', for this parish alone. Mass schedule
    box: ''Saturday: 5PM Mass, 7:30PM Spanish Mass / Sunday Masses: 9:30AM, Noon''.'
- url: https://olfnewcastle.com/
  seen: 2026-10-27
  note: 'probe url: HTTP 200; links https://church-bulletin.org/?id=304, which redirects to the church-bulletin.org
    listing of dated PDFs (latest 2026-10-25, then 10-18, 10-11, 10-04, 09-27).'
promoted: 2026-10-27
publication_reviews:
- parish: holy-spirit-st-peter-the-apostle-new-castle
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-fatima-church-new-castle-de-19720/2026-10-25.pdf
    seen: 2026-10-27
    quote: Rev. David F. Murphy, Pastor
    note: '25 October 2026 Our Lady of Fatima issue: own masthead, Mass schedule (Sat 5PM and 7:30PM Spanish;
      Sun 9:30AM, Noon) and content. Checked 2026-10-27: Our Lady of Fatima''s masthead names Fatima alone;
      the Holy Spirit / St. Peter masthead lists those two churches only. The only cross-mention is Holy
      Spirit''s food-pantry strip (p.4) naming all four parishes as partners.'
  - url: https://container.parishesonline.com/bulletins/03/1089/20261025B.pdf
    seen: 2026-10-27
    quote: Rev. Timothy M. Nolan, Pastor
    note: '25 October 2026 joint Holy Spirit / St. Peter issue: its own cover, Mass schedules for those
      two churches and pastor; its food-pantry strip names Our Lady of Fatima and St. Paul only as ministry
      partners.'
- parish: st-paul-delaware-city
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-fatima-church-new-castle-de-19720/2026-10-25.pdf
    seen: 2026-10-27
    quote: Rev. David F. Murphy, Pastor
    note: '25 October 2026 Our Lady of Fatima issue: own masthead, Mass schedule (Sat 5PM and 7:30PM Spanish;
      Sun 9:30AM, Noon) and content. Checked 2026-10-27: Our Lady of Fatima''s masthead names Fatima alone
      and its text never names St. Paul; St. Paul''s one-page issue names St. Paul alone and never names
      Fatima.'
  - url: https://stpauldc.org/wp-content/uploads/2026/10/B102526.pdf
    seen: 2026-10-27
    quote: Saturday Oct. 24 - 5:00pm
    note: '25 October 2026 St. Paul issue: one page, own Mass intentions (Sat 5:00pm, Sun 9:00am) and
      Christmas bazaar notice, different publisher.'
---

## Publisher

Our Lady of Fatima's bulletin is a John Patrick Publishing issue listed at church-bulletin.org/our-lady-of-fatima-church-new-castle-de-19720 (the parish site links `church-bulletin.org/?id=304`). The 25 October 2026 issue has its own masthead (801 North DuPont Highway, pastor Rev. David F. Murphy), its own Mass schedule and its own parish content, so it is a separate publication from the Holy Spirit / St. Peter ParishesOnline bulletin (container 03/1089) even though the two bulletins share a religious education coordinator (Migdalia Ibarrondo) and the Holy Spirit/St. Peter pantry footer names Our Lady of Fatima.

## Worship sites

One church, 801 N. DuPont Highway. Its religious education classes are held at St. Peter the Apostle (page 1 of the 25 October issue), which is a classroom use, not a Mass site.

## Website and bulletin provider

olfnewcastle.com is the parish site; the PDFs live on church-bulletin.org, so the resolver reads the listing page (`page-pdfs`). GCatholic and the diocese map agree on the website. See *Fetch check* below.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish our-lady-of-fatima-new-castle` (2026-10-27): the pinned `page-pdfs` recipe resolved to 2026-10-25.pdf (3.2 MB), 'current', transport ok, document type PDF, issue date observed in the text ('October 25, 2026') and fresh. Identity is 'unverified' by the tool (none supplied); the masthead read above settles it.
