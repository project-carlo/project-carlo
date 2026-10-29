---
name: St. Rocco Parish
website: https://www.stroccochurch.org/schedule.jsp
bulletin_provider: other
provider_id: page-pdfs https://www.stroccochurch.org/schedule.jsp
publication: ['url:https://www.stroccochurch.org/schedule.jsp']
group: ''
evidence:
- url: https://www.stroccochurch.org/src/en/pdfs/b20261018.pdf
  seen: 2026-10-28
  quote: Misión Santa María, Madre de Dios
  note: 'Page 1 of the 18 October 2026 issue (Spanish, 8 pages, text layer on pages 1-4): masthead names
    ''Saint Rocco Parish / Parroquia San Roque, Hispanic National Catholic Parish, 313 Sunny Dell Road,
    Avondale, PA 19311'' and ''Oficinas Parroquiales: Saint Rocco Center, 9016 Gap Newport Pike''. ''Celebración
    de las Misas'': Saturday vigil 6:00 PM; Sundays 8:45 AM (Bilingüe), 10:00 AM, 11:30 AM, 4:00 PM, 6:00
    PM, and ''2:00 PM (Sagrado Corazón, Oxford)''; weekdays Monday to Friday 12:00 PM and 6:30 PM. Page
    2 lists Msgr. Francis J. Depman as Párroco and a Vicario Parroquial.'
- url: https://www.stroccochurch.org/schedule.jsp
  seen: 2026-10-28
  quote: Schedules and Bulletins
  note: The parish's own page (reached in Chrome from the home page's 'Schedules and Bulletins' menu item;
    the home page is plain HTML with no links in its source) links `/src/en/pdfs/b20261018.pdf`, `b20261011.pdf`,
    `b2026104.pdf` and `b20260927.pdf`, newest first. The newest is 18 October 2026; `b20261025.pdf` answered
    404 on 2026-10-28. The site hosts its own PDFs; no John Patrick listing exists for St. Rocco (raw/jppc-pa.json
    has no Avondale listing but St. Gabriel's, 247).
- url: https://archphila.org/parish/st-rocco-avondale/
  seen: 2026-10-28
  note: 'Directory page (updated 2 years ago): ''333 Sunny Dell Rd. (For mail, please send to: 9016 Gap
    Newport Pike)''; pastor Msgr. Francis J. Depman, ''In residence at Assumption B.V.M., West Grove'';
    Mass times agree with the bulletin; ''Donation Center: Mision Santa Maria, Madre de Dios, 29 Gap Newport
    Pike''.'
promoted: 2026-10-29
research:
- method: pnpm fetch:check --diocese philadelphia (page-pdfs on schedule.jsp) and probe get of b20261025.pdf
    / b20261101.pdf
  url: https://www.stroccochurch.org/schedule.jsp
  checked: '2026-10-29'
  outcome: not-found
  next_action: Rerun pnpm fetch:check --diocese philadelphia --parish st-rocco-avondale and confirm it
    picks an issue dated within a week; if the site stays two or more weeks behind, record it as a late
    publisher
  retry_when: After Sunday 1 November 2026, when the 25 October or 1 November file should be posted
  revisit_after: 2026-11-03
---

## Publisher

St. Rocco, 'Hispanic National Catholic Parish', publishes its own weekly bulletin, in Spanish, as PDFs on its own site. The 18 October 2026 issue (page 1) names Saint Rocco Parish at 313 Sunny Dell Road, Avondale and its Mass schedule; it is the newest posted on 2026-10-28.

## Worship sites

The bulletin's Mass schedule covers St. Rocco Church (Avondale) and, every Sunday at 2:00 PM, the Sacred Heart church in Oxford ('Misa, en la Iglesia del Sagrado Corazón, en Oxford, a las 2:00 PM', page 3 calendar). Sacred Heart, Oxford is a parish with its own bulletin and row (`sacred-heart-oxford`): its 25 October 2026 issue prints '2:00 PM (Spanish)' in its own weekend schedule, so the Oxford church is its row's church and St. Rocco's schedule is a second listing of the same Mass, not a second site of this row.

**Mision Santa Maria, Madre de Dios, 29 Gap Newport Pike** (directory entry `mision-santa-maria-madre-de-dios-avondale`) is not a worship site: the bulletin masthead prints 'Centro de Las Donaciones: Misión Santa María, Madre de Dios, "The Avondale Center", 29 Gap Newport Pike, Avondale' and the weekly calendar puts catechism, RCIA and prayer circles 'en el Centro' while every Mass is 'en la Iglesia' or at Sacred Heart. See `excluded/mision-santa-maria-madre-de-dios-avondale`.

## Website and bulletin provider

`www.stroccochurch.org` is a hand-built site (`probe url`: ok, no publication ids, no links in the home page source). Its Schedules and Bulletins page lists the PDFs; the row is `other` with a `page-pdfs` recipe on that page. Spanish version: iglesiasanroque.org.

## Not yet confirmed

The site posts late. Reconcile's fetch check on 2026-10-29 picked `b20261018.pdf` (18 October 2026, page 1 names Saint Rocco Parish), still the newest file on the Schedules page; `b20261025.pdf` and `b20261101.pdf` both answered 404. Transport, document type and parish identity are fine; freshness is one week behind (within the 14-day threshold). See `research` for the retry.
