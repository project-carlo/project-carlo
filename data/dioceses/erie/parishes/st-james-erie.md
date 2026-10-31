---
name: St. James Parish
website: https://saintjamesrcc.org
bulletin_provider: parishes_online
provider_id: saint-james-roman-catholic-church
publication: ['po-org:saint-james-roman-catholic-church', 'lpi:0018000000Qc1NwAAJ', 'po-container:14/1107']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/1107/20261025B.pdf
  seen: 2026-10-23
  quote: St. James, Erie, PA 14-1107
  note: 'Footer of pages 7 and 8 (the only text-layer pages) of the 25 October 2026 issue, container 14/1107.
    Pages 1-6 are images with no text layer; I rendered page 1 with pdftoppm and read it: masthead ''Saint
    James Roman Catholic Parish, 2635 Buffalo Road, Erie, Pa. 16510, 814-899-6178'', dated ''October 25,
    2026''; Weekend Masses ''Saturday 5:00 PM, & 7:00 PM; Sunday 7:30, 9:30 at St. Mark, 11:30, and 5:00
    PM''; weekday ''Monday - Friday 7:00 AM, Saturday - 8:00 AM''; a ''St. Mark Church, 695 Smithson Ave.,
    Erie, Pa. 16511'' box; footer ''St. James Parish: united in the Heart of Christ and embracing the
    faith families of Mt. Calvary, St. James, St. Mark the Evangelist and all others who enter our doors.''
    Page 2 (rendered) lists weekly Mass intentions including ''Sunday, November 1 ... SJ 9:30'' in red
    and ''Holy Hours 11:00 at St. James & 6:30 at St. Mark'' on Wednesday 28 October (holy hours, not
    Masses).'
- url: https://parishesonline.com/organization/saint-james-roman-catholic-church
  seen: 2026-10-23
  note: 'probe po: organization ''Saint James Roman Catholic Church'', 2635 Buffalo Rd, Erie PA 16510,
    website www.saintjamesrcc.org, LPi 0018000000Qc1NwAAJ, container 14/1107, latest issue 2026-10-25.
    probe url on http://www.saintjamesrcc.org/ redirects to https://saintjamesrcc.org/ and finds the same
    po-org embedded.'
- url: https://www.eriercd.org/Parish10209-St-James.html
  seen: 2026-10-23
  note: 'Diocese directory record 10209 (GCatholic 24511). Locator Mass times: ''Sat: 5, 7 p.m. ... Sun:
    7:30, (9:30 at St. Mark), 11:30 a.m.; 5 p.m.''. Mission record 10212 (St. Mark the Evangelist) is
    its secondary mission church; its website is this same site.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: McCormick, Rev. James P.
  note: 'Clergy list ''Updated 8/7/2026'': ''Pastor ... St. James, Erie, 2635 Buffalo Road''. He is the
    pastor of this parish alone (no other assignment listed).'
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese erie --parish st-james-erie (headed Chrome), with --expected-identity
    James and 14-1107
  url: https://parishesonline.com/organization/saint-james-roman-catholic-church
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF signature (container 14/1107, 20261025B.pdf), issue date 2026-10-25
    inferred from the URL, freshness 'future' only because it posts two days early. Publication identity
    reads 'unknown' because pages 1-6 are images with no text layer; I confirmed the masthead by rendering
    page 1 (see evidence).
---

## Publisher

St. James Parish, Erie (Buffalo Road, 16510) publishes its own weekly bulletin through ParishesOnline (organization `saint-james-roman-catholic-church`, container 14/1107). I read the 25 October 2026 issue on 2026-10-23: pages 1-6 are images (no text layer), so I rendered page 1 and read the masthead 'Saint James Roman Catholic Parish, 2635 Buffalo Road' with its Mass times. The bulletin covers the whole merged parish: it lists St. James weekend Masses and 'Sunday ... 9:30 at St. Mark' and prints a box for St. Mark Church at 695 Smithson Ave. The parish's website embeds the same organization.

In July 2024 Mount Calvary and St. Mark the Evangelist (Lawrence Park) were merged into St. James by decree ('Merging Mount Calvary and St. Mark the Evangelist into St. James Erie'); the diocese lists St. Mark as a 'Secondary Mission' church of St. James and Mount Calvary no longer has Mass. Pastor: Rev. James P. McCormick (clergy list, updated 8/7/2026). No other parish row is needed for St. Mark or Mount Calvary: St. Mark's old website `stmarkslp.org` (GCatholic's) is dead (DNS) and the directory gives St. Mark the St. James website.

## Worship sites

Two churches with public Mass: St. James (2635 Buffalo Rd) and St. Mark the Evangelist (695 Smithson Ave, 9:30 a.m. Sunday and a 5:30 p.m. holy day Mass). Mount Calvary (2022 E Lake Rd) is excluded as closed: regularly scheduled Masses ceased there in July 2024 and the church was relegated effective 2025-03-10 (see `excluded/mount-calvary-erie`). The directory also lists St. Mark as a 'Secondary Mission'; the bulletin's Sunday 9:30 Mass confirms it holds Mass.

## Website and bulletin provider

`saintjamesrcc.org` is the parish website; it embeds the ParishesOnline organization and hosts no bulletin PDFs of its own. All three ids (po-org, LPi, container 14/1107) are one bulletin. The 25 Oct issue was available two days early (issues post ahead).

## Not yet confirmed

Whether the 9:30 St. Mark Mass is the only Sunday Mass there and whether weekday Masses happen there (the bulletin gives weekday Masses without a site; the directory lists them 'At St. James'). The page-1 masthead is an image, so `recheck` can't find it; the quoted footer is the text-layer proof of the container.
