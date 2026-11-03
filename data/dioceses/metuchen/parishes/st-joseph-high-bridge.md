---
name: St. Joseph
website: https://www.sjchb.org
bulletin_provider: parishes_online
provider_id: st-joseph-church-08829
publication: ['po-org:st-joseph-church-08829', 'lpi:0018000000QxA43AAF', 'po-container:03/1327']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1327/20261101B.pdf
  seen: 2026-11-02
  quote: St. Joseph Church, High Bridge, NJ 03-1327
  note: '1 November 2026 issue (6 pages; pages 1-5 have no text layer, the quote is the LPi code line
    on ad page 6). Page 1 masthead (rendered): ''ST. JOSEPH R.C. CHURCH, Parish Office: 59 Main St. High
    Bridge, NJ 08829, Ph: (908) 638-6211, www.sjchb.org''; ''Weekend Mass Schedule: Saturday: Vigil Mass
    at 4 pm; Sunday: Mass at 8 am & 11am''; ''Daily Mass Schedule: Chapel, Tuesday, Wednesday, Thursday:
    8 am''; adoration ''in the Madonna & Child Chapel, behind the Rectory''; ''Our Parish is served by:
    Rev. Roy Quesea, JCL~ Administrator, Deacon Tom McGovern, Deacon Steve Fortier''. Names no other church.'
- url: https://parishesonline.com/organization/st-joseph-church-08829
  seen: 2026-11-02
  note: 'probe po 0018000000QxA43AAF: org ''St. Joseph Church'', 59 Main St, High Bridge, New Jersey,
    08829-1904, website www.sjchb.org, container 03/1327, weekly issues 2026-09-27 to 2026-11-01.'
- url: https://www.sjchb.org/
  seen: 2026-11-02
  note: Parish site (Duda builder) embeds the ParishesOnline publication widget with id=0018000000QxA43AAF;
    menu has /bulletin and /mass-times9da99a40.
- url: https://www.sjchb.org/mass-times9da99a40
  seen: 2026-11-02
  quote: 'Tuesday, Wednesday &amp; Thursday: Chapel at 8 am'
  note: 'Mass Times page: ''Saturday: 4 pm Vigil Mass'', ''Sunday: 8 am & 11 am Mass'', contact ''59 Main
    Street, High Bridge, NJ 08829''.'
promoted: 2026-11-03
bulletin_status: available
publication_reviews:
- parish: st-john-neumann-califon
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1327/20261101B.pdf
    seen: 2026-11-02
    note: The 1 November 2026 masthead (page 1, rendered) names St. Joseph R.C. Church, High Bridge alone,
      with its own Mass times (Sat 4 pm; Sun 8 and 11 am).
  - url: https://storage.googleapis.com/wzukusers/user-12949076/documents/9faabde67de34d55b87991eefefb910e/2026-11-01bulletin.pdf
    seen: 2026-11-02
    note: The 1 November 2026 masthead (page 1) names The Catholic Community of St. John Neumann, Califon
      alone, with its own Mass times (Sat 5:30 pm; Sun 9:30 am and 5:30 pm).
---

## Publisher

St. Joseph R.C. Church, High Bridge, publishes its own weekly bulletin through LPi / ParishesOnline (org `st-joseph-church-08829`, LPi id 0018000000QxA43AAF, container 03/1327). I read the 1 November 2026 issue (2026-11-02): pages 1-5 are images, so the masthead was read from a page-1 render: 'ST. JOSEPH R.C. CHURCH, Parish Office: 59 Main St. High Bridge, NJ 08829', weekend Masses Saturday 4 pm vigil and Sunday 8 and 11 am, daily Mass Tuesday-Thursday 8 am in the chapel, 'Rev. Roy Quesea, JCL~ Administrator'. Page 6 carries the LPi code line 'St. Joseph Church, High Bridge, NJ 03-1327'. The parish finder gives Rev. James A. Kyrpczak as administrator; the masthead names Fr. Quesea, so the finder is out of date.

Fr. Quesea is also administrator of St. John Neumann, Califon (its 1 November 2026 masthead), and that issue's page 5 remembers priests 'who served the communities of Saint Joseph and Saint John Neumann'. The two parishes still print separate bulletins with separate mastheads and Mass schedules through different publishers (LPi here, John Patrick there), so they are separate rows; see `publication_reviews`.

## Worship sites

One church, 59 Main Street (directory:24495, gcatholic:18664). The weekday Masses are in a chapel, and adoration is in 'the Madonna & Child Chapel, behind the Rectory', on the same campus; I took the chapel as part of this church's site, not a separate worship site. The bulletin names no other place.

## Website and bulletin provider

Website https://www.sjchb.org, whose home page embeds the ParishesOnline publication widget. Provider `parishes_online`, provider id the org slug. The survey's `probe url` said DEAD-DNS for sjchb.org, but `probe get` loaded it (see *Bulletin publishers here*: DEAD-DNS is unreliable). GCatholic's website `home.comcast.net/~sjchb/` is a long-dead Comcast home page.

## Not yet confirmed

Nothing open. The masthead is image-only, so a recheck has to render page 1 or rely on the page-6 code line and the Mass Times page.

## Fetch check

`pnpm fetch:check` on 2026-11-02 picked `container.parishesonline.com/bulletins/03/1327/20261101B.pdf`: transport ok, PDF, issue date 2026-11-01 inferred from the file name, freshness `fresh` (1 day); identity unverified by the tool (image-only masthead), read from a render above.
