---
name: St. Anthony of Padua, Bronx
website: https://sapbronx.com/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:11125']
group: ''
evidence:
- url: https://sapbronx.com/bulletins
  seen: 2026-11-08
  quote: Bulletin ARCHIVE 2018 April 1, 2018
  note: 'eCatholic bulletin archive (site 11125) read in headed Chrome: the newest issue is 1 April 2018
    (files.ecatholic.com/11125/bulletins/20180401.pdf).'
- url: https://sapbronx.com/
  seen: 2026-11-08
  quote: MASS TIMES SUNDAY 8:30 AM English 10:30 AM Spanish Spanish 12:30 PM English 3:00 PM Spanish
  note: Home page Mass schedule; the home page links no bulletin.
research:
- method: visit.py --bulletin on sapbronx.com and its /bulletins archive
  url: https://sapbronx.com/bulletins
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-read the archive; if 2026 issues appear, set bulletin_provider ecatholic and run fetch:check
  retry_when: The archive lists an issue dated after 1 April 2018, or the home page links a bulletin
  revisit_after: 2027-02-01
- method: issues.py discovermass st-anthony-of-padua-bronx-ny ('no bulletins available'); probe po st-anthony-of-padua-church-10459
    (org exists, no publications)
  url: https://parishesonline.com/organization/st-anthony-of-padua-church-10459
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-run probe po and issues.py discovermass
  retry_when: The parish site links either publisher
bulletin_status: not-found
---

## Publisher

St. Anthony of Padua (832 E. 166th St.) has an eCatholic site (11125) whose bulletin archive stops at 1 April 2018, and its home page links no bulletin. Discover Mass lists the church with 'no bulletins available', and ParishesOnline has a directory org for it with no publications (all checked 8 November 2026). No current bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, St. Anthony of Padua, 832 E 166th St (corner of Prospect Ave.). The home page gives Sunday 8:30 AM, 10:30 AM (Spanish), 12:30 PM and 3:00 PM (Spanish, September-June), Saturday 5:00 PM vigil (Spanish), weekday 7:00 PM (Spanish) in the church and Tuesday-Friday 9:00 AM in the 'Centro Chapel', a chapel at the parish, not a separate worship site. This is not St. Anthony on Mansion Street or Richardson Avenue.

## Website and bulletin provider

`no_bulletin`; the website is the eCatholic archive, so an upload there is the first thing to check.

## Not yet confirmed

Whether the parish prints a bulletin it does not post. It runs an email list ('Join Our E-Mail List'), which may carry announcements.
