---
name: Infant Jesus Shrine
revisit: Confirm current Mass times with the shrine (716-694-4313) or its own site (northtonawanda.sac.org.pl),
  and look for a Polish-language bulletin there.
revisit_after: 2027-03-01
roster: ['gcatholic:33107']
evidence:
- url: https://discovermass.com/church/infant-jesus-shrine-wheatfield-ny/
  seen: 2026-11-16
  quote: Sunday 9:00am , 10:00am , 11:00am , 4:00pm
  note: Discover Mass church page ("Powered by MassTimes.org"), under a "Mass Times during COVID-19" banner;
    it also lists "Saturday 9:30am , 4:00pm" and "Weekdays 9:30am , 4:00pm", and "There are currently
    no bulletins available for Infant Jesus Shrine."
- url: https://gcatholic.org/churches/usa-02/33107
  seen: 2026-11-16
  quote: 'Served by: Pallottines'
  note: 'GCatholic''s page: ''Shrine of the Holy Infant Jesus'', Languages: English, Polish; Telephone
    +1 (716) 694-4313; website northtonawanda.sac.org.pl.'
- url: https://www.buffalodiocese.org/wp-content/uploads/DOB_CatholicDirectory.pdf
  seen: 2026-11-24
  quote: 'Sundays and Holydays: 9 a.m., 10 a.m. (Polish),'
  note: 'The diocese''s Official Catholic Directory, dated September 2025, page 54 (Shrines): Infant Jesus
    Shrine, conducted by the Pallottine Fathers, Director Rev. John Posiewala, SAC; Sundays and Holydays
    9 a.m., 10 a.m. (Polish), 11 a.m. and 4 p.m.; weekdays 9:30 a.m. and 4 p.m. These agree with Discover
    Mass''s times, so those are not only COVID-era data, but nothing dated 2026 confirms them.'
line1: 3452 Niagara Falls Blvd.
city: North Tonawanda
state: NY
postal_code: '14120'
research:
- method: probe url and visit.py on northtonawanda.sac.org.pl; web search; Discover Mass page
  url: http://northtonawanda.sac.org.pl
  checked: '2026-11-16'
  outcome: access-blocked
  next_action: Open the shrine site in a browser that accepts its certificate, or call the shrine
  retry_when: The shrine site loads
- method: probe get over http; Wayback CDX for northtonawanda.sac.org.pl; web search
  url: http://northtonawanda.sac.org.pl
  checked: '2026-11-24'
  outcome: access-blocked
  next_action: Find the shrine's current site or Facebook page (the Pallottines' sac.org.pl site was last
    archived in 2008), or call 716-694-4313
  retry_when: A current site or Facebook page for the shrine is found
---

## What is known

The Shrine of the Holy Infant Jesus, 3452 Niagara Falls Blvd., North Tonawanda (Wheatfield), is run by the Pallottines (Polish province) with Masses in English and Polish (GCatholic). Its Mass times are published only by Discover Mass, from MassTimes.org data under a COVID-era banner, so they may be years old. Its own site (northtonawanda.sac.org.pl) failed to load: the certificate doesn't match the host, and a browser couldn't open it on 16 November 2026. No bulletin was found (Discover Mass has none). It isn't on the diocese's finder or Mass-times pages: as a Pallottine shrine it may not be under a diocesan family.

## Mass times published

- https://discovermass.com/church/infant-jesus-shrine-wheatfield-ny/ (seen 2026-11-16): "Saturday 9:30am , 4:00pm"; "Sunday 9:00am , 10:00am , 11:00am , 4:00pm"; "Weekdays 9:30am , 4:00pm" (MassTimes.org data; age unknown, possibly COVID-era). Other directories found by search give fewer Masses, including a Sunday 10 a.m. Polish Mass, so treat these times as unconfirmed.

## Why it is not decided

Under the owner's rule of 16 November 2026, a place whose public Mass is listed online but which publishes no bulletin is kept open here, not excluded as `no-bulletin`, so a coming feature can show it from the published times. `open/` is the closest status the CLI has: it keeps the place off the site and on the work list.
