---
name: St. Patrick's Oratory
reason: other
line1: 3656 State Route 13
city: Truxton
state: NY
postal_code: '13158'
decided: 2026-09-26
roster: ['gcatholic:18052', 'directory:33197']
evidence:
- url: https://gcatholic.org/churches/usa-02/18052
  seen: 2026-09-25
  quote: 3656 State Route 13, Truxton, New York 13158-0015
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Syracuse as ''St. Patrick'', 3656
    State Route 13, Truxton, NY, 13158; kind: Church'
- url: https://www.syracusediocese.org/parishfinder
  seen: 2026-09-26
  note: Listed in Diocese of Syracuse parish finder (Mass-times map) as 'St. Patrick Oratory', 3656 State
    Route 13, Truxton, NY, 13158-0015
- url: https://discovermass.com/church/st-mary-cortland-ny/
  seen: 2026-09-26
  quote: St Patrick's Oratory is open Thursday's from 2 - 3:30 PM. The rosary is recited at 2:45 PM followed
    by Divine Mercy Chaplet at 3 PM.
  note: The Cortland parishes' bulletin, 23 August 2026 issue, page 6 ("Opportunities For Quiet Prayer
    Available at St. Anthony's & St. Mary's Churches And St Patrick's Oratory"); the same notice is in
    every issue from 12 July to 27 September 2026 (page 5 or 6). Discover Mass links are per-visit tokens,
    so the church page is cited.
- url: https://discovermass.com/church/st-mary-cortland-ny/
  seen: 2026-09-26
  quote: 'The New Weekend Mass Schedule Is: … 4 PM Vigil Mass at St. Mary''s … 5:15 PM Vigil Mass at St.
    Lawrence''s … 9:15 AM Mass at St. Anthony''s … 4 PM Mass at The Newman Center'
  note: 6 September 2026 issue, page 2. The pastor's full weekend schedule from 12/13 September; Truxton
    is not in it.
- url: https://www.syracusediocese.org/st-patrick-oratory-truxton
  seen: 2026-09-26
  quote: St. Patrick is an Oratory of St. Margaret, Homer.
  note: The diocese's page (behind Cloudflare; read with visit.py), physical address 3656 State Route
    13, Truxton 13158, served by the Cortland clergy.
- url: https://www.openstreetmap.org/way/1212812544
  seen: 2026-09-26
  note: OSM place_of_worship "St. Patrick's", State Route 13, Truxton; the building exists.
parish: st-mary-cortland
---

## Why it is excluded

St. Patrick's in Truxton is an oratory ("St. Patrick is an Oratory of St. Margaret, Homer", diocese
page read 2026-09-26), open, but with no Mass that I could find. The Cortland parishes' bulletin,
which serves it, describes it in every issue from 12 July to 27 September 2026 as open for prayer:
"St Patrick's Oratory is open Thursday's from 2 - 3:30 PM. The rosary is recited at 2:45 PM followed
by Divine Mercy Chaplet at 3 PM." The pastor's complete weekend schedule from 12/13 September lists
St. Mary's, St. Lawrence's, St. Anthony's, St. Margaret's and the Newman Center, not Truxton. I
searched the text of the nine issues Discover Mass served readably between 12 July and 27 September
(three others, 19 July, 2 and 30 August, would not download) for "Truxton" and "Oratory": the only
hits are this prayer notice, and no Mass-intention list names St. Patrick's.

The reason is `other`, not `closed` (the building is open and used for prayer) and not
`no-public-mass` in the sense of an office or private chapel: it is a public oratory where, on this
evidence, Mass is not celebrated. The evidence is absence of Mass in three months of bulletins plus
the bulletin's positive description of what does happen there.

## What would change this

A Mass at the oratory, even once a year (see `revisit`): then it becomes a church row under
`st-mary-cortland`.
