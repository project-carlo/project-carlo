---
name: St. Margaret Mary, Bronx
website: https://smmbronx.com/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:25441']
group: ''
evidence:
- url: https://smmbronx.com/bulletins
  seen: 2026-11-09
  quote: Bulletin Archive 2024 November 3, 2024
  note: 'eCatholic archive (site 25441) read in headed Chrome: its only issue is 3 November 2024 (files.ecatholic.com/25441/bulletins/20241103.pdf).
    The home page links no bulletin.'
- url: https://smmbronx.com
  seen: 2026-11-09
  quote: SUNDAY 9 AM Español 11 AM English 12:30 PM Español
  note: Home page Mass schedule, with special Masses dated November and December 2026; it is kept current.
research:
- method: visit.py --bulletin and --links on smmbronx.com and /bulletins; issues.py ecatholic ecatholic:25441
    over 10 Sundays to 8 November 2026
  url: https://smmbronx.com/bulletins
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-read the archive and home page; if weekly issues appear, set bulletin_provider ecatholic
    and run fetch:check
  retry_when: The archive lists an issue dated after 3 November 2024
  revisit_after: 2027-02-01
- method: probe po st-margaret-mary-church-10453 (org exists, 110 East Tremont Avenue, no publications);
    issues.py discovermass st-margaret-mary-bronx-ny ('no bulletins available')
  url: https://parishesonline.com/organization/st-margaret-mary-church-10453
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-run probe po
  retry_when: The parish site links another publisher
bulletin_status: not-found
---

## Publisher

St. Margaret Mary has an eCatholic site (25441) whose bulletin archive holds a single issue, 3 November 2024; the home page carries a detailed, current schedule instead (special Masses dated to December 2026) and links no bulletin. ParishesOnline has a directory org with no publications and Discover Mass lists no bulletins (8-9 November 2026). No current bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, St. Margaret Mary, at Morris Avenue and East Tremont Avenue: Saturday 6:30 PM (Spanish), Sunday 9 AM (Spanish), 11 AM (English), 12:30 PM (Spanish), weekday Masses and monthly special Masses, per the home page read 9 November 2026.

## Website and bulletin provider

`no_bulletin`; the website is the eCatholic archive. The home page's schedule is HTML only, not a bulletin.

## Not yet confirmed

Whether the parish prints a bulletin; its Flocknote and WhatsApp channels were not readable as a public bulletin.
