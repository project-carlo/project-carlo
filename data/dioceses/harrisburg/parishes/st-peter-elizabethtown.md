---
name: St. Peter Catholic Church
website: https://www.stpeteretown.org/
bulletin_provider: discover_mass
provider_id: st-peter-elizabethtown-pa
publication: ['discovermass:st-peter-elizabethtown-pa', 'url:https://www.stpeteretown.org/weekly-bulletin.html']
group: ''
evidence:
- url: https://discovermass.com/church/st-peter-elizabethtown-pa/
  seen: 2026-10-19
  quote: St.PeterChurch,Elizabethtown Twenty-ninthSundayinOrdinaryTime-October18,2026
  note: Page 2 heading of the 18 October 2026 issue (J.S. Paluch; newest listed on Discover Mass; the
    same PDF is the parish site's /uploads/1/3/1/7/131710540/2026-10-18.pdf). Page 1 is a cover. The text
    layer drops spaces.
- url: https://www.stpeteretown.org/uploads/1/3/1/7/131710540/2026-10-18.pdf
  seen: 2026-10-19
  quote: 1:00PM +J osephSeibert(CollegeMassHC)
  note: Page 3 Mass intentions of the same issue - Saturday 4:30PM, Sunday 8:30AM, 10:30AM (C = church)
    and the 1:00PM Elizabethtown College Mass at the Historic Church (HC); "NODAILYMASSatSt.Peter" 19-23
    October (priests' workshop).
- url: https://www.stpeteretown.org/mass--reconciliation.html
  seen: 2026-10-19
  quote: HC= Historic Church ~ One St. Peter Place, Elizabethtown, PA C= Church - 904 Mill Road, Elizabethtown,
    PA
  note: The parish's Mass & Reconciliation page; weekday Masses Monday-Wednesday and Friday 8:00am HC,
    Thursday 6:00pm C; Sunday 1:00 pm Elizabethtown College Mass at Historic St. Peter Church "(When in
    session)".
- url: https://www.stpeteretown.org/weekly-bulletin.html
  seen: 2026-10-19
  quote: Weekly Parish Bulletin
  note: The parish's bulletin page embeds the current issue (as /uploads/1/3/1/7/131710540/101826.pdf
    on 19 October) and lists earlier ones as 2026-10-11.pdf, 2026-10-04.pdf; the homepage links 2026-10-18.pdf.
promoted: 2026-10-20
---

## Publisher

St. Peter Catholic Church, Elizabethtown, publishes one weekly bulletin through J.S. Paluch for
its two buildings. The 18 October 2026 issue (read 19 October; on Discover Mass and the parish's
Weebly site) heads page 2 "St. Peter Church, Elizabethtown" and pictures the "~Historic Church~"
and the "~Church~". Its page 3 Mass intentions mark each Mass by building: Saturday 4:30PM and
Sunday 8:30AM and 10:30AM at the church (C), and Sunday 1:00PM "College Mass HC" at the
Historic Church. The parish's Mass page explains the codes: "HC= Historic Church ~ One St.
Peter Place ... C= Church - 904 Mill Road", with weekday Masses Monday-Wednesday and Friday 8:00am
at the Historic Church and Thursday 6:00pm at the church.

## Worship sites

- `st-peter-elizabethtown`: the present church (904 Mill Road; mailing address 1840 Marshall
  Drive).
- `historic-st-peter-elizabethtown`: Historic St. Peter Church, One St. Peter Place, with four
  weekday Masses and the Sunday 1:00 pm Elizabethtown College Mass during the academic year.
  Neither the directory nor GCatholic lists it as a separate site; the directory's weekday
  line "(Historic Church)" refers to it.

## Website and bulletin provider

`discover_mass`, provider_id `st-peter-elizabethtown-pa`: Discover Mass lists the issues
through 18 October with dates, while the parish's own bulletin page renames its current file
(101826.pdf) from week to week. Both are recorded as publications. The website is the parish
homepage, www.stpeteretown.org.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows, under xvfb-run with Chrome): the resolver found the newest issue's download link but got a 134-byte page instead of the PDF: Discover Mass answered "Maximum number of files downloaded today", a daily download cap this sandbox had used up while the region was being researched (the same issues downloaded as PDFs on 19 October). Re-run the check on another day before treating it as a failure.
Re-run on 2026-10-20 after the cap cleared: `ok`, the newest issue downloaded (2,154,025 bytes).

## Not yet confirmed

Nothing. The text layer of these issues drops most spaces, which the pipeline's text reader
will have to cope with.
