---
name: St. Ann's Church
website: https://www.churchstann.org/bulletinnews/bulletin
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://www.churchstann.org/bulletinnews/bulletin']
group: St. Ann Parish, Emmaus
evidence:
- url: https://www.churchstann.org/s/20261018B.pdf
  seen: 2026-10-18
  quote: 7:30am, 9:00am*, 11:00am*
  note: 'Page 1 of the 18 October 2026 issue: MASS SCHEDULE Saturday 4:30pm (Vigil), Sunday 7:30am, 9:00am*,
    11:00am*, Weekday 8:00am* (Mon.-Sat.); footer "415 S. Sixth Street, Emmaus, PA 18049 | www.churchstann.org".'
- url: https://www.churchstann.org/bulletinnews/bulletin
  seen: 2026-10-18
  note: Squarespace bulletin page linking /s/YYYYMMDDB.pdf (LPi-style names, but self-hosted; no LPi id
    on the site) plus inserts cwb_MM-DD.pdf and pwb_MM-DD.pdf.
promoted: 2026-10-19
---

## Publisher

St. Ann, Emmaus, posts its own weekly bulletin on its Squarespace site. The 18 October
2026 issue gives Masses Saturday 4:30 pm, Sunday 7:30, 9 and 11 am, weekdays 8 am, all
at St. Ann's; no other church is named.

## Worship sites

- `st-ann-emmaus`, 500 block of Wood Street (the rectory is 415 S. Sixth Street).

## Website and bulletin provider

`other`, Squarespace. The bulletin is `/s/YYYYMMDDB.pdf`; the page also links two weekly
inserts (`cwb_`, `pwb_`), which are not the bulletin.

Fetch check (2026-10-19, `fetch_check` on a temporary CSV of these records): the resolver picked 20261018B.pdf ("current"), not the cwb/pwb inserts. Its recipe, `page-pdfs`, is recorded as `provider_id`.

## Not yet confirmed

Nothing.
