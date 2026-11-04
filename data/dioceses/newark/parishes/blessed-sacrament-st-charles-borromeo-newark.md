---
name: Blessed Sacrament–St. Charles Borromeo, Newark
website: https://www.bsscb.org/bulletins
bulletin_provider: unsupported
provider_id: page-pdfs https://www.bsscb.org/bulletins
publication: ['url:https://www.bsscb.org/bulletins']
group: Planning Area I
evidence:
- url: https://www.bsscb.org/_files/ugd/3c4934_eb9ebe1a47b7453cbcb9d45c8fe6e037.pdf
  seen: 2026-11-04
  quote: 'Sunday Masses: 8 a.m. and 10 a.m.; Igbo Mass: 12:30 p.m.'
  note: '18 October 2026 issue (4 pages, text layer; page 3 ''OCTOBER 18, 2026''). Page 1 masthead: ''Blessed
    Sacrament St. Charles Borromeo Roman Catholic Church'', Fr. Albert Nzeh, Pastor; ''610 Clinton Avenue,
    Newark, NJ 07108 • Parish Center , 19 Van Ness Place''; daily Masses Mon-Sat 8 a.m. (virtual) and
    6:30 pm (Convent Chapel). No printer''s footer: produced by the parish.'
- url: https://www.bsscb.org/bulletins
  seen: 2026-11-04
  note: 'Wix page listing about 400 _files/ugd PDFs by month-day labels without a year in the link text
    (''October 25'', ''October 18'', ...). The ''October 25'' link (3c4934_529f5299a8ef4d7ebd596e1f767f23a5.pdf)
    is a one-page placeholder: ''INTENTIONALLY BLANK BULLETIN COMING SOON''. The 11 and 4 October 2026
    links are full issues with the same masthead.'
- url: https://www.church-bulletin.org/blessed-sacrament-saint-charles-borromeo-newark-nj-07108
  seen: 2026-11-04
  quote: Readings for the Week of November 1, 2026
  note: 'John Patrick listing 546 (church-bulletin.org/546 redirects here) shows only the week''s readings,
    no bulletin issues: not where this parish posts.'
- url: https://www.bsscb.org/parish-history
  seen: 2026-11-04
  quote: Blessed Sacrament and St. Charles Borromeo were merged on May 10, 1999
  note: Parish history page.
research:
- method: fetch:check, headed, page-pdfs on the Wix bulletin page
  url: https://www.bsscb.org/bulletins
  checked: '2026-11-04'
  outcome: unsupported-format
  next_action: When a collector can read Wix link text ('Month D') with the page's year headings, set
    provider other with that recipe and rerun fetch:check; also recheck church-bulletin.org/546 for issues
  retry_when: A collector for undated Wix PDF lists lands, or the parish moves its bulletin to John Patrick
    listing 546
bulletin_status: available
fetch_gap:
  kind: first-pdf-not-current
  seen: 2026-11-04
  url: https://www.bsscb.org/bulletins
  note: 'The Wix bulletin page lists every issue as an undated _files/ugd hash-named PDF, labelled only
    ''October 18'' etc. and laid out in month blocks out of date order. fetch:check 2026-11-04 (page-pdfs
    on the page: first-listed) picked 3c4934_ece2a92fa4704ab8b0facc37891c6bd7.pdf, the 30 August 2026
    issue; the newest full issue is 18 October 2026 (3c4934_eb9ebe1a47b7453cbcb9d45c8fe6e037.pdf). No
    filename glob can select by date, and the parish also posts ''coming soon'' placeholders under the
    next date.'
---

## Publisher

The parish produces its own weekly bulletin (no printer's footer) and posts it on its Wix site. I read the 18 October 2026 issue (https://www.bsscb.org/_files/ugd/3c4934_eb9ebe1a47b7453cbcb9d45c8fe6e037.pdf, page 3 'OCTOBER 18, 2026'): page 1 masthead 'Blessed Sacrament St. Charles Borromeo Roman Catholic Church', Fr. Albert Nzeh, Pastor, '610 Clinton Avenue, Newark, NJ 07108 • Parish Center , 19 Van Ness Place', and one Mass schedule: 'Sunday Masses: 8 a.m. and 10 a.m.; Igbo Mass: 12:30 p.m.'; daily Masses Monday-Saturday 8 a.m. (virtual) and 6:30 pm in the convent chapel.

The newest link on the bulletin page, 'October 25', is a one-page placeholder ('INTENTIONALLY BLANK BULLETIN COMING SOON'); the 18, 11 and 4 October links are full issues.

## Worship sites

- Blessed Sacrament–St. Charles Borromeo Church, 610 Clinton Avenue (`blessed-sacrament-st-charles-borromeo-church-newark`): the only church in the bulletin's schedule. The weekday 6:30 pm Mass in the 'Convent Chapel' is on the parish's own premises (no separate address given), so it is not a separate church row.

The parishes of Blessed Sacrament and St. Charles Borromeo merged on 10 May 1999 (parish history page). GCatholic still lists St. Charles Borromeo church at 84 Custer Ave (18503); the 18 October bulletin does not mention Custer Avenue, and that building is now Greater Friendship Baptist Church (`excluded/st-charles-borromeo-custer-ave-newark`). The directory entry (144) and GCatholic 18489 are this parish and its church.

## Website and bulletin provider

https://www.bsscb.org/ (the directory's bsscb.org redirects there) is a Wix site; probe url found no publisher ids and links /bulletins, which lists every issue as an undated _files/ugd hash-named PDF labelled by month and day only, in month blocks that are not in date order. John Patrick Publishing holds a listing for the parish (546, church-bulletin.org/blessed-sacrament-saint-charles-borromeo-newark-nj-07108), but it shows only the readings for the week of 1 November 2026, so the parish does not post there.

Fetch check (2026-11-04, headed): transport ok, PDF, resolved 'page-pdfs on https://www.bsscb.org/bulletins: first-listed' and picked 3c4934_ece2a92fa4704ab8b0facc37891c6bd7.pdf, which is the 30 August 2026 issue (page text 'AUGUST 30, 2026'), not the current one; issue date and freshness `unknown`. No glob can pick by date from hash names, so the row is `unsupported` with fetch_gap `first-pdf-not-current`, keeping the page as its publication id.

## Not yet confirmed

A collector that reads the page's 'Month D' link labels would also need to skip the 'coming soon' placeholders (see research).
