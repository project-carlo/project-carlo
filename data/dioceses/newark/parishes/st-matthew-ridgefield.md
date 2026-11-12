---
name: St. Matthew, Ridgefield
website: https://stmatthewridgefield.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6014
publication: ['url:https://www.church-bulletin.org/the-roman-catholic-community-of-saint-matthew-ridgefield-nj-07657']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/the-roman-catholic-community-of-saint-matthew-ridgefield-nj-07657/2026-11-01.pdf
  seen: 2026-11-03
  note: 'Image-only issue (8 pages, no text layer), read with render.py. Page 1 masthead: ''The Roman
    Catholic Community of St. Matthew Church''. Page 2: ''555 Prospect Avenue • Ridgefield • New Jersey
    07657'', Mass Schedule Monday-Friday 7:30AM, Saturday 9:00AM, Saturday Mass of Anticipation 4:00PM,
    Sunday 8:00AM, 10:00AM & 12NN; Thursday Holy Hour of Adoration at St. Nicholas Church, Palisades Park.
    Served by the Vocationist Fathers, Fr. Jimson Varghese, SDV, Pastor.'
- url: https://www.church-bulletin.org/bulletin/the-roman-catholic-community-of-saint-matthew-ridgefield-nj-07657/2026-11-01.pdf
  seen: 2026-11-03
  note: 'Page 8 footer (image): ''6014 The Roman Catholic Community of Saint Matthew, Ridgefield, NJ (B)
    John Patrick Publishing Company, Inc.'''
- url: https://church-bulletin.org/6014
  seen: 2026-11-03
  note: The John Patrick listing for id 6014 links weekly issues 2026-11-01, 10-25, 10-18, 10-11 … under
    /bulletin/the-roman-catholic-community-of-saint-matthew-ridgefield-nj-07657/.
- url: https://stmatthewridgefield.org/
  seen: 2026-11-03
  note: The parish homepage (probe get) links https://www.jppc.net/onlinebulletins/6014template.pdf as
    its bulletin.
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

John Patrick Publishing prints St. Matthew's bulletin (id 6014). I read the 1 November 2026 issue, which is image-only (rendered pages 1, 2 and 8): page 1 masthead "The Roman Catholic Community of St. Matthew Church", page 2 "555 Prospect Avenue • Ridgefield • New Jersey 07657", and the page-8 footer "6014 The Roman Catholic Community of Saint Matthew, Ridgefield, NJ (B) John Patrick Publishing Company, Inc." Quotes are by note, since recheck can't read image pages.

## Worship sites

One church, `st-matthew-ridgefield`. The page-2 Mass Schedule gives Monday-Friday 7:30 AM, Saturday 9:00 AM, Saturday Anticipation 4:00 PM and Sunday 8:00 AM, 10:00 AM and 12 noon, with no other Mass site; it mentions a Thursday Holy Hour of Adoration at St. Nicholas Church, Palisades Park, which is another parish's church and is not a Mass of this one. The archdiocese directory (174) and GCatholic (18542) each list only this church.

## Website and bulletin provider

The website is the directory's https://stmatthewridgefield.org/, whose homepage links jppc.net/onlinebulletins/6014template.pdf. The provider is `other`, pinned to `page-pdfs https://church-bulletin.org/6014` as the playbook advises (the ?id= form runs a week ahead).

Fetch check (2026-11-03, headed): ok, resolved `page-pdfs on https://church-bulletin.org/6014: current` and picked the 1 November 2026 issue read above (date from the URL), fresh (2 days); identity `unverified` because the issue has no text layer, but the rendered masthead and footer confirm it. The recipe is the one in `provider_id`.

## Not yet confirmed

Nothing open.
