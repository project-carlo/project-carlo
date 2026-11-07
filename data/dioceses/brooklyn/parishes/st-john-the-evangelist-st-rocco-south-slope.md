---
name: St. John the Evangelist - St. Rocco (South Slope)
website: https://stjohnstrocco-brooklyn.org/
bulletin_provider: other
provider_id: page-pdfs https://stjohnstrocco-brooklyn.org/bulletins
publication: []
group: Deanery B4 (Brooklyn West)
evidence:
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMjcvNHd0ZXh5bWlkbV9Ob3ZlbWJlcl8xXzIwMjZfQWxsX3NhaW50cy5wZGYiXV0/November%201%2C%202026%20-%20All%20saints.pdf
  seen: 2026-11-06
  quote: 250 21st Street  Brooklyn, New York 11215
  note: '1 November 2026 issue (5 pages, text, self-made: no LPi footer, no ad pages). Page 1 masthead
    ''Saint John the Evangelist -Saint Rocco Roman Catholic Parish'', pastor ''Rev. Kevin P. Cavalluzzi,
    D.Min.''; MASS SCHEDULE Sunday English 8:45 a.m., Spanish 10:00 a.m.; Monday - Thursday English 8:30
    a.m.; Friday Spanish 7:30 p.m. No 27th Street address anywhere in the issue (grep ''27th'': none).'
- url: https://stjohnstrocco-brooklyn.org/mass-times
  seen: 2026-11-06
  quote: All Masses take place at 250 21st Street, between 5th & 6th Avenues.
  note: 'Parish Mass Times page: Sunday 8:45am (English), 10am (Spanish); Monday-Thursday 8:30am; Friday
    7:30pm (Spanish).'
- url: https://stjohnstrocco-brooklyn.org/about/history
  seen: 2026-11-06
  quote: On May 20, 2011, Bishop Nicholas DiMarzio issued a decree uniting the parishes of Saint John
    the Evangelist and Saint Rocco. The parishes merged on June 30, 2011.
research:
- method: fetch:check other page-pdfs on the Tilma /bulletins page
  url: https://stjohnstrocco-brooklyn.org/bulletins
  checked: '2026-11-06'
  outcome: found
bulletin_status: available
---

## Publisher

The parish publishes its own weekly bulletin (self-made, 5 pages, no LPi footer or ad pages) on its Tilma webstudio site's `/bulletins` page. I read the 1 November 2026 issue (2026-11-06): page 1 masthead "Saint John the Evangelist -Saint Rocco Roman Catholic Parish", parish office "250 21st Street Brooklyn, New York 11215", pastor Rev. Kevin P. Cavalluzzi. No publisher container, so no publication id.

## Worship sites

One church, St. John the Evangelist at 250 21st Street. The bulletin's MASS SCHEDULE (Sunday 8:45 a.m. English, 10:00 a.m. Spanish; Monday-Thursday 8:30 a.m.; Friday 7:30 p.m. Spanish) gives no other place, and the parish's Mass Times page says "All Masses take place at 250 21st Street, between 5th & 6th Avenues." The parish history says the two parishes merged on 30 June 2011. The former St. Rocco church (216 27th Street), which GCatholic 16773 still lists, has its own `excluded/` record (`st-rocco-south-slope`). Mass finder 905 gives this parish's name with the 27th Street address but pins 250 21st Street; it is linked to the St. John church.

## Website and bulletin provider

`other`, recipe `page-pdfs https://stjohnstrocco-brooklyn.org/bulletins`. `fetch:check` (2026-11-06) resolved it to the 1 November 2026 issue ("November 1st, 2026" in the text; freshness `fresh`), transport ok, a PDF; it is the newest card on the page, and the 8 November issue was not yet posted on Friday 6 November.

## Not yet confirmed

Nothing open.
