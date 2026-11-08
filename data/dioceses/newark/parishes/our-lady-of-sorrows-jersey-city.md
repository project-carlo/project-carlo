---
name: Our Lady of Sorrows, Jersey City
website: https://olsnj.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:our-lady-of-sorrows-church-07305', 'lpi:0018000000QxACQAA3']
group: ''
evidence:
- url: https://olsnj.org/
  seen: 2026-11-03
  note: 'probe url: UNREACHABLE (certificate does not verify); visit.py: the browser ends at marthasvineyardtours.net,
    ERR_SSL_PROTOCOL_ERROR, verdict REDIRECT-OFFSITE. The parish domain no longer serves the parish site.'
- url: https://web.archive.org/web/20251013055043/https://olsnj.org/bulletins
  seen: 2026-11-03
  note: 'Wayback copy of 13 October 2025 (read in the browser with quick_snap.py; the id_ API answered
    429): eCatholic site (files.ecatholic.com/13524), ''Bulletin'' page with only an ''ARCHIVE'' tile
    and no issues. The 8 February 2025 copy (/web/20250208193136/https://www.olsnj.org/bulletins) is the
    same.'
- url: https://web.archive.org/web/20250619150213/https://www.olsnj.org/mass-schedule
  seen: 2026-11-03
  note: 'Wayback copy of 19 June 2025, read with visit.py: ''WEEKLY MASS SCHEDULE SUNDAY 9:00 AM Latin
    Mass 11:00 AM English Mass 1:00 PM Spanish Mass … TUESDAY … 7:00 PM Spanish Mass SATURDAY 8:00 AM
    Bilingual Mass''.'
- url: https://parishesonline.com/organization/our-lady-of-sorrows-church-07305
  seen: 2026-11-03
  note: 'probe po: org ''Our Lady of Sorrows Church'', 93 Clerk St # 95, Jersey City, NJ 07305-4323, lpi
    0018000000QxACQAA3, website null, no publications (''this organization does not publish a bulletin
    here now'').'
- url: https://rcan.org/clergy-appointments-april-2024/
  seen: 2026-11-03
  quote: Father Esterminio Chica has been granted another term to his pastorate at Christ the King and
    Our Lady of Sorrows, Jersey City, ending June 30, 2029.
- url: https://rcan.org/clergy-appointments-june-23-2026/
  seen: 2026-11-03
  quote: Reverend Michael C. Barone has been appointed part-time chaplain of the Traditional Latin Mass
    community at Our Lady of Sorrows, Jersey City
- url: https://latinmassjc.com/
  seen: 2026-11-03
  quote: Please join us for the Most Holy Sacrifice of the Mass on Sundays at 9:00am at Our Lady of Sorrows
    Church 73 Claremont Avenue Jersey City
  note: Latin Mass Community of Jersey City (WordPress), linked from the old olsnj.org menu. Homepage
    headed 'November 8, 2026'. It links a Google Drive folder of 'Music Programs' (worship aids), not
    a bulletin.
revisit: 'Look for the parish''s current site or bulletin: read Christ the King''s newest issue (church-bulletin.org/693)
  for an Our Lady of Sorrows section or masthead, probe po our-lady-of-sorrows-church-07305 for new issues,
  and check whether olsnj.org serves the parish again. If a bulletin turns up, set the provider and run
  fetch:check.'
revisit_after: 2026-12-01
research:
- method: probe url and visit.py on the directory's and GCatholic's site
  url: https://olsnj.org/
  checked: '2026-11-03'
  outcome: not-found
  next_action: Find the parish's new site (masthead of a future issue, Facebook page, rcan.org directory
    update)
  retry_when: The directory lists a new website or olsnj.org serves the parish again
  revisit_after: 2026-12-01
- method: Wayback copies of olsnj.org/bulletins (Feb and Oct 2025) and issues.py ecatholic on ecatholic:13524,
    60 Sundays back from 2026-11-08 and every 4th Sunday from 2025-10-12 back to 2024
  url: https://web.archive.org/web/20251013055043/https://olsnj.org/bulletins
  checked: '2026-11-03'
  outcome: not-found
  next_action: None on this source; the eCatholic site posted no bulletins in 2025
  retry_when: A new parish site appears
- method: probe po on the ParishesOnline org
  url: https://parishesonline.com/organization/our-lady-of-sorrows-church-07305
  checked: '2026-11-03'
  outcome: not-found
  next_action: probe po our-lady-of-sorrows-church-07305 again
  retry_when: Revisit date
  revisit_after: 2026-12-01
- method: 'John Patrick: church-bulletin.org/693 suffixes A, B, O, S, L; Run scan output ids 1-1000 and
    6000-6060 (scratch/newark-map-1/029-map/jp-*.tsv) grepped for sorrows and 07305'
  url: https://church-bulletin.org/693
  checked: '2026-11-03'
  outcome: not-found
  next_action: Read Christ the King's next issues for an Our Lady of Sorrows section
  retry_when: Revisit date
  revisit_after: 2026-12-01
bulletin_status: not-found
---

## Publisher

No bulletin found. Our Lady of Sorrows shares its pastor with Christ the King: rcan.org's April 2024 appointments say 'Father Esterminio Chica has been granted another term to his pastorate at Christ the King and Our Lady of Sorrows, Jersey City'. But Christ the King's 1 November 2026 bulletin (John Patrick 693, `christ-the-king-jersey-city`) names Christ the King alone on pages 1 and 2, and no John Patrick listing for Our Lady of Sorrows turned up (see research). So this parish is not folded into that row.

Its ParishesOnline org (`our-lady-of-sorrows-church-07305`, lpi 0018000000QxACQAA3) exists but has no publications; those ids are kept in `publication` so a future issue there is matched to this row.

## Worship sites

- Our Lady of Sorrows, 93 Clerk Street (`our-lady-of-sorrows-jersey-city`). The parish's last archived schedule (June 2025) gives Sunday 9:00 AM Latin, 11:00 AM English, 1:00 PM Spanish, Tuesday 7:00 PM Spanish and Saturday 8:00 AM bilingual; the Latin Mass Community's site, headed 8 November 2026, still gives 'Sundays at 9:00am at Our Lady of Sorrows Church'. The Traditional Latin Mass community (chaplain Rev. Michael C. Barone from 20 April 2026, per rcan.org's 23 June 2026 appointments) worships in this church, so it is no separate church row. Its Google Drive 'Music Programs' are worship aids, not a bulletin.

The directory (76) and GCatholic (18442) list only this church.

## Website and bulletin provider

`no_bulletin`. The directory's and GCatholic's site olsnj.org no longer serves the parish: its certificate fails and the browser lands on marthasvineyardtours.net (2026-11-03). Its Wayback copies (February and October 2025) show an eCatholic site (files.ecatholic.com/13524) whose Bulletin page holds only an empty 'ARCHIVE' tile, and `issues.py` found no `ecatholic:13524` bulletins back to 2024. The website field keeps olsnj.org, the last site the parish used, until a new one is found.

## Not yet confirmed

Whether the parish prints a bulletin at all (on paper only, on a Facebook page, or as part of Christ the King's). The `revisit` lists the checks; the Facebook route was not tried.
