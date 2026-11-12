---
name: Resurrection Ascension - Our Lady of the Angelus (Rego Park)
website: https://www.rachurch.net/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:24728', 'ecatholic:29323']
group: Deanery Q6 (Queens West)
evidence:
- url: https://files.ecatholic.com/24728/bulletins/20261101.pdf
  seen: 2026-11-06
  quote: RESURRECTION ASCENSION — OUR LADY OF THE ANGELUS PARISH
  note: '1 November 2026 issue (15 pages) on the Resurrection-Ascension eCatholic site 24728. Page 1 masthead
    names the parish and two churches with their own Mass schedules: R.A. Roman Catholic Church, 85-25
    61st Road, Rego Park (Mon-Sat 9am; Sat vigil 4:00pm; Sunday 9:30am, 11:00am, 12:30pm Spanish) and
    O.L.A. Roman Catholic Church, 63-63 98th Street, Rego Park (Mon-Fri 12pm, Thursday 7:30pm, Sat 9am;
    Sat vigil 5:30pm; Sunday 9:30am, 11:00am Spanish, 12:30pm), ''Two locations, one Rego Park Catholic
    parish family''.'
- url: https://files.ecatholic.com/29323/bulletins/20261101.pdf
  seen: 2026-11-06
  quote: Two locations, one Rego Park Catholic parish family
  note: 'The Our Lady of the Angelus eCatholic site (www.olaqueens.org, ecatholic:29323) posts the same
    1 November 2026 issue: 15 pages, the same page 1 masthead naming both churches. Neither site had an
    8 November file on 2026-11-06 (403).'
- url: https://files.ecatholic.com/24728/bulletins/20261101.pdf
  seen: 2026-11-06
  quote: 'RA-OLA Goal:'
  note: Page 13 lists both rectories (R.A. office at 61-11 85th Street; O.L.A. at 63-63 98th Street, www.olaqueens.org)
    and the Annual Catholic Appeal is reported for RA-OLA together.
- url: https://dioceseofbrooklyn.org/parish-merger-decree-resurrection-ascension-our-lady-of-the-angelus/
  seen: 2026-11-05
  note: 'Survey: the diocese posted the merger decree on 2025-09-10, effective 2023-01-01, keeping two
    churches for worship. Not read by this job; the row rests on the bulletin, not the decree.'
- url: https://www.rachurch.net/
  seen: 2026-11-06
  note: 'Resurrection-Ascension Parish site (403 to probe url; read with parish-site-access visit.py):
    eCatholic site 24728, bulletins at /bulletins.'
research:
- method: fetch:check (headed Chrome), ecatholic from https://www.rachurch.net/
  url: https://www.rachurch.net/bulletins
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check after 8 November and confirm it picks that issue
  retry_when: files.ecatholic.com/24728/bulletins/20261108.pdf is posted
  revisit_after: 2026-11-09
- method: 'Reconcile: headed fetch:check of every Brooklyn row'
  url: https://files.ecatholic.com/24728/bulletins/20261108.pdf?t=1793983192000
  checked: '2026-11-12'
  outcome: found
  next_action: 'None: the pick is the 8 November 2026 issue (files.ecatholic.com/24728/bulletins/20261108.pdf).'
bulletin_status: available
---

## Publisher

The merged parish of Resurrection Ascension and Our Lady of the Angelus publishes one weekly bulletin on eCatholic. The 1 November 2026 issue (read 2026-11-06, 15 pages) is headed "RESURRECTION ASCENSION — OUR LADY OF THE ANGELUS PARISH" and gives the two churches' Mass schedules side by side, "Two locations, one Rego Park Catholic parish family". The same file is posted on both parish sites: www.rachurch.net (eCatholic 24728) and www.olaqueens.org (eCatholic 29323), each 15 pages with the same masthead.

## Worship sites

Two, both in the 1 November masthead: R.A. Roman Catholic Church, 85-25 61st Road (`resurrection-ascension-rego-park`), and O.L.A. Roman Catholic Church, 63-63 98th Street (`our-lady-of-the-angelus-rego-park`). The diocese's merger decree (posted 2025-09-10, effective 2023-01-01) keeps both as churches, but the diocese directory, deanery list, GCatholic and the Mass finder still list them as separate parishes; those entries are linked to the two church records. Following the settled rule, this is one row because the current bulletin covers both churches. The bulletin also lists monthly Indonesian (second Sunday 2 pm) and Filipino (third Sunday 3 pm) Masses on the R.A. page, and a Monday Spanish Lectio Divina in the "Chapel at Trinity Center", a parish building, not a separate Mass site.

## Website and bulletin provider

`ecatholic`, read from the Resurrection-Ascension eCatholic site www.rachurch.net (24728). Both eCatholic site ids are recorded as publication ids because each site posts this same bulletin, so no second row can claim the OLA copy.

## Not yet confirmed

The 8 November 2026 file was not yet posted on 2026-11-06; see research.
