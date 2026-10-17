---
name: Saint Monica Parish
website: https://www.stmonicanepa.com
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.stmonicanepa.com/', 'ecatholic:13540']
group: Saint Monica Parish
evidence:
- url: https://files.ecatholic.com/13540/documents/2026/10/Saint%20Monica%20Bulletin%20-%20October%2011%202026-2.pdf
  seen: 2026-10-16
  quote: Reverend Peter A. Tomczak, Pastor
  note: 'Masthead, page 1 of the 11 October 2026 issue: Saint Monica Parish, Catholic Community of Wyoming
    & West Wyoming, 363 West 8th St., West Wyoming. Mass schedule: Saturday Vigil 4:00 PM; Sunday 8:30
    AM & 11:00 AM; Monday, Tuesday, Wednesday, Friday 8:00 AM.'
- url: https://files.ecatholic.com/13540/documents/2026/10/Saint%20Monica%20Bulletin%20-%20October%2011%202026-2.pdf
  seen: 2026-10-16
  quote: 11:00AM – Giampiero Tafani
  note: Page 2 Mass intentions for 12-18 October at the same times; no other church named.
- url: https://www.stmonicanepa.com/
  seen: 2026-10-16
  note: eCatholic site 13540 (403 to plain fetches; read in a browser). The homepage links the current
    issue as a document, files.ecatholic.com/13540/documents/2026/10/Saint Monica Bulletin - October 11
    2026-2.pdf. Its /bulletins page lists only an old issue, files.ecatholic.com/13540/bulletins/20250525.pdf
    (25 May 2025).
promoted: 2026-10-17
---

## Publisher

Saint Monica Parish, West Wyoming ("Catholic Community of Wyoming & West Wyoming") publishes its
own weekly bulletin. The 11 October 2026 issue's masthead (page 1) names the parish alone, 363 West
8th St., Rev. Peter A. Tomczak, pastor, with Saturday 4 pm, Sunday 8:30 and 11 am, and Monday,
Tuesday, Wednesday and Friday 8 am (Friday followed by Adoration). Page 2's intentions match.

## Worship sites

One: `our-lady-of-sorrows-west-wyoming`, Our Lady of Sorrows Church at the parish address, the
finder's only worship site for the parish. The bulletin names the parish, not the building. No
other church of the parish is in a roster here.

## Website and bulletin provider

stmonicanepa.com is the parish's eCatholic site (site id 13540), named in the masthead. The parish
does **not** use eCatholic's bulletin feature: its /bulletins page and
`files.ecatholic.com/13540/bulletins/` stop at 25 May 2025. Current issues are uploaded as documents
(`files.ecatholic.com/13540/documents/<y>/<m>/Saint Monica Bulletin - <date>.pdf`) and linked from
the homepage, as Holy Family, Little Falls does in Albany. So `bulletin_provider` is `other` (an
`ecatholic` row would read the stale feed), with the homepage as `website`; `ecatholic:13540` is
recorded so that no other row claims the site. No recipe pinned: `fetch:check` reads only promoted
rows.

## Not yet confirmed

Which link the `other` resolver picks on the homepage (it also links a monthly calendar, "October
2026.pdf"); pin the recipe after promotion.
