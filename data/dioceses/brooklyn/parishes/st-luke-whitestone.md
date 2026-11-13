---
name: St. Luke (Whitestone)
website: https://www.stlukewhitestone.org/
bulletin_provider: other
provider_id: page-pdfs https://www.stlukewhitestone.org/ filename=[0-9][0-9][0-9][0-9][0-9][0-9].pdf
publication: []
group: Deanery Q4 (Queens East)
evidence:
- url: https://www.stlukewhitestone.org/resources/2026-bulletins/110126.pdf
  seen: 2026-11-05
  quote: 16-34 Clintonville Street | Whitestone, New York 11357
  note: 1 November 2026 issue ('NOVEMBER 1, 2026'), 16 pages, pages 2-14 images. Page 1 masthead 'ST.
    LUKE ROMAN CATHOLIC CHURCH', Pastor Very Rev. John J. Costello, V.E.; 'Saturday Vigil 4:30pm | Sunday
    8:30am (Italian/English), 10:30am,12:30pm,4:30pm', daily 'Monday to Friday 12 Noon | Saturday 8:30am'.
    No other church or chapel is named.
- url: https://www.stlukewhitestone.org/
  seen: 2026-11-05
  note: Homepage link 'This Week's Bulletin' points to resources/2026-bulletins/110126.pdf; it also links
    the Bulletin Archive and a Parish-Census-Form.pdf.
- url: https://www.stlukewhitestone.org/news_and_events/bulletin_archive.html
  seen: 2026-11-05
  note: 'Bulletin Archive: weekly PDFs named MMDDYY.pdf under resources/<year>-bulletins/, laid out by
    year in a table that is not newest first (2024-2026).'
promoted: 2026-11-12
research:
- method: fetch:check with recipe 'page-pdfs https://www.stlukewhitestone.org/ filename=[0-9][0-9][0-9][0-9][0-9][0-9].pdf';
    picked 110126.pdf (1 November 2026) on Thursday 5 November, before the 8 November issue was posted;
    freshness unknown because fetch cannot date MMDDYY file names
  url: https://www.stlukewhitestone.org/
  checked: '2026-11-05'
  outcome: found
  next_action: Rerun fetch:check and confirm it picks 110826.pdf (the 8 November issue)
  retry_when: After the weekend of 7-8 November 2026
  revisit_after: 2026-11-09
---

## Publisher

St. Luke publishes its own weekly bulletin as PDFs on its site (`resources/<year>-bulletins/MMDDYY.pdf`). The 1 November 2026 issue (read 2026-11-05, the latest posted) has a text page 1 whose masthead reads "ST. LUKE ROMAN CATHOLIC CHURCH / 16-34 Clintonville Street | Whitestone, New York 11357", Pastor Very Rev. John J. Costello, V.E. Pages 2-14 are images.

## Worship sites

One church. Page 1 gives "Saturday Vigil 4:30pm | Sunday 8:30am (Italian/English), 10:30am,12:30pm,4:30pm" and daily Masses Monday-Friday 12 Noon and Saturday 8:30am, with extra school-day Masses ("Tuesday and Thursday when school is in session", First Friday 8:30AM), and names no other church or chapel. St. Luke School (16-01 Msgr. Dillon Place) is a school, not a separate listed Mass site. The diocese directory, deanery list, GCatholic 16800 and Mass finder 1149 list only this church.

## Website and bulletin provider

`other`, pinned to the homepage's "This Week's Bulletin" link: `page-pdfs https://www.stlukewhitestone.org/ filename=[0-9][0-9][0-9][0-9][0-9][0-9].pdf`. The filter keeps the six-digit MMDDYY issue file and drops Parish-Census-Form.pdf. The unpinned resolver followed the Bulletin Archive, whose table is not newest first, and wrongly picked `2024-bulletins/111024.pdf` (10 November 2024) as current.

## Not yet confirmed

The pinned pick on 2026-11-05 was the 1 November issue because the 8 November file was not yet posted, and fetch cannot date the MMDDYY names, so it reports freshness as unknown. A recheck after 8 November should show it picking 110826.pdf (see research).
