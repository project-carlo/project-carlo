---
name: St. Joseph Parish of the Panther Valley
website: https://stjscatholicchurch.org/
bulletin_provider: other
provider_id: page-pdfs https://www.jppc.net/onlinebulletins/248template.pdf
publication: ['url:https://www.church-bulletin.org/saint-joseph-parish-of-the-panther-valley-summit-hill-pa-18250']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-joseph-parish-of-the-panther-valley-summit-hill-pa-18250/2026-10-18.pdf
  seen: 2026-10-18
  note: 'Page 1 of the 18 October 2026 issue (every page is a scanned image with no text layer; read rendered
    with parish-site-access render.py, so recheck cannot find a quote in it). Masthead "St. Joseph Parish
    of the Panther Valley"; "Church 462 W. Ludlow St. Summit Hill, PA 18250"; "Weekend Mass Schedule Saturday
    Evening: 4:00 PM Sunday: 8:00 & 10:15 AM"; "Daily Mass Schedule Mon., Wed., Thurs., Fri.: 8:00 AM
    Tuesday: 6:00 PM Sat.: 9:00 AM - Shrine of St. Therese"; lower panel "The Shrine of Saint Therese
    of Lisieux 1 E. Garibaldi Ave., Nesquehoning, PA 18240", "Rev. Thomas Osei Gyau - Rector". Page 3
    intentions: "Saturday, October 24 … Shrine -Daily Mass- 9am" and "St. Joseph - Vigil Mass - 4pm".'
- url: https://www.church-bulletin.org/saint-joseph-parish-of-the-panther-valley-summit-hill-pa-18250
  seen: 2026-10-18
  quote: Saint Joseph Parish of the Panther Valley Summit Hill, PA 18250 Latest Edition October 18, 2026
  note: John Patrick Publishing's listing (jppc.net/onlinebulletins/248template.pdf and church-bulletin.org/?id=248
    redirect here). One PDF per Sunday at /bulletin/saint-joseph-parish-of-the-panther-valley-summit-hill-pa-18250/YYYY-MM-DD.pdf,
    archive back to 2025.
- url: https://stjscatholicchurch.org/
  seen: 2026-10-18
  quote: Saturday Vigil 4:00 pm Sunday 8:00 am 10:15 am Weekdays Daily Mass Monday, Wednesday, Thursday
    & Friday – 8:00 am Tuesday- 6:00 pm Saturday 9:00 am Mass at the Shrine
  note: The parish's WordPress site; its "Bulletin" menu item links https://www.jppc.net/onlinebulletins/248template.pdf.
- url: https://stjscatholicchurch.org/diocesan-shrine-of-st-therese/
  seen: 2026-10-18
  quote: St. Francis Parish and St. Katherine Drexel Parish, formed by the consolidation of the three
    churches in both Lansford and Coaldale, then became part of St. Joseph Parish of the Panther Valley,
    Summit Hill, on July 1, 2016.
- url: https://www.tnonline.com/20160423/panther-valley-catholic-parishes-merging-our-lady-school-to-close/
  seen: 2026-10-18
  quote: the merger of St. Francis of Assisi Parish in Nesquehoning and St. Katharine Drexel parish in
    Lansford into St. Joseph's Roman Catholic Church in Summit Hill, effective later this year.
  note: Times News, 23 April 2016 (the URL carries the date; tnonline.com/?p=190107 redirects here).
promoted: 2026-10-19
---

## Publisher

St. Joseph Parish of the Panther Valley (Summit Hill) publishes one weekly bulletin through
John Patrick Publishing (church-bulletin.org). I read the 18 October 2026 issue, the newest
on 18 October. Its page-1 masthead is "St. Joseph Parish of the Panther Valley" with the
church at 462 W. Ludlow St., Summit Hill, the weekend Masses (Saturday 4:00 pm, Sunday 8:00
and 10:15 am), weekday Masses at St. Joseph, and "Sat.: 9:00 AM - Shrine of St. Therese".
The lower half of the cover is the Shrine of Saint Therese of Lisieux, 1 E. Garibaldi Ave.,
Nesquehoning, with the same priest (Rev. Thomas Osei Gyau) as rector. So the bulletin covers
two worship sites, and the shrine has no bulletin of its own (its site,
shrineofsainttherese.com, posts only "Weekly Mass, Saturday 9:00 AM, at the Shrine" and
names St. Joseph's as its parish).

**The 2016 Panther Valley merger** (checked against the coordinator's lead): the Times News
reported on 23 April 2016 the diocese's plan to merge St. Francis of Assisi (Nesquehoning) and
St. Katharine Drexel (Lansford) into St. Joseph, Summit Hill, "effective later this year",
and the closing of Our Lady of the Angels Academy, Lansford. It happened: the parish's own
history page says both "became part of St. Joseph Parish of the Panther Valley, Summit Hill,
on July 1, 2016", the diocesan map names St. Joseph as the repository for both parishes'
records, and St. Katharine Drexel held its final Mass on Sunday 26 June 2016 (Times News,
26 June 2016). Both former parish churches are closed and sold (see `excluded/`); the
former Our Lady of Mount Carmel church in Nesquehoning stays open as the diocesan shrine.

## Worship sites

- `st-joseph-summit-hill`: Saturday 4:00 pm, Sunday 8:00 and 10:15 am, Monday, Wednesday,
  Thursday, Friday 8:00 am, Tuesday 6:00 pm.
- `shrine-of-st-therese-nesquehoning` (former Our Lady of Mount Carmel church): Saturday
  9:00 am Mass every week. It does not satisfy the Sunday obligation, but it is a weekly
  public Mass.

Ruled out: St. Katharine Drexel, Lansford (`excluded/st-katharine-drexel-lansford`, closed
June 2016, sold 2021) and the former St. Francis of Assisi church, 140 W. Mill St.,
Nesquehoning (`excluded/st-francis-of-assisi-nesquehoning`, closed June 2016, sold to
Family Promise in 2021). GCatholic still lists St. Katharine Drexel; its "St. Francis of
Assisi" entry (23658) carries the shrine's Plus Code and "Shrine of St. Therese of Lisieux",
so it is linked to the shrine.

## Website and bulletin provider

stjscatholicchurch.org (WordPress) links the bulletin as
`https://www.jppc.net/onlinebulletins/248template.pdf`, which redirects to
church-bulletin.org/?id=248 and on to the listing page above. Recorded as `other` with the
listing page as the publication. **The bulletin is image-only** (all 8 pages of the 18 October
issue are scans with no text layer), so the pipeline has to read it as images.

Fetch check (2026-10-18): resolved; recipe `page-pdfs https://www.jppc.net/onlinebulletins/248template.pdf` picked `2026-10-18.pdf` (current, 9.1 MB of images). Recorded as provider_id.

## Not yet confirmed

Nothing about structure. The directory's Mass times (Sunday 8, 9:30, 11, pastor Rev. Eric J.
Gruber) are out of date against the bulletin (Sunday 8:00 and 10:15, Rev. Thomas Osei Gyau,
Parochial Administrator).
