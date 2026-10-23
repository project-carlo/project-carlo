---
name: St. Gregory Thaumaturgus Parish
website: https://stgregoryparish.info
bulletin_provider: parishes_online
provider_id: st-gregory-church
publication: ['po-org:st-gregory-church', 'lpi:0018000000QxBkLAAV', 'po-container:14/1167']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/1167/20261025B.pdf
  seen: 2026-10-23
  quote: Pastor, Rev. Thomas Brooks
  note: 'Page 1 of the issue dated October 25, 2026 (30th Sunday in Ordinary Time; 8 pages; posted early).
    Header: 48 South Pearl Street, North East; parish office 136 W. Main St.; website www.stgregoryparish.info.
    Mass schedule: Saturday 5:00PM; Sunday 7:30AM, 9:00AM & 12:00PM; weekdays Mon/Tue/Wed/Fri 8:00 AM,
    Thursday 12:10 PM. Names no other church.'
- url: https://stgregoryparish.info/weeklybulletin.php
  seen: 2026-10-23
  quote: No Bulletin found.
  note: The diocese-hosted weeklybulletin.php page (the template that holds PDFs on other Erie parish
    sites) lists no PDF at all; it prints 'No Bulletin found.' Its navigation 'Bulletins' link carries
    onClick=location.assign('https://www.parishesonline.com/organization/st-gregory-church'), i.e. the
    parish's bulletin is the ParishesOnline org.
- url: https://www.parishesonline.com/organization/st-gregory-church
  seen: 2026-10-23
  note: 'probe po st-gregory-church: publication ids po-org:st-gregory-church, lpi:0018000000QxBkLAAV,
    po-container:14/1167; issues 2026-09-20 through 2026-10-25 weekly (latest 20261025B.pdf).'
- url: https://www.eriercd.org/Parish10208-St-Gregory-Thaumaturgus.html
  seen: 2026-10-23
  note: 'Directory record 10208: 48 S. Pearl St., North East 16428; Mass Sat 5 p.m.; Sun 7:30, 9, 12;
    daily Mon/Tue/Wed/Fri 8 a.m., Thu 12:10 p.m. Matches the bulletin.'
research:
- method: Compared stgregoryparish.info/weeklybulletin.php with the ParishesOnline org st-gregory-church
    (probe po, probe pdf)
  url: https://stgregoryparish.info/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: None. weeklybulletin.php is empty ('No Bulletin found.'); ParishesOnline is the live channel,
    so provider is parishes_online. Re-check only if the weeklybulletin.php page starts listing PDFs that
    differ from container 14/1167.
- method: pnpm fetch:check --diocese erie --parish st-gregory-thaumaturgus-north-east --expected-identity
    Brooks (headed Chrome)
  url: https://parishesonline.com/organization/st-gregory-church
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF, identity matched, issue date observed (25 October 2026), freshness
    'future' because ParishesOnline posts the issue early; overall 'unverified' for that reason only.
    Re-run after 25 October to see it verified.
---

## Publisher

St. Gregory Thaumaturgus Parish, North East, publishes one weekly bulletin through ParishesOnline (org `st-gregory-church`, container 14/1167, LPi 0018000000QxBkLAAV). The issue dated 25 October 2026, read on 2026-10-23, has the parish header (48 South Pearl Street, parish office 136 W. Main St.), Rev. Thomas Brooks as pastor and one Mass schedule for St. Gregory Church alone.

## Worship sites

One church, St. Gregory Thaumaturgus, 48 S. Pearl St. The bulletin's address block also names "St. Gregory Parish Office and Our Mother of Perpetual Help Chapel, 136 W. Main St." and the schedule says only "Our Mother of Perpetual Help Devotion following the 8:00 AM Mass on Wednesday": a devotion after the Mass at the church, not a Mass at the chapel. No roster lists the chapel as a church, and no Mass there is printed, so it is not a church row. It would change if a bulletin printed a Mass at the chapel.

## Website and bulletin provider

The batch asked to compare two candidate channels. (1) The parish site stgregoryparish.info is a diocese-hosted template site whose `weeklybulletin.php` page says "No Bulletin found." and lists no PDF; its Bulletins menu link sends visitors to the ParishesOnline org. (2) ParishesOnline `st-gregory-church` carries the current weekly issue (weekly from 20 September to 25 October 2026). The provider is therefore `parishes_online` with the org slug; no recipe is needed. `probe url` on the site embeds `po-org:st-gregory-church`.

## Not yet confirmed

Nothing outstanding. The 25 October issue is posted ahead of its date, so `fetch:check` may report it as future; that is not a failure.
