---
name: Holy Cross Parish
website: https://www.hcsjchurches.org
bulletin_provider: parishes_online
provider_id: holy-cross-catholic-church
publication: ['po-org:holy-cross-catholic-church', 'po-org:the-parish-of-st-john-the-evangelist', 'lpi:0018000000QxBkFAAV',
  'lpi:0018000000QxBkHAAV', 'po-container:14/1073']
group: Holy Cross (10302) and St. John the Evangelist (10308), Rev. Scott Detisch
evidence:
- url: https://container.parishesonline.com/bulletins/14/1073/20261025B.pdf
  seen: 2026-10-23
  quote: 'Two Households: One Family of Faith'
  note: 'Page 1 of the 25 October 2026 issue (container 14/1073, 6 pages). Masthead: ''ROMAN CATHOLIC
    CHURCHES Holy Cross & St. John the Evangelist'', Holy Cross 7100 W. Ridge Road, St. John the Evangelist
    1001 Main Street E; Rev. Scott P. Detisch, Ph.D., Pastor. One bulletin names both churches.'
- url: https://container.parishesonline.com/bulletins/14/1073/20261025B.pdf
  seen: 2026-10-23
  quote: Holy Cross & St. John the Evangelist
  note: 'Page 1 liturgy schedule for both: Saturday vigil 4:30pm at St. John''s June 1-November 30 and
    Holy Cross December 1-May 31; Sunday 8:30 a.m. at St. John''s, 10:30 a.m. at Holy Cross; weekdays
    Tuesday/Friday 8:00 a.m. Holy Cross, Wednesday/Thursday 8:00 a.m. St. John''s.'
- url: https://parishesonline.com/organization/the-parish-of-st-john-the-evangelist
  seen: 2026-10-23
  note: 'probe po the-parish-of-st-john-the-evangelist (LPi 0018000000QxBkHAAV, 1001 Main St E, website
    stjohngirard.org): publication ids include po-container:14/1073 and latest issue 2026-10-25, the same
    container and the same six issues (2026-09-20 to 10-25) as probe po holy-cross-catholic-church (LPi
    0018000000QxBkFAAV, 7100 W Ridge Rd, website hc-parish.org). Two org records, one container.'
- url: https://www.hcsjchurches.org/weeklybulletin.php
  seen: 2026-10-23
  note: The shared site's diocese-hosted weeklybulletin.php lists only two non-bulletin PDFs ('2026-2027
    Faith Formation Schedule', 'Suggested Donation Christian Cupboard'); no weekly bulletins. Its probe
    url embeds po-org holy-cross-catholic-church and lpi 0018000000QxBkFAAV. So the page is not a second
    bulletin channel.
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  note: 'Clergy list ''Updated 8/7/2026'' (read by the surveyor, see diocese.md): S. Detisch is pastor
    of St. John, Girard and Holy Cross, Fairview. Directory records 10302 (Holy Cross) and 10308 (St.
    John, group ''Holy Cross Parish (10302)'') both give website hcsjchurches.org.'
research:
- method: pnpm fetch:check --diocese erie --parish holy-cross-fairview --expected-identity Detisch --expected-issue-date
    2026-10-25 (headed Chrome)
  url: https://parishesonline.com/organization/holy-cross-catholic-church
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF, identity matched on the pastor surname, issue date observed 2026-10-25;
    freshness reads future only because the Sunday issue is posted early.
---

## Publisher

Holy Cross (Fairview) and St. John the Evangelist (Girard) share one pastor, Rev. Scott P. Detisch, and publish **one** bulletin through ParishesOnline, container 14/1073. I read the 25 October 2026 issue on 2026-10-23: the masthead reads 'ROMAN CATHOLIC CHURCHES Holy Cross & St. John the Evangelist', lists both addresses, gives both parishes' office contacts and one liturgy schedule ('Two Households: One Family of Faith'), and the weekly Mass intentions cover both churches ('Wednesday October 28 - At St. John's Church', 'Saturday October 31 - At St. John's Church'). The two ParishesOnline organizations (holy-cross-catholic-church and the-parish-of-st-john-the-evangelist, each with its own LPi id) resolve to the same container and the same six issues, so this is one row with both organization ids recorded; the roster entries directory:10302 and directory:10308 are one publisher.

## Worship sites

Two churches, both with a recurring public Mass in the 25 October 2026 schedule: Holy Cross, 7100 W. Ridge Rd, Fairview, and St. John the Evangelist, 1001 Main St E, Girard (the former parish center, in use as the parish church since 2020 and made the parish church by decree in 2022). The old St. John church at 101 Olin Ave (GCatholic 24515) was relegated to profane but not sordid use effective 2022-07-17: see excluded/st-john-the-evangelist-olin-ave-girard.

## Website and bulletin provider

hcsjchurches.org is a diocese-hosted site that embeds the Holy Cross ParishesOnline organization; `fetch` reads the bulletin by provider_id. The site's own weeklybulletin.php carries only faith-formation fliers. GCatholic's websites for the two churches (holycrossfairview.org redirects to hc-parish.org, which shows the same org; saint-john-church.com is dead DNS) are not used.

## Not yet confirmed

Nothing outstanding on structure. The Saturday vigil location alternates seasonally (St. John's June-November, Holy Cross December-May); a reader of the bulletin in winter should see the vigil at Holy Cross.
