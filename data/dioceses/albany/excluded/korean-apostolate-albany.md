---
name: Korean Catholic Community of Albany (Korean Apostolate), former St. Francis de Sales Church
reason: no-bulletin
line1: 17 Exchange Street
city: Albany
state: NY
postal_code: '12205'
decided: 2026-09-28
roster: ['directory:267']
evidence:
- url: https://www.rcda.org/parishes/parish/korean-apostolate-albany-ny
  seen: 2026-09-28
  quote: 'Korean Apostolate Mass Schedule Sunday: 10:00 am'
  note: The directory's Korean Apostolate page (entry 267), "17 Exchange St. Albany, NY 12205", Rev. Dojin
    Angelo Na; website http://cafe.daum.net/kccalbany.
- url: https://cafe.daum.net/kccalbany/bJaB
  seen: 2026-09-28
  note: 'The community''s Daum cafe (올바니 한인 천주교회, "Albany Korean Catholic Church"; JavaScript, read in a
    browser with visit.py). Its 주보 ("bulletin") board has one post per Sunday, newest "2026년 9월 27일 한가위
    미사" (27 September 2026, Chuseok Mass), posted 26.09.27. Each post carries a single PowerPoint attachment
    (.pptx, 1.34 MB for 27 September), not a PDF; the board is public but the attachment sits in the Daum
    viewer.'
- url: https://cafe.daum.net/kccalbany
  seen: 2026-09-28
  note: 'Cafe home, "미사와 성사안내" (Mass and sacraments) post of 18.05.23: "주일미사: 매주 일요일 오전 10시" (Sunday
    Mass every Sunday 10 am), weekday Mass Tuesday 10 am; "오시는 길" post: "17Exchange St Albany, NY 12205".'
- url: https://evangelist.org/news/2018/apr/06/korean-catholics-greet-new-leader/
  seen: 2026-09-28
  quote: Sunday Mass in Korean at St. Francis de Sales Church on Exchange Street in Albany
  note: The Evangelist, on the Korean Catholic Apostolate's chaplain (article date as given in the URL).
- url: https://www.openstreetmap.org/way/663697115
  seen: 2026-09-28
  quote: addr:housenumber 17 addr:postcode 12205 addr:state NY addr:street Exchange Street amenity place_of_worship
  note: OpenStreetMap way 663697115, "Saint Francis De Sales Roman Catholic Church", at 42.68410, -73.78022;
    Nominatim places it in the Town of Colonie.
revisit: If the community starts posting its bulletin as a PDF or a readable page (or the pptx turns
  out to carry the weekly schedule and the pipeline can read it), make it a parish row with this church.
revisit_after: 2027-03-01
---

## Why it is excluded

The Korean Catholic Community of Albany (the diocese's Korean Apostolate) holds public Mass in
Korean every Sunday at 10 am in the former St. Francis de Sales Church, 17 Exchange Street
(directory, read 2026-09-28; the community's own cafe; The Evangelist). The building is in the
Town of Colonie per OpenStreetMap, with the Albany 12205 postal address every source uses. The
St. Francis de Sales parish itself is closed: the institutional-records index sends its
records to Christ Our Light, Loudonville; the church stays in use by the Korean community.

It is in scope (a place with public Mass) but publishes nothing the pipeline can read: its
only channel is a Daum cafe (a Korean portal forum rendered in JavaScript) whose "bulletin"
board carries one PowerPoint file per Sunday, the newest dated 27 September 2026. No PDF,
ParishesOnline, eCatholic or Discover Mass bulletin was found, and no Albany parish bulletin
read for this region lists the Korean Mass. So `no-bulletin`, not `closed`.

## What would change this

See `revisit`. If the pipeline can later read a .pptx behind the Daum viewer, the weekly
board could be the publication (`url:https://cafe.daum.net/kccalbany/bJaB`).
