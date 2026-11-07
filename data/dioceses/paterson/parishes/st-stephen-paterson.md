---
name: St. Stephen
website: https://saintstephensparish.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:33773']
group: ''
evidence:
- url: https://saintstephensparish.com/bulletins
  seen: 2026-11-05
  note: 'Read with parish-site-access visit.py (probe url reads the home page too: eCatholic site 33773).
    The ''Boletín'' page''s newest links are files.ecatholic.com/33773/bulletins/20260621.pdf, 20260620.pdf
    and 20260619.pdf (labelled June 21, 20 and 19, 2026), then June 5-7 and May 10-12, 2026, then 7 December
    2025 back to 8 November 2025: nothing after 21 June 2026.'
- url: https://files.ecatholic.com/33773/bulletins/20260619.pdf
  seen: 2026-11-05
  quote: 86 Martin Street,  Paterson, New Jersey  07501
  note: 'English edition labelled June 19, 2026 (2 pages): masthead ''ST. STEPHEN''S ROMAN CATHOLIC CHURCH'',
    ''Rev. Fr. Diego Monsalve, Pastor''; Mass schedule Saturday vigil 5:00 PM English and 7:00 PM Spanish,
    Sunday 8:00 AM Spanish, 10:00 AM Polish, 12:00 PM and 2:00 PM Spanish, Monday to Friday 7:00 PM Spanish.
    20260620.pdf is the Polish and 20260621.pdf the Spanish edition of the same week (weekend collection
    of 13-14 June).'
- url: https://saintstephensparish.com/
  seen: 2026-11-05
  quote: -10:00AM (POLISH)
  note: 'Home page (visit.py) ''HORARIO DE MISA'': Sábado 5:00PM English, 7:00PM Español; Domingo 8:00AM
    Español, 10:00AM Polish, 12:00PM and 2:00PM Español; weekdays 7:00PM Español. Office telephone 973-742-2822.'
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: Finder pin directory:33773 "Saint Stephen's Roman Catholic Church", Paterson, no street address
    or coordinates, website https://saintstephensparish.com/; Sunday 8:00 AM Spanish, 10:00 AM Polish,
    12:00 PM and 2:00 PM Spanish, Saturday 5:00 PM English.
revisit: Reopen https://saintstephensparish.com/bulletins with visit.py and run issues.py ecatholic ecatholic:33773
  (also --day sat and --day fri, the Polish and English editions' dates); if weekly issues have resumed,
  set provider ecatholic and run fetch:check.
revisit_after: 2027-01-15
research:
- method: visit.py on the eCatholic /bulletins page, then issues.py ecatholic ecatholic:33773 for 20 weeks
    (Sunday, --day sat and --day fri names)
  url: https://saintstephensparish.com/bulletins
  checked: '2026-11-05'
  outcome: not-found
  next_action: Rerun visit.py on /bulletins and issues.py ecatholic ecatholic:33773 (Sunday, sat, fri);
    look at the parish Facebook page 'San Esteban RC' and Instagram 'sanestebanrc' for a posted bulletin
  retry_when: The /bulletins page lists an issue dated after 21 June 2026
  revisit_after: 2027-01-15
bulletin_status: not-found
---

## Publisher

St. Stephen, Paterson published its own weekly bulletin on its eCatholic site (site 33773, the finder pin id) in three language editions a week, each a dated file: the week of 21 June 2026 is `20260619.pdf` (English), `20260620.pdf` (Polish) and `20260621.pdf` (Spanish). The English edition's masthead reads "ST. STEPHEN'S ROMAN CATHOLIC CHURCH", "86 Martin Street, Paterson, New Jersey 07501", "Rev. Fr. Diego Monsalve, Pastor". Nothing has been posted since: the Boletín page (visit.py, 2026-11-05) lists 21 June 2026 as its newest file, and `issues.py ecatholic ecatholic:33773` found no Sunday-, Saturday- or Friday-dated file for the 20 weeks back from 8 November 2026 (403 each, meaning never posted). The archive is irregular before that too (May 10-12, June 5-7, June 19-21 2026, then back to December 2025). So the row is `no_bulletin` for now, with a revisit.

## Worship sites

One church, `st-stephen-paterson` (86 Martin Street). The June 2026 English edition's schedule and the parish home page (read 2026-11-05) give Saturday 5:00 PM English and 7:00 PM Spanish, Sunday 8:00 AM Spanish, 10:00 AM Polish, 12:00 PM and 2:00 PM Spanish, and weekdays 7:00 PM Spanish, all with no other place named. The finder (directory:33773, no address) and GCatholic (19051) list this one church.

## Website and bulletin provider

`https://saintstephensparish.com/`, eCatholic site 33773 (probe url reads it). Provider `no_bulletin` until issues resume (Settled policy 4: kept in the records, left off the site); `ecatholic:33773` is kept. If they resume as three language editions dated Friday, Saturday and Sunday, check which file fetch picks before setting provider `ecatholic`.

## Not yet confirmed

- Whether the parish posts its bulletin anywhere else (its Facebook page 'San Esteban RC' or Instagram 'sanestebanrc', not read). Revisit after 2027-01-15.
