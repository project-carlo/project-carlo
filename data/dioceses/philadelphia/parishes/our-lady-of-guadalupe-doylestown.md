---
name: Our Lady of Guadalupe Parish
website: https://www.olguadalupe.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-of-guadalupe-roman-catholic-church-buckingham-pa-18902
publication: ['url:https://www.church-bulletin.org/our-lady-of-guadalupe-roman-catholic-church-buckingham-pa-18902']
group: ''
evidence:
- url: https://www.church-bulletin.org/our-lady-of-guadalupe-roman-catholic-church-buckingham-pa-18902
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 131, 'Our Lady of Guadalupe Roman Catholic Church', Buckingham, PA 18902,
    5194 Cold Spring Creamery Road, phone (267) 247-5374; latest edition October 25, 2026, dated archive
    back to November 2024.
- url: https://www.church-bulletin.org/bulletin/our-lady-of-guadalupe-roman-catholic-church-buckingham-pa-18902/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (12 pages, image-only; pages 1-2 rendered). Page-1 cover: ''Our Lady of
    Guadalupe Roman Catholic Church''; ''MASS TIMES Saturday Vigil: 5 p.m. Sunday: 9 a.m. and 11 a.m.
    Tuesday through Saturday: 8 a.m.''; ''Our Lady of Guadalupe Church, Parish Life Center & Parish Offices,
    5194 Cold Spring Creamery Road, Doylestown, PA 18902''; date band ''Sunday, October 25, 2026, Buckingham,
    Pennsylvania''. Names this parish alone.'
- url: https://www.olguadalupe.org/bulletin
  seen: 2026-10-29
  note: 'Parish site (Wix): the Bulletin page links 49 hash-named _files/ugd/*.pdf files and no jppc or
    church-bulletin.org link. The first four sampled were one-page files, one of them empty, none a bulletin
    issue, so the page is not shown to be a current archive; the listing stays the channel.'
- url: https://archphila.org/parish/our-lady-of-guadalupe-doylestown/
  seen: 2026-10-29
  note: 'Directory: pastor Rev. Msgr. Joseph P. Gentili; 5194 Cold Spring Creamery Road, Doylestown, PA
    18902; Hispanic apostolate parish.'
promoted: 2026-10-29
research:
- method: probe url on olguadalupe.org, probe get of the /bulletin page and four sampled _files/ugd PDFs
  url: https://www.olguadalupe.org/bulletin
  checked: '2026-10-29'
  outcome: not-found
  next_action: Open the newest _files/ugd link on the /bulletin page, if the listing ever stops updating,
    to see whether the site carries issues of its own
  retry_when: The John Patrick listing's latest edition falls more than two weeks behind
bulletin_status: available
---

## Publisher

Our Lady of Guadalupe Parish (Rev. Msgr. Joseph P. Gentili, Pastor, per the directory) prints its bulletin with John Patrick Publishing: listing 131 has an issue for 25 October 2026 and a dated archive back to November 2024. The row is `other`, `page-pdfs` on the listing. The PDFs have no text layer, so the cover and Mass times were read from a render of page 1 (page 2 rendered too).

## Worship sites

One church, 5194 Cold Spring Creamery Road. The page-1 cover gives one set of Mass times and names the 'Parish Life Center & Parish Offices' at the same address; no mission or chapel is named. The directory and the bulletin say Doylestown; the listing and GCatholic say Buckingham (the township); the diocese's `city_aliases` treats the two as one.

## Website and bulletin provider

`https://www.olguadalupe.org` is a Wix site. Its Bulletin page links hash-named PDFs that were not bulletin issues in a four-file sample, and no John Patrick link, so it is not used as a channel. Directory Mass times (Saturday vigil 5 PM, Sunday 9 and 11 AM, Tuesday 4 PM, Wednesday-Saturday 8 AM) differ from the bulletin only in the Tuesday time (bulletin: Tuesday through Saturday 8 a.m.).

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (4 days, date inferred from the file name); identity `unverified` because no expected identity is supplied by the check and the PDF has no text layer (cover read from a render). It printed no `recipe` line, as the pinned `provider_id` already holds it.

## Not yet confirmed

Pages 3-12 were not read. The Wix Bulletin page's other 45 files were not opened.
