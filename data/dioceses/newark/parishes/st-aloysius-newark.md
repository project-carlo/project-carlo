---
name: St. Aloysius, Newark
website: https://www.saintaloysiusnewark.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:st-aloysius-church-07105', 'lpi:0018000000QxAAuAAN']
group: ''
evidence:
- url: https://www.saintaloysiusnewark.org/
  seen: 2026-11-04
  quote: 8:30am - English mass
  note: 'Wix homepage, ''Saint Aloysius Church, a place of worship in the Ironbound'', 66 Fleming Ave.
    Divine Worship Times: Sunday 8:30 AM English, 9:30 AM Portuguese, 11:30 AM Spanish; Saturday 5:00
    PM English; Thursday 7:30 PM Portuguese. Menu: Home, About, Sacraments, Ministries, Donations, Contact;
    no bulletin link or PDF. Links ''Saint Benedict RCC - our sister parish''.'
- url: https://www.saintaloysiusnewark.org/contact
  seen: 2026-11-04
  quote: Rev. Elky Reyes, Pastor
  note: The same pastor as St. Benedict's contact page.
- url: https://parishesonline.com/organization/st-aloysius-church-07105
  seen: 2026-11-04
  note: 'probe po: org ''St. Aloysius Church'', 66 Fleming Ave, Newark 07105, website saintaloysiusnewark.com,
    lpi 0018000000QxAAuAAN, no publications (''this organization does not publish a bulletin here now'').'
- url: http://web.archive.org/cdx/search/cdx?url=saintaloysiusnewark.com&matchType=prefix
  seen: 2026-11-04
  note: The old WordPress site saintaloysiusnewark.com (now redirecting to the Wix .org site) had a /bulletin/
    page captured 2019-11-14; no bulletin PDF captures.
revisit: Recheck the ParishesOnline org st-aloysius-church-07105 and the Wix site for a bulletin; if one
  appears, check whether it also covers St. Benedict (same pastor).
revisit_after: 2027-02-04
research:
- method: probe url / probe get on the Wix site (home, about, contact, ministries, sacraments)
  url: https://www.saintaloysiusnewark.org/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Reread the site for a Bulletin page or PDF
  retry_when: The site's menu gains a bulletin link
  revisit_after: 2027-02-04
- method: probe po on the ParishesOnline org; John Patrick scans (029-map jp-*.tsv) grepped for Aloysius,
    Newark and 07105; DuckDuckGo html search for St. Benedict/St. Aloysius Newark bulletin
  url: https://parishesonline.com/organization/st-aloysius-church-07105
  checked: '2026-11-04'
  outcome: not-found
  next_action: Rerun probe po st-aloysius-church-07105 for new publications
  retry_when: The org lists a publication, or a printer's listing names St. Aloysius Newark
  revisit_after: 2027-02-04
bulletin_status: not-found
---

## Publisher

No current bulletin found. St. Aloysius's Wix site (read 4 November 2026) has no bulletin page or PDF. Its ParishesOnline org (st-aloysius-church-07105) exists with no publications. No John Patrick listing in the Run's scans names St. Aloysius, Newark: the Aloysius listings are Caldwell 691 and Jersey City 6058, and the 07105 listings are St. James 655, Our Lady of Mount Carmel 6017 and St. Casimir 6033. The old WordPress site saintaloysiusnewark.com had a /bulletin/ page in 2019 (Wayback CDX), with no PDF captures.

St. Aloysius and St. Benedict share a pastor: both contact pages name 'Rev. Elky Reyes, Pastor', and each homepage links the other as 'our sister parish'. I looked for one shared bulletin and found none for either parish. They are kept as two rows because they have separate sites, separate Mass schedules and separate ParishesOnline orgs. If a bulletin turns up, read its masthead to see whether it covers both.

## Worship sites

One church, `st-aloysius-newark` (66 Fleming Avenue): Saturday 5:00 PM English; Sunday 8:30 AM English, 9:30 AM Portuguese, 11:30 AM Spanish; Thursday 7:30 PM Portuguese, per the homepage. The directory (146) and GCatholic (18497) each list only this church.

## Website and bulletin provider

The website is the parish's Wix site https://www.saintaloysiusnewark.org/ (the directory's saintaloysiusnewark.com redirects to it). The provider is `no_bulletin` (Settled policy 4 keeps the row off the site). No fetch check was run, since there is no bulletin to check. The ParishesOnline ids stay in `publication` because they are this parish's account.

## Not yet confirmed

Whether the parish prints a bulletin that is handed out but not posted online. See research and `revisit_after`.
