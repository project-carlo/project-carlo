---
name: Our Lady of Victory Parish, State College
website: https://ourladyofvictory.com/bulletin-archive/
bulletin_provider: other
provider_id: dated-post https://ourladyofvictory.com/bulletin-archive/
publication: ['url:https://ourladyofvictory.com/bulletin-archive/']
group: ''
evidence:
- url: https://ourladyofvictory.com/wp-content/uploads/2026/10/October-18-2026.pdf
  seen: 2026-10-21
  quote: 820 Westerly Parkway, State College, PA 16801
  note: 'Page 1 of the 17-18 Oct 2026 issue (7 pages, text layer): masthead "Our Lady of Victory Catholic
    Church", MASS SCHEDULE "Saturday: 5:00pm (Vigil)", "Sunday: 7:30am, 9:30am, 11:30am", weekday Masses
    Mon-Fri 8:00am, Thu 6:30pm, Sat 9:00am. Page 2 names Pastor Fr. George Jakopac and Fr. Ralph Mensah.
    It names this church alone: no other Mass site. A grep for Penn State, Pasquerilla and Nittany finds
    only "Mount Nittany Medical Center".'
- url: https://ourladyofvictory.com/bulletin-archive/
  seen: 2026-10-21
  quote: Below you will find an archive of all of the OLV Church Bulletins going back multiple years.
  note: 'WordPress archive page: one child post per week (october-18-2026, october-11-2026, october-4-2026,
    ...), each embedding wp-content/uploads/2026/10/<Month>-<D>-2026.pdf. `fetch:check` read it with the
    dated-post collector, "current", 2026-10-18.'
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'Directory: Our Lady of Victory Parish, State College, 820 Westerly Parkway 16801, homepage ourladyofvictory.com;
    Masses Sat 9:00 AM and 5:00 PM, Sun 7:30, 9:30 and 11:30 AM, Mon-Wed 8:00 AM, Thu 8:00 AM and 6:30
    PM, Fri 8:00 AM. Agrees with the bulletin.'
promoted: 2026-10-21
---

## Publisher

Our Lady of Victory publishes its own weekly bulletin as a PDF on its WordPress site, one post per issue under `/bulletin-archive/`. The 17-18 October 2026 issue (read 2026-10-21) is headed "Our Lady of Victory Catholic Church, 820 Westerly Parkway, State College" and gives only this church's Masses. Fr. George Jakopac is pastor. It is a self-hosted bulletin (`other`, `dated-post` recipe on the archive page).

## Worship sites

One church: Our Lady of Victory, 820 Westerly Parkway (directory, GCatholic and bulletin agree). The nearby Penn State campus Masses (Pasquerilla Spiritual Center) are a separate ministry with no bulletin of its own; see `excluded/penn-state-catholic-campus-ministry-university-park`. This bulletin does not list them.

## Website and bulletin provider

`provider_id: dated-post https://ourladyofvictory.com/bulletin-archive/`. `pnpm fetch:check --diocese altoona-johnstown --parish our-lady-of-victory-state-college` (2026-10-21) picked `https://ourladyofvictory.com/wp-content/uploads/2026/10/October-18-2026.pdf`, "dated-post ... current", status ok (12.7 MB). `probe url` of the bare domain found no publisher ids: the archive page is the channel. No ParishesOnline, eCatholic or Discover Mass id was embedded (the Discover Mass page `our-lady-of-victory-state-college-pa` exists but was not read as a channel).

## Not yet confirmed

Nothing outstanding.
