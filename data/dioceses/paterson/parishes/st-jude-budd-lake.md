---
name: St. Jude Thaddeus
website: https://stjudeparish.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=11146
publication: ['url:http://sponsors.bonventure.net/?page=11146']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/11146/2026-11-01.pdf
  seen: 2026-11-04
  quote: 169E (PK) - St. Jude Thaddeus, Budd Lake
  note: Pages 1-5 are images; rendered with render.py. Page 1 masthead names 'ST. JUDE THADDEUS CHURCH,
    17 Mount Olive Road, Budd Lake, NJ 07828', www.stjudeparish.org, Pastor Rev. J. Antonio Gaviria, with
    Mass Times Saturday 5:30PM; Sunday 8:00 AM, 10:00 AM, 12:00 PM; Monday-Saturday 9:00 AM. Page 2 heads
    'ALL SOULS DAY November 1, 2026'. The quote is the page 6 ad footer.
- url: https://stjudeparish.org/
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403). eCatholic site id 20010; the menu
    link 'BULLETINS' goes to http://sponsors.bonventure.net/?page=11146. The site has no /bulletins page.
- url: http://sponsors.bonventure.net/?page=11146
  seen: 2026-11-04
  note: Bon Venture sponsor page; probe url finds the bulletin link http://sponsors.bonventure.net/pdfs/11146/2026-11-01.pdf.
bulletin_status: available
---

## Publisher

St. Jude Thaddeus Church, Budd Lake publishes its own weekly bulletin through Bon Venture (sponsor page 11146). The 1 November 2026 issue (`http://sponsors.bonventure.net/pdfs/11146/2026-11-01.pdf`, read 2026-11-04) is image-only on pages 1-5, so page 1-2 were rendered with render.py. Page 1's masthead reads "ST. JUDE THADDEUS CHURCH, 17 Mount Olive Road, Budd Lake, NJ 07828", website www.stjudeparish.org, pastor Rev. J. Antonio Gaviria. Page 2 is headed "ALL SOULS DAY November 1, 2026". The page 6 ad footer (text layer) reads "169E (PK) - St. Jude Thaddeus, Budd Lake".

## Worship sites

- `st-jude-budd-lake`: the only church. Page 1's "MASS TIMES" (Saturday 5:30PM; Sunday 8:00 AM, 10:00 AM, 12:00 PM; Monday - Saturday 9:00 AM; Holy Days 9:00 AM, 7:00 PM) names no other place; page 2 mentions only the "Daily Mass Chapel", a room in the church used for adoration and meetings, not a separate site.

The diocese's finder (directory:20010) and GCatholic (19039) both list this one church.

## Website and bulletin provider

`stjudeparish.org` is the parish's eCatholic site (site id 20010, the finder pin id), behind Cloudflare (probe url: 403). visit.py read it on 2026-11-04: its menu link "BULLETINS" goes to the Bon Venture sponsor page, and there is no eCatholic /bulletins page, so the eCatholic id is not recorded as this bulletin's publication. Provider `other` with the recipe `page-pdfs http://sponsors.bonventure.net/?page=11146`; `fetch:check` on 2026-11-04 resolved it to `http://sponsors.bonventure.net/pdfs/11146/2026-11-01.pdf` (the 1 November 2026 issue, 3 days old: fresh). It reports identity unverified because page 1 has no text layer; the masthead was checked by hand above.

## Not yet confirmed

Nothing open.
