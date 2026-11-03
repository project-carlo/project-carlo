---
name: Church of the Sacred Heart
website: https://churchofthesacredheart.net
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2141
publication: ['url:http://sponsors.bonventure.net/?page=2141']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/2141/2026-11-01.pdf
  seen: 2026-11-02
  quote: 'Church: 149 South Plainfield Ave., South Plainfield, NJ 07080'
  note: '1 November 2026 issue (8 text pages). The page 1 masthead names Church of the Sacred Heart alone:
    ''Weekend: Saturday Vigil Mass 5:00PM, Sunday 9:00AM and 11:30AM''; daily Monday 7:00PM, Tuesday-Saturday
    9:00AM; ''Parish Center & Mailing Address: 200 Randolph Ave.'' Page 2 ''Parish Staff'' lists ''Pastor:
    Rev. Edmund Luciano III, KCHS, KOGCO''.'
- url: http://sponsors.bonventure.net/?page=2141
  seen: 2026-11-02
  quote: Church of the Sacred Heart 149 South Plainfield Ave. • South Plainfield, NJ 07080
  note: 'Bon Venture sponsor page 2141 for this parish only: ''Click to View Current Bulletin'' and weekly
    previous issues through November 01, 2026.'
- url: https://churchofthesacredheart.net/
  seen: 2026-11-02
  note: Parish WordPress site (www. redirects here); its bulletin link is http://sponsors.bonventure.net/?page=2141.
    No other publisher's link found on the home page.
bulletin_status: available
---

## Publisher

Church of the Sacred Heart, South Plainfield, publishes its own weekly bulletin through Bon Venture (sponsor page 2141; files at `sponsors.bonventure.net/pdfs/2141/<YYYY-MM-DD>.pdf`). The 1 November 2026 issue (read 2026-11-02) has a text page 1 naming 'Church of the Sacred Heart, Church: 149 South Plainfield Ave., South Plainfield, NJ 07080' with its own Mass schedule; page 2 lists 'Pastor: Rev. Edmund Luciano III, KCHS, KOGCO'. The parish finder lists Rev. John P. Alvarado as pastor and Rev. Pervais Indrias as parochial vicar; neither is on the masthead, so I followed the bulletin.

## Worship sites

One church, 149 South Plainfield Avenue (directory:24545, gcatholic:18596). The bulletin's Mass schedule names no other place; 200 Randolph Avenue is the parish center and mailing address, not a worship site. Holy Redeemer Cemetery appears in the staff list; it is a cemetery, not a church.

## Website and bulletin provider

Website https://churchofthesacredheart.net (the finder's www. form redirects there; `probe url` reported DEAD-DNS but `probe get` fetched it, as the playbook warns). Provider `other`, recipe `page-pdfs http://sponsors.bonventure.net/?page=2141`, as for the other Bon Venture parishes here.

## Not yet confirmed

Nothing about the publisher.

## Fetch check

`pnpm fetch:check` on 2026-11-02 resolved `page-pdfs http://sponsors.bonventure.net/?page=2141` and picked pdfs/2141/2026-11-01.pdf: transport ok, PDF, issue date inferred from the file name, freshness `fresh`, identity unverified by the tool. That is the 1 November 2026 issue whose masthead I read (above). No `recipe` line was printed, so the provider settings stay as set.
