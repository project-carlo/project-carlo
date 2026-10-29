---
name: Saint Bridget University Parish
website: https://www.stbridgetup.org/
bulletin_provider: other
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
revisit: Find the ParishesOnline organization slug for container 03/1233 (or see the widget answer again)
  so fetch can read the bulletin; then set bulletin_provider parishes_online and run fetch:check
revisit_after: 2026-12-01
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
bulletin_status: access-blocked
---

## Publisher

Saint Bridget University Parish, Glassboro (the parish of Rowan University and a Hispanic community, per its site) publishes one weekly bulletin through ParishesOnline, container 03/1233. The 1 November 2026 issue (text layer, read 2026-10-29) is headed 'SAINT BRIDGET UNIVERSITY PARISH', pastor Rev. John A. Rossi, with a single church's Mass schedule.

## Worship sites

One church, `st-bridget-glassboro` (125 Church St.). The bulletin's schedule says 'in Church' and names no other place for Mass; the Newman House at 1 Redmond Ave. (Rowan campus ministry) and the Franciscan Sisters Convent (212 Ellis St.) appear only as contacts. St. Michael the Archangel Regional School (51 W. North St., Clayton) is listed as a school contact, and belongs to the Parish of St. Michael the Archangel's territory, not this parish. The old site churchofstbridget.com (GCatholic's website) has no DNS; the current one is stbridgetup.org (the diocese directory's).

## Website and bulletin provider

`other` for now. The bulletin is on ParishesOnline, but I found only its container (03/1233, from a search-engine hit on its PDFs) and not the organization slug, so `parishes_online` can't be set (see research). The parish page embeds the ParishesOnline widget, which was down (502) during this check, so the pipeline cannot find the issue from the page either. `fetch:check` (2026-10-29) with provider `other` and the site as the page: resolve_failed, 'No bulletin page link found for other provider at https://www.stbridgetup.org/'. The bulletin exists and is current (the 2026-11-01 issue read at its container URL above); only the pipeline's route to it is missing, so `bulletin_status` is `access-blocked`.

## Not yet confirmed

The organization slug (see research), and whether the pipeline can read the current issue from the site. Whether Newman House holds public Mass is not shown in the bulletin (no Mass listed there).
