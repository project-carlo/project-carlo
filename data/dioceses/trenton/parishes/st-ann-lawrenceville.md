---
name: Church of St. Ann
website: https://www.churchofsaintann.net/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=11520
publication: ['url:http://sponsors.bonventure.net/?page=11520']
group: Cohort 7 (St. Ann, Lawrenceville and the Korean Martyrs)
evidence:
- url: http://sponsors.bonventure.net/pdfs/11520/2026-11-01.pdf
  seen: 2026-10-30
  quote: The weekly parish bulletin for The Church of Saint Ann 1253 Lawrenceville Road, Lawrenceville,
    NJ 08648 and the Saint Michael Church, Trenton, NJ
  note: 'Masthead (page 1) of the 1 November 2026 issue, ''The Sunday Steward'' (12 pages, text layer,
    footer ''#562 St. Ann''). It names St. Ann and St. Michael Church, Trenton together. Page 4 lists
    St. Ann''s Masses and St. Michael''s Church''s: Sunday 8:30 AM (English), 10:00 AM (Slovak), 12:30
    PM (Korean); Thursday 10:00 AM Korean Mass; Friday 8:00 PM Korean Mass. Page 10 names Rev. Leandro
    Dela Cruz, Pastor, and Rev. Peter Bujdos, Weekend Assistant - Saint Michael Church.'
- url: http://sponsors.bonventure.net/?page=11520
  seen: 2026-10-30
  quote: Saint Ann Church
  note: Bon Venture sponsor page 11520, headed 'Saint Ann Church, 1253 Lawrenceville Road, Lawrenceville,
    NJ 08648'; 'Click to View Current Bulletin'; previous bulletins listed weekly from 1 November 2026
    back through 2025.
- url: https://www.churchofsaintann.net/
  seen: 2026-10-30
  note: Read in the browser (probe url answers 403). The homepage's 'Weekly Bulletin' link goes to http://sponsors.bonventure.net/?page=11520;
    its 'Bulletin Archive' (/bulletins, eCatholic 20164) lists only files.ecatholic.com/20164/bulletins/
    issues from October 2021 and earlier, so ecatholic:20164 hosts the website and is not the current
    bulletin. The site's Mass Schedule page lists a 'St. Michael Church' block beside St. Ann's, and the
    homepage links 'St. Michael's Church - Live-stream Channel'.
- url: https://trentonmonitor.com/2026/10/19/trenton-church-to-host-annual-st-jude-novena-oct-20-28/
  seen: 2026-10-30
  quote: St. Michael Church, which is part of St. Ann Parish, Lawrenceville, is currently a trilingual
    community serving English, Korean and Slovak-speaking Catholics.
  note: 'The Monitor, 19 October 2026: the St. Jude Solemn Novena is at St. Michael Church, 1130 Brunswick
    Ave., Trenton; it is part of St. Ann Parish.'
research:
- method: 'probe url on the finder''s website (churchofsaintann.net), then visit.py in the browser: homepage
    links, /bulletins, /mass-schedule'
  url: https://www.churchofsaintann.net/
  checked: '2026-10-30'
  outcome: found
  next_action: None; the Bon Venture page is current.
- method: John Patrick listing 562 (church-bulletin.org), via tools/jppc-trenton.tsv
  url: https://www.church-bulletin.org/the-church-of-saint-ann-saint-michael-church-lawrenceville-nj-08648
  checked: '2026-10-30'
  outcome: not-found
  next_action: 'None needed: the listing has no edition, but the bulletin''s footer ''#562 St. Ann'' shows
    John Patrick''s number 562 is this parish''s template, and the issues are served from Bon Venture
    11520.'
  retry_when: Only if the Bon Venture page stops updating
bulletin_status: available
---

## Publisher

The Church of St. Ann, 1253 Lawrenceville Road, Lawrenceville, publishes its own weekly bulletin, *The Sunday Steward*, hosted by Bon Venture Services on sponsors.bonventure.net, account 11520. The masthead of the 1 November 2026 issue (page 1) reads "The weekly parish bulletin for The Church of Saint Ann 1253 Lawrenceville Road, Lawrenceville, NJ 08648 and the Saint Michael Church, Trenton, NJ", so one bulletin covers both churches. Page 10 names Rev. Leandro Dela Cruz as pastor and Rev. Peter Bujdos as weekend assistant for Saint Michael Church. The issue's footer "#562 St. Ann" is the John Patrick number the survey found as listing 562 ("The Church of Saint Ann & Saint Michael Church", no edition); that listing is empty, and the bulletins are on the Bon Venture page.

## Worship sites

Two churches share this bulletin:

- `st-ann-church-lawrenceville`, 1253 Lawrenceville Road. Page 4: Saturday 4:00 PM vigil; Sunday 9:00 AM, 10:30 AM, 12:00 PM and 4:00 PM (sensory-friendly); daily Mass Monday to Saturday 8:00 AM in the Chapel, which is on this campus (the parish office, Faith Development Center and school are behind the church).
- `st-michael-trenton`, 1130 Brunswick Ave, Trenton, the home of the Church of the Korean Martyrs community (the diocese's "Korean Martyrs Parish", finder pin directory:14575, GCatholic 18711). The bulletin schedules St. Michael's Sunday 8:30 AM (English), 10:00 AM (Slovak), 12:30 PM (Korean), Thursday 10:00 AM (Korean) and Friday 8:00 PM (Korean).

John Patrick listing 530, "Saint Michael Church, Trenton" (no edition), is St. Michael's own old listing and has no bulletin.

## Website and bulletin provider

The parish site is eCatholic (20164) but its bulletin is not: the homepage's "Weekly Bulletin" link goes to the Bon Venture page, and the eCatholic /bulletins archive stops in October 2021. The row is `other` with `page-pdfs http://sponsors.bonventure.net/?page=11520`.

## Not yet confirmed

The Korean Martyrs community also keeps its own Korean-language site and weekly bulletin (see `st-michael-trenton`); it is not part of this row's bulletin.
