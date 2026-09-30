---
name: Southern Adirondack Catholic Community (St. Mary's, Ticonderoga and Sacred Heart, Crown Point)
website: https://www.southernadirondackcatholics.org/
bulletin_provider: parishes_online
provider_id: st-mary-s-church-sacred-heart-our-lady-of-lordes
publication: ['po-org:st-mary-s-church-sacred-heart-our-lady-of-lordes', 'lpi:0018000000Qc2bhAAB', 'po-container:03/0940']
group: Southern Adirondack Catholic Community (St. Mary's, Sacred Heart, Our Lady of Lourdes)
evidence:
- url: https://container.parishesonline.com/bulletins/03/0940/20260927B.pdf
  seen: 2026-09-30
  quote: St. Mary’s Church/Sacred Heart/Our Lady of Lordes, Ticonderoga, NY 03-0940
  note: 'Page 5 (text) of the 27 September 2026 issue, ParishesOnline container 03/0940: the LPi footer
    naming the account. Pages 1-3 are images (read with render.py): page 1 is headed ''SOUTHERN ADIRONDACK
    CATHOLIC COMMUNITY / ST. MARY''S, SACRED HEART, AND OUR LADY OF LOURDES'' with photos of the three
    churches and a Mass schedule for St. Mary''s (Sat 4:00 PM, Sun 9:30 AM) and Sacred Heart (Sun 8:00
    AM); page 2 ''MASS INTENTIONS'' lists St. Mary''s, Sacred Heart and Our Lady of Lourdes.'
- url: https://container.parishesonline.com/bulletins/03/0940/20260927B.pdf
  seen: 2026-09-30
  quote: Wilcox & Regan Wilcox & Regan Funeral HomeFuneral Home Since 1892 Ticonderoga, NY
  note: Page 5 text; the issue's ads are all Ticonderoga businesses. Same issue as above.
- url: https://www.southernadirondackcatholics.org/sacred-heart-bulletin
  seen: 2026-09-30
  note: 'Read with visit.py (Wix site). The ''Sacred Heart Bulletin'' page embeds the ParishesOnline widget:
    publications lpi:0018000000Qc2bhAAB and po-container:03/0940, listing issues MON SEP 28, 21, 14 and
    7. The ''St. Mary''s Bulletin'' page (/st-mary-s-bulletin) shows no widget when loaded that way.'
- url: https://parishesonline.com/organization/st-mary-s-church-sacred-heart-our-lady-of-lordes
  seen: 2026-09-30
  note: 'probe po: organization ''St. Mary''s Church/Sacred Heart/Our Lady of Lourdes'', 22 Fr Jogues
    Pl, Ticonderoga, website southernadirondackcatholics.org, ids po-org:st-mary-s-church-sacred-heart-our-lady-of-lordes,
    lpi:0018000000Qc2bhAAB, po-container:03/0940; latest issue 2026-09-27, weekly (20 Sep, 13 Sep, 6 Sep
    also present).'
- url: https://www.southernadirondackcatholics.org/
  seen: 2026-09-30
  note: 'Home page read with visit.py: ''Southern Adirondack Catholics is a vibrant and growing faith
    community within the Diocese of Ogdensburg, NY, bringing together the parishes of St. Mary''s (Ticonderoga),
    Our Lady of Lourdes (Schroon Lake), and Sacred Heart of Jesus (Crown Point).'' It links a separate
    ''Our Lady of Lourdes Bulletin'' (the rcdony.org PDF, see our-lady-of-lourdes-schroon-lake).'
- url: https://www.rcdony.org/parish/ticonderoga
  seen: 2026-09-30
  note: 'Diocese directory: St. Mary''s, 22 Father Jogues Place, Ticonderoga; website southernadirondackcatholics.org;
    Administrator Rev. Fernando V. Solomon, Jr.; Crown Point and Schroon Lake list the same website and
    administrator.'
promoted: 2026-09-30
---

## Publisher

One weekly ParishesOnline bulletin (container `03/0940`, organization "St. Mary's Church/Sacred Heart/Our Lady of Lourdes", Ticonderoga) serves the Southern Adirondack Catholic Community: St. Mary's (Ticonderoga), Sacred Heart of Jesus (Crown Point) and Our Lady of Lourdes (Schroon Lake), three canonical parishes under one administrator, Rev. Fernando V. Solomon, Jr. The 27 September 2026 issue (read 2026-09-30) is headed "SOUTHERN ADIRONDACK CATHOLIC COMMUNITY / ST. MARY'S, SACRED HEART, AND OUR LADY OF LOURDES" and its page 2 lists Mass intentions at all three churches. Pages 1 to 3 of the PDF are images with no text layer (rendered with `render.py` and read as pictures), so only the ads and footer on pages 4 to 5 can be quoted; the pipeline will need to read this bulletin as an image.

## Worship sites

- `st-marys-ticonderoga`: Saturday 4:00 pm, Sunday 9:30 am, Monday and Friday 9:00 am.
- `sacred-heart-of-jesus-crown-point`: Sunday 8:00 am, Tuesday 8:30 am.

**Our Lady of Lourdes, Schroon Lake is a separate row**, `our-lady-of-lourdes-schroon-lake`, although this bulletin also lists its Masses (page 2 "Mass Intentions"). Schroon Lake keeps publishing its own one-church-headed bulletin, a PDF on rcdony.org dated 27 September 2026, and the community's own website links that PDF as the "Our Lady of Lourdes Bulletin" and this ParishesOnline widget for the other two. One live member channel means no merge (README, Method step 5). Both bulletins carry the same three-church Mass list, so the pipeline may read Schroon Lake's Masses twice; that is a question for the pipeline, not for the rows.

## Website and bulletin provider

southernadirondackcatholics.org is a Wix site (`probe url` 200, no embedded id on the home page). Its "Sacred Heart Bulletin" page embeds the ParishesOnline widget, which gives `lpi:0018000000Qc2bhAAB` and `po-container:03/0940`; `probe po` on the organization gives the slug. The diocese's Parish Bulletins page links the same organization for Ticonderoga and Crown Point. Provider `parishes_online`, `provider_id` is the organization slug.

## Not yet confirmed

The pages of the bulletin that are images were read by eye on the 27 September issue only. Whether the ParishesOnline account will keep listing Our Lady of Lourdes alongside a Schroon Lake PDF is not known; see `our-lady-of-lourdes-schroon-lake`.
