---
name: Princeton University Catholic Campus Ministry (Aquinas Institute), University Chapel
revisit: 'Read the Aquinas Institute''s ''GET UPDATES'' newsletter sign-up and the University Chapel''s
  own schedule page: is there a weekly bulletin or newsletter the pipeline could read, and are the Masses
  open to the public? Then exclude it as no-bulletin (public Mass, nothing to read) or add a parish row
  if a readable weekly schedule exists.'
revisit_after: 2027-01-31
roster: []
evidence:
- url: https://princetoncatholic.org/current-students/mass-and-confession/daily-mass-confession-adoration/
  seen: 2026-10-30
  quote: Our worship schedule follows Princeton University’s academic calendar. When school’s in session,
    so are Mass and confession!
  note: 'Read with visit.py (plain probe url got no answer). ''2026-2027 Schedule'': Daily Mass Monday-Friday,
    12pm; Sunday Mass 4:30 and 10pm; ''All in University Chapel''. The page sits under ''Current Students''.'
- url: https://princetoncatholic.org
  seen: 2026-10-30
  quote: (609) 924-1820 | 134 Nassau St. | Princeton, NJ, 08542
  note: 'Homepage read with visit.py --text: 134 Nassau St. is the Aquinas Institute''s own building (office);
    visit.py found no bulletin link on the homepage.'
parish: st-paul-princeton
line1: Princeton University Chapel
city: Princeton
state: NJ
postal_code: 08544
research:
- method: probe url, then visit.py --text and --links (Mass-times pages)
  url: https://princetoncatholic.org
  checked: '2026-10-30'
  outcome: not-found
  next_action: Check the 'GET UPDATES' sign-up for a weekly newsletter archive and whether the University
    Chapel Masses are public; decide no-bulletin exclusion or parish row.
  retry_when: Revisit date, or the owner decides whether campus ministries with term-time Mass count as
    worship sites
  revisit_after: 2027-01-31
---

## What is known

The Aquinas Institute is the Catholic campus ministry at Princeton University (134 Nassau St., Princeton, its office). Its 2026-2027 schedule page (read 2026-10-30) lists daily Mass Monday-Friday at 12pm and Sunday Mass at 4:30 and 10pm, 'All in University Chapel', following the university's academic calendar. St. Paul, Princeton's bulletin advertises it ('Mass & confession on campus') but doesn't print its schedule, so it isn't a church of that row. Neither the diocese's finder nor GCatholic lists it, so it moves no coverage figure. The batches carried it over from earlier jobs as a lead, and reconcile read the site on 2026-10-30.

## Why it is not decided

The Masses are said in the university's interdenominational chapel during term, and the schedule page sits under 'Current Students'. Nothing read says whether they are open to the public, and the homepage shows no bulletin, only a newsletter sign-up ('GET UPDATES') that wasn't read. A place with public Mass and nothing readable would be excluded as no-bulletin (README, Settled policy 4); a readable weekly schedule would make it a parish row of its own. Neither is established, so it stays here. The address line is the chapel's name, since its street address wasn't confirmed.
