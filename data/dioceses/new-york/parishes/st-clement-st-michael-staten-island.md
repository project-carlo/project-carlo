---
name: St. Clement and St. Michael
website: https://www.facebook.com/StClementStMichael/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: St. Clement and St. Michael
evidence:
- url: https://www.archny.org/places/sc-sm-st-clement
  seen: 2026-10-31
  quote: 126 Van Pelt Avenue
  note: 'Official archdiocesan page for St. Clement Church: Mass Schedule Saturday 4:00 PM English, Sunday
    11:30 AM English; phone 718-442-1688; its only website link is facebook.com/StClementStMichael. No
    bulletin link.'
- url: https://www.archny.org/places/sc-sm-st-michael
  seen: 2026-10-31
  quote: 211 Harbor Road
  note: 'Official archdiocesan page for St. Michael Church: Sunday 10:00 AM English and 12:45 PM Spanish,
    Monday-Friday 9:00 AM English; same phone and Facebook link. No bulletin link.'
- url: https://www.facebook.com/StClementStMichael/
  seen: 2026-10-31
  quote: St. Michael - 207 Harbor Road SINY 10303
  note: Parish Facebook page read logged out in a headed browser (parish-site-access visit.py). Intro
    gives the same Mass schedule for both churches; the latest visible post is a live-streamed Holy Rosary
    of Tuesday 27 October 2026. No bulletin post or link visible; the Photos tab requires login.
revisit: 'Find a published bulletin: a website or bulletin link on the archdiocesan pages, a bulletin
  posted on the Facebook page, or a ParishesOnline/Discover Mass/Bon Venture listing for ZIP 10303. Mass
  at both churches is settled.'
revisit_after: 2027-01-31
research:
- method: Official archdiocesan church pages for both buildings re-read (probe get)
  url: https://www.archny.org/places/sc-sm-st-clement
  checked: '2026-10-31'
  outcome: not-found
  next_action: Re-read both archny.org pages for a parish website or bulletin link
  retry_when: The archdiocesan page links a parish website other than Facebook
  revisit_after: 2027-01-31
- method: Facebook page (Intro, visible posts, Photos tab) in a headed browser, logged out
  url: https://www.facebook.com/StClementStMichael/
  checked: '2026-10-31'
  outcome: not-found
  next_action: Look for a posted bulletin (PDF or image issue) in the page's visible posts; Photos albums
    need a logged-in session
  retry_when: A logged-in browser session is available, or a visible post links a bulletin
- method: Web search for a bulletin on ParishesOnline, Discover Mass, eCatholic and generally; ParishesOnline
    org slugs st-clement-st-michael-10303 and st-clement-and-st-michael-10303 tried with probe po
  checked: '2026-10-31'
  outcome: not-found
  next_action: Search ParishesOnline, Discover Mass and Bon Venture again by parish name and ZIP 10303
  retry_when: A search result or directory entry shows a bulletin channel for the parish
  revisit_after: 2027-01-31
bulletin_status: not-found
---

## Publisher

The Parish of St. Clement and St. Michael, Mariners Harbor, has public Mass at two churches but no bulletin was found on 31 October 2026. The archdiocese's two church pages (read 31 October) give its schedule and office phone 718-442-1688 and link only the parish Facebook page. That page, read logged out in a headed browser, repeats the Mass schedule in its Intro and shows a live-streamed rosary of 27 October 2026, but no bulletin; its Photos albums need a login. Web searches and ParishesOnline slug probes found no ParishesOnline, Discover Mass, eCatholic or Bon Venture listing. The 8 October session found the same. This row is therefore `no_bulletin` with `bulletin_status: not-found` (Settled policy 4): kept in the records, left off the site until a readable bulletin turns up. This is a statement about what was found, not evidence that the parish publishes nothing.

## Worship sites

- `st-clement-staten-island`, St. Clement Church, 126 Van Pelt Avenue: Saturday 4 PM and Sunday 11:30 AM (archdiocesan page re-read 8 November and Facebook Intro agree).
- `st-michael-staten-island`, St. Michael Church, 211 Harbor Road: Sunday 10 AM English and 12:45 PM Spanish, Monday-Friday 9 AM (same two sources agree). Facebook and GCatholic say 207 Harbor Road; the official 211, which OSM also gives for the building, is stored.

Both are listed by the official map under the group "St. Clement and St. Michael" and share one office, phone and Facebook account. One parish row is used because they are one canonical parish with one office and no separate publishing channel for either; if a bulletin turns up, its masthead decides whether it covers both. The parish school (OSM: Saint Clement and Saint Michael School, 2 Gridley Avenue) is not a worship site.

## Website and bulletin provider

The Facebook page is stored as `website` because it is the only site the parish or the archdiocese gives. It is not a bulletin channel (Settled policy 1 needs the bulletin posted there), which is why the provider is `no_bulletin`.

## Not yet confirmed

Whether the parish publishes a bulletin at all, and where. See `research` for the checks made and their retry triggers.
