---
name: Abbey Church of St. Gregory the Great (Portsmouth Abbey)
reason: no-bulletin
line1: 285 Cory's Lane
city: Portsmouth
state: RI
postal_code: 02871
decided: 2026-11-15
roster: ['gcatholic:39136']
evidence:
- url: https://www.portsmouthabbeymonastery.org/schedule
  seen: 2026-11-15
  quote: SUNDAY - 9:30 am ET
  note: 'The monastery''s eCatholic site (ecatholic:15150; 403 to probe url, read with visit.py): ''THE
    HOLY MASS / WEEKDAYS - 7:20 am ET / SUNDAY - 9:30 am ET'', ''VESPERS (Daily) - 5:30 pm ET'', ''Friday
    Adoration 1:30 pm - 5:00 pm''. Its header Mass Times widget shows ''Sunday Mass Schedule (Nov 15)
    9:30 AM'' with ''Get Directions'' to ''Portsmouth Abbey Church of St Gregory the Great and Queen of
    Peace, 285 Corys Lane''.'
- url: https://www.portsmouthabbeymonastery.org/
  seen: 2026-11-15
  note: 'Home page: ''Sunday Mass 9:30 am ET / Daily Mass 7:20 am ET / Vespers 5:30 pm ET''; its newsletter
    is ''The Current'' (web posts). visit.py found no bulletin link or PDF; issues.py ecatholic ecatholic:15150
    found no file at files.ecatholic.com/15150/bulletins for the four Sundays to 15 November 2026 (403
    each).'
- url: https://gcatholic.org/churches/usa-01/39136
  seen: 2026-11-14
  note: 'GCatholic 39136: St. Gregory, Abbatial Church, Portsmouth Abbey (Monastery), 285 Cory’s Lane,
    Portsmouth, Rhode Island 02871, Plus Code 87HCJP2H+FX. The diocesan finder does not list it.'
revisit: Check portsmouthabbeymonastery.org for a bulletin or PDF newsletter with the Mass schedule
revisit_after: 2027-05-01
research:
- method: visit.py on portsmouthabbeymonastery.org home, /schedule (--bulletin) and /plan-your-visit;
    issues.py ecatholic ecatholic:15150 --weeks 4
  url: https://www.portsmouthabbeymonastery.org/schedule
  checked: '2026-11-15'
  outcome: not-found
  next_action: Re-open the monastery site's menus for a bulletin or a PDF schedule; check whether 'The
    Current' becomes a PDF issue
  retry_when: The monastery site links a bulletin or PDF newsletter with its Mass schedule
---

## Why it is excluded

The abbey church of Portsmouth Abbey (Benedictine monastery and school; GCatholic 39136, "Abbatial Church", not in the diocesan finder) holds Mass that the monastery advertises to the public: its schedule page (https://www.portsmouthabbeymonastery.org/schedule, read 2026-11-15) gives "THE HOLY MASS / WEEKDAYS - 7:20 am ET / SUNDAY - 9:30 am ET", and its site header has a Mass Times widget ("Sunday Mass Schedule (Nov 15) 9:30 AM") with directions to the church at 285 Cory's Lane and a live stream. So it is open with public Mass.

It publishes no bulletin the pipeline could read: the site (eCatholic 15150) links none, its newsletter "The Current" is web posts, and no file exists at files.ecatholic.com/15150/bulletins for the Sundays 25 October to 15 November 2026. It was never a parish row, so it is recorded here as `no-bulletin`, not as a church.

Whether the monastery's Mass counts as public was judged from the site's own public Mass-times listing and directions; no source says the Mass is closed to visitors.

## What would change this

A bulletin or PDF newsletter carrying the abbey church's Mass schedule (for example if "The Current" were issued as a PDF): then it becomes a parish row of its own with this church.
