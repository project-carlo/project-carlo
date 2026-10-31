---
name: Our Lady Queen of Peace Church
website: https://ourladyqop.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-queen-of-peace-church-hainesport-nj-08036
publication: ['url:https://www.church-bulletin.org/our-lady-queen-of-peace-church-hainesport-nj-08036']
group: Cohort 4 (Hainesport, Mount Holly, Browns Mills, New Egypt)
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-queen-of-peace-church-hainesport-nj-08036/2026-11-01.pdf
  seen: 2026-10-30
  quote: 1603 Marne Highway, Hainesport, New Jersey 08036
  note: 8-page issue of 1 November 2026 (Solemnity of All Saints), text layer. Page 1 is headed 'Our Lady
    Queen of Peace Church' alone; the page footers read '565 Our Lady Queen of Peace (B) ... John Patrick
    Publishing Company'. The 'Masses For the Week' block (page 2) lists Saturday 4:30 p.m., Sunday 7:30,
    9:00 and 10:30 a.m., and weekday 9:00 a.m. (Monday a Communion Service), with no other church named.
    Page 6 carries a 'Sacred Heart, Mt. Holly' food-pantry notice, an item for a neighbouring parish,
    not a joint masthead.
- url: https://www.church-bulletin.org/our-lady-queen-of-peace-church-hainesport-nj-08036
  seen: 2026-10-30
  note: 'John Patrick Publishing listing 565 (''Our Lady Queen of Peace Church, Hainesport, NJ 08036'',
    1603 Marne Highway, (609) 267-0230): latest edition 1 November 2026, archive back through September
    and earlier. It is not in tools/jppc-trenton.tsv, which missed ZIP 08036; the scan file jppc-nj-1-1300.jsonl
    has it.'
- url: https://ourladyqop.org/news-events/bulletin
  seen: 2026-10-30
  note: Solutio site (plain fetch answers 403; read in the browser with visit.py). Its Bulletin page lists
    numbered issues 'October 25, 2026 New' (291) back to June 2026 over 8 pages, each a /file link that
    also answers 403 to probe get. The site's issue is a week behind the listing's 1 November issue, so
    the row reads the listing.
promoted: 2026-10-30
research:
- method: visit.py ourladyqop.org --bulletin; probe get of the Solutio /file link; church-bulletin.org
    listing 565
  url: https://ourladyqop.org/news-events/bulletin
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: the row reads the John Patrick listing, whose PDFs probe pdf reads.'
- method: pnpm fetch:check --diocese trenton --parish our-lady-queen-of-peace-hainesport (headed Chrome);
    page-pdfs on the John Patrick listing
  url: https://www.church-bulletin.org/our-lady-queen-of-peace-church-hainesport-nj-08036
  checked: '2026-10-30'
  outcome: found
  next_action: 'None. Picked the 1 November 2026 issue (3.46 MB, pdf, issue date observed in the text
    and URL; freshness ''future'': the coming Sunday''s issue). Identity unverified only because fetch:check
    was given no expected identity.'
bulletin_status: available
publication_reviews:
- parish: sacred-heart-mount-holly
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-queen-of-peace-church-hainesport-nj-08036/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Our Lady Queen of Peace Church, Hainesport alone (1603 Marne
      Highway), with its own Mass times.
  - url: https://www.church-bulletin.org/bulletin/sacred-heart-church-mt-holly-nj-08060/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Sacred Heart Church, Mount Holly alone (pastor Rev. John
      P. Czahur, 260 High Street), with its own Mass times.
- parish: st-ann-browns-mills
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-queen-of-peace-church-hainesport-nj-08036/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Our Lady Queen of Peace Church, Hainesport alone (1603 Marne
      Highway), with its own Mass times.
  - url: https://irp.cdn-website.com/0b085e54/files/uploaded/10.25.26.pdf
    seen: 2026-10-30
    note: The 25 October 2026 cover names St. Ann's, Browns Mills alone (pastor Rev. Pierre C. Lunimbu,
      SVD; parish office (609) 893-3246), with its own Mass times.
- parish: st-isidore-the-farmer-new-egypt
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-queen-of-peace-church-hainesport-nj-08036/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Our Lady Queen of Peace Church, Hainesport alone (1603 Marne
      Highway), with its own Mass times.
  - url: https://www.church-bulletin.org/bulletin/parish-of-saint-isidore-the-farmer-new-egypt-nj-08533/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1, image-only issue) names the Parish of St. Isidore
      the Farmer alone, with Mass at its St. Andrew and Assumption worship sites and Assumption Chapel.
---

## Publisher

Our Lady Queen of Peace, Hainesport publishes its own weekly bulletin through John Patrick Publishing (listing 565 on church-bulletin.org). The 1 November 2026 issue (text layer, 8 pages) is headed 'Our Lady Queen of Peace Church, 1603 Marne Highway, Hainesport, New Jersey 08036' and lists one church's Masses. The parish's Solutio site (ourladyqop.org) posts the same bulletins a week behind, so the row reads the listing (settled rule: take the channel with the latest issue).

It is Cohort 4 with Sacred Heart (Mount Holly), St. Ann (Browns Mills) and St. Isidore the Farmer (New Egypt) in the diocese's July 2024 cohort list. A cohort is not a shared bulletin: each of the four publishes its own, and this masthead names Hainesport alone.

## Worship sites

One church, Our Lady Queen of Peace, 1603 Marne Highway (see `our-lady-queen-of-peace-hainesport`). GCatholic and the finder list the same address. The site's calendar lists Mass at the 'Parish Church' and meetings at a parish center, not a second worship site.

## Website and bulletin provider

The finder's and GCatholic's old site is ourladyqop.org (the finder) and olqponline.org (GCatholic, dead: no DNS per the diocese's *Sources*). ourladyqop.org answers 403 to probe url and loads in the browser; its bulletin links are Solutio `/file` downloads that 403 to probe get, so the row uses the printer's listing.

## Not yet confirmed

Nothing outstanding. `fetch:check` (2026-10-30) picks the 1 November 2026 issue from the listing (pdf, date observed, freshness 'future' because it is the coming Sunday's issue).
