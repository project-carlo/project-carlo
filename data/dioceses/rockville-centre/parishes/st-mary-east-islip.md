---
name: St. Mary & St. Peter the Apostle
website: https://www.stmaryei.org/bulletin/
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stmaryei.org/bulletin/']
group: ''
evidence:
- url: https://www.canva.com/design/DAHZaSMHVeM/LcQ_MDCfBTn0RiJD1Ij4MQ/view
  seen: 2026-11-13
  note: 'Canva design titled ''2026 Nov 8 - St. Mary''s & St. Peter''s'', 18 pages, opened from the stmaryei.org
    bulletin page''s ''11/8/26'' link (canva.link/wx0bzx46npq8h70). Page 1 masthead names ''The Catholic
    Churches of ST. MARY & ST. PETER THE APOSTLE'', ''EAST ISLIP & ISLIP TERRACE, NEW YORK'', ''NOVEMBER
    8, 2026''. Page 2 (screenshot): Church of Saint Mary, 20 Harrison Avenue, East Islip; St. Peter the
    Apostle Church, Church Address 70 Rockaway Street, Islip Terrace, NY 11752, Rectory/Mailing Address
    20 Harrison Ave; Mass at St. Mary Saturday 4:30 PM (Auditorium), Sunday 7:30 AM, 9 AM, 10:30 AM, 12
    PM, 5 PM, Monday to Friday 7:30 AM & 9 AM, Saturday 8:30 AM; Mass at St. Peter the Apostle Saturday
    5 PM, Sunday 8 AM & 10 AM, Monday, Tuesday, Thursday 8:30 AM, Saturday 8:30 AM. One pastoral staff
    (Rev. Anthony Iaconis, Pastor) for both.'
- url: https://www.stmaryei.org/bulletin/
  seen: 2026-11-13
  note: Bulletin page (read with visit.py; probe url could not connect) lists 'Current Bulletin 11/8/26'
    and past bulletins 11/1/26 back to 1/4/26; 7/12/26 onwards link canva.link short links, 7/5/26 and
    earlier link /wp-content/uploads/2026/MM/St.-Mary-Bulletin-<m>-<d>-<yy>.pdf.
- url: https://stpeterit.org/
  seen: 2026-11-13
  note: St. Peter the Apostle's site (same WordPress theme as stmaryei.org) links its bulletin to the
    same canva.link/wx0bzx46npq8h70 short link and its registration and faith formation pages to stmaryei.org.
research:
- method: 'Looked for a PDF copy of the Canva issues: stmaryei.org bulletin page and stpeterit.org home
    page'
  url: https://www.stmaryei.org/bulletin/
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Recheck the bulletin page for PDF links again, or use a Canva collector once one exists
  retry_when: The parish posts PDFs again or fetch gains a Canva viewer collector
bulletin_status: unsupported-format
fetch_gap:
  kind: canva-design-viewer
  seen: 2026-11-13
  url: https://canva.link/wx0bzx46npq8h70
  note: 'Since the 12 July 2026 issue the stmaryei.org /bulletin/ page links each week''s issue as a
    canva.link short link that opens a Canva design viewer (the 8 November 2026 issue: canva.com/design/DAHZaSMHVeM/.../view,
    18 pages), not a PDF; issues up to 5 July 2026 were WordPress PDFs (St.-Mary-Bulletin-<m>-<d>-<yy>.pdf).
    stpeterit.org links the same canva.link. Pages can only be read as screenshots (view#N). fetch:check
    on 2026-11-13 (provider other, unpinned) picked page-pdfs first-listed DRVC-Baptism-Confirmation-Sponsor-Form.pdf
    (2022), not a bulletin.'
---

## Publisher

The Catholic Churches of St. Mary (East Islip) and St. Peter the Apostle (Islip Terrace) publish one weekly bulletin. The 8 November 2026 issue, a Canva design titled "2026 Nov 8 - St. Mary's & St. Peter's" (18 pages, opened from `https://canva.link/wx0bzx46npq8h70` on 2026-11-13), has the masthead "The Catholic Churches of ST. MARY & ST. PETER THE APOSTLE", "EAST ISLIP & ISLIP TERRACE, NEW YORK". Page 2 gives one pastoral staff (Rev. Anthony Iaconis, Pastor; deacons marked St. Mary's or St. Peter's) and a Mass schedule for each church: St. Mary Saturday 4:30 PM (Auditorium), Sunday 7:30, 9, 10:30 AM, 12 and 5 PM (no 5 PM in July and August), Monday-Friday 7:30 and 9 AM, Saturday 8:30 AM; St. Peter the Apostle Saturday 5 PM, Sunday 8 and 10 AM, Monday, Tuesday, Thursday 8:30 AM, Saturday 8:30 AM.

## Worship sites

Two: St. Mary, 20 Harrison Avenue, East Islip (`st-mary-east-islip-church`) and St. Peter the Apostle, 70 Rockaway Street, Islip Terrace (`st-peter-the-apostle-islip-terrace-church`). The Saturday 4:30 PM Mass is in St. Mary's auditorium, part of the St. Mary campus, not a separate site. The diocese lists the two as separate parishes (locator 125 and 130); the bulletin decides the row.

## Website and bulletin provider

The locator's parishofstmary.org redirects to stmaryei.org (read with visit.py; `probe url` could not connect). Its `/bulletin/` page links each issue from 12 July 2026 onward to a canva.link short link opening a Canva design viewer; earlier 2026 issues were WordPress PDFs. St. Peter's own site, stpeterit.org (the locator's stpetersnyit.org no longer resolves), links the same short link. No PDF of the current issues was found, so the row is `unsupported` with `fetch_gap` `canva-design-viewer`.

## Not yet confirmed

Nothing about the structure. The row goes live only when the parish posts PDFs again or fetch can read Canva designs.
