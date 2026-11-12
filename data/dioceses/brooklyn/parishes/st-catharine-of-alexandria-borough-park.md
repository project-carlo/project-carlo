---
name: St. Catharine of Alexandria (Borough Park)
website: https://stcatharineofalexandria-brooklyn.org/
bulletin_provider: other
provider_id: page-pdfs https://stcatharineofalexandria-brooklyn.org/bulletins
publication: []
group: Deanery B8 (Brooklyn West)
evidence:
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMjgvMnB3eWNkeTJmdF9DYXRoQWxleDEwXzI1LnBkZiJdXQ/CathAlex10-25.pdf
  seen: 2026-11-06
  note: '25 October 2026 issue (Thirtieth Sunday in Ordinary Time), 6 pages; pages 1-4 are images (read
    rendered). Page 1 masthead: St. Catharine of Alexandria RC Church, 1119 41st Street, Brooklyn, New
    York 11218; Pastor Rev. Jose Agustin Orellana. Weekend Mass: Saturday Vigil 5pm (Bilingual); Sunday
    8:30am (English), 10:00am and 11:30am (Spanish). Weekday: Monday-Saturday 8:30am (Bilingual), Wednesday
    and Friday 7pm (Spanish). No other church or chapel is named.'
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMjgvMnB3eWNkeTJmdF9DYXRoQWxleDEwXzI1LnBkZiJdXQ/CathAlex10-25.pdf
  seen: 2026-11-06
  quote: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON, NY 11704-1104
  note: 'Page 6 ad-page footer ''#178'': printed by The Church Bulletin Inc., not LPi; no ParishesOnline
    container.'
- url: https://stcatharineofalexandria-brooklyn.org/bulletins
  seen: 2026-11-06
  quote: Bulletin for Sunday, October 25, 2026
  note: 'Tilma bulletins page, server-rendered, newest first: October 25, October 18, October 11 (all
    three files uploaded 2026-10-28 per their resource tokens), then October 4 (uploaded 2026-10-02).
    The 1 November issue was not yet posted on 2026-11-06.'
revisit: Rerun fetch:check and confirm it picks the 15 November 2026 issue or later (the newest posted
  on 2026-11-12 was older than 8 November).
revisit_after: 2026-11-17
research:
- method: probe po on st-catharine-of-alexandria-church-11218, st-catharine-church-11218, st-catharine-of-alexandria-roman-catholic-church-11218
  checked: '2026-11-06'
  outcome: not-found
  next_action: None needed while the Tilma page posts Church Bulletin Inc. issues
  retry_when: The Tilma page stops posting new issues
- method: 'fetch:check (headed Chrome) on recipe page-pdfs https://stcatharineofalexandria-brooklyn.org/bulletins:
    picked CathAlex10-25.pdf, first-listed, dated 2026-10-25, freshness fresh (12 days)'
  url: https://stcatharineofalexandria-brooklyn.org/bulletins
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check and confirm it picks a November 2026 issue; the parish uploads issues
    in batches (three on 2026-10-28)
  retry_when: A November 2026 card appears
  revisit_after: 2026-11-16
- method: 'Reconcile: headed fetch:check of every Brooklyn row picked the issue dated 2026-10-25; the
    bulletin page lists no newer issue than the one picked'
  url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMjgvMnB3eWNkeTJmdF9DYXRoQWxleDEwXzI1LnBkZiJdXQ/CathAlex10-25.pdf
  checked: '2026-11-12'
  outcome: not-found
  next_action: Rerun fetch:check and confirm it picks the 15 November 2026 issue or later
  retry_when: After the weekend of 14-15 November 2026
bulletin_status: available
---

## Publisher

St. Catharine of Alexandria, Borough Park publishes its own weekly bulletin, printed by The Church Bulletin Inc. (West Babylon; ad-page footer "#178") and posted as PDFs on the parish's Tilma site. The 25 October 2026 issue (read 2026-11-06, 6 pages, pages 1-4 images read rendered) has the masthead "St. Catharine of Alexandria RC Church, 1119 41st Street, Brooklyn, New York 11218" on page 1, with Rev. José Agustín Orellana, Pastor.

## Worship sites

One. The page 1 schedule lists Saturday Vigil 5pm (Bilingual), Sunday 8:30am (English), 10:00am and 11:30am (Spanish), Monday-Saturday 8:30am (Bilingual) and Wednesday and Friday 7pm (Spanish), with no other church or chapel. The directory, the deanery list, GCatholic 16693 and Mass finder 789 all give the one church at 1119 41st Street.

## Website and bulletin provider

`other`, recipe `page-pdfs https://stcatharineofalexandria-brooklyn.org/bulletins` (the Tilma bulletins page, newest first). There is no publication id: The Church Bulletin Inc. has no online container, and `probe po` found no ParishesOnline org under the usual slugs. Pages 1-4 of the issue are images with no text layer, so the Mass schedule must be read as an image.

## Not yet confirmed

On 2026-11-06 the newest card was 25 October 2026; the 1 November issue was not yet posted. The parish uploads in batches (the 11, 18 and 25 October files all carry a 2026-10-28 upload stamp), so this is a posting lag, not a stop; see research.
