---
name: St. Joseph/Bread of Life Community and Sacred Heart of Jesus Parishes
website: https://stjoseph-sacredheart.org
bulletin_provider: parishes_online
provider_id: sacred-heart-church-16508
publication: ['po-org:sacred-heart-church-16508', 'lpi:0018000000QxBkeAAF', 'po-org:st-joseph-church-bread-of-life-community',
  'lpi:0018000000Qc1UgAAJ', 'po-org:st-paul-church-16502', 'lpi:0018000000QxBkQAAV', 'po-container:14/1876']
group: 'Erie city partnership (effective 2024-07-09): St. Joseph/Bread of Life Community, Sacred Heart
  of Jesus, St. Paul (mission)'
evidence:
- url: https://container.parishesonline.com/bulletins/14/1876/20261025B.pdf
  seen: 2026-10-23
  quote: St. Paul Church (Mission)
  note: 'Page 1 masthead of the 25 October 2026 issue (8 pages, container 14/1876): ''Sacred Heart of
    Jesus Church and Saint Joseph Church / St. Paul Church (Mission)'', pastor ''Rev. Steve Schreiber''.
    One bulletin names all three churches and gives one combined Mass box. Issues of 18 October and 27
    September 2026 carry the same masthead (read 2026-10-23).'
- url: https://container.parishesonline.com/bulletins/14/1876/20261025B.pdf
  seen: 2026-10-23
  quote: Saturday 4:00 pm @ St. Paul
  note: 'Same masthead, WEEKEND MASSES box: ''Saturday 4:00 pm @ St. Paul / Sunday 8:45 am @ Sacred Heart
    / 10:45 am @ St. Joseph BOL''; WEEKDAY MASSES all ''at St. Joseph Bread of Life'' (Mon and Tue 7:00
    am, Wed 6:00 pm, Thu and Fri 7:00 am).'
- url: https://container.parishesonline.com/bulletins/14/1876/20261025B.pdf
  seen: 2026-10-23
  quote: Hungry Hearts Erie
  note: 'Page 1 pastor''s letter: the three churches chose ''Hungry Hearts Erie'' as the shared parish
    nickname (''One Parish Mindset''), which supports one bulletin and one row for the partnership.'
- url: https://stjoseph-sacredheart.org
  seen: 2026-10-23
  note: Parish site (title 'St. Joseph & Sacred Heart Parish | Our Erie Catholic Community') links the
    ParishesOnline organization sacred-heart-church-16508 (probe url publication po-org:sacred-heart-church-16508).
    The site has Schedules pages for St. Joseph/BoL, Sacred Heart and St. Paul, so it is one site for
    the partnership.
- url: https://parishesonline.com/organization/sacred-heart-church-16508
  seen: 2026-10-23
  note: 'probe po: three ParishesOnline organizations list the same container 14/1876 and the same issues
    (latest 2026-10-25): sacred-heart-church-16508 (lpi 0018000000QxBkeAAF, 816 W 26th St), st-joseph-church-bread-of-life-community
    (lpi 0018000000Qc1UgAAJ, 147 W 24th St, website stjoseph-sacredheart.org) and st-paul-church-16502
    (lpi 0018000000QxBkQAAV, 1617 Walnut St). All three are one bulletin, so all ids are recorded on this
    one row.'
- url: https://www.eriercd.org/Parish10309-St-Joseph-Bread-of-Life-Community.html
  seen: 2026-10-23
  note: 'Diocese directory: St. Joseph/Bread of Life Community Parish (10309), 147 W. 24th St.; Sacred
    Heart of Jesus Parish (10305, locator group 10309); St. Paul Church (10316) is a ''Mission'' under
    Sacred Heart (city list: ''secondary church''). Directory Mass times: St. Joseph Sun 10:45 a.m. and
    weekdays; Sacred Heart Sun 8:45 a.m.; St. Paul Sat 4 p.m. The clergy PDF (diocese.md, Sources) gives
    Schreiber as pastor of both parishes.'
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese erie --parish st-joseph-sacred-heart-erie --expected-identity 'Sacred
    Heart of Jesus' --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://parishesonline.com/organization/sacred-heart-church-16508
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF (container 14/1876, 20261025B.pdf), identity matched on page 1,
    issue date observed 2026-10-25; freshness 'future' only because the issue is posted two days early
    on the reference date.
---

## Publisher

St. Joseph/Bread of Life Community Parish and Sacred Heart of Jesus Parish, Erie, partnered by decree effective 2024-07-09 under Rev. Stephen Schreiber, publish **one** weekly bulletin through ParishesOnline, container 14/1876. The masthead of the 25 October 2026 issue (read 2026-10-23, page 1) names 'Sacred Heart of Jesus Church and Saint Joseph Church' and 'St. Paul Church (Mission)', with one pastor and one combined Mass box; the 18 October and 27 September issues carry the same masthead. The pastor's letter says the community adopted the nickname 'Hungry Hearts Erie'. So the two canonical parishes and St. Paul are one row (one bulletin).

The directory has three records (10309 St. Joseph/BoL, 10305 Sacred Heart, 10316 St. Paul mission); GCatholic has three churches (24524, 24465, 24548). No second bulletin exists: the old parish site stjoesbol.org (Wix, old schedule 'Sunday: 8:30 am & 11:00 am & 7:00 PM', no bulletin read) is stale, and sacredhearterie.org is a spam-taken domain (probe url SPAM-SQUAT, 2026-10-23).

## Worship sites

Three churches, all with a public Mass in the current masthead: St. Joseph/Bread of Life (147 W. 24th St.; Sunday 10:45 am and all weekday Masses), Sacred Heart of Jesus (816 W. 26th St.; Sunday 8:45 am) and St. Paul (1617 Walnut St.; Saturday 4:00 pm). St. Paul was merged into Sacred Heart canonically and is called a mission, but it still holds the Saturday vigil.

## Website and bulletin provider

stjoseph-sacredheart.org (WordPress) links the ParishesOnline organization sacred-heart-church-16508; `fetch` reads it by provider_id. The St. Joseph and St. Paul organizations on ParishesOnline are aliases of the same container 14/1876 and are listed in `publication`.

## Not yet confirmed

Nothing outstanding on identity; the directory's Mass times were not compared line by line with the bulletin beyond the weekend box.
