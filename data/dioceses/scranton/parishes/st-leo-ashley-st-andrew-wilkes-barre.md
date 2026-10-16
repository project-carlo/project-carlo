---
name: St. Leo the Great and St. Andrew Parishes
website: https://www.standrewwilkesbarre.org
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.standrewwilkesbarre.org/bulletin0283fa5e', 'url:https://stleos-holyrosary.org/bulletins/']
group: Saint Leo the Great Parish; Saint Andrew Parish
evidence:
- url: https://irp.cdn-website.com/2c459b39/files/uploaded/bulletin_october_11_2026.pdf
  seen: 2026-10-16
  quote: ST. LEO the GREAT and ST. ANDREW MASS SCHEDULE
  note: '11 October 2026 issue as posted on St. Andrew''s site, page 1: one masthead for St. Leo the Great
    Parish (33 Manhattan Street, Ashley) and St. Andrew Parish (316 Parrish Street, Wilkes-Barre).'
- url: https://irp.cdn-website.com/2c459b39/files/uploaded/bulletin_october_11_2026.pdf
  seen: 2026-10-16
  quote: Sunday 8:30 a.m. (St. Leo), 11:00 a.m. (St. Andrew)
- url: https://irp.cdn-website.com/2c459b39/files/uploaded/bulletin_october_11_2026.pdf
  seen: 2026-10-16
  quote: 'St. Leo the Great Mission Statement … St. Andrew Mission Statement'
- url: https://stleos-holyrosary.org/wp-content/uploads/2026/10/101126-Combined-bulletin.pdf-.pdf
  seen: 2026-10-16
  quote: ST. LEO the GREAT and ST. ANDREW MASS SCHEDULE
  note: The same 11 October issue as posted on St. Leo's site ('101126 Combined bulletin', Canva PDF).
    stleos-holyrosary.org answers plain fetchers with a bot challenge (HTTP 403 to probe url); read with
    curl and a browser user agent, so recheck may report it unreachable.
- url: https://www.standrewwilkesbarre.org/bulletin0283fa5e
  seen: 2026-10-16
  note: 'St. Andrew''s Bulletin page (Duda site): one PDF per Sunday at irp.cdn-website.com/2c459b39/files/uploaded/bulletin_<month>_<dd>_<yyyy>.pdf,
    newest bulletin_october_11_2026.pdf on 2026-10-16.'
- url: https://stleos-holyrosary.org/bulletins/
  seen: 2026-10-16
  note: 'St. Leo''s Bulletins page (WordPress, read with visit.py): one post per Sunday linking ''<mmddyy>-Combined-bulletin.pdf'',
    newest 101826 (18 October 2026).'
---

## Publisher

St. Leo the Great Parish (Ashley) and St. Andrew Parish (Wilkes-Barre) share a pastor, Rev.
Vincent H. Dang, and publish one combined weekly bulletin. The 11 October 2026 issue has a
single page-1 masthead naming both parishes with their addresses, a joint "ST. LEO the GREAT
and ST. ANDREW MASS SCHEDULE" (Saturday 4:00 p.m. St. Leo, 5:30 p.m. St. Andrew; Sunday 8:30
a.m. St. Leo, 11:00 a.m. St. Andrew; weekdays Monday, Tuesday, Thursday, Friday 8:00 a.m. at
St. Leo), and announcements for both. Both parishes post the same issue on their own sites
(St. Leo's file is called "Combined bulletin"); the two PDFs differ as files but have the
same masthead, date and contents, so this is one bulletin and one row. The diocese's finder
lists them as two canonical parishes, recorded in `group`.

## Worship sites

Two: St. Leo the Great Church, 33 Manhattan Street, Ashley (`st-leo-ashley`), and St.
Patrick Church, 316 Parrish Street, Wilkes-Barre (`st-patrick-wilkes-barre`), the worship
site of St. Andrew Parish, which the bulletin calls "St. Andrew". The masthead says St. Leo
the Great is "A Community of Faith Formed by the Union of Holy Family, Holy Rosary and St.
Leo Parishes". Holy Family, Sugar Notch closed on 19 September 2021
(`excluded/holy-family-sugar-notch.md`). Holy Rosary, Ashley is in neither GCatholic nor the
finder, so no record was made for it.

## Website and bulletin provider

`other`. The website is St. Andrew's (standrewwilkesbarre.org), because its bulletin page
answers plain fetches and links every issue as a PDF; St. Leo's site
(stleos-holyrosary.org) carries the same issue but blocks non-browser clients. Both pages
are recorded as `url:` publications so that no second row can claim either. No recipe has
been pinned: `fetch:check` reads `data/parishes.csv`, which this row is not in yet; the
bulletin page is https://www.standrewwilkesbarre.org/bulletin0283fa5e (page-pdfs; newest
link is the current issue, file names carry the date in words).

## Not yet confirmed

Nothing.
