---
name: Church of Sacred Heart
website: https://sacredheartmh.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/sacred-heart-church-mt-holly-nj-08060
publication: ['url:https://www.church-bulletin.org/sacred-heart-church-mt-holly-nj-08060']
group: Cohort 4 (Hainesport, Mount Holly, Browns Mills, New Egypt)
evidence:
- url: https://www.church-bulletin.org/bulletin/sacred-heart-church-mt-holly-nj-08060/2026-11-01.pdf
  seen: 2026-10-30
  quote: 'Pastor: Rev. John P. Czahur ext. 308'
  note: '12-page issue of 1 November 2026, text layer. Page 1 masthead: ''Sacred Heart Church 260 High
    Street, Mount Holly, NJ 08060-1404 Telephone: 609-267-0209 ... Website: https://sacredheartmh.org'';
    ''Mass Schedule Saturday: 4:30pm (Vigil) Sunday: 7:30am, 9:30am Live Stream, 11:30am Weekday: Mon.-Fri.
    7:00am & 8:30am Saturday: 8:30am''. It names Sacred Heart alone. The issue never names Christ the
    Redeemer or 113 South Avenue (grepped ''Redeemer'', ''South Ave'', ''Cristo'', ''Hispanic'', ''Spanish'':
    no hits), and prints no Spanish Mass.'
- url: https://www.church-bulletin.org/sacred-heart-church-mt-holly-nj-08060
  seen: 2026-10-30
  note: 'John Patrick Publishing listing 512 (''Sacred Heart Church, Mt. Holly, NJ 08060'', 260 High Street,
    (609) 267-0209): latest edition 1 November 2026.'
- url: https://sacredheartmh.org/
  seen: 2026-10-30
  note: 'Homepage (answers 403 to plain fetch; read in the browser): the link ''Click here to access our
    current bulletin.'' goes to https://www.jppc.net/onlinebulletins/512template.pdf, which redirects
    to the listing above.'
- url: https://sacredheartmh.org/bulletins
  seen: 2026-10-30
  note: The parish's eCatholic site (id 14457; probe url reads it, issues.py finds no Sunday-dated files)
    has an Archived Bulletins page that ends at 'March 16, 2025' (files.ecatholic.com/14457/bulletins/20250316.pdf).
    It is frozen, so ecatholic:14457 is not recorded as the bulletin.
research:
- method: visit.py sacredheartmh.org and /bulletins; issues.py ecatholic 14457; church-bulletin.org listing
    512
  url: https://sacredheartmh.org/bulletins
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: the row reads the John Patrick listing.'
- method: pnpm fetch:check --diocese trenton --parish sacred-heart-mount-holly (headed Chrome); page-pdfs
    on the John Patrick listing
  url: https://www.church-bulletin.org/sacred-heart-church-mt-holly-nj-08060
  checked: '2026-10-30'
  outcome: found
  next_action: 'None. Picked the 1 November 2026 issue (pdf, issue date observed, freshness ''future'':
    the coming Sunday''s issue).'
bulletin_status: available
publication_reviews:
- parish: our-lady-queen-of-peace-hainesport
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/sacred-heart-church-mt-holly-nj-08060/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Sacred Heart Church, Mount Holly alone (pastor Rev. John
      P. Czahur, 260 High Street), with its own Mass times.
  - url: https://www.church-bulletin.org/bulletin/our-lady-queen-of-peace-church-hainesport-nj-08036/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Our Lady Queen of Peace Church, Hainesport alone (1603 Marne
      Highway), with its own Mass times.
- parish: st-ann-browns-mills
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/sacred-heart-church-mt-holly-nj-08060/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Sacred Heart Church, Mount Holly alone (pastor Rev. John
      P. Czahur, 260 High Street), with its own Mass times.
  - url: https://irp.cdn-website.com/0b085e54/files/uploaded/10.25.26.pdf
    seen: 2026-10-30
    note: The 25 October 2026 cover names St. Ann's, Browns Mills alone (pastor Rev. Pierre C. Lunimbu,
      SVD; parish office (609) 893-3246), with its own Mass times.
- parish: st-isidore-the-farmer-new-egypt
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/sacred-heart-church-mt-holly-nj-08060/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Sacred Heart Church, Mount Holly alone (pastor Rev. John
      P. Czahur, 260 High Street), with its own Mass times.
  - url: https://www.church-bulletin.org/bulletin/parish-of-saint-isidore-the-farmer-new-egypt-nj-08533/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1, image-only issue) names the Parish of St. Isidore
      the Farmer alone, with Mass at its St. Andrew and Assumption worship sites and Assumption Chapel.
---

## Publisher

Sacred Heart, Mount Holly publishes one weekly bulletin through John Patrick Publishing (listing 512 on church-bulletin.org). The 1 November 2026 issue is headed 'Sacred Heart Church, 260 High Street, Mount Holly' with Rev. John P. Czahur as pastor and one Mass schedule (Saturday 4:30pm vigil; Sunday 7:30, 9:30, 11:30; weekdays 7:00 and 8:30; Saturday 8:30am). The parish's own site (sacredheartmh.org, eCatholic 14457) links the listing as its 'current bulletin'; its eCatholic archive stopped in March 2025.

The 2017 *Faith in Our Future* decisions (https://dioceseoftrenton.org/decisions, Cohort 4, item 3) continued the linkage of Christ the Redeemer and Sacred Heart, 'with Christ the Redeemer designated as Center For Hispanic Ministry'. The July 2024 cohort list names Sacred Heart, Mount Holly and not Christ the Redeemer. The two parishes never had separate rows in this batch: no Christ the Redeemer bulletin was found, and the Sacred Heart masthead does not name it now (see `christ-the-redeemer-mount-holly` in `open/`).

It is Cohort 4 with Hainesport, Browns Mills and New Egypt; a cohort is not a shared bulletin, and each publishes its own.

## Worship sites

One church, Sacred Heart, 260 High Street (see `sacred-heart-mount-holly`). The Chapel of the Two Hearts and the Eucharistic Chapel the bulletin mentions are inside the church/parish buildings. GCatholic's Christ the Redeemer, 113 South Avenue is not a row here: the 2018 to January 2020 Sacred Heart mastheads list it only as the priests' 'Residence', and it is in `open/`.

## Website and bulletin provider

The finder's website, parishofsacredheart.org, has moved to sacredheartmh.org (the finder's and GCatholic's old name still answers on the eCatholic host). The row's website is sacredheartmh.org; it reads the printer's listing because the site's own archive is frozen.

## Not yet confirmed

`fetch:check` (2026-10-30) picks the 1 November 2026 issue from the listing. Nothing else about this bulletin. Whether Christ the Redeemer still holds Mass is open; see its record.
