---
name: Our Lady, Queen of the Americas Parish
website: https://olqachurch.org
bulletin_provider: parishes_online
provider_id: our-lady-queen-of-the-americas
publication: ['po-org:our-lady-queen-of-the-americas', 'lpi:0018000000QxBk0AAF', 'po-container:14/1153']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/1153/20261025B.pdf
  seen: 2026-10-23
  quote: 155 South Ninth Street, Conneaut Lake
  note: 'Page 1 of the 25 October 2026 issue (4 pages; posted early): ''OUR LADY QUEEN OF THE AMERICAS
    CATHOLIC CHURCH / OCTOBER 25, 2026 / 30TH SUNDAY IN ORDINARY TIME''. Names this parish alone; one
    Mass schedule.'
- url: https://container.parishesonline.com/bulletins/14/1153/20261025B.pdf
  seen: 2026-10-23
  quote: Saturday Vigil | 5:00pm
  note: 'Same page: WEEKEND MASS ''Saturday Vigil | 5:00pm'', ''Sunday | 8:00am & 10:30am''; WEEKDAY MASS
    ''Monday | 6:00pm'', ''Tuesday | Noon'', ''Wednesday |6:00pm'', ''Thursday | Noon'', ''Friday | No
    Mass''. Matches the directory (Sat 5 p.m.; Sun 8, 10:30; Mon/Wed 6 p.m.; Tue/Thu noon).'
- url: https://container.parishesonline.com/bulletins/14/1153/20261025B.pdf
  seen: 2026-10-23
  quote: Our Lady Queen of the Americas, Conneaut Lake, PA 14-1153
  note: Page 4 publisher footer; container 14/1153 matches probe po our-lady-queen-of-the-americas (lpi:0018000000QxBk0AAF,
    latest issue 2026-10-25).
- url: https://olqachurch.org/bulletin.html
  seen: 2026-10-23
  quote: Bulletins
  note: Diocese-hosted site (footer 'Diocese of Erie 429 East Grandview Blvd.'); its Bulletins page links
    https://www.parishesonline.com/find/our-lady-queen-of-the-americas. No weeklybulletin.php PDFs; ParishesOnline
    is the channel.
research:
- method: pnpm fetch:check --diocese erie --parish our-lady-queen-of-the-americas-conneaut-lake --expected-identity
    Conneaut (headed Chrome)
  url: https://parishesonline.com/organization/our-lady-queen-of-the-americas
  checked: '2026-10-23'
  outcome: found
  next_action: None. Resolver parishes_online picked container 14/1153 20261025B.pdf (2,193,585 bytes);
    transport ok, PDF, identity matched (Conneaut in first-page text; Carter is not on page 1), issue
    date 2026-10-25 observed; freshness future only because posted two days early.
---

## Publisher

Our Lady, Queen of the Americas, Conneaut Lake publishes its own weekly bulletin through ParishesOnline/LPi (organization our-lady-queen-of-the-americas, container 14/1153). The 25 October 2026 issue (read 2026-10-23, posted early) has the masthead 'Our Lady Queen of the Americas Catholic Church, 155 South Ninth Street, Conneaut Lake' and one Mass schedule, Saturday 5:00pm, Sunday 8:00am and 10:30am, weekdays Mon/Wed 6:00pm, Tue/Thu noon. The pastor is Rev. David E. Carter (clergy PDF of 8/7/2026: 'Pastor ... Our Lady Queen of the Americas, Conneaut Lake'), who serves no other parish.

## Worship sites

One church, 155 S. 9th St., Conneaut Lake. No secondary church or mission is listed in the directory (both the web list and the printable directory of Oct. 6, 2026 show this parish with no churches under it) or in the bulletin. The partner parishes St. Peter/St. Philip print only a religious-education contact for OLQA, nothing more (their 25 October bulletin: 'Conneaut Area Religious Education OLQA, Conneaut Lake 814-382-7252'), and a 14 November Rosary Rally at OLQA.

## Website and bulletin provider

`parishes_online`, org slug our-lady-queen-of-the-americas. The site is https://olqachurch.org (the directory's http://www.olqachurch.org redirects there). Discover Mass has a page (our-lady-queen-of-the-americas-conneaut-lake-pa) that says 'no bulletins available' (read 2026-10-23), so not a channel.

## Not yet confirmed

Nothing open about identity; run the fetch check for freshness.
