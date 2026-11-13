---
name: St. Aloysius Parish
website: https://starcc.com/
bulletin_provider: other
provider_id: page-pdfs https://starcc.com/
publication: ['url:https://starcc.com/weekly-bulletins/#st-aloysius-new-canaan']
group: ''
evidence:
- url: https://starcc.com/wp-content/uploads/dlm_uploads/2026/11/11-15-26-final.pdf
  seen: 2026-11-12
  quote: Thirty-Third Sunday in Ordinary Time - November 15, 2026
  note: 'Page 1 of the 15 November 2026 issue: ''New Canaan, Connecticut'', ''www.starcc.com'', ''Msgr.
    Robert M. Kinnally, Pastor''. Sunday Masses: Saturday Vigil 5:00 p.m.; Sunday 7:00, 8:30, 10:00, 11:30
    a.m. and 5:00 p.m. Weekday: Monday-Friday 7:00 a.m. and 5:30 p.m.; Saturday 7:00 a.m. Parish office
    40 Maple St. Page footers ''St. Aloysius Church, New Canaan, CT''.'
- url: https://starcc.com/weekly-bulletins/
  seen: 2026-11-12
  note: WordPress Weekly Bulletins page lists issues newest first as Download Monitor links (https://starcc.com/download/10317/,
    10259, 10193 ...); /download/10317/ redirects to the 15 November PDF at wp-content/uploads/dlm_uploads/2026/11/11-15-26-final.pdf.
- url: https://parishesonline.com/organization/st-aloysius-church-06840
  seen: 2026-11-12
  note: 'probe po: a ParishesOnline org ''St. Aloysius Church'' (LPi 0018000000Qc096AAB) exists but lists
    no issues, and the bulletin carries no LPi footer or container number; not recorded as this bulletin''s
    publication.'
revisit: 'Rerun fetch:check: the pinned recipe depends on the home page linking the newest bulletin PDF
  directly; if it stops, the Weekly Bulletins page''s Download Monitor links (/download/<id>/) are not
  read by page-pdfs and the row needs a fetch_gap'
revisit_after: 2027-01-15
promoted: 2026-11-12
bulletin_status: available
---

## Publisher

The parish posts its own weekly bulletin on its WordPress site. The 15 November 2026 issue (`https://starcc.com/wp-content/uploads/dlm_uploads/2026/11/11-15-26-final.pdf`, read 2026-11-12) has on page 1 "New Canaan, Connecticut", "www.starcc.com", "Thirty-Third Sunday in Ordinary Time - November 15, 2026" and "Msgr. Robert M. Kinnally, Pastor"; its pages are footed "St. Aloysius Church, New Canaan, CT".

## Worship sites

- `st-aloysius-new-canaan`: Saturday Vigil 5:00 p.m.; Sunday 7:00, 8:30, 10:00, 11:30 a.m. and 5:00 p.m. (the directory's "Teen Mass" note is the Sunday 5:00 p.m. in the diocese's mass-times API); Monday-Friday 7:00 a.m. and 5:30 p.m.; Saturday 7:00 a.m.

The bulletin mentions a "Chapel" for Saturday confessions and Friday adoration, with no Mass listed there; I took it as part of the church and gave it no row. The diocese's directory (directory:1397) and GCatholic (21971) list this one church.

## Website and bulletin provider

`starcc.com` is WordPress with the Download Monitor plugin: the Weekly Bulletins page (`https://starcc.com/weekly-bulletins/`) links each issue as `https://starcc.com/download/<id>/`, which redirects to `wp-content/uploads/dlm_uploads/<YYYY>/<MM>/<MM-DD-YY>-final.pdf`. The home page links the newest PDF directly. A ParishesOnline org for the church exists with no issues, and the bulletin has no LPi footer, so provider `other`.

`fetch:check` on 2026-11-12 (headed Chrome): with the Weekly Bulletins page as website it failed ("No PDF links found on bulletin page": page-pdfs doesn't follow `/download/<id>/` links), and unpinned from the home page it wandered into `bulletin_board` posts and failed. Pinned as `page-pdfs https://starcc.com/` it picked `https://starcc.com/wp-content/uploads/dlm_uploads/2026/11/11-15-26-final.pdf`, the 15 November 2026 issue read above (freshness `future`, checked the Thursday before). The website is therefore the home page and the recipe is pinned on it; the revisit checks it still links each new issue.

## Not yet confirmed

Nothing open.
