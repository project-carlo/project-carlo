---
name: St. Kateri Tekakwitha
website: https://www.kateriirondequoit.org
bulletin_provider: parishes_online
provider_id: st-kateri-tekakwitha-parish-14617
publication:
- po-org:st-kateri-tekakwitha-parish-14617
- lpi:0018000000Qbz92AAB
- po-container:06/0078
group: Saint Kateri Tekakwitha
evidence:
- url: https://container.parishesonline.com/bulletins/06/0078/20260927B.pdf
  seen: '2026-10-02'
  quote: Saint Kateri Tekakwitha, Rochester, NY 06-0078
  note: 'Page footer (page 7 of 8, text layer) of the 27 September 2026 issue. Pages 1-6 are images with
    no text layer: I read page 1 as a picture (render.py). Its masthead is "SAINT KATERI TEKAKWITHA PARISH",
    "445 Kings Highway South, Rochester, NY 14617", with the Mass schedule "SATURDAY: 4:00 pm: Christ
    The King Church / SUNDAY: 4:00 pm: Christ The King Church, 8:00 am: St. Cecilia Church, 9:30 am: St.
    Margaret Mary Church, 11:00 am: Christ The King Church; weekday noon Mass Monday - Friday: Christ
    The King Church", and a "LATIN MASS COMMUNITY St. Thomas The Apostle Visit: www.skt-lmc.org" box with
    no times.'
- url: https://ps.dor.org/directory/st-kateri-tekakwitha/
  seen: '2026-10-02'
  quote: Saturday 4 pm at Christ the King Sunday 8 am at St. Cecilia 9:30 am at St. Margaret Mary 11 am
    at Christ the King
  note: 'Diocesan directory listing: "St. Kateri Tekakwitha, a multi-site parish" with Christ the King,
    St. Cecilia, St. Margaret Mary and St. Thomas the Apostle (the last with the "Latin Mass Community"
    Masses, 9 am English and 11:15 am Latin).'
- url: https://www.kateriirondequoit.org/about-us/bulletins/
  seen: '2026-10-02'
  note: 'Parish bulletins page embeds po-org:st-kateri-tekakwitha-parish-14617 (visit.py --bulletin).
    `probe po`: org title "Christ The King Church", latest issue 2026-10-04, container 06/0078.'
promoted: 2026-10-02
---

## Publisher

St. Kateri Tekakwitha (Irondequoit) is a multi-site parish with one ParishesOnline bulletin (container 06/0078, org `st-kateri-tekakwitha-parish-14617`, LPi id 0018000000Qbz92AAB; the org's own title is still "Christ The King Church"). The 27 September 2026 issue is mostly image pages: the masthead and Mass schedule on page 1 are a picture (I viewed it; `recheck` can't find them). Its Mass schedule lists Christ the King, St. Cecilia and St. Margaret Mary, with the weekend and daily noon Masses, and points to the Latin Mass Community at St. Thomas the Apostle with no times ("Visit: www.skt-lmc.org"). The pipeline will need to read this bulletin as an image.

## Worship sites

Three: `christ-king` (445 Kings Highway South), `st-cecilia` (2732 Culver Road) and `st-margaret-mary-rochester` (401 Rogers Parkway). I moved the fourth, `st-thomas-apostle` (4536 St. Paul Boulevard), to its own row `st-kateri-latin-mass-community`: it has its own weekly bulletin, with its own masthead and Mass times, and this bulletin carries none of its Masses. The diocesan directory also notes an Ordinariate Mass at St. Cecilia at 11 am ("Chair of St. Peter Ordinariate Mass at St. Cecilia"); that community is in `excluded/st-alban-ordinariate-community.md`. Other former parishes (St. Salome, St. George on the Lake, St. Thomas the Apostle as a parish) have records here per the sacramental index.

## Website and bulletin provider

`kateriirondequoit.org` is alive and its bulletins page embeds the org. Provider and `provider_id` correct.

## Not yet confirmed

Page 1's masthead is only an image, so the Mass times above come from that picture and the diocesan directory; the 4 October issue was not rendered.
