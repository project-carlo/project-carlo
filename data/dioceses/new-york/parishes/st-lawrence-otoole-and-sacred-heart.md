---
name: St. Lawrence O'Toole and Sacred Heart Parishes
website: https://stlawrence-sacredheart.org
bulletin_provider: other
provider_id: dated-post https://stlawrence-sacredheart.org/category/bulletin/
publication: ['url:https://stlawrence-sacredheart.org/category/bulletin/']
group: St. Lawrence O'Toole & Sacred Heart
evidence:
- url: https://stlawrence-sacredheart.org/wp-content/uploads/2026/09/146c_2026_09_27.pdf
  seen: 2026-09-26
  quote: 31 Prospect Street … Saturday Vigil 5:00, 7:30 pm (Spanish) … Sunday 8:00, 9:30, 11:00 am, 12:30
    pm (Spanish) 5:30 pm … Confessions 4:00 pm-7:00 pm Monday & Friday … 414 Haviland Drive … Sunday 10:30
    am … st. lawrence o'toole & sacred heart parishes
  note: Page 1 of the 27 September 2026 bulletin, the issue linked from the top of the bulletin archive
    that day. One schedule names both churches, and the footer calls them "st. lawrence o'toole & sacred
    heart parishes". The printer line is "146C (JR) - St. Lawrence O'Toole - Brewster, NY"; that is a
    printer code on a PDF the parish hosts, not a ParishesOnline container.
- url: https://stlawrence-sacredheart.org/wp-content/uploads/2026/09/146c_2026_09_27.pdf
  seen: 2026-09-26
  quote: for our two churches as we introduce our Increased Offertory Appeal
  note: Fr. Richard Gill's letter on page 3 of the same issue, dated 27 September 2026. He writes to both
    parishes about the two churches. Parts of that page use a font the extractor garbles; this sentence
    is in the extractable text.
- url: https://stlawrence-sacredheart.org/category/bulletin/
  seen: 2026-09-26
  quote: 31 Prospect Street Brewster, NY 10509
  note: Footer of the bulletin archive, which also lists Sacred Heart at 414 Haviland Drive, Patterson,
    NY 12563. On 2026-09-26 the newest post was "September 27-Twenty-Sixth Sunday in Ordinary Time", and
    that post embeds the PDF above through the DFlip viewer. The issue title changes every week; the footer
    addresses do not.
- url: https://stlawrence-sacredheart.org/wp-content/uploads/2026/10/146c_2026_10_25.pdf
  seen: 2026-10-31
  quote: October 25, 2026 thirtieth sunday in ordinary time
  note: Page 1 of the issue fetch:check picked on 2026-10-31 with dated-post; same schedule for St. Lawrence
    O'Toole (31 Prospect Street) and Sacred Heart (414 Haviland Drive).
- url: https://stlawrence-sacredheart.org/category/bulletin/
  seen: 2026-10-31
  quote: October 25-Thirtieth Sunday in Ordinary Time
  note: Newest post on the bulletin archive on 2026-10-31; the posts above it are not yet there for November
    1.
- url: https://stlawrence-sacredheart.org/wp-content/uploads/2026/11/146c_2026_11_08.pdf
  seen: 2026-11-08
  quote: thirty second sunday in ordinary time
  note: Page 1 of the 8 November 2026 issue, picked by the pinned dated-post recipe on 2026-11-08 (fetch:check,
    identity 'lawrence' matched, fresh); masthead lists St. Lawrence O'Toole, 31 Prospect Street, Brewster.
promoted: 2026-09-26
research:
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --diocese new-york --parish st-lawrence-otoole-and-sacred-heart
  url: https://stlawrence-sacredheart.org/category/bulletin/
  checked: '2026-10-31'
  outcome: found
- method: fetch:check --diocese new-york --parish st-lawrence-otoole-and-sacred-heart with the pinned
    dated-post recipe
  url: https://stlawrence-sacredheart.org/category/bulletin/
  checked: '2026-11-08'
  outcome: found
bulletin_status: available
---

## Publisher

St. Lawrence O'Toole (Brewster) and Sacred Heart (Patterson) publish one weekly bulletin on
stlawrence-sacredheart.org. I read the 27 September 2026 issue. Page 1 is a single Mass schedule
for both churches, and the footer names "st. lawrence o'toole & sacred heart parishes". The
pastor's letter on page 3 of that issue speaks of "our two churches". They are two canonical
parishes with one bulletin, so they are one row. Added because the parish was requested, not as
part of a survey of the Archdiocese of New York.

## Worship sites

Two, both on the 27 September schedule:

- St. Lawrence O'Toole Church, 31 Prospect Street, Brewster (`churches/st-lawrence-otoole-brewster.md`).
  Saturday 5:00 pm and 7:30 pm (Spanish); Sunday 8:00, 9:30 and 11:00 am, 12:30 pm (Spanish)
  and 5:30 pm; Monday–Friday 8:30 am. Confessions Monday and Friday, 4:00–7:00 pm.
- Sacred Heart Church, 414 Haviland Drive, Patterson (`churches/sacred-heart-patterson.md`).
  Sunday 10:30 am.

The same issue mentions three places that are not separate worship sites. St. Lawrence O'Toole
Cemetery is a notice that plots and niches are for sale, with no Mass. The Early Childhood
Learning Center is the preschool in the old school building, which the pastor's letter describes
as converted into the parish center. The Adoration Chapel is named only as the place a prayer
list is kept, with a signup link at adorationpro.org for org `lawrence`; this issue gives it no
address and no standing hour, so it stays part of the Brewster church rather than its own row.
A talk at St. Lawrence Church on 16 October 2026 is followed by adoration that evening; that is
one dated event, not another building.

The archdiocese place page for this pair (https://www.archny.org/places/slot-sh-lawrence-o-toole)
lists St. Lawrence O'Toole's schedule and calls the city "Town of Southeast". It does not give
Sacred Heart its own address. I did not find a separate archdiocese page for Sacred Heart.

## Website and bulletin provider

https://stlawrence-sacredheart.org is the parish's own site. Its navigation links
https://stlawrence-sacredheart.org/category/bulletin/, a WordPress archive of one post per
week. The current post does not link a PDF directly; it embeds one in a DFlip viewer. `probe url`
found no ParishesOnline, eCatholic or DiscoverMass id. Fetch treats `other` as "start at the
homepage and follow the bulletin link", which is this archive, so `bulletin_provider` is `other`
and the publication id is the archive page.

On 2026-10-31 `fetch:check --diocese new-york` (no recipe pinned) resolved this archive with
`dated-post on https://stlawrence-sacredheart.org/category/bulletin/: first-listed` and
downloaded https://stlawrence-sacredheart.org/wp-content/uploads/2026/10/146c_2026_10_25.pdf
(3.9 MB PDF). The newest post on the archive that day was "October 25-Thirtieth Sunday in
Ordinary Time" (the November 1 issue was not yet posted), and page 1 of the PDF reads "October
25, 2026 thirtieth sunday in ordinary time" over the same two-church schedule. So the pick was
this week's issue, and the recipe it printed, `dated-post https://stlawrence-sacredheart.org/category/bulletin/`,
is now pinned in `provider_id`. This settles the connector question raised on October 8 (then
the September 27 post was eleven days old, outside dated-post's seven-day window for posts whose
title doesn't say "bulletin", and the replay found nothing). If the parish posts a week late
again, the pick can still fail for the same reason; that is a fetch failure to watch for, not
a wrong issue.

Rechecked 2026-11-08 with the pinned recipe: it picked https://stlawrence-sacredheart.org/wp-content/uploads/2026/11/146c_2026_11_08.pdf (`dated-post ...: current`), the 8 November 2026 issue, whose first page names St. Lawrence O'Toole at 31 Prospect Street.

## Not yet confirmed

Nothing that would change the row. The GCatholic roster for the archdiocese was not fetched, and
no diocesan family list was read. Neither is needed to see that these two churches share this
bulletin.
