---
name: All Saints Parish
website: https://allsaintsrcc.org
bulletin_provider: other
provider_id: page-pdfs https://allsaintsrcc.org/weeklybulletin.php
publication: ['url:https://allsaintsrcc.org/weeklybulletin.php#all-saints-waterford']
group: ''
evidence:
- url: https://allsaintsrcc.org/images/weeklybulletin/e9eb7b6a0bc0d7561b91d3a152476b32.pdf
  seen: 2026-10-23
  quote: Welcome to All Saints Parish, established in 2005, located in Waterford, Pennsylvania.
  note: 'Page 1 of the issue dated October 25, 2026 (7 pages; posted early): ''ALL SAINTS CATHOLIC CHURCH,
    WATERFORD, PENNSYLVANIA'', 11264 Route 97 N, Waterford, PA 16441, 814-796-3023; Msgr. David Rubino,
    Parochial Administrator; Mass schedule Saturday 4:30pm Vigil, Sunday 9:00am; confession Saturday 3:30-4:00pm.
    Names this parish alone.'
- url: https://allsaintsrcc.org/weeklybulletin.php
  seen: 2026-10-23
  note: 'Diocese-hosted weeklybulletin.php (scratch/map-erie/tools/weeklybulletin_issues.sh), newest first:
    October 25, 2026 (e9eb7b6a...pdf), October 18 (56443351...), October 4 (da47c66b...), September 27,
    September 20 ... one distinct PDF per issue, so the page is current (today''s date 2026-10-23, the
    25 October issue already posted). 11 October is not listed.'
- url: https://www.eriercd.org/Parish10320-All-Saints.html
  seen: 2026-10-23
  note: 'Directory record 10320: 11264 Route 97 N, Waterford 16441; Mass Sat 4:30 p.m., Sun 9 a.m., no
    daily Mass; administrator Msgr. David Rubino (the locator''s ''Rev. Gregory P. Passauer'' is stale).
    Matches the bulletin.'
promoted: 2026-10-23
research:
- method: probe url allsaintsrcc.org; weeklybulletin_issues.sh; probe pdf of the newest issue
  url: https://allsaintsrcc.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None: probe url finds no ParishesOnline or LPi widget, so the diocese-hosted page is the
    only channel.'
- method: pnpm fetch:check --diocese erie --parish all-saints-waterford --expected-identity Rubino (headed
    Chrome)
  url: https://allsaintsrcc.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Resolver page-pdfs on weeklybulletin.php: current; first-listed e9eb7b6a...pdf (25
    October 2026), transport ok, PDF; freshness ''future'' (posted two days early) so overall ''unverified''
    for that reason only. Recipe is the provider_id.'
---

## Publisher

All Saints Parish, Waterford publishes its own weekly bulletin on its diocese-hosted site (`weeklybulletin.php`, one PDF per issue under `images/weeklybulletin/`). The issue dated 25 October 2026, read on 2026-10-23, is headed All Saints Catholic Church, Waterford, with Msgr. David Rubino as parochial administrator and one Mass schedule (Saturday 4:30 pm vigil, Sunday 9:00 am).

## Worship sites

One church, All Saints, 11264 Route 97 N, Waterford. The bulletin's page 2 also prints "Thursday 6:00 pm Healing Mass Maria House" among the Mass times; that line appears in the 25 October issue only (the 18 and 4 October and 20 September issues do not carry it) and is recorded as an open question (`open/maria-house-healing-mass`), not as a church of this parish.

## Website and bulletin provider

`other`, read from allsaintsrcc.org/weeklybulletin.php (newest first, current to 25 October). No ParishesOnline or LPi widget on the site. Recipe `page-pdfs https://allsaintsrcc.org/weeklybulletin.php`.

## Not yet confirmed

The Maria House line, above.
