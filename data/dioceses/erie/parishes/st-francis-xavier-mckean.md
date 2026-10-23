---
name: St. Francis Xavier Parish
website: https://www.stfrancisxaviermckean.org
bulletin_provider: parishes_online
provider_id: st-francis-xavier-church-16426
publication: ['po-org:st-francis-xavier-church-16426', 'lpi:0018000000QxBkKAAV', 'po-container:14/1700']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/1700/20261025B.pdf
  seen: 2026-10-23
  quote: MASS & SACRAMENT SCHEDULE
  note: 'Page 1 of the 25 October 2026 issue (8 pages): ''OCTOBER 25, 2026'', Rev. Benjamin Daghir pastor,
    P.O. Box 317 / 8880 Main Street, McKean PA 16426, office@stfrancisxaviermckean.org, schedule ''Weekdays:
    7:30 am Saturday 6:00 pm Sunday 8:00 & 10:30 am''. Footer p.8: ''St. Francis Xavier Church - McKean,
    PA 14-1700''. Content concerns this parish alone.'
- url: https://www.stfrancisxaviermckean.org/
  seen: 2026-10-23
  quote: Bulletins
  note: The parish's own site (diocese-hosted template) has a 'Bulletins' menu item whose onClick goes
    to https://www.parishesonline.com/find/st-francis-xavier-church-16426. Its weeklybulletin.php lists
    no weekly PDFs (the page returns 200 with no bulletin links).
- url: https://parishesonline.com/organization/st-francis-xavier-church-16426
  seen: 2026-10-23
  note: 'probe po: 8880 Main St, McKean (41.9957118, -80.143393), LPi 0018000000QxBkKAAV, container 14/1700,
    six weekly issues 2026-09-20 to 2026-10-25.'
- url: https://www.eriercd.org/Parish10306-St-Francis-Xavier.html
  seen: 2026-10-23
  note: 'Directory record 10306: one parish record, own locator_group_id, no secondary church or partner.
    Locator pastor ''Rev. Jason R. Feigh'' vs detail page and bulletin ''Rev. Benjamin Daghir'' (the bulletin
    is followed).'
research:
- method: pnpm fetch:check --diocese erie --parish st-francis-xavier-mckean --expected-identity Daghir
    --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://parishesonline.com/organization/st-francis-xavier-church-16426
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF (container 14/1700), identity matched on the pastor surname Daghir
    (the website in the masthead has a ligature artefact), issue date inferred 2026-10-25; freshness future
    only because the Sunday issue is posted early.
---

## Publisher

St. Francis Xavier, McKean publishes its own weekly bulletin through ParishesOnline (organization st-francis-xavier-church-16426, container 14/1700). I read the 25 October 2026 issue on 2026-10-23: the contact block gives 8880 Main Street, McKean, Rev. Benjamin Daghir as pastor, and the Mass schedule 'Weekdays: 7:30 am Saturday 6:00 pm Sunday 8:00 & 10:30 am'; the page-8 footer is 'St. Francis Xavier Church - McKean, PA 14-1700'. The directory shows a single parish record with no partner or mission, so it is its own row.

## Worship sites

One church, St. Francis Xavier at 8880 Main (W. Main) St, McKean. The directory lists no secondary church for it.

## Website and bulletin provider

stfrancisxaviermckean.org is a diocese-hosted site whose Bulletins menu goes to ParishesOnline; `fetch` reads the bulletin by provider_id. The site's weeklybulletin.php page holds no issues.

## Not yet confirmed

Nothing outstanding. The page-1 masthead's site address extracts with a ligature artefact ('s�rancis'), so fetch identity is checked on the pastor's surname (Daghir).
