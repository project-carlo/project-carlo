---
name: Saint Joseph Parish, Bellwood
website: https://saintjosephbellwood.org
bulletin_provider: ecatholic
provider_id: '40290'
publication: ['ecatholic:40290']
group: ''
evidence:
- url: https://files.ecatholic.com/40290/bulletins/20261018.pdf
  seen: 2026-10-21
  quote: 'MASS SCHEDULE & INTENTIONS: OCT 17-OCT 25, 2026'
  note: Issue dated "OCT 18, 2026" (2 pages, text layer), masthead "623 E. Third Street, Bellwood, PA
    16617 www.saintjosephbellwood.org ... SAINT JOSEPH CATHOLIC CHURCH". It lists Masses for St. Joseph
    only (Sat 4:00 PM, Sun 9:00 AM, Mon 8:00 AM, Tue 6:00 PM, Wed 7:30 AM Holy Hour) and names no other
    parish or church.
- url: https://saintjosephbellwood.org/bulletins
  seen: 2026-10-21
  note: eCatholic site id 40290 (found by headed Chrome visit.py on the home page; curl and probe url
    get a Cloudflare 403). The /bulletins page links files.ecatholic.com/40290/bulletins/<YYYYMMDD>.pdf,
    dated by the Sunday (20261018.pdf).
- url: https://discovermass.com/church/st-joseph-bellwood-pa/
  seen: 2026-10-21
  quote: no bulletins available for St. Joseph.
  note: 'A Discover Mass page exists for the church but carries no bulletin: not a live channel.'
promoted: 2026-10-21
---

## Publisher

St. Joseph Parish, Bellwood publishes its own weekly bulletin on its eCatholic site,
saintjosephbellwood.org (eCatholic site id 40290). The newest issue read on 2026-10-21 is
`https://files.ecatholic.com/40290/bulletins/20261018.pdf`, dated "OCT 18, 2026": headed "SAINT
JOSEPH CATHOLIC CHURCH, 623 E. Third Street, Bellwood, PA 16617", with a Mass schedule and
intentions for 17-25 October for this church only.

**Bellwood and Tyrone: two bulletins.** The lead noted that St. Joseph and St. Matthew, Tyrone
share a pastor. They do not share a bulletin: St. Matthew's is eCatholic site 37833 on
stmatthewtyrone.com, with its own file of the same Sunday (`files.ecatholic.com/37833/bulletins/
20261018.pdf`). Neither issue names the other parish (searched both for "Tyrone", "Bellwood",
"Matthew" and "Joseph"), their Mass schedules are separate, and each parish has its own
website. Neither bulletin names the pastor, so the shared pastor is not verified here; it would
not change the rows. See parishes/saint-matthew-tyrone.

## Worship sites

One church, St. Joseph (churches/saint-joseph-bellwood). The volunteer schedule lists a
"Chapel" eucharistic-minister slot ("Chapel-M. Kissel"), which is a post inside the church, not
a separate building with its own Masses. Nothing else in the bulletin or the directory entry.

## Website and bulletin provider

`bulletin_provider: ecatholic`, `provider_id: 40290`, `publication: ecatholic:40290`.
`website` is `https://saintjosephbellwood.org`, the eCatholic-hosted site (the directory has
`https://saintjosephbellwood.org/`; GCatholic has the older `http://www.stjosephbellwood.org`).
It answers 403 to curl and `probe url` (Cloudflare) and loads in headed Chrome, occasionally
after a "Just a moment..." page (the first load of the session was BLOCKED, the next two
passed). `pnpm fetch:check --diocese altoona-johnstown --parish saint-joseph-bellwood` on
2026-10-21 fetched `files.ecatholic.com/40290/bulletins/20261018.pdf` (status ok, 1,357,256
bytes, url_date 2026-10-18), this week's issue.

## Not yet confirmed

The pastor is not named in the bulletin or the site pages read; the shared-pastor lead is
unverified (it does not affect the row).
