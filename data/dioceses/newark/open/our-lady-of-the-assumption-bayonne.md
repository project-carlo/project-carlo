---
name: Our Lady of the Assumption
revisit: 'Find a source that settles whether the church still holds any Mass: a St. John Paul II bulletin
  or site naming it (pages 3-6 of a recent issue, a feast-day or funeral notice), an archdiocese decree
  or property listing, or a news item on its closure or sale.'
revisit_after: 2027-02-01
roster: ['gcatholic:18354']
evidence:
- url: https://gcatholic.org/churches/usa-03/18354
  seen: 2026-11-03
  quote: 91 W 23rd St., Bayonne, New Jersey 07002
  note: GCatholic (last updated 2025-12-21) lists the Church of Our Lady of the Assumption, Plus Code
    87G7MV8H+6G, telephone +1 (201) 436-8160, website olassumption.org.
- url: https://en.wikipedia.org/wiki/Our_Lady_of_Mt._Carmel_(Bayonne,_New_Jersey)
  seen: 2026-11-03
  quote: in 2016 Our Lady of Mt. Carmel Parish merged with two other parishes (Our Lady of the Assumption
    and St. Michael & St. Joseph) into the present-day St. John Paul II Parish
- url: https://www.church-bulletin.org/bulletin/saint-john-paul-ii-parish-bayonne-nj-07002/2026-11-01.pdf
  seen: 2026-11-03
  note: Pages 1-2 of the 1 November 2026 St. John Paul II bulletin (image-only) name only the Church of
    Our Lady of Mount Carmel and give no other Mass location.
- url: http://www.olassumption.org
  seen: 2026-11-03
  note: 'probe url: SPAM-SQUAT (an Indonesian certification site); a Wayback snapshot of 2019-12-09 is
    already a Japanese spam page, so the domain lapsed by then.'
parish: st-john-paul-ii-bayonne
line1: 91 West 23rd Street
city: Bayonne
state: NJ
postal_code: '07002'
research:
- method: rcan.org WordPress search ('Assumption Bayonne', 'Bayonne church') and property search ('Bayonne')
  url: https://rcan.org/wp-json/wp/v2/search?search=Assumption%20Bayonne
  checked: '2026-11-03'
  outcome: not-found
  next_action: Search rcan.org again for a decree or property listing naming Our Lady of the Assumption,
    Bayonne
  retry_when: The archdiocese posts a new decree or the next map/reconcile pass
- method: St. John Paul II site pages (home, liturgy-schedule, our-patron-saint) and bulletin pages 1-2
  url: https://johnpaul2parish.com/liturgy-schedule
  checked: '2026-11-03'
  outcome: not-found
  next_action: Read pages 3-6 of a current bulletin (render.py) for any mention of the Assumption church
  retry_when: Next check of this row
---

## What is known

Our Lady of the Assumption parish merged with Our Lady of Mount Carmel and St. Michael & St. Joseph into St. John Paul II Parish in 2016 (Wikipedia; the archdiocese's records table lists it as 'Merged'). GCatholic (18354, updated 2025-12-21) still lists its church at 91 W 23rd St. The 1 November 2026 St. John Paul II bulletin and the parish's site name only the Church of Our Lady of Mount Carmel, with every Mass there. The church's own domain, olassumption.org, has been spam since at least 2019.

## Why it is not decided

The evidence is absence: no current schedule lists Mass at the Assumption church, but no decree, property listing or news item found says it closed or was sold (searched rcan.org and the parish site, 2026-11-03). Bulletin pages 3-6 were not read. A source stating closure would move it to `excluded/` as closed; a Mass listed there would make it a church of `st-john-paul-ii-bayonne`.
