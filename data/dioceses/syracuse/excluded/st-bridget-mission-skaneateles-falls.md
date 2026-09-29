---
name: St. Bridget Mission
reason: closed
line1: ''
city: Skaneateles Falls
state: NY
postal_code: '13153'
parish: st-mary-of-the-lake-skaneateles
decided: 2026-09-26
roster: ['directory:36318']
evidence:
- url: https://www.syracusediocese.org/parishes
  seen: 2026-09-26
  quote: St. Bridget Mission, Skaneateles Falls (CLOSED - See St. Mary of the Lake, Skaneateles)
  note: The diocese's alphabetical parish list (behind Cloudflare; read in a browser, copy in the orchestrator's
    scratchpad diocese-parish-list.txt). The parish finder lists it as "St. Bridget Mission (Closed)"
    with no address and a 0,0 map pin.
- url: https://www.syracusediocese.org/st-mary-of-the-lake-skaneateles
  seen: 2026-09-26
  quote: St. Bridget Mission, Skaneateles Falls are retained here.
  note: The successor's page on the diocese site ("Sacramental Records for St. Bridget Mission, Skaneateles
    Falls are retained here."; behind Cloudflare, read with parish-site-access visit.py).
- url: https://www.stmarysskaneateles.com/mass-schedule
  seen: 2026-09-26
  quote: Saturday Vigil 4:30pm Sunday 8:00am & 10:15am
  note: The successor's Mass schedule page. Weekend, weekday (Tuesday to Friday 8:15am), communion service
    and reconciliation times, all at St. Mary's, 10 West Austin Street; nothing in Skaneateles Falls.
    The 27 September 2026 bulletin masthead (ParishesOnline 06/0119, page 1, an image) gives the same
    schedule and only St. Mary's.
- url: https://www.stmarysskaneateles.com/history
  seen: 2026-09-26
  quote: To serve Catholics in Skaneateles Falls, he also founded St. Bridget’s Mission Church in 1874.
  note: The successor's history page. It says St. Mary's today "serves approximately 1,200 families from
    Skaneateles, Skaneateles Falls, and the surrounding area" and says nothing of St. Bridget's closure.
---

## Why it is excluded

The diocese's parish list says the mission closed ("St. Bridget Mission, Skaneateles Falls
(CLOSED - See St. Mary of the Lake, Skaneateles)"), and the diocese keeps its sacramental
records at St. Mary of the Lake. The successor's current Mass schedule (its site and its
27 September 2026 bulletin) has Mass only at St. Mary's in Skaneateles, and its history page,
which tells of Fr. Purcell founding St. Bridget's in 1874, now describes St. Mary's as serving
Skaneateles Falls families from Skaneateles. So the parish closed and its successor holds no
Mass in Skaneateles Falls.

No date for the last Mass was found (the Catholic Sun's 16 September 2026 article on St. Mary's
175th anniversary mentions St. Bridget's 1874 dedication only), so `last_mass` is empty. No
source gave the building's street address; GCatholic does not list it, so the record has the
hamlet (ZIP 13153) only.

## What would change this

Nothing expected. A dated closure notice would fill in `last_mass`.
