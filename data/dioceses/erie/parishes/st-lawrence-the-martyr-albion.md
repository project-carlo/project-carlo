---
name: St. Lawrence the Martyr Parish
website: https://www.stlawrencealbion.org
bulletin_provider: other
provider_id: page-pdfs https://www.stlawrencealbion.org/weeklybulletin.php
publication: ['url:https://www.stlawrencealbion.org/weeklybulletin.php#st-lawrence-the-martyr-albion']
group: St. Lawrence the Martyr (10312) with secondary mission St. Philip (31009)
evidence:
- url: https://www.stlawrencealbion.org/images/weeklybulletin/29c42114369cc157ff4d345f94acd796.pdf
  seen: 2026-10-23
  quote: Rev. Michael Kesicki - Pastor
  note: 'Page 1 masthead of the issue dated ''October 11, 2026'' (Twenty-Eighth Sunday in Ordinary Time):
    ''Saint Lawrence the Martyr / Saint Philip , Secondary Mission'', Rev. Michael Kesicki pastor, ''St.
    Lawrence-St. Philip Church, 180 East State Street, Albion''. The one bulletin covers both churches.'
- url: https://www.stlawrencealbion.org/images/weeklybulletin/29c42114369cc157ff4d345f94acd796.pdf
  seen: 2026-10-23
  quote: Sunday @ 8:00 am
  note: 'Page 2 Mass box: ''Weekend Masses: Saturday @ 4:00 pm at St. Lawrence; Sunday @ 8:00 am at St.
    Philip; Sunday @ 10:00 am at St. Lawrence''; ''Weekday Masses All at St. Lawrence 8:00am Monday, Wednesday,
    Thursday, and Friday, No Mass on Tuesday''.'
- url: https://www.stlawrencealbion.org/weeklybulletin.php
  seen: 2026-10-23
  note: 'Diocese-hosted weeklybulletin.php (scratch/map-erie/tools/weeklybulletin_issues.sh): two issues,
    ''October 11, 2026'' (29c42114...pdf) and ''October 4, 2026'' (989293b2...pdf), newest first, distinct
    files (different md5). On 2026-10-23 the 18 October issue was not posted: the page runs 12 days behind.
    The 25 October issue is not due until later.'
- url: https://www.stlawrencealbion.org/
  seen: 2026-10-23
  quote: St. Philip Church, our mission church in Edinboro, Pennsylvania
  note: Parish homepage; its Mass schedule box is 'St. Philip Mission Schedule Weekend Mass Sunday - 8:00am
    Reconciliation Sunday - 7:30am'. probe url finds no ParishesOnline or LPi widget.
- url: https://www.eriercd.org/Parish10312-St-Lawrence-the-Martyr.html
  seen: 2026-10-23
  note: Directory record 10312 (pastor Rev. Michael Kesicki; locator pastor 'Fr. Marc Solomon' is stale);
    St. Philip is record 31009, a 'secondary mission church' under 10312 in the city list.
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese erie --parish st-lawrence-the-martyr-albion --expected-identity Kesicki
    (headed Chrome)
  url: https://www.stlawrencealbion.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Resolver: page-pdfs on weeklybulletin.php, first-listed, dated 2026-10-11 (29c42114...pdf,
    2.5 MB); transport ok, PDF, identity matched, issue date observed, fresh (12 days, limit 14), overall
    verified. No separate recipe line was printed; provider_id pins the same page-pdfs recipe. Re-check
    freshness once the 25 October issue is due, as the page lags up to two weeks.'
---

## Publisher

St. Lawrence the Martyr, Albion publishes one weekly bulletin on its diocese-hosted site (weeklybulletin.php, one PDF per issue under images/weeklybulletin/). The issue dated 11 October 2026, read on 2026-10-23, is headed 'Saint Lawrence the Martyr / Saint Philip, Secondary Mission' with Rev. Michael Kesicki as pastor, and its Mass box covers both churches. St. Philip (directory record 31009) is a secondary mission of this parish with no bulletin of its own, so the two churches are one row.

## Worship sites

Two churches: St. Lawrence the Martyr, 180 E. State St., Albion (Saturday 4:00 pm, Sunday 10:00 am, weekdays Monday/Wednesday/Thursday/Friday 8:00 am) and St. Philip, State Highway 98 near Crossingville (the directory files it under Edinboro; Sunday 8:00 am). See the church records.

## Website and bulletin provider

`other`, read from stlawrencealbion.org/weeklybulletin.php, which lists issues newest first. Freshness: the newest posted issue on 2026-10-23 was 11 October (the 18 October issue was never posted), so the page lags by up to two weeks; the pipeline should expect old issues in some weeks.

## Not yet confirmed

Whether the lag is routine; re-check after the 25 October issue is due.
