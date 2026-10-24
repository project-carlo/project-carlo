---
name: St. Patrick Parish
website: http://www.StPatrickFranklin.org
bulletin_provider: parishes_online
provider_id: st-patrick-church-16323
publication: ['po-org:st-patrick-church-16323', 'lpi:0018000000QxBk1AAF', 'po-container:14/1166']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/1166/20261025B.pdf
  seen: 2026-10-23
  quote: 949 LIBERTY STREET, FRANKLIN, PENNSYLVANIA 16323
  note: 'Page 1 of the 25 October 2026 issue (posted early; 30th Sunday in Ordinary Time), container 14/1166:
    masthead ''SAINT PATRICK ROMAN CATHOLIC CHURCH, 949 LIBERTY STREET, FRANKLIN, PENNSYLVANIA 16323''.
    MASS SCHEDULE: weekend Saturday 9:00am (misprinted ''9::00am'') & 4:30pm Vigil, Sunday 8:00am & 10:30am;
    weekdays Monday 9:00am, Tuesday 9:00am, Wednesday 5:00pm, Thursday 9:00am, Friday 9:00am. It lists
    no other church.'
- url: https://container.parishesonline.com/bulletins/14/1166/20261025B.pdf
  seen: 2026-10-23
  quote: Rev. James C. Campbell
  note: 'Page 1 parish staff: ''Rev. James C. Campbell, Pastor; Rev. Mr. Richard O''Polka, Deacon''; parish
    office ''952 Buffalo Street, Franklin, PA 16323, (814) 437-5763, stpatrickfranklin.org''. Matches
    the clergy PDF (Campbell, pastor, St. Patrick, Franklin) and the directory.'
- url: https://parishesonline.com/organization/st-patrick-church-16323
  seen: 2026-10-23
  note: 'probe po st-patrick-church-16323: lpi:0018000000QxBk1AAF, ''St. Patrick Church'', 949 Liberty
    St, Franklin, PA; website https://www.stpatrickfranklin.org/ (so the org belongs to this parish);
    latest issue 2026-10-25, container 14/1166; issues 2026-10-04, 10-11, 10-18, 10-25 found.'
- url: https://www.eriercd.org/images/directoryparishchurch.pdf
  seen: 2026-10-23
  quote: 'Email: church@StPatrickFranklin.org'
  note: 'Printable directory of 6 October 2026, Franklin: St. Patrick Parish, 952 Buffalo St. (office),
    pastor Rev. James C. Campbell, Mass Mon, Tue, Thu, Fri 9 a.m., Wed 5 p.m., Sat 9 a.m. and 4:30 p.m.,
    Sun 8 a.m. and 10:30 a.m.; Website http://www.StPatrickFranklin.org. No secondary churches.'
promoted: 2026-10-23
research:
- method: probe url on http://www.StPatrickFranklin.org, then parish-site-access visit.py --bulletin in
    headed Chrome
  url: http://www.StPatrickFranklin.org
  checked: '2026-10-23'
  outcome: access-blocked
  next_action: 'None needed for the bulletin: it is read from ParishesOnline container 14/1166 (lpi:0018000000QxBk1AAF,
    whose org record lists this website). Re-open the site only to confirm Mass times or find a different
    bulletin host.'
  retry_when: The sandbox can load stpatrickfranklin.org, or the ParishesOnline container stops posting
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --diocese erie --parish st-patrick-franklin
    --expected-identity Patrick --expected-issue-date 2026-10-25
  url: https://container.parishesonline.com/bulletins/14/1166/20261025B.pdf
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF, identity matched, issue date inferred (25 October 2026); freshness
    'future' because the issue is posted two days early.
---

## Publisher

St. Patrick Parish, Franklin publishes its own weekly bulletin through ParishesOnline / LPi: organization `st-patrick-church-16323` (lpi:0018000000QxBk1AAF), container 14/1166. The 25 October 2026 issue (read 2026-10-23, posted early) is headed 'Saint Patrick Roman Catholic Church, 949 Liberty Street, Franklin', names Rev. James C. Campbell as pastor, and prints one Mass schedule for St. Patrick alone. The parish is a single-church parish with one pastor (clergy PDF 8/7/2026: Campbell, pastor, St. Patrick, Franklin) and is not linked to St. Joseph or St. Titus (Hoffman's parishes) in any source.

## Worship sites

St. Patrick Church, 949 Liberty St., Franklin: the only church. The bulletin's other Masses are not worship sites: 'Mass at Sugarcreek Station' (Monday 26 October 2:00 p.m., a residential facility) and 'St. Stephen School Mass' (a school Mass, 29 October 10:30), neither a public parish church. The directory lists no secondary churches.

## Website and bulletin provider

stpatrickfranklin.org answers HTTP 403 to `probe url` and to the headed Chrome visit (BLOCKED, one load), so the parish site's own bulletin page could not be read. The bulletin was found at ParishesOnline: the org's website field is `https://www.stpatrickfranklin.org/`, its address is the church's (949 Liberty St), and its masthead names this parish. Provider `parishes_online`, org slug `st-patrick-church-16323`. The directory's detail page for it is https://www.eriercd.org/Parish10401-St-Franklin.html (HTTP 200, 952 Buffalo St. office address, pastor Rev. James Campbell, deacon Richard O'Polka); the roster id 30911 is the locator's, and the alphabetical list omits this parish.

## Not yet confirmed

The parish site was never read; if it hosts a different bulletin than LPi's, compare. Nothing suggests it does.
