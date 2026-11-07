---
name: Jesus Christ, Prince of Peace Chapel (William Paterson University)
reason: no-bulletin
line1: 219 Pompton Road
city: Haledon
state: NJ
postal_code: 07508
decided: 2026-11-04
roster: ['directory:12280']
evidence:
- url: https://wpuprinceofpeace.org/
  seen: 2026-11-04
  quote: Prince of Peace Chapel at 6:00 PM
  note: Read with visit.py --text (probe url gets 403). eCatholic site 12280, title 'Prince of Peace Chapel,
    Wayne'; header '219 Pompton Rd, Haledon NJ'; under 'Sunday Mass Schedule' the quoted line; 'Confession
    Times Sundays 5:30 PM (during academic year)'; Wednesday Adoration 5:00-7:00 PM '*during the semester';
    its calendar has 'POP Mass' on Sundays 1 and 8 November 2026. visit.py --bulletin found no bulletin
    link or PDF on the site.
- url: https://wpuprinceofpeace.org/the-prince-of-peace-chapel
  seen: 2026-11-04
  quote: Jesus Christ, Prince of Peace Chapel and the Bishop Rodimer Catholic Campus Ministry Center exist
    to serve the students, faculty and staff of William Paterson University.
  note: Read with visit.py --text.
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: Finder pin directory:12280 'Prince of Peace Chapel, Wayne', no address, no coordinates and no
    Mass times; website wpuprinceofpeace.org.
- url: https://nominatim.openstreetmap.org/search?q=219+Pompton+Road+Haledon+NJ&format=json&limit=5
  seen: 2026-11-04
  note: OSM way 1364993958, a house-class feature at 219 Pompton Road, Haledon 07508, 40.94048, -74.19565
    (the campus edge on Pompton Road). No OSM feature named Prince of Peace Chapel was found.
revisit: Check wpuprinceofpeace.org for a bulletin, newsletter or schedule document the pipeline could
  read; if one appears, make the chapel a parish row with its own church
revisit_after: 2027-02-01
research:
- method: visit.py --bulletin and --text on wpuprinceofpeace.org (home page and The Prince of Peace Chapel
    page)
  url: https://wpuprinceofpeace.org/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Look again on wpuprinceofpeace.org for a bulletin, newsletter or schedule PDF
  retry_when: The site adds a bulletin or newsletter link, or a nearby parish bulletin starts listing
    the chapel's Mass
  revisit_after: 2027-02-01
---

## Why it is excluded

Jesus Christ, Prince of Peace Chapel is William Paterson University's Catholic campus chapel, with the Bishop Rodimer Catholic Campus Ministry Center, at 219 Pompton Road, Haledon (the finder calls it "Prince of Peace Chapel, Wayne": the campus spans Wayne and Haledon, and the site's own header gives Haledon). Its site (eCatholic 12280, read 2026-11-04) lists a Sunday Mass, "Prince of Peace Chapel at 6:00 PM", with confession on Sundays at 5:30 PM "during academic year", and its calendar shows "POP Mass" on 1 and 8 November 2026. The site describes the chapel as serving "the students, faculty and staff of William Paterson University"; the Mass is advertised openly on the public site, so it is treated as a campus chapel with public Mass (README: campus chapels count). It publishes no bulletin the pipeline could read: `visit.py --bulletin` found no bulletin page, PDF or publisher link, and the schedule is HTML only. No bulletin in this batch lists it, and the finder pin has no address or Mass times. So it is open with Mass but nothing to read: `no-bulletin`.

## What would change this

A bulletin, newsletter or schedule document on wpuprinceofpeace.org (or a parish bulletin that lists the chapel's Mass) would make it a church; see `research`. The schedule is for the academic year: if a later check finds no Sunday Mass in term time, check whether the chapel still has Mass. Coordinates were not recorded here; OSM has only the 219 Pompton Road house-class feature, not the chapel building.
