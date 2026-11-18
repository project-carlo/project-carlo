---
name: St. Patrick
website: https://stpatrickbayshore.org/bulletins/
bulletin_provider: other
provider_id: page-pdfs https://stpatrickbayshore.org/bulletins/
publication: ['url:https://stpatrickbayshore.org/bulletins/']
group: ''
evidence:
- url: https://stpatrickbayshore.org/wp-content/uploads/2026/11/St.-Patrick-Bulletin-11-8-26.pdf
  seen: 2026-11-13
  note: 'Sunday, November 8, 2026 issue, 20 pages, image-only (no text layer; pages 1, 2 and 20 read as
    renders). Page 1: ''the parish of saint patrick, Bay Shore, New York''. Page 2: 9 North Clinton Avenue,
    Bay Shore, NY 11706; Mass Schedule Saturday 5:00 p.m. Msgr. Purick Hall; Sunday 7:30 a.m. Church,
    9:30 a.m. Church, 9:30 a.m. Msgr. Purick Hall, 11:00 a.m. Church, 12:30 p.m. Church (Spanish), 5:30
    p.m. Church; Monday-Friday 6:30 and 8:00 a.m.; Wednesday 12:10 p.m.; Thursday 8:00 p.m. (Spanish);
    Saturday 8:00 a.m. Page 20 footer: ''474 St. Patrick, Bay Shore, NY (back) FX'' and ''John Patrick
    Publishing Company''.'
- url: https://stpatrickbayshore.org/bulletins/
  seen: 2026-11-13
  note: WordPress bulletin page (read with visit.py; probe url could not connect) lists St.-Patrick-Bulletin-11-8-26.pdf,
    -11-1-2026.pdf, -10-25-26.pdf ... newest first under /wp-content/uploads/.
- url: https://stpatrickbayshore.org/wp-content/uploads/2026/07/St.-Patrick-Bulletin-7-19-26.pdf
  seen: 2026-11-13
  note: Sunday, July 19, 2026 issue, 16 pages, image-only (pages 1-3 read as renders after a browser_get.py
    download). Page 2's Mass Schedule lists only Msgr. Purick Hall and the Church (Saturday 5:00 p.m.
    Msgr. Purick Hall; Sunday 7:30, 9:30, 11:00 a.m., 12:30 p.m. Spanish, 5:30 p.m. Church); it has no
    Our Lady Star of the Sea Mission, Saltaire, Masses, though the mission's own summer 2026 schedule
    had Saturday 5:00 p.m. and Sunday 9:00 and 11:00 a.m. Masses that month.
promoted: 2026-11-13
research:
- method: Tried John Patrick listings church-bulletin.org/st-patrick-bay-shore-ny-11706, /st-patrick-church-bay-shore-ny-11706
    and /saint-patrick-bay-shore-ny-11706
  url: https://church-bulletin.org/st-patrick-bay-shore-ny-11706
  checked: '2026-11-13'
  outcome: not-found
  next_action: None needed while the parish's own page serves the current issue; use the JP listing if
    the parish site stops posting
  retry_when: The parish's /bulletins/ page stops posting new issues
bulletin_status: available
---

## Publisher

The Parish of St. Patrick, 9 North Clinton Avenue, Bay Shore publishes its own weekly bulletin, printed by John Patrick Publishing (page 20 footer "474 St. Patrick, Bay Shore, NY"). The Sunday, November 8, 2026 issue (`https://stpatrickbayshore.org/wp-content/uploads/2026/11/St.-Patrick-Bulletin-11-8-26.pdf`, read 2026-11-13) is image-only; its page 1 names "the parish of saint patrick, Bay Shore, New York" and page 2 gives one Mass Schedule: Saturday 5:00 p.m. in Msgr. Purick Hall; Sunday 7:30 a.m., 9:30 a.m., 11:00 a.m., 12:30 p.m. (Spanish) and 5:30 p.m. in the Church and 9:30 a.m. in Msgr. Purick Hall; Monday-Friday 6:30 and 8:00 a.m.; Wednesday 12:10 p.m.; Thursday 8:00 p.m. (Spanish); Saturday 8:00 a.m.

## Worship sites

Two: the church at 9 North Clinton Avenue (`st-patrick-bay-shore-church`) and, in summer, Our Lady Star of the Sea Mission, 210 Pilot Walk, Saltaire (`our-lady-star-of-the-sea-saltaire-church`, directory:138). Msgr. Purick Hall, where two weekend Masses are held, is the parish's own hall (the diocese's Mass-times page lists its Masses under the church), not a separate worship site. The diocesan locator (directory:127), GCatholic (16809) and the Mass-times page list this building under St. Patrick.

The Saltaire mission is St. Patrick's: the parish site has its page (`https://stpatrickbayshore.org/star-of-the-sea-mission/`, read 2026-11-13) and links its "Mass Schedule and Intentions - Summer 2026" (Sunday 11:00 a.m. from May 24; Saturday 5:00 p.m. and Sunday 9:00 and 11:00 a.m. in July and August; last Mass Saturday, September 19). The bulletin itself does not print the mission's Masses: the Sunday, July 19, 2026 issue (image-only, page 2 read as a render on 2026-11-13) lists only the Church and Msgr. Purick Hall. No other bulletin covers the mission, so it stays with this row; its schedule has to come from the parish site's document, not the bulletin. (Reconcile, 2026-11-13.)

## Website and bulletin provider

stpatrickbayshore.org is self-hosted WordPress (`probe url` could not connect; `visit.py` and fetch:check read it). Its `/bulletins/` page lists `St.-Patrick-Bulletin-<m>-<d>-<yy>.pdf` newest first, so the row is `other` pinned to `page-pdfs https://stpatrickbayshore.org/bulletins/`. fetch:check on 2026-11-13 picked `St.-Patrick-Bulletin-11-8-26.pdf` and dated it 2026-11-08, the right issue. Guessed John Patrick listings on church-bulletin.org returned only the generic archive page.

## Not yet confirmed

Nothing about the parish or church. The issues are image-only scans, so the pipeline needs OCR to read the Mass schedule.
