---
name: Our Lady of the Skies Chapel (JFK Airport)
reason: no-bulletin
line1: JFK International Airport, Terminal 4, Suite 461-037
city: Jamaica
state: NY
postal_code: '11430'
decided: 2026-11-06
roster: ['gcatholic:16802', 'directory:our-lady-of-the-skies-chapel', 'massfinder:999']
evidence:
- url: https://www.jfkchapel.org/services
  seen: 2026-11-06
  quote: Saturday's at 5:00 PM (Vigil Mass)
  note: '''Masses at Our Lady of the Skies'': Monday''s, Tuesday''s and Friday''s at 12:45 PM, Saturday''s
    at 5:00 PM (Vigil Mass), Sunday''s at 12:45 PM. Footer: JFK International Airport, Terminal 4, Suite
    461-037, Jamaica, New York 11430.'
- url: https://www.jfkchapel.org/location
  seen: 2026-11-06
  quote: We are PRE-SECURITY, which means that anyone can have access to our Chapel.
  note: The chapel is on the 4th floor (Departure Floor) of Terminal 4 and open 6:00 AM to 10:00 PM daily.
- url: https://www.jfkchapel.org/
  seen: 2026-11-06
  note: 'Wix site (menu: Our Chapel, Mass Schedule, History, Strollers, Prayer Room, Takeoff, Guild, News,
    Calendar, Request Mass Intention, Visit Us, Contact Us). The homepage, /services, /location, /news,
    /takeoff (a podcast and vlog), /what-we-offer and /calendar link no bulletin, newsletter or PDF; probe
    url found no publications or publishers. ParishesOnline has no org our-lady-of-the-skies-11430 (the
    org ''our-lady-of-the-skies'' is the Nellis AFB chapel in Nevada).'
- url: https://gcatholic.org/churches/usa-02/16802
  seen: 2026-11-05
  quote: Terminal 4 (4th floor departure level), JFK Airport, Jamaica, New York 11430
  note: GCatholic 16802 Our Lady of the Skies, Chapel, Plus Code 87G8J6V9+F3 (40.6437, -73.7823), 1955.
- url: https://dioceseofbrooklyn.org/directories/parishes/
  seen: 2026-11-05
  note: 'Diocese parish directory: Our Lady of the Skies Chapel, JFK International Airport, Terminal 4,
    4th Floor, Jamaica, NY 11430, (718) 656-5348, www.jfkchapel.org. Mass finder 999 lists the chapel
    with no address and a pin at 40.7055,-73.7949 (central Jamaica), not at the airport.'
---

## Why it is excluded

The chapel has public Mass but publishes no bulletin. Its own site, jfkchapel.org (read 2026-11-06), lists "Masses at Our Lady of the Skies" on Monday, Tuesday and Friday at 12:45 PM, Saturday 5:00 PM (Vigil) and Sunday 12:45 PM, and its location page says the chapel, on the 4th (departure) floor of Terminal 4, is pre-security: "anyone can have access to our Chapel". So the Mass is public, and under the diocese's settled rule for chaplaincy chapels it is a worship site. No page of the site (homepage, Mass schedule, location, news, Takeoff podcast, what we offer, calendar) links a bulletin, newsletter or PDF, and ParishesOnline has no organization for it. The schedule exists only as text on a Wix page, which `fetch` can't read as a bulletin, and no parish bulletin covers the airport. So it is `no-bulletin`, not `closed`.

The address is the site's own (Terminal 4, Suite 461-037); the directory and GCatholic 16802 agree on Terminal 4, 4th floor. Mass finder 999 gives no address and pins central Jamaica (40.7055, -73.7949), which is wrong for the chapel; GCatholic's Plus Code 87G8J6V9+F3 (40.6437, -73.7823) is in Terminal 4.

The site's news page also says the chaplaincy served LaGuardia but that "there are no regular Masses said at the airport" there now; no Brooklyn roster lists a LaGuardia chapel, so no record is made for it.

## What would change this

If the chaplaincy starts posting a bulletin or newsletter (a PDF on jfkchapel.org or a ParishesOnline container), the chapel becomes a parish row of its own with that bulletin. If the site drops the Mass schedule or says the chapel has closed, the reason becomes `closed` with the date.
