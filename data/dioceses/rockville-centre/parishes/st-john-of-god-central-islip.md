---
name: St. John of God
website: https://stjohnofgodparish.org/news-events/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['po-container:03/4101']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/4101/20261115B.pdf
  seen: 2026-11-13
  quote: 84 CARLETON AVENUE * CENTRAL ISLIP, NY 11722
  note: 'November 15, 2026 issue in LPi container 03/4101 (probe container, 12 pages). Page 1 masthead
    ''Saint John of God Parish / Parroquia San Juan De Dios'', one Mass schedule: Monday-Thursday 12:00pm
    (English); Tuesday and Thursday 6:45pm (Spanish); Saturday 5:00pm (English), 7:00pm (Spanish); Sunday
    8:00am, 11:15am (English), 5:00pm (Ghanaian Community), 9:30am, 1:00pm (Spanish).'
- url: https://stjohnofgodparish.org/news-events/bulletin/230-november-8-2026/file
  seen: 2026-11-13
  quote: St. John of God Parish | 03-4101
  note: 'The parish''s own copy of the November 8, 2026 issue (Solutio /file, downloaded through Chrome;
    Creator Canva): footer ''For ad info. call 1-800-950-9952 | www.4lpi.com St. John of God Parish |
    03-4101'', so LPi prints it.'
- url: https://stjohnofgodparish.org/news-events/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py: ''pdf November 8, 2026'' (230-november-8-2026/file),
    November 1, October 25 ...'
research:
- method: 'Looked for the ParishesOnline organization of container 03/4101 so fetch can read it: probe
    po on st-john-of-god-parish, st-john-of-god-11722, church-of-st-john-of-god-11722, st-john-of-god-church-11722,
    st-john-of-god-parish-11722, saint-john-of-god-parish(-11722), st-john-of-god-central-islip, st-john-of-god-catholic-church-11722,
    st-john-of-god-roman-catholic-church(-11722) (the last without zip and st-john-of-god are other dioceses''
    parishes); a web search; the site embeds no LPi id'
  url: https://container.parishesonline.com/bulletins/03/4101/20261115B.pdf
  checked: '2026-11-13'
  outcome: not-found
  next_action: Find the org slug or LPi widget id (a 4lpi.com or parishesonline.com link on the parish
    site or Facebook page, or the ParishesOnline church search in a browser), then set bulletin_provider
    parishes_online with that provider_id and run fetch:check
  retry_when: A ParishesOnline org page or LPi id for St. John of God, Central Islip turns up, or fetch
    gains a container collector
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post but failed: "No PDF
    links found on bulletin post page: .../230-november-8-2026/file" (the /file URL is the PDF and answers
    403 outside a browser). The same bulletin is in LPi container 03/4101 (20261115B.pdf live), but no
    ParishesOnline org slug for it was found, and fetch reads ParishesOnline only by org slug.'
  url: https://stjohnofgodparish.org/news-events/bulletin/230-november-8-2026/file
---

## Publisher

St. John of God, 84 Carleton Avenue, Central Islip publishes a weekly bilingual bulletin printed by LPi (footer "www.4lpi.com St. John of God Parish | 03-4101"). The November 15, 2026 issue in container 03/4101 (`https://container.parishesonline.com/bulletins/03/4101/20261115B.pdf`, read 2026-11-13) has the page 1 masthead "Saint John of God Parish / Parroquia San Juan De Dios" and one Mass schedule: Monday-Thursday 12:00pm (English); Tuesday and Thursday 6:45pm (Spanish); Saturday 5:00pm (English) and 7:00pm (Spanish); Sunday 8:00am and 11:15am (English), 9:30am and 1:00pm (Spanish), and 5:00pm for the Ghanaian community. The parish's own copy of the 8 November issue on its site carries the same footer.

## Worship sites

One: the church at 84 Carleton Avenue (`st-john-of-god-central-islip-church`); the Chapel used for Thursday adoration is part of the parish plant. The diocesan locator (directory:110), GCatholic (16825) and the Mass-times page list only this building.

## Website and bulletin provider

stjohnofgodparish.org is a Solutio (Joomla) site; its `/news-events/bulletin` list links `/news-events/bulletin/<n>-<month>-<d>-<yyyy>/file`, which answers 403 outside a browser, and fetch:check on 2026-11-13 failed on it ("No PDF links found on bulletin post page"). Following the diocese's settled rule, the printer's listing was looked for first: the LPi container 03/4101 is live, but no ParishesOnline organization for it could be found (see `research`), and fetch reads ParishesOnline only by org slug. The row is therefore `unsupported` with `fetch_gap` `joomla-file-endpoint`, keeping `po-container:03/4101`.

## Not yet confirmed

The ParishesOnline org slug and LPi id for container 03/4101. With either, set `bulletin_provider: parishes_online`, run fetch:check and clear `fetch_gap`.
