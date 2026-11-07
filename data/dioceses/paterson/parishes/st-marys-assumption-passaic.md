---
name: St. Mary's Assumption
website: https://stmarypassaic.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:14062']
group: ''
evidence:
- url: https://files.ecatholic.com/14062/bulletins/20261108.pdf
  seen: 2026-11-05
  note: 'Page 1 of the 8 November 2026 bulletin is an image (rendered with render.py): ST. MARY''S Assumption,
    63 MONROE ST. PASSAIC, NJ 07055, A Welcoming Community of Faith, Hope and Love; phone 973-779-0427;
    Mass schedule Saturday 5PM English, 7PM Spanish; Sunday 9AM English, 11AM Spanish; XXXII Week of Ordinary
    Time. Six pages, only pages 2-3 with text; no printer''s footer (grep for Bon Venture, John Patrick
    found none).'
- url: https://files.ecatholic.com/14062/bulletins/20261108.pdf
  seen: 2026-11-05
  quote: Mass Intentions Readings for the Week
  note: 'Page 2: intentions for 7-15 November, weekday Masses at 8:00AM, and the 1 November collection
    by Mass (5:00 PM, 7:00 PM, 9:00 AM, 11:00 AM).'
- url: https://stmarypassaic.org/bulletins
  seen: 2026-11-05
  note: 'eCatholic site 14062 (read with visit.py): Bulletins newest November 8, 2026, then November 1,
    October 25, 18, weekly back to January 2026.'
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. Mary's Assumption, Passaic produces its own weekly bilingual (English and Spanish) bulletin and posts it on its eCatholic site, site id 14062. Page 1 of the 8 November 2026 issue (`https://files.ecatholic.com/14062/bulletins/20261108.pdf`, read 2026-11-05) is an image; rendered, it reads "St. Mary's Assumption, 63 Monroe St. Passaic, NJ 07055", with phone 973-779-0427 and the Mass schedule. No printer's footer appears.

## Worship sites

- `st-marys-assumption-passaic`: the only church. The page 1 schedule (Saturday 5 PM English, 7 PM Spanish; Sunday 9 AM English, 11 AM Spanish) and page 2's intentions and collections by Mass name no other place; a grep of the text pages for Chapel finds none.

The diocese's finder (directory:14062) and GCatholic (18990) list this one church.

## Website and bulletin provider

The website is the parish's eCatholic site; its `/bulletins` page lists `files.ecatholic.com/14062/bulletins/<YYYYMMDD>.pdf` issues weekly through 8 November 2026 (posted mid-week), so the provider is `ecatholic` with `ecatholic:14062`. Page 1 (masthead and Mass times) is an image and four of six pages have no text layer, so the pipeline's text reading gets only pages 2-3. `fetch:check` on 2026-11-05 picked `https://files.ecatholic.com/14062/bulletins/20261108.pdf`, next Sunday's issue (freshness `future`, age -3 days); its identity is unverified, as expected with an image masthead.

## Not yet confirmed

Nothing open.
