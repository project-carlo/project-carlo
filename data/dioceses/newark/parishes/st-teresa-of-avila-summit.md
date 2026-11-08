---
name: St. Teresa of Avila Parish, Summit
website: https://www.st-teresa.org/
bulletin_provider: other
provider_id: page-pdfs https://www.st-teresa.org/
publication: ['url:https://www.st-teresa.org/#sunday-bulletin']
group: ''
evidence:
- url: https://www.st-teresa.org/_files/ugd/b2c90c_4a1ba061e9674da88056e78e733d25bc.pdf
  seen: 2026-11-05
  quote: 306 Morris Avenue, Summit , NJ 07901
  note: '1 November 2026 issue (10 pages, 8 with text). Page 1 masthead ''St Teresa of Avila est. 1863'',
    ''November 1, 2026 Solemnity of All Saints'', Fall Mass Schedule: Daily 7:00 am Church; Saturday 8:30
    am Church, 4:00 pm (Vigil) Memorial Hall; Sunday 7:30 am Church, 9:00 am (Family) Memorial Hall, 10:30
    am Church, 12:00 pm (Spanish) Church, 5:00 pm Church. No printer footer: produced by the parish.'
- url: https://www.st-teresa.org/
  seen: 2026-11-05
  note: 'Wix homepage (probe get): the ''Sunday Bulletin November 1, 2026'' link is the first _files/ugd/
    PDF on the page (b2c90c_4a1ba061...pdf); the other 13 ugd PDFs are flyers and reports (e.g. ''2025-2026
    Fiscal Year'').'
promoted: 2026-11-05
research:
- method: fetch:check page-pdfs first-listed on the Wix homepage; undated _files/ugd/ names give freshness
    unknown
  url: https://www.st-teresa.org/
  checked: '2026-11-05'
  outcome: found
  next_action: Confirm the first-listed homepage PDF is still the newest 'Sunday Bulletin' (date on page
    1)
  retry_when: Next fetch review, or when fetch:check picks a PDF whose page 1 is not a bulletin
  revisit_after: 2026-12-05
bulletin_status: available
---

## Publisher

St. Teresa of Avila Parish, Summit, produces its own weekly bulletin and posts it on its Wix homepage under 'Sunday Bulletin'. I read the 1 November 2026 issue: page 1 masthead '306 Morris Avenue, Summit , NJ 07901 / St Teresa of Avila / est. 1863', dated 'November 1, 2026 Solemnity of All Saints', with one Fall Mass Schedule for the church and Memorial Hall. No John Patrick, LPi or Bon Venture footer appears in the text layer.

## Worship sites

- St. Teresa of Avila Church, 306 Morris Avenue (`st-teresa-of-avila-summit`): daily 7:00 am; Saturday 8:30 am, 4:00 pm Vigil (in Memorial Hall); Sunday 7:30, 9:00 (Family, Memorial Hall), 10:30, 12:00 pm Spanish, 5:00 pm. Memorial Hall is on the parish campus and is not recorded as a separate church.

The directory (192) and GCatholic (18560) list only this church. GCatholic's Rosary Shrine (33105, the Dominican nuns' monastery on Springfield Avenue, Summit) is not in this bulletin's schedule; it has its own record (`rosary-shrine-summit`).

## Website and bulletin provider

The directory gives https://www.st-teresa.org/; GCatholic still gives the old http://www.stteresachurch.org. The bulletin is linked from the homepage as an undated Wix `_files/ugd/` upload, labelled 'Sunday Bulletin November 1, 2026'; it is the first PDF on the page, ahead of 13 flyers and reports.

Fetch check (2026-11-05, headed): transport ok, PDF, resolved `page-pdfs on https://www.st-teresa.org/: first-listed` and picked `_files/ugd/b2c90c_4a1ba061e9674da88056e78e733d25bc.pdf`, the 1 November 2026 issue read above (current on 5 November). Issue date and freshness `unknown` because the file name is undated and the check found no date it trusts; page 1 reads 'November 1, 2026'. The recipe is the one in `provider_id`.

## Not yet confirmed

Freshness is `unknown` by construction (undated Wix names): research asks for a recheck that the first-listed PDF is still the newest bulletin. The task notes a temporary administrator to February 2027; the 1 November text layer does not name the clergy, so it is not recorded here.
