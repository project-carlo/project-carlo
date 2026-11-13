---
name: St. Margaret (Middle Village)
website: https://stmargaretmv.com/
bulletin_provider: parishes_online
provider_id: st-margaret-church-11379
publication: ['po-org:st-margaret-church-11379', 'lpi:0018000000QxB9lAAF', 'po-container:03/1438']
group: Deanery Q6 (Queens West)
evidence:
- url: https://container.parishesonline.com/bulletins/03/1438/20261108B.pdf
  seen: 2026-11-06
  note: 'Page 1 (an image with no text layer, rendered with parish-site-access render.py) of the 8 November
    2026 bulletin: masthead ''St. Margaret Roman Catholic Church'', November 8, 2026; Pastor Rev. Peter
    Okajima; parish office 66-05 79th Place, Middle Village, NY 11379; website www.stmargaretmv.com.'
- url: https://container.parishesonline.com/bulletins/03/1438/20261108B.pdf
  seen: 2026-11-06
  note: 'Page 2 (image, rendered) MASS TIMES: Monday - Friday 7:00 am, 9:00 am; Saturday 9:00 am, 5:00
    pm; Sunday 8:00 am, 10:00 am (Bilingual Italian/English), 12:00 pm, 5:00 pm. No other church or chapel
    is named.'
- url: https://parishesonline.com/organization/st-margaret-church-11379
  seen: 2026-11-06
  note: 'probe po: org ''St. Margaret Church'', 66-05 79th Place, Queens, New York 11379, website https://stmargaretmv.com/,
    lpi 0018000000QxB9lAAF, container 03/1438, weekly issues through 2026-11-08.'
- url: https://stmargaretmv.com/
  seen: 2026-11-06
  note: probe url answers HTTP 403 (bot blocking); a parish-site-access visit.py load did not finish.
    The site was not read; the bulletin was read from ParishesOnline.
promoted: 2026-11-12
bulletin_status: available
---

## Publisher

St. Margaret publishes its own weekly bulletin through LPi (ParishesOnline org `st-margaret-church-11379`, container 03/1438). Page 1 of the 8 November 2026 issue (`https://container.parishesonline.com/bulletins/03/1438/20261108B.pdf`, read 2026-11-06) is an image; rendered, its masthead reads "St. Margaret Roman Catholic Church / November 8, 2026", with Rev. Peter Okajima as Pastor and the parish office at 66-05 79th Place, Middle Village.

## Worship sites

One church. The page 2 MASS TIMES (Monday - Friday 7:00 and 9:00 am; Saturday 9:00 am and 5:00 pm; Sunday 8:00 am, 10:00 am bilingual Italian/English, 12:00 pm, 5:00 pm) name no other place. The diocese directory, the deanery directory (Q6), GCatholic 16739 and Mass finder place 1150 all list the one church at 66-05 79th Place. St. John Cemetery's chapel, also in Middle Village, is not in this bulletin; it has its own `excluded/` record.

## Website and bulletin provider

`parishes_online`, read by org slug. The website is the parish's own site, which the masthead and the ParishesOnline org both name; it answers 403 to `probe url` and was not read. The bulletin's front pages are images with no text layer (pages 1-3 of the 8 November and 1 November issues), so the pipeline has to read the masthead and schedule as images.

## Not yet confirmed

Whether the parish site links the ParishesOnline bulletin or reposts it was not checked (the site blocked the probe); it doesn't affect the row, which fetch reads by org slug.
