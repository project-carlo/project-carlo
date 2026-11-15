---
name: St. Lawrence
website: https://www.stlawrencechurch.com
bulletin_provider: parishes_online
provider_id: st-lawrence-roman-catholic-community
publication: ['po-org:st-lawrence-roman-catholic-community', 'lpi:0018000000Qc1W8AAJ', 'po-container:04/0920']
group: 'Yoked: Higganum, Killingworth'
evidence:
- url: https://container.parishesonline.com/bulletins/04/0920/20261115B.pdf
  seen: 2026-11-14
  note: 'November 15, 2026 issue, 6 pages. Its text layer is in a shifted font encoding (each character
    29 code points low; digits do not survive), so no verbatim quote is possible. Decoded, page 1 reads:
    Hemlock Drive, Killingworth, CT; www.stlawrencechurch.com; Rev. Joseph F. De Costa, Pastor; Rev. Martin
    Jones, Parochial Vicar; Sunday Masses (Vigil Saturday, Sunday); Daily Masses (Monday No Mass, Tuesday
    pm, Wednesday - Saturday am).'
- url: https://parishesonline.com/organization/st-lawrence-roman-catholic-community
  seen: 2026-11-14
  note: 'probe po: title ''St. Lawrence Roman Catholic Community'', 7 Hemlock Dr, Killingworth, website
    www.stlawrencechurch.com, lpi 0018000000Qc1W8AAJ, container 04/0920, weekly issues to 2026-11-15.'
- url: https://saintjohnmiddletownct.weebly.com/area-parish-bulletins.html
  seen: 2026-11-14
  note: St. John Middletown's area-bulletins page links parishesonline.com/organization/st-lawrence-roman-catholic-community
    for Killingworth.
- url: https://www.stlawrencechurch.com
  seen: 2026-11-14
  note: Duda site (irp.cdn-website.com files); probe url counts a parishesonline.com link. Its calendar
    shows 4pm Vigil Mass on Saturday, 8:30am and 10:30am Mass on Sunday, 7pm Mass on Tuesday.
promoted: 2026-11-14
research:
- method: probe pdf of the November 15, 2026 issue (container 04/0920)
  url: https://container.parishesonline.com/bulletins/04/0920/20261115B.pdf
  checked: '2026-11-14'
  outcome: unsupported-format
  next_action: Check whether the pipeline's extraction of this container gives Mass times (OCR or a fixed
    encoding); if every issue keeps the shifted encoding and the pipeline gets no times, set bulletin_provider
    unsupported with a fetch_gap
  retry_when: After the first pipeline run that reads this row, or a later issue whose text layer decodes
    normally
bulletin_status: available
publication_reviews:
- parish: st-peter-higganum
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/04/0920/20261115B.pdf
    seen: 2026-11-14
    note: The 15 November 2026 masthead names St. Lawrence alone, 7 Hemlock Drive, Killingworth, with
      its own Sunday and daily Masses; it mentions St. Peter Church only as another parish.
  - url: https://container.parishesonline.com/bulletins/04/0514/20261115B.pdf
    seen: 2026-11-14
    note: The 15 November 2026 St. Peter masthead names Saint Peter Church alone, with its own Mass schedule;
      this is the bulletin for St. Peter only.
---

## Publisher

St. Lawrence, Killingworth publishes its own LPi bulletin, ParishesOnline org `st-lawrence-roman-catholic-community` (container 04/0920, lpi:0018000000Qc1W8AAJ). The November 15, 2026 issue (read 2026-11-14) has on page 1 the parish's Hemlock Drive, Killingworth address, www.stlawrencechurch.com, "Rev. Joseph F. De Costa, Pastor" and its own Sunday and daily Mass boxes. Its text layer uses a font with shifted codes (each character 29 code points low, digits lost), so these words were read by decoding, not verbatim; no quote is stored.

## Worship sites

One church. The page 1 boxes give a Saturday Vigil, two Sunday morning Masses and daily Masses Tuesday evening and Wednesday to Saturday morning; the diocese's March 2026 list gives Saturday 4:00 pm, Sunday 8:30 and 10:30 a.m., Tuesday 7:00 p.m., Wednesday to Saturday 8:30 a.m., and the parish site's calendar (read 2026-11-14) shows the same times. The issue mentions St. Peter Church, Higganum only as another parish (CCD on Sundays, its Christmas Fair) and Sacred Heart on the Lake only for retreats.

## Website and bulletin provider

ParishesOnline, read by `provider_id`. St. Lawrence is yoked with St. Peter, Higganum (same pastor); the bulletins are separate (different containers and LPi ids, each 15 November 2026 masthead names only its own church; see `publication_reviews`).

## Not yet confirmed

Whether the pipeline can read Mass times from this container's text: the 15 November issue's text layer is in a shifted encoding with digits lost (see `research`). Download and identity are fine; extraction is the open question.
