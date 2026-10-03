---
name: St. James Catholic Church
website: https://stjamescaz.org/category/media-bulletins/
bulletin_provider: other
provider_id: dated-post https://stjamescaz.org/category/bulletins/
publication: ['url:https://stjamescaz.org/category/media-bulletins/']
group: Rev. Kevin Corcoran (Cazenovia, Chittenango)
evidence:
- url: https://stjamescaz.org/wp-content/uploads/09-27-2026-Bulletin.pdf
  seen: 2026-09-26
  quote: St. James Catholic Church … 6 Green Street, Cazenovia, NY 13035
  note: Page 1 of the 27 September 2026 issue. Names St. James alone (Fr. Kevin Corcoran, Pastor).
- url: https://stjamescaz.org/wp-content/uploads/09-27-2026-Bulletin.pdf
  seen: 2026-09-26
  quote: 'Saturday: 5:30pm (Lived streamed on website)    Sunday: 9:00am'
  note: The same page's Mass schedule; daily Mass Thursdays 6:45am & 11:00am. The page-2 calendar has
    every Mass at "Ch" (the church).
- url: https://stjamescaz.org/category/media-bulletins/
  seen: 2026-09-26
  note: '`probe url`: the parish''s WordPress bulletin category, linking the weekly PDFs under /wp-content/uploads/
    (newest 09-27-2026-Bulletin.pdf).'
- url: https://www.syracusediocese.org/st-patrick-chittenango
  seen: 2026-09-26
  quote: PASTOR, ST. JAMES, CAZENOVIA; ST. PATRICK, CHITTENANGO
  note: The diocese's page for St. Patrick, Chittenango (behind Cloudflare; read in a browser), listing
    Rev. Kevin J. Corcoran.
promoted: 2026-09-26
---

## Publisher

St. James publishes its own weekly bulletin as a PDF on its own WordPress site. I read the
27 September 2026 issue: page 1 names St. James Catholic Church, 6 Green Street, Cazenovia, alone,
with its own staff and Mass schedule (Saturday 5:30 pm, Sunday 9:00 am, Thursday 6:45 and 11:00 am).
St. James shares its pastor and deacons with St. Patrick, Chittenango, but St. Patrick publishes its
own bulletin through ParishesOnline (`parishes/st-patrick-chittenango.md`) and neither bulletin
mentions the other's Masses, so they are two rows.

## Worship sites

One: `churches/st-james-cazenovia.md`. St. Lawrence Mission in DeRuyter, the nearest mission in the
roster, is not served from here: the diocese makes it "a Mission of St. Margaret, Homer", and the
Cortland/Homer bulletin schedules its Mass.

## Website and bulletin provider

stjamescaz.org (the diocese's link; GCatholic's stjamescaz.com is the older domain) posts each issue
at /wp-content/uploads/MM-DD-YYYY-Bulletin.pdf and lists them in the "Bulletins" category page,
which is `website` and the `url:` publication id. Provider `other`.

Fetch recipe `dated-post https://stjamescaz.org/category/bulletins/`, pinned 2026-10-03:
on the pages recorded 2026-09-27 (`tests/fixtures/fetch/st-james-cazenovia.json.gz`) the
resolver found https://stjamescaz.org/wp-content/uploads/09-27-2026-Bulletin.pdf this way,
dated that week.

## Not yet confirmed

Nothing.
