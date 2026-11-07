---
name: St. Ann
reason: closed
line1: 155 Broad St.
city: Elmer
state: NJ
postal_code: 08318
decided: 2026-10-29
roster: ['gcatholic:18855']
evidence:
- url: https://www.camdendiocese.org/bishop-issues-decrees-establishing-parishes-in-hammonton-mullica-hill-and-north-cape-may/
  seen: 2026-10-29
  quote: St. Joseph Church also will be used as a worship site by the new parish.
  note: 'Diocese news, 2010-05-21: the decree names Holy Name of Jesus Church as the location and St.
    Joseph Church as the one other worship site; St. Ann, Elmer is not named.'
- url: https://holyspiritweb.org/history/
  seen: 2026-10-29
  quote: Currently there is two campuses (Woodstown and Mullica Hill) and the churches of St. Joseph and
    Holy Name of Jesus are still in use.
  note: The parish's History page; its St. Ann section ends with the 2010 merger and does not give a closing.
- url: https://www.church-bulletin.org/bulletin/the-catholic-community-of-the-holy-spirit-mullica-hill-nj-08062/2026-11-01.pdf
  seen: 2026-10-29
  note: The 1 November 2026 bulletin's Mass schedule lists Mullica Hill, Woodstown and St. Joseph only;
    searched for 'St. Ann' and 'Elmer' (the one hit is an advertiser's Elmer address).
- url: https://www.nj.com/salem/2016/09/at_south_jersey_catholic_church_an_emotional_day_a.html
  seen: 2026-11-07
  quote: St. Ann's Church in Elmer was permanently closed
  note: 'nj.com, published 2016-09-04, in its story on Queen of the Apostles'' final Mass. Behind a 403
    to probe get and a paywall: read in the browser (parish-site-access visit.py --text). It gives no
    closing date.'
parish: the-catholic-community-of-the-holy-spirit
research:
- method: probe get on the nj.com article (403), Wayback copy (429), diocese and Catholic Star Herald
    REST searches for Elmer
  url: https://www.nj.com/salem/2016/09/at_south_jersey_catholic_church_an_emotional_day_a.html
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: Read the article and any 2010-2016 Catholic Star Herald notice for the final Mass date;
    set last_mass.
  retry_when: nj.com stops answering 403 to probe get, or a browser read of the page is permitted
- method: 'Hand refresh against main: parish-site-access visit.py --text rendered the nj.com article (probe
    get still 403); it says St. Ann''s ''was permanently closed'' and gives no date'
  url: https://www.nj.com/salem/2016/09/at_south_jersey_catholic_church_an_emotional_day_a.html
  checked: '2026-11-07'
  outcome: not-found
  next_action: Find a 2010-2016 Catholic Star Herald or Holy Spirit notice of St. Ann's final Mass; set
    last_mass
  retry_when: A notice of the final Mass at St. Ann, Elmer turns up
---

## Why it is excluded

**St. Ann, 155 Broad St., Elmer — closed before September 2016, final Mass date not found.** GCatholic (18855) lists it under 'Holy Spirit Parish'. The 2010 decree uniting Holy Name of Jesus, St. Joseph and St. Ann named only Holy Name of Jesus Church (the location) and St. Joseph Church as worship sites, and the parish's 1 November 2026 bulletin and Worship page list Mass at the Mullica Hill and Woodstown Parish Centers and St. Joseph Church only, though the page says the parish 'serves Elmer'. The 2016 nj.com story on Queen of the Apostles' final Mass (published 2016-09-04; read in the browser with visit.py on 2026-11-07, as `probe get` gets 403) says: 'Elsewhere in Salem County, St. Ann's Church in Elmer was permanently closed. Parishioners there are now part of the Catholic Community of the Holy Spirit.' It gives no date, so `last_mass` is empty.

## What would change this

A bulletin or page listing Mass in Elmer. A Catholic Star Herald or parish notice of the final Mass would give `last_mass`.
