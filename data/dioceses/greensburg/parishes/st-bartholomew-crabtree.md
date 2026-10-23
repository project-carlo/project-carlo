---
name: St. Bartholomew Parish, Crabtree
website: https://www.stbartholomewcrabtree.org
bulletin_provider: parishes_online
provider_id: st-bartholomew-church-15624
publication: ['po-org:st-bartholomew-church-15624', 'lpi:0018000000QxC0bAAF', 'po-container:14/1822',
  'url:https://www.stbartholomewcrabtree.org/bulletins/']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/1822/20261025B.pdf
  seen: 2026-10-23
  quote: 'Pastor: Rev. Justin Matro, O.S.B.'
  note: 'Page 1 of the 25 Oct 2026 issue (6 pages): "ST. BARTHOLOMEW CATHOLIC CHURCH", "OCTOBER 25, 2026 | THIRTIETH SUNDAY IN ORDINARY TIM E", "Staffed by the Benedictine Monks of Saint Vincent Archabbey", "Mailing Address: P.O. Box A, Crabtree, PA 15624", website "http://stbartholomew.wpengine.com". One Mass schedule: "Saturday Vigil | 5:00 PM", "Sunday | 8:00 AM & 10:30 AM", "Monday -Friday 8:00AM", "First Saturday | 8:00 AM". grep "Chapel" finds nothing.'
- url: https://container.parishesonline.com/bulletins/14/1822/20261025B.pdf
  seen: 2026-10-23
  quote: St. Bartholomew Church  |  14-1822
  note: Page 6 LPi footer, naming the container.
- url: https://www.stbartholomewcrabtree.org/wp-content/uploads/2026/10/October-25-2026-1.pdf
  seen: 2026-10-23
  note: 'The parish site reposts each issue as a dFlip post on /bulletins/ (sunday-october-25-2026, posted 2026-10-20 per wp-json) with a month-named PDF. Same bulletin as the container, not a second channel.'
- url: https://parishesonline.com/organization/st-bartholomew-church-15624
  seen: 2026-10-23
  note: 'probe po: "St. Bartholomew Church", 2538 State Route 119, Crabtree, website stbartholomewcrabtree.org, lpi 0018000000QxC0bAAF, container 14/1822, issues 2026-10-25, 10-18, 10-11. fetch:check 2026-10-23 ok, picked 20261025B.pdf.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=071
  seen: 2026-10-22
  note: 'Directory: St. Bartholomew Parish, 2538 Route 119, Crabtree, mailing P.O. Box A, pastor Father Justin Matro, OSB, "Saturday: 5:00 p.m.; Sunday: 8:00 a.m., 10:30 a.m.", no Partner Parishes. Fr. Matro serves no other parish in the clergy directory (tools/pastors.tsv).'
---

## Publisher

St. Bartholomew Parish, Crabtree (directory 071) publishes its own weekly bulletin through ParishesOnline, container 14/1822. The 25 October 2026 issue (read 2026-10-23 with `probe pdf`) is headed "ST. BARTHOLOMEW CATHOLIC CHURCH", "OCTOBER 25, 2026 | THIRTIETH SUNDAY IN ORDINARY TIM E", with "Pastor: Rev. Justin Matro, O.S.B." and "Staffed by the Benedictine Monks of Saint Vincent Archabbey", and one Mass schedule (Saturday Vigil 5:00 PM; Sunday 8:00 AM and 10:30 AM; Monday to Friday 8:00 AM). The page-6 footer reads "St. Bartholomew Church | 14-1822". No other parish or church appears. The directory lists no partner parishes, and Fr. Matro is pastor of this parish only (tools/pastors.tsv). One row.

## Worship sites

St. Bartholomew church, Crabtree: the only place in the bulletin's schedule and intentions (page 3, "SAT, 10/24- Vigil" etc. with no church named), and the only site GCatholic (24121) and the directory list for this parish. Within 6 miles of Crabtree the LPi geo-search also finds St. Florian (United), St. Bede/St. Mary and others, which are separate parishes with rows of their own.

## Website and bulletin provider

stbartholomewcrabtree.org is a diocese-template WordPress site (403 to `probe url`, 200 to curl with a browser User-Agent). The bulletin's masthead gives the template's wpengine host, stbartholomew.wpengine.com. Its /bulletins/ page reposts each container issue as a dFlip post with a month-named PDF (`October-25-2026-1.pdf`). The container is the source, so the provider is `parishes_online` with the org slug `st-bartholomew-church-15624` (from the LPi geo-search and `probe po`). The site's bulletin page is recorded as a `url:` publication id. `fetch:check` on 2026-10-23 was ok and picked `14/1822/20261025B.pdf`.

## Not yet confirmed

Nothing.
