---
name: Holy Infant
website: https://holyinfantparish.com/
bulletin_provider: other
provider_id: page-pdfs http://fataonline.com/bulletins/holyinfant
publication: ['url:https://www.fataonline.com/bulletins/holyinfant']
group: ''
evidence:
- url: https://www.fataonline.com/bulletins/holyinfant
  seen: 2026-10-19
  quote: View Current Bulletin
  note: FATA Online page, linked as "Weekly Bulletins" from holyinfantparish.com/bulletins. "View Current
    Bulletin" links /bulletin/bulletin-661792005981.pdf (18 October 2026); archive of dated issues (10/11/2026,
    10/04/2026, 09/27/2026, ...).
- url: https://www.fataonline.com/bulletin/bulletin-661792005981.pdf
  seen: 2026-10-19
  quote: 'WEEKEND MASSES Saturday Vigil: 5:00 PM Sunday: 8:00 AM & 11:00 AM'
  note: 'The 18 October 2026 issue (10 pages, text layer). Page 1: "29th Sunday in Ordinary Time, Sunday,
    October 18, 2026, Holy Infant Church, 535 Conewago Creek Rd * Manchester, PA 17345", Rev. Richard
    McAlister, Pastor. Page 2 calendar lists each Mass and service with place "Church".'
- url: https://holyinfantparish.com/bulletins
  seen: 2026-10-19
  note: eCatholic site behind Cloudflare (read in a browser, parish-site-access visit.py; plain curl gets
    403). Its only bulletin link is "Weekly Bulletins" -> http://fataonline.com/bulletins/holyinfant.
    eCatholic site id 6740 has no files.ecatholic.com/6740/bulletins/ issues for 11, 18 or 25 October.
promoted: 2026-10-20
---

## Publisher

Holy Infant, 535 Conewago Creek Road, Manchester (Manchester and York Haven area, northern
York County) publishes its own weekly bulletin and posts it through FATA Online. I read the
18 October 2026 issue (10 pages): page 1 is headed "Sunday, October 18, 2026, Holy Infant
Church, 535 Conewago Creek Rd * Manchester, PA 17345", names Rev. Richard McAlister,
pastor, and gives "Weekend Masses: Saturday Vigil 5:00 PM, Sunday 8:00 AM & 11:00 AM" (10 am
in summer) and weekday Masses; the page-2 calendar puts every Mass in "Church". One church.

## Worship sites

- Holy Infant, 535 Conewago Creek Road, Manchester (`holy-infant-manchester`).

GCatholic's entry (23714) gives the parish's former address, 34 3rd St., York Haven, and a
Plus Code on that building, which OpenStreetMap now names "Believers in Christ Community
Church" (37 Pennsylvania Avenue, York Haven); its note "ded. 2016.06.19" fits the new
church. I linked 23714 to the current church rather than creating a record for the York
Haven building: no current source lists Mass there.

## Website and bulletin provider

`other`. The parish's own site (eCatholic, holyinfantparish.com) is behind Cloudflare; its
Bulletins page links only to FATA Online, whose page has a fixed "View Current Bulletin"
link and a dated archive of per-issue PDFs. `website` is the parish site; `provider_id`
pins the recipe the fetch check printed, `page-pdfs http://fataonline.com/bulletins/holyinfant`.
The check (2026-10-19/20, Chrome under xvfb) picked the "View Current Bulletin" PDF
(bulletin-661792005981.pdf, 3.5 MB), which I had read by hand as the 18 October 2026 issue.

## Not yet confirmed

Nothing.
