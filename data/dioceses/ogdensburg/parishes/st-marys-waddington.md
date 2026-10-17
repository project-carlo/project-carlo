---
name: St. Mary's Parish (Waddington and Madrid)
website: https://mwcatholics.org/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://mwcatholics.org/files/bulletin.pdf']
group: St. Mary's Parish, Waddington (formerly St. Mary's and St. John the Baptist, Madrid)
evidence:
- url: https://mwcatholics.org/files/bulletin.pdf
  seen: 2026-09-30
  quote: St. Mary’s Parish Weekly 26th SUNDAY OF ORDINARY TIME — SEPTEMBER 27, 2026
  note: Page 1 masthead of the bulletin PDF as served on 2026-09-30 (Last-Modified 2026-09-28). The file
    name never changes, so this quote will disappear when the next issue replaces it; the page-1 block
    also reads "One Parish ~ Two Worship Sites", with "St. John the Baptist, 29 North Street, Madrid,
    NY 13660, Mass Saturday 4:30pm" and "St. Mary’s Church, 34 Oak Street, Waddington, NY 13694, Mass
    Sunday 9:30am".
- url: https://mwcatholics.org/files/bulletin.pdf
  seen: 2026-09-30
  quote: Beginning November 2nd our Mass schedule will be
  note: 'Page 1, "Scheduling Masses": Saturday 4:30 pm at St. John''s, Sunday 9:30 am at St. Mary''s,
    Monday 8:00 am at St. Mary''s, Tuesday 8:00 am at St. John''s, Thursday 8:00 am at St. John''s. Page
    2 "Weekly Parish Schedule" lists the current Masses marked (SJ) and (SM) for the two churches.'
- url: https://mwcatholics.org/
  seen: 2026-09-30
  quote: we are now one parish, with two worship sites (churches)
  note: 'Parish site home page: "As of July 1, 2026, St. John’s Parish of Madrid and St. Mary’s Parish
    of Waddington were officially merged; we are now one parish, with two worship sites (churches)." It
    continues "Beginning November 1, 2026, St. Mary’s Parish will be linked with St. Peter’s Parish."
    The page embeds no bulletin id; its Bulletin link is the PDF above.'
- url: https://www.nny360.com/news/stlawrencecounty/changes-coming-to-area-catholic-communities-on-nov-1/article_03d6fbd0-b5c6-5400-a5ad-766fb7489267.html
  seen: 2026-09-30
  quote: had officially merged as of July 1, and are now one parish with two worship sites
  note: 'Watertown Daily Times, 2 Sep 2026 (paywalled; body scrambled in the raw HTML and readable only
    in a browser, so recheck will probably not find it): the Madrid and Waddington parishes merged 1 July
    2026; Fr. Garry Giroux retires in November and Rev. Mark Reilly (pastor of St. Peter''s Parish, Massena)
    becomes pastor of Madrid and Waddington on 1 November, with Rev. Matthew Conger as parochial vicar.'
- url: https://www.rcdony.org/parish/waddington
  seen: 2026-09-30
  quote: 'Worship Site: St. John the Baptist Church - Madrid'
  note: 'Diocesan directory: "St. Mary''s Church, 34 Oak Street, Waddington" with Madrid as its worship
    site (the directory still has a separate St. John the Baptist entry, Madrid, sharing the same phone
    and website).'
revisit: After 1 November 2026 look at mwcatholics.org and the Massena bulletin. If the Waddington PDF
  stops being updated and the St. Peter's bulletin (container 06/0114) starts to carry Madrid and Waddington,
  merge this row into st-peters-parish-massena; if both are still published keep them apart.
revisit_after: 2026-11-15
promoted: 2026-09-30
---

## Publisher

St. Mary's Parish, Waddington, and St. John the Baptist, Madrid, publish **one** weekly bulletin, "St. Mary's Parish Weekly", as a PDF at mwcatholics.org/files/bulletin.pdf. The issue served on 2026-09-30 is dated 27 September 2026 (2 pages, text layer). Page 1 gives both churches with their Mass times under "One Parish ~ Two Worship Sites" and page 2 has one "Weekly Parish Schedule" for both, marking each Mass (SJ) or (SM). The parish website and the Watertown Daily Times (2 Sep 2026) say the two parishes merged canonically on 1 July 2026 into one parish with two worship sites, under Fr. Garry Giroux until his retirement on 1 November 2026.

## Worship sites

- `st-marys-waddington` (34 Oak St., Waddington): Sunday 9:30 am, Monday (and Wednesday until 2 November) mornings.
- `st-john-the-baptist-madrid` (29 North St., Madrid): Saturday 4:30 pm vigil, Tuesday and Thursday mornings.

The directory's Waddington and Madrid entries are the same two buildings, GCatholic's two entries (18342, 18297) likewise. Nothing else is listed.

## Website and bulletin provider

mwcatholics.org (a small self-hosted site; `probe url` reads it, 200) links "Bulletin" to `mwcatholics.org/files/bulletin.pdf`, which is overwritten each week, so provider `other` with `url:https://mwcatholics.org/files/bulletin.pdf` as the publication. The diocese's Parish Bulletins page links the same PDF for Madrid and Waddington. There is no ParishesOnline, eCatholic or Discover Mass account: the page embeds no id (`visit.py --bulletin`: "looks self-hosted"). Because the URL never changes, dated quotes from the PDF are lost each week; the site's home page text is the more durable evidence.

Recipe `page-pdfs`, pinned after `fetch:check` on 2026-10-17 picked the fixed `files/bulletin.pdf`, then carrying the 18 October 2026 issue (`titled`).

## Not yet confirmed

- From 1 November 2026 the parish is "linked with St. Peter's Parish" (Massena) and shares its pastor. The parish keeps its own bulletin in the issue read; whether it will fold into the Massena bulletin is unknown. Not a merge yet, because the Waddington channel is live and no shared bulletin exists. See `revisit`.
