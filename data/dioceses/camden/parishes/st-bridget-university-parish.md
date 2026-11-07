---
name: Saint Bridget University Parish
website: https://www.stbridgetup.org/
bulletin_provider: unsupported
provider_id: ''
publication: ['po-container:03/1233']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1233/20261101B.pdf
  seen: 2026-10-29
  quote: SAINT BRIDGET UNIVERSITY PARISH
  note: 'Text-layer bulletin (8 pages), page 1: ''SUNDAY, NOVEMBER 1, 2026''; ''Pastor Rev.John A. Rossi'';
    Mass schedule ''Saturday Vigil:  4:30 PM'', ''Sunday: 9:00 AM and 11:00 AM'', ''No Tuesday Mass'';
    ''Saturday 3:30 - 4:00 PM in Church'' for confessions; ''Parish Office 127 Church Street, Glassboro'';
    ''Newman House Catholic Campus Ministry Rowan University 1 Redmond Ave., Glassboro''. Names this parish
    alone.'
- url: https://www.stbridgetup.org/en/bulletins
  seen: 2026-10-29
  quote: If you would like information on past bulletins please contact the parish center.
  note: 'The parish''s ''Weekly Bulletin'' page. It embeds a ParishesOnline widget script (widget.parishesonline.com/publications?id=37e1781454dd8300f93cdbda275b78546ed43745)
    that answered HTTP 502 to probe get and to the browser, so the page shows no issue. Its footer repeats
    the schedule: Saturday Vigil 4:30 PM, Sunday 9 am and 11 am, daily Mass 9am (Mon/Wed/Thurs/Fri), no
    Mass on Tuesdays, confessions Saturday 3:30-4:00pm at Church.'
- url: https://container.parishesonline.com/bulletins/03/1233/20250518B.pdf
  seen: 2026-10-29
  note: 'Search-engine result (duckduckgo, 2026-10-29) for the container''s earlier issues: ''St. Bridget
    University Parish May 18, 2025'', office ''127 Church Street, Glassboro'', ''Website: www.StBridgetUP.org''.
    Links container 03/1233 to this parish and its website.'
- url: https://container.parishesonline.com/bulletins/03/1233/20261108B.pdf
  seen: 2026-11-07
  quote: SAINT BRIDGET UNIVERSITY PARISH
  note: 'Page 1 of the 8 November 2026 issue (probe container 03/1233), headed ''SUNDAY, NOVEMBER 8, 2026'',
    with the parish staff and Mass schedule: the container is current.'
revisit: 'Find the ParishesOnline organization slug for container 03/1233 (or see the widget answer again);
  then set bulletin_provider parishes_online with the slug, add po-org: and lpi: ids, clear fetch_gap
  and run fetch:check'
revisit_after: 2026-12-01
promoted: 2026-10-30
research:
- method: probe po with slug guesses (st-bridget-university-parish, saint-bridget-university-parish and
    -glassboro/-08028 variants, saint-bridget), the widget id and container 03/1233; probe get on the
    widget URL; two duckduckgo searches
  url: https://www.stbridgetup.org/en/bulletins
  checked: '2026-10-29'
  outcome: not-found
  next_action: Find the ParishesOnline organization slug (parishesonline.com/organization/<slug>) so the
    row can be parishes_online with provider_id; or re-run probe get on the widget URL when widget.parishesonline.com
    stops answering 502, which would expose the org
  retry_when: widget.parishesonline.com answers the St. Bridget widget id, or the parish site links a
    parishesonline.com/organization page
- method: 'Hand refresh against main: probe get on the widget URL (502), probe po on four more slug guesses
    (st-bridget-08028, saint-bridget-08028, st-bridget-university-parish-08028, saint-bridget-university:
    none exist), probe container 03/1233, fetch:check --diocese camden'
  url: https://widget.parishesonline.com/publications?id=37e1781454dd8300f93cdbda275b78546ed43745
  checked: '2026-11-07'
  outcome: unsupported-format
  next_action: Row set unsupported with fetch_gap po-org-unknown; find the org slug (the widget, once
    it answers, or the parish office) and set parishes_online
  retry_when: widget.parishesonline.com answers the St. Bridget widget id, or a collector reads a ParishesOnline
    container without an org slug
  revisit_after: 2026-12-01
bulletin_status: available
fetch_gap:
  kind: po-org-unknown
  seen: 2026-11-07
  note: The current LPi bulletin is in ParishesOnline container 03/1233 (20261108B.pdf, 8 November 2026,
    masthead 'SAINT BRIDGET UNIVERSITY PARISH'), but no ParishesOnline org slug for it was found, and
    the parishes_online collector reads by slug. The parish's Squarespace /en/bulletins page only embeds
    widget.parishesonline.com/publications?id=37e17814…, which answered 502 on 2026-10-29 and 2026-11-07,
    so fetch:check on the site finds no bulletin page link.
  url: https://container.parishesonline.com/bulletins/03/1233/20261108B.pdf
---

## Publisher

Saint Bridget University Parish, Glassboro (the parish of Rowan University and a Hispanic community, per its site) publishes one weekly bulletin through ParishesOnline, container 03/1233. The 1 November 2026 issue (text layer, read 2026-10-29) is headed 'SAINT BRIDGET UNIVERSITY PARISH', pastor Rev. John A. Rossi, with a single church's Mass schedule.

## Worship sites

One church, `st-bridget-glassboro` (125 Church St.). The bulletin's schedule says 'in Church' and names no other place for Mass; the Newman House at 1 Redmond Ave. (Rowan campus ministry) and the Franciscan Sisters Convent (212 Ellis St.) appear only as contacts. St. Michael the Archangel Regional School (51 W. North St., Clayton) is listed as a school contact, and belongs to the Parish of St. Michael the Archangel's territory, not this parish. The old site churchofstbridget.com (GCatholic's website) has no DNS; the current one is stbridgetup.org (the diocese directory's).

## Website and bulletin provider

**`unsupported`, with `fetch_gap` `po-org-unknown`** (hand refresh against main, 2026-11-07), so `promote` keeps the row and its churches off the site until the pipeline can read the bulletin. The bulletin is on ParishesOnline and current (container 03/1233; the 8 November 2026 issue read at its container URL on 2026-11-07), but I found only its container (from a search-engine hit on its PDFs), not the organization slug, so `parishes_online` can't be set (see research). The parish page embeds the ParishesOnline widget, which answered 502 on 2026-10-29 and again on 2026-11-07, so the pipeline cannot find the issue from the page either: `fetch:check` with provider `other` on the site (2026-10-29 and 2026-11-07) returns resolve_failed, 'No bulletin page link found for other provider at https://www.stbridgetup.org/'. `bulletin_status` is `available`: the bulletin is published and readable, only the pipeline's route to it is missing. Once the slug turns up, set the provider to `parishes_online` with that slug, add `po-org:` and `lpi:` ids to `publication`, clear the gap and run `fetch:check`.

## Not yet confirmed

The organization slug (see research). Whether Newman House holds public Mass is not shown in the bulletin (no Mass listed there).
