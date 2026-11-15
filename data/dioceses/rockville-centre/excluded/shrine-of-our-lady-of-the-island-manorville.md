---
name: Shrine of Our Lady of the Island
reason: no-bulletin
line1: 258 Eastport Manor Road
city: Manorville
state: NY
postal_code: '11949'
decided: 2026-11-13
roster: ['gcatholic:32371']
evidence:
- url: https://www.ourladyoftheisland.com/
  seen: 2026-11-13
  quote: Everyday at 11:30 AM (except Mondays) outdoors weather permitting otherwise Mass is indoors
  note: 'Shrine home page (Squarespace; read with visit.py) SCHEDULE: MASS everyday at 11:30 AM except
    Mondays; ''MISA EN ESPAÑOL Domingos a las 4pm''; Exposition Fridays after Mass; Confessions Fridays
    1:30 PM. Its November 2026 calendar adds a Filipino Mass at 2pm every First Sunday and a Thanksgiving
    Day Mass at 11:30 AM. No bulletin or newsletter is linked.'
- url: https://www.ourladyoftheisland.com/visit
  seen: 2026-11-13
  quote: 258 Eastport Manor Road
  note: 'Visit page address: ''258 Eastport Manor Road, Manorville, New York 11949''.'
- url: https://www.ourladyoftheisland.com/about-2
  seen: 2026-11-13
  quote: established by the Missionaries of the Company of Mary (the Montfort Fathers)
  note: 'About page: the shrine is run by the Montfort Fathers (SMM).'
- url: https://gcatholic.org/churches/usa-02/32371
  seen: 2026-11-12
  note: GCatholic shrine 'Our Lady of the Island', 'Eastport-Manor Rd., Eastport, New York 11941'; Plus
    Code 87G9R6XR+HG. Not in the diocesan locator or the diocese's Mass-times page.
- url: https://discovermass.com/church/shrine-of-our-lady-of-the-island-eastport-ny/
  seen: 2026-11-13
  note: 'Discover Mass church page exists (discovermass:shrine-of-our-lady-of-the-island-eastport-ny)
    but lists no bulletins (parish-site-access issues.py: ''no bulletins listed'').'
revisit: Check ourladyoftheisland.com and discovermass.com/church/shrine-of-our-lady-of-the-island-eastport-ny/
  for a bulletin the pipeline could read.
revisit_after: 2027-05-01
research:
- method: DuckDuckGo search for the shrine's Mass schedule and bulletin; visit.py of ourladyoftheisland.com
    home, Visit and About pages; issues.py on its Discover Mass page
  url: https://www.ourladyoftheisland.com/
  checked: '2026-11-13'
  outcome: not-found
  next_action: Look again on ourladyoftheisland.com and its Discover Mass page for a bulletin or newsletter
    PDF
  retry_when: The shrine site links a bulletin or newsletter, or Discover Mass lists issues
  revisit_after: 2027-05-01
---

## Why it is excluded

The Shrine of Our Lady of the Island, 258 Eastport Manor Road, Manorville (GCatholic files it under Eastport 11941), is open and has public Mass: its home page (read 2026-11-13) gives "MASS Everyday at 11:30 AM (except Mondays) outdoors weather permitting otherwise Mass is indoors" and "MISA EN ESPAÑOL Domingos a las 4pm", and its November 2026 calendar adds a Filipino Mass at 2pm every First Sunday. It publishes no bulletin: the Squarespace site links none, and its Discover Mass page (`discovermass:shrine-of-our-lady-of-the-island-eastport-ny`) lists no issues. It is run by the Montfort Fathers ("established by the Missionaries of the Company of Mary (the Montfort Fathers)", About page), not by a parish: the nearby Sts. Peter and Paul, Manorville also has a Montfort pastor (Rev. Matthew Considine, SMM), but its 8 November 2026 bulletin lists no shrine Mass, so the shrine is not that row's worship site. It was never a parish row, so it is recorded here as `no-bulletin`.

The diocesan locator and the diocese's Mass-times page do not list the shrine; GCatholic does (gcatholic:32371). The shrine's own address (Visit page) is recorded; GCatholic's "Eastport-Manor Rd., Eastport" is the same road without a number.

## What would change this

A bulletin or newsletter PDF on ourladyoftheisland.com or issues on its Discover Mass page would make it a parish row of its own (`other` or `discover_mass`) with the shrine as its church. If a parish bulletin (e.g. Sts. Peter and Paul's) began listing the shrine's Masses, the shrine would become that row's church.
