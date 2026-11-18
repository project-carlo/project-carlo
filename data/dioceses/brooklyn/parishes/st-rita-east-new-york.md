---
name: St. Rita
website: https://saintritabrooklyn.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://saintritabrooklyn.org/bulletins']
group: Deanery B6 (Brooklyn East)
evidence:
- url: https://saintritabrooklyn.org/bulletins
  seen: 2026-11-06
  quote: Bulletin for Sunday, Apr 02, 2023
  note: 'Tilma bulletins page, newest card first: ''Bulletin for Sunday, Apr 02, 2023'', then Mar 26,
    Mar 19, Mar 12, Mar 05, Feb 26, Feb 19 (2023). The tokens decode to one upload on 2023/03/29; nothing
    since.'
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjMvMDMvMjkvMXhuZzEwcWI0NV9XRUVLTFlfQlVMTEVUSU5fVVBEQVRFRF9BUFJJTF8yXzIwMjMucGRmIl1d/WEEKLY%20BULLETIN%20UPDATED%20APRIL%202%2C%202023.pdf
  seen: 2026-11-06
  quote: St. Rita’s R.C. Church
  note: 'Newest posted issue, 2 April 2023 (4 pages, self-made, no LPi container number, John Patrick
    or Church Bulletin Inc. mark): page 1 ''St. Rita’s R.C. Church MASS SCHEDULE'' for the one church
    (weekdays 9:30am Spanish, Saturdays 6pm Spanish, Sundays 9am English & 11am Spanish).'
- url: https://parishesonline.com/organization/st-rita-church-11208
  seen: 2026-11-06
  note: 'probe po: org ''St. Rita Church'', 275 Shepherd Ave, Brooklyn 11208, has no issues (empty org,
    not a publication). st-ritas-church-11208, st-rita-roman-catholic-church-11208, saint-rita-church-11208,
    st-rita-church-brooklyn and st-rita-brooklyn don''t exist.'
- url: https://discovermass.com/church/st-rita-brooklyn-ny/
  seen: 2026-11-06
  quote: no bulletins available
  note: Discover Mass lists no bulletins and links the old website stritabrooklyn.com/index.htm, which
    probe url now reports SPAM-SQUAT ('Best Online Casinos USA 2026'); GCatholic 16771 links the same
    old domain.
revisit: Check the Tilma /bulletins page for a card newer than 2 April 2023 and the parish Facebook page
  for bulletins; if current, set other with page-pdfs https://saintritabrooklyn.org/bulletins and run
  fetch:check.
revisit_after: 2027-02-06
research:
- method: Read the Tilma /bulletins page and homepage; probe po st-rita-church-11208 and slug variants;
    Discover Mass church page; probe url on the GCatholic/Discover Mass website; fetch:check with page-pdfs
    on /bulletins
  url: https://saintritabrooklyn.org/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: Reread /bulletins for a card newer than 2 April 2023, probe po st-rita-church-11208 for
    issues, and read the parish Facebook page (facebook.com/StRitas-RC-Church-150126588356971) for posted
    bulletins; if the Tilma page is current again, set bulletin_provider other with recipe page-pdfs https://saintritabrooklyn.org/bulletins
    and run fetch:check (on 2026-11-06 it picked the 2 April 2023 issue, stale, 1314 days).
  retry_when: After 2027-02-06, or when the parish site shows a new bulletin card
  revisit_after: 2027-02-06
bulletin_status: not-found
---

## Publisher

The parish once self-published a weekly bulletin on its Tilma site, but the newest card on `/bulletins` (read 2026-11-06) is "Bulletin for Sunday, Apr 02, 2023", from a single batch uploaded 2023-03-29: nothing in three and a half years. That issue (4 pages, no publisher mark) has the masthead "St. Rita’s R.C. Church" and a MASS SCHEDULE for the one church.

## Worship sites

One church, St. Rita, 275 Shepherd Avenue. The site's current Mass Times page (read 2026-11-06) lists weekdays 9:30am, Saturday 7:00 pm Spanish vigil, Sunday 9:00 am English and 11:00 am Spanish, for that church alone; the diocese's directory, deanery list, Mass finder and GCatholic list no other site for it.

## Website and bulletin provider

`no_bulletin`: `fetch:check` with `page-pdfs https://saintritabrooklyn.org/bulletins` (2026-11-06) picked the 2 April 2023 issue, stale by 1314 days. ParishesOnline has an empty org (`st-rita-church-11208`), Discover Mass lists no bulletins, and the old domain stritabrooklyn.com (still linked by GCatholic and Discover Mass) is now a casino spam squat. If issues are posted again, the row is `other` with that recipe (see research).

## Not yet confirmed

Whether the parish prints a bulletin it doesn't post, or posts one on Facebook (not read): recheck after 2027-02-06.
