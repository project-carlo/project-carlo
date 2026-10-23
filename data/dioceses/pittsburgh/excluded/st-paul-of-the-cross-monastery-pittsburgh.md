---
name: St. Paul of the Cross Monastery (Passionist)
reason: no-bulletin
line1: 148 Monastery Ave.
city: Pittsburgh
state: PA
postal_code: '15203'
decided: 2026-10-23
roster: ['gcatholic:47063']
evidence:
- url: https://www.stpaulofthecrossmonastery.com/
  seen: 2026-10-23
  quote: Saturday Vigil - 5:00pm Sunday - 8:00am & 10:00am
  note: 'Home page of the monastery''s Google Site (updated 10-25-2026): ''MASS SCHEDULE'' Saturday vigil
    5:00pm, Sunday 8:00am and 10:00am, Monday 10 am and 2 pm (Novena Service), Tuesday 7:30am and 12:10pm,
    Wednesday 12:10pm, Thursday and Friday 7:30am and 12:10pm, Saturday 8:00am; address ''148 Monastery
    Avenue Pittsburgh, PA 15203''; ''To purchase Mass Cards, Click Here''. Public Mass, weekly intentions
    below.'
- url: https://www.stpaulofthecrossmonastery.com/weekly-bulletin
  seen: 2026-10-23
  quote: Mass Intentions for the Week Saturday, October 24
  note: 'The ''Weekly Bulletin'' page is HTML text on Google Sites (announcements updated 10-25-2026 plus
    the week''s Mass intentions); it links no PDF, Drive file or image (links on the page: /home, /fr-patricks-column,
    /confessions, /more/*; checked 2026-10-23).'
- url: https://parishesonline.com/organization/saint-paul-of-the-cross-parish
  seen: 2026-10-23
  note: 'Not this place: that org is Saint Paul of the Cross Parish (Castle Shannon and Mount Lebanon),
    whose bulletin (14/1799) lists Saint Anne and Saint Winifred only; see parishes/saint-paul-of-the-cross-pittsburgh.'
- url: https://gcatholic.org/churches/usa-03/47063
  seen: 2026-10-23
  quote: 148 Monastery Ave., Pittsburgh, Pennsylvania 15203
  note: GCatholic, kind Monastery, website stpaulofthecrossmonastery.com, Plus Code 87G2C2F8+76.
research:
- method: Grepped the diocese's directory and Mass Finder rosters for 'Monastery Ave' and 'Passionist'
    (no match); fetched the monastery site and its weekly-bulletin page; probed ParishesOnline (LPi geo-search
    TSV, no Passionist or monastery org); DuckDuckGo search for the monastery with 'bulletin'; fetched
    passionistsspiritualplaces.org (province site, no bulletin link)
  url: https://www.stpaulofthecrossmonastery.com/weekly-bulletin
  checked: '2026-10-23'
  outcome: unsupported-format
  next_action: If the monastery posts a PDF or image bulletin, or the pipeline reads Google Sites HTML
    pages, make this a parish row with church st-paul-of-the-cross-monastery-pittsburgh
  retry_when: The monastery site links a PDF bulletin, or an HTML/Google Sites collector exists
---

## Why it is excluded

St. Paul of the Cross Monastery (Passionist monastery, church and retreat center, 148 Monastery Avenue, South Side Slopes) holds public Mass, but no bulletin the pipeline can read prints it. Its own site's home page (read 2026-10-23, updated 10-25-2026) lists a Mass schedule open to the public (Saturday vigil 5:00pm; Sunday 8:00am and 10:00am; weekday Masses; 'To purchase Mass Cards, Click Here'). Its 'Weekly Bulletin' page is plain HTML on Google Sites with that week's Mass intentions and Fr. Patrick's column, and no PDF or image to fetch. Rules settled 1 therefore applies: public Mass that no bulletin prints is `no-bulletin`, with the source that shows the Mass (above).

It is not a site of the parish Saint Paul of the Cross (Castle Shannon / Mount Lebanon, parishes/saint-paul-of-the-cross-pittsburgh): different building and neighbourhood, and that parish's 18 October 2026 bulletin lists Saint Anne and Saint Winifred only. The monastery appears in neither the diocese directory nor the Mass Finder (searched for 'Monastery Ave' and 'Passionist'); GCatholic lists it (47063, kind Monastery). The name match is a coincidence of the saint, not a link.

## What would change this

A PDF or image bulletin on the monastery site or a bulletin host, or an HTML collector in the pipeline: then a parish row (provider `other`, website the weekly-bulletin page) with this church under it. A statement that the monastery's Masses are not for the public would make it `no-public-mass`; the site says the opposite (see evidence).
