---
name: Transfiguration
website: https://transfiguration-brooklyn.org/
bulletin_provider: other
provider_id: page-pdfs https://transfiguration-brooklyn.org/bulletins
publication: ['url:https://transfiguration-brooklyn.org/bulletins']
group: Deanery B1 (Brooklyn West)
evidence:
- url: https://transfiguration-brooklyn.org/system/resources/W1siZiIsIjIwMjYvMTEvMDUvZ3BwaGFscmpjX05ld3NsZXR0ZXJfVHJhbnNmaWd1cmF0aW9uX1BhcmlzaF9Ob3ZlbWJlcl8xXzIwMjYucGRmIl1d/Newsletter%20Transfiguration%20Parish%20November%201%202026.pdf
  seen: 2026-11-07
  quote: 263 Marcy Avenue, Brooklyn, N.Y. 11211
  note: '1 November 2026 newsletter (6 pages), page 1 masthead names TRANSFIGURATION R.C. CHURCH, La Gran
    Familia, Very Rev. Jeremias E. Castillo, Pastor, ''BOLETIN PARROQUIAL | NUMERO 43'', NOVEMBER 1, 2026;
    Schedule of Masses: Monday to Friday 9:30 am Spanish, Saturday 5:30 pm Spanish, Sunday 10:00 am Spanish
    and 11:30 AM English. No LPi, John Patrick or Church Bulletin Inc. footer; self-made.'
- url: https://transfiguration-brooklyn.org/bulletins
  seen: 2026-11-07
  quote: November 01, 2026
  note: 'Tilma /bulletins cards newest first: November 01, 2026, October 25, 2026 (both uploaded 2026/11/05
    per the resource tokens), then September 06, 2026, June 07, 2026, May 24, 2026.'
revisit: Rerun fetch:check and confirm it picks the 15 November 2026 issue or later (the newest posted
  on 2026-11-12 was older than 8 November).
revisit_after: 2026-11-17
promoted: 2026-11-12
research:
- method: pnpm fetch:check with page-pdfs https://transfiguration-brooklyn.org/bulletins
  url: https://transfiguration-brooklyn.org/bulletins
  checked: '2026-11-07'
  outcome: found
  next_action: The parish posts in batches with gaps of weeks to months (6 Sep, then 25 Oct and 1 Nov
    uploaded together on 5 Nov); if fetch finds nothing newer, recheck after the usual gap before calling
    it stopped.
  revisit_after: 2026-12-15
- method: 'Reconcile: headed fetch:check of every Brooklyn row picked the issue dated 2026-11-01; the
    bulletin page lists no newer issue than the one picked'
  url: https://transfiguration-brooklyn.org/system/resources/W1siZiIsIjIwMjYvMTEvMDUvZ3BwaGFscmpjX05ld3NsZXR0ZXJfVHJhbnNmaWd1cmF0aW9uX1BhcmlzaF9Ob3ZlbWJlcl8xXzIwMjYucGRmIl1d/Newsletter%20Transfiguration%20Parish%20November%201%202026.pdf
  checked: '2026-11-12'
  outcome: not-found
  next_action: Rerun fetch:check and confirm it picks the 15 November 2026 issue or later
  retry_when: After the weekend of 14-15 November 2026
bulletin_status: available
---

## Publisher

Transfiguration publishes its own bilingual (Spanish/English) weekly newsletter as a PDF on its Tilma site, https://transfiguration-brooklyn.org/bulletins. The 1 November 2026 issue (read 2026-11-07) has the masthead "TRANSFIGURATION R.C. CHURCH", "La Gran Familia", Very Rev. Jeremías E. Castillo, J.C.L., Pastor, "BOLETÍN PARROQUIAL | NÚMERO 43", "NOVEMBER 1, 2026", and "263 Marcy Avenue, Brooklyn, N.Y. 11211". No LPi, John Patrick or Church Bulletin Inc. footer: the parish makes it itself.

## Worship sites

One church, Transfiguration, 263 Marcy Avenue. The issue's "Schedule of Masses" gives Monday to Friday 9:30 am (Spanish), Saturday 5:30 pm (Spanish), Sunday 10:00 am (Spanish) and 11:30 AM (English), with no other place named. The "Chapel" it mentions is where adult catechesis meets after the 10:00 am Mass, not a Mass site; 280 Marcy Avenue appears only as a distribution event's address. The directory, the deanery list, GCatholic 16792 and Mass finder 1091 list only 263 Marcy Avenue.

## Website and bulletin provider

`other` with the recipe `page-pdfs https://transfiguration-brooklyn.org/bulletins`. `fetch:check` on 2026-11-07 picked the 1 November 2026 issue (first-listed, dated from the file name, fresh). The site posts in batches: cards jump from 6 September to 25 October 2026, and the 25 October and 1 November files were both uploaded on 5 November (resource tokens decode to 2026/11/05). GCatholic's website transfigurationbrooklyn.org no longer resolves (probe url DEAD-DNS, 2026-11-07); the directory's transfiguration-brooklyn.org is current.

## Not yet confirmed

Nothing open; if fetch returns a stale issue, recheck after the parish's usual posting gap (research).
