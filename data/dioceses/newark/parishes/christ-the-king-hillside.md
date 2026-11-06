---
name: Christ the King, Hillside
website: https://christthekinghillsidenj.org/
bulletin_provider: other
provider_id: dated-post https://christthekinghillsidenj.org/category/bulletin/
publication: ['url:https://christthekinghillsidenj.org/category/bulletin/']
group: ''
evidence:
- url: https://christthekinghillsidenj.org/wp-content/uploads/2026/10/CTK20261101.pdf
  seen: 2026-11-05
  note: '1 November 2026 issue, 3 pages (proxy gets RemoteDisconnected; read with visit.py --screenshot).
    Page 1 masthead: ''CHRIST THE KING ROMAN CATHOLIC CHURCH, 411 RUTGERS AVENUE, HILLSIDE NJ 07205'';
    ''Rev. Gabriel J. Curtis … Pastor'', ''Rev. Joseph Simon DosSantos … Parochial Vicar''; website christthekinghillsidenj.org.
    ''SUNDAY MASSES: Saturday evening: 5:30 PM; Sunday: 8:00 AM (English), 9:30 AM (Vietnamese), 11:00
    AM (English), 7:00 PM (Portuguese). WEEKDAY MASSES: Monday - Saturday: 8:30 AM''. No other parish
    or church named.'
- url: https://christthekinghillsidenj.org/wp-json/wp/v2/media?mime_type=application/pdf&per_page=20
  seen: 2026-11-05
  note: 'WordPress media list (visit.py --text): weekly uploads CTK20261101.pdf (2026-10-29), CTK20261025,
    CTK20261018, CTK20261011, CTK20261004, CTK20260927 … CTK20260906, plus OCT-2026-newsletter.pdf.'
- url: https://christthekinghillsidenj.org/
  seen: 2026-11-05
  quote: visit our church and rectory at 411 Rutgers Ave, Hillside NJ 07205
  note: WordPress homepage (visit.py; probe url UNREACHABLE, RemoteDisconnected). Recent posts 'Bulletin
    – Nov 1, 2026', 'Bulletin – Oct 25, 2026', 'Bulletin – Oct, 18, 2026' (category /category/bulletin/),
    each embedding that week's CTK<yyyymmdd>.pdf.
bulletin_status: available
publication_reviews:
- parish: st-catherine-of-siena-hillside
  decision: separate
  evidence:
  - url: https://christthekinghillsidenj.org/wp-content/uploads/2026/10/CTK20261101.pdf
    seen: 2026-11-05
    note: The 1 November 2026 masthead names Christ the King Roman Catholic Church alone (411 Rutgers
      Avenue), with its own Mass schedule; self-hosted on its WordPress site.
  - url: https://www.church-bulletin.org/bulletin/the-church-of-saint-catherine-of-siena-hillside-nj-07205/2026-11-01.pdf
    seen: 2026-11-05
    note: The 1 November 2026 masthead names Saint Catherine of Siena Church alone (1000 North Broad St.),
      with its own Mass schedule; John Patrick id 651.
---

## Publisher

Christ the King, Hillside, posts its own weekly bulletin on its WordPress site: one post per issue in the 'Bulletin' category, each embedding a PDF named `CTK<yyyymmdd>.pdf` in wp-content/uploads (weekly since at least 6 September 2026, from the wp-json media list). I read the 1 November 2026 issue (CTK20261101.pdf, 3 pages, opened in the browser): masthead 'Christ the King Roman Catholic Church, 411 Rutgers Avenue, Hillside NJ 07205', 'Rev. Gabriel J. Curtis, Pastor', 'Rev. Joseph Simon DosSantos, Parochial Vicar', and one Mass schedule for this church. No printer's footer: self-made.

**St. Catherine of Siena, Hillside (same pastor from July 2026).** The job input says the two Hillside parishes have had one pastor since July 2026. The bulletins are still separate: St. Catherine's John Patrick bulletin (id 651) of 1 November 2026 names St. Catherine alone, with its own schedule, and its pastor signs 'Fr. Gabo' / 'P. Gabriel'. This one names Christ the King alone. Recorded as a `separate` review.

## Worship sites

- Christ the King Church, 411 Rutgers Avenue (`christ-the-king-hillside`): Saturday 5:30 PM; Sunday 8:00 AM, 9:30 AM (Vietnamese), 11:00 AM, 7:00 PM (Portuguese); Monday-Saturday 8:30 AM (1 November 2026 masthead). The homepage schedule still says 8:00 AM weekdays; the bulletin is newer.

The directory (64) and GCatholic (18425) list only this church.

## Website and bulletin provider

https://christthekinghillsidenj.org/ (the directory's and the masthead's site). `probe url` and `probe pdf` get RemoteDisconnected from it through the proxy (as for sjanj.net in the playbook), while the browser reads it. Provider `other`, read with `dated-post https://christthekinghillsidenj.org/category/bulletin/` (one post per issue).

Fetch check (2026-11-05, headed): transport ok, PDF, resolved `dated-post on https://christthekinghillsidenj.org/category/bulletin/: current` and picked wp-content/uploads/2026/10/CTK20261101.pdf, the 1 November 2026 issue read above; freshness fresh (4 days). Publication identity `unverified` only because no expected identity is supplied. Without a pin, the resolver picked `page-pdfs` on the single 1 November post, which would not move to later issues, so the `dated-post` recipe is pinned instead. `publication` is the bulletin category page, the one place this bulletin is published.

## Not yet confirmed

Nothing open for the row.
