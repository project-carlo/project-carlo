---
name: St. Frances Xavier Cabrini Parish
website: https://cabriniroc.org/faq
bulletin_provider: other
provider_id: ''
publication:
- url:https://cabriniroc.org/faq
group: ''
evidence:
- url: https://cabriniroc.org/faq
  seen: '2026-10-02'
  quote: 'To view our September 5-6th bulletin click on the following link:'
  note: '"Parish Bulletin" section of the English FAQ page (eCatholic, behind Cloudflare; read with visit.py):
    one Google Drive file link, https://drive.google.com/file/d/1aeIO3IX6qAqL_7TpxOPcLmyWERxDuKaz/view?usp=sharing.
    The Spanish page /preguntas-frecuentes carries a different file (…1FLga19-YA4SNVTWwN9wtmjXzsHitW_qV…)
    for the same issue. Neither the home page nor any other page links a Drive folder.'
- url: https://drive.google.com/uc?export=download&id=1aeIO3IX6qAqL_7TpxOPcLmyWERxDuKaz
  seen: '2026-10-02'
  quote: MASS at Annunciation—For Ida Caruso  by Carmen Caruso
  note: 'The 5-6 September 2026 issue (and the week to 13 September): masses at Annunciation (Saturday
    4:00 pm), Corpus Christi (Sunday 8:30 am English, 10:00 am Spanish) and Saint Michael (Sunday 11:45
    am Spanish). Read via drive.google.com/uc?export=download.'
- url: https://cabriniroc.org/faq
  seen: '2026-10-02'
  quote: Saturday 4 pm at Annunciation 1760 Norton St
  note: 'FAQ page Mass schedule: English Saturday 4 pm Annunciation; Sunday 8:30 am Corpus Christi 864
    E Main St; Spanish Sunday 10 am Corpus Christi, 11:45 am Saint Michael "859 N Clinton Ave"; Tuesday
    12:10 pm; Friday 6:15 pm Corpus Christi.'
- url: https://ps.dor.org/directory/st-frances-xavier-cabrini-parish/
  seen: '2026-10-02'
  quote: Church of the Annunciation, 1760 Norton Street Corpus Christi Church, 864 East Main Street St.
    Michael's Church, 869 N. Clinton Avenue
  note: 'Diocesan directory listing: the parish was constituted from twelve former parishes; "Of all the
    former churches only Annunciation, Corpus Christi and Saint Michael''s remain as Catholic Churches,
    others have been repurposed or demolished."'
promoted: 2026-10-02
revisit: Check whether cabriniroc.org/faq links a current bulletin (it was on 5-6 September on 2 October
  2026); if not, switch the row to no_bulletin
revisit_after: '2026-11-01'
---

## Publisher

Cabrini Parish (one parish for the former Holy Redeemer, St. Francis Xavier, Our Lady of Mount Carmel, Our Lady of Perpetual Help, St. Andrew, Light of Christ, Our Lady of the Americas, Our Lady of Sorrows, Corpus Christi, St. Michael and Annunciation) posts a bulletin as a Google Drive file link on its eCatholic website's FAQ page (English) and Preguntas Frecuentes page (Spanish). The newest issue linked, read 2 October 2026, is the one for 5-6 September 2026 (it runs to 13 September), four weeks old. It names Annunciation, Corpus Christi and Saint Michael as the three Mass sites. I did not find a 27 September or 4 October issue on the website or in the eCatholic file host (`files.ecatholic.com/29120/bulletins/<date>.pdf` answers 403 for 13 Sept to 4 Oct); the parish may post current issues on Facebook (`facebook.com/CabriniRochester`), which I could not read.

## Worship sites

Three: `annunciation` (1760 Norton Street), `corpus-christi` (864 East Main Street; GCatholic and the locator call it Our Lady of the Americas), `st-michael` (869 North Clinton Avenue). The locator's "Corpus Christi School, 546 Oxford St" is a school (`excluded/corpus-christi-school-rochester.md`). The former churches are all listed as repurposed or demolished by the directory; GCatholic's Holy Redeemer is in `excluded/holy-redeemer-rochester.md`. The locator also gives Cabrini and "St. Michaels" an address of 124 Evergreen St, which matches no worship site (`open/cabrini-124-evergreen-street-rochester.md`).

## Website and bulletin provider

The live row said `google_drive` with the home page as website. The home page links no folder: it is a landing page ("ESPAÑOL / ENGLISH" buttons to /preguntas-frecuentes and /faq) and the bulletin is a single Drive file link on /faq. So `google_drive` has nothing to read. I changed the row to `bulletin_provider: other` with `website: https://cabriniroc.org/faq` (the page with the "Parish Bulletin" section and the Drive file link; the fetch's `other` resolver reads Drive file links as PDFs). The risk is that the link on that page is four weeks stale and the parish updates it irregularly.

## Not yet confirmed

Whether the parish posts a current bulletin anywhere readable (it is also possible the parish only updates the FAQ link monthly). Revisit 2026-11-01: if /faq is still on the September issue, the parish effectively has no current bulletin and the row should become `no_bulletin`.
