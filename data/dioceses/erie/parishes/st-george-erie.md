---
name: St. George Parish
website: https://stgeorgeerie.org
bulletin_provider: discover_mass
provider_id: saint-george-erie-pa
publication: ['discovermass:saint-george-erie-pa']
group: ''
evidence:
- url: https://discovermass.com/church/saint-george-erie-pa/
  seen: 2026-10-23
  note: 'Discover Mass church page: current bulletin is the 25 October 2026 issue, bulletin number 3303.
    I downloaded it once and read it (8 pages): page 1 lists ''Saint George Roman Catholic Church, 5145
    Peach Street, Erie, PA 16509, Phone (814) 864-0622, www.stgeorgeerie.org, Fr. Brian Vossler, Pastor'';
    the last page prints 3303.'
- url: https://discovermass.com/church/saint-george-erie-pa/
  seen: 2026-10-23
  quote: Saturday 4:30pm Vigil; Sunday 7:30am, 9:30am, 11:30am
  note: 'Page 1 Mass schedule of the 25 Oct 2026 issue (read from the PDF text layer): ''Weekday Mass
    Times: Monday-Friday 7:15am; Saturday 8:00am'', ''Weekend Mass Times: Saturday 4:30pm Vigil; Sunday
    7:30am, 9:30am, 11:30am'', ''Holy Day Mass Times: 7:15am, 9:00am (School Mass), 12:10pm, & 7:00pm''.
    Matches the diocese directory.'
- url: https://stgeorgeerie.org/news-and-events/bulletin/
  seen: 2026-10-23
  quote: October 25th, 2026
  note: 'The parish''s own Bulletin page lists the Discover Mass downloads, newest ''October 25th, 2026'',
    then October 18, 11, 4 (cover images from bulletins.discovermass.com): the site hosts no PDFs of its
    own and reposts the Discover Mass channel.'
- url: https://www.eriercd.org/Parish10307-St-George.html
  seen: 2026-10-23
  note: 'Diocese directory record 10307 (also GCatholic 24507): one parish record, no mission or partner.'
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese erie --parish st-george-erie --expected-identity 'Saint George' --expected-issue-date
    2026-10-25 (headed Chrome)
  url: https://discovermass.com/church/saint-george-erie-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF, identity matched in first-page text; date 'unknown' because the
    masthead date text is split by the layout. Downloaded 2,907,230 bytes, the same size as the 25 October
    2026 issue (number 3303) I read.
---

## Publisher

St. George Parish, Erie publishes its own bulletin through Diocesan Publications' Discover Mass. I read the 25 October 2026 issue on 2026-10-23: the cover block names 'Saint George Roman Catholic Church, 5145 Peach Street, Erie, PA 16509' with 'Fr. Brian Vossler, Pastor', and the content is about this parish only (it lists the parochial vicar Fr. Brandon Feikles and Fr. Phil Oriole, in residence). The diocese has no families; the directory shows one parish record (10307) with no partner or secondary church. The clergy PDF's multi-parish pastor list does not include Vossler.

## Worship sites

One church, St. George at 5145 Peach St. The issue's Mass schedule is for this church alone: weekdays Mon-Fri 7:15am and Saturday 8:00am; weekend Saturday 4:30pm vigil and Sunday 7:30, 9:30 (livestreamed on YouTube) and 11:30am. No other building is named for Mass. The St. George school campus (Erie Catholic School System - St. George Campus) is on the same grounds and not a separate Mass site.

## Website and bulletin provider

`stgeorgeerie.org` (WordPress; the directory's `http://www.stgeorgeerie.org` redirects to https without www) has a Bulletin page that reposts Discover Mass issues, so one channel: provider `discover_mass`, slug `saint-george-erie-pa`. Per the playbook, Discover Mass downloads are capped per IP per day and repeated page hits get blocked, so each page was read once. Bulletin number 3303 on the cover class of the Discover Mass page matches the number on the PDF's last page.

## Not yet confirmed

Nothing open for the row itself.
