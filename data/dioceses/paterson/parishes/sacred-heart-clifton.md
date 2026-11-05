---
name: Sacred Heart
website: https://sacredheartclifton.com/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:11647']
group: ''
evidence:
- url: https://files.ecatholic.com/11647/bulletins/20261025.pdf
  seen: 2026-11-05
  note: '25 October 2026 issue. Page 1 is an image (no text layer for the masthead; the hidden text says
    ''Sunday, October 4, 2026''), rendered with render.py: ''Church of the Sacred Heart 145 Randolph Avenue
    + Clifton, New Jersey + 07011'', ''Thirtieth Sunday in Ordinary Time October 25, 2026'', MASS TIMES
    ''Saturday: 12:00p.m. Noon, 5:00p.m. (Anticipated), 7:00p.m. (Español) Sunday: 8:00a.m. (EF: Latin),
    10:00a.m., 12:00p.m. Weekdays: 12:00p.m., 7:00p.m. (Español: lunes, martes, jueves, viernes)''; pastor
    Rev. Robert W. Wisniefski. No other parish or church named.'
- url: https://files.ecatholic.com/11647/bulletins/20261101.pdf
  seen: 2026-11-05
  quote: Sunday, November 1, 2026
  note: 1 November 2026 issue (8 pages). Page 1 is an image-only All Saints/All Souls cover (rendered;
    artwork marked JPPC), no masthead. Page 2 Mass intentions for 2-8 November at 12:00 pm, 7:00 pm (Spanish),
    Saturday 5:00 pm and 7:00 pm, Sunday 8:00, 10:00 am and 12:00 pm.
- url: https://sacredheartclifton.com/bulletins
  seen: 2026-11-05
  note: 'Read with visit.py. eCatholic site 11647, title ''Sacred Heart Church - Clifton, NJ''; lists
    files.ecatholic.com/11647/bulletins/ issues newest first: ''November 1, 2026'' (20261101.pdf), ''October
    25, 2026'', ''October 18, 2026'' ..., weekly.'
bulletin_status: available
---

## Publisher

Sacred Heart, Clifton publishes its own weekly bulletin on its eCatholic site. The 25 October 2026 issue (`https://files.ecatholic.com/11647/bulletins/20261025.pdf`, read 2026-11-05; page 1 is an image, rendered) is headed "Church of the Sacred Heart 145 Randolph Avenue + Clifton, New Jersey + 07011" and names no other parish. The 1 November issue has a seasonal All Saints/All Souls cover (artwork marked JPPC) instead of the masthead; its page 2 carries the week's Mass intentions.

## Worship sites

- `sacred-heart-clifton`: the 25 October page 1 gives "Saturday: 12:00p.m. Noon, 5:00p.m. (Anticipated), 7:00p.m. (Español) Sunday: 8:00a.m. (EF: Latin), 10:00a.m., 12:00p.m." and weekdays 12:00 p.m. and 7:00 p.m. (Spanish).

The bulletin names no other place of Mass. The finder (directory:11647) and GCatholic (18948) list this one church.

## Website and bulletin provider

`sacredheartclifton.com` is eCatholic site 11647 (the finder pin id). visit.py read its `/bulletins` page on 2026-11-05: `files.ecatholic.com/11647/bulletins/<YYYYMMDD>.pdf` weekly, newest 20261101 (the 8 November file answers 403, not posted yet). Provider `ecatholic`. `fetch:check` on 2026-11-05 picked `https://files.ecatholic.com/11647/bulletins/20261101.pdf?t=1793313537000` (the 1 November 2026 issue, 4 days old: fresh); it reports "First page has no extractable text" and identity unverified, which is expected here. Page 1 of each issue is an image (the masthead and Mass times are drawn, and its hidden text layer carries a stale 'Sunday, October 4, 2026'), so the pipeline has to read page 1 as an image.

## Not yet confirmed

Nothing outstanding.
