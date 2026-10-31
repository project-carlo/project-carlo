---
name: St. Vincent de Paul
website: https://www.saint-vincent-church.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://us16.campaign-archive.com/home/?u=3e023a9d5646bd96aafe4420f&id=ac149a954f
  seen: 2026-10-29
  note: 'Mailchimp archive ''St. Vincent De Paul Parish, Email Campaign Archive'', linked from the parish
    home page: weekly issues titled "St. Vincent''s October 28 eBulletin", back to June 2026. These are
    HTML emails, not PDFs.'
- url: https://us16.campaign-archive.com/?u=3e023a9d5646bd96aafe4420f&id=c6db53eeca
  seen: 2026-10-29
  quote: St. Vincent de Paul/Germantown Weekly eBulletin
  note: 'The 28 October 2026 eBulletin (HTML, 265 kB): ''ST. VINCENT de PAUL / GERMANTOWN, 109 E. PRICE
    ST. 19144 215-438-2925, Pastor: Fr. Sy Peterka, CM''; ''MASS AT ST. VINCENT''S: Saturday 4 PM, Sunday
    9 AM, 10:30 AM (also live-streamed on YouTube), Daily Masses Monday-Saturday 7:00 AM (in chapel)''.
    It names this one church only. The page''s links include no PDF.'
- url: https://www.saint-vincent-church.org/
  seen: 2026-10-29
  note: 'probe url: 200, title ''St.Vincent de Paul Church, Germantown'', no publication ids; the only
    PDFs linked are a choir-director job description (2026/07) and a 2025 Gospel-sharing flyer. Home page
    Mass Schedule: Saturday Vigil 4pm, Sunday 9am and 10:30am, Daily Mass 7am Monday-Saturday, adoration
    after the first-Saturday Mass in the rectory chapel.'
- url: https://parishesonline.com/organization/st-vincent-de-paul-19144
  seen: 2026-10-29
  note: 'probe po st-vincent-de-paul-19144: LPi 0018000000QxAd0AAF, 109 E Price St, website saint-vincent-church.org,
    ''no publications: this organization does not publish a bulletin here now''.'
- url: https://archphila.org/parish/st-vincent-de-paul-philadelphia/
  seen: 2026-10-28
  note: 'Directory page (updated 4 months before): ''Corner of Price and Lena Sts.'', rectory 109 E. Price
    St. 19144, Rev. William J. Chiriaco (Parochial Administrator); ''Merged with St. Francis of Assisi
    and Immaculate Conception: 2012''; no deanery. The eBulletin names Fr. Sy Peterka, CM as pastor, so
    the directory''s pastor line is out of date.'
revisit: Check whether the parish posts a PDF bulletin or a reader for Mailchimp eBulletins exists
revisit_after: 2027-01-31
research:
- method: 'Looked for a PDF bulletin: probe url and home-page links on saint-vincent-church.org; the Mailchimp
    eBulletin archive and its latest issue; probe po on the ParishesOnline organization; John Patrick
    listings 100 (St. Francis of Assisi, 19144) and 185 (Immaculate Conception, 19138), the merged parishes''
    own listings, which carry readings only'
  url: https://us16.campaign-archive.com/home/?u=3e023a9d5646bd96aafe4420f&id=ac149a954f
  checked: '2026-10-29'
  outcome: unsupported-format
  next_action: Read the weekly eBulletin as the bulletin if the pipeline gains an HTML-email reader, or
    find a PDF bulletin if the parish starts posting one (website or John Patrick listing)
  retry_when: The pipeline can read Mailchimp campaign pages, or the parish posts a PDF
bulletin_status: unsupported-format
---

## Publisher

St. Vincent de Paul, Germantown (the 2012 merger of St. Vincent de Paul, St. Francis of Assisi and Immaculate Conception) has no PDF bulletin that was found. Its home page links no bulletin; the only Mass publication is a weekly 'eBulletin', an HTML email archived on Mailchimp (28 October 2026 issue read, giving Mass times and the pastor). Its ParishesOnline organization is empty, and the John Patrick listings of the two merged parishes (100 and 185) carry readings only. An HTML email cannot be read by `page-pdfs` or `dated-post`, so the row is `no_bulletin` with `bulletin_status: unsupported-format`, following the Holy Redeemer precedent in this diocese, and it stays off the site until a readable bulletin exists.

## Worship sites

One church, St. Vincent de Paul (109 E. Price St., at Lena St.). The eBulletin's Mass box and the home page list Masses there only (Saturday 4 PM, Sunday 9 and 10:30 AM, weekdays 7 AM, the weekday Mass 'in chapel' in the attached rectory). The directory says the parish merged with St. Francis of Assisi and Immaculate Conception in 2012; neither is listed in the Mass box, and neither is in this batch's rosters.

## Website and bulletin provider

`no_bulletin`: see Publisher and `research`.

## Not yet confirmed

Whether a PDF version of the weekly bulletin exists (the eBulletin may be the only edition). Whether the merged St. Francis of Assisi (Germantown) and Immaculate Conception churches still hold Mass: neither appears in any current St. Vincent's schedule I read; they are in no roster of this batch, so I recorded no decision on them.
