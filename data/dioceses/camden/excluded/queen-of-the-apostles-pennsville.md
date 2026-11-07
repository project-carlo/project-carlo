---
name: Queen of the Apostles
reason: closed
line1: 391 S Broadway
city: Pennsville
state: NJ
postal_code: 08070
decided: 2026-10-29
roster: ['gcatholic:37921']
evidence:
- url: https://www.camdendiocese.org/decrees-establishing-st-gabriel-the-archangel-parish-and-the-parish-of-all-saints-on-oct-29/
  seen: 2026-10-29
  quote: Queen of the Apostles and St. Mary also will be used as worship sites for the new parish.
  note: 'Diocese news, 2010-10-29: the church was a worship site of St. Gabriel the Archangel Parish when
    it was established.'
- url: https://irp.cdn-website.com/f0e3bb89/files/uploaded/BULLETIN+10.25.26+FINAL.pdf
  seen: 2026-10-29
  note: The 25 October 2026 bulletin's Mass schedule lists Corpus Christi (Carneys Point) and St. Mary’s
    (Salem) only; a text search of the whole issue for Pennsville, Queen and Apostles found no church
    mention (the one 'Pennsville' in the 4 October issue is 'Riverview Beach Park, Pennsville'). The parish's
    Mass Times page also lists only those two churches.
- url: https://www.nj.com/salem/2016/09/at_south_jersey_catholic_church_an_emotional_day_a.html
  seen: 2026-11-07
  quote: The final Sunday service on Aug. 28 saw the church full
  note: 'nj.com, published 2016-09-04 (Bill Gallo Jr.). Behind a 403 to probe get and a paywall: read
    in the browser (parish-site-access visit.py --text). Also: ''no more regular Masses will be held at
    the Catholic church on South Broadway''; the church ''will be used as a worship site for funerals,
    weddings and other special Masses and services''.'
parish: st-gabriel-the-archangel-carneys-point
last_mass: 2016-08-28
research:
- method: probe get on the nj.com article, then the Wayback Machine copy
  url: https://www.nj.com/salem/2016/09/at_south_jersey_catholic_church_an_emotional_day_a.html
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: Read the article text and take the day of the final Mass from it; set last_mass to that
    date.
  retry_when: nj.com stops answering 403 to probe get, or a browser read of the page is permitted
- method: 'Hand refresh against main: probe get on the article (still 403), then parish-site-access visit.py
    --text, which rendered the article (published 2016-09-04, by Bill Gallo Jr.)'
  url: https://www.nj.com/salem/2016/09/at_south_jersey_catholic_church_an_emotional_day_a.html
  checked: '2026-11-07'
  outcome: found
---

## Why it is excluded

**Queen of the Apostles, 391 S Broadway, Pennsville — closed to regular Mass, final Sunday Mass 28 August 2016.** GCatholic (37921) still lists it as a church with no parish group, and the diocese's 2010 decree made it a worship site of St. Gabriel the Archangel Parish. The nj.com story 'At South Jersey Catholic church, an 'emotional' day as final Mass is held' (published 2016-09-04; read in the browser with visit.py on 2026-11-07, as `probe get` gets 403) says 'The final Sunday service on Aug. 28 saw the church full', that 'no more regular Masses will be held at the Catholic church on South Broadway', according to diocese spokesman Michael Walsh, and 'With the Queen of the Apostles closed'. The parish's current bulletin (25 October 2026) and its Mass Times page list Mass at Corpus Christi and St. Mary's only.

The same article quotes the diocese that the church 'will be used as a worship site for funerals, weddings and other special Masses and services', with no plans to sell it. Those are occasional private or family services, not a public Mass schedule, so the row stays `closed` (no Mass any more on any schedule), not a church. Earlier, only a search snippet of this article had been read, and `last_mass` was given as the month of publication (2016-09); the article gives 28 August.

## What would change this

A bulletin or parish page listing Mass in Pennsville, or a source that reads the building as in regular use again. Discover Mass still lists 'St. Gabriel the Archangel Parish – Queen of the Apostles Church' with no times or bulletins and the COVID-19 notice; that is a stale listing, not evidence of Mass.
