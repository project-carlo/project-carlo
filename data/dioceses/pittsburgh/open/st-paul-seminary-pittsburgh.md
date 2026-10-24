---
name: St. Paul Seminary (Holy Family of Nazareth Chapel)
revisit: Ask the seminary office (412-456-3048) or read a seminary/diocesan page whether its chapel Masses
  are open to the public; if a public schedule appears, add a church row (under whichever bulletin prints
  it, else exclude as no-bulletin)
revisit_after: 2027-01-31
roster: ['gcatholic:40411']
evidence:
- url: https://pghpriest.com/st-paul-seminary
  seen: 2026-10-23
  quote: where seminarians gather daily for prayer, Mass, and formation, and where the entire seminary
    community comes together to worship
  note: Vocations office page (read in headed Chrome; 403 to curl). The Holy Family of Nazareth Chapel
    is 'the spiritual heart of St. Paul Seminary'; 'daily Mass' is part of the seminary's horarium. It
    gives no schedule and does not say whether outsiders may attend.
- url: https://diopitt.org/seminary
  seen: 2026-10-23
  quote: Diocesan Pastoral Center 2900 Noblestown Road Pittsburgh, PA 15205-4227
  note: Diocese page for Saint Paul Seminary (rector Very Rev. Thomas A. Sparacino, (412) 456-3048). No
    Mass times on the page (read with visit.py, 1,602 characters of body text).
- url: https://gcatholic.org/churches/usa-03/40411
  seen: 2026-10-23
  quote: 2900 Noblestown Rd., Pittsburgh, Pennsylvania 15205
  note: 'GCatholic: ''St. Paul'', kind Seminary, founded 1965, website stpaulsem.org (dead DNS 2026-10-23).'
line1: 2900 Noblestown Rd.
city: Pittsburgh
state: PA
postal_code: '15205'
research:
- method: 'Searched the diocese directory and Mass Finder rosters for ''seminary'' (no entry); read diopitt.org/seminary,
    pghpriest.com/st-paul-seminary and GCatholic; DuckDuckGo searches for a public Mass schedule (only
    the Saint Paul Seminary of St. Paul, Minnesota, saintpaulseminary.org, came up with public Mass times:
    a different seminary); probed stpaulsem.org, stpaulseminary.edu, stpaulsem.edu and seminary.diopitt.org
    (all DEAD-DNS); Catholic Index page (Cloudflare challenge, third-party aggregator, not used)'
  url: https://diopitt.org/seminary
  checked: '2026-10-23'
  outcome: not-found
  next_action: Phone the seminary office, (412) 456-3048, or find a seminary page or a parish bulletin
    that prints chapel Mass times and says whether the public may attend
  retry_when: A diocesan or parish page lists the chapel's Mass times, or the diocese's Mass Finder adds
    the seminary
  revisit_after: 2027-01-31
---

## What is known

St. Paul Seminary, 2900 Noblestown Road (Crafton, Pittsburgh 15205) is the diocese's pre-theology seminary (founded 1965) and shares the site with the Diocesan Pastoral Center. Its Holy Family of Nazareth Chapel (renovated 2014) is where the seminarians have daily Mass; a maryqueenofsaints.org news item (search snippet seen 2026-10-23, undated) says Bishop Zubik live-streamed daily Mass from its chapel while parish Masses were resuming. GCatholic lists it (40411). The Mass Finder, the diocese directory and the parish bulletins read so far list no Mass there.

The similarly named Saint Paul Seminary at saintpaulseminary.org publishes public daily Mass times for St. Mary's Chapel; that is the St. Paul, Minnesota seminary and not this one.

## Why it is not decided

Rule 1 of the diocese's settled rules: a place with public Mass no bulletin prints is `no-bulletin`; a chapel with only community or private Masses is `no-public-mass`; with nothing found, `open/`. The sources show daily Mass for the seminary community but nothing says whether the public may attend or when, and no Mass times are printed anywhere read. The seminary's own website is gone (stpaulsem.org does not resolve), and the diocese page lists staff only. Next step: ask the seminary office or find a published chapel schedule. Do not infer public Mass from the word 'Mass' in a description of seminary life.
