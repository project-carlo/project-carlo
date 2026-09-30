---
name: River Catholics (St. Mary's and St. Paul's)
website: https://rivercatholics.org/bulletins-1
bulletin_provider: other
provider_id: ''
publication: ['ecatholic:21398', 'url:https://rivercatholics.org/bulletins-1']
group: River Catholics
evidence:
- url: https://files.ecatholic.com/21398/documents/2026/9/September%2027%202026.pdf
  seen: 2026-09-30
  quote: River Catholics Parishes of St. Mary's and St. Paul's
  note: Page 1 of the 27 September 2026 issue (2 pages, text layer), an eCatholic-hosted PDF uploaded
    under files.ecatholic.com/21398/documents/2026/9/. Pastor Fr. Frank T. Natale, MSC; deacons Daniel
    LeRoy and William Johnston, Jr.
- url: https://files.ecatholic.com/21398/documents/2026/9/September%2027%202026.pdf
  seen: 2026-09-30
  quote: Sunday Masses - effective 9/5 & 9/6/26 O.L.S.H. 4:00 PM (Sat. Ant.) St. Mary's 8:00 AM O.L.S.H.
    9:45 AM St. Paul's 11:30 AM
  note: 'Page 1: the bulletin''s Sunday schedule, which includes Our Lady of the Sacred Heart, Watertown
    (see that parish''s own bulletin).'
- url: https://files.ecatholic.com/21398/documents/2026/9/September%2027%202026.pdf
  seen: 2026-09-30
  quote: Weekly Mass Intentions Saturday, September 26, 2026
  note: 'Page 2: Sunday St. Mary''s 8:00 am and St. Paul''s 11:30 am; Thursday 1 October St. Mary''s 9:15
    am; Monday, Tuesday, Wednesday and Friday "NO MASS" (weekday Masses that week are at OLSH, which this
    bulletin does not list).'
- url: https://rivercatholics.org/bulletins-1
  seen: 2026-09-30
  note: The parish site (eCatholic, custom domain; read with visit.py) "Bulletins" page, headed "St. Mary's
    - St. Paul's Bulletin", links one PDF per Sunday (30 August, 6, 13, 20 and 27 September 2026) under
    files.ecatholic.com/21398/documents/2026/. The files are uploaded documents with free-form names,
    not the dated bulletins/YYYYMMDD.pdf pattern, so `issues.py ecatholic` will not find them.
- url: https://rivercatholics.org/about-us
  seen: 2026-09-30
  note: '"The River Catholics are comprised of the parishes of St. Paul''s (Black River) and St. Mary''s
    (Evans Mills)."'
- url: https://rivercatholics.org/parish-consolidation
  seen: 2026-09-30
  note: Lists the 2019 consolidation documents ("St. Mary; St. Joseph; St. Theresa" and "St Paul and St
    Rita"); see excluded/st-joseph-philadelphia and excluded/st-theresa-of-avila-theresa.
---

## Publisher

St. Mary's (Evans Mills) and St. Paul's (Black River), together "River Catholics", publish **one**
weekly bulletin, headed "River Catholics - Parishes of St. Mary's and St. Paul's", with Fr. Frank T.
Natale, MSC as pastor and one parish office (8422 S. Main Street, Evans Mills). The 27 September 2026
issue is a 2-page PDF: page 1 has the masthead, staff and a Sunday schedule (St. Mary's 8:00 am, St.
Paul's 11:30 am, and OLSH, Watertown 4:00 pm Saturday and 9:45 am Sunday, "effective 9/5 & 9/6/26"),
page 2 the weekly intentions (Sunday and Thursday 9:15 am at St. Mary's; "NO MASS" the other weekdays)
and the 125th-anniversary dinner notice for St. Paul's (8 November, after the 11:30 Mass).

The diocese's directory lists both churches with the website rivercatholics.org and no group. The
diocese's Parish Bulletins page also sends Black River and Evans Mills to rivercatholics.org.

**Overlap with OLSH's bulletin.** Father Natale is also pastor of Our Lady of the Sacred Heart in
Watertown, whose own bulletin (`our-lady-of-the-sacred-heart-watertown`, ParishesOnline) lists St. Mary's and
St. Paul's Masses as well as its own. They are separate publications (different mastheads, accounts and
content), so two rows, with each church under the bulletin that carries its name.

## Worship sites

- `st-mary-evans-mills`, 8422 S. Main Street (directory evans-mills, GCatholic 18275).
- `st-paul-black-river`, 208 LeRay Street (directory black-river, GCatholic 18237).

Not here: **St. Joseph, Philadelphia and St. Theresa of Avila, Theresa**, merged into St. Mary's and
relegated to profane use by decrees of 5 March 2019 (see `excluded/st-joseph-philadelphia` and
`excluded/st-theresa-of-avila-theresa`); GCatholic still lists both. **St. Rita, Deferiet** (merged into
St. Paul's in the same year, per the site's consolidation page) is in neither roster in this region and
holds no Mass in the current bulletin; whoever owns Deferiet should check it.

## Website and bulletin provider

rivercatholics.org is an eCatholic-hosted site (id 21398). Its Bulletins page lists the weekly PDFs as
uploaded documents, so the row uses provider `other` with the Bulletins page as `website`, like Holy
Family, Little Falls in Albany, and records both `ecatholic:21398` and `url:https://rivercatholics.org/bulletins-1`.
`probe url` gets 403 (Cloudflare); a browser loads the pages.

## Not yet confirmed

Nothing outstanding. The current schedule changed on 5-6 September 2026 ("effective 9/5 & 9/6/26");
earlier issues may show different Sunday times.
