---
name: St. Charles Borromeo Parish
website: https://www.stcharlesashland.com/
bulletin_provider: other
provider_id: page-pdfs https://www.stcharlesashland.com/s-projects-side-by-side
publication:
- url:https://www.stcharlesashland.com/s-projects-side-by-side
group: St. Charles Borromeo Parish
evidence:
- url: https://www.stcharlesashland.com/_files/ugd/23b1db_5ff7151c62a641f59cf5dbc1925ba022.pdf
  seen: 2026-10-18
  quote: 'Saint Charles Borromeo Parish Rev. Christopher M. Zelonis, Pastor Deacon John Sutter Parish
    Office: 1115 Walnut Street, Ashland PA 17921'
  note: Page 1 of the 18 October 2026 issue (the first "View" link on the 2026 Bulletins page, under "October
    18, 2026").
- url: https://www.stcharlesashland.com/_files/ugd/23b1db_5ff7151c62a641f59cf5dbc1925ba022.pdf
  seen: 2026-10-18
  quote: Mass Times Saturday 4:00 PM Sunday 9:00 AM
  note: 'Page 1. Page 2 lists the week''s Masses: Saturday 4:00 PM and Sunday 9:00 AM here, Tuesday and
    Friday 8:30 AM, with St. Joseph the Worker, Frackville''s times (5:30 PM, 11:00 AM) given alongside
    as the sister parish''s.'
- url: https://www.stcharlesashland.com/s-projects-side-by-side
  seen: 2026-10-18
  quote: October 18, 2026 Twenty-ninth Sunday in Ordinary Time View
  note: 'The Wix "2026 Bulletins" page: a grid of dated cards, each with a "View" link to a `_files/ugd/23b1db_<hash>.pdf`
    file (no date in the file name).'
- url: https://shensentinel.com/news/new-priest-assigned-to-ashland-frackville-parish/
  seen: 2026-10-18
  quote: Rev. Christopher M. Zelonis has been assigned as Pastor of St. Charles Borromeo Parish in Ashland
    and St. Joseph the Worker Parish in Frackville.
  note: Shenandoah Sentinel, 17 May 2026; effective June 16.
---

## Publisher

St. Charles Borromeo Parish, Ashland (formed in 2015 from St. Joseph and St. Mauritius,
Ashland; St. Joseph and St. Vincent de Paul, Girardville; and Our Lady of Good Counsel,
Gordon) publishes its own weekly bulletin on its Wix site. The 18 October 2026 issue (5 pages;
pages 1–4 text, page 5 an image) has the masthead "Saint Charles Borromeo Parish, Rev.
Christopher M. Zelonis, Pastor ... Parish Office: 1115 Walnut Street, Ashland" and "Mass Times
Saturday 4:00 PM, Sunday 9:00 AM".

It shares a pastor, deacon and webmaster (both Wix sites store files under `23b1db_`) with St.
Joseph the Worker, Frackville, and its Mass list prints Frackville's weekend times, but the two
publish **separate bulletins** with their own mastheads (Frackville's 18 October issue is
"St. Joseph the Worker Parish", six image pages), so they are two rows.

## Worship sites

- `st-charles-borromeo-ashland`: the parish church at Walnut Street, Ashland, with daily Mass
  in St. Anne Chapel on its lower level (same building, no separate row).

Ruled out (`excluded/`): St. Vincent de Paul, Girardville (kept as a worship site after 2015,
regular Masses ended 2021, last Mass 5 January 2026); St. Joseph, Girardville; St. Mauritius,
Ashland; Our Lady of Good Counsel, Gordon (all named as closed churches in 2019).

## Website and bulletin provider

`other`: stcharlesashland.com (the diocese map's website) lists the PDFs on its "2026
Bulletins" page (/s-projects-side-by-side). The bulletin PDFs have undated hash names; each
sits in a Wix card (`role="listitem"`) whose text gives its date ("October 18, 2026") and
Sunday. The first `fetch_check_rows.py` run on 2026-10-18 picked
`23b1db_b2e89158728245ffb01ce935bd08daa3.pdf` ("first-listed"), the parish's one-page
coat-of-arms description linked from the site header on every page. The resolver now dates
an undated PDF link by the one date in its card; on 2026-10-19 it picked
`23b1db_5ff7151c62a641f59cf5dbc1925ba022.pdf`, the 18 October issue ("page-pdfs on
https://www.stcharlesashland.com/s-projects-side-by-side: current"), and that recipe is
pinned.

## Not yet confirmed

Nothing about the publisher.
