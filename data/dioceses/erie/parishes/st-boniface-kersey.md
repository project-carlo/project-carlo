---
name: St. Boniface Parish
website: https://st-boniface.org
bulletin_provider: discover_mass
provider_id: st-boniface-kersey-pa
publication: ['discovermass:st-boniface-kersey-pa']
group: ''
evidence:
- url: https://discovermass.com/church/st-boniface-kersey-pa/
  seen: 2026-10-23
  quote: 355 Main St., Kersey, PA 15846
  note: 'Quote is from the Discover Mass church page. The bulletin read there: Page 1 of the 25 October
    2026 issue (4 pages, Discover Mass bulletin number 3404; PDF downloaded from the church page''s ''bulletin-current''
    link, cover class ''bulletin-cover X-|2026-10-25|1792782535|3404''): ''A Welcoming Parish in the Heart
    of Elk County, 355 Main Street, Kersey, PA 15846'', ''St. Boniface Parish'', ''Mass Times: Saturday
    Evening: 4:15 p.m. Sunday: 8:00 & 10:30 a.m. Daily Masses Tue. - Thurs. 7:15 a.m.''. The text layer
    garbles the date (''OOctober 225, 5, 2026''). Names this parish alone; the issue does not mention
    Holy Cross or Brandy Camp.'
- url: https://st-boniface.org/church/bulletin/
  seen: 2026-10-23
  quote: Click for the Bulletin
  note: 'Parish site (WordPress) Bulletin page: ''The weekly bulletin is available at all weekend masses
    and online here.'' The link goes to http://discovermass.com/church/st-boniface-kersey-pa/#bulletins;
    no PDF is hosted on the site. The page also says advertising is sold by ''Diocesan: Catholic Life
    Every Day''.'
- url: https://www.eriercd.org/Parish20606-St-Boniface.html
  seen: 2026-10-23
  note: 'Directory record 20606: 355 Main St., Kersey 15846; Pastor Rev. Christopher Beran (clergy list
    updated 8/7/2026: ''Pastor ... St. Boniface, Kersey''); Mass Sat 4:15 p.m., Sun 8, 10:30 a.m., Tue-Thu
    7:15 a.m. The locator''s ''Very Rev. Ross R. Miceli'' is stale. The printable directory (Oct. 6, 2026)
    lists St. Boniface Parish under Kersey with a single physical address and no Brandy Camp church.'
research:
- method: probe url st-boniface.org; read church/bulletin page; read Discover Mass church page once; downloaded
    the current PDF and grepped it for Holy Cross and Brandy Camp
  url: https://discovermass.com/church/st-boniface-kersey-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: None.
- method: pnpm fetch:check --diocese erie --parish st-boniface-kersey --expected-identity Kersey (headed
    Chrome)
  url: https://discovermass.com/church/st-boniface-kersey-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Resolver discover_mass: transport ok, PDF, identity matched on page 1 (''355 main
    street kersey pa 15846''); issue date ''unknown'' (the masthead date is split by the layout) so overall
    ''unverified'' for that reason only; the cover class carries 2026-10-25.'
---

## Publisher

St. Boniface Parish, Kersey (pastor Rev. Christopher Beran per the clergy list updated 8/7/2026) publishes its own weekly bulletin, posted on its Discover Mass church page `st-boniface-kersey-pa`. The 25 October 2026 issue (bulletin number 3404), read on 2026-10-23, is headed 'St. Boniface Parish, 355 Main Street, Kersey, PA 15846' and prints one Mass schedule (Saturday 4:15 pm, Sunday 8:00 and 10:30 am, Tuesday-Thursday 7:15 am). The parish site st-boniface.org hosts no PDF: its Bulletin page sends readers to the Discover Mass page. Not shared with the St. Marys parishes (separate pastor, separate document).

## Worship sites

One church, St. Boniface, 355 Main Street, Kersey. Holy Cross, Brandy Camp was merged into this parish on 2017-02-13 and relegated to profane use effective 2020-07-26; it is excluded as closed (`excluded/holy-cross-brandy-camp`). The 25 Oct 2026 bulletin and the printable directory (Oct. 6, 2026) list no other church.

## Website and bulletin provider

`discover_mass`, provider_id `st-boniface-kersey-pa`. Website st-boniface.org (WordPress). The Discover Mass listing is the only channel found; there is no ParishesOnline or eCatholic widget on the site (probe url, 2026-10-23). The old domain stbonifacekersey.org is dead DNS and not used.

## Not yet confirmed

Nothing outstanding. Fetch check reports issue date unknown because the layout splits the masthead date; the date is inferred from the Discover Mass cover class.
