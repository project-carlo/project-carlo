---
name: Holy Redeemer Parish
website: https://www.holyredeemerwarren.com
bulletin_provider: parishes_online
provider_id: holy-redeemer-church-16365
publication: ['po-org:holy-redeemer-church-16365', 'lpi:0018000000Qbz2CAAR', 'po-container:14/0961']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/0961/20261025B.pdf
  seen: 2026-10-23
  quote: 'St. Anthony of Padua Church: 7226 Route 6, Sheffield, PA 16347'
  note: 'Page 1 masthead of the 25 October 2026 issue (6 pages, posted two days early): ''HOLY REDEEMER
    CATHOLIC PARISH / Holy Redeemer Church: 11 Russell Street, Warren, PA 16365 / St. Anthony of Padua
    Church: 7226 Route 6, Sheffield, PA 16347 / Phone: 814-723-4222''. Page 5 ''Mass Schedule'': ''Weekend
    Masses Saturday: 4:30pm Vigil (Holy Redeemer) Sunday: 8:15am (Holy Redeemer), 11:00am (St. Anthony)
    / Weekday Masses Wednesday - Friday: 7:00am (Holy Redeemer)''; Pastor Rev. Mark O''Hern. Page 6 footer
    ''Holy Redeemer Church, Warren, PA 14-0961''. Names these two churches and not St. Joseph or St. Luke.'
- url: https://parishesonline.com/organization/holy-redeemer-church-16365
  seen: 2026-10-23
  note: 'probe po holy-redeemer-church-16365: LPi 0018000000Qbz2CAAR, website https://www.holyredeemerwarren.com/
    (the parish''s own domain, which Cloudflare blocks), address 11 Russell Street, Warren; container
    14/0961; issues 2026-10-25, 10-18, 10-11, 10-04 listed. The org''s website field matching the blocked
    parish domain is the identity evidence.'
- url: http://www.holyredeemerwarren.com
  seen: 2026-10-23
  note: 'probe url: HTTP 403; visit.py (headed Chrome) loaded 8 times and got Cloudflare ''Just a moment...''
    every time (verdict BLOCKED). The bulletin was found on ParishesOnline instead.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor ..............................................................................................Holy
    Redeemer, Warren
  note: 'Clergy list updated 8/7/2026: ''O''Hern, Rev. Mark A. - Pastor - Holy Redeemer, Warren'' (one
    assignment). The directory''s locator lists ''Rev. Stephen Schreiber'' for this parish; the clergy
    list and the bulletin agree on O''Hern.'
research:
- method: probe url; headed visit.py (8 loads); ParishesOnline search API near the church's coordinates;
    probe po
  url: https://parishesonline.com/organization/holy-redeemer-church-16365
  checked: '2026-10-23'
  outcome: found
  next_action: 'None for the bulletin: use ParishesOnline. The parish''s own site stays unreadable (Cloudflare).'
  retry_when: Only if the ParishesOnline container 14/0961 stops publishing
- method: pnpm fetch:check --diocese erie --parish holy-redeemer-warren --expected-identity 'Holy Redeemer'
    (headed Chrome)
  url: https://parishesonline.com/organization/holy-redeemer-church-16365
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Picked container 14/0961 issue 20261025B.pdf: transport ok, PDF, identity matched;
    issue date inferred from the file name, freshness ''future'' (posted two days early), so overall ''unverified''
    for that reason only.'
bulletin_status: available
publication_reviews:
- parish: st-joseph-warren
  decision: separate
  evidence:
  - url: https://www.stjosephwarrenpa.org/images/weeklybulletin/b8b4c590a251435c331579a759782d7a.pdf
    seen: 2026-10-23
    quote: Saint Luke Church- 420 North Main Street - Youngsville, PA 16371
    note: St. Joseph's 25 Oct 2026 masthead covers St. Joseph and St. Luke with Fr. Tomasone; Holy Redeemer's
      25 Oct issue (ParishesOnline 14/0961) is headed Holy Redeemer and St. Anthony of Padua, Sheffield,
      with Fr. O'Hern, and prints its own Mass schedule. The two publish different documents on different
      channels, though they cross-reference joint events (Faith Formation @ HR, All Saints Day coffee
      'at HR and 10:45 am at SJ').
---

## Publisher

Holy Redeemer Parish, Warren publishes its weekly bulletin through ParishesOnline (organization `holy-redeemer-church-16365`, container 14/0961). The 25 October 2026 issue, read on 2026-10-23, is headed 'Holy Redeemer Catholic Parish' and lists two churches under it: Holy Redeemer, 11 Russell Street, Warren and St. Anthony of Padua, 7226 Route 6, Sheffield. Pastor Rev. Mark O'Hern (clergy list updated 8/7/2026).

## Worship sites

Two churches, both in the masthead and the 'Mass Schedule' box: Holy Redeemer (Saturday 4:30 pm; Sunday 8:15 am; Wednesday-Friday 7:00 am) and St. Anthony of Padua, Sheffield (Sunday 11:00 am). The 25 Oct issue's intentions page lists Tuesday 7:00 am too, and the directory says Tuesday through Friday 7 a.m.; the bulletin's schedule box says Wednesday-Friday. The disagreement is on weekday Masses only and does not change the church list. St. Joseph, Warren (a separate parish and bulletin; see its `publication_reviews`) is not in this masthead.

## Website and bulletin provider

`parishes_online`, org `holy-redeemer-church-16365`. The parish's own domain holyredeemerwarren.com returns 403 to `probe url` and a Cloudflare challenge to headed Chrome on every one of eight loads, so it cannot be read here; the ParishesOnline org record names that domain as its website, which ties the org to this parish. The issue was posted two days early (25 October when read on 23 October), so `fetch:check` may report freshness `future`.

## Not yet confirmed

Whether the parish's own site hosts anything the ParishesOnline issue does not (it was not readable). No evidence it does.
