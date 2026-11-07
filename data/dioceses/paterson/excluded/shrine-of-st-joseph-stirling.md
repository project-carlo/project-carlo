---
name: Shrine of Saint Joseph
reason: no-bulletin
line1: 1050 Long Hill Rd.
city: Stirling
state: NJ
postal_code: 07980
decided: 2026-11-04
roster: ['gcatholic:33104']
evidence:
- url: https://www.shrineofsaintjoseph.com/
  seen: 2026-11-04
  quote: Mass is offered daily—Mon., Wed., Fri., Sat 8:00 am.
  note: 'Home page (read with parish-site-access visit.py --text) continues: Tue., Thu. 5:30 pm in English
    & Wed. 7:00 pm in Spanish; Sunday Masses at the 5:30 pm Vigil Mass on Sat., Sun. 8:00 English, 9:45
    English, 9:45 Spanish (Auditorium), 11:45 am Spanish. It says the Shrine was founded in 1924 by Fr.
    Thomas Augustine Judge and is owned and operated by Trinity Missions (Missionary Servants of the Most
    Holy Trinity).'
- url: https://gcatholic.org/churches/usa-03/33104
  seen: 2026-11-04
  quote: 1050 Long Hill Rd., Stirling, New Jersey 07980
  note: GCatholic 33104 'St. Joseph', Shrine, founded 1924, website shrineofsaintjoseph.com.
revisit: Check shrineofsaintjoseph.com for a bulletin or newsletter; if one appears, make the shrine a
  parish row with its own church
revisit_after: 2027-05-01
research:
- method: probe url and parish-site-access visit.py --bulletin on the shrine's Squarespace site; read
    its home page links
  url: https://www.shrineofsaintjoseph.com/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Look again for a bulletin or newsletter PDF on the site (menu, calendar page) or a ParishesOnline/Discover
    Mass listing for the shrine
  retry_when: The site adds a Bulletin or Newsletter page, or a publisher listing for the shrine turns
    up
  revisit_after: 2027-05-01
---

## Why it is excluded

The Shrine of Saint Joseph, 1050 Long Hill Rd., Stirling, holds public Mass: its home page (read 2026-11-04) says "Mass is offered daily—Mon., Wed., Fri., Sat 8:00 am. Tue., Thu. 5:30 pm in English & Wed. 7:00 pm in Spanish", with Sunday Masses at a Saturday 5:30 pm Vigil and Sunday 8:00 and 9:45 (English), 9:45 and 11:45 am (Spanish). It is owned and operated by Trinity Missions (Missionary Servants of the Most Holy Trinity), not by St. Vincent de Paul parish, whose 8 November 2026 bulletin schedules only its own church (see `st-vincent-de-paul-stirling`).

It publishes nothing the pipeline can read: `probe url` and `visit.py --bulletin` on 2026-11-04 found no bulletin links, PDFs or publisher ids on the site, and its menu (About, Visit, Calendar, Columbarium, Gift Shop, Men of Saint Joseph, etc.) has no bulletin or newsletter page. Its schedule is on the home page and a calendar page only. So it is `no-bulletin`, not a church row.

## What would change this

A bulletin or newsletter PDF from the shrine (on its site or a publisher such as ParishesOnline or Discover Mass) would make it a parish row of its own with this church. If a parish bulletin starts listing its Masses, it would join that parish's row.
