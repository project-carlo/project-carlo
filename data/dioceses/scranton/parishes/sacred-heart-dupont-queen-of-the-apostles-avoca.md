---
name: Sacred Heart of Jesus Parish (Dupont) and Queen of the Apostles Parish (Avoca)
website: https://stmaryavoca.com
bulletin_provider: other
provider_id: ''
publication: ['url:https://stmaryavoca.com/bulletin/', 'url:https://sacredheartdupont.com/blog/']
group: Sacred Heart of Jesus Parish Dupont; Queen of the Apostles Parish
evidence:
- url: https://stmaryavoca.com/wp-content/uploads/2026/10/10-11-26-final.pdf
  seen: 2026-10-16
  quote: 'Both parish offices will be closed on Monday, October 12. The SM'
  note: 'Page 1 of the 11 October 2026 issue, from St. Mary Avoca''s Bulletin page. The issue speaks for both parishes throughout, coding them SH (Sacred Heart, Dupont) and SM (St. Mary, Avoca).'
- url: https://stmaryavoca.com/wp-content/uploads/2026/10/10-11-26-final.pdf
  seen: 2026-10-16
  quote: '5:30pm (SM) Jason Kuna'
  note: 'Page 2 MASS INTENTIONS for 12-18 October: Mon, Wed, Fri 7:30 am (SH); Tue, Thu 9:00 am (SM); Saturday 4:00 pm (SH) and 5:30pm (SM); Sunday 8:00 am (SM) and 10:30 am (SH). Page 3 is a blank image page.'
- url: https://sacredheartdupont.com/wp-content/uploads/2026/10/10-11-26-final.pdf
  seen: 2026-10-16
  note: 'The same issue as linked from Sacred Heart Dupont''s Blog page: byte-identical to the Avoca copy (same MD5, 541,703 bytes). Both sites list the same five issues, 13 September to 11 October 2026, under the same file names.'
- url: https://sacredheartdupont.com/schedule/
  seen: 2026-10-16
  quote: 'was named also the pastor of Queen of the Apostles Parish in Avoca'
  note: 'Parish history on the Dupont site: Rev. Thomas J. Petro, pastor in Dupont, named pastor of Queen of the Apostles on 1 July 2025.'
---

## Publisher

Sacred Heart of Jesus Parish (Dupont) and Queen of the Apostles Parish (Avoca) are two canonical
parishes in the diocese's finder. Since 1 July 2025 they share a pastor, Rev. Thomas J. Petro (the
Dupont site's parish history says he "was named also the pastor of Queen of the Apostles Parish in
Avoca"), and they now publish one weekly bulletin. The 11 October 2026 issue is a single file that
both parish sites post: the Avoca copy and the Dupont copy are byte-identical. It is written for both
parishes ("Both parish offices will be closed...", "CCD students ... in both parishes") and codes
them SH and SM. Its Mass intentions for 12-18 October give the full schedule: Monday, Wednesday and
Friday 7:30 am (SH); Tuesday and Thursday 9 am (SM); Saturday 4 pm (SH) and 5:30 pm (SM); Sunday
8 am (SM) and 10:30 am (SH).

## Worship sites

Two: `sacred-heart-of-jesus-dupont` (SH) and `st-mary-avoca` (SM), the only buildings the bulletin
schedules, and the only worship sites the finder lists for the two parishes. The All Souls Masses on
2 November at the Sacred Heart Cemetery Chapel (Dupont) and the SS. Peter and Paul Cemetery Chapel
(Moosic) are one-day cemetery Masses, not regular worship sites, and no roster lists them.

## Website and bulletin provider

The bulletin is self-hosted twice: on stmaryavoca.com's Bulletin page (/bulletin/) and on
sacredheartdupont.com's Blog page (/blog/), each linking WordPress uploads named by date
(`/wp-content/uploads/2026/10/10-11-26-final.pdf`). `website` is the Avoca site, whose homepage
links its Bulletin page directly; both listing pages are recorded as `publication` so that neither
can be claimed by another row. `bulletin_provider: other` with no recipe pinned: `fetch:check` reads
only promoted rows, so it could not be run here. The Avoca recipe is likely `page-pdfs
https://stmaryavoca.com/bulletin/`.

## Not yet confirmed

The pages before page 3 carry no masthead naming either church (page 3 is a blank image). Run
`fetch:check` after promotion and pin the recipe it prints.
