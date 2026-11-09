---
name: Mount Alvernia Retreat Center
reason: no-bulletin
line1: 158 Delavergne Ave.
city: Wappingers Falls
state: NY
postal_code: '12590'
decided: 2026-11-08
roster: ['gcatholic:149070']
evidence:
- url: https://gcatholic.org/churches/usa-02/149070
  seen: 2026-10-06
  quote: 158 Delavergne Ave., Wappingers Falls, New York 12590
  note: 'Listed in GCatholic: churches of the Archdiocese of New York as ''(Mount Alvernia Retreat Center)'',
    158 Delavergne Ave., Wappingers Falls, NY, 12590; kind: Mount Alvernia Retreat Center'
- url: https://mtalvernia.org/
  seen: 2026-11-08
  quote: SUNDAY MASSES
  note: 'Homepage (headed Chrome): Franciscan Friars (OFM) retreat center at 158 Delavergne Ave.; Sunday
    Masses 8:30 AM and 10:00 AM, weekday Masses Monday-Saturday 8:00 AM. Its menu links (Prayer Resources,
    News and Messages) carry prayer texts and external news, not a bulletin.'
- url: https://www.church-bulletin.org/bulletin/church-of-saint-mary-wappingers-falls-ny-12590/2026-11-08.pdf
  seen: 2026-11-08
  note: The November 8, 2026 bulletin of St. Mary, Wappingers Falls (the parish in the same town) does
    not mention Mt. Alvernia, Delavergne Ave. or the friars.
research:
- method: headed-Chrome read of mtalvernia.org (homepage links filtered for bulletin, newsletter, PDF);
    grep of the St. Mary Wappingers Falls November 8 bulletin
  url: https://mtalvernia.org/
  checked: '2026-11-08'
  outcome: not-found
  next_action: Look for a bulletin or weekly PDF on mtalvernia.org, or the friary's Mass in a nearby parish
    bulletin
  retry_when: mtalvernia.org adds a bulletin, newsletter or schedule PDF link
  revisit_after: 2027-05-01
---

## Why it is excluded

Mt. Alvernia is a retreat center of the Franciscan Friars (OFM) at 158 Delavergne Ave., Wappingers Falls, with public Mass: its homepage (read 2026-11-08) lists Sunday Masses at 8:30 and 10:00 AM and weekday Masses Monday to Saturday at 8:00 AM, with confession before or after Mass. It is not a parish and publishes no bulletin the pipeline could read: the site's Prayer Resources and News and Messages pages carry prayer texts and outside news (checked October 8 and again today), and it has no bulletin, newsletter or schedule PDF link. No parish bulletin carries its Masses either: the November 8, 2026 bulletin of St. Mary, Wappingers Falls does not mention it. So it is excluded as `no-bulletin`, not closed: Mass continues there.

## What would change this

A weekly bulletin or schedule PDF on mtalvernia.org, or a nearby parish's bulletin listing the friary's Masses, would make it a church (under that publisher, or as its own row).
