---
name: St. Paul's Roman Catholic Church
website: https://www.stpaulsrcc.org
bulletin_provider: other
provider_id: page-pdfs https://www.stpaulsrcc.org/about/bulletins/
publication: ['url:https://www.stpaulsrcc.org/about/bulletins/']
group: ''
evidence:
- url: https://www.stpaulsrcc.org/wp-content/uploads/September-13-2026.pdf
  seen: 2026-10-02
  quote: 783 Hard Road, Webster, New York 14580
  note: Page 1 of the 13 September 2026 issue (8 pages, text).
- url: https://www.stpaulsrcc.org/wp-content/uploads/September-13-2026.pdf
  seen: 2026-10-02
  quote: Mass Times Saturday at 4:00 p.m. Sunday at 9:00 a.m. & 11:00 a.m.
  note: Page 1 of the same issue. St. Paul alone.
- url: https://www.stpaulsrcc.org/about/bulletins/
  seen: 2026-10-02
  note: The "Bulletins" page links one PDF per Sunday under /wp-content/uploads/ (October-4-2026.pdf newest
    on 2 October, back to August 2).
- url: https://www.stpaulsrcc.org/wp-content/uploads/October-4-2026.pdf
  seen: 2026-10-02
  note: 'The 4 October 2026 issue is a scanned image (no extractable text); read as an image with render.py:
    masthead "ST. PAUL’S CHURCH, 783 Hard Road, Webster, New York 14580", "Twenty-Seventh Sunday in Ordinary
    Time October 4, 2026", Mass Times "Saturday: 4:00 p.m. Sunday: 9:00 a.m. & 11:00 a.m.". recheck cannot
    find this by text.'
promoted: 2026-10-02
---

## Publisher

St. Paul's publishes its own weekly bulletin, one PDF per Sunday on its own site. The 13
September 2026 issue (text) gives "783 Hard Road, Webster" and Masses Saturday 4:00 pm and
Sunday 9:00 am and 11:00 am. The 4 October issue is image-only; rendered, it has the same
masthead and Mass times. St. Paul's alone, no group in the diocese's lists.

## Worship sites

One: `st-pauls` at 783 Hard Road.

## Website and bulletin provider

`stpaulsrcc.org` is a WordPress site whose "Bulletins" page (`/about/bulletins/`) links the
PDFs, so provider `other`. **`probe url` and `visit.py` report SPAM-SQUAT for this site, and
that is a false alarm**: the page is the live parish site, with current bulletins, but its HTML
has a hidden `<div style="position:absolute; left:-20914565266523px">` of casino-spam links
("slot gacor" and similar), the mark of a hacked WordPress install. The real content is
intact. Some issues are image-only or partly image (20 September has no text layer; 27
September has three image pages), so extraction will need the OCR path on those weeks.

Fetch recipe `page-pdfs https://www.stpaulsrcc.org/about/bulletins/`, pinned 2026-10-03: on the pages recorded in `tests/fixtures/fetch/st-pauls-webster.json.gz` the resolver found https://www.stpaulsrcc.org/wp-content/uploads/September-27-2026.pdf this way, dated that week.

## Not yet confirmed

Nothing about the publisher. The injected spam is worth a note to the parish if anyone has a
contact. `fetch-check` could not be run here.
