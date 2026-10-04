---
name: St. John the Evangelist (Spencerport)
website: https://stjohnschurchspencerport.org
bulletin_provider: discover_mass
provider_id: st-john-the-evangelist-spencerport-ny
publication: ['discovermass:st-john-the-evangelist-spencerport-ny']
group: ''
evidence:
- url: https://discovermass.com/church/st-john-the-evangelist-spencerport-ny/
  seen: 2026-10-02
  quote: 55 Martha Street, Spencerport, NY 14559
  note: 'Discover Mass church page; Bulletins section: "Current Bulletin Oct 4, 2026", archive back through
    July. Mass Times field: "Saturday 9:00am - First Sat. , 5:00pm Sunday 7:45am , 9:30am , 11:15am".'
- url: https://stjohnschurchspencerport.org/
  seen: 2026-10-02
  note: 'Behind a bot block to curl (403); visit.py loaded it. Its "Bulletins" menu item links straight
    to discovermass.com/church/st-john-the-evangelist-spencerport-ny/. The site itself is eCatholic-hosted
    (site id 17421), but the bulletin is not on eCatholic, so ecatholic:17421 is not recorded as a publication.
    Home page address: "55 Martha Street Spencerport, NY 14559".'
- url: https://ps.dor.org/directory/st-john-the-evangelist-2/
  seen: 2026-10-02
  quote: Rev. Sriram K. Sadhanala, Pastor
  note: 'Diocesan directory (1/27/25): one worship site, address given as 58 Amity Street (see the church
    record), Sunday Masses 7:45, 9:30 and 11:15.'
promoted: 2026-10-02
---

## Publisher

St. John the Evangelist, Spencerport, publishes its weekly bulletin through Discover Mass (church slug `st-john-the-evangelist-spencerport-ny`). The Discover Mass page lists "Current Bulletin Oct 4, 2026" and the 27 September, 20 September ... issues. I read the 27 September and 4 October issues: both are the parish's own six-page bulletin with its Mass intentions (Saturday 5:00pm, Sunday 7:45, 9:30 and 11:15am) and its pastor's column. The bulletin PDF has no address masthead, so the address evidence is the Discover Mass page, the parish site, GCatholic and the diocese (see the church record). One church only.

## Worship sites

One: `churches/st-john-evangelist-spencerport.md`. Not to be confused with St. John the Evangelist, Greece (`parishes/st-john-greece.md`, a different bulletin).

## Website and bulletin provider

`stjohnschurchspencerport.org` is an eCatholic site behind a bot block that links its "Bulletins" item to the Discover Mass church page, so `discover_mass` with that slug is right, and the live `provider_id` was already correct. The Discover Mass issue links are tokens that change on each page load; `recheck` re-reads the church page instead.

## Not yet confirmed

The address: 55 Martha Street (parish site, GCatholic, Discover Mass) against 58 Amity Street (the diocese's directory and OpenStreetMap). Recorded on the church.
