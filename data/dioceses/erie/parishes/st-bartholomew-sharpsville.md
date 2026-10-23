---
name: St. Bartholomew Parish
website: https://www.saintbartholomews.com
bulletin_provider: parishes_online
provider_id: st-bartholomew-church-16150
publication: ['po-org:st-bartholomew-church-16150', 'lpi:0018000000Qc0CzAAJ', 'po-container:14/0202']
group: Partnered with Notre Dame, Hermitage (one pastor, Rev. John Miller)
evidence:
- url: https://container.parishesonline.com/bulletins/14/0202/20261025B.pdf
  seen: 2026-10-23
  quote: St. Bartholomew, Sharpsville, PA 14-0202
  note: 'Page 8 footer of the 25 October 2026 issue (8 pages; pages 1-7 are images). Page 1 rendered:
    ''St. Bartholomew Roman Catholic Church, 311 W. Ridge Ave., Sharpsville, PA 16150, 724-962-7130'';
    Weekend Mass Saturday 5:30 PM, Sunday 8:30 AM; Daily Mass Tuesday 5:30PM, Thursday 7:30 AM; Confession
    Tuesday 4:45-5:15PM; Pastor Rev. John Miller. Names this parish alone. md5 b6f42230...'
- url: https://www.saintbartholomews.com/
  seen: 2026-10-23
  note: 'probe url: HTTP 200, final URL https://www.saintbartholomews.com/, embeds lpi:0018000000Qc0CzAAJ,
    bulletin link https://www.saintbartholomews.com/bulletins.'
- url: https://parishesonline.com/organization/st-bartholomew-church-16150
  seen: 2026-10-23
  note: 'probe po 0018000000Qc0CzAAJ: org st-bartholomew-church-16150, website https://www.saintbartholomews.com/,
    311 W Ridge Ave, Sharpsville; container 14/0202; latest issue 2026-10-25.'
- url: https://container.parishesonline.com/bulletins/14/1705/20261025B.pdf
  seen: 2026-10-23
  quote: Church of Notre Dame, Hermitage, PA
  note: The partner's issue of the same date (container 14/1705, md5 fae97ac5...) is a different file
    with a Notre Dame masthead; see publication_reviews.
- url: https://www.eriercd.org/Parish31111-St-Bartholomew.html
  seen: 2026-10-23
  note: 'Directory record 31111: 311 W. Ridge Ave., Sharpsville; Pastor Rev. John Miller; Sat 5:30 p.m.,
    Sun 8:30 a.m., Tue 5:30 p.m., Thu 7:30 a.m.; city list ''partnered with Notre Dame Parish, Hermitage''.
    The locator''s pastor (Strickenberger) is stale.'
research:
- method: probe url; probe po on the embedded LPi id; masthead render; md5 comparison of 4 weeks against
    Notre Dame's container
  url: https://parishesonline.com/organization/st-bartholomew-church-16150
  checked: '2026-10-23'
  outcome: found
  next_action: None.
- method: pnpm fetch:check --diocese erie --parish st-bartholomew-sharpsville --expected-identity Miller
    (headed Chrome)
  url: https://parishesonline.com/organization/st-bartholomew-church-16150
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Resolver parishes_online picked container 14/0202 20261025B.pdf: transport ok, PDF,
    issue date 2026-10-25 inferred from the URL; freshness future (posted two days early) and identity
    unknown because pages 1-7 are images with no text layer (masthead checked by rendering page 1). Overall
    unverified for those reasons only.'
publication_reviews:
- parish: notre-dame-hermitage
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/14/0202/20261025B.pdf
    seen: 2026-10-23
    quote: St. Bartholomew, Sharpsville, PA 14-0202
    note: 'St. Bartholomew container 14/0202: masthead ''St. Bartholomew Roman Catholic Church'', md5
      b6f42230...; different file every week checked (4, 11, 18, 25 October). Each masthead names only
      its own parish.'
  - url: https://container.parishesonline.com/bulletins/14/1705/20261025B.pdf
    seen: 2026-10-23
    note: 'Notre Dame container 14/1705: masthead ''Church of Notre Dame'', footer ''Church of Notre Dame,
      Hermitage, PA 14-1705'', md5 fae97ac5...'
---

## Publisher

St. Bartholomew, Sharpsville publishes its own weekly ParishesOnline bulletin (container 14/0202; the LPi id embedded on saintbartholomews.com is the org's). The 25 October 2026 issue, read on 2026-10-23, is headed 'St. Bartholomew Roman Catholic Church, 311 W. Ridge Ave., Sharpsville' and gives only this church's Masses (Sat 5:30 pm, Sun 8:30 am, Tue 5:30 pm, Thu 7:30 am), with Rev. John Miller as pastor.

**Partner:** Father Miller is also pastor of Notre Dame, Hermitage (clergy PDF, updated 8/7/2026). Notre Dame's bulletin (container 14/1705) is a separate file with its own masthead, and prints both parishes' Mass boxes; this parish's issue does not print Notre Dame's Masses (text-layer search of the OCR-free pages found no 'Notre Dame'; pages 1-7 are images, page 1 was viewed). Four weeks compared (4, 11, 18, 25 October 2026) all differ. Two rows, per the diocese rule that a partner with its own live channel and distinct content is its own row.

## Worship sites

One church, St. Bartholomew, 311 W. Ridge Ave.

## Website and bulletin provider

`parishes_online`, org `st-bartholomew-church-16150`. The parish site embeds the LPi widget; the Bulletins page was not read separately.

## Not yet confirmed

Nothing outstanding. Result of `fetch:check` is in research.
