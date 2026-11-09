---
name: St. John Baptist de la Salle Church
reason: other
line1: 70 Jackson St.
city: Staten Island
state: NY
postal_code: '10304'
decided: 2026-11-09
roster: ['gcatholic:16386']
evidence:
- url: https://www.dropbox.com/scl/fi/s7vafo0lworx170w0xxdl/Saint-Joseph-and-Immaculate-Conception-St.-Mary-Staten-Island.pdf?rlkey=tjqe197za4v5xma75q2fa8czi&dl=1
  seen: 2026-11-09
  note: 'Decree of merger signed November 2, 2014 (implemented by August 1, 2015), linked from https://www.archny.org/parish-planning.
    Image-only PDF, page 4 read visually. Paragraph 1 merges St. Joseph, Immaculate Conception and St.
    Mary and says ''The parish will have three churches''; paragraphs 2-4 name them: St. Joseph (parish
    church), Immaculate Conception (regular Masses) and St. Mary (open, no regular Masses). St. John Baptist
    de la Salle is not named anywhere in the decree.'
- url: https://files.ecatholic.com/6497/bulletins/20261108.pdf
  seen: 2026-11-09
  quote: Immaculate Conception Church
  note: '8 November 2026 St. Joseph and St. Mary Immaculate bulletin, page 1: weekend and weekday Masses
    at St. Joseph''s Church and Immaculate Conception Church only. No La Salle or Jackson Street. All
    46 weekly issues from 28 December 2025 to 8 November 2026 were searched for Salle and Jackson with
    no match, though 22 of them have text on only 2 of 8-12 pages (the rest are images).'
- url: https://data.cityofnewyork.us/resource/64uk-42ks.json?bbl=5005170016
  seen: 2026-11-09
  quote: ST JOHN BAPT DE LA SA
  note: 'NYC PLUTO tax lot 5005170016, 70 Jackson Street: owner ''ST JOHN BAPT DE LA SA'', building class
    W2 (educational: parochial school), one building, built 1927. The city classes the building as a school,
    not a church (class M1).'
- url: https://gcatholic.org/churches/usa-02/16386
  seen: 2026-10-08
  quote: 'Mission of: Church of the Immaculate Conception'
  note: GCatholic lists St. John Baptist de la Salle, 70 Jackson St., 10304, as a mission of Immaculate
    Conception. No Mass times.
parish: st-joseph-and-st-mary-immaculate-staten-island
revisit: Grep new St. Joseph and St. Mary Immaculate bulletins (eCatholic 6497) for La Salle or 70 Jackson
  Street; a public Mass there makes it a church of st-joseph-and-st-mary-immaculate-staten-island.
revisit_after: 2027-05-01
research:
- method: Grep of every weekly St. Joseph and St. Mary Immaculate bulletin (eCatholic 6497) from 28 December
    2025 to 8 November 2026 for Salle and Jackson; archdiocesan parish-planning decree index
  url: https://files.ecatholic.com/6497/bulletins/20261108.pdf
  checked: '2026-11-09'
  outcome: not-found
  next_action: Grep new St. Joseph and St. Mary Immaculate issues for La Salle or Jackson Street
  retry_when: A bulletin, the parish site or the archdiocese mentions Mass at 70 Jackson Street
  revisit_after: 2027-05-01
---

## Why it is excluded

No source shows public Mass at 70 Jackson Street, and the archdiocese's own decree leaves it out of the parish's churches. The November 2, 2014 decree merging St. Joseph, Immaculate Conception and St. Mary (page 4, read 9 November 2026) says "The parish will have three churches" and names them: St. Joseph, Immaculate Conception and St. Mary. St. John Baptist de la Salle does not appear. The parish's current bulletin (8 November 2026) schedules Mass only at St. Joseph's and Immaculate Conception; no weekly issue since 28 December 2025 mentions La Salle or Jackson Street (22 of the 46 are only partly text-readable). The official archdiocesan map doesn't list it. NYC's tax-lot data classes the 1927 building at 70 Jackson Street, still owned in the La Salle corporate name, as a parochial school (W2), not a church. GCatholic's "mission of Immaculate Conception" is the only source calling it a church.

## Judgment

This is a judgment call, not a dated closure: no source says when Mass there ended or that the building was relegated, so the reason is `other`, not `closed`, and `last_mass` is empty. The building looks like a school-and-chapel mission of the old Immaculate Conception parish that was not carried into the 2015 merged parish. The 8 October session's open question asked the parish office; under the follow-up's no-contact rule it is settled from the decree, the bulletins and the city record instead.

## What would change this

A bulletin, parish-site or archdiocesan notice of Mass at St. John Baptist de la Salle or 70 Jackson Street, which would make it a church of `st-joseph-and-st-mary-immaculate-staten-island`.
