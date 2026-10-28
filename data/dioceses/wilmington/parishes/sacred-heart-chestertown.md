---
name: Sacred Heart
website: https://www.sacredparish.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2169
publication: ['url:http://sponsors.bonventure.net/?page=2169']
group: Central Deanery; mission St. John, Rock Hall
evidence:
- url: http://sponsors.bonventure.net/pdfs/2169/2026-10-25.pdf
  seen: 2026-10-27
  quote: A86925 (CK) - Sacred Heart / St. John, Chestertown
  note: The 25 October 2026 issue (8 pages; page 1 is an image, the rest has text). Footer of the last
    page names both churches; page 4 has 'Sunday 8:00 a.m. – St. John – 76' in the weekend attendance
    count, page 6 'blessing of St. John Cemetery, Rock Hall'.
- url: https://www.sacredparish.org/bulletin
  seen: 2026-10-27
  note: 'Read in the browser (curl gets HTTP 403). The home page''s ''Weekly Bulletin'' menu item goes
    to this page: ''Our bulletin is available online, click the image below to view or the link as usual...
    Click here -->to see what''s happening at Sacred Heart & St. John''. The image links to sponsors.bonventure.net/?page=2169,
    whose newest file is pdfs/2169/2026-10-25.pdf.'
- url: https://www.sacredparish.org/bulletins
  seen: 2026-10-27
  quote: September 27, 2026
  note: 'The site''s own eCatholic archive (site 1393) stops at 27 September 2026: files.ecatholic.com/1393/bulletins/20261004.pdf,
    20261011, 20261018 and 20261025 answer 403 (not uploaded). The 27 September file is the same publication
    as the Bonventure 2169 listing.'
- url: https://files.ecatholic.com/1393/bulletins/20260927.pdf
  seen: 2026-10-27
  quote: Rev. Jones Kukatla, Pastor
  note: 'Page 1 of the 27 September 2026 issue: ''SACRED HEART PARISH / MASS SCHEDULE / SACRED HEART Saturday
    ... Mass 4:00 pm, Sunday Mass 10:00 am, Mon., Tues., Wed., Fri. and Sat. Mass at 8:30 am / ST. JOHN
    Sunday Mass 8:00 am, Thursday Mass 8:30 am''. One pastor, one cover for both churches.'
research:
- method: Bonventure listing sponsors.bonventure.net/?page=2169 read with curl over http; archive links
    pdfs/2169/<date>.pdf
  url: http://sponsors.bonventure.net/?page=2169
  checked: '2026-10-27'
  outcome: found
  next_action: Run fetch:check; if Bonventure ever stops, return to the eCatholic archive (site 1393)
bulletin_status: available
publication_reviews:
- parish: holy-rosary-claymont
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2169/2026-10-25.pdf
    seen: 2026-10-27
    quote: Sacred Heart
    note: 'Sacred Heart, Chestertown''s 25 October 2026 issue (Bonventure page 2169): its masthead names
      Sacred Heart, and its weekend Mass counts (p.4) list Sacred Heart and St. John only.'
  - url: http://sponsors.bonventure.net/pdfs/2100/2026-10-25.pdf
    seen: 2026-10-27
    quote: Holy Rosary Church
    note: 'Holy Rosary, Claymont''s 25 October 2026 issue (Bonventure page 2100): the masthead names Holy
      Rosary Church, 3200 Philadelphia Pike, Claymont, and the issue names no other parish''s Mass schedule.'
- parish: our-lady-of-lourdes-seaford
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2169/2026-10-25.pdf
    seen: 2026-10-27
    quote: Sacred Heart
    note: 'Sacred Heart, Chestertown''s 25 October 2026 issue (Bonventure page 2169): its masthead names
      Sacred Heart, and its weekend Mass counts (p.4) list Sacred Heart and St. John only.'
  - url: http://sponsors.bonventure.net/pdfs/2167/2026-10-25.pdf
    seen: 2026-10-27
    quote: Our Lady of Lourdes
    note: 'Our Lady of Lourdes, Seaford''s 25 October 2026 issue (Bonventure page 2167): page 1''s masthead
      names Our Lady of Lourdes Roman Catholic Church with its own weekend Masses.'
- parish: st-john-the-baptist-holy-angels-newark
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2169/2026-10-25.pdf
    seen: 2026-10-27
    quote: Sacred Heart
    note: 'Sacred Heart, Chestertown''s 25 October 2026 issue (Bonventure page 2169): its masthead names
      Sacred Heart, and its weekend Mass counts (p.4) list Sacred Heart and St. John only.'
  - url: http://sponsors.bonventure.net/pdfs/2103/2026-10-25.pdf
    seen: 2026-10-27
    quote: ST. JOHN - HOLY ANGELS PARISH
    note: 'St. John - Holy Angels, Newark''s 25 October 2026 issue (Bonventure page 2103): the page 1
      masthead names St. John - Holy Angels Parish, 82 Possum Park Road, Newark.'
---

## Publisher

Sacred Heart, Chestertown publishes one weekly bulletin for itself and its mission St. John, Rock Hall. Its site (sacredparish.org, eCatholic site 1393) carries an archive of files that stopped on 27 September 2026; the home page's 'Weekly Bulletin' link instead goes to a Bon Venture listing (sponsors.bonventure.net page 2169) whose newest file is dated 25 October 2026. The 27 September cover is headed 'SACRED HEART PARISH' with 'Rev. Jones Kukatla, Pastor' and lists the Mass times of both churches (quoted in the evidence); the 25 October footer reads 'Sacred Heart / St. John, Chestertown'.

## Worship sites

- Sacred Heart, 508 High Street, Chestertown: Saturday 4:00 pm, Sunday 10:00 am, weekdays 8:30 am (Monday and Saturday only during November, Advent and Lent).
- St. John the Evangelist, Rock Hall: Sunday 8:00 am, Thursday 8:30 am. The summer guide calls it 'mission of Sacred Heart, Chestertown, MD'; the home page says 'One Parish - Two Churches'.

See `churches/sacred-heart-chestertown.md` and `churches/st-john-the-evangelist-rock-hall.md`.

## Website and bulletin provider

`other`, pinned to the Bon Venture page, as the playbook records for Bonventure hosts (use the http:// form; the https host fails TLS verification from Python). It is not `ecatholic` because the eCatholic archive is four weeks behind the current issue.

## Not yet confirmed

Page 1 of the 25 October issue is an image and was not rendered; the Mass schedule is quoted from the 27 September cover and the home page ('4:00 p.m. Vigil Mass at Sacred Heart (Saturdays); Sundays 8:00 a.m. at St. John, 10:00 a.m. at Sacred Heart').
