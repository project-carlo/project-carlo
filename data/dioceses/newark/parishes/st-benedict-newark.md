---
name: St. Benedict, Newark
website: https://www.saintbenedictnewark.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:st-benedict-church-07105', 'lpi:0018000000Qc0DFAAZ']
group: Planning Area I
evidence:
- url: https://www.saintbenedictnewark.org/
  seen: 2026-11-04
  quote: 12:30PM (Spanish)
  note: 'Wix homepage, ''Saint Benedict Roman Catholic Church ... A place of worship in the Ironbound'',
    65 Barbara Street. Divine Worship Times: weekdays 8:00 AM (English), 7:00 PM (Portuguese); Saturday
    5:00 PM (English); Sunday 9:00 AM (Portuguese), 11:00 AM (English), 12:30 PM (Spanish). Menu: Home,
    About, Sacraments, Ministries, Donations, Contact; no bulletin link or PDF. Links ''Saint Aloysius
    RCC - our sister parish''.'
- url: https://www.saintbenedictnewark.org/contact
  seen: 2026-11-04
  quote: Rev. Elky Reyes, Pastor
  note: Also lists Rev. Jose Arturo Ortiz, Parochial Vicar, and Rev. Gabriel Costa, Weekend Assistant.
    St. Aloysius's contact page names the same pastor.
- url: https://parishesonline.com/organization/st-benedict-church-07105
  seen: 2026-11-04
  note: 'probe po: org ''St. Benedict Church'', 65 Barbara St, Newark 07105, website saintbenedictnewark.org,
    lpi 0018000000Qc0DFAAZ, no publications (''this organization does not publish a bulletin here now'').
    A web search shows a 7 February 2016 ParishesOnline upload ''St. Benedict''s Newark, V Sunday of Ordinary
    Time C'', so the parish printed with LPi then.'
- url: http://web.archive.org/cdx/search/cdx?url=saintbenedictnewark.com&matchType=prefix
  seen: 2026-11-04
  note: The old WordPress site saintbenedictnewark.com (now redirecting to the Wix site) had a /bulletin/
    page (captured 2019) and one upload, wp-content/uploads/2020/08/08-23-2020.pdf, which is a one-page
    USCCB 'Catholic Current' insert (image, rendered), not a parish bulletin.
revisit: Recheck the ParishesOnline org st-benedict-church-07105 and the Wix site for a bulletin; if one
  appears, check whether it also covers St. Aloysius (same pastor).
revisit_after: 2027-02-04
research:
- method: probe url / probe get on the Wix site (home, about, contact, ministries, sacraments)
  url: https://www.saintbenedictnewark.org/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Reread the site for a Bulletin page or PDF
  retry_when: The site's menu gains a bulletin link
  revisit_after: 2027-02-04
- method: probe po on the ParishesOnline org; John Patrick scans (029-map jp-*.tsv) grepped for Benedict,
    Newark and 07105; DuckDuckGo html search for St. Benedict/St. Aloysius Newark bulletin
  url: https://parishesonline.com/organization/st-benedict-church-07105
  checked: '2026-11-04'
  outcome: not-found
  next_action: Rerun probe po st-benedict-church-07105 for new publications
  retry_when: The org lists a publication, or a printer's listing names St. Benedict Newark
  revisit_after: 2027-02-04
bulletin_status: not-found
---

## Publisher

No current bulletin found. St. Benedict's own Wix site (read 4 November 2026) has no bulletin page or PDF; its ParishesOnline org (st-benedict-church-07105) exists with no publications, though a 7 February 2016 LPi upload 'St. Benedict's Newark' shows the parish once printed there. No John Patrick listing in the Run's scans names St. Benedict, Newark (the 07105 listings are St. James 655, Our Lady of Mount Carmel 6017 and St. Casimir 6033). The old WordPress site saintbenedictnewark.com had a /bulletin/ page in 2019, and its only PDF upload seen (23 August 2020) is a USCCB insert.

St. Benedict and St. Aloysius share a pastor: both contact pages name 'Rev. Elky Reyes, Pastor', and each homepage links the other as 'our sister parish'. I looked for one shared bulletin and found none for either parish. They are kept as two rows because they have separate sites, separate Mass schedules and separate ParishesOnline orgs. If a bulletin turns up, read its masthead to see whether it covers both.

## Worship sites

One church, `st-benedict-newark` (65 Barbara Street): weekdays 8:00 AM (English), 7:00 PM (Portuguese); Saturday 5:00 PM; Sunday 9:00 AM (Portuguese), 11:00 AM (English), 12:30 PM (Spanish), per the homepage. The directory (147) and GCatholic (18501) each list only this church.

## Website and bulletin provider

The website is the parish's Wix site https://www.saintbenedictnewark.org/ (GCatholic's address; saintbenedictnewark.com redirects to it; the directory gives none). The provider is `no_bulletin` (Settled policy 4 keeps the row off the site). No fetch check was run, since there is no bulletin to check. The ParishesOnline ids stay in `publication` because they are this parish's account.

## Not yet confirmed

Whether the parish prints a bulletin that is handed out but not posted online. See research and `revisit_after`.
