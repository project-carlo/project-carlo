---
name: Holy Cross, Dover and Immaculate Conception, Marydel
website: https://www.iccmarydel.org/bulletin.html
bulletin_provider: other
provider_id: page-pdfs https://www.iccmarydel.org/bulletin.html
publication: ['discovermass:holy-cross-dover-de', 'url:https://www.iccmarydel.org/bulletin.html']
group: Central Deanery
evidence:
- url: https://www.iccmarydel.org/uploads/6/9/0/4/69049539/october_25_2026.pdf
  seen: 2026-10-27
  quote: Sunday, 7:30, 9:30, 11:30 am Spanish
  note: 'Page 1 of the 25 October 2026 issue (10 pages), posted on iccmarydel.org/bulletin.html. The cover
    is headed ''holy cross'' and ''icc'' with one Mass box for each: Holy Cross Saturday vigil 5 pm, Sunday
    7:30, 9:30, 11:30 am Spanish, weekdays 8 am (Wednesday 8:15); Immaculate Conception Sunday 8:30 and
    11 am, 1 pm Spanish, Thursday 6 pm Spanish. Page 4 lists one staff for both: Rev. Anthony Giamello
    (Pastor), Rev. John Enemuo and Rev. Rommel Padilla (Parochial Vicars), with the Holy Cross School
    address 631 S. State St.'
- url: https://www.iccmarydel.org/uploads/6/9/0/4/69049539/october_25_2026.pdf
  seen: 2026-10-27
  quote: At Holy Cross and Immaculate
  note: 'Page 3, the pastor''s column: ''At Holy Cross and Immaculate Conception, we express this love
    together through the Holy Mass'' (the line breaks before ''Conception''). The pastor writes to one
    ''collaborative Parish community''.'
- url: https://www.iccmarydel.org/parish-clergy-and-staff.html
  seen: 2026-10-27
  quote: serving both Holy Cross Parish and Immaculate Conception Parish
  note: Marydel's clergy page names the priests as serving both parishes and links www.holycrossdover.org.
- url: https://www.discovermass.com/church/holy-cross-dover-de/
  seen: 2026-10-27
  quote: Holy Cross | Discover Mass
  note: 'Holy Cross''s Discover Mass listing (publication discovermass:holy-cross-dover-de) serves the
    same 25 October 2026 issue: page 1 of its newest PDF has the same ''holy cross'' / ''icc'' cover with
    the same Mass boxes (12 pages against the parish copy''s 10, with the text spaced oddly).'
- url: https://holycrossdover.org/about-us/bulletin
  seen: 2026-10-27
  quote: Church of the Holy Cross
  note: 'Holy Cross''s real site, read in the browser (curl gets 403). Its Bulletin page lists dated files
    (newest ''October 25, 2026'', links /about-us/bulletin/2078-october-25-2026/file), so a third copy
    exists. Footer: 631 S State St, Dover, DE 19901 | 302-674-5787.'
promoted: 2026-10-27
research:
- method: curl and probe pdf against holycrossdover.org bulletin files
  url: https://holycrossdover.org/about-us/bulletin/2078-october-25-2026/file
  checked: '2026-10-27'
  outcome: access-blocked
  next_action: Read the file in the browser (visit.py or tools/browser_download.py) if the iccmarydel.org
    copy ever stops being posted
  retry_when: iccmarydel.org/bulletin.html stops listing the current issue
---

## Publisher

Holy Cross, Dover, DE and Immaculate Conception, Marydel, MD print one weekly bulletin. The 25 October 2026 issue (iccmarydel.org, page 1) is headed 'holy cross' and 'icc' with a Mass box for each church; page 4 gives one staff, Rev. Anthony Giamello (Pastor), Rev. John Enemuo and Rev. Rommel Padilla (Parochial Vicars), and page 3's pastor's column addresses the 'collaborative Parish community' of 'Holy Cross and Immaculate Conception'. Marydel's clergy page says the priests serve both parishes. One row, two churches. The pair also shares associates in The Dialog's 2024-25 appointments, which is why the batch checked them.

The 18 October issue (iccmarydel.org/uploads/.../october_18_2026.pdf) has the same headings, so the shared cover is not a one-off. The diocese's map lists the two as separate parishes (Holy Cross `directory:137`, Immaculate Conception `directory:149`, both Central Deanery); the bulletin is what joins them.

## Worship sites

Two churches: Holy Cross, 631 S State St, Dover and Immaculate Conception, 522 Main St, Marydel (a Maryland town on the Delaware line). Nothing else is named in the Mass boxes.

## Website and bulletin provider

Three places carry the same issue: Marydel's Weebly page `https://www.iccmarydel.org/bulletin.html` (dated PDFs newest first, plain curl works), Holy Cross's own `holycrossdover.org/about-us/bulletin` (403 to curl, readable in the browser) and Holy Cross's Discover Mass listing (daily download cap). The row is `other`, pinned `page-pdfs https://www.iccmarydel.org/bulletin.html`, because that is the one the pipeline can read without a browser or a cap. The directory's website for Holy Cross (sub.ireland724.info) is a spam page and GCatholic's (holycrossnet.org) has no DNS; neither is used. `publication` records the Discover Mass id and the Marydel page; the Holy Cross site is an alternate pick if the Marydel page stops updating.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish holy-cross-immaculate-conception-dover-marydel` (2026-10-27): picked iccmarydel.org/uploads/6/9/0/4/69049539/october_25_2026.pdf; transport ok, PDF, issue date inferred as 2026-10-25, freshness fresh. Identity is reported unverified by the tool; the cover read above settles it.

## Not yet confirmed

The Dialog appointment posts were not reopened; the structure rests on the bulletin. Holy Cross's Mass schedule on holycrossdover.org matches the cover (Saturday 5 pm; Sunday 7:30, 9:30, 11:30 am Spanish; Mon, Tue, Thu, Fri, Sat 8 am; Wed 8:15 am).
