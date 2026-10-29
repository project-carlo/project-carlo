---
name: St. Timothy and St. Bartholomew Parish
website: https://www.st-tims.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-roman-catholic-church-of-saint-timothy-and-saint-bartholomew-philadelphia-pa-19149
publication: ['url:https://www.church-bulletin.org/the-roman-catholic-church-of-saint-timothy-and-saint-bartholomew-philadelphia-pa-19149']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/the-roman-catholic-church-of-saint-timothy-and-saint-bartholomew-philadelphia-pa-19149/2026-10-25.pdf
  seen: 2026-10-29
  quote: St. Bartholomew & St. Timothy Parish Office
  note: '25 October 2026 issue (12 pages, text layer). Page 1 masthead has two columns, ''THE CHURCH OF
    SAINT TIMOTHY, Founded 1928'' and ''THE CHURCH OF SAINT BARTHOLOMEW, Founded 1919'', over one parish
    office (3001-3033 Levick Street, 215-624-6188) and one clergy list (Rev. Francis P. Foley, Pastor).
    One combined Mass box: Saint Timothy 4:00 pm vigil, Sunday 8:00 and 11:30 am, daily Tue-Sat 8:30 am;
    St. Bartholomew Sunday 10:00 am; Holy Day Masses at St. Timothy. Page 2 onward gives separate Mass
    intentions, sanctuary candles and collections for each church.'
- url: https://www.church-bulletin.org/the-roman-catholic-church-of-saint-timothy-and-saint-bartholomew-philadelphia-pa-19149
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 116, 'The Roman Catholic Church of Saint Timothy and Saint Bartholomew',
    Philadelphia, PA 19149; latest edition October 25, 2026, then 2026-10-18 and 2026-10-11. St. Bartholomew's
    own listing 73 (Saint Bartholomew Catholic Church, 19124) has no editions.
- url: https://www.st-tims.org/bulletins
  seen: 2026-10-29
  note: 'probe url on www.st-tims.org answered HTTP 403; opened in Chrome (visit.py): 200, ''St. Timothy
    Parish | Philadelphia, PA'', links church-bulletin.org/?id=116 and the jppc 116template.pdf, and embeds
    ecatholic:22681. Its /bulletins archive lists files.ecatholic.com/22681/bulletins/<yyyymmdd>.pdf with
    newest 20250329, so the archive stopped in March 2025 and is not the channel.'
- url: https://archphila.org/parish/st-bartholomew-philadelphia/
  seen: 2026-10-28
  quote: Rev. Francis P. Foley (Parochial Administrator) in residence at Saint Timothy, Philadelphia
  note: 'Directory page for St. Bartholomew: website https://www.st-tims.org/, Mass ''Sundays, 10:00 AM.
    Holy Days: Celebrated at St. Timothy Church.'' St. Timothy''s page names Rev. Francis P. Foley as
    Pastor, website http://www.st-tims.org.'
promoted: 2026-10-29
research:
- method: Read listing 116 and its 25 October text layer; opened st-tims.org and its /bulletins archive
    in Chrome; checked listing 73
  url: https://www.church-bulletin.org/the-roman-catholic-church-of-saint-timothy-and-saint-bartholomew-philadelphia-pa-19149
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

St. Timothy and St. Bartholomew publish **one** bulletin: John Patrick listing 116 (`church-bulletin.org/?id=116`), whose 25 October 2026 issue has a joint masthead (two church titles side by side, one parish office, one pastor) and one combined Mass schedule. That makes one row with two churches, under the listing that has issues; St. Bartholomew's own listing 73 has none. The row is `other`, `page-pdfs` on listing 116.

The canonical status is not stated in the sources read: the directory keeps two parish pages (St. Bartholomew's names Fr. Foley as Parochial Administrator in residence at St. Timothy, St. Timothy's names him Pastor), and the bulletin says 'Pastor'. The row follows the bulletin, not the canonical form.

## Worship sites

Two: St. Timothy (Levick and Battersby Sts., 19149; upper and lower church, one site; the Chinese Mass on the first Sunday at 3 pm is at St. Timothy) and St. Bartholomew (5600 Jackson St., 19124; Sunday 10:00 am; Holy Day Masses are at St. Timothy). St. Timothy's lower church is a room of the same building, not a church row.

## Website and bulletin provider

st-tims.org is the parish's own eCatholic site (22681), 403 to `probe url`, loads in Chrome. Its `/bulletins` archive stops in March 2025, so the listing is the channel. Recipe `page-pdfs https://www.church-bulletin.org/the-roman-catholic-church-of-saint-timothy-and-saint-bartholomew-philadelphia-pa-19149`.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (date inferred from the listing file name); identity `unverified` because the check is given no expected identity (masthead and Mass schedule read above). It printed no `recipe` line, as the pinned `provider_id` already holds it.
