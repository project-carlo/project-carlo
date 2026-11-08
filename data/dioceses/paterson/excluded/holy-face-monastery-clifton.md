---
name: Holy Face Monastery
reason: no-bulletin
line1: 1697 State Route 3
city: Clifton
state: NJ
postal_code: '07013'
decided: 2026-11-05
roster: ['gcatholic:37950']
evidence:
- url: https://holyfacemonastery.com/
  seen: 2026-11-05
  quote: Holy Mass Schedule
  note: 'Read with visit.py (the page is rendered by JavaScript; probe get returns only the title). ''Holy
    Mass Schedule ● Sunday 10:00 AM 11:30 AM ● Sunday Vespers & Benediction 3:30 PM ● Daily Mass (Monday
    to Saturday) 7:30 AM ● Tuesday 7:00 pm. Healing Mass & HolyFace of Jesus Novena ● Thursday 7:00 PM
    (Mass & St. Jude Novena)''; confessions Tuesday-Saturday 2:00-5:00 PM ''at Holy Face Chapel''. Its
    calendar lists ''Nov 8: 10:00 AM Sunday Mass 11:30 AM Sunday Mass''. Address in the footer: 1697 State
    Route 3.'
- url: https://holyfacemonastery.com/about
  seen: 2026-11-05
  quote: Holy Face Monastery is a dependent house of St. Benedict Priory in Oxford, Michigan
  note: 'Read with visit.py: Sylvestrine Congregation, O.S.B.; dedicated 20 December 1953; ''The celebration
    of Conventual Mass, Benediction and blessings, confessions ... add to the spiritual enrichment of
    those who come to us.'''
- url: https://holyfacemonastery.com/events
  seen: 2026-11-05
  note: 'visit.py --bulletin on /, /events, /worship, /visit and /about: no bulletin link, PDF link or
    publication id; the site gives its schedule as a web calendar only.'
- url: https://gcatholic.org/churches/usa-03/37950
  seen: 2026-11-04
  note: GCatholic 37950 'Holy Face', Monastery, 1697 State Route 3, Clifton 07013, Plus Code 87G7VR59+H8;
    website holyfacemonasterygiftshop.blogspot.com (404 on 2026-11-05). OSM node 357723503 'Holy Face
    of Jesus Monastery' (place_of_worship, Vincent Drive) is at 40.85911, -74.18201, about 35 m from the
    Plus Code.
revisit: Check holyfacemonastery.com for a weekly bulletin or newsletter PDF; if one appears, make the
  monastery a parish row with its own church
revisit_after: 2027-05-01
research:
- method: visit.py --bulletin and --text on holyfacemonastery.com (home, /events, /worship, /visit, /about);
    probe get on the GCatholic website holyfacemonasterygiftshop.blogspot.com (404)
  url: https://holyfacemonastery.com/
  checked: '2026-11-05'
  outcome: not-found
  next_action: Look again for a bulletin or newsletter PDF on holyfacemonastery.com, or a ParishesOnline/Discover
    Mass/Bon Venture listing for the monastery
  retry_when: The site adds a bulletin page or a publisher listing for the monastery turns up
  revisit_after: 2027-05-01
---

## Why it is excluded

Holy Face Monastery, 1697 State Route 3, Clifton (GCatholic 37950), a Sylvestrine Benedictine house dependent on St. Benedict Priory, Oxford, Michigan, holds public Mass: its home page (read 2026-11-05 with visit.py) gives a "Holy Mass Schedule" of Sunday 10:00 and 11:30 AM, daily Mass Monday-Saturday 7:30 AM and Tuesday and Thursday evening Masses, and its calendar lists the 8 November Sunday Masses. It publishes no bulletin: the site's home, events, worship, visit and about pages carry no bulletin link, PDF or publication id, only a web calendar, and GCatholic's listed website (a gift-shop blog) answers 404. No parish bulletin covers it either: a grep for "Holy Face" in the current issues of the four Clifton parishes nearby (St. Paul, Sts. Cyril & Methodius, Sacred Heart, St. Brendan & St. George) finds nothing. So it is open with public Mass but nothing the pipeline could read: `no-bulletin`. The diocese's finder has no pin for it.

## What would change this

A weekly bulletin or Mass schedule document on holyfacemonastery.com (or a publisher listing for the monastery) would make it a parish row with its own church; see `research`.
