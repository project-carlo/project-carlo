---
name: Our Lady of Providence Seminary
reason: no-public-mass
line1: 485 Mt. Pleasant Ave.
city: Providence
state: RI
postal_code: 02908
decided: 2026-11-15
roster: ['gcatholic:40413']
evidence:
- url: https://olpseminary.com/daily-schedule
  seen: 2026-11-15
  quote: Holy Mass 7:00am
  note: 'Seminary site (eCatholic 38798, behind Cloudflare; read with visit.py --html). ''Daily Schedules
    MONDAY - SATURDAY'' tabs give the seminarians'' horarium: ''Morning Meditation 6:30am Lauds 6:45am
    Holy Mass 7:00am Breakfast 7:30am Lunch 11:00am – 2:00pm Adoration 5:00pm Lectio Divina 5:30pm Vespers
    5:45pm Dinner 6:00pm ...'' and on one day ''Holy Mass 8:00am Breakfast 8:30am''. The page names no
    public Mass and gives no Sunday schedule. Footer: ''485 Mt. Pleasant Avenue Providence, RI 02908'',
    Rev. Ryan W. Connors, Rector.'
- url: https://gcatholic.org/churches/usa-01/40413
  seen: 2026-11-15
  note: 'GCatholic 40413 ''Our Lady of Providence Seminary'', Type: Seminary, 485 Mt Pleasant Ave., Providence
    02908, Plus Code 87HCRGQX+WG.'
- url: https://dioceseofprovidence.org/parishfinder
  seen: 2026-11-14
  note: The diocesan finder, which gives Mass times for its parishes and chapels, has no entry for the
    seminary.
research:
- method: visit.py --text on the seminary homepage, looking for a public Mass time (reconcile)
  url: https://olpseminary.com/
  checked: '2026-11-16'
  outcome: access-blocked
  next_action: Read olpseminary.com (home, Daily Schedule, news) for a Mass the public is invited to;
    a published public time makes the chapel a church row
  retry_when: The site loads in the browser (timed out twice, 180 s and 500 s, on 2026-11-16)
---

## Why it is excluded

Our Lady of Providence Seminary is the diocese's house of formation (GCatholic 40413, Type: Seminary). Its own Daily Schedule page (read 2026-11-15) places "Holy Mass 7:00am" (one day 8:00am) inside the seminarians' horarium, between "Lauds 6:45am" and "Breakfast 7:30am": a community Mass of the house, like a convent chapel's. The site advertises no Mass for the public and no Sunday Mass, the news pages mention only special liturgies (ordinations, the Mass of the Holy Spirit), and the diocesan finder doesn't list the seminary. This is a judgement from the schedule's form and those absences; no source says in words that the chapel is closed to the public.

## What would change this

A seminary or diocesan page inviting the public to a regular Mass in the chapel (a published Sunday or daily public Mass time).
