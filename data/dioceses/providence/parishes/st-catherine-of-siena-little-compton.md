---
name: St. Catherine of Siena
website: https://saintcatherinesiena.com/
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://saintcatherinesiena.com/']
group: ''
evidence:
- url: https://saintcatherinesiena.com/wp-content/uploads/2026/11/bulletin-11.15.26-thirty-third-sunday.doc
  seen: 2026-11-15
  note: '15 November 2026 bulletin, a Word 97 .doc (188,416 bytes; saved with tools/fetch_raw.py, read
    with tools/doc_text.py). Text: ''thirty-third sunday In ordinary time November 15, 2026 / MASS INTENTIONS
    / SAT – NOV 14th - 4:00 PM (ST. M) ... 4:00 PM (ST. C) ... SUN– NOV 15th - 8:00 AM (ST. C) ... 9:00
    AM (ST. M) ... 10:00 AM (ST. C) ...'', weekday 8:00 AM (ST. C) Monday-Friday; signed ''Fr. Stephan
    Silipigni''.'
- url: https://saintcatherinesiena.com/
  seen: 2026-11-15
  note: 'Parish WordPress site (drops probe url connections; read with parish-site-access visit.py): ''St.
    Catherine of Siena Parish, Little Compton, Rhode Island / St. Madeleine Sophie Chapel, Tiverton, Rhode
    Island / Reverend Stephan A. Silipigni''. Its menu item ''BULLETIN'' links the current issue directly
    as wp-content/uploads/2026/11/bulletin-11.15.26-thirty-third-sunday.doc.'
- url: https://saintcatherinesiena.com/mass-times/
  seen: 2026-11-15
  note: 'Mass Times page: St. Catherine (Little Compton) Saturday 4:00 pm (November 1, 2026 to March 14,
    2027), Sunday 8:00 am & 10:00 am; St. Madeleine Chapel (Tiverton) Saturday 4:00pm, Sunday 9:00am;
    daily Mass Monday-Friday 8:00 am (St. Catherine only).'
research:
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --diocese providence --parish
    st-catherine-of-siena-little-compton (provider other on https://saintcatherinesiena.com/)
  url: https://saintcatherinesiena.com/
  checked: '2026-11-15'
  outcome: unsupported-format
  next_action: Set a real provider and rerun fetch:check once a collector reads .doc bulletins, or once
    the parish posts PDFs
  retry_when: A Word-document collector lands, or the BULLETIN link points to a PDF
bulletin_status: unsupported-format
fetch_gap:
  kind: word-doc-bulletin
  seen: 2026-11-15
  note: 'The bulletin is posted only as a Word 97 .doc linked from the home page''s BULLETIN menu item
    (wp-content/uploads/YYYY/MM/bulletin-MM.DD.YY-<sunday>.doc). fetch:check on 2026-11-15 (other, from
    the website) followed that link and failed with ''Page.goto: Download is starting''; the pipeline
    downloader (tools/fetch_pdf.py) gets the file but refuses it as ''Not a PDF''. The text is readable
    (tools/doc_text.py).'
  url: https://saintcatherinesiena.com/wp-content/uploads/2026/11/bulletin-11.15.26-thirty-third-sunday.doc
---

## Publisher

St. Catherine of Siena, Little Compton publishes one weekly bulletin for itself and St. Madeleine Sophie, Tiverton, which merged into it on 24 January 2023 (finder 12164: "Saint Madeleine Sophie Parish merged into Saint Catherine of Siena Parish effective January 24, 2023"). The bulletin is a Word .doc linked from the site's BULLETIN menu item. The 15 November 2026 issue (https://saintcatherinesiena.com/wp-content/uploads/2026/11/bulletin-11.15.26-thirty-third-sunday.doc) is headed "thirty-third sunday / In ordinary time / November 15, 2026" and lists Mass intentions at both churches, "(ST. C)" and "(ST. M)": Saturday 4:00 PM at both, Sunday 8:00 AM (ST. C), 9:00 AM (ST. M), 10:00 AM (ST. C), weekdays 8:00 AM (ST. C). The pastor's letter is signed Fr. Stephan Silipigni.

## Worship sites

- St. Catherine of Siena, 74 Simmons Rd., Little Compton: Saturday 4:00 pm (5:00 pm from 21 March 2027), Sunday 8:00 and 10:00 am, Monday-Friday 8:00 am.
- St. Madeleine Sophie ("St. Madeleine Chapel"), 35 Lake Rd., Tiverton: Saturday 4:00 pm, Sunday 9:00 am.

The finder (12164, 12223) and GCatholic (22378, 22440) list these two and nothing else for the parish.

## Website and bulletin provider

The bulletin is posted only as a Word 97 .doc (wp-content/uploads/YYYY/MM/bulletin-MM.DD.YY-<sunday>.doc), linked from the home page's menu; no PDF version was found. The pipeline's downloader fetches the file but refuses it ("Not a PDF"), so the row is `unsupported` with fetch_gap `word-doc-bulletin` until a collector reads .doc files.

## Not yet confirmed

Nothing about the parish is open; the row waits for a collector that reads Word bulletins (see fetch_gap).
