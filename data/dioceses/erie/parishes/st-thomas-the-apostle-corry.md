---
name: St. Thomas the Apostle Parish
website: https://stthomastheapostle.church
bulletin_provider: other
provider_id: page-pdfs https://stthomastheapostle.church/weeklybulletin.php
publication: ['url:https://stthomastheapostle.church/weeklybulletin.php#st-thomas-the-apostle-corry',
  'po-container:14/1154']
group: St. Thomas the Apostle (10408) with St. Teresa of Avila, Union City (10407, merged 2024-07-09;
  secondary mission)
evidence:
- url: https://stthomastheapostle.church/images/weeklybulletin/4aeaa8937152d1a599af7f21b21122e1.pdf
  seen: 2026-10-23
  quote: Rev. Thomas J. Whitman
  note: 'Page 1 of the issue dated October 25, 2026 (30th Sunday in Ordinary Time; 5 pages, text layer):
    masthead ''the parish of St. Thomas the Apostle and its mission St. Teresa of Avila'', ''Saint Thomas
    the Apostle Church, 203 W. Washington Street, Corry, PA 16407'' and ''Saint Teresa of Avila Church,
    9 Third Avenue, Union City, PA 16438'', Rev. Thomas J. Whitman, Pastor. One bulletin for both churches.'
- url: https://stthomastheapostle.church/weeklybulletin.php
  seen: 2026-10-23
  note: 'Diocese-hosted weeklybulletin.php (scratch/map-erie/tools/weeklybulletin_issues.sh): 52 issues,
    newest October 25, 2026 (4aeaa893...pdf), then October 18, 11, 4 ... weekly back to November 2, 2025;
    current.'
- url: https://container.parishesonline.com/bulletins/14/1154/20261025B.pdf
  seen: 2026-10-23
  quote: St. Thomas the Apostle and St. Teresa Avila Churches, Corry, PA 14-1154
  note: 'Page 6 footer of ParishesOnline container 14/1154''s 25 October 2026 issue (6 pages; pages 1-5
    are images, page 1 rendered: the same masthead ''THE PARISH OF ST. THOMAS THE APOSTLE AND ITS MISSION
    ST. TERESA OF AVILA, October 25, 2026''). Its file differs from the site''s (md5 ef7a762a... vs 6a937b62...,
    6 pages vs 5): the ad edition of the same bulletin, whose text layer holds only the ad page. probe
    po finds no organization for 14/1154, only the container.'
- url: https://st-teresa-unioncity.org/images/weeklybulletin/e9ee37a60ec43052ad7da736896d64a9.pdf
  seen: 2026-10-23
  note: 'St. Teresa''s own site (st-teresa-unioncity.org, diocese template) lists the same weekly issues:
    its October 25 file is byte-identical (md5 6a937b62e1ddc2a58991cb0b5641a16b) to St. Thomas''s, and
    its October 18 and October 11 files are identical too (ef93bd67..., 138dcaba...). St. Teresa has no
    bulletin of its own.'
- url: https://www.eriercd.org/Parish10408-St-Thomas-the-Apostle.html
  seen: 2026-10-23
  note: 'Directory record 10408: 203 W. Washington St., Corry 16407; Saturday 4:30 pm alternates monthly
    between St. Thomas and St. Teresa; Sunday 8 am (Corry) and 11 am (Union City); pastor Rev. Thomas
    Whitman (the locator''s ''Rev. DG (Skip) Davis'' is stale).'
research:
- method: pnpm fetch:check --diocese erie --parish st-thomas-the-apostle-corry --expected-identity Whitman
  url: https://stthomastheapostle.church/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'See body: recipe page-pdfs on weeklybulletin.php chosen over container 14/1154 because
    the container''s pages 1-5 are images.'
- method: pnpm fetch:check --diocese erie --parish st-thomas-the-apostle-corry --expected-identity Whitman
    (headed Chrome)
  url: https://stthomastheapostle.church/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Resolver page-pdfs on weeklybulletin.php: current; first-listed 4aeaa893...pdf (25
    October 2026), transport ok, PDF; freshness ''future'' (posted early) so overall ''unverified'' for
    that reason only. Recipe is the provider_id.'
---

## Publisher

St. Thomas the Apostle Parish, Corry publishes one weekly bulletin for the parish and its mission St. Teresa of Avila, Union City. The issue dated 25 October 2026, read on 2026-10-23, is headed "the parish of St. Thomas the Apostle and its mission St. Teresa of Avila" with Rev. Thomas J. Whitman as pastor, and it lists the Masses of both churches. St. Teresa of Avila parish, including its secondary church Our Lady of Fatima, merged into St. Thomas on July 9, 2024 (the relegation decree for Our Lady of Fatima states the date; the merger decree PDF carries drafting dates June 22, 2023, August 29, 2023 and February 28, 2024); the bulletin shows both churches still hold Mass.

## Worship sites

Two churches: St. Thomas the Apostle, 203 W. Washington St., Corry, and St. Teresa of Avila, 9 Third Ave., Union City. Excluded as closed: St. Elizabeth, Corry (relegated 2019-12-01) and Our Lady of Fatima, Canadohta Lake (relegated 2024-08-14; no regular Mass since 2023). The directory and GCatholic still list both; see their `excluded/` records. The 'St. Elizabeth Parish Center' named in recent issues is a parish hall used for Knights of Columbus and Rosary meetings, not a place of Mass.

## Website and bulletin provider

Two channels carry the same bulletin. (1) The diocese-hosted `weeklybulletin.php` on stthomastheapostle.church, with a text layer. It is identical, file for file, to the one on st-teresa-unioncity.org (see evidence). (2) ParishesOnline container 14/1154 (no org record; the church site embeds only the container), which carries the ad edition as mostly image pages. `other` with `page-pdfs https://stthomastheapostle.church/weeklybulletin.php` was chosen because its text layer can be read; the container is recorded in `publication`. The directory's other website for St. Teresa (st-teresa-unioncity.org) and the GCatholic website corrycatholics.org (dead DNS) are not channels of their own.

## Not yet confirmed

Nothing outstanding for the structure. The PO container's current state follows the site's.
