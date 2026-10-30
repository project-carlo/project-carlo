---
name: St. Mary, Star of the Sea
website: https://saintmarysa.org
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/537
publication: ['url:https://www.church-bulletin.org/saint-mary-star-of-the-sea-church-south-amboy-nj-08879']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-mary-star-of-the-sea-church-south-amboy-nj-08879/2026-10-25.pdf
  seen: 2026-10-30
  quote: Rev. Guy W. Selvester, M.Div., M.A., PASTOR
  note: 'Page 1 of the 25 October 2026 issue (8 pages): masthead ''Saint Mary, Star of the Sea'' parish
    information with Masses Saturday 4:00 PM, Sunday 9:00 AM and 11:00 AM, weekdays Tuesday through Friday
    8:00 AM, Monday 7:00 PM (Mass Association); parish website www.saintmarysa.org; rectory phone 732-721-0179.
    Names no other church.'
- url: https://saintmarysa.org/bulletin
  seen: 2026-10-30
  quote: Current Bulletin
  note: 'Read with the browser (visit.py --links): the parish''s Bulletin page links https://www.jppc.net/onlinebulletins/537template.pdf
    under ''Current Bulletin''. John Patrick Publishing id 537; church-bulletin.org/?id=537 redirects
    to the listing for ''Saint Mary, Star of the Sea Church, South Amboy, NJ 08879'', newest issue 2026-11-01.'
bulletin_status: available
---

## Publisher

St. Mary, Star of the Sea (256 Augusta Street, South Amboy) publishes its own weekly bulletin through John Patrick Publishing (id 537), linked as 'Current Bulletin' from its eCatholic website's Bulletin page. The 25 October 2026 issue (8 pages, text layer) names Rev. Guy W. Selvester as Pastor and gives one Mass schedule: Saturday 4:00 PM; Sunday 9:00 AM and 11:00 AM; Tuesday to Friday 8:00 AM; Monday 7:00 PM (Mass Association). Pages 2 to 4 are the parish's own Mass intentions and pastor's column.

**The finder's clergy line is stale.** It names Rev. Dennis R. Weezorak as pastor (with Rev. Glenn J. Comandini in residence); the 2026 bulletin names Rev. Guy W. Selvester, whom its pastor's column and masthead present as the current pastor, and the column says the Most Rev. Michael A. Saporito 'officially became the sixth Bishop of Metuchen' on the preceding Thursday. I did not look for when the pastor changed.

**Not shared with Sacred Heart.** A grep of this issue for 'Sacred Heart', 'Gromadzki', 'Matawan' and 'Redeemer' found nothing, and Sacred Heart's own bulletin has a different pastor and publisher (see `sacred-heart-south-amboy`). The two South Amboy parishes are separate rows.

## Worship sites

One church, 256 Augusta Street (`st-mary-star-of-the-sea-south-amboy`; directory:24542, gcatholic:18679). The bulletin names 'St. Pat's Hall' and St. Mary's Elementary School for events, not for Mass.

## Website and bulletin provider

The finder and GCatholic give http://saintmarysa.org, now https://saintmarysa.org, an eCatholic site (id 34325, probe url). Site id 34325 identifies the website, not the bulletin, which the site does not host: its Bulletin page has only the John Patrick link. Provider `other`, recipe `page-pdfs https://church-bulletin.org/537` (see the diocese's John Patrick lesson). The publication id is the listing URL, as for the Bound Brook rows.

## Fetch check

`pnpm fetch:check` on 2026-10-30 resolved `page-pdfs` on https://church-bulletin.org/537 and picked `bulletin/saint-mary-star-of-the-sea-church-south-amboy-nj-08879/2026-11-01.pdf` (6 pages, 3.3 MB): transport ok, PDF, issue date 2026-11-01 inferred from the file name, freshness `future` (John Patrick posts the coming Sunday two days early). Publication identity was not machine-checked; a grep of that issue finds 'Selvester' twice and I read the 25 October masthead myself. Recipe recorded: `page-pdfs https://church-bulletin.org/537`.

## Not yet confirmed

Nothing open. The only gap is the freshness status `future`, which is the publisher posting the next Sunday's issue early.
