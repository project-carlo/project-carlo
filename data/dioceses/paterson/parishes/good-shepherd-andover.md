---
name: Good Shepherd
website: https://goodshepherdrc.org/bulletins-1
bulletin_provider: other
provider_id: page-pdfs https://goodshepherdrc.org/bulletins-1
publication: ['ecatholic:11119']
group: ''
evidence:
- url: https://files.ecatholic.com/11119/documents/2026/10/November%201%202026%20web.pdf
  seen: 2026-11-04
  quote: 48 Tranquility Road (Route 517), Andover, NJ 07821
  note: '1 November 2026 issue (8 pages; pages 2-6 are images with no text layer, pages 7-8 a November
    calendar insert). Page 1 text: ''©2012 Bon Venture Services, LLC Good Shepherd R.C. Church'', the
    address above and an All Saints cover. Page 2 (rendered with render.py, an image): ''NOVEMBER 1, 2026
    SOLEMNITY OF ALL SAINTS'', Mass intentions Saturday 5:00 PM, Sunday 7:30, 9:00 and 11:00 AM, Daily
    Mass November 2-6 @ 8:30 AM, and a PRIEST''S MASS SCHEDULE for the same four weekend Masses. The ad
    page footer reads ''024E (PK) - Andover, Good Shepherd ... BON VENTURE SERVICES, LLC''.'
- url: https://goodshepherdrc.org/bulletins-1
  seen: 2026-11-04
  note: Read with visit.py. 'Weekly Bulletins' lists dated labels 'November 1, 2026', 'October 25, 2026',
    ... each Sunday back to March, linking files.ecatholic.com/11119/documents/<y>/<m>/<Month D YYYY>
    web.pdf; nothing under the site's bulletins/ archive.
- url: https://goodshepherdrc.org/
  seen: 2026-11-04
  note: 'probe url: status 200, title ''Good Shepherd, Andover - Andover, NJ'', publications ecatholic:11119
    and ecatholic:5303 (the diocese''s own site, not recorded); bulletin link /bulletins-1. Finder pin
    directory:11119 gives this website.'
- url: https://goodshepherd-church.com/
  seen: 2026-11-04
  note: 'GCatholic 19036''s website (www.goodshepherd-church.com) now loads ''Good Shepherd Mission Church'',
    a mission founded at Mamallapuram, Tamil Nadu (read with visit.py): a lapsed domain unrelated to this
    parish, not used.'
bulletin_status: available
---

## Publisher

Good Shepherd, Andover publishes its own weekly bulletin, printed by Bon Venture (page 1 "©2012 Bon Venture Services, LLC", ad footer "024E (PK) - Andover, Good Shepherd") and posted on the parish's eCatholic site (id 11119). The 1 November 2026 issue (`https://files.ecatholic.com/11119/documents/2026/10/November%201%202026%20web.pdf`, read 2026-11-04) is headed "Good Shepherd R.C. Church, 48 Tranquility Road (Route 517), Andover" and names no other parish.

## Worship sites

- `good-shepherd-andover`: page 2 of the 1 November issue (an image, rendered) gives Saturday 5:00 PM, Sunday 7:30, 9:00 and 11:00 AM (the intentions print "7:30 PM"; the Priest's Mass Schedule beside them gives 7:30 AM, as do the finder and the site), and Daily Mass November 2-6 at 8:30 AM.

The issue's text names no chapel or mission. The finder (directory:11119) and GCatholic (19036) list this one church.

## Website and bulletin provider

`goodshepherdrc.org` is the eCatholic site (id 11119, finder pin 11119). It posts the bulletin not in the eCatholic `bulletins/` archive but as documents-folder PDFs listed on `/bulletins-1` with dated labels ("November 1, 2026"), so the row is `other` with a page-pdfs recipe on that page, and keeps `ecatholic:11119` as its publication id. Bon Venture is the printer, not the host. Pages 2-6 of the issue are images: probe pdf can't read the Mass times, and render.py was used for page 2. `fetch:check` on 2026-11-04 resolved "page-pdfs on https://goodshepherdrc.org/bulletins-1: current" (the recipe recorded in `provider_id`) and picked the "November 1 2026 web.pdf" file, dated 2026-11-01 from its label (3 days old: fresh). Identity is unverified (no expected identity supplied, and the masthead pages are images); page 1-2 were checked by hand above.

GCatholic's website for the church, goodshepherd-church.com, is a lapsed domain now used by an unrelated mission in India.

## Not yet confirmed

Nothing open.
