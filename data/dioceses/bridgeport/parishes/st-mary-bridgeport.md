---
name: St. Mary
website: https://stmarychurchbridgeport.org/boletin-bulletin/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://stmarychurchbridgeport.org/boletin-bulletin/#st-mary-bridgeport']
group: ''
evidence:
- url: https://stmarychurchbridgeport.org/wp-content/uploads/2026/11/11.08.2026-32th-Sunday-in-Ordinary-Time.pdf
  seen: 2026-11-12
  quote: venir a almorzar con el P. Rolando
  note: 'The 8 November 2026 issue is one page with no masthead (rendered with parish-site-access render.py;
    titled ''32 Domingo del Tiempo Ordinario, November 08, 2026''). Mass intentions: Monday, Thursday,
    Friday 6:30pm, Saturday 4:00pm, Sunday 8:30, 10:00, 11:30am; offertory by Mass 4:00pm, 8:30am, 10:00am,
    11:30am; a procession at St. Margaret Shrine after the Saturday 4:00pm Mass. These are St. Mary''s
    times in the diocese''s mass-times API; Fr. Rolando Torres is St. Mary''s pastor in the directory.'
- url: https://stmarychurchbridgeport.org/boletin-bulletin/
  seen: 2026-11-12
  quote: 25 Sherman St, Bridgeport, CT 06608
  note: Header of the parish's Boletín/Bulletin page (WordPress), which links weekly PDFs under /wp-content/uploads/<yyyy>/<mm>/<mm.dd.yyyy>-<title>.pdf
    from 2021 to 11.08.2026; the page is not in date order (June 2026 issues are listed first).
promoted: 2026-11-12
bulletin_status: available
publication_reviews:
- parish: sts-cyril-methodius-bridgeport
  decision: separate
  evidence:
  - url: https://stmarychurchbridgeport.org/wp-content/uploads/2026/11/11.08.2026-32th-Sunday-in-Ordinary-Time.pdf
    seen: 2026-11-12
    note: 'The 8 November 2026 St. Mary sheet is the bulletin for St. Mary: Fr. Rolando, Saturday 4:00pm
      and Sunday 8:30, 10:00, 11:30am Masses; it does not mention Sts. Cyril & Methodius.'
  - url: https://institute-christ-king.org/images/b11.8.2026_Resumed_Epiphany_V.pdf
    seen: 2026-11-12
    note: The 8 November 2026 masthead names the Church of Saints Cyril & Methodius alone, with Canon
      Altiere as rector and its own Latin Mass times.
---

## Publisher

St. Mary, Bridgeport posts its own weekly bulletin, a single bilingual page, on its WordPress site. The 8 November 2026 issue (`https://stmarychurchbridgeport.org/wp-content/uploads/2026/11/11.08.2026-32th-Sunday-in-Ordinary-Time.pdf`, read 2026-11-12; partly text, rendered to read the layout) has no masthead, only the title "32 Domingo del Tiempo Ordinario, November 08, 2026". It is identified as St. Mary's by where it is posted, by "P. Rolando" (Fr. Rolando Torres, St. Mary's pastor in the directory), and by its Mass times (Saturday 4:00pm, Sunday 8:30, 10:00, 11:30am, weekdays 6:30pm), which are St. Mary's in the diocese's mass-times API.

## Worship sites

- `st-mary-bridgeport`: the church at 25 Sherman Street (site header, GCatholic 22000), with directory:1331 linked.

The diocese's directory gives St. Mary at 79 Church Street, the address of Sts. Cyril & Methodius (ICKSP). That is not a shared church or bulletin: St. Mary has its own pastor, site and bulletin with different Mass times, and the 8 November issues of the two bulletins don't mention each other (see `publication_reviews`). The directory's address is taken to be an error.

## Website and bulletin provider

Provider `other`, read from the Boletín/Bulletin page (`https://stmarychurchbridgeport.org/boletin-bulletin/`). It links every issue since 2021 by file name `mm.dd.yyyy-<title>.pdf`, but not newest first (June 2026 issues are at the top), so the pick has to come from the dates in the file names.

`fetch:check` on 2026-11-12 printed recipe `page-pdfs` and picked `https://stmarychurchbridgeport.org/wp-content/uploads/2026/11/11.08.2026-32th-Sunday-in-Ordinary-Time.pdf`, the 8 November 2026 issue and the newest posted (age 4 days; identity unverified as reported, content checked by hand above). The recipe is recorded in `provider_id`.

## Not yet confirmed

Nothing open.
