---
name: Church of Notre Dame
website: http://notredame-pa.org
bulletin_provider: parishes_online
provider_id: church-of-notre-dame
publication: ['po-org:church-of-notre-dame', 'lpi:0018000000QxBjrAAF', 'po-container:14/1705']
group: Partnered with St. Bartholomew, Sharpsville (one pastor, Rev. John Miller)
evidence:
- url: https://container.parishesonline.com/bulletins/14/1705/20261025B.pdf
  seen: 2026-10-23
  quote: Church of Notre Dame, Hermitage, PA
  note: 'Page 8 footer of the 25 October 2026 issue: ''... www.4lpi.com Church of Notre Dame, Hermitage,
    PA 14-1705''. Pages 1-7 are images; page 1 (rendered) is headed ''Church of Notre Dame, 2325 Highland
    Rd, Hermitage, PA 16148'', ''MASS SCHEDULE [NOTRE DAME] Weekend Masses Saturday: 4 pm / Sunday: 11
    am; Weekday Masses Wednesday & Friday: 9:00 am; Confession Saturday 3:00-3:30 pm'', then a second
    box ''Mass Schedule [St. Bartholomew] Weekend Masses Saturday: 5:30 pm / Sunday: 8:30 am; Weekday
    Masses Tuesday: 5:30 pm & Thursday: 7:30 am'', pastor Rev. John Miller. md5 fae97ac5...'
- url: https://container.parishesonline.com/bulletins/14/0202/20261025B.pdf
  seen: 2026-10-23
  quote: St. Bartholomew, Sharpsville, PA 14-0202
  note: 'The partner''s issue of the same date (md5 b6f42230...) is a different file from this row''s
    (md5 fae97ac5...); its page 1 masthead is ''St. Bartholomew Roman Catholic Church, 311 W. Ridge Ave.,
    Sharpsville'' with only St. Bartholomew''s Masses. Issues of 18, 11 and 4 October also differ between
    the two containers (first 8 hex of md5: 5e97cd61/c3b04e20, b6e7e213/f8f903ba, 426a74ea/06447603).
    So two live, distinct bulletins: see publication_reviews.'
- url: https://parishesonline.com/organization/church-of-notre-dame
  seen: 2026-10-23
  note: 'probe po church-of-notre-dame: org 0018000000QxBjrAAF, website http://notredame-pa.org, address
    2325 Highland Rd, Hermitage; container 14/1705; latest issue 2026-10-25 (issues weekly back to at
    least 2026-09-20).'
- url: https://notredame-pa.org/Resources/Sunday-Bulletins
  seen: 2026-10-23
  note: 'The parish site''s own Sunday Bulletins page (Connecting Members CMS, Cloudflare, plain curl
    works) lists only issues up to ''September 7, 2025'' with LinkClick download links: it is a stale
    channel, over a year behind. The current bulletin is the ParishesOnline container.'
- url: https://www.eriercd.org/Parish31105-Notre-Dame.html
  seen: 2026-10-23
  note: 'Directory record 31105: 2325 Highland Road, Hermitage; ''Pastor: Rev. John Miller''; Sat 4 p.m.,
    Sun 11 a.m., Wed and Fri 9 a.m.; city list ''partnered with St. Bartholomew Parish, Sharpsville''.
    The locator''s pastor ''Very Rev. Richard J. Allen'' is stale; the clergy PDF (updated 8/7/2026) names
    Miller for both parishes.'
research:
- method: probe url notredame-pa.org; probe po (ParishesOnline search API at the parish's coordinates);
    md5 and masthead comparison of 4 weeks of both containers
  url: https://parishesonline.com/organization/church-of-notre-dame
  checked: '2026-10-23'
  outcome: found
  next_action: None; fetch:check result in body.
- method: pnpm fetch:check --diocese erie --parish notre-dame-hermitage --expected-identity Miller (headed
    Chrome)
  url: https://parishesonline.com/organization/church-of-notre-dame
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Resolver parishes_online picked container 14/1705 20261025B.pdf: transport ok, PDF,
    issue date 2026-10-25 inferred from the URL; freshness future (posted two days early) and identity
    unknown because pages 1-7 are images with no text layer (masthead checked by rendering page 1). Overall
    unverified for those reasons only.'
publication_reviews:
- parish: st-bartholomew-sharpsville
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/14/1705/20261025B.pdf
    seen: 2026-10-23
    note: 'Notre Dame container 14/1705: masthead ''Church of Notre Dame'', footer ''Church of Notre Dame,
      Hermitage, PA 14-1705'', md5 fae97ac5... Each masthead names only its own parish.'
  - url: https://container.parishesonline.com/bulletins/14/0202/20261025B.pdf
    seen: 2026-10-23
    quote: St. Bartholomew, Sharpsville, PA 14-0202
    note: 'St. Bartholomew container 14/0202: masthead ''St. Bartholomew Roman Catholic Church'', md5
      b6f42230...; different file every week checked (4, 11, 18, 25 October).'
---

## Publisher

The Church of Notre Dame, Hermitage publishes its own weekly bulletin through ParishesOnline (container 14/1705, org `church-of-notre-dame`). The issue of 25 October 2026, read on 2026-10-23, is headed 'Church of Notre Dame, 2325 Highland Rd, Hermitage' with pastor Rev. John Miller. Its page-1 sidebar prints two Mass boxes: 'MASS SCHEDULE [NOTRE DAME]' (Sat 4 pm, Sun 11 am, Wed/Fri 9 am) and 'Mass Schedule [St. Bartholomew]' (Sat 5:30 pm, Sun 8:30 am, Tue 5:30 pm, Thu 7:30 am), the partner's Masses printed beside the parish's own.

**One bulletin or two: two.** Father Miller is pastor of both Notre Dame and St. Bartholomew, Sharpsville (clergy PDF, updated 8/7/2026; both directory records name him). Each parish still has its own ParishesOnline container with its own masthead and different content every week checked (4, 11, 18 and 25 October 2026: four different md5 pairs). St. Bartholomew's issue names only St. Bartholomew. Per the diocese's settled rule, a partner with its own live channel and distinct content is its own row; see `st-bartholomew-sharpsville`.

## Worship sites

One church, Notre Dame, 2325 Highland Rd. The bulletin's second Mass box lists St. Bartholomew's Masses, but that building is the other row's church. The bulletin also lists St. Rose (851 Dutch Ln) and St. Mary (664 Carbon Dr), both Hermitage, under 'Cemetery Association': cemeteries, not Mass sites.

## Website and bulletin provider

`parishes_online`, org `church-of-notre-dame`. The parish site notredame-pa.org (a Connecting Members site) has a Sunday Bulletins page that stops at 7 September 2025, so it isn't used. The website field keeps the parish's own domain, which is also the org's website.

## Not yet confirmed

Nothing outstanding about identity; the `fetch:check` result is recorded in research.
