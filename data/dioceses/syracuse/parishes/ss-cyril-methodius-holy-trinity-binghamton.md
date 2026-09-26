---
name: SS. Cyril & Methodius and Church of the Holy Trinity
website: https://www.ht-sscmbinghamton.org
bulletin_provider: parishes_online
provider_id: the-roman-catholic-parishes-of-ss-cyril-methodius-and-the-church-of-the-holy-trinity
publication: ['po-org:the-roman-catholic-parishes-of-ss-cyril-methodius-and-the-church-of-the-holy-trinity',
  'lpi:0018000000Qbz9WAAR', 'po-container:03/0543']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/0543/20260927B.pdf
  seen: 2026-09-26
  quote: SS. Cyril & Methodius and The Church of the Holy Trinity, Binghamton, NY 03-0543
  note: 'The 27 September 2026 issue. Pages 1-4 are scanned images with no text layer, so this quote is
    the LPi footer on page 6. Page 1, read as a rendered image: masthead "The Roman Catholic Parishes
    of SS. Cyril & Methodius and Church of the Holy Trinity"; "MASS SCHEDULE / Saturday Vigil: 4:30 pm
    SS. Cyril & Methodius / Sunday: 8:45 am Holy Trinity / 10:15 am Ss Cyril & Methodius / Weekday Mass:
    8:00 am M, W, & F - Holy Trinity / 12:05 pm Tues. & Thrs. Ss. Cyril & Methodius"; "Parish Office:
    Ss. Cyril & Methodius 148 Clinton Street"; "Pastoral Team For Both Parishes" headed by Rev. Msgr.
    John P. Putano.'
- url: https://parishesonline.com/organization/the-roman-catholic-parishes-of-ss-cyril-methodius-and-the-church-of-the-holy-trinity
  seen: 2026-09-26
  note: '`probe po`: "The Roman Catholic Parishes of SS. Cyril & Methodius and The Church of the Holy
    Trinity", 148 Clinton Street, LPi id 0018000000Qbz9WAAR, container 03/0543, weekly issues through
    2026-09-27. The parish site ht-sscmbinghamton.org embeds this organization (`probe url`).'
- url: https://www.syracusediocese.org/holy-trinity-binghamton
  seen: 2026-09-26
  note: 'Diocese page (behind Cloudflare; read with visit.py): Holy Trinity, 346 Prospect Street; "Parish
    Office & Mailing Address 148 Clinton Street"; website ht-sscmbinghamton.org; "Sacramental records
    for St. Ann, Binghamton, St. Joseph, Binghamton, and St. Stanislaus Kosta, Binghamton are retained
    here." Msgr. Putano is listed as pastor of St. Patrick and St. Thomas Aquinas with "PASTORAL CARE,
    CHURCH OF SAINTS CYRIL & METHODIUS, BINGHAMTON; CHURCH OF THE HOLY TRINITY, BINGHAMTON".'
---

## Publisher

SS. Cyril & Methodius and the Church of the Holy Trinity are two canonical parishes (the diocese
lists each separately) that publish **one** weekly bulletin through ParishesOnline, container
03/0543. I read the 27 September 2026 issue. Its pages 1-4 are scanned images, so I read page 1
as a rendered image: the masthead is "The Roman Catholic Parishes of SS. Cyril & Methodius and
Church of the Holy Trinity", the Mass schedule covers both churches (Saturday 4:30 pm and Sunday
10:15 am at SS. Cyril & Methodius, Sunday 8:45 am at Holy Trinity, plus weekday Masses at both),
the parish office is at SS. Cyril & Methodius, 148 Clinton Street, and a "Pastoral Team For Both
Parishes" is headed by Msgr. John P. Putano. The text-layer footer on page 6 names both parishes
and the container. One bulletin, so one row.

Msgr. Putano is also pastor of St. Patrick and St. Thomas Aquinas, but those two publish their own
bulletin (container 06/0167, `parishes/st-patrick-st-thomas-aquinas-binghamton.md`), so they are
a separate row.

## Worship sites

Two: SS. Cyril & Methodius, 148 Clinton Street (`churches/sts-cyril-methodius-binghamton.md`)
and Holy Trinity, 346 Prospect Street (`churches/holy-trinity-binghamton.md`).

Holy Trinity was formed on 1 July 2003 from St. Ann's, St. Joseph's and St. Stanislaus Kostka;
its history page dates each closing Mass. St. Ann's building is the present Holy Trinity church
(renovated 2003-04), so the directory's "St. Anne (Closed)" is linked to the Holy Trinity church
record; St. Joseph's and St. Stanislaus Kostka are excluded as closed
(`excluded/st-joseph-binghamton.md`, `excluded/st-stanislaus-kostka-binghamton.md`).

## Website and bulletin provider

ht-sscmbinghamton.org is the two parishes' shared site; `probe url` found it embedding the
ParishesOnline organization above (LPi 0018000000Qbz9WAAR, container 03/0543), publishing weekly
through 27 September 2026. All three ids are in `publication`.

## Not yet confirmed

Nothing about the structure. The bulletin's front pages are images, so the pipeline's text
extraction will not get the Mass schedule from them.
