---
name: St. Raymond, Providence
website: https://www.straymonds.com/
bulletin_provider: parishes_online
provider_id: st-raymond-church
publication: ['po-org:st-raymond-church', 'lpi:0018000000Qc2PXAAZ', 'po-container:04/0915']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0915/20261115B.pdf
  seen: 2026-11-15
  quote: 1240  NORTH MAIN STREET
  note: '15 November 2026 issue (4 pages, text). Page 1: ''November 15, 2026'', ''1240 NORTH MAIN STREET
    PROVIDENCE • RHODE ISLAND 02904'', ''St. Raymond''s Catholic Parish''; Pastor Reverend Edward L. Pieroni;
    MASS SCHEDULE Weekend Saturday Vigil 4:00 p.m., Sunday 8:00 a.m. & 10:00 a.m.; Weekdays Monday through
    Friday 9:00 a.m.'
- url: https://parishesonline.com/organization/st-raymond-church
  seen: 2026-11-15
  note: 'probe po st-raymond-church: ''St. Raymond Church'', 1240 North Main St., Providence 02904-1812,
    LPi 0018000000Qc2PXAAZ, container 04/0915, latest issue 2026-11-15.'
- url: https://www.straymonds.com/bulletins.htm?week=0
  seen: 2026-11-15
  note: Parish site's bulletin links (bulletins.htm?week=0..3) run a script that redirects to a self-hosted
    copy, https://www.straymonds.com/bulletin/20261115B.pdf (same 4-page issue, same page 1 text); commented-out
    lines in the script point to container.parishesonline.com/bulletins/04/0915/.
promoted: 2026-11-16
bulletin_status: available
---

## Publisher

St. Raymond, Providence publishes its weekly bulletin through LPi (container 04/0915, org `st-raymond-church`). The 15 November 2026 issue (https://container.parishesonline.com/bulletins/04/0915/20261115B.pdf), page 1, gives "November 15, 2026", "1240 NORTH MAIN STREET PROVIDENCE • RHODE ISLAND 02904", "St. Raymond's Catholic Parish", Pastor Reverend Edward L. Pieroni, and the Mass schedule: Saturday Vigil 4:00 p.m., Sunday 8:00 a.m. and 10:00 a.m., Monday-Friday 9:00 a.m.

## Worship sites

One church, at 1240 North Main Street. The bulletin names no other place, and the finder (12213) and GCatholic (22430) list only this church.

## Website and bulletin provider

`parishes_online`, org `st-raymond-church`. Note the region: this container is 04, not the diocese's usual 03. The parish site (straymonds.com) has no publisher id in its HTML, so `probe url` says NO-PARISH-WORDS. Its `bulletins.htm?week=N` links compute the Sunday date in JavaScript and redirect to self-hosted copies of the LPi issue (`/bulletin/YYYYMMDDB.pdf`), so the site serves the same bulletin and is not a separate one.

## Not yet confirmed

Nothing open.
