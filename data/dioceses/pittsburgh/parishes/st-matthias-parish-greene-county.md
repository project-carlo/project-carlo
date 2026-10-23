---
name: St. Matthias Parish (Greene County)
website: https://www.stmatthiasgreene.org
bulletin_provider: ecatholic
provider_id: '23303'
publication: ['ecatholic:23303']
group: ''
evidence:
- url: https://files.ecatholic.com/23303/bulletins/20261025.pdf
  seen: 2026-10-23
  quote: St. Matthias Parish
  note: 'Page 1 (cover) of the 25 October 2026 issue (10 pages, text layer): masthead ''St. Matthias Parish'',
    ''PASTOR: Rev. Thomas Lewandowski'', ''COUNTY WEBSITE ACCESS: www.stmatthiasgreene.org'', office hours
    at the St. Ann Office, Waynesburg and the St. Hugh Office, Carmichaels, and a CHURCHES panel listing
    St. Ann, St. Hugh, St. Marcellus and St. Ignatius with addresses. The same single issue covers all
    four churches.'
- url: https://files.ecatholic.com/23303/bulletins/20261025.pdf
  seen: 2026-10-23
  quote: are available at all four St. Matthias Churches
  note: 'Page 2. Page 3 (an image, rendered) is the MASS SCHEDULE for 24 Oct to 1 Nov 2026: Sat 4:00 pm
    St. Ann and 6:00 pm St. Hugh; Sun 8:30 St. Ann, 9:30 St. Hugh, 10:30 St. Marcellus, 11:30 St. Ignatius;
    Mon 9:00 St. Hugh; Tue 9:00 St. Marcellus; Wed 9:00 St. Hugh and 6:30 pm St. Ann; Thu 9:00 St. Ignatius;
    Fri 9:00 St. Hugh. No other church or campus appears.'
- url: https://www.stmatthiasgreene.org/bulletins
  seen: 2026-10-23
  note: Rendered in headed Chrome (visit.py --links; probe url alone answers 403). Site title 'St. Matthias
    | Greene County, PA', publication ecatholic:23303. The /bulletins page links 60 weekly files.ecatholic.com/23303/bulletins/<yyyymmdd>.pdf
    from 2025-09-07 to 2026-10-25, one per Sunday. issues.py ecatholic ecatholic:23303 returns 20261025.pdf
    as the latest. I downloaded all 60 and grepped them for Nemacolin, Clarksville, Rices Landing, Consolation,
    Crucible, Sacred Heart and Waynesburg University (see the church and excluded records).
- url: https://www.stmatthiasgreene.org/st-matthias-parish
  seen: 2026-10-23
  quote: The other four churches, Saint Ann, Waynesburg; Saint Hugh, Carmichaels; St. Ignaitus of Antioch,
    Bobtown, and Saint Marcellus, Jefferson remain open.
  note: Parish history page (headed Chrome). St. Matthias Parish established 1 July 2019 from Our Lady
    of Consolation (Nemacolin), St. Ann, St. Hugh, St. Ignatius of Antioch and St. Thomas (Clarksville);
    'the five parishes included eight church buildings' and four closed in July 2019 (excluded records).
- url: https://diopitt.org/saintmatthiasparish
  seen: 2026-10-23
  note: 'Diocese directory (roster directory:saintmatthiasparish/1-4): one parish, four churches, website
    www.stmatthiasgreene.org, Rev. Thomas J. Lewandowski (Pastor). Nothing links it to another parish''s
    bulletin.'
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese pittsburgh --parish st-matthias-parish-greene-county (headed Chrome)
  checked: '2026-10-23'
  outcome: found
  next_action: None; reread the masthead only if the parish merges or the pastor changes.
---

## Publisher

St. Matthias Parish, Greene County (Waynesburg, Carmichaels, Jefferson, Bobtown), publishes one weekly bulletin on its own eCatholic site 23303. The 25 October 2026 issue (https://files.ecatholic.com/23303/bulletins/20261025.pdf, read 2026-10-23, 10 pages) has the masthead 'St. Matthias Parish' on page 1, a CHURCHES panel for the four churches, and a page-3 Mass schedule image for all four. One row, one bulletin. The site publishes one issue per Sunday (60 files between 2025-09-07 and 2026-10-25 on the /bulletins page), so the issue read is the current one.

The diocese directory lists Rev. Thomas J. Lewandowski as pastor of this parish only (the only shared pastor in the diocese is Rev. Edward L. Yuhas, per diocese.md), and no other parish uses this website or bulletin, so no peer review is needed.

## Worship sites

Four churches, each with Mass in the 25 October 2026 schedule: St. Ann (Waynesburg), St. Hugh (Carmichaels), St. Ignatius of Antioch (Bobtown), St. Marcellus (Jefferson). Four more buildings of the predecessor parishes closed in 2019 and are in `excluded/`: Sacred Heart (Rices Landing), St. Mary (Crucible), St. Thomas (Clarksville), Our Lady of Consolation (Nemacolin). The parish also has a Waynesburg University student Mass question: the bulletin printed a Sunday 1:00 pm Mass at St. Ann for the university in early 2026 but the 6 September 2026 issue says there will be no Sunday afternoon or evening Mass and only a monthly University Student Mass is planned; see `open/`.

## Website and bulletin provider

https://www.stmatthiasgreene.org is the parish's eCatholic site (publication ecatholic:23303) and posts the bulletin PDFs itself; it answers 403 to probe url and needs headed Chrome. provider ecatholic, provider_id 23303.

## Not yet confirmed

Nothing about the row. The weekday times on the Mass Times page (M W F 9:00 am St. Hugh; a 'MON FRI 8:00 AM St. Ann' line; Wed 6:30 pm St. Ann) differ from the bulletin's current schedule (Mon 9:00 St. Hugh; Wed 9:00 St. Hugh and 6:30 St. Ann; Fri 9:00 St. Hugh; no 8:00 am St. Ann line); the bulletin is later and wins.
