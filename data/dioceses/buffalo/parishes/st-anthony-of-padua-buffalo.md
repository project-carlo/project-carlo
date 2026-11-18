---
name: St. Anthony of Padua Church
website: https://stanthonybuffalo.org
bulletin_provider: other
provider_id: ''
publication: ['url:https://stanthonybuffalo.org/mass-times-%26-bulletins']
group: 'Family #22'
evidence:
- url: https://img1.wsimg.com/blobby/go/8dbbabb8-9ff6-446f-a296-5bae6eb122c0/downloads/c1cf8138-d826-4132-8e9a-b1df62054f98/2_2026-9-13.pdf?ver=1789651774309
  seen: 2026-09-26
  note: 'The current bulletin (latest issue), read 2026-09-26. Its Mass schedule and masthead cover: St.
    Anthony of Padua Church.'
promoted: 2026-09-26
research:
- method: fetch-check (headed Chrome) and probe get of the bulletin page, after the live site showed the
    25 October issue on 14 November and the 8 November issue on 16 November
  url: https://stanthonybuffalo.org/mass-times-%26-bulletins
  checked: '2026-11-16'
  outcome: found
  next_action: 'None: the page-pdfs recipe picks the newest listed issue (2026-11-8). The page lists weekly
    issues from 2026-9-6 to 2026-11-8, so the live row lags because the parish posts late, not because
    fetch misses issues.'
  retry_when: The live row falls more than two issues behind the parish's page
---

## Publisher

One bulletin, published by St. Anthony of Padua Church (Family #22), covering 1 worship site(s). PR 14 modelled this as `st-anthony-of-padua-buffalo`.

## Worship sites

St. Anthony of Padua Church. Each church record gives the Mass evidence. Churches of the family that no longer hold Mass are in excluded/ or open/.

## Website and bulletin provider

The bulletin is at https://img1.wsimg.com/blobby/go/8dbbabb8-9ff6-446f-a296-5bae6eb122c0/downloads/c1cf8138-d826-4132-8e9a-b1df62054f98/2_2026-9-13.pdf?ver=1789651774309. Provider `other`.

Checked 2026-11-16: fetch works. The Mass Times & Bulletins page lists weekly PDFs from 6 September to 8 November 2026, and fetch picks the newest (`2026-11-8 (1) (1).pdf`). On 14 November the live row still had the 25 October issue, so this parish posts its bulletin a week or more late, after the weekly fetch runs. This is not a fetch gap.

## Not yet confirmed

Nothing beyond the per-church notes.
