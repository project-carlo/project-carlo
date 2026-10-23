---
name: Saint James Parish and Saint Katharine Drexel Parish (Catholic Partner Parishes)
website: https://www.catholicpartnerparishes.org
bulletin_provider: ecatholic
provider_id: '20435'
publication: ['ecatholic:20435']
group: 'Catholic Partner Parishes: Saint James (Washington) and Saint Katharine Drexel (Bentleyville)'
evidence:
- url: https://files.ecatholic.com/20435/bulletins/20261025.pdf
  seen: 2026-10-23
  quote: SaintJ ames Parish & SaintK atharine Drexel Parish
  note: 'Page 1 (cover) of the 25 October 2026 issue (22 pages, letter-split text layer): masthead ''Catholic
    PartnerP arishes / SaintJ ames Parish & SaintK atharine Drexel Parish / Serving the Greater Washington
    County Area''. One issue, both parishes.'
- url: https://files.ecatholic.com/20435/bulletins/20261025.pdf
  seen: 2026-10-23
  quote: 'Sunday: 9:00 am –R icheyville Mission church'
  note: 'Page 2 of the same issue carries a Mass Schedules & Locations page for each parish. Saint James:
    Saturday Vigil 4:00 pm Immaculate Conception; Sunday 8:00 am Saint Hilary, 10:00 am and 12:00 pm Immaculate
    Conception; weekdays Mon-Fri 12:00 pm Immaculate Conception. Saint Katharine Drexel: Saturday Vigil
    4:00 pm Bentleyville Main church; Sunday 9:00 am Richeyville Mission church; Mon and Fri 9:00 am Bentleyville
    / Drexel Hall chapel; Tue and Thu 8:30 am Richeyville. The parish page''s Mass Times box (catholicpartnerparishes.org/catholic-partner-masses)
    adds Sunday 5:00 PM W&J College - Rossin Campus Center.'
- url: https://files.ecatholic.com/20435/bulletins/20261025.pdf
  seen: 2026-10-23
  note: 'Page 7 (Mass Intentions, an image, rendered): Sunday 25 Oct lists 8:00 am (H), 9:00 am (R), 10:00
    am (IC), 12:00 pm (IC) and ''5:00 pm (RCC)'', i.e. the Rossin Campus Center Mass; the legend defines
    (IC) Immaculate Conception, (R) Richeyville, (B) Bentleyville, (H) Saint Hilary, (SH) Sacred Heart,
    (RCC) Rossin Campus Center, 60 S. Lincoln Street, Washington, PA 15301 (W&J). The 25 Oct week has
    no (SH) Mass.'
- url: https://www.catholicpartnerparishes.org/
  seen: 2026-10-23
  note: Rendered in headed Chrome (visit.py --bulletin; probe url alone answers 403). Title 'Saint James
    Parish and Saint Katharine Drexel Parish - Washington and Bentleyville, PA', publication ecatholic:20435,
    bulletin page /bulletins listing files.ecatholic.com/20435/bulletins/<yyyymmdd>.pdf back to 2025.
    The parish's old domains www.stjameswashpa.org and www.katharinedrexelpgh.org both redirect here (visit.py,
    2026-10-23).
- url: https://diopitt.org/saint-james-parish
  seen: 2026-10-23
  note: Diocese parish pages for Saint James and Saint Katharine Drexel (https://diopitt.org/saintkatharinedrexelparish)
    both list Rev. Edward L. Yuhas, MDiv as Pastor and give www.catholicpartnerparishes.org as the website
    (directory roster, 2026-10-23).
- url: https://parishesonline.com/organization/saint-james-parish
  seen: 2026-10-23
  note: 'ParishesOnline org saint-james-parish (LPi 0018000000Qx7sSAAR, website stjameswashpa.org) has
    no issues: ''no publications: this organization does not publish a bulletin here now''. Not a channel;
    no Saint Katharine Drexel org in raw/lpi-catholic.tsv.'
- url: https://www.catholicpartnerparishes.org/bulletins
  seen: 2026-10-23
  note: 'Masthead check across the archive: issues 20250601, 20260104 and 20260614 (downloaded and read
    with pdftotext) all begin ''Catholic Partner Parishes / Saint James [Parish] & Saint Katharine Drexel
    Parish / Serving the Greater Washington County Area''. 74 issues from June 2025 to 25 Oct 2026 are
    in the archive, one per Sunday, none for either parish alone.'
research:
- method: 'pnpm fetch:check --diocese pittsburgh --parish catholic-partner-parishes-washington (headed
    Chrome): resolved the /bulletins page link'
  url: https://files.ecatholic.com/20435/bulletins/20261025.pdf
  checked: '2026-10-23'
  outcome: found
  next_action: 'None: eCatholic provider reads the site; reread masthead only if the parishes split their
    bulletin'
---

## Publisher

The two parishes publish one bulletin, so this is one row (Rules settled 3). The 25 October 2026 issue at https://files.ecatholic.com/20435/bulletins/20261025.pdf (read 2026-10-23) has the masthead "Catholic Partner Parishes / Saint James Parish & Saint Katharine Drexel Parish / Serving the Greater Washington County Area" and, on page 2, a separate Mass Schedules & Locations box for each parish. The same masthead heads the issues of 1 June 2025, 4 January 2026 and 14 June 2026, and the parish site's /bulletins archive holds one file per Sunday from June 2025 with no per-parish edition. Both diocese parish pages give the same pastor, Rev. Edward L. Yuhas, and the same website.

Publisher: the parishes' own eCatholic site (id 20435, catholicpartnerparishes.org), which posts `files.ecatholic.com/20435/bulletins/<yyyymmdd>.pdf` weekly. The footer says "View this bulletin online at www.DiscoverMass.com": a Discover Mass copy exists but was not looked for (same PDF; Discover Mass mirrors elsewhere in this diocese are byte-identical).

## Worship sites

Five buildings and one campus Mass hold Mass now (see each church record):

- Saint James Parish (Washington): Immaculate Conception, Saint Hilary, Sacred Heart in Claysville (no weekly Mass since the end of December 2025; occasional Masses, so a church row under Rules settled 2) and the W&J College Newman Center Mass at the Rossin Campus Center (Sunday 5:00 pm, printed in the bulletin's Mass Intentions).
- Saint Katharine Drexel Parish: Ave Maria (Bentleyville Main church) and Saint Agnes (Richeyville Mission church). The Drexel Hall chapel in Bentleyville (weekday Mass, Monday and Friday 9:00 am) is part of the Bentleyville campus, not a separate building worth its own row; noted on the Ave Maria record.

Ruled out (own records): Saint Thomas Aquinas (California) and Saint Michael the Archangel (Fredericktown), both sold; Saint Joseph (Roscoe) and Saints Mary and Ann (Marianna), closed by decree in March 2019 (2019 press). The California University of PA campus Mass is in `open/` (not printed in any bulletin; sources disagree on time and place).

## Website and bulletin provider

eCatholic, read from the site: `files.ecatholic.com/20435/bulletins/` downloads without a browser. The 74 issues from June 2025 were downloaded and read with pdftotext (the text layer of the 2026 issues is fine; the Mass Intentions page is mostly an image, so intentions need rendering, not grepping). Check run: see Not yet confirmed.

## Not yet confirmed

Fetch check (2026-10-23): ok, transport ok, PDF, 25 Oct 2026 issue (6.4 MB), freshness `future` because the issue is dated two days ahead; publication identity `unverified` by the tool (no expected identity), settled here by the masthead above. The Discover Mass listing id, if one is wanted as a second publication id, was not looked up. Open: the California University campus Mass (open/california-university-of-pa-campus-mass).
