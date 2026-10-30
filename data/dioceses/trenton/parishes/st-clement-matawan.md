---
name: St. Clement Parish
website: https://stclementmatawan.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/church-of-saint-clement-matawan-nj-07747
publication: ['url:https://www.church-bulletin.org/church-of-saint-clement-matawan-nj-07747']
group: Cohort 14 (Keyport, Matawan, Union Beach, Holmdel)
evidence:
- url: https://www.church-bulletin.org/bulletin/church-of-saint-clement-matawan-nj-07747/2026-10-25.pdf
  seen: 2026-10-30
  quote: 'Mass Schedule: Saturday: 5:00PM | Sunday 8:00, & 11:00AM Daily Mass: Mon, Tues, Wed, Fri 8:00AM'
  note: '25 October 2026 issue (8 pages, text layer). Page 1 masthead: "Church of ST. CLEMENT, 172 Freneau
    Avenue Matawan, NJ 07747 (732)-566-3616 www.stclementmatawan.org"; staff list names "REV. THOMAS VALA,
    PASTOR". It names St. Clement alone, with no other church or parish. The 18 October and 1 November
    issues on the same listing are image-only (no text layer).'
- url: https://stclementmatawan.org/weekly-bulletins/
  seen: 2026-10-30
  quote: 'Click here to view our current bulletin: https://church-bulletin.org/677'
  note: 'The parish''s own Bulletins page sends readers to John Patrick listing 677; it carries no PDFs
    of its own. Its Mass schedule matches the bulletin (Saturday 5:00 PM; Sunday 8:00 AM, 11:00 AM; Monday,
    Tuesday, Wednesday and Friday 8:00 AM). Footer: ''Proudly Designed and Hosted by John Patrick Publishing
    Company''.'
- url: https://files.ecatholic.com/14277/documents/2024/7/2024%20July%20-%20Updated%20%20Parish%20Cohorts%20and%20Deaneries.pdf
  seen: 2026-10-30
  quote: Matawan
  note: 'July 2024 cohort list, Cohort 14: St. Benedict (Holmdel), St. Clement (Matawan), Our Lady of
    Fatima (Keyport), Holy Family (Union Beach). A cohort is not a shared bulletin; each of the four publishes
    its own (see the sibling rows).'
research:
- method: pnpm fetch:check --diocese trenton --parish st-clement-matawan (headed Chrome); page-pdfs on
    the church-bulletin.org listing
  url: https://www.church-bulletin.org/church-of-saint-clement-matawan-nj-07747
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: it picked the 1 November 2026 issue (coming Sunday, "future" freshness, the current
    issue); identity unverified because the check had no expected identity; the issue is image-only so
    the check read no text.'
bulletin_status: available
---

## Publisher

St. Clement Parish, Matawan (Cohort 14). It publishes its own weekly bulletin through John Patrick Publishing, listing 677 (`church-bulletin.org/church-of-saint-clement-matawan-nj-07747`, dated PDFs `/bulletin/<slug>/<yyyy-mm-dd>.pdf`, latest 1 November 2026). The 25 October 2026 issue's page 1 masthead names "Church of ST. CLEMENT, 172 Freneau Avenue Matawan" and the pastor Rev. Thomas Vala; nothing in it names Keyport, Holmdel or Union Beach. Pastor and masthead differ from Our Lady of Fatima's (Rev. Rene Pulgarin), so the cohort is not a shared bulletin.

## Worship sites

One church, St. Clement, 172 Freneau Avenue. GCatholic (18747) and the finder (14607) list the same place. The bulletin's Mass schedule gives one set of Masses and no mission or chapel. GCatholic's former Basilian monastery in Matawan is a different place in batch `eastern-catholic`.

## Website and bulletin provider

`fetch:check` (2026-10-30, headed Chrome) picked the 1 November 2026 issue, status ok.

stclementmatawan.org is a WordPress site hosted by John Patrick; its Bulletins page links listing 677. Row: `other` with `page-pdfs` on the listing. The 18 October and 1 November 2026 issues are image-only, so `fetch:check` passes them as a PDF with identity unverified; the 25 October issue is the text-layer read of the masthead.

## Not yet confirmed

Nothing outstanding. The 1 November issue's masthead was not rendered (image-only); the 25 October text issue and the unchanged site schedule were used.
