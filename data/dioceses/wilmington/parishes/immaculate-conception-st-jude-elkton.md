---
name: Immaculate Conception, Elkton and St. Jude, North East
website: https://www.iccelkton.org/bulletins
bulletin_provider: other
provider_id: page-pdfs https://www.iccelkton.org/bulletins
publication: ['url:https://www.iccelkton.org/bulletins']
group: Iron Hill Deanery
evidence:
- url: https://irp.cdn-website.com/ba20104a/files/uploaded/10.25.2026-13a56019.pdf
  seen: 2026-10-27
  quote: Immaculate Conception Parish & St. Jude Mission Church
  note: 'Page 1 masthead of the 25 October 2026 issue (8 pages), Rev. Richard J. Jasper, Pastor. Masses:
    Saturday 5:00 pm, Sundays 7:00 and 11:00 am, weekdays Mon.-Sat. 8:30 am at 454 Bow Street, Elkton;
    Sundays 9:00 am at 928 Turkey Point Rd., North East. Names these two sites only; no mention of St.
    Thomas More or the Newman Center anywhere in the 7 text pages.'
- url: https://www.iccelkton.org/bulletins
  seen: 2026-10-27
  quote: At Immaculate Conception and St. Jude, our parish bulletins are your go-to source for the latest
    news
  note: The parish's own Duda page lists dated PDFs newest first (irp.cdn-website.com/ba20104a/files/uploaded/...,
    10.25.2026-13a56019.pdf the newest; weekly back to June 2025).
- url: https://thedialog.org/our-diocese/clergy-appointments-as-announced-may-19-by-bishop-koenig-in-the-diocese-of-wilmington/
  seen: 2026-10-27
  quote: The Reverend Richard J. Jasper is appointed Pastor of both Immaculate Conception, Elkton, and
    Saint Thomas More Oratory, Newark.
  note: Why a shared bulletin with the Newman Center was checked; it does not exist (see body).
promoted: 2026-10-27
---

## Publisher

Immaculate Conception, Elkton publishes one weekly bulletin on its own Duda site (https://www.iccelkton.org/bulletins), a page of dated PDFs. The 25 October 2026 masthead reads 'Immaculate Conception Parish & St. Jude Mission Church' and gives the schedules of both, so St. Jude, North East is covered by the same bulletin (one row, two churches), as the summer guide's 'mission of Immaculate Conception' says.

## Not shared with St. Thomas More

Fr. Richard Jasper has been pastor of both this parish and St. Thomas More Oratory (Newman Center, Newark) since June 2024, but the bulletin never mentions the Oratory (no match for 'Thomas More' or 'Newman' in the 25 October issue), and the Newman Center publishes a semester newsletter only. See `parishes/st-thomas-more-oratory-newark.md`.

## Website and bulletin provider

`other`, pinned `page-pdfs https://www.iccelkton.org/bulletins`. The old domain iccparish.org (GCatholic's website for both churches) did not load in the survey; the directory's iccelkton.org is current. The page lists only bulletin PDFs, so no filename filter is needed.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish immaculate-conception-st-jude-elkton` (2026-10-27): picked irp.cdn-website.com .../10.25.2026-13a56019.pdf, the newest on the page; transport ok, document type PDF, issue date observed, freshness fresh. Identity is reported unverified by the tool; the masthead read above settles it. The pin is already in `provider_id`.
