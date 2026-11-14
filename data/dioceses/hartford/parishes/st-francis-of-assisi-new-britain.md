---
name: St. Francis of Assisi Parish
website: https://stfranciscatholic.org/bulletins/
bulletin_provider: other
provider_id: page-pdfs
publication: []
group: ''
evidence:
- url: https://cdn.diocesanweb.org/beacon/francisnb/wp-content/uploads/2026/11/SFC-The-Bulletin-October-25-2026.pdf
  seen: 2026-11-13
  quote: St. Joseph and St. Peter Churches are no longer used for regular Masses.
  note: 'Page 2 of the 25 October - 7 November 2026 issue (''The Bulletin'', St. Francis Catholic, 15
    pages, text layer): Mass times Saturday Vigil 4:00 pm St. Jerome, Sunday 8:30 am St. Maurice, Sunday
    10:30 am St. Francis, daily Monday-Saturday 8:00 am and Wednesday 6:00 pm all at St. Francis; ''Our
    Parish Churches'' lists St. Jerome 1010 Slater Road, St. Francis 1755 Stanley Street, St. Maurice
    100 Wightman Road, St. Joseph* 195 S. Main Street, St. Peter* 98 Franklin Square.'
- url: https://stfranciscatholic.org/bulletins/
  seen: 2026-11-13
  note: The Bulletins page links fortnightly diocesanweb uploads named SFC-The-Bulletin-<Month>-<D>-<YYYY>*.pdf,
    newest first (SFC-The-Bulletin-October-25-2026.pdf, then October-11-2026), back to December 21, 2025;
    no other PDFs on the page.
- url: https://www.courant.com/2021/12/01/deeper-not-wider-as-new-britain-loses-several-catholic-churches-rev-michael-casey-sees-small-but-intentional-community-growing-together/
  seen: 2026-11-13
  quote: Members of St. Maurice, St. Andrew and St. Peter are being invited to Masses there; their churches
    will be available for weddings and funerals for now, but most likely will be sold to reduce the costs
    of maintenance and repairs.
  note: 'Hartford Courant, 1 December 2021: from January 2022 St. Jerome, St. John, St. Joseph and St.
    Francis of Assisi remain parish churches under Rev. Michael Casey. The 2026 schedule has since changed
    (St. Maurice has a Sunday Mass again; St. John and St. Joseph do not).'
revisit: Rerun fetch:check once the 8 November 2026 issue is uploaded; confirm it picks it (the page lags
  the fortnightly issue date).
revisit_after: 2026-11-27
bulletin_status: available
---

## Publisher

St. Francis of Assisi Parish, New Britain ("St. Francis Catholic") publishes "The Bulletin" every two weeks. The issue read is 25 October - 7 November 2026 (`SFC-The-Bulletin-October-25-2026.pdf`, uploaded to the parish's diocesanweb site); page 2 is the masthead page: "Welcome to Saint Francis Catholic", Mass, confession and adoration times, and "Our Parish Churches".

## Worship sites

Three, from page 2 of the 25 October 2026 issue: St. Jerome, 1010 Slater Road (Saturday Vigil 4:00 pm; `st-jerome-new-britain`), St. Maurice, 100 Wightman Road (Sunday 8:30 am; `st-maurice-new-britain`) and St. Francis, 1755 Stanley Street (Sunday 10:30 am and all weekday Masses; `st-francis-of-assisi-new-britain`).

Ruled out:

- St. Joseph, 195 S. Main Street and St. Peter, 98 Franklin Square: the same page lists them among the parish churches with "*St. Joseph and St. Peter Churches are no longer used for regular Masses." They are `excluded/st-joseph-new-britain` (Sunday Masses ended in April 2024) and `excluded/st-peter-new-britain` (regular Masses ended in 2022; condemned after earthquake damage in 2025).
- St. Andrew, 396 Church St. (GCatholic 22131): regular Masses ended in January 2022 (Hartford Courant, 1 December 2021) and the church was later sold; `excluded/st-andrew-new-britain`.
- St. John the Evangelist, 655 East St. (GCatholic 22135): still a parish church in January 2022, absent from every 2025-2026 issue's church list and on sale as a religious facility, but no source found says when its Masses ended; `open/st-john-the-evangelist-new-britain`.

The directory's five St. Francis entries (28, 48, 46, 45, 27) are these five buildings. The 2017 plan (Hartford Courant, 7 May 2017) merged St. Jerome and St. Maurice into St. Katharine Drexel, St. Andrew and St. John into Holy Apostles, and St. Joseph and St. Peter into Divine Providence; the archdiocese's January 2026 closed-parish list gives all three as closed in 2022, the year they were folded into St. Francis.

## Website and bulletin provider

`other`, recipe `page-pdfs` (printed by `fetch:check` on 2026-11-13). It read the Bulletins page and picked `SFC-The-Bulletin-October-25-2026.pdf`, the newest issue posted (dated 2026-10-25 from the file name). Transport and PDF signature passed. Freshness was 'stale' (19 days against a 14-day limit) because the fortnightly issue for 8 November had not been uploaded yet, and identity was not inspected because the PDF is over 25 MB. The page links only the parish's own `SFC-The-Bulletin-*` files, so no filename filter is needed.

## Not yet confirmed

Nothing open for the row. The next fortnightly issue (8 November 2026) was not yet uploaded on 13 November. `revisit_after` asks for a fetch:check rerun once it is.
