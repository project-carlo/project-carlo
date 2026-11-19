---
name: Assumption of the Blessed Virgin Mary, Providence
website: https://assumptionparishpro.faith/parish-bulletin.php
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://dioceseofprovidence.org/parishfinder
  seen: 2026-11-14
  quote: is mission church of Assumption of the Blessed Virgin Mary, Providence
  note: 'Finder entry 12191 ''Assumption of the Blessed Virgin Mary'', 791 Potters Ave., website assumptionparishpro.faith,
    Pastor Rev. Gildardo Suarez: ''Beginning July 2010, St. Anthony Church, 549 Plainfield St., Providence,
    RI, 02909, is mission church of Assumption of the Blessed Virgin Mary, Providence.'' Entry 12202 (St.
    Anthony) gives the same website and pastor. Read in a browser.'
- url: https://web.archive.org/web/20250707203145/https://assumptionparishpro.faith/
  seen: 2026-11-15
  note: Last archived homepage (7 July 2025), titled 'Assumption of the BVM & St Anthony's Mission | Providence,
    RI'; its bulletin links are parish-bulletin.php and files/bulletins/scan-20200314.pdf ('Weekend of
    March 14-15, 2020'), the newest bulletin it lists.
revisit: Reopen assumptionparishpro.faith (522 on 2026-11-15) and its parish-bulletin.php for issues newer
  than March 2020.
revisit_after: 2026-12-15
research:
- method: probe url and parish-site-access visit.py --bulletin on the finder's homepage (http and https,
    with and without www)
  url: https://assumptionparishpro.faith/
  checked: '2026-11-15'
  outcome: access-blocked
  next_action: Reopen the site and its parish-bulletin.php page; if issues newer than March 2020 are listed,
    set provider other with a page-pdfs recipe on that page
  retry_when: The site answers again (it returned Cloudflare 522 'Connection timed out' on 2026-11-15)
  revisit_after: 2026-12-15
- method: Wayback CDX listing of assumptionparishpro.faith/* and the 2025-07-07 homepage snapshot
  url: https://web.archive.org/web/20250707203145/https://assumptionparishpro.faith/
  checked: '2026-11-15'
  outcome: not-found
  next_action: None from the archive; check the live site instead
  retry_when: The live site returns
- method: probe po guesses (assumption-church-02907, church-of-the-assumption-02907, assumption-of-the-blessed-virgin-mary-02907,
    st-anthony-church-02909, st-anthonys-church-02909) and DuckDuckGo searches for the parish with 'Potters
    Ave' and for St. Anthony '549 Plainfield'
  checked: '2026-11-15'
  outcome: not-found
  next_action: Ask the parish office (401-941-1248) or read its Facebook page (facebook.com/assumptionparishpro,
    which refused probe get with HTTP 400) in a browser for a posted bulletin
  retry_when: A browser session that can read Facebook pages, or a new link from the parish or diocese
bulletin_status: not-found
---

## Publisher

No current bulletin found. The parish's site, assumptionparishpro.faith (the finder's link for both Assumption and its mission St. Anthony), answered Cloudflare 522 "Connection timed out" to `probe url` and to the browser on 15 November 2026. Its last archived homepage (Wayback, 7 July 2025), titled "Assumption of the BVM & St Anthony's Mission", still linked the bulletin "Weekend of March 14-15, 2020" (`files/bulletins/scan-20200314.pdf`) as its newest, so the parish appears to have stopped posting bulletins in 2020. No ParishesOnline org or other publisher turned up; see `research`.

## Worship sites

Two churches, both from the finder: Assumption, 791 Potters Ave. (Saturday 6:30 PM Spanish, Sunday 9:00 AM English and 12:00 PM Spanish, Wednesday 7:00 PM), and its mission St. Anthony, 549 Plainfield St. (Saturday 4:00 PM and Sunday 10:30 AM, bilingual), "mission church of Assumption" since July 2010. A bulletin, if one turns up, would cover both: the site was the parish's and the mission's together.

## Website and bulletin provider

`no_bulletin`. `website` is the site's bulletin page, which is where issues were posted until 2020; it was unreachable when checked.

## Not yet confirmed

Whether the parish publishes a bulletin anywhere now (site down, Facebook unread); see `research` and `revisit`.
