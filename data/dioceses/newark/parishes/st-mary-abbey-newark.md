---
name: St. Mary's Church at Newark Abbey, Newark
website: https://www.smcnewark.org/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.canva.com/design/DAGov7FvS1o']
group: ''
evidence:
- url: https://www.canva.com/design/DAGov7FvS1o/n-0xWu7Cxg86CuvONsTzHA/view
  seen: 2026-11-04
  note: 'Read with visit.py --text (title "St. Mary''s Church Bulletin"). Page 1: ''Weekly Bulletin /
    ST. MARY''S CHURCH / OCTOBER 25, 2026 / WWW.SMCNEWARK.ORG / 973-792-5793'', message from the rector,
    signed ''Fr. Patrick, O.S.B.''. Page 3 (#3): ''Mass Schedule / St. Mary''s Church / at NEWARK ABBEY
    / 528 Dr. Martin Luther King Jr. Blvd''; ''Sunday: 7:30 AM, 10:00 AM, 5:00 PM / Monday to Friday:
    12:15 PM / Saturday: 8:45 AM''. Page 4: ''NEW DAILY MASS SCHEDULE: The 12:15 Mass is now the Conventual
    Mass for the monastic community. All are welcome to attend! This will be the only Mass celebrated
    in the Church. The 5pm Mass is no longer offered.'' One church.'
- url: https://www.smcnewark.org/bulletin
  seen: 2026-11-04
  note: 'Wix page (visit.py): "This Week''s Bulletin 12/15/2025 ... Click Here" links the Canva design
    above; ''Past Bulletins'' link _files/ugd PDFs labelled 11/30, 11/23, 11/16 and 11/9 (2025). The 11/30
    PDF (f6fd2f_fd283318ae14410087b3a0242328edf2.pdf, 8 pages, text) is headed ''ST. MARY''S CHURCH NOVEMBER
    30, 2025 WWW.SMCNEWARK.ORG'', the same layout as the Canva issue.'
- url: https://parishesonline.com/organization/st-mary-church-07102
  seen: 2026-11-04
  note: 'probe po: org ''St. Mary Church'', 528 Martin Luther King Jr Blvd, Newark, New Jersey, 07102-1314,
    with no issues (latest_issue empty). Not this bulletin''s publisher now.'
research:
- method: probe po on guessed ParishesOnline slugs; grep of the John Patrick scans (029-map/jp-*.tsv)
    for 07102
  checked: '2026-11-04'
  outcome: not-found
  next_action: Look again for a PDF edition (a Wix _files/ugd upload, a John Patrick or LPi listing) that
    a collector could read
  retry_when: The bulletin page links a PDF dated within two weeks, or a collector for Canva designs exists
bulletin_status: unsupported-format
fetch_gap:
  kind: canva-design-viewer
  seen: 2026-11-04
  note: 'The bulletin page''s ''This Week''s Bulletin ... Click Here'' opens a Canva design (canva.com/design/DAGov7FvS1o/.../view)
    that the parish edits each week: on 2026-11-04 it showed the 25 October 2026 issue, 8 pages, readable
    only in Canva''s JavaScript viewer (pages addressed as #1..#8). No PDF is linked; the Wix PDFs on
    the same page stop at 30 November 2025.'
  url: https://www.canva.com/design/DAGov7FvS1o/n-0xWu7Cxg86CuvONsTzHA/view
---

## Publisher

St. Mary's Church at Newark Abbey, the Benedictine abbey church, publishes its own weekly bulletin, designed in Canva. The bulletin page of https://www.smcnewark.org/ links 'This Week's Bulletin' to one Canva design that is updated each week. On 2026-11-04 it showed the 25 October 2026 issue (8 pages): page 1 'Weekly Bulletin / ST. MARY'S CHURCH / OCTOBER 25, 2026 / WWW.SMCNEWARK.ORG', the rector's message signed 'Fr. Patrick, O.S.B.'; page 3 'Mass Schedule / St. Mary's Church / at NEWARK ABBEY / 528 Dr. Martin Luther King Jr. Blvd'. No printer is named.

## Worship sites

- St. Mary's Church, 528 Dr. Martin Luther King Jr. Blvd (`st-mary-abbey-newark`): Sunday 7:30 AM, 10:00 AM, 5:00 PM; Saturday 8:45 AM; Monday-Friday 12:15 PM, the abbey's Conventual Mass, 'the only Mass celebrated in the Church' on weekdays (pages 3-4, 25 October 2026).

The directory (276) and GCatholic (18509, 'Abbey Church', qualifier Monastery) both list this church. GCatholic's 'Former Church of St. Joseph' on West Market Street (38882), which the survey grouped here, is closed and is now a restaurant (`excluded/st-joseph-former-church-newark`); the bulletin does not mention it.

## Website and bulletin provider

The Wix site's PDFs (_files/ugd, 32-hex names) stop at the 30 November 2025 issue, and the label still reads 'This Week's Bulletin 12/15/2025'. Since then the current issue lives only in the Canva viewer, which `fetch` can't read (no PDF; pages render in JavaScript). So the row is `unsupported` with fetch_gap `canva-design-viewer`, and the Canva design id is its `publication`. A ParishesOnline org `st-mary-church-07102` exists for this address but has no issues. fetch:check (2026-11-04) refuses the row: "unsupported, so fetch has no collector for it".

## Not yet confirmed

Whether a PDF edition exists anywhere else (Facebook, a publisher listing): see research. The page 4 note about the 5pm Mass refers to weekdays; the page 3 schedule still gives Sunday 5:00 PM, and the note says 'The Sunday Mass schedule will remain the same'.
