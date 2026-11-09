---
name: Most Holy Redeemer
reason: closed
line1: 173 E 3rd St.
city: New York City
state: NY
postal_code: '10009'
decided: 2026-11-09
roster: ['gcatholic:16309', 'directory:4798']
evidence:
- url: https://mhr173.org/mass-times
  seen: 2026-10-31
  quote: As of Sunday, August 31, 2025 there will be no regularly scheduled Masses at Most Holy Redeemer
    Church.
  note: East Village Catholic's Mass and Sacramental Schedule, rendered in headed Chrome; the sentence
    continues 'Please refer to the Mass schedule for Saint Brigid Church at 119 Avenue B'. The page lists
    no Mass at Most Holy Redeemer, only at Saint Brigid.
- url: https://files.ecatholic.com/34038/bulletins/20261108.pdf
  seen: 2026-11-09
  note: The 8 November 2026 Saint Brigid bulletin (the East Village Catholic publisher, eCatholic 34038,
    linked from mhr173.org/bulletins) gives Masses at 119 Avenue B only and never mentions Redeemer. Grepping
    'Redeemer' across fourteen issues, fortnightly from 17 May to 1 November 2026 plus 8 November, found
    no mention, so no occasional Mass at the shrine was announced in six months.
- url: https://gcatholic.org/churches/usa-02/16309
  seen: 2026-10-07
  note: GCatholic identity, address and Plus Code.
- url: https://www.archny.org/places/evc-mhr-n
  seen: 2026-10-07
  quote: 'East Village Catholic: Most Holy Redeemer - Nativity Church'
  note: Archdiocesan map entry (directory:4798) for the same building.
parish: st-brigid-new-york-city
last_mass: 2025-08
research:
- method: issues.py ecatholic ecatholic:34038 --all --step 2 --grep Redeemer (17 May-1 November 2026)
    and --weeks 3 --grep Redeemer --grep Shrine (8 November 2026)
  url: https://files.ecatholic.com/34038/bulletins/20261108.pdf
  checked: '2026-11-09'
  outcome: found
---

## Why it is excluded

The responsible parish's own schedule page (East Village Catholic, the parishes of Most Holy Redeemer-Nativity and Saint Brigid-Saint Emeric), read 31 October 2026, says: "As of Sunday, August 31, 2025 there will be no regularly scheduled Masses at Most Holy Redeemer Church" and sends worshippers to Saint Brigid, 119 Avenue B. The parish's bulletin (eCatholic 34038, Saint Brigid's masthead) lists Masses only at Saint Brigid, and fourteen issues from May to 8 November 2026 never mention Most Holy Redeemer. `last_mass` is August 2025, the month regular Mass ended; the source gives no final date. The site still calls the building a pilgrimage shrine, so it is not described as sold or demolished.

## What would change this

An announced Mass at 173 East 3rd Street in the Saint Brigid bulletin or on mhr173.org/mass-times (an occasional Mass counts), which would make it a church under `st-brigid-new-york-city`.
