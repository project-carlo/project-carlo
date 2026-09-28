---
name: Parish of the Holy Trinity
website: https://www.holytrinityhudson.org
bulletin_provider: parishes_online
provider_id: holy-trinity-parish-12534
publication: ['po-org:holy-trinity-parish-12534', 'lpi:0018000000Qc2beAAB', 'po-container:03/0174']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/0174/20260927B.pdf
  seen: 2026-09-28
  quote: HOLY TRINITY PARISH Hudson and Germantown, New York 429 E. Allen St.
  note: 27 September 2026 issue, masthead, page 1 (pastor Very Rev. Msgr. Anthony Barratt).
- url: https://container.parishesonline.com/bulletins/03/0174/20260927B.pdf
  seen: 2026-09-28
  quote: 'SATURDAY VIGIL MASS: (October 3) … (HUD) Christine Dorsch - Cheryl Clow … For The Living & Deceased
    of the Parish (LNLTH) … SUNDAY MORNING MASS: (October 4) … (HUD) Paul Baggata … (G’TWN) Thomas Farrell
    - Jane & Bill Martin'
  note: '27 September 2026 issue, page 3, "Masses for this week": Saturday 4:00 pm (HUD), 5:30 pm (LNLTH
    = Linlithgo), Sunday 9:00 am (HUD), 11:00 am (G''TWN = Germantown). The "am/pm" after each time is
    set in a symbol font and extracts as garbage, so the quote skips it.'
- url: https://www.holytrinityhudson.org/sunday-bulletin
  seen: 2026-09-28
  note: The parish site (eCatholic, ecatholic:2170, behind Cloudflare; read with parish-site-access visit.py).
    Its Bulletin page lists one link per Sunday and embeds lpi:0018000000Qc2beAAB and po-container:03/0174.
- url: https://www.rcda.org/parishes/parish/parish-holy-trinity-hudson-ny
  seen: 2026-09-28
  quote: 'Sunday: 9:00 am Hudson Sunday: 11:00 am Germantown'
  note: 'Directory detail page (directory:274): also "Saturday: 4:00 pm (Vigil Mass) Hudson Saturday:
    5:30 pm (Vigil Mass) Linlithgo".'
promoted: 2026-09-28
---

## Publisher

The Parish of the Holy Trinity (Hudson and Germantown) publishes its own weekly bulletin
through ParishesOnline, container 03/0174. The 27 September 2026 masthead reads "HOLY
TRINITY PARISH Hudson and Germantown, New York, 429 E. Allen St." and page 3 lists the
week's Masses by site code: weekdays 7:15 am (HUD), Friday 9:00 am (G'TWN), Saturday 4:00
pm (HUD) and 5:30 pm (LNLTH), Sunday 9:00 am (HUD) and 11:00 am (G'TWN). The diocese
directory's schedule for the parish (directory:274) matches, naming Hudson, Germantown and
Linlithgo.

## Worship sites

- `st-mary-hudson` (429 E. Allen St., the parish church; the directory entry "Parish of the
  Holy Trinity & Our Lady of Victory Adoration Chapel" is linked here; the adoration chapel
  is inside Holy Trinity, not a separate Mass site)
- `resurrection-germantown` (Church Ave., Germantown)
- `nativity-linlithgo` (Nativity chapel, Linlithgo; Saturday 5:30 pm)

The parish was formed in 2009 by merging St. Mary's (Hudson) and Resurrection (Germantown),
"with both remaining open" (The Evangelist's 2009 list). The institutional-records index also
sends Hudson's Our Lady of Mt. Carmel, Our Lady of Perpetual Help and Sacred Heart to this
parish; none is in either roster and none appears in the bulletin, so no records were made
for them. St. Nicholas, 206 Union St., Hudson is Ukrainian Catholic
(`excluded/st-nicholas-ukrainian-hudson`).

## Website and bulletin provider

holytrinityhudson.org is the parish's eCatholic site (Cloudflare; `probe url` gets 403,
visit.py loaded it). Its /sunday-bulletin page embeds the ParishesOnline ids, and `probe po
0018000000Qc2beAAB` gives org holy-trinity-parish-12534, 429 E Allen St, container 03/0174,
issues weekly through 2026-09-27. The eCatholic site id (ecatholic:2170) is the website, not
a bulletin: `issues.py ecatholic ecatholic:2170` found no Sunday-dated issue, so it is not a
publication id.

## Not yet confirmed

Nothing.
