---
name: St. Stephen's R.C. Magyar Church
website: https://ststephenspassaic.com/
bulletin_provider: other
provider_id: page-pdfs https://ststephenspassaic.com/2026-2/
publication: ['url:https://ststephenspassaic.com/bulletins/']
group: ''
evidence:
- url: https://ststephenspassaic.com/wp-content/uploads/2026/10/2026-44-November-1-2026.pdf
  seen: 2026-11-05
  quote: 223 THIRD STREET
  note: 'Page 1 of the 1 November 2026 issue (BULLETIN#44) is an image (rendered with render.py): St.
    Stephen''s R.C. Magyar Church, 223 Third Street, Passaic, NJ 07055, Fr. Imre Juhász, Pastor; Mass
    list Sat. Oct 31 4:30PM (E) All Saints Vigil, Sun. Nov 1 11:00AM (H), Mon. Nov 2 6:30PM (H) All Souls,
    Fri. Nov 6 6:30PM (H), Sat. Nov 7 6:30PM (E), Sun. Nov 8 11:00AM (H). 18 pages; pages 1-3, 10, 11,
    16, 17 have no text; the quoted line is on page 18. A grep for Chapel and Kápolna finds none.'
- url: https://ststephenspassaic.com/2026-2/
  seen: 2026-11-05
  note: 'The 2026 bulletin page (linked from /bulletins/, which lists one page per year 2017-2026) links
    weekly PDFs newest first: 2026-44-November-1-2026.pdf, 2026-43-October-25-2026.pdf, 2026-42-October-18-2026.pdf
    ... and no other PDFs.'
- url: https://ststephenspassaic.com/wp-json/wp/v2/media?mime_type=application/pdf&per_page=40&_fields=date,source_url
  seen: 2026-11-05
  note: 'WordPress media list: weekly bulletins uploaded each Friday or Saturday before their Sunday (1
    November issue on 30 October, 25 October on 23 October), plus monthly ENG/HUN calendars and flyers.'
revisit: Open https://ststephenspassaic.com/bulletins/; when a 2027 year page lists the first 2027 issue,
  repin provider_id to page-pdfs on that page and rerun fetch:check.
revisit_after: 2027-01-04
bulletin_status: available
---

## Publisher

St. Stephen's R.C. Magyar Church, Passaic, a Hungarian parish, produces its own weekly bilingual (Hungarian and English) bulletin and posts it as a PDF on its WordPress site. Page 1 of the 1 November 2026 issue (`https://ststephenspassaic.com/wp-content/uploads/2026/10/2026-44-November-1-2026.pdf`, read 2026-11-05) is an image; rendered, it reads "St. Stephen's R.C. Magyar Church ... BULLETIN#44", with "223 Third Street, Passaic, NJ 07055" and Fr. Imre Juhász, Pastor. Pages 5-6 are Liguori Publications inserts; no printer hosts it.

## Worship sites

- `st-stephen-passaic`: the only church. The page 1 Mass list (Saturday 4:30 or 6:30 PM English, Sunday 11:00 AM Hungarian, weekday evening Masses) names no other place, and a grep for Chapel and Kápolna finds none.

The diocese's finder has two pins for this church: directory:22153 "St. Stephen Parish" (223 Third Street, the parish's site) and the addressless directory:40503 "St. Stephen's RC Magyar Church", whose name is the bulletin's masthead name. Both are linked to the one church under the diocese's two-pins rule. GCatholic (18997) lists the one church.

## Website and bulletin provider

The site's `/bulletins/` page links one page per year (2017 to 2026); the 2026 page (`https://ststephenspassaic.com/2026-2/`) links each weekly issue newest first, named `<year>-<week>-<Month>-<day>-<year>.pdf`. The provider is `other`, pinned as `page-pdfs https://ststephenspassaic.com/2026-2/`; the publication is recorded as the bulletin page. `fetch:check` on 2026-11-05 (headed) without a recipe failed (`resolve_failed`: the bulletin page links only the year pages); with the recipe it picked `https://ststephenspassaic.com/wp-content/uploads/2026/10/2026-44-November-1-2026.pdf` (freshness `fresh`, age 4 days, date from the file name), the issue read above. Its identity is unverified because page 1 is an image. The 8 November issue is normally uploaded on the Friday or Saturday before.

## Not yet confirmed

The recipe names the 2026 year page. The first 2027 issue will most likely go on a new year page (`/2027-2/`, following `/2025-2/` and `/2026-2/`), and the pinned recipe will then pick the last 2026 issue: in early January 2027, open `/bulletins/` and repin the recipe to the 2027 page (see `revisit`).
