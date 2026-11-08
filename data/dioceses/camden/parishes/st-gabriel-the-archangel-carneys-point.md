---
name: St. Gabriel the Archangel Parish
website: https://www.saintgabrielarchangel.org/
bulletin_provider: other
provider_id: page-pdfs https://www.saintgabrielarchangel.org/bulletin
publication: ['url:https://www.saintgabrielarchangel.org/bulletin#st-gabriel-the-archangel']
group: ''
evidence:
- url: https://irp.cdn-website.com/f0e3bb89/files/uploaded/BULLETIN+10.25.26+FINAL.pdf
  seen: 2026-10-29
  quote: CORPUS CHRISTI CHURCH, CARNEYS POINT, NJ ST. MARY’S CHURCH, 25 OAK STREET, SALEM, NJ
  note: 'Page 1 of the 25 October 2026 issue (text layer; the newest on the parish''s Bulletin page).
    Masthead ''St. Gabriel the Archangel Parish'', ''Parish Office: 369 Georgetown Road, Carneys Point,
    NJ 08069'', ''Rev. Jerold C. Mariastanislaus'' first in the staff column with ''Pastor-ext. 303''.
    One Mass schedule over two churches: ''Corpus Christi Church'' Saturday 4pm [Vigil], Sunday 10am and
    12:30pm [Español]; ''St. Mary’s Church'' Sunday 8am; weekday 8:30am in the Corpus Christi chapel.
    Searched the whole issue for Pennsville, Queen, Apostles: no hits.'
- url: https://www.saintgabrielarchangel.org/mass-times
  seen: 2026-10-29
  quote: 'Corpus Christi Saturday [Vigil]: 4pm'
  note: The parish's own Mass Times page gives the same two churches (Corpus Christi; St. Mary’s Church
    Sunday 8am) and no third.
- url: https://www.saintgabrielarchangel.org/bulletin
  seen: 2026-10-29
  quote: Bulletin October 25, 2026
  note: 'Parish Bulletin page: eight dated links (6 Sept to 25 Oct 2026) to irp.cdn-website.com/f0e3bb89/files/uploaded/BULLETIN+MM.DD.26+….pdf,
    newest first in the page source.'
- url: https://www.camdendiocese.org/decrees-establishing-st-gabriel-the-archangel-parish-and-the-parish-of-all-saints-on-oct-29/
  seen: 2026-10-29
  quote: St. Gabriel the Archangel Parish will be established through the consolidation of Corpus Christi,
    Carneys Point, Queen of the Apostles, Pennsville, St. James, Penns Grove, and St. Mary, Salem.
  note: 'Diocese news, 2010-10-29: parish established 1 December 2010; ''The seat of the new parish will
    be located at Corpus Christi Church. Queen of the Apostles and St. Mary also will be used as worship
    sites''. St. James, Penns Grove was merged in but not named a worship site.'
promoted: 2026-10-30
research:
- method: probe url on the directory's website, then the parish's /bulletin page source
  url: https://www.saintgabrielarchangel.org/bulletin
  checked: '2026-10-29'
  outcome: found
  next_action: None. The page lists dated PDFs on irp.cdn-website.com; probe get shows only text, so the
    links come from the page source (plain curl).
---

## Publisher

St. Gabriel the Archangel Parish (Salem County) publishes its own weekly bulletin, posted as PDFs on its Duda site. The 25 October 2026 issue (page 1, text layer, read 2026-10-29) is headed with the parish office at 369 Georgetown Road, Carneys Point, names Rev. Jerold C. Mariastanislaus as pastor, and gives one Mass schedule across Corpus Christi Church (Carneys Point) and St. Mary's Church, 25 Oak Street, Salem. The parish was established 1 December 2010 from Corpus Christi (Carneys Point), Queen of the Apostles (Pennsville), St. James (Penns Grove) and St. Mary (Salem) (diocese news, 2010-10-29).

## Worship sites

Two churches have Mass in the current bulletin and on the parish's Mass Times page: `corpus-christi-carneys-point` (the seat; the directory's and GCatholic's 'St. Gabriel the Archangel' at 369 Georgetown Rd. is this church) and `st-mary-salem`. GCatholic's two ungrouped entries, St. Mary (Salem) and Queen of the Apostles (Pennsville), are this parish's: St. Mary is a worship site, linked to `st-mary-salem`; Queen of the Apostles is excluded as closed (`excluded/queen-of-the-apostles-pennsville`). St. James, Penns Grove was merged in 2010 but the decree names only Corpus Christi, Queen of the Apostles and St. Mary as worship sites; it is in no roster and the bulletin lists no Mass there, so it has no record.

## Website and bulletin provider

`other` with `page-pdfs` on the parish's /bulletin page, which lists uniform dated names (BULLETIN MM.DD.26 …) newest to oldest. The directory's website (saintgabrielarchangel.org) is current; GCatholic gives none. The hosting account (irp.cdn-website.com/f0e3bb89) is the parish's own.

## Not yet confirmed

Nothing about the structure. The pick is checked by `fetch:check` (result in diocese.md's log).
