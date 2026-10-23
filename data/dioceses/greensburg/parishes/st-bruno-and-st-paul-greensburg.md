---
name: Partnered Parishes of St. Bruno and St. Paul, Greensburg
website: https://www.pbcatholic.org
bulletin_provider: parishes_online
provider_id: st-paul-and-st-bruno-parishes
publication: ['po-container:14/1234', 'po-org:st-paul-and-st-bruno-parishes', 'lpi:0018000000QxBzmAAF',
  'po-org:st-paul-church-15601', 'lpi:0018000000QxBzqAAF', 'url:https://www.pbcatholic.org/bulletin/read-our-weekly-bulletins/']
group: 'Partners: St. Bruno + St. Paul, Greensburg'
evidence:
- url: https://container.parishesonline.com/bulletins/14/1234/20261025B.pdf
  seen: 2026-10-22
  quote: St. Paul and St. Bruno Parishes - South Greensburg, PA 14-1234
  note: 'LPi footer on page 8 (the only page with a text layer) of the 25 Oct 2026 issue. Pages 1-7 are
    a Canva image; page 1 rendered and read: masthead "PARTNERED PARISHES OF ST. BRUNO AND ST. PAUL",
    "1729 Poplar St. Greensburg, PA 15601" and "820 Carbon Rd. Greensburg, PA 15601", "Website: pbcatholic.org",
    "OCTOBER 25, 2026 - THIRTIETH SUNDAY IN ORDINARY TIME", pastor Rev. Andrew J. Hamilton.'
- url: https://container.parishesonline.com/bulletins/14/1234/20261025B.pdf
  seen: 2026-10-22
  note: 'Page 1 (image, rendered): "St. Bruno Mass Schedule: Tuesday 8:00 AM Mass; Thursday 7:00 PM Mass;
    1st Saturdays 9:00 AM Mass; Saturday Vigil 5:00 PM Mass; Sunday 11:00 AM Mass" and "St. Paul Mass
    Schedule: Monday, Wednesday, and Friday 8:00 AM Mass; Saturday Vigil 4:30 PM Mass; Sunday 9:00 AM
    Mass". No other worship site.'
- url: https://parishesonline.com/organization/st-paul-and-st-bruno-parishes
  seen: 2026-10-22
  note: 'probe po: two LPi organizations publish into container 14/1234: st-paul-and-st-bruno-parishes
    (title "St. Bruno Parish", 1715 Poplar St, South Greensburg, lpi:0018000000QxBzmAAF) and st-paul-church-15601
    ("St. Paul Church", 820 Carbon Rd, lpi:0018000000QxBzqAAF). Both list weekly issues 2026-09-20 through
    2026-10-25.'
- url: https://www.pbcatholic.org/bulletin/read-our-weekly-bulletins/
  seen: 2026-10-22
  quote: Read our Weekly Bulletin - St. Paul and St. Bruno, Greensburg
  note: The partners' shared site also self-hosts the same Canva bulletin (WordPress uploads; latest linked
    on 2026-10-22 is October-11-2026-final-1.pdf, page 1 the same masthead and Mass schedules). It lags
    the ParishesOnline container by a week or more, so the container is the channel.
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=003
  seen: 2026-10-22
  note: 'Directory: St. Bruno Parish, pastor Father Andrew J. Hamilton, "Saturday: 5:00 p.m.; Sunday:
    11:00 a.m.", Partner Parishes "St. Paul Parish, Greensburg (007)", website pbcatholic.org, mailing
    address c/o 820 Carbon Road. LocationID=007 (St. Paul): same pastor, "Saturday: 4:30 p.m.; Sunday:
    9:00 a.m.", partner St. Bruno, website pbcatholic.org.'
promoted: 2026-10-23
---

## Publisher

St. Bruno Parish (directory 003) and St. Paul Parish (directory 007) are two canonical parishes in a diocesan "partnership" with one pastor (Fr. Andrew J. Hamilton), one office and one website, pbcatholic.org. They publish one weekly bulletin, "Partnered Parishes of St. Bruno and St. Paul", on ParishesOnline container 14/1234. The 25 October 2026 issue (read 2026-10-22; pages 1-7 are a Canva image, so page 1 was rendered and read) carries both parishes' addresses in the masthead and a separate Mass schedule for each church. Two LPi organizations (one per parish) point at that same container, so both slugs are recorded as publication ids of this one row.

## Worship sites

St. Bruno church (1715 Poplar Street, in South Greensburg borough) and St. Paul church (820 Carbon Road, Hempfield Township): the only two places in the bulletin's Mass schedules. The diocesan directory and GCatholic list no other site for either parish.

## Website and bulletin provider

`website` is the partners' shared WordPress site (diocese template), which links the same bulletin as uploaded PDFs, but a week or more behind (on 2026-10-22 its newest was the 11 Oct issue, while the container already had 25 Oct). Provider `parishes_online`, org slug `st-paul-and-st-bruno-parishes` (the one whose slug names both parishes); `fetch:check` 2026-10-22 picked the 25 Oct 2026 issue from container 14/1234.

## Not yet confirmed

The bulletin's text pages are images; the pipeline needs to read them by image. The masthead gives St. Bruno's address as 1729 Poplar St. while the directory, GCatholic and LPi say 1715 (see the church record).
