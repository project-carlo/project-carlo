---
name: Holy Family Parish, Seward
website: https://www.holyfamilyseward.org
bulletin_provider: other
provider_id: dated-post https://www.holyfamilyseward.org/bulletins/ filename=20??-*-Bulletin.pdf
publication: ['url:https://www.holyfamilyseward.org/bulletins/', 'po-org:holy-family-church-15954', 'lpi:0018000000QxC0pAAF']
group: ''
evidence:
- url: https://www.holyfamilyseward.org/wp-content/uploads/2026/10/2026-10-18-Bulletin.pdf
  seen: 2026-10-23
  quote: OUR PARISH BULLETIN FOR THE WEEKEND OF OCTOBER 18, 2026
  note: 'The 18 Oct 2026 issue: a single page, headed "WHAT''S HAPPENING AT HOLY FAMILY", no masthead.
    Its "LITURGY SCHEDULE" lists Sat 10/17 4:00 PM, Sun 10/18 9:30 AM, weekday Masses (Mon 6:30 PM; Tue,
    Thu, Fri 12:00 NN; "No Daily Mass" Wednesday) and Sat 10/24 4:00 PM, Sun 10/25 9:30 AM, all with no
    church named; "For the People of Holy Family" on Friday. No other parish or church appears.'
- url: https://www.holyfamilyseward.org/bulletins/
  seen: 2026-10-23
  note: Diocese-template WordPress page (403 to probe url, 200 to curl with a browser User-Agent) listing
    one dFlip post per issue, august-16-2026 to october-18-2026. Each post's PDF is `wp-content/uploads/<yyyy>/<mm>/<yyyy>-<m>-<d>-Bulletin.pdf`
    (2026-9-13-Bulletin.pdf, 2026-10-4-Bulletin.pdf). wp-json shows october-18-2026 posted 2026-10-17
    11:07, the Saturday of that weekend; the earlier issues were back-filled on 2026-10-12.
- url: https://parishesonline.com/organization/holy-family-church-15954
  seen: 2026-10-23
  note: 'probe po: "Holy Family Church", 425 Bridge Street, Seward, website holyfamilyseward.org, lpi
    0018000000QxC0pAAF, no container and no issues. An empty LPi org, recorded here so no other row claims
    it; not a channel.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=261
  seen: 2026-10-22
  note: 'Directory: Holy Family Parish, 425 Bridge Street, Seward, pastor Father John J. Harrold, "Saturday:
    4:00 p.m.; Sunday: 9:30 a.m.", no Partner Parishes. Fr. Harrold serves no other parish in the clergy
    directory (tools/pastors.tsv).'
promoted: 2026-10-23
---

## Publisher

Holy Family Parish, Seward (directory 261) posts its own one-page weekly bulletin on its site. The 18 October 2026 issue (read 2026-10-23 with `probe pdf`) is headed "WHAT'S HAPPENING AT HOLY FAMILY" and "OUR PARISH BULLETIN FOR THE WEEKEND OF OCTOBER 18, 2026", and its "LITURGY SCHEDULE" covers Saturday 17 to Sunday 25 October (Sat 4:00 PM, Sun 9:30 AM, weekday Masses) without naming any other church. There is no masthead and no pastor's name in it. The directory lists no partner parishes and Fr. John J. Harrold is pastor of this parish only (tools/pastors.tsv). One parish, one bulletin, one row.

## Worship sites

Holy Family church, Seward: the only church this parish has in GCatholic (24101) and the directory, and the bulletin's schedule names no other place ("For the People of Holy Family", candle intentions at the Holy Family, St. Therese and St. Anthony shrines inside the church). The LPi geo-search within 6 miles of Seward finds no other Catholic organization.

## Website and bulletin provider

holyfamilyseward.org is a diocese-template WordPress site (403 to `probe url`, 200 to curl with a browser User-Agent). Its /bulletins/ page lists one dFlip post per issue, each with a PDF named `<yyyy>-<m>-<d>-Bulletin.pdf`. The parish's LPi organization (holy-family-church-15954) is empty: no container and no issues. So the provider is `other`, pinned as `dated-post https://www.holyfamilyseward.org/bulletins/ filename=20??-*-Bulletin.pdf` (the playbook's rule for template sites, so a sidebar or privacy-policy PDF can't be picked). `fetch:check` on 2026-10-23 (headed) was ok, "dated-post on https://www.holyfamilyseward.org/bulletins/: current", and picked `2026-10-18-Bulletin.pdf`. That was the newest issue on Friday 23 October; the 18 Oct post went up on Saturday 17 October, so the 25 Oct issue is expected on the 24th.

## Not yet confirmed

The church's street address is not printed in the bulletin itself; it comes from the site footer, the directory, GCatholic and LPi (see the church record).
