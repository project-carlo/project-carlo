---
name: St. Peter Catholic Church
website: https://www.stpetercolumbiapa.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:14732']
group: ''
evidence:
- url: https://files.ecatholic.com/14732/bulletins/20261018.pdf
  seen: 2026-10-20
  quote: St. Peter Church, Columbia Mother of Holy Purity Chapel, Wrightsville
  note: Page 1 masthead of the 18 October 2026 issue (8 pages, text), under "St. Peter Catholic Church,
    121 South Second Street - Columbia, PA 17512". Pastor "Rev. Mark Wilke".
- url: https://files.ecatholic.com/14732/bulletins/20261018.pdf
  seen: 2026-10-20
  quote: Weekdays at Mother of Holy Purity Chapel (St. Mary), Wrightsville 1st Wednesday of the Month
    ------------------------------ 6:00 pm
  note: Page 1 "Mass Schedule" of the same issue, after "Saturday ... 6:00 pm, Sunday ... 10:30 am, Weekdays
    at St. Peter Church Tuesday & Thursday ... 8:00 am".
- url: https://www.stpetercolumbiapa.org/bulletins
  seen: 2026-10-20
  note: 'Behind Cloudflare (visit.py challenged on every load on 19 October, through on the first load
    on 20 October). eCatholic bulletins page: "October 18, 2026" -> files.ecatholic.com/14732/bulletins/20261018.pdf,
    one issue per Sunday back to August 2026 and earlier.'
---

## Publisher

St. Peter Catholic Church, 121 South Second Street, Columbia, publishes its own weekly bulletin
on its eCatholic site for its church and a chapel across the river. The 18 October 2026 issue
(read 20 October) has the page 1 masthead "St. Peter Catholic Church ... St. Peter Church,
Columbia - Mother of Holy Purity Chapel, Wrightsville", Rev. Mark Wilke pastor, and one schedule:
Saturday 6:00 pm, Sunday 10:30 am, weekdays Tuesday & Thursday 8:00 am at St. Peter Church, and
"1st Wednesday of the Month 6:00 pm" at Mother of Holy Purity Chapel (St. Mary), Wrightsville.

St. Peter and Holy Trinity, Columbia share a pastor, but Holy Trinity prints its own bulletin
(see `holy-trinity-columbia`) and this one lists only St. Peter's Masses: two rows.

## Worship sites

- `st-peter-columbia`, 121 S. 2nd St., Columbia.
- `mother-of-holy-purity-chapel-wrightsville`, 217 Maple St., Wrightsville (York County),
  monthly Mass. No roster lists it; the directory's St. Peter entry mentions "Saint Mary
  Chapel, Wrightsville".

## Website and bulletin provider

`ecatholic`, website https://www.stpetercolumbiapa.org/ (directory; GCatholic's
stpeterromancc.org answers 502), publication `ecatholic:14732`, from the bulletins page's file
links. Behind Cloudflare; the PDFs on files.ecatholic.com fetch without a browser. The LPi
organization st-peter-roman-catholic-church-17512 and the Discover Mass page have no bulletins.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows, under xvfb-run with Chrome): ok, picked files.ecatholic.com/14732/bulletins/20261018.pdf, this week's bulletin. The resolver got past the site's Cloudflare where plain curl could not.

## Not yet confirmed

Nothing.
