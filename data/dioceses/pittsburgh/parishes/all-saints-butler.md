---
name: All Saints Parish (Butler)
website: https://allsaintsbutler.org
bulletin_provider: parishes_online
provider_id: all-saints-parish-st-andrew-st-conrad-st-michael-the-archangel-st-paul-st-peter-
publication: ['po-org:all-saints-parish-st-andrew-st-conrad-st-michael-the-archangel-st-paul-st-peter-',
  'lpi:0018000000Qc1JyAAJ', 'po-container:14/1322']
group: All Saints Parish
evidence:
- url: https://container.parishesonline.com/bulletins/14/1322/20261025B.pdf
  seen: 2026-10-23
  quote: All Saints Parish, Butler, PA 14-1322
  note: 25 October 2026 issue, container 14/1322, 16 pages; pages 1-13 are images with no text layer,
    the quote is the LPi ad-page footer (page 14). Rendered with render.py, page 1 reads 'All Saints Parish
    / www.allsaintsbutler.org / 30th Sunday of Ordinary Time | Oct. 25, 2026 / Rev. Kevin C. Fazio, Pastor'
    with the MASS SCHEDULE box naming all five churches by street address. recheck cannot find the image
    text.
- url: https://container.parishesonline.com/bulletins/14/1322/20261025B.pdf
  seen: 2026-10-23
  note: 'Page 1 Mass schedule (rendered image). Weekend, Saturday: 8am St. Paul (128 N. McKean St.); Vigil
    4pm St. Michael (432 Center Ave.); 5:30pm St. Conrad (125 Buttercup Rd.). Sunday: 8am St. Peter (127
    Franklin St.); 8:30am St. Conrad; 10am St. Paul; 11am St. Andrew (1660 N. Main St. Ext.); 11:30am
    St. Conrad; 6pm St. Paul. Weekday: Mon 8am St. Paul; Tue 8am St. Paul and 12:05pm St. Michael; Wed
    8am St. Paul and 12:05pm St. Conrad; Thu 8am St. Paul and 12:05pm St. Andrew; Fri 8am St. Paul and
    12:05pm St. Peter. Matches the diocese directory''s weekend times for each church. Page 2 (''About
    our parish'') lists one clergy and staff team under one office phone 724-287-1759.'
- url: https://parishesonline.com/organization/all-saints-parish-st-andrew-st-conrad-st-michael-the-archangel-st-paul-st-peter-
  seen: 2026-10-23
  note: 'probe po: ''All Saints Parish - Sts. Andrew, Conrad, Michael, Paul, Peter Churches'', 128 N.
    McKean St., Butler; lpi 0018000000Qc1JyAAJ; container 14/1322; issues 2026-10-11, 10-18 and 10-25
    (probe container 14/1322 found 20261025B.pdf). The only Butler-area ParishesOnline org that names
    All Saints.'
- url: https://allsaintsbutler.org/
  seen: 2026-10-23
  note: Rendered in headed Chrome (visit.py --bulletin). verdict ok; publications po-org:all-saints-parish-st-andrew-...
    and ecatholic:22444. Home page lists the five churches (St. Conrad, St. Paul, St. Michael the Archangel,
    St. Andrew, St. Peter) and a Bulletins tile 'Current & Past Publications'. issues.py ecatholic 22444
    found no Sunday-dated eCatholic bulletin in 12 weeks (all 403), so the eCatholic site hosts no bulletin
    files of its own.
- url: https://diopitt.org/saint-fidelis-of-sigmaringen
  seen: 2026-10-23
  quote: This ended on July 1, 2021 when St. Fidelis of Sigmaringen Parish merged with St. Andrew Parish,
    Center Township and the Butler parishes of St. Peter, St. Paul and St. Michael the Archangel to form
    the new All Saints Parish.
  note: Diocese history page (headed Chrome). Says the predecessor parishes were already 'publishing a
    joint bulletin' before the merger.
promoted: 2026-10-23
bulletin_status: available
---

## Publisher

All Saints Parish (Butler, Center Township and Meridian), formed 2021-07-01 from St. Andrew (Center Twp.), St. Fidelis of Sigmaringen (Lyndora/Meridian), St. Michael the Archangel, St. Paul and St. Peter (Butler), publishes one weekly bulletin on ParishesOnline container 14/1322. The 25 October 2026 issue (read 2026-10-23) has its cover, page 1, as an image: rendered, it reads "All Saints Parish ... 30th Sunday of Ordinary Time | Oct. 25, 2026 ... Rev. Kevin C. Fazio, Pastor" and prints one Mass schedule box for all five churches (see the evidence). The text-layer footer on the ad pages reads "All Saints Parish, Butler, PA 14-1322". The diocese directory gives the same pastor (Rev. Kevin C. Fazio) for all five churches and one phone, 724-287-1759. No other bulletin channel for any of the five exists: eCatholic site 22444 hosts no bulletin files, and no other ParishesOnline org names any of them.

## Worship sites

Five churches, each named with its street address in the 25 October Mass schedule and each holding weekend or weekday Mass: St. Andrew (Center Twp.), St. Conrad (Meridian; the diocese history page calls it St. Fidelis of Sigmaringen Church, the former St. Conrad Church), St. Michael the Archangel, St. Paul, St. Peter. St. Paul has Masses every weekday morning, plus Saturday 8am, Sunday 10am and 6pm. The diocese directory and Mass Finder list the same five. Ruled out: St. Stanislaus Kostka, Lyndora (GCatholic 24290, Former Church), closed 2020-07-01, see excluded/st-stanislaus-kostka-lyndora.md. GCatholic's St. John the Baptist and St. Michael, Lyndora (nearby entries) belong to no roster entry of this batch; the diocese history page says St. John closed at the 1995 merger and was sold.

## Website and bulletin provider

allsaintsbutler.org is diocese-provided eCatholic (site 22444) behind Cloudflare; read with headed Chrome. The site's Bulletin tile leads to the ParishesOnline widget, so fetch reads the container. **The bulletin's pages are images** (pages 1-13 of 16 have no text layer in the 25 Oct issue), so the pipeline will need to read the Mass schedule from the rendered page.

## Not yet confirmed

Nothing outstanding for the row. The 25 October issue was read two days ahead of its date; the previous issues (10-11, 10-18) exist in the same container.
