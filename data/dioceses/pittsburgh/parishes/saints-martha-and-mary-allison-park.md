---
name: Saints Martha and Mary Parish
website: https://www.smmpgh.org
bulletin_provider: parishes_online
provider_id: saints-martha-and-mary-parish
publication: ['po-org:saints-martha-and-mary-parish', 'lpi:0018000000Qx7rwAAB', 'po-container:14/1169',
  'ecatholic:21597']
group: Saints Martha and Mary Parish
evidence:
- url: https://container.parishesonline.com/bulletins/14/1169/20261025B.pdf
  seen: 2026-10-23
  quote: St. Catherines/St. Richards
  note: 'Page 20 (ad page, the only text-layer line naming the churches) of the 25 October 2026 issue,
    container 14/1169, 20 pages, 83,738,163 bytes, image-only apart from pages 17-20. Rendered page 1
    (pdftoppm, 70 dpi): cover masthead ''SAINT[S] MARTHA & MARY PARISH'' over ''St. Catherine of Sweden,
    2554 Wildwood Road, Allison Park, PA 15101, 412-486-6001'' and ''St. Richard, 3841 Dickey Road, Gibsonia,
    PA 15044, 724-444-1971''. Ad-page footers read ''Saints Martha and Mary Parish, Wildwood, PA  14-1169''.'
- url: https://container.parishesonline.com/bulletins/14/1169/20261025B.pdf
  seen: 2026-10-23
  note: 'Page 2 (image, rendered and read by eye): WEEKEND MASS SCHEDULE Saturday vigil 4:00 pm St. Catherine
    of Sweden, 5:00 pm St. Richard; Sunday 7:30 am St. Richard, 9:15 am St. Catherine of Sweden, 10:00
    am St. Richard, 11:30 am St. Catherine of Sweden. WEEKDAY: Mon/Wed/Fri 9:00 am St. Catherine of Sweden;
    Tue/Thu 9:00 am St. Richard. Photos of the two churches under ''SAINTS MARTHA & MARY PARISH''. Only
    these two churches.'
- url: https://www.smmpgh.org/masstimes
  seen: 2026-10-23
  quote: 9:00 AM St. Richard
  note: 'Parish Mass Times page (diocese-provided eCatholic site 21597, read in headed Chrome): same weekend
    and weekday times at St. Catherine and St. Richard; adds ''St. Barnabas Retirement Village - 1st Friday
    of the Month'' 9:30 AM, and All Saints and All Souls Masses at the two churches.'
- url: https://www.smmpgh.org/bulletin
  seen: 2026-10-23
  note: The parish's /bulletin page links parishesonline.com/organization/saints-martha-and-mary-parish
    and the container 14/1169 issues of 20261025, 20261018, 20261011 and 20261004; it hosts no PDF of
    its own (visit.py --links). Its Bulletin page lists the St. Catherine of Sweden and St. Richard addresses.
- url: https://parishesonline.com/organization/saints-martha-and-mary-parish
  seen: 2026-10-23
  note: 'probe po: org ''Saints Martha & Mary Parish'', 2554 Wildwood Rd, Allison Park; container 14/1169;
    latest issue 2026-10-25; website smmpgh.org.'
- url: https://diopitt.org/saints-martha-and-mary-parish
  seen: 2026-10-23
  note: 'Diocese parish page (directory roster): two churches, Saint Catherine of Sweden (Hampton) and
    Saint Richard (Richland); pastor Rev. Robert J. Vular. The predecessor list maps St. Catherine of
    Sweden (Hampton Twp.) and St. Richard (Richland Twp.) to Sts. Martha and Mary.'
promoted: 2026-10-23
bulletin_status: available
---

## Publisher

Saints Martha and Mary Parish (Hampton and Richland townships; pastor Rev. Robert J. Vular per the diocese page) publishes one weekly bulletin for its two churches through ParishesOnline, container 14/1169. The 25 October 2026 issue's cover names the parish over the two churches' addresses, page 2 gives one combined Mass schedule for both, and the ad-page footers read 'Saints Martha and Mary Parish, Wildwood, PA 14-1169'.

## Worship sites

Two churches: Saint Catherine of Sweden (2554 Wildwood Road, Allison Park, in Hampton Township) and Saint Richard (3841 Dickey Road, Gibsonia, in Richland Township). Both have weekend and weekday Mass in the bulletin and on the parish Mass Times page. The diocese directory and Mass Finder list the same two; the predecessor list shows no other predecessor church. A First Friday 9:30 AM Mass at St. Barnabas Retirement Village appears on the parish Mass Times page and in the Mass-intention list; nothing says it is open to the public, and it is not in the bulletin's Mass schedule, so it is not a church row (see Not yet confirmed).

## Website and bulletin provider

smmpgh.org is diocese-provided eCatholic (site 21597) behind Cloudflare (`probe url` gets 403; headed Chrome reads it). Its bulletin page only links the ParishesOnline container 14/1169. The bulletin is image-only apart from the last four pages and about 84 MB (the 4, 11, 18 and 25 October issues all have 20 pages and 4 readable ones), so the pipeline will have to read it as an image. `render.py` crashed on the 84 MB file; `pdftoppm -r 70 -f 1 -l 3 -png` renders it.

## Not yet confirmed

Whether the First Friday Mass at St. Barnabas Retirement Village (a retirement community, address not found) is open to the public. Next step: ask the office (412-486-6001) or find a source saying who may attend. Not modelled meanwhile.
