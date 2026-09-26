---
name: St. Daniel Church
website: https://www.stdaniel.com
bulletin_provider: parishes_online
provider_id: st-daniel-church
publication: ['po-org:st-daniel-church', 'lpi:0018000000Qc1WhAAJ', 'po-container:06/0145']
group: 'Fr. Kurgan: Holy Cross, St. Daniel, St. Anthony of Padua'
evidence:
- url: https://container.parishesonline.com/bulletins/06/0145/20260927B.pdf
  seen: 2026-09-26
  quote: 3004 Court St., Syracuse, NY 13208
  note: Masthead, page 1 of the 27 September 2026 issue. St. Daniel alone.
- url: https://container.parishesonline.com/bulletins/06/0145/20260927B.pdf
  seen: 2026-09-26
  quote: Saturday - 4:00pm - Sunday 10:30am
  note: Page 1 Mass schedule.
- url: https://www.stdaniel.com/bulletins
  seen: 2026-09-26
  note: The parish's bulletins page links parishesonline.com/publication-page/st-daniel-church issues
    in container 06/0145 (visit.py --bulletin). `probe po st-daniel-church` gives LPi id 0018000000Qc1WhAAJ
    and weekly issues through 2026-09-27.
---

## Publisher

St. Daniel publishes its own weekly bulletin through ParishesOnline. The 27 September 2026
issue (container 06/0145) has a page-1 masthead for St. Daniel alone, 3004 Court St., with
"Saturday - 4:00pm - Sunday 10:30am" and weekday Masses. Its canonical pastor, Rev. John
Kurgan, also has Holy Cross (DeWitt) and St. Anthony of Padua; each of those publishes its
own bulletin, so this is its own row in that `group`.

## Worship sites

One: the church at 3004 Court Street (`st-daniel-syracuse`).

## Website and bulletin provider

stdaniel.com/bulletins embeds the ParishesOnline publication page for `st-daniel-church`;
`probe po` confirms the organization (LPi 0018000000Qc1WhAAJ, container 06/0145) and weekly
issues. All three ids are in `publication`.

## Not yet confirmed

Nothing.
