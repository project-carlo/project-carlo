---
name: Saint Mark and Holy Rosary Parishes, Altoona
website: https://www.churchofsaintmarks.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://www.churchofsaintmarks.org/']
group: ''
revisit: Look for a posted bulletin PDF (parish Facebook page, Discover Mass, a Bulletins page on churchofsaintmarks.org); if one appears set the provider and run fetch:check.
revisit_after: 2027-01-15
evidence:
- url: https://www.churchofsaintmarks.org/
  seen: 2026-10-21
  quote: We have included Holy Rosary Catholic Church on this website.
  note: 'Homepage of the St. Mark site, which is headed "THE CATHOLIC COMMUNITY OF SAINT MARK''S AND HOLY ROSARY" and carries both churches'' addresses and one pastor. The weekly text on it changes, so later rechecks of the dated quotes below will fail.'
- url: https://www.churchofsaintmarks.org/
  seen: 2026-10-21
  quote: Pastor of Saint Mark Church and Holy Rosary Church.
  note: One pastor for both. The page also lists "WEEKEND MASSES Saturday, Oct 17, 2026 4:30 pm Saint Mark's Church Sunday, Oct 18, 2026 8:30 am - Saint Mark’s Church 11:00 am Holy Rosary Church", so the two churches share one weekend schedule.
- url: https://www.churchofsaintmarks.org/mass-information.html
  seen: 2026-10-21
  quote: MASSES FOR THE COMING WEEK (SM) Saint Mark Church (HR) Holy Rosary Church
  note: One joint list of Mass intentions for both churches from Saturday 17 October 2026.
- url: https://discovermass.com/church/st-mark-altoona-pa/
  seen: 2026-10-21
  quote: There are currently no bulletins available for St. Mark.
  note: Discover Mass has a page for each church but no bulletin on either.
- url: https://discovermass.com/church/holy-rosary-altoona-pa/
  seen: 2026-10-21
  quote: There are currently no bulletins available for Holy Rosary.
  note: Its listed website is also http://www.churchofsaintmarks.org.
---

## Publisher

The two parishes have no separate channel, and no bulletin file at all that the pipeline
could read. Holy Rosary (900 N. Fourth St.) has no homepage in the diocese directory; the
directory gives St. Mark (416 Sixth Ave.) `churchofsaintmarks.org`, and that site is for
both: the page header reads "THE CATHOLIC COMMUNITY OF SAINT MARK'S AND HOLY ROSARY", it
gives both addresses and phone numbers, and the page says "We have included Holy Rosary
Catholic Church on this website." Both churches share Fr. Nelson Javier, T.O.R. as pastor
(the page, 21 Oct 2026; the diocese directory says the same), one weekend schedule and one
list of weekly Mass intentions ("MASSES FOR THE COMING WEEK (SM) Saint Mark Church (HR) Holy
Rosary Church", mass-information page). So this is **one row**, not two. No second channel
exists for Holy Rosary: Discover Mass has a page for each church
(`st-mark-altoona-pa`, `holy-rosary-altoona-pa`) and both say no bulletins are available.

What the site does publish is the week's notices as text on the homepage (the 18 October 2026
"29th Sunday in Ordinary Time" notices) and the Mass intentions as text on `mass-information`.
The homepage refers to "the bulletin" ("The forms ... will be on the back tables of both
churches and inside the bulletin"), so a printed bulletin exists, but I found no PDF of it:
the homepage, Mass Information, Contact Us and Archive pages (the last through headed Chrome,
because Cloudflare challenges curl on some pages) link to no PDF, widget or bulletin page.

## Worship sites

Two churches, both holding Mass now (see their records): `saint-mark-altoona` (Sat 4:30 PM,
Sun 8:30 AM, weekday Masses Monday and Friday) and `holy-rosary-altoona` (Sun 11:00 AM,
weekday Masses Tuesday and Thursday). The weekly notices also mention St. Therese's youth
group, which is a different parish (`saint-therese-of-the-child-jesus-altoona` in the
directory), not a site of this one.

## Website and bulletin provider

`no_bulletin`: the site is the parish's channel but it posts no bulletin file, so there is
nothing for `fetch` to read. `website` is the St. Mark site that serves both parishes, and
`publication` is `url:` of it. If a bulletin is ever posted as PDFs, set `other` and run
`fetch:check`. Not run now, since there is no PDF.

## Not yet confirmed

- Whether the printed bulletin is posted anywhere (a Facebook page, `facebook.com/saintmarksofaltoona`,
  is mentioned on the homepage; not opened). Revisit: ask or look for a PDF link, and check
  Discover Mass again.
- Whether the weekly homepage notices should count as a bulletin. They are text on a Weebly
  page, not a document, so I did not treat them as one.
