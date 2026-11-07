---
name: Church of the Holy Child
website: https://www.chcparish.org/
bulletin_provider: parishes_online
provider_id: church-of-the-holy-child
publication: ['po-org:church-of-the-holy-child', 'lpi:0018000000Qx8yyAAB', 'po-container:03/1109']
group: Brandywine Hundred Deanery; pastor shared with St. Helena
evidence:
- url: https://container.parishesonline.com/bulletins/03/1109/20261018B.pdf
  seen: 2026-10-27
  quote: Church of the Holy Child
  note: 'Page 1 of the 18 October 2026 issue (latest in container 03/1109), a cover-page masthead for
    this parish alone. Page 7 lists staff: ''Very Reverend Michael J. Carrier, KHS, V.F., Pastor'' and
    ''Reverend Sylvester Obumneme, Parochial Vicar''.'
- url: https://container.parishesonline.com/bulletins/03/1109/20261018B.pdf
  seen: 2026-10-27
  quote: Pastor ~ St. Helena’s
  note: 'Page 7: the Holy Child bulletin names the same pastor as St. Helena''s, as a staff-directory
    line. It carries Holy Child''s own Mass intentions, which differ from St. Helena''s issue (see publication_reviews).'
- url: https://www.chcparish.org/
  seen: 2026-10-27
  note: 'probe url: HTTP 200, embeds lpi:0018000000Qx8yyAAB and links /bulletin.'
- url: https://parishesonline.com/organization/church-of-the-holy-child
  seen: 2026-10-27
  note: 'probe po: org ''Church of the Holy Child'', 2500 Naamans Rd, latest issue 2026-10-18 (container
    03/1109), weekly issues back to at least 20 Sept.'
revisit: Check that container 03/1109 has posted an issue after 18 October 2026 (none for 25 October to
  8 November on 2026-11-07).
revisit_after: 2026-11-21
promoted: 2026-10-27
research:
- method: fetch:check --diocese wilmington (hand refresh); probe po church-of-the-holy-child; probe container
    03/1109 --weeks 4; browser read of chcparish.org (visit.py --bulletin)
  url: https://parishesonline.com/organization/church-of-the-holy-child
  checked: '2026-11-07'
  outcome: not-found
  next_action: Rerun fetch:check --parish church-of-the-holy-child-wilmington and probe container 03/1109;
    if still nothing after 18 October, read the parish site and St. Helena's bulletin (same pastor) for
    a notice about the bulletin
  retry_when: Container 03/1109 posts an issue after 18 October 2026, or the parish site links another
    bulletin
  revisit_after: 2026-11-21
publication_reviews:
- parish: st-helena-wilmington
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1109/20261018B.pdf
    seen: 2026-10-27
    quote: Church of the Holy Child
    note: 'Holy Child''s 18 October 2026 issue: its own cover, Mass intentions (e.g. ''9:00 a.m.   Brenda
      Howard ~ Rosemary Lynch'') and a second collection ''for Parish Deficit Reduction''. Checked 2026-10-27:
      each masthead names its own parish only (Church of the Holy Child; St. Helena Church). Holy Child''s
      issue names St. Helena only in a deanery parish list (p.3) and a staff line (p.7); St. Helena''s
      names Holy Child only in a deanery list (p.3).'
  - url: https://www.church-bulletin.org/bulletin/saint-helena-s-church-wilmington-de-19809/2026-10-25.pdf
    seen: 2026-10-27
    quote: ST. HELENA CHURCH
    note: 'St. Helena''s 25 October 2026 issue: different publisher, masthead, intentions (''9:00 AM —
      Samuel & Marie Emmi'') and a second collection for ''All Saints Day Maintenance & Repair''. Different
      weeks, so the content test is the mastheads, intentions and publishers, not the collection.'
---

## Publisher

Holy Child publishes its own weekly bulletin through LPi / ParishesOnline (org `church-of-the-holy-child`, container 03/1109). The 18 October 2026 issue (the newest; 25 October answered 403 on 2026-10-27) has a cover headed 'Church of the Holy Child' and a staff page (page 7) with the pastor, parochial vicar and a pastoral associate.

## Worship sites

One church, Church of the Holy Child, 2500 Naamans Road. Page 7 gives Mass as Sunday vigil (Saturday) 4:00 p.m., Sunday 8:30 a.m. and 11:00 a.m., and weekdays Monday to Thursday 9:00 a.m., which agrees with the diocese map's times.

## Shared pastor, separate bulletin

Since 14 January 2026 Holy Child and St. Helena have had one pastor (The Dialog, 2025-12-01, per diocese.md *Sources*). The two bulletins confirm it, with Very Rev. Michael J. Carrier as pastor in both staff lists, but they remain two publications: St. Helena's is a John Patrick Publishing issue at church-bulletin.org with its own masthead and Mass intentions (see the `st-helena-wilmington` record). The shared pastor does not make a shared bulletin (diocese.md *Rules settled*), so these are two rows.

## Website and bulletin provider

chcparish.org is a Duda site that embeds the LPi widget, so the ParishesOnline org is the publication. The fetch check is described under *Fetch check* below.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish church-of-the-holy-child-wilmington` (2026-10-27): Resolved through the LPi widget to container 03/1109; picked `20261018B.pdf` (8 pages), fresh. The tool reports identity 'unverified' (no expected identity supplied); identity rests on the masthead read above.

Hand refresh (2026-11-07, `scratch/wilmington-map-1/refresh/fetch_check.out`): the same pick, `20261018B.pdf`, now **stale** (20 days). The container answers 403 for 25 October, 1 November and 8 November; `probe po` lists 18 October as the newest issue, and chcparish.org's bulletin widget still shows it. The pick is the newest issue there is, so the staleness is the source's.

## Not yet confirmed

No issue has been posted since 18 October 2026 (checked 2026-11-07). Nothing says the bulletin moved: the parish site still embeds the same widget, and St. Helena's 8 November issue (same pastor) names Holy Child only in the deanery's joint notices ('parishes of: The Church of the Holy Child, Holy Rosary, ...') and for an event held there. The row stays live; see `research` for the next check.
