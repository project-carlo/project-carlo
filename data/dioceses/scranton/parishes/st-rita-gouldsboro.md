---
name: St. Rita Parish
website: https://www.stritaspa.org/News-Events
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.stritaspa.org/News-Events']
group: Saint Rita Parish
evidence:
- url: https://www.stritaspa.org/News-Events/ID/5176/27th-Sunday-In-Ordinary-Time--October-4-2026
  seen: 2026-10-16
  quote: View the bulletin regarding the 27th Sunday Ordinary
  note: The parish site's News & Events post of Friday 2 October 2026, which embeds the 4 October bulletin
    PDF from c1.nd-cdn.us (read in a browser, parish-site-access visit.py; the Net Driven site gave curl
    a Cloudflare 502 once).
- url: https://c1.nd-cdn.us/PDFs/3547627TH_ORD_10_04_26-1.pdf
  seen: 2026-10-16
  quote: Sat. Oct. 3 VIGIL-TWENTY-SEVENTH SUNDAY IN ORDINARY TIME
  note: 'Page 1 of the 4 October 2026 bulletin: Mass intentions Saturday 4:00pm, Sunday 9:00am and 10:30am,
    Tuesday and Thursday 9:00am, all unnamed (one church), and the prayer list "by calling the parish
    office at 570-842-4995" (St. Rita''s number).'
- url: https://www.stritaspa.org/Mass-Schedule
  seen: 2026-10-16
  quote: Saturday-Vigil 4:00 p.m
  note: 'Parish Mass Schedule page: Sunday 9:00 a.m and 10:30 a.m., daily Tuesday & Thursday 9:00 a.m.,
    and "Please check the current bulletin which can be found on the News Page".'
- url: https://discovermass.com/church/st-rita-gouldsboro-pa/
  seen: 2026-10-16
  note: Discover Mass page for St. Rita lists no bulletins (issues.py, 2026-10-16).
promoted: 2026-10-17
---

## Publisher

St. Rita Parish, Gouldsboro posts its own weekly bulletin as a News & Events post on its
site, each embedding a PDF. The newest on 2026-10-16 is "27th Sunday In Ordinary Time -
October 4, 2026" (posted 2 October). Its page 1 lists the week's Mass intentions with no
church named (Saturday 4:00pm, Sunday 9:00am and 10:30am, Tuesday and Thursday 9:00am) and
the parish office number 570-842-4995; the times match the site's Mass Schedule page and the
diocese's finder. The PDF has no masthead naming the parish (page 1 is intentions, the rest
Bon Venture and Loyola Press filler and a "Father Rawel's Corner"), so "this is St. Rita's"
rests on where it is posted and the phone number, not on a title.

The diocese does not group St. Rita with any other parish, and no neighbouring bulletin I
read in this region mentions it.

## Worship sites

One: St. Rita, 512 Main Street (`st-rita-gouldsboro`). GCatholic also lists St. Anthony of
Padua, 889 Main St. (Route 191), Newfoundland, which it calls a mission of St. Rita. The
finder lists only St. Rita for this parish, and neither the bulletin nor the site mentions
Newfoundland, so it is an open question (`open/st-anthony-of-padua-newfoundland.md`), not a
church row.

## Website and bulletin provider

The website is the News & Events list (stritaspa.org/News-Events), where each week's post
links the PDF on Net Driven's CDN (`c1.nd-cdn.us/PDFs/<number><name>.pdf`, file names not
date-based). The posts are not always dated to the week: "23rd Sunday ... August 9, 2026"
and "22 Sunday ... August 30, 2026" were posted on 4 September. The PDF is text. No
publisher id, so `other`. `fetch:check` after promotion (2026-10-17) failed twice with "Execution context was
destroyed" (the page navigates by script while it is read). No recipe would read it yet
either: `dated-post` follows only posts labelled "bulletin", or, on a listing whose address
says "bulletin", posts dated this week, and these posts are titled by their Sunday alone and
run two weeks late (newest 4 October on 17 October). Left without a recipe.

## Not yet confirmed

The 11 October bulletin was not yet posted on 2026-10-16; the site may lag a week or two.
