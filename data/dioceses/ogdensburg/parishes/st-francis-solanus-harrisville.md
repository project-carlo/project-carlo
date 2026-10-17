---
name: St. Francis Solanus Church, Harrisville
website: https://www.rcdony.org/images/Harrisvillebulletin-1.pdf
bulletin_provider: other
provider_id: redirected-pdf
publication: ['url:https://www.rcdony.org/images/Harrisvillebulletin-1.pdf']
group: ''
evidence:
- url: https://www.rcdony.org/images/Harrisvillebulletin-1.pdf
  seen: 2026-09-30
  quote: Telephone & Fax (315)543-2421
  note: 'The bulletin dated 27 September 2026 (2 pages, text layer): letterhead "St. Francis Solanus Church
    14361 Maple Street Post Office Box 208 Harrisville, NY 13648-0208", pastor Rev. Joseph Morgan, "Readings
    and Intentions" for Sunday 27 September and Sunday 4 October, "COFFEE HOUR Next Sunday, October 4th
    downstairs after Mass". The URL is one fixed file on the diocese''s site that is overwritten each
    week, so the quote will stop being found; it is not a dated URL. It prints no Mass time.'
- url: https://www.rcdony.org/directory/parish-bulletins.html
  seen: 2026-09-30
  note: 'The diocese''s "Parish Bulletins" page lists Harrisville with exactly this file (rcdony.org/images/Harrisvillebulletin-1.pdf).
    The parish has no website of its own: the directory entry (www.rcdony.org/parish/harrisville) gives
    none.'
- url: https://discovermass.com/church/st-francis-solanus-harrisville-ny/
  seen: 2026-09-30
  note: 'Discover Mass listing (`discovermass:st-francis-solanus-harrisville-ny` per `probe url`): "Mass
    Times Sunday 10:30am" and "Shucks! There are no bulletins available." The Mass time is the only source
    for 10:30 and its date is unknown; no bulletin is posted there, so it is not recorded as a publication
    id.'
promoted: 2026-09-30
---

## Publisher

St. Francis Solanus Church, 14361 Maple Street, Harrisville publishes a two-page parish
bulletin that the diocese hosts at a fixed URL (`www.rcdony.org/images/Harrisvillebulletin-1.pdf`,
server Apache, 805 kB, fetched 2026-09-30). The issue read is dated 27 September 2026. It is
headed by the church's own name, has one pastor (Rev. Joseph Morgan, who also administers
St. Stephen's, Croghan, whose bulletin is separate) and a parish-office telephone and e-mail
(harrisvillebk@rcdony.org), and lists the next two Sundays' intentions. It prints no
Mass times: Sunday 10:30 am comes from Discover Mass only.

## Worship sites

One: `st-francis-solanus-harrisville`. The directory and GCatholic list only this church.

## Website and bulletin provider

The parish has no website. The diocese's bulletin page links the fixed PDF, so the PDF URL is
used as the `website` (where the bulletin can be found) and as the `url:` publication, and the
provider is `other`. There is no ParishesOnline, eCatholic or Discover Mass bulletin (Discover
Mass has a listing with no issues). As the file is overwritten weekly, the pipeline reads
whatever the current issue is.

Recipe `redirected-pdf`, pinned after `fetch:check` on 2026-10-17 picked the PDF itself, then carrying the 18 October 2026 issue (`only-link`).

## Not yet confirmed

- The Sunday Mass time (10:30 am, Discover Mass only; undated) is not in the bulletin. Confirm
  against a later bulletin or the office (315-543-2421) before relying on it.
- Fixed-URL evidence: recheck will report the quote missing once the next issue replaces this one.
