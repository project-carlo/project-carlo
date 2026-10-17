---
name: St. Therese and St. Frances X. Cabrini
website: https://stthereses-shavertown.com
bulletin_provider: other
provider_id: ''
publication: ['url:https://stthereses-shavertown.com/bulletins/', 'url:https://sfcbsp.org/bulletin-2/',
  'url:https://www.thebostonpilot.com/bcd/bulletinclick_AD_ED_Code.asp?ED_Code=32223']
group: Saint Therese Parish; Saint Frances X. Cabrini Parish (Carverton)
evidence:
- url: https://www.thebostonpilot.com/bcd/Bulletins/261011/32223_261011.pdf
  seen: 2026-10-16
  quote: A Publication of St. Therese and St. Frances X. Cabrini Churches
  note: 'Cover, page 1 of the 11 October 2026 issue (Pilot Bulletins, ED code 32223), with both churches''
    addresses: 64 Davis Street, Shavertown and 585 Mount Olivet Road, Wyoming.'
- url: https://www.thebostonpilot.com/bcd/Bulletins/261011/32223_261011.pdf
  seen: 2026-10-16
  quote: Rev. Joseph J. Pisaneschi
  note: 'Page 2 PASTORAL STAFF: one pastor and staff for both churches, with separate office hours for
    St. Therese and St. Frances Cabrini.'
- url: https://www.thebostonpilot.com/bcd/Bulletins/261011/32223_261011.pdf
  seen: 2026-10-16
  quote: 9:30AM (SFC) Nowell Young Hann
  note: 'Page 5 REMEMBERING (Mass intentions, 12-18 October): Mon, Wed, Thu, Fri 9:00AM (ST); Tue 9:00AM
    (SFC); Sat 4:00PM (SFC), 5:30PM (ST); Sun 8:00AM (ST), 9:30AM (SFC), 11:00AM (ST).'
- url: https://stthereses-shavertown.com/bulletins/
  seen: 2026-10-16
  note: St. Therese's Bulletins page (read in a browser; 403 to plain fetches) links thebostonpilot.com/bcd/bulletinclick_embed.asp?Id=32223_<YYMMDD>.pdf
    for each Sunday, 16 August to 11 October 2026.
- url: https://sfcbsp.org/bulletin-2/
  seen: 2026-10-16
  note: St. Frances X. Cabrini's Bulletin page (read in a browser) links the same Pilot ids, 32223_260802
    to 32223_261011. Its older /bulletin/ page lists self-hosted PDFs only up to 26 July 2026.
promoted: 2026-10-17
---

## Publisher

Saint Therese Parish (Shavertown) and Saint Frances X. Cabrini Parish (Carverton) are two canonical
parishes in the diocese's finder with one pastor, Rev. Joseph J. Pisaneschi, and one weekly bulletin
printed by Pilot Bulletins (ED code 32223). The 11 October 2026 issue's cover reads "A Publication of
St. Therese and St. Frances X. Cabrini Churches" and gives both churches; page 2 has one staff for
both; page 5's Mass intentions cover both, coded ST and SFC: weekdays 9 am (ST Monday, Wednesday,
Thursday, Friday; SFC Tuesday), Saturday 4 pm SFC and 5:30 pm ST, Sunday 8 am ST, 9:30 am SFC and
11 am ST. Both parish sites link the same Pilot issues.

## Worship sites

Two: `st-therese-shavertown` and `st-frances-x-cabrini-carverton`, the two churches on the cover
and in the intentions, and the finder's only worship sites for the two parishes. An outdoor Mass at
Frances Slocum State Park on 18 October is a one-off. The diocese's consolidated-parishes list gives
Blessed Sacrament Mission, Centermoreland, "closed 7/26/2009" under St. Frances X. Cabrini; it is in
no roster here.

## Website and bulletin provider

stthereses-shavertown.com is St. Therese's site (named on the cover) and the finder's website for
that parish; its Bulletins page links each issue at
`thebostonpilot.com/bcd/bulletinclick_embed.asp?Id=32223_<YYMMDD>.pdf`, which is an HTML page that
meta-refreshes to `Bulletin_embed.asp?BULLETINID=<YYMMDD>/32223_<YYMMDD>.pdf`, an Adobe-viewer page
whose PDF is `thebostonpilot.com/bcd/Bulletins/<YYMMDD>/32223_<YYMMDD>.pdf` (fetches without a
browser). sfcbsp.org's /bulletin-2/ page links the same. `bulletin_provider: other` with no recipe:
`fetch:check` reads only promoted rows, and the `other` resolver may not follow the Pilot embed
pages to the PDF. **This publisher (Pilot Bulletins, thebostonpilot.com/bcd) is new to the
dataset**; the PDF path is predictable from the date, so a small collector would read it reliably.

## Not yet confirmed

Whether the `other` resolver finds the PDF behind the Pilot embed links; run `fetch:check` after
promotion. The bulletin's site is behind a 403 for plain fetches.
