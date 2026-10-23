---
name: St. John the Baptist Parish
website: https://stjohn-holyrosary-erie.org/
bulletin_provider: parishes_online
provider_id: st-john-the-baptist-church-16504
publication: ['po-org:st-john-the-baptist-church-16504', 'po-org:st-john-the-baptist-parish-holy-rosary-holy-trinity-partnered-parish',
  'lpi:0018000000Qc1QoAAJ', 'lpi:0018000000Qbz2OAAR', 'po-container:14/0962']
group: 'Erie partnership: St. John the Baptist, Holy Trinity (Holy Rosary a mission church); pastor Rev.
  James Piszker'
evidence:
- url: https://container.parishesonline.com/bulletins/14/0962/20261025B.pdf
  seen: 2026-10-23
  quote: Holy Rosary Mission Church
  note: 'Page 1 masthead of the 25 October 2026 issue (4 pages) names three places under one title: ''St.
    John the Baptist Parish, 509 E 26th Street'', ''Holy Trinity Parish, GPS Address Only: 2220 Reed Street''
    and ''Holy Rosary Mission Church, GPS Address ONLY: 1002 East 28th St.'', then one combined MASS SCHEDULE
    (daily 8 AM St. John Tue-Fri and Holy Trinity Mon/Tue/Thu/Fri; Saturday 4 PM Holy Trinity; Sunday
    8 AM St. John, 10:30 AM Holy Rosary, 10:30 AM Holy Trinity).'
- url: https://container.parishesonline.com/bulletins/14/0962/20261025B.pdf
  seen: 2026-10-23
  quote: Rev. James Piszker, Pastor
  note: 'Page 1 staff list: Pastor Piszker, Rev. Msgr. Daniel Magraw Senior Associate, Permanent Deacon
    Denis Coan; two office blocks (St. John''s/Holy Rosary 814-454-2873; Holy Trinity 814-456-0671).'
- url: https://container.parishesonline.com/bulletins/14/0962/20261025B.pdf
  seen: 2026-10-23
  quote: Page Two St. John the Baptist - Holy Rosary - Holy Trinity - Erie, PA
  note: Pages 2 and 3 carry the running header 'St. John the Baptist - Holy Rosary - Holy Trinity - Erie,
    PA'; the page 3 'Mass Intentions for the Week' lists SJB, HT and HR Masses in one table (e.g. '10:30
    am HR  For All Living & Deceased Parishioners', '10:30 am HT Living & Deceased Parishioners of Holy
    Trinity').
- url: https://holytrinityrc.org/
  seen: 2026-10-23
  note: 'Holy Trinity''s own site (probe url) embeds the same ParishesOnline widget as stjohn-holyrosary-erie.org:
    script https://widget.parishesonline.com/publications?id=543f3d6fad921a7a6a70f6e6206de3a83f2330be
    in both pages (curl, line 339 of each), and its Bulletin menu link goes to https://parishesonline.com/organization/st-john-the-baptist-church-16504.
    Its text reads ''We are the Roman Catholic Communities of Saint John the Baptist, Holy Rosary, and
    Holy Trinity in Erie, Pennsylvania.'' No bulletin of its own.'
- url: https://stjohn-holyrosary-erie.org/
  seen: 2026-10-23
  quote: St. John/Holy Rosary Bulletins
  note: Home page menu entry; the Bulletin link goes to the ParishesOnline organization st-john-the-baptist-church-16504
    (title 'St. John the Baptist Church', website www.sjberie.org, 509 E 26th St, latest issue 2026-10-25,
    container 14/0962).
- url: https://parishesonline.com/organization/st-john-the-baptist-parish-holy-rosary-holy-trinity-partnered-parish
  seen: 2026-10-23
  note: 'probe po: a second ParishesOnline organization, ''St. John the Baptist Parish, Holy Rosary Mission
    Church & Holy Trinity Partnered Parish'' (LPi 0018000000Qbz2OAAR, address 2701 East Avenue), lists
    the same container 14/0962 and the same issue URLs as st-john-the-baptist-church-16504 (checked 2026-10-25,
    10-18 and 10-11). Two organization records, one bulletin.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor ......................................................... 1) St. John the Baptist, Erie;
    2) Holy Trinity, Erie
  note: 'Clergy list ''Updated 8/7/2026'', entry Piszker, Rev. James E. (text layer; the dotted leader
    is longer in the PDF). Holy Rosary is not an assignment of its own: it is a mission church of St.
    John.'
- url: https://www.eriercd.org/images/directoryparishchurch.pdf
  seen: 2026-10-23
  quote: Partnered with Holy Trinity Parish, Erie
  note: 'Printable directory dated Oct. 6, 2026: St. John the Baptist Parish ''Partnered with Holy Trinity
    Parish, Erie''; Holy Rosary Church listed as ''Secondary Mission'' under it; Holy Trinity Parish ''Partnered
    with St. John the Baptist, Parish''.'
research:
- method: pnpm fetch:check --diocese erie --parish st-john-the-baptist-erie --expected-identity "Holy
    Rosary" --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://parishesonline.com/organization/st-john-the-baptist-church-16504
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF (container 14/0962, 20261025B.pdf), identity matched on page 1,
    issue date inferred 2026-10-25; freshness reads future only because the Sunday issue is posted two
    days early on 2026-10-23. An identity string of St. John the Baptist did not match because the text
    layer renders the ligature in Baptist as a replacement character; Holy Rosary matched.
publication_reviews:
- parish: st-luke-erie
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/14/0962/20261025B.pdf
    seen: 2026-10-23
    quote: Holy Rosary Mission Church
    note: 'Container 14/0962, 25 Oct 2026: masthead for St. John the Baptist, Holy Trinity and Holy Rosary
      under Rev. James Piszker; Mass-intention table lists only SJB, HT and HR.'
  - url: https://container.parishesonline.com/bulletins/14/1178/20261025B.pdf
    seen: 2026-10-23
    quote: Our Lady
    note: 'Container 14/1178, same date: masthead Saint Luke and Our Lady of Mt. Carmel Parishes, pastor
      Fr. Larry (Richards). Different container, masthead, pastor and content: two bulletins.'
---

## Publisher

St. John the Baptist, Holy Trinity and Holy Rosary (Erie) share one weekly bulletin, published through ParishesOnline (container 14/0962). I read the 25 October 2026 issue on 2026-10-23: the page 1 masthead names 'St. John the Baptist Parish', 'Holy Trinity Parish' and 'Holy Rosary Mission Church' together over one combined Mass schedule and the staff 'Rev. James Piszker, Pastor'; pages 2 and 3 are headed 'St. John the Baptist - Holy Rosary - Holy Trinity - Erie, PA' and list Mass intentions for all three places in one table. Holy Trinity does not publish a separate bulletin: holytrinityrc.org embeds the same ParishesOnline widget id as stjohn-holyrosary-erie.org and its Bulletin menu link is the st-john-the-baptist-church-16504 organization. So the three canonical units (two parishes and a mission church) are one row, per the one-bulletin rule.

Peer decision (shared): Holy Trinity Parish (directory 10202, GCatholic 24443) and Holy Rosary (directory 10201, GCatholic 24441) are folded into this row. No `publication_reviews` entry is recorded because a review needs a peer parish row and neither has one; the decision is in the evidence above. Not shared with the other Erie partnerships: the St. Luke / Our Lady of Mount Carmel row prints a different bulletin (container 14/1178, masthead 'Saint Luke and Our Lady of Mt. Carmel Parishes').

## Worship sites

Three churches, each named in the masthead with Mass: St. John the Baptist (509 E 26th St, Sunday 8 AM, weekdays Tue-Fri 8 AM), Holy Rosary (Sunday 10:30 AM) and Holy Trinity (Saturday 4 PM vigil, Sunday 10:30 AM 'based on the availability of Msgr. Daniel Magraw', weekdays Mon/Tue/Thu/Fri 8 AM). The 25 October issue's Mass intentions show Holy Trinity weekday Masses of 26, 27, 29 and 30 October as 'No Mass' (page 3), so the weekday Holy Trinity schedule is nominal that week. The task brief described Holy Rosary as 'merged into St. John'; the sources read here call it a 'Mission Church' of St. John (bulletin masthead) and 'Secondary Mission' (printable directory, 2026-10-06), and the bulletin shows a regular Sunday 10:30 AM Mass there, so it is an open church row. The directory's web record for St. John lists Sunday 8 AM only and puts the Saturday 4 PM Mass at Holy Trinity.

## Website and bulletin provider

Website: https://stjohn-holyrosary-erie.org/ (the directory's address for St. John; the Holy Trinity site holytrinityrc.org carries the same widget). Provider: parishes_online, organization st-john-the-baptist-church-16504 (LPi 0018000000Qc1QoAAJ, container 14/0962). A second organization record, st-john-the-baptist-parish-holy-rosary-holy-trinity-partnered-parish (LPi 0018000000Qbz2OAAR), points at the same container and issues, so all five ids are one bulletin.

## Not yet confirmed

Nothing open on identity or freshness. The directory pages disagree with each other and with the bulletin on who pastors (locator: Jacquel for St. John, Glover for Holy Trinity; detail page and clergy list: Piszker); the clergy list ('Updated 8/7/2026') and the bulletin masthead agree on Piszker, so I followed them.
