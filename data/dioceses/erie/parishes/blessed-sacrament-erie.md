---
name: Blessed Sacrament Parish
website: https://www.bsparisherie.org
bulletin_provider: parishes_online
provider_id: blessed-sacrament-church-16508
publication: ['po-org:blessed-sacrament-church-16508', 'lpi:0018000000QxBkdAAF', 'po-container:14/1555']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/1555/20261025B.pdf
  seen: 2026-10-23
  quote: Blessed Sacrament Church, Erie, PA
  note: Container 14/1555 issue of 25 October 2026 (8 pages). Page 1 text has the staff list (Father Philip
    Pinczewski, Pastor) and Mass box but the parish name is graphic; the name is in the page-8 advertiser
    footer 'Blessed Sacrament Church, Erie, PA 14-1555' and page-1 address line 'WWW.BSPARISHERIE.ORG
    - (814)454-0171 - 1626 WEST 26TH STREET, ERIE, PA 16508'.
- url: https://container.parishesonline.com/bulletins/14/1555/20261025B.pdf
  seen: 2026-10-23
  quote: Saturday 4:00pm
  note: 'Page 1 MASS SCHEDULE box: ''WEEKEND MASSES Saturday 4:00pm / Sunday 8:30AM, 11:00AM and 7:30PM;
    WEEKDAY MASSES (in the chapel) Monday - Thursday 8:00am; First Friday of the month 8:00am''. Matches
    the directory (record 10301).'
- url: https://www.bsparisherie.org/bulletins
  seen: 2026-10-23
  note: The parish's Duda site embeds the ParishesOnline widget for LPi id 0018000000QxBkdAAF; probe po
    resolves it to organization blessed-sacrament-church-16508, 1626 W 26th St, container 14/1555, latest
    issue 2026-10-25 (six weekly issues from 2026-09-20).
- url: https://www.eriercd.org/Parish10301-Blessed-Sacrament.html
  seen: 2026-10-23
  note: 'Diocese directory record 10301: one parish record, no group, partner or secondary church (locator_group_id
    is its own id); pastor Rev. Philip Pinczewski.'
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese erie --parish blessed-sacrament-erie --expected-identity Pinczewski
    --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://parishesonline.com/organization/blessed-sacrament-church-16508
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF (container 14/1555, 20261025B.pdf), issue date observed 2026-10-25;
    freshness reads 'future' only because the Sunday issue is posted two days early. Identity matched
    on the pastor's surname; the parish name 'Blessed Sacrament' is not in page-1 text (graphic masthead),
    so --expected-identity 'Blessed Sacrament' reports not_matched.
---

## Publisher

Blessed Sacrament Parish, Erie publishes its own weekly bulletin through ParishesOnline (organization blessed-sacrament-church-16508, container 14/1555). I read the 25 October 2026 issue on 2026-10-23: the staff list names Father Philip Pinczewski as pastor and the footer names 'Blessed Sacrament Church, Erie, PA 14-1555'; its content (Mass intentions, 'Parishioners of Blessed Sacrament', parish ads) concerns this parish alone. The directory shows it as a single parish record with no partner and the Erie-city partnerships (St. Joseph/Sacred Heart, St. John/Holy Trinity, ...) don't include it, so it is its own row. Its bulletin is a different container from the St. Joseph/Sacred Heart one (14/1876) and from every other Erie row.

## Worship sites

One church, Blessed Sacrament at 1626 W. 26th St. Weekend: Saturday 4:00 pm, Sunday 8:30 am, 11:00 am and 7:30 pm; weekdays Monday to Thursday 8:00 am in the chapel, plus first Fridays. The diocese directory lists no mission or secondary church for it.

## Website and bulletin provider

bsparisherie.org (Duda/WeConnect) embeds the ParishesOnline widget (LPi 0018000000QxBkdAAF); `fetch` reads it by provider_id. The site's own bulletin page has no separate PDF links.

## Not yet confirmed

Nothing outstanding. The page-1 masthead of the PDF does not print the parish name as text; identity rests on the footer, container id and the parish site embedding the widget.
