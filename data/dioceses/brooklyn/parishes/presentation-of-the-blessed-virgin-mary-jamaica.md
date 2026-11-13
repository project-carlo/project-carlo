---
name: Presentation of the Blessed Virgin Mary (Jamaica)
website: https://pbvmrcc.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery Q7 (Queens East)
evidence:
- url: https://pbvmrcc.org/wp-content/uploads/2025/12/PresentationBVM12-7.pdf
  seen: 2026-11-06
  quote: 88-19 Parsons Boulevard Jamaica, New York 11432
  note: 'Newest bulletin file on the site (7 December 2025 issue, uploaded 2025-12-08), 8 pages. Page
    1 masthead: ''Presentation of the Blessed Virgin Mary Parish'', Pastor Rev. Victor Manuel Bolaños;
    page 8 footer ''#240 FOR ADVERTISING: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON''.'
- url: https://pbvmrcc.org/wp-json/wp/v2/media?mime_type=application/pdf&per_page=50
  seen: 2026-11-06
  note: 'The site''s PDF media list, newest first: the latest bulletin uploads are PresentationBVM11-9.pdf,
    Presentation11-16.pdf and PresentationBVM12-7.pdf (all 2025-12-08); nothing in 2026.'
- url: https://pbvmrcc.org/mass/
  seen: 2026-11-06
  quote: HORARIO DE LA SANTA MISA
  note: 'Current Mass schedule page: Monday-Friday 12:15 PM (English), 7:00 PM (Español); Saturday 9:00
    AM (Español), 12:15 PM (English); Vigil 5:30 PM (English), 7:00 PM (Español), 8:00 PM (bilingual,
    Neocatechumenal Way); Sunday 7:00 AM, 11:00 AM, 1:00 PM (Español), 9:00 AM (English).'
revisit: Look for a current bulletin on pbvmrcc.org (WordPress media list) or another channel; if weekly
  issues resume, record other with a pinned recipe
revisit_after: 2027-02-01
research:
- method: probe url on the directory homepage (redirects to pbvmrcc.org), probe get of the homepage HTML,
    visit.py --bulletin on pbvmrcc.org, WordPress media API for PDFs
  url: https://pbvmrcc.org/
  checked: '2026-11-06'
  outcome: not-found
  next_action: Re-list pbvmrcc.org's PDF media and menu for a 2026 bulletin; ask whether The Church Bulletin
    Inc. issues are posted anywhere else (Facebook)
  retry_when: A bulletin link appears on pbvmrcc.org, or after 2027-02-01
- method: Discover Mass church page and probe po presentation-church-11432
  url: https://discovermass.com/church/presentation-of-the-blessed-virgin-mary-jamaica-ny/
  checked: '2026-11-06'
  outcome: not-found
  next_action: Recheck Discover Mass for bulletins
  retry_when: After 2027-02-01
bulletin_status: not-found
---

## Publisher

Presentation of the Blessed Virgin Mary printed its own bulletin with The Church Bulletin Inc. (West Babylon): the 7 December 2025 issue (PresentationBVM12-7.pdf, read 2026-11-06) has the masthead "Presentation of the Blessed Virgin Mary Parish", 88-19 Parsons Boulevard, Jamaica, Pastor Rev. Victor Manuel Bolaños, and on page 8 the footer "#240 FOR ADVERTISING: THE CHURCH BULLETIN INC.". No issue after that is posted anywhere found, so the row is `no_bulletin` for now.

## Worship sites

One church. The parish site's Mass page (read 2026-11-06) gives Monday-Friday 12:15 PM and 7:00 PM, Saturday 9:00 AM and 12:15 PM, Vigil 5:30 PM, 7:00 PM and 8:00 PM (Neocatechumenal Way), Sunday 7:00, 9:00, 11:00 AM and 1:00 PM, all at the parish church; the December 2025 bulletin listed the same church only. The diocese's parish and deanery directories (Q7), GCatholic 16655 and Mass finder 1172 list only this church.

## Website and bulletin provider

`no_bulletin`. The directory's homepage presentationparish.nyc redirects to the parish's WordPress site pbvmrcc.org (the masthead's website). Its menu has no bulletin page; its WordPress media list holds bulletin PDFs only through the 7 December 2025 issue (uploaded 2025-12-08). The Discover Mass page says "There are currently no bulletins available", and `probe po presentation-church-11432` finds no ParishesOnline org. The Church Bulletin Inc. has no online container.

## Not yet confirmed

Whether the parish still prints a weekly bulletin and posts it somewhere not checked (Facebook was not read). See research for the retry.
