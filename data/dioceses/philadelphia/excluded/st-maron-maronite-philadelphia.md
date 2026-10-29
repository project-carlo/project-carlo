---
name: St. Maron (Maronite)
reason: other-jurisdiction
line1: 1013 Ellsworth St.
city: Philadelphia
state: PA
postal_code: '19147'
decided: 2026-10-29
roster: ['gcatholic:17051']
evidence:
- url: https://gcatholic.org/churches/usa-03/17051
  seen: 2026-10-29
  quote: 'Jurisdiction: Maronite Diocese of Saint Maron of Brooklyn'
  note: 'GCatholic page (read 2026-10-29, last updated 2025.12.21): ''Jurisdiction: Maronite Diocese of
    Saint Maron of Brooklyn'', ''Location: within the territory of the Roman Metropolitan Archdiocese
    of Philadelphia'', ''Rite: Maronite (Antiochian)''.'
- url: https://www.stmaron.org/s/2026-Eparchial-Directory-wd4l.pdf
  seen: 2026-10-29
  quote: 1013 Ellsworth Street
  note: '2026 Directory of the Eparchy of Saint Maron of Brooklyn, page 12: ''Saint Maron Church'', Reverend
    Andrawos (Fadi) El Tabchi, Pastor, 1013 Ellsworth Street, Philadelphia, PA 19147, phone (215) 389-2000,
    website saintmaron.org. GCatholic gives 1010 Ellsworth St. with the same phone; this record takes
    the eparchy''s 1013 (same block).'
research:
- method: probe url on https://www.saintmaron.org/
  url: https://www.saintmaron.org/
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: Read the site later if the street number needs settling
  retry_when: The site stops answering HTTP 500; irrelevant to the exclusion, which rests on the eparchy
    directory
---

## Why it is excluded

St. Maron (Maronite), Ellsworth St., Philadelphia is a Maronite church of the Eparchy of St. Maron of Brooklyn, not of the Roman Catholic Archdiocese of Philadelphia. GCatholic (read 2026-10-29) gives 'Jurisdiction: Maronite Diocese of Saint Maron of Brooklyn'; the eparchy's 2026 directory (read 2026-10-29) lists 'Saint Maron Church' at 1013 Ellsworth Street where GCatholic has 1010; the phone number is the same. The church's site saintmaron.org answered HTTP 500 on 2026-10-29. Excluded as `other-jurisdiction` under the rule settled in `diocese.md`.

## What would change this

Nothing expected: it belongs to its own eparchy's dataset, not this archdiocese's.
