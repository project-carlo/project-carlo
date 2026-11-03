---
name: St. Edward the Confessor and Our Lady of Victories
website: https://stedolv.org
bulletin_provider: other
provider_id: page-pdfs https://stedolv.org/weekly-bulletin
publication: ['url:https://stedolv.org/weekly-bulletin']
group: ''
evidence:
- url: https://stedolv.org/images/bulletin/bulletin110126.pdf
  seen: 2026-11-02
  note: '1 November 2026 issue, 6 pages; its text layer uses a shifted font encoding (pdftotext output
    is unreadable without shifting each character by 29), so I rendered page 1. The masthead reads ''We,
    the Parishes of St. Edward the Confessor & Our Lady of Victories, have as our mission …'' and gives
    two columns: St. Edward the Confessor Roman Catholic Church, 61 Mill Street, Milford NJ 08848 (Saturday
    4:00pm, Sunday 8:00 & 10:00am, Monday-Thursday 9:00am) and Our Lady of Victories Roman Catholic Church,
    1005 County Rd. 519, Frenchtown NJ 08825 (Saturday 5:15pm, Sunday 9:00 & 11:00am, Monday-Thursday
    8:00am); both list ''Fr. Bede Kim, Pastor'' and the website stedolv.org.'
- url: https://stedolv.org/weekly-bulletin
  seen: 2026-11-02
  note: '''Weekly Bulletin - St. Edward the Confessor and Our Lady of Victories'': one list of weekly
    PDFs /images/bulletin/bulletin<MMDDYY>.pdf, newest ''November 1, 2026'', back to March 2024.'
- url: https://stedolv.org/welcome-our-lady-of-victories
  seen: 2026-11-02
  quote: 1005 County Road 519, Frenchtown, NJ 08825 Mass Schedule Saturday at 5:15 PM
  note: The joint site's footer reads '© 2026 The Parishes of St. Edward the Confessor and Our Lady of
    Victories'.
bulletin_status: available
---

## Publisher

St. Edward the Confessor, Milford, and Our Lady of Victories, Frenchtown (Baptistown), two parishes under one pastor, publish one weekly bulletin on their joint site stedolv.org. The 1 November 2026 issue (read 2026-11-02 by rendering page 1, since the text layer is in a shifted font encoding) opens 'We, the Parishes of St. Edward the Confessor & Our Lady of Victories' and gives each church's address, Mass schedule and staff side by side, both under 'Fr. Bede Kim, Pastor' (as the parish finder lists for both). It is one document for both canonical parishes, so one row, as the batch note anticipated.

## Worship sites

Two churches, each named with its Mass schedule in the masthead: St. Edward the Confessor, 61 Mill Street, Milford (directory:24507, gcatholic:18647) and Our Lady of Victories, 1005 County Road 519, Frenchtown (directory:24466, gcatholic:18627). The finder lists no other worship site for either, and the masthead names none.

## Website and bulletin provider

Neither finder entry gives a website. GCatholic gives `stedwardmilford.parishesonline.com` for St. Edward, which does not resolve, and no ParishesOnline org was found under the usual slug forms (`st-edward-the-confessor-church-08848` and others, 2026-11-02). A browser search for the parishes on DuckDuckGo found https://stedolv.org, which the bulletin masthead prints as both parishes' website. `probe url` said DEAD-DNS, but `probe get` and `visit.py` loaded it (the playbook's warning). Its Weekly Bulletin page lists self-hosted PDFs by Sunday date, so provider `other`.

## Not yet confirmed

Nothing about the publisher. Because pdftotext output is unreadable, recheck quotes come from the parish site's pages.

## Fetch check

`pnpm fetch:check` on 2026-11-02 (US Eastern) resolved `page-pdfs on https://stedolv.org/weekly-bulletin: current` and picked `images/bulletin/bulletin110126.pdf`: transport ok, PDF, identity unverified, issue date and freshness `unknown` ('No unambiguous issue date in inspected masthead or selected URL filename': the file names are MMDDYY and the text layer is in a shifted font). That is the 1 November 2026 issue whose page 1 I rendered and read, the newest on the page. Recipe recorded: `page-pdfs https://stedolv.org/weekly-bulletin`. The file names are not reliable dates (the 'June 14, 2026' link is `bulletin071426.pdf`, 'January 4, 2026' is `bulletin010425.pdf`), so the page order, not the name, gives the newest issue.
