---
name: St. John the Evangelist
website: https://www.stjohnsdunellen.org
bulletin_provider: other
provider_id: page-pdfs https://www.stjohnsdunellen.org/bulletins.html
publication: ['url:https://www.stjohnsdunellen.org/bulletins.html']
group: ''
evidence:
- url: http://www.stjohnsdunellen.org/uploads/8/7/9/4/87942936/2026-11-01-164bweb.pdf
  seen: 2026-11-02
  quote: Reverend Alphonsus Kariuki, Pastor
  note: 'Page 1 of the 1 November 2026 bulletin: the masthead names ''Saint John the Evangelist ROMAN
    CATHOLIC CHURCH'', 317 First Street, Dunellen, alone, above one WEEKLY MASS SCHEDULE; page 6 publisher
    line ''164B (PK) - St. John’s, Dunellen … Bon Venture Services, LLC''.'
- url: https://www.stjohnsdunellen.org/bulletins.html
  seen: 2026-11-02
  quote: November 1, 2026
  note: The parish's Weebly Bulletins page lists 2026 issues as /uploads/8/7/9/4/87942936/<YYYY-MM-DD>-164bweb.pdf;
    newest November 1, 2026; no October 2026 issues are posted (the one before is September 20, with a
    September 27 label). Older years are on /bulletin-archive.html.
research:
- method: 'Looked for a Bon Venture sponsors listing: links on the parish home and Bulletins pages; DuckDuckGo
    search ''bonventure St. John the Evangelist Dunellen bulletin'''
  url: https://www.stjohnsdunellen.org/bulletins.html
  checked: '2026-11-02'
  outcome: not-found
  next_action: If the parish page again goes weeks without a new issue, look for a sponsors.bonventure.net/?page=<n>
    listing for '164B' (St. John's, Dunellen) and switch the recipe to it
  retry_when: The Bulletins page's newest issue is more than three weeks old
bulletin_status: available
---

## Publisher

St. John the Evangelist, Dunellen publishes its own weekly bulletin, printed by Bon Venture Services (ad-page code "164B (PK) - St. John’s, Dunellen"), and posts the PDFs on its own Weebly site. I read the 1 November 2026 issue: page 1 names Saint John the Evangelist Roman Catholic Church, 317 First Street, Dunellen, alone, with Rev. Alphonsus Kariuki as Pastor and Deacon Glenn Robitaille (the finder agrees), and one Mass schedule (Saturday Vigil 5:00 pm; Sunday 8:30 am, 10:30 am, Noon Spanish; weekdays 8:00 am in the chapel; Tuesday 7:00 pm Spanish; second Sunday 3:30 pm Kiswahili).

## Worship sites

One church, 317 First Street (`st-john-the-evangelist-dunellen`; directory:24480, gcatholic:18658). The bulletin names no mission; the weekday chapel and the Church Auditorium (where the monthly reception is held) are on the same site.

## Website and bulletin provider

The parish site's Bulletins page (www.stjohnsdunellen.org/bulletins.html; the finder's http://www.stjohnsdunellen.org) links each issue as `/uploads/8/7/9/4/87942936/<YYYY-MM-DD>-164bweb.pdf` (some with `-1`/`-2` suffixes). Provider `other`, recipe `page-pdfs` on that page. The parish posts irregularly: on 2 November the page held no October 2026 issues. The site links no Bon Venture listing (`sponsors.bonventure.net`), so I recorded the parish-hosted copy.

## Fetch check

`pnpm fetch:check` on 2026-11-02 resolved `page-pdfs on https://www.stjohnsdunellen.org/bulletins.html: current` and picked `2026-11-01-164bweb.pdf`: transport ok, PDF, issue date 2026-11-01 inferred from the URL, freshness `fresh`. Publication identity unverified by the tool; I read that issue's masthead (above). The recipe it printed is pinned in `provider_id`.

## Not yet confirmed

Whether Bon Venture also posts this bulletin on a `sponsors.bonventure.net` listing (which would fill the parish site's gaps): the parish site links none and a web search found none (see research).
