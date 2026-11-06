---
name: St. Anthony of Padua, Belleville
website: https://www.stantbell.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/644
publication: ['url:https://www.stantbell.org/', 'url:https://www.church-bulletin.org/saint-anthony-of-padua-church-newark-nj-07107']
group: ''
evidence:
- url: https://www.stantbell.org/uploads/1774ff66a67d452da88dfaac543c8c8a.pdf
  seen: 2026-11-03
  quote: 63 Franklin Street (Silver Lake)
  note: '1 November 2026 issue (5 pages, text layer). Page 1 masthead: ''Solemnity of All Saints November
    1, 2026 St. Anthony of Padua Church 63 Franklin Street (Silver Lake) Belleville, NJ 07109 … www.stantbell.org'';
    pastor Rev. Ranulfo D. Docabo; Mass schedule Saturday 5:30PM (Sunday Vigil Mass), Sunday 8AM, 10:30AM
    & 12:15PM, Monday-Thursday 7AM & 8AM, Friday & Saturday 8AM, every 2nd Sunday 5:30 PM Spanish Mass,
    every last Sunday 5:30 PM Filipino Mass; ''Parish Office: 750 N. 7th Street Newark, NJ 07107''. No
    other church is named and no publisher''s footer appears.'
- url: https://www.stantbell.org/
  seen: 2026-11-03
  note: Read with visit.py (probe url sees no links). The homepage's 'Parish Bulletin' panel lists 'Solemnity
    of All Saints Nov 1, 2026', then Oct 25, Oct 18 and Oct 11, each with a Download link to an undated
    hash-named file under /uploads/ (Nov 1 = 1774ff66a67d452da88dfaac543c8c8a.pdf); the page also links
    OnlineGiving_instructions.pdf before them. The directory's www.saintanthonybelleville.org redirects
    here.
- url: https://www.church-bulletin.org/bulletin/saint-anthony-of-padua-church-newark-nj-07107/2026-11-01.pdf
  seen: 2026-11-05
  quote: 644 St. Anthony of Padua, Belleville, NJ
  note: 'John Patrick listing 644 (church-bulletin.org/644 redirects to saint-anthony-of-padua-church-newark-nj-07107),
    1 November 2026 issue, 6 pages: page 1 masthead ''St. Anthony of Padua Church 63 Franklin Street (Silver
    Lake) Belleville, NJ 07109'', website www.stantbell.org, ''5:30PM (Sunday Vigil Mass)'', the same
    page as the stantbell.org upload of that week; footer names John Patrick Publishing. The listing has
    dated issues through 2026-11-08.'
bulletin_status: available
---

## Publisher

The parish makes its own bulletin and posts it on its site. I read the 1 November 2026 issue (text layer, 5 pages): page 1 reads "Solemnity of All Saints November 1, 2026 St. Anthony of Padua Church 63 Franklin Street (Silver Lake) Belleville, NJ 07109". No printer's footer appears.

## Worship sites

One church, `st-anthony-of-padua-belleville`. Page 1's schedule gives Saturday 5:30pm vigil, Sunday 8:00, 10:30am and 12:15pm, a Spanish Mass every second Sunday and a Filipino Mass every last Sunday at 5:30pm, and weekdays 7:00 and 8:00am (Friday and Saturday 8:00am), naming no other place. The parish office is at 750 N. 7th Street, Newark, which the bulletin and site give only as an office. The directory (6) and GCatholic (18362) list only this church.

## Website and bulletin provider

The directory's https://www.saintanthonybelleville.org/ redirects to https://www.stantbell.org/, which the masthead prints. Its homepage builds its links in JavaScript (probe url sees none; visit.py does) and lists the four latest issues newest first as undated 32-character hash names under /uploads/, after a giving-instructions PDF.

The bulletin is printed by John Patrick Publishing: the footer reads '644 St. Anthony of Padua, Belleville, NJ ... John Patrick Publishing Company', and listing https://church-bulletin.org/644 (slug saint-anthony-of-padua-church-newark-nj-07107, after the office's Newark zip) posts the same issue under dated names (1 November 2026 page 1 identical to the stantbell.org upload; 8 November already listed on 2026-11-05). Reconcile (2026-11-05) moved the pin from the hash-named uploads, whose freshness read `unknown`, to the dated listing: provider `other`, `page-pdfs https://church-bulletin.org/644`. Both pages are kept in `publication`.

Earlier fetch check (2026-11-03, headed) on the homepage recipe: ok, picked uploads/1774ff66a67d452da88dfaac543c8c8a.pdf, freshness `unknown`; that is the 1 November 2026 issue. Fetch check (2026-11-05, headed) on the new pin: ok, `page-pdfs on https://church-bulletin.org/644: current`, picked saint-anthony-of-padua-church-newark-nj-07107/2026-11-08.pdf (issue date from the URL, 8 November 2026).

## Not yet confirmed

Whether the hash-name glob keeps selecting the bulletin: if the parish uploads another hash-named PDF (a flyer) above the bulletins, the pick will be wrong.
