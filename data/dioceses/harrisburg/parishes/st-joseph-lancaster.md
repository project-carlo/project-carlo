---
name: St. Joseph Catholic Church
website: http://www.stjosephslanc.com/
bulletin_provider: discover_mass
provider_id: st-joseph-lancaster-pa
publication: ['discovermass:st-joseph-lancaster-pa']
group: ''
evidence:
- url: https://discovermass.com/church/st-joseph-lancaster-pa/
  seen: 2026-10-19
  quote: 440 SaintJoseph Street Lancaster, PA17603
  note: Page 1 masthead of the 18 October 2026 issue (J.S. Paluch; newest listed), after "SAINTJ OSEPHC
    ATHOLIC CHURCH". Text layer garbles spacing.
- url: https://discovermass.com/church/st-joseph-lancaster-pa/
  seen: 2026-10-19
  quote: Saturday evening at 5:00pm Sunday at 8:00am and 10:30am, 9:00am (Swahili Mass) 2nd and 4thS undayso
    ft he month
  note: Weekend Mass box of the same issue; it continues "Monday to Friday at 6:30am".
- url: https://parishesonline.com/organization/st-joseph-church-17603
  seen: 2026-10-19
  note: LPi organization lpi:0018000000Qx9QAAAZ has no publications (probe po); not recorded.
- url: https://lancasterlatinmass.com/mass-confession-schedule/
  seen: 2026-10-20
  quote: 'Masses are currently offered at two different locations: St. Joseph Church and Holy Family Chapel.'
  note: 'The Lancaster Latin Mass Community''s schedule: "St. Joseph Catholic Church 440 St. Joseph Street
    Lancaster, PA 17603 Sundays: 1:00 p.m."'
revisit: 'Re-run the fetch check: on 2026-10-20 Discover Mass refused the download with its daily cap
  ("Maximum number of files downloaded today").'
revisit_after: 2026-10-22
---

## Publisher

St. Joseph Catholic Church ("on Cabbage Hill"), 440 Saint Joseph Street, Lancaster, publishes
its own weekly bulletin through J.S. Paluch on Discover Mass. The 18 October 2026 issue (read
19 October) has a page 1 masthead naming the church at 440 Saint Joseph Street and Father Pang
Joseph Shiu Tcheou as pastor, and a Mass box: Saturday 5:00pm; Sunday 8:00am and 10:30am, with a
9:00am Swahili Mass on the 2nd and 4th Sundays; weekdays Monday-Friday 6:30am. It reports Mass
attendance at the 5:00pm, 8:00am and 10:30am Masses of 11 October.

## Worship sites

One church, `st-joseph-lancaster`. The Adoration Chapel and the "lower chapel" for weekday
Mass are rooms of the same church. No other building is named.

The Lancaster Latin Mass Community ("of St. Joseph's") holds a Sunday 1:00 p.m. Traditional
Latin Mass in this church and a Tuesday 7:30 a.m. one in Holy Family Chapel at Historic St.
Mary's, per its own site (lancasterlatinmass.com, read 20 October 2026). St. Joseph's 18 October
bulletin does not list the 1:00 p.m. Mass; the community publishes its own schedule and
newsletter, which is not a row here (see Not yet confirmed).

## Website and bulletin provider

`discover_mass`, provider_id `st-joseph-lancaster-pa`. The parish's own site
(www.stjosephslanc.com, from the directory) is behind a Cloudflare challenge that did not clear
in about 20 browser loads on 19 October, so it is the website but not the source read. Its empty
LPi organization is noted in evidence.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows, under xvfb-run with Chrome): the resolver found the newest issue's download link but got a 134-byte page instead of the PDF: Discover Mass answered "Maximum number of files downloaded today", a daily download cap this sandbox had used up while the region was being researched (the same issues downloaded as PDFs on 19 October). Re-run the check on another day before treating it as a failure.

## Not yet confirmed

Whether the Lancaster Latin Mass Community's newsletter (lancasterlatinmass.com) should be a
bulletin row of its own; its Masses are at this church and at Holy Family Chapel, St. Mary's.
