---
name: Saint John the Evangelist Parish, Lakemont
website: https://stjohnsaltoona.org/bulletins/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://stjohnsaltoona.org/bulletins/']
group: ''
evidence:
- url: https://stjohnsaltoona.org/wp-content/uploads/2026/10/October-18-2026.pdf
  seen: 2026-10-21
  note: 'Page 1 of the 18 October 2026 issue (29th Sunday in Ordinary Time), read as a rendered image because the PDF has no text layer. Masthead: "St. John the Evangelist Church, 309 Lotz Avenue, Altoona, PA 16602, 814-942-5503", Mass schedule "SATURDAY - 4:00 PM, SUNDAY - 8:00 AM & 11:00 AM", weekdays 8:30 AM Mon/Tue/Thu/Fri and 6:00 PM Wed; staff list Monsignor Michael Becker. It names this church alone.'
- url: https://stjohnsaltoona.org/bulletins/
  seen: 2026-10-21
  note: 'The parish''s own Bulletins page is a flat list of PDFs at wp-content/uploads/<year>/<month>/<Month>-<day>-<year>.pdf, one per Sunday back to 2015; the newest are October-4, October-11 and October-18-2026. There is no ParishesOnline, eCatholic or Discover Mass widget on it.'
---

## Publisher

St. John the Evangelist, Lakemont (Altoona) publishes its own weekly bulletin on its own
WordPress site. I rendered page 1 of the 18 October 2026 issue (the newest, 6 pages, no text
layer) on 2026-10-21. Its masthead reads "St. John the Evangelist Church, 309 Lotz Avenue,
Altoona, PA 16602" with the Mass schedule "SATURDAY - 4:00 PM, SUNDAY - 8:00 AM & 11:00 AM"
and weekday Masses, and names Monsignor Michael Becker. It mentions no other church or parish.
The diocese's directory lists the parish with one church and no companion parish, and the
directory's Mass times (Sat 4:00 PM, Sun 8:00 AM and 11:00 AM) agree with the masthead.

## Worship sites

One church, St. John the Evangelist (churches/saint-john-the-evangelist-altoona). Nothing
else is named in the masthead or the directory entry.

## Website and bulletin provider

`https://stjohnsaltoona.org/bulletins/` lists every issue as a PDF link, so the resolver reads
it as `page-pdfs` (`provider: other`). `pnpm fetch:check --diocese altoona-johnstown --parish
saint-john-the-evangelist-altoona` on 2026-10-21 picked
`https://stjohnsaltoona.org/wp-content/uploads/2026/10/October-18-2026.pdf` (url date
2026-10-18, 652,815 bytes, status ok), the current issue, with recipe `page-pdfs`. `provider_id` is that recipe, `page-pdfs`.

**The bulletins are image-only** (scans: `probe pdf` reports "no extractable text"), so the
pipeline has to read them as images. `recheck` cannot find quotes in them, which is why the
evidence for this issue is a note, not a quote. The directory homepage was `http://stjohnsaltoona.org/`,
which redirects to the https site; `publication` is `url:` of the bulletins page.

## Not yet confirmed

Nothing about the bulletin. The street address of the church is disputed; see the church record.
