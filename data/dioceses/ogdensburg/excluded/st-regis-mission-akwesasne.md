---
name: St. Regis Mission Church
reason: other-jurisdiction
line1: Route 37
city: Hogansburg
state: NY
postal_code: '13655'
decided: 2026-09-30
roster:
- gcatholic:18282
- directory:hogansburg
evidence:
- url: https://gcatholic.org/churches/usa-02/18282
  seen: 2026-09-30
  quote: Route 37, Hogansburg, New York 13655
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Ogdensburg as ''St. Regis'', Route
    37, Hogansburg, NY, 13655; kind: Mission'
- url: https://www.rcdony.org/parish/hogansburg
  seen: 2026-09-30
  quote: St. Regis, Quebec H0M 1A0
  note: 'Ogdensburg diocese directory entry (directory:hogansburg), listed under "Hogansburg": "St. Regis
    Mission, 109 Angus Thomas Memorial Street, St. Regis, Quebec H0M 1A0, Canada", pastor Reverend Jerome
    Pastores, mailing address P.O. Box 429, Hogansburg, NY.'
- url: https://diocesevalleyfield.org/fr/bulletins-paroissiaux/bp-septembre-2026
  seen: 2026-09-30
  quote: St. Regis Mission Church - Saint-Régis
  note: The Diocese of Valleyfield (Quebec) list of parish bulletins for September 2026 includes "St.
    Regis Mission Church - Saint-Régis" (links http://stregismission.org/ and a Facebook page) among its
    own parishes, with no PDF linked for any Sunday.
- url: https://northcountrycatholic.org/Articles/2026/4_1Missionvisit.html
  seen: 2026-09-30
  quote: Bishop Alain Faubert of the Diocese of Valleyfield
  note: 'North Country Catholic, 1 April 2026, "Valleyfield bishop visits Mission" by Dr. Rose-Alma McDonald
    of St. Regis Mission Church: on 21 and 22 March the mission "welcomed a special pastoral visit from
    Bishop Alain Faubert of the Diocese of Valleyfield", who celebrated Mass, and its parishioners hope
    for "ongoing collaboration with the diocese".'
- url: https://diocesevalleyfield.org/sites/default/files/february_5_2023_bulletin_st._regis_mission.pdf
  seen: 2026-09-30
  quote: For weekend masses at the St. Regis Mission Church
  note: 'A 5 February 2023 St. Regis Mission bulletin hosted on the Diocese of Valleyfield''s site: Saturday
    4:00 PM and Sunday 10:00 AM Mass, collections in CDN and USD.'
- url: https://www.openstreetmap.org/way/1264645745
  seen: 2026-09-30
  note: 'OpenStreetMap way 1264645745, "St. Regis Mission Catholic Church, Rue du Mémorial Angus Thomas,
    Montérégie, Québec, H0M 1A0" at 45.00278, -74.64262: the church is on the Quebec side of Akwesasne.'
- url: https://www.stregismission.org/
  seen: 2026-09-30
  note: The mission's own site (linked from Valleyfield) answered Cloudflare error 1016, "Origin DNS error",
    on 2026-09-30, and stregismission.org does not resolve in `probe url`.
---

## Why it is excluded

The St. Regis Mission Church, 109 Angus Thomas Memorial Street (Rue du Mémorial Angus Thomas), Saint-Régis,
Quebec is in the Diocese of Valleyfield, not the Diocese of Ogdensburg. The Ogdensburg directory lists it
(directory:hogansburg) with a Quebec address, postal code H0M 1A0, and only a Hogansburg, NY mailing address
(P.O. Box 429); GCatholic lists "St. Regis", a mission, at "Route 37, Hogansburg" with no coordinates
(gcatholic:18282), which this record also takes to be the same church. The Diocese of Valleyfield lists "St.
Regis Mission Church - Saint-Régis" among its own parishes on its September 2026 bulletin page, the
Ogdensburg diocese's paper reported its bishop's pastoral visit on 21 and 22 March 2026 (Valleyfield's
Bishop Alain Faubert), and OpenStreetMap places the building on the Quebec side of Akwesasne. It holds
public Mass (Saturday and Sunday in a 2023 bulletin) but is out of this diocese, so
`other-jurisdiction`. The record keeps GCatholic's NY address fields because the validator does not
accept a Canadian postal code.

The New York side of Akwesasne has no other Catholic church in either roster: St. Patrick's, Hogansburg was
sold (`excluded/st-patrick-hogansburg`).

## What would change this

Whether GCatholic's "Route 37, Hogansburg" mission is a separate New York chapel is not settled: it has no
coordinates and no bulletin, and the Ogdensburg directory has no New York entry for the Akwesasne area
besides this one. If a New York-side chapel with public Mass turned up, it would be a new record. The mission's
own bulletins are not on Valleyfield's site for September 2026 and stregismission.org is down; if the mission
were ever to publish under Ogdensburg it would need a bulletin first.
