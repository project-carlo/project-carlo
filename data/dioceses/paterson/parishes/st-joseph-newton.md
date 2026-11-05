---
name: St. Joseph
website: https://stjosephnewton.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:11734']
group: ''
evidence:
- url: https://files.ecatholic.com/11734/bulletins/20261101.pdf
  seen: 2026-11-04
  quote: 24 Halsted Street - Newton - New Jersey - 07860 - www.stjosephnewton.org
  note: 'Page 1 of the 1 November 2026 issue (8 pages; ''Solemnity of All Saints - November 1, 2026''):
    masthead ''Saint Joseph Catholic Church''; Weekend Masses Saturday (Sunday Vigil) 5:00pm, Sunday 8:00am,
    9:30am and 11:30am; Weekday Masses Monday-Friday 12:15pm. Page 2: ''Father ST Sutton, Pastor''.'
- url: https://stjosephnewton.org/bulletins
  seen: 2026-11-04
  note: Read with visit.py (probe get answers 403). Lists weekly files.ecatholic.com/11734/bulletins/<YYYYMMDD>.pdf
    issues, newest 'November 1, 2026', then October 25, 18, 11, 4 and every Sunday back to June 28.
- url: https://stjosephnewton.org/
  seen: 2026-11-04
  note: 'probe url: status 200, title ''Saint Joseph, Newton - Newton, New Jeresey'', publication ecatholic:11734;
    it also links copies of the same issues under files.ecatholic.com/11734/documents/2026/10/. Finder
    pin directory:11734 gives this website.'
bulletin_status: available
---

## Publisher

St. Joseph, Newton publishes its own weekly bulletin on its eCatholic site (id 11734). The 1 November 2026 issue (`https://files.ecatholic.com/11734/bulletins/20261101.pdf`, read 2026-11-04) is headed "Saint Joseph Catholic Church, 24 Halsted Street - Newton - New Jersey", with "Father ST Sutton, Pastor" on page 2, and names no other parish.

## Worship sites

- `st-joseph-newton`: page 1's Weekend Masses, Saturday (Sunday Vigil) 5:00pm, Sunday 8:00am, 9:30am and 11:30am; weekdays Monday-Friday 12:15pm.

A grep of the issue for Chapel and Abbey found no other place of Mass. St. Paul's Abbey, Newton (GCatholic 39141), a Benedictine monastery in the same town, is not in this bulletin; it has its own record (`excluded/st-pauls-abbey-newton`, open with public Mass but no bulletin). The finder (directory:11734) and GCatholic (19029) list this one church.

## Website and bulletin provider

`stjosephnewton.org` is the eCatholic site (id 11734, finder pin 11734); probe url reads its home page (200) but its `/bulletins` page answers 403, so it was read with visit.py on 2026-11-04: weekly `files.ecatholic.com/11734/bulletins/<YYYYMMDD>.pdf` issues, newest 20261101. Provider `ecatholic`. `fetch:check` on 2026-11-04 picked `https://files.ecatholic.com/11734/bulletins/20261101.pdf` (the 1 November 2026 issue, 3 days old: fresh). It reports identity unverified ("No expected identity supplied", as for every eCatholic row); page 1 was checked by hand above.

## Not yet confirmed

Nothing open.
