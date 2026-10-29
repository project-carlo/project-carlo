---
name: St. Michael Parish
website: https://www.church-bulletin.org/saint-michael-s-parish-philadelphia-pa-19122
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-michael-s-parish-philadelphia-pa-19122
publication: ['url:https://www.church-bulletin.org/saint-michael-s-parish-philadelphia-pa-19122']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-michael-s-parish-philadelphia-pa-19122
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 214, 'Saint Michael's Parish', 1445 North Second Street, Philadelphia PA
    19122, phone (215) 739-2358; newest dated issue October 25, 2026, weekly back through at least November
    2024.
- url: https://www.church-bulletin.org/bulletin/saint-michael-s-parish-philadelphia-pa-19122/2026-10-25.pdf
  seen: 2026-10-29
  note: 'The 25 October 2026 issue (6 pages, text layer, md5 1cbafdcb...): page 1 masthead ''SAINT MICHAEL''S
    PARISH, FOUNDED 1831, Rev. Fernando Londono, Parochial Administrator, 1445 North Second Street'';
    Sunday Mass 9:30 am English and 11:30 am Spanish, daily Mass Mon-Fri 8:30 a.m., confessions Sunday
    10:30-11:20 and Thursday 5-6:30 pm, exposition Thursday after Mass. The word ''Immaculate'' does not
    occur anywhere in the issue and no second church or address is named.'
- url: https://stmichaelsphiladelphia.com/
  seen: 2026-10-29
  note: 'The directory''s website. probe url: SSLCertVerificationError, certificate has expired; visit.py
    over https and http: ERROR (no page loaded). Not usable as the row''s website, so the John Patrick
    listing it prints with is.'
- url: https://archphila.org/parish/st-michael-philadelphia/
  seen: 2026-10-28
  note: 'Directory page (updated 9 months ago): 2nd and Jefferson Sts., Rev. Fernando Londono, Parochial
    Administrator, rectory 1445 N. 2nd St.; Sundays 9:30 English and 11:30 Spanish, weekdays 8:30 AM,
    which agrees with the bulletin; ''Worship Site: Immaculate Conception Church'', which the bulletin
    does not support (see excluded/immaculate-conception-philadelphia-2).'
research:
- method: pnpm fetch:check --diocese philadelphia --parish st-michael-philadelphia (page-pdfs on John
    Patrick listing 214)
  url: https://www.church-bulletin.org/saint-michael-s-parish-philadelphia-pa-19122
  checked: '2026-10-29'
  outcome: found
  next_action: None
  retry_when: ''
- method: probe url and visit.py (https and http) on stmichaelsphiladelphia.com
  url: https://stmichaelsphiladelphia.com/
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: None needed for the bulletin, which the listing carries; recheck the parish's own site
    only if the listing stops updating
  retry_when: The site's certificate is renewed or the listing's issues stop
bulletin_status: available
---

## Publisher

St. Michael's (Rev. Fernando Londono, Parochial Administrator) prints with John Patrick Publishing: listing 214 has an issue for 25 October 2026 with a text layer. The directory's own site, `stmichaelsphiladelphia.com`, has an expired certificate and does not load, so the row's website is the listing. The row is `other`, `page-pdfs` on the listing.

## Worship sites

One church, St. Michael, 1445 North 2nd Street (2nd and Jefferson Sts.). The directory names 'Immaculate Conception Church' (1020 N. Front St.) as a worship site, but that church was relegated to profane but not sordid use effective 11 January 2021 and had had no Mass since 2018; the bulletin lists no Mass there (see `excluded/immaculate-conception-philadelphia-2`).

## Website and bulletin provider

See evidence: the directory site is dead for TLS reasons. Nothing else is known of it.

## Not yet confirmed

Nothing open about the bulletin. The parish's own site could not be read.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on listing 214 picked `2026-10-25.pdf`: transport ok, PDF, issue date 2026-10-25, fresh. Identity shows `unverified` only because no expected identity is supplied; the masthead was read from the issue as described above. It printed no `recipe` line, as the pinned `provider_id` already holds it.
