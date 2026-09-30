---
name: St. James and St. Mary's Parish Community (Carthage and Copenhagen)
website: http://www.catholicsofcarthagecopenhagen.org
bulletin_provider: other
provider_id: ''
publication: ['url:http://www.catholicsofcarthagecopenhagen.org/bulletins.html']
group: ''
evidence:
- url: http://www.catholicsofcarthagecopenhagen.org/images/Bulletin_-_September_27,_2026.pdf
  seen: 2026-09-30
  note: 'Image-only PDF (5 pages, no text layer; `probe pdf` reads 0 pages), drawn with render.py and read by
    eye, so `recheck` cannot find a quote in it. Page 1 is headed "ST JAMES & ST MARY''S PARISH COMMUNITY",
    "SEPTEMBER 27, 2026 | TWENTY-SIXTH SUNDAY IN ORDINARY TIME", with photos of St. James (State Street,
    Carthage) and St. Mary''s (NYS Rt. 12, Copenhagen), pastor Rev. Jaya Kumar Francis, MSC, and "Weekend
    Mass Schedule: Saturday: 4:00pm(ant.) St. James; Sunday: 8:00am St. Mary''s, 10:00am St. James".
    Page 2 "Mass Intentions" lists the week''s Masses at SJ and SM.'
- url: http://www.catholicsofcarthagecopenhagen.org/bulletins.html
  seen: 2026-09-30
  quote: Bulletin for September 27, 2026
  note: 'The parish site''s "Printable Church Bulletins" page (browser, static HTML): six weekly PDFs from
    23 August to 27 September 2026 at /images/Bulletin_-_<Month>_<day>,_2026.pdf. The diocese''s bulletin
    page links this page for both Carthage and Copenhagen.'
- url: http://www.catholicsofcarthagecopenhagen.org/massschedule.html
  seen: 2026-09-30
  quote: 10:00AM St. James
  note: 'The site''s Mass Schedule page: "Saturday: 4:00PM St. James (Ant)", "Sunday: 8:00AM St. Mary''s
    10:00AM St. James"; reconciliation Saturdays 2:30PM at St. James, Sundays 7:30AM at St. Mary''s.'
- url: http://www.sj-sm.org/
  seen: 2026-09-30
  note: 'The directory''s website for both entries, and the address printed on the bulletin ("Website:
    www.sj-sm.org"). It answers 404 (http) and 502 (https) to a browser on 2026-09-30, so the directory''s
    link is dead; GCatholic''s link (the domain used here) works.'
---

## Publisher

The parishes of St. James (Carthage) and St. Mary's (Copenhagen) publish one weekly bulletin,
titled "St James & St Mary's Parish Community", posted as a PDF on their own site
(`catholicsofcarthagecopenhagen.org/bulletins.html`). The 27 September 2026 issue read on
2026-09-30 is an image-only PDF. Its cover shows both churches, one pastor (Rev. Jaya Kumar
Francis, MSC, since May 2026 per the site's St. James history page) and one Mass schedule
(Saturday 4:00 pm and Sunday 10:00 am at St. James; Sunday 8:00 am at St. Mary's); page 2
prints one list of Mass intentions with codes SJ and SM. The directory lists both under one
website and one phone number (315-493-3224, the St. James rectory). One bulletin, one row.

## Worship sites

Two: St. James Minor, Carthage (`st-james-minor-carthage`) and St. Mary's, Copenhagen
(`st-marys-copenhagen`). The bulletin names no other Mass site. GCatholic also lists St. Rita,
Deferiet (an oratory since 2019, see `excluded/st-rita-deferiet`), which is in the Black River
bulletin's area, not this one. The Augustinian Academy (317 West St., Carthage; the
bulletin's own address for it) is the parish school, not a worship site; GCatholic's address
for St. James is the school's.

## Website and bulletin provider

`catholicsofcarthagecopenhagen.org` is GCatholic's link and the diocese's bulletin page's
link; the directory's `sj-sm.org` is dead (see evidence). The site hosts the bulletins
itself, with no ParishesOnline, eCatholic or Discover Mass id (`probe url` found none), so
the provider is `other` and the publication is `url:` of the bulletins page.
**The 27 September bulletin is an image-only PDF** (no text layer), so the pipeline will need
to read the pages as images.

## Not yet confirmed

- Whether every weekly issue is image-only: only the 27 September issue was checked.
- The site's Mass Schedule page lists the same times as the bulletin, but says nothing about
  holy days or seasonal changes.
