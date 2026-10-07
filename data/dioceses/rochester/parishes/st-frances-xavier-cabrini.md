---
name: St. Frances Xavier Cabrini Parish
website: https://cabriniroc.org/faq
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://cabriniroc.org/faq']
group: ''
evidence:
- url: https://cabriniroc.org/faq
  seen: 2026-10-02
  quote: 'To view our September 5-6th bulletin click on the following link:'
  note: '"Parish Bulletin" section of the English FAQ page (eCatholic, behind Cloudflare; read with visit.py):
    one Google Drive file link, https://drive.google.com/file/d/1aeIO3IX6qAqL_7TpxOPcLmyWERxDuKaz/view?usp=sharing.
    The Spanish page /preguntas-frecuentes carries a different file (…1FLga19-YA4SNVTWwN9wtmjXzsHitW_qV…)
    for the same issue. Neither the home page nor any other page links a Drive folder.'
- url: https://drive.google.com/uc?export=download&id=1aeIO3IX6qAqL_7TpxOPcLmyWERxDuKaz
  seen: 2026-10-02
  quote: MASS at Annunciation—For Ida Caruso  by Carmen Caruso
  note: 'The 5-6 September 2026 issue (and the week to 13 September): masses at Annunciation (Saturday
    4:00 pm), Corpus Christi (Sunday 8:30 am English, 10:00 am Spanish) and Saint Michael (Sunday 11:45
    am Spanish). Read via drive.google.com/uc?export=download.'
- url: https://cabriniroc.org/faq
  seen: 2026-10-02
  quote: Saturday 4 pm at Annunciation 1760 Norton St
  note: 'FAQ page Mass schedule: English Saturday 4 pm Annunciation; Sunday 8:30 am Corpus Christi 864
    E Main St; Spanish Sunday 10 am Corpus Christi, 11:45 am Saint Michael "859 N Clinton Ave"; Tuesday
    12:10 pm; Friday 6:15 pm Corpus Christi.'
- url: https://ps.dor.org/directory/st-frances-xavier-cabrini-parish/
  seen: 2026-10-02
  quote: Church of the Annunciation, 1760 Norton Street Corpus Christi Church, 864 East Main Street St.
    Michael's Church, 869 N. Clinton Avenue
  note: 'Diocesan directory listing: the parish was constituted from twelve former parishes; "Of all the
    former churches only Annunciation, Corpus Christi and Saint Michael''s remain as Catholic Churches,
    others have been repurposed or demolished."'
- url: https://cabriniroc.org/faq
  seen: 2026-10-07
  quote: 'To view our September 5-6th bulletin click on the following link:'
  note: Unchanged since 2 October (read in headed Chrome). The Spanish page /preguntas-frecuentes still
    links "Boletin Cabrini 5 y 6 de septiembre de 2026". files.ecatholic.com/29120/bulletins/<date>.pdf
    answers 403 (not there) for every Sunday from 6 September to 11 October.
revisit: Check cabriniroc.org/faq and /preguntas-frecuentes, and the parish Facebook, for a bulletin newer
  than 5-6 September 2026; if one is posted weekly, set the row back to `other` (the fetch needs a recipe
  or a resolver fix, see Website and bulletin provider)
revisit_after: 2027-01-15
---

## Publisher

Cabrini Parish (one parish for the former Holy Redeemer, St. Francis Xavier, Our Lady of Mount Carmel, Our Lady of Perpetual Help, St. Andrew, Light of Christ, Our Lady of the Americas, Our Lady of Sorrows, Corpus Christi, St. Michael and Annunciation) posts a bulletin as a Google Drive file link on its eCatholic website's FAQ page (English) and Preguntas Frecuentes page (Spanish). The newest issue linked, read 2 October 2026, is the one for 5-6 September 2026 (it runs to 13 September), four weeks old. It names Annunciation, Corpus Christi and Saint Michael as the three Mass sites. I did not find a 27 September or 4 October issue on the website or in the eCatholic file host (`files.ecatholic.com/29120/bulletins/<date>.pdf` answers 403 for 13 Sept to 4 Oct); the parish may post current issues on Facebook (`facebook.com/CabriniRochester`), which I could not read.

## Worship sites

Three: `annunciation` (1760 Norton Street), `corpus-christi` (864 East Main Street; GCatholic and the locator call it Our Lady of the Americas), `st-michael` (869 North Clinton Avenue). The locator's "Corpus Christi School, 546 Oxford St" is a school (`excluded/corpus-christi-school-rochester.md`). The former churches are all listed as repurposed or demolished by the directory; GCatholic's Holy Redeemer is in `excluded/holy-redeemer-rochester.md`. The locator also gives Cabrini and "St. Michaels" an address of 124 Evergreen St, which matches no worship site (`open/cabrini-124-evergreen-street-rochester.md`).

## Website and bulletin provider

The live row said `google_drive` with the home page as website. The home page links no folder: it is a landing page ("ESPAÑOL / ENGLISH" buttons to /preguntas-frecuentes and /faq) and the bulletin is a single Drive file link on /faq. So `google_drive` has nothing to read. I changed the row to `bulletin_provider: other` with `website: https://cabriniroc.org/faq` (the page with the "Parish Bulletin" section and the Drive file link; the fetch's `other` resolver reads Drive file links as PDFs). The risk is that the link on that page is four weeks stale and the parish updates it irregularly.

**Changed 2026-10-07 to `no_bulletin`.** As `other` the row never fetched anything: the weekly runs of 27 September and 4 October both failed with `resolve_failed` ("No bulletin page link found for other provider at https://cabriniroc.org/faq"), because the Drive link's text is the bare Drive URL and nothing on the page says "bulletin" in a link. And there is nothing current to fetch: on 7 October the FAQ page still links the 5-6 September issue, five weeks old. The page also carries hidden, empty-text Drive links to older issues (Content-Disposition names "Cabrini Bulletin January 3-4, 2025.pdf", "January 10-11, 2026", "April 25-26, 2026"), so a recipe that takes the page's first PDF link would read a 2025 bulletin. As `no_bulletin` the parish and its three churches are kept here but left off the site.

## Not yet confirmed

Whether the parish posts current issues on Facebook (`facebook.com/CabriniRochester`, unreadable without a login). If it starts posting weekly on /faq again, the row needs a resolver that takes the link under "Parish Bulletin" rather than the first Drive link on the page.
