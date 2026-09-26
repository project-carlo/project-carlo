---
name: Prince of Peace Parish at St. Ambrose, St. Anthony & St. Joseph
website: https://northendicottcatholic.org
bulletin_provider: discover_mass
provider_id: st-ambrose-endicott-ny
publication: ['discovermass:st-ambrose-endicott-ny', 'discovermass:st-anthony-of-padua-endicott-ny', 'discovermass:st-joseph-endicott-ny']
group: Prince of Peace Parish, Endicott
evidence:
- url: https://discovermass.com/church/st-ambrose-endicott-ny/
  seen: 2026-09-26
  quote: 203 Washington Ave., Endicott, NY 13760
  note: 'Discover Mass listing; `issues.py discovermass` lists weekly issues through 2026-09-27. Page
    1 of the 27 September 2026 issue: "Prince of Peace Parish at St. Ambrose, St. Anthony & St. Joseph",
    www.northendicottcatholic.org, pastor Rev. Richard P. Prior Jr., with the three churches'' addresses.
    Page 2 "WEEKLY MASS & CONFESSION" (STAM-St. Ambrose, STA-St. Anthony, STJ-St. Joseph): Saturday 4:00pm
    Mass STAM, 5:30pm Mass STA; Sunday 8:30am Mass STA, 11:00am Mass STJ; Monday 8:30am STA; Thursday
    8:30am STJ. The St. Anthony (st-anthony-of-padua-endicott-ny) and St. Joseph (st-joseph-endicott-ny)
    listings serve the same PDF.'
- url: https://northendicottcatholic.org/bulletin/
  seen: 2026-09-26
  note: 'The parish''s "Bulletin" page (read with visit.py): links "September 27, 2026", "September 20,
    2026", "September 13, 2026" to bulletins.discovermass.com download links. The site is hosted by eCatholic
    (site id 34417) but no bulletins are on files.ecatholic.com (`issues.py ecatholic ecatholic:34417`:
    403 for the last three Sundays).'
---

## Publisher

This row is the second bulletin of Prince of Peace Parish, Endicott: the "North Endicott Catholic
Community" of St. Ambrose, St. Anthony of Padua and St. Joseph, published through Discover Mass.
I read the 27 September 2026 issue. Its page-1 masthead is "Prince of Peace Parish at St.
Ambrose, St. Anthony & St. Joseph", with the three churches' addresses and offices, and page 2's
"Weekly Mass & Confession" schedule has Saturday 4:00 pm at St. Ambrose and 5:30 pm at St.
Anthony, Sunday 8:30 am at St. Anthony and 11:00 am at St. Joseph, and weekday Masses at St.
Anthony and St. Joseph. It does not list Our Lady of Good Counsel, whose own bulletin (container
06/0139) is also current, so the parish is two rows in one group; see
`parishes/prince-of-peace-our-lady-of-good-counsel-endicott.md`.

## Worship sites

Three: St. Ambrose (`churches/st-ambrose-endicott.md`), St. Anthony of Padua
(`churches/st-anthony-of-padua-endicott.md`) and St. Joseph (`churches/st-joseph-endicott.md`).
The staff list names a trustee "(St. Casimirs)", and the diocese keeps St. Casimir's records
here, but no Mass at St. Casimir appears in the schedule; it is excluded as closed
(`excluded/st-casimir-endicott.md`).

## Website and bulletin provider

northendicottcatholic.org is an eCatholic-hosted site (`probe url` finds `ecatholic:34417`), but
its Bulletin page links Discover Mass downloads, and files.ecatholic.com has no issues for that
id. The bulletin is on Discover Mass under three church listings (St. Ambrose, St. Anthony of
Padua, St. Joseph) that serve the same PDF; `provider_id` is the St. Ambrose listing and all three
are in `publication`. `ecatholic:34417` is left out of `publication` because nothing is published
under it.

## Not yet confirmed

Nothing about the structure. See the OLGC row's `revisit` on combining the two bulletins.
