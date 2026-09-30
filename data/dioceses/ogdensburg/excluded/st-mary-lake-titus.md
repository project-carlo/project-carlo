---
name: St. Mary
reason: closed
line1: 753 County Route 41
city: Lake Titus
state: NY
postal_code: '12953'
decided: 2026-09-30
roster:
- gcatholic:18300
evidence:
- url: https://gcatholic.org/churches/usa-02/18300
  seen: 2026-09-30
  quote: 753 County Route 41, Lake Titus, New York 12953
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Ogdensburg as ''St. Mary'', 753
    County Route 41, Lake Titus, NY, 12953; kind: Church'
- url: http://standres.org/
  seen: &id001 2026-09-30
  quote: the last regularly scheduled Masses were offered in St. Joseph’s and St. Mary’s in 2007
  note: 'St. André Bessette parish website, History: "St. Helen’s would go on to establish mission churches
    in the surrounding communities of Mountain View (St. Elizabeth’s, 1907), Owls Head (St. Joseph’s,
    1923), and Lake Titus (St. Mary’s, 1925); St. Elizabeth’s closed in 1959, and the last regularly scheduled
    Masses were offered in St. Joseph’s and St. Mary’s in 2007."'
- url: https://container.parishesonline.com/bulletins/06/0038/20260927B.pdf
  seen: *id001
  quote: Notre Dame and St. Helen’s Churches
  note: '27 September 2026 masthead and schedule: no Lake Titus Mass. "Titus" appears in none of the 17
    issues from 7 June to 27 September 2026.'
- url: https://gcatholic.org/churches/usa-02/18300
  seen: *id001
  note: GCatholic lists "St. Mary", 753 County Route 41, Lake Titus (no coordinates). That address is
    two numbers from the directory's address for St. Helen's (755 County Highway 41, Chasm Falls), so
    it is probably a placeholder.
parish: st-andre-bessette-malone
---

## Why it is excluded

St. Mary's, Lake Titus (GCatholic: 753 County Route 41) was a mission of St. Helen's, Chasm Falls, founded in
1925. The parish website's history says "the last regularly scheduled Masses were offered in St. Joseph's
and St. Mary's in 2007", and no 2026 bulletin of St. André Bessette Parish has a Mass there (17 issues from 7
June to 27 September 2026, no "Titus" in any). "Regularly scheduled" leaves room for an occasional Mass; no
source says the building was closed, sold or relegated, so `last_mass` is left blank. I filed it as `closed`
rather than `open` because the parish itself lists only Notre Dame and St. Helen's as its churches and
its 2026 schedules are complete for the weekend. GCatholic's address, 753 County Route 41, is two numbers from
St. Helen's (755 County Highway 41) and unlikely to be the lake chapel's; the real location was not found.

## What would change this

An occasional or summer Mass at the chapel in a bulletin (it would become a church row under
`st-andre-bessette-malone`, "summer only" if seasonal). Owls Head's St. Joseph's, the other 2007 mission, is
in neither roster and was not given a record.
