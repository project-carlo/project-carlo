---
name: St. Michael Parish
website: https://www.stmichaelgreenville.com/weeklybulletin.php
bulletin_provider: other
provider_id: page-pdfs https://www.stmichaelgreenville.com/weeklybulletin.php
publication: ['url:https://www.stmichaelgreenville.com/weeklybulletin.php#st-michael-greenville']
group: ''
evidence:
- url: https://www.stmichaelgreenville.com/images/weeklybulletin/33770ebd1c9593e74521095fbe7e713a.pdf
  seen: 2026-10-23
  quote: Saint Margaret, Mission
  note: 'Page 2 (page 1 is an image-only cover showing the Saint Michael Catholic Parish logo) of the
    issue dated Sunday, October 25, 2026 (4 pages): ''Saint Michael Roman Catholic Parish, 85 North High
    Street, Greenville, PA 16125 (724) 588-9800; Saint Margaret, Mission, 701 Denver Street, Jamestown,
    PA 16134''; MASS TIMES ''Tuesday-Friday, 9:00am (Saint Michael); First Saturday, 9:00am (Saint Michael);
    Saturday, 4:30pm (Saint Michael); Sunday, 8:00am (Saint Margaret); Sunday, 11:00am (Saint Michael)'';
    ''Father Thomas Trocchio, Pastor''. Names this parish and its mission alone.'
- url: https://www.stmichaelgreenville.com/weeklybulletin.php
  seen: 2026-10-23
  note: 'Diocese-hosted page (scratch/map-erie/tools/weeklybulletin_issues.sh), newest first: October
    25, 2026 (33770ebd...pdf), October 18 (bec2bd07...), October 11 (d663e00f...), October 4 (0e2875fe...):
    four distinct PDFs (md5 a36d82e3, bb226eab, 2487c1aa, a6795792), the 25 October issue posted two days
    early. No ParishesOnline or LPi id on the site (probe url).'
- url: https://www.stmichaelgreenville.com/
  seen: 2026-10-23
  quote: 'two worship sites: Saint Michael Church, Greenville and Saint Margaret Mission, Jamestown'
  note: 'Home page: Mass Times Saturday vigil 4:30 p.m.; Sunday St Margaret 8:00 a.m., St Michael 11:00
    a.m. No mention of Thiel College or a campus Mass.'
- url: https://www.eriercd.org/Parish31114-St-Michael.html
  seen: 2026-10-23
  note: 'Directory record 31114: 85 N. High St., Greenville; clergy ''Pastor: Rev. Thomas Trocchio; Deacons
    Martin Aubel, Frank Luciani'' (matches the bulletin; the locator''s ''Rev. Brandon Kleckner'' is stale;
    the clergy PDF lists Kleckner at Fryburg, Lucinda, Crown). Mission 31122 St. Margaret is its ''secondary
    mission church'' in the city list.'
research:
- method: Grepped the four issues on weeklybulletin.php (4-25 October 2026) for Thiel, college, campus,
    university; read the home page; one DuckDuckGo search for Thiel Catholic campus Mass
  url: https://www.stmichaelgreenville.com/weeklybulletin.php
  checked: '2026-10-23'
  outcome: not-found
  next_action: 'If a bulletin issue lists a Thiel College Mass, apply the campus rule (church row under
    this parish). Evidence seen: a 1 December 2022 Thiel calendar event ''Celebrate Catholic Mass with
    Fr. Brandon Kleckner of St. Michael''s Parish'' (iqweb.thiel.edu), not a current schedule.'
  retry_when: A St. Michael bulletin or the parish site lists a Thiel campus Mass, or Thiel's spiritual-life
    page gives a current Mass time
- method: pnpm fetch:check --diocese erie --parish st-michael-greenville --expected-identity Trocchio
    (headed Chrome)
  url: https://www.stmichaelgreenville.com/weeklybulletin.php
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Resolver page-pdfs on weeklybulletin.php picked 33770ebd...pdf (25 October 2026):
    transport ok, PDF, 4.3 MB. Identity and issue date read unknown only because page 1 is an image-only
    cover (masthead text is on page 2, read by hand); overall unverified for that reason alone. Recipe
    is the provider_id.'
---

## Publisher

St. Michael Parish, Greenville publishes its own weekly bulletin on its diocese-hosted site (`weeklybulletin.php`, one PDF per issue under `images/weeklybulletin/`). The issue dated 25 October 2026 (page 1 is an image-only cover; masthead on page 2), read on 2026-10-23, is headed 'Saint Michael Roman Catholic Parish, 85 North High Street, Greenville' and 'Saint Margaret, Mission, 701 Denver Street, Jamestown', with Father Thomas Trocchio as pastor and one combined Mass-times box.

## Worship sites

Two churches: St. Michael (85 N. High St., Greenville) and its mission St. Margaret (701 Denver St., Jamestown, Sunday 8:00am). The directory lists St. Margaret as a 'secondary mission church' under this parish; GCatholic lists it separately. The bulletin has no other Mass site.

**Thiel College (Greenville).** The brief said campus ministry at Thiel is served from St. Michael. None of the four October 2026 issues, nor the parish home page, lists a Thiel campus Mass (grep for Thiel, college, campus, university found only the Saint Margaret lines). The only source found is a 2022 Thiel calendar event of a Mass celebrated by Fr. Kleckner, then pastor here. So no campus church row: the campus rule applies only when a bulletin lists a weekly campus Mass. See research for the retry trigger.

## Website and bulletin provider

`other` with recipe `page-pdfs https://www.stmichaelgreenville.com/weeklybulletin.php` (newest first). The site embeds no ParishesOnline or LPi org. Parish facebook/YouTube livestream pages exist but are not bulletins.

## Not yet confirmed

Thiel campus Mass (above). The `fetch:check` result is recorded in research once run.
