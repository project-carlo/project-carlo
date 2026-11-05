---
name: St. Elizabeth of Hungary, Linden
website: https://parishesonline.com/organization/st-elizabeth-of-hungary-church-07036
bulletin_provider: parishes_online
provider_id: st-elizabeth-of-hungary-church-07036
publication: ['po-org:st-elizabeth-of-hungary-church-07036', 'lpi:0018000000QxAA5AAN', 'po-container:03/1108']
group: Planning Area K
evidence:
- url: https://container.parishesonline.com/bulletins/03/1108/20261108B.pdf
  seen: 2026-11-05
  quote: 220 E. Blancke Street, Linden, New Jersey 07036
  note: 'Issue for ''November 8 & November 15, 2026'' (8 pages, text; headed ''32nd & 33rd Sundays in
    Ordinary Time''). Page 1 masthead: ''St. Elizabeth of Hungary Roman Catholic Church'', www.sehplinden.org;
    ''MASS SCHEDULES (All Masses are open to the public) Weekend Masses Saturday: 4 PM & 7:30 PM Sunday:
    8 AM, 10 AM & 12:00 PM''; ''Rectory Address 179 Hussa Street''; ''Rev. Arlou T. Buslon, Pastor''.
    One church named.'
- url: https://parishesonline.com/organization/st-elizabeth-of-hungary-church-07036
  seen: 2026-11-05
  note: 'probe po: St. Elizabeth of Hungary Church, 179 Hussa St., Linden, NJ 07036; lpi 0018000000QxAA5AAN;
    container 03/1108; website https://sehplinden.org/; latest issues 2026-11-08, 10-25, 10-11, 09-27,
    09-13 (one issue every two weeks).'
- url: https://sehplinden.org/
  seen: 2026-11-05
  note: 'Directory website, a JavaScript app (probe get returns an empty shell; read with parish-site-access
    visit.py). Its ''Parish Bulletin'' section links parishesonline.com/publication-page/st-elizabeth-of-hungary-church-07036
    issues of container 03/1108 (20261108B, 20261025B, 20261011B, 20260927B). Mass schedule: Saturday
    12:05 PM, 4:00 PM Anticipatory Mass (English), 7:30 PM Anticipatory Mass (Spanish); Sunday 8:00 AM,
    10:00 AM, 12:00 PM; weekdays 8:00 AM and 12:05 PM; ''Every Second Sunday of the month Mass with the
    Filipino Apostolate''.'
research:
- method: fetch:check freshness on a biweekly container
  url: https://parishesonline.com/organization/st-elizabeth-of-hungary-church-07036
  checked: '2026-11-05'
  outcome: found
  next_action: Confirm fetch picks the 22 November 2026 issue once it is posted; the two-week issue can
    read as stale late in its fortnight
  retry_when: The 22 November 2026 issue is posted
  revisit_after: 2026-11-23
bulletin_status: available
---

## Publisher

St. Elizabeth of Hungary, Linden, publishes a bulletin with LPi (ParishesOnline org `st-elizabeth-of-hungary-church-07036`, container 03/1108), one issue every two weeks: the container's latest issues are 2026-11-08, 10-25, 10-11, 09-27 and 09-13. I read the issue dated 'November 8 & November 15, 2026' (8 pages, text). Page 1 is the masthead: 'St. Elizabeth of Hungary Roman Catholic Church, 220 E. Blancke Street, Linden, New Jersey 07036', www.sehplinden.org, pastor Rev. Arlou T. Buslon, rectory at 179 Hussa Street, and one Mass schedule ('All Masses are open to the public').

## Worship sites

- St. Elizabeth of Hungary Church (`st-elizabeth-of-hungary-linden`): Saturday 12:05 PM, vigils 4:00 PM (English) and 7:30 PM (Spanish); Sunday 8:00 AM, 10:00 AM, 12:00 PM; weekdays 8:00 AM and 12:05 PM (parish website, 2026-11-05; the bulletin's page 1 gives the weekend Masses). The 'small chapel' where Wednesday adoration is held is on the parish grounds, not a separate worship site.

The directory (99) and GCatholic (18464) list only this church. The Filipino Apostolate's monthly Mass is part of this schedule.

## Website and bulletin provider

The parish site sehplinden.org (the directory's and the masthead's website) links this container's issues, so the bulletin is read from ParishesOnline by org slug. GCatholic's www.sainteonline.org does not resolve (probe url DEAD-DNS, 2026-11-05), an old domain.

Fetch check (2026-11-05, headed): transport ok, PDF, picked container 03/1108's `20261108B.pdf`, the issue read above; freshness `future` (age -3 days, window 14) because it is dated the coming Sunday. Identity `unverified` only because no expected identity is supplied.

## Not yet confirmed

Whether fetch keeps the biweekly issue fresh through its second week (research holds the recheck after the 22 November issue).
