---
name: St. John Neumann
website: https://ccsjn.org/bulletins
bulletin_provider: other
provider_id: page-pdfs https://ccsjn.org/bulletins filename=*bulletin.pdf
publication: ['url:https://www.church-bulletin.org/the-catholic-community-of-saint-john-neumann-califon-nj-07830']
group: ''
evidence:
- url: https://storage.googleapis.com/wzukusers/user-12949076/documents/9faabde67de34d55b87991eefefb910e/2026-11-01bulletin.pdf
  seen: 2026-11-02
  quote: Fr. Roy N. Quesea, Administrator
  note: '1 November 2026 issue, posted on the parish site (6 pages, all with text). Page 1: ''The Catholic
    Community of St. John Neumann'', ''We are located at: 398 County Road 513, Califon, NJ 07830, 908-832-2513,
    www.ccsjn.org''; ''Weekend Masses: Saturday Vigil 5:30 p.m.; Sunday 9:30 a.m. & 5:30 p.m.; Weekday
    Masses: Tuesday-Thursday 9:00 a.m.'' Page 6 code line ''652 The Catholic Community of St. John Neumann,
    Califon, NJ (B) John Patrick Publishing Company''. Names no other church.'
- url: https://www.church-bulletin.org/bulletin/the-catholic-community-of-saint-john-neumann-califon-nj-07830/2026-11-01.pdf
  seen: 2026-11-02
  note: 'John Patrick copy of the same 1 November 2026 issue: 6 pages, and its pdftotext output is identical
    to the parish-hosted file''s (whitespace-normalised diff empty). church-bulletin.org/?id=652 redirects
    to the listing, newest issue 2026-11-01, the same as the parish page.'
- url: https://ccsjn.org/bulletins
  seen: 2026-11-02
  note: Bulletins page (website-builder site, JavaScript-rendered; read with parish-site-access visit.py
    --links). Lists storage.googleapis.com/wzukusers/user-12949076/documents/<hash>/<YYYY-MM-DD>bulletin.pdf
    weekly from 2026-08-09 to 2026-11-01, plus older files named 2017-10-15.pdf and 2026-08-02.pdf without
    the 'bulletin' suffix.
bulletin_status: available
publication_reviews:
- parish: st-joseph-high-bridge
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1327/20261101B.pdf
    seen: 2026-11-02
    note: The 1 November 2026 masthead (page 1, rendered) names St. Joseph R.C. Church, High Bridge alone,
      with its own Mass times (Sat 4 pm; Sun 8 and 11 am).
  - url: https://storage.googleapis.com/wzukusers/user-12949076/documents/9faabde67de34d55b87991eefefb910e/2026-11-01bulletin.pdf
    seen: 2026-11-02
    note: The 1 November 2026 masthead (page 1) names The Catholic Community of St. John Neumann, Califon
      alone, with its own Mass times (Sat 5:30 pm; Sun 9:30 am and 5:30 pm).
---

## Publisher

The Catholic Community of St. John Neumann, Califon, publishes its own weekly bulletin, printed by John Patrick Publishing (id 652) and posted both on church-bulletin.org and on the parish's own site. I read the 1 November 2026 issue on both (2026-11-02): each has 6 pages with a text layer, and their `pdftotext` output is identical. Page 1 names 'The Catholic Community of St. John Neumann', 398 County Road 513, Califon, with Masses Saturday 5:30 pm, Sunday 9:30 am and 5:30 pm, Tuesday-Thursday 9 am, and 'Fr. Roy N. Quesea, Administrator'. So the two copies are one publication; under *Rules settled* (one bulletin on the parish's site and a publisher's) I recorded the parish-hosted copy and listed the John Patrick listing as the publication id. The parish page is current (newest 1 November, the same as John Patrick).

The parish finder lists Rev. Krzysztof Kaczynski as pastor. Page 5 of the issue says 'we remember Father Kris Kaczynski, my predecessor, who passed away on November 5, 2025', so the finder is out of date. Fr. Quesea is also administrator of St. Joseph, High Bridge, and the same page remembers priests 'who served the communities of Saint Joseph and Saint John Neumann'; the two parishes print separate bulletins with their own mastheads and schedules (LPi container 03/1327 for St. Joseph), so they are separate rows; see `publication_reviews`.

## Worship sites

One church, 398 County Road 513 (directory:24476, gcatholic:18656). The finder's note says 'All Masses are celebrated in Church (398 Rt 513)', and the bulletin names no other place.

## Website and bulletin provider

Website https://ccsjn.org/bulletins, the parish's Bulletins page, which lists each issue as a PDF on Google Cloud Storage (the site builder's file store). Provider `other` with recipe `page-pdfs` on that page, filtered to `*bulletin.pdf` so the 2017 file listed first is skipped. The survey's `probe url` said DEAD-DNS for ccsjn.org, but `probe get` and the browser loaded it.

## Not yet confirmed

Nothing open.

## Fetch check

`pnpm fetch:check` on 2026-11-02 resolved 'page-pdfs on https://ccsjn.org/bulletins: current' and picked `.../9faabde67de34d55b87991eefefb910e/2026-11-01bulletin.pdf`: transport ok, PDF, issue date 2026-11-01 inferred from the file name, freshness `fresh`; identity unverified by the tool, the masthead read above.
