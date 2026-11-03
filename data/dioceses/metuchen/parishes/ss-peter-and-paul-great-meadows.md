---
name: Ss. Peter and Paul
website: http://www.peterpaulgm.com
bulletin_provider: other
provider_id: page-pdfs http://www.peterpaulgm.com/English/Bulletins.html
publication: ['url:http://www.peterpaulgm.com/English/Bulletins.html']
group: ''
evidence:
- url: http://www.peterpaulgm.com/Bulletins/110126.pdf
  seen: 2026-11-03
  quote: SAINTS PETER & PAUL CHURCH
  note: 1 November 2026 issue (dated 'October 31 / November 1, 2026' on page 2), 4 pages, text layer.
    Page 1 masthead names Saints Peter & Paul Church alone, 360 US Hwy 46, Great Meadows, New Jersey 07838,
    'Rev. Grzegorz Podsiadlo Administrator', Masses Saturday Evening 5:00 pm, Sundays 7:30 am, 10:00 am
    (Eng), 11:30 am (Pol), weekdays (including Sat.) 8:30 am.
- url: http://www.peterpaulgm.com/Bulletins/110126.pdf
  seen: 2026-11-03
  quote: 106B (CK)  Sts. Peter & Paul, Great Meadow
  note: 'Page 4 ad-page code line: Bon Venture Services prints the bulletin (account 106B); the parish
    posts it on its own site.'
- url: http://www.peterpaulgm.com/English/Bulletins.html
  seen: 2026-11-03
  note: Plain HTML Bulletins page (read with visit.py --links) lists '11/1/26--All Saints Day' at /Bulletins/110126.pdf
    first, then weekly issues back to 8/16/26, named <MMDDYY>.pdf.
- url: https://diometuchen.org/parishfinder
  seen: 2026-10-30
  note: 'The diocese''s finder lists Ss. Peter and Paul, 360 U.S. Highway 46, Great Meadows, NJ 07838-0156,
    website http://www.peterpaulgm.com, ''Administrator: Rev. Grzegorz Podsiadlo, SDS'', matching the
    masthead.'
promoted: 2026-11-03
bulletin_status: available
---

## Publisher

The parish posts its own bulletin on its plain HTML site, www.peterpaulgm.com/English/Bulletins.html, as `/Bulletins/<MMDDYY>.pdf`. The 1 November 2026 issue (4 pages, text layer; page 2 dates it "October 31 / November 1, 2026") has the masthead on page 1: "SAINTS PETER & PAUL CHURCH", 360 US Hwy 46, Great Meadows, New Jersey 07838, Rev. Grzegorz Podsiadlo, Administrator, Masses Saturday Evening 5:00 pm, Sundays 7:30 am, 10:00 am (Eng) and 11:30 am (Pol), weekdays (including Sat.) 8:30 am. Bon Venture Services prints it: page 4's code line reads "106B (CK) Sts. Peter & Paul, Great Meadow". No other parish or church is named. A DuckDuckGo search (2026-11-03) found no `sponsors.bonventure.net` listing for the parish, so only the parish-hosted copy is recorded.

## Worship sites

One church, 360 U.S. Highway 46 (directory:24491, gcatholic:18691). Page 2 mentions "our chapel" for a noon devotion; it is part of the church building, not a separate site.

## Website and bulletin provider

`other` with `page-pdfs http://www.peterpaulgm.com/English/Bulletins.html`. The site is http only: `probe url` reported DEAD-DNS (unreliable here), and https fails with a certificate hostname mismatch, while the browser loads the http site. `fetch:check` (2026-11-03) picked `/Bulletins/110126.pdf`, the 1 November issue, but reports issue date and freshness `unknown`: the `<MMDDYY>` file name and the masthead carry no date it can parse (the date is on page 2).

## Not yet confirmed

Nothing open.
