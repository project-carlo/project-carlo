---
name: Parish of the Transfiguration, Newark
website: https://www.transfigurationparishnwk.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: 'Parish Mission Partners: Transfiguration and St. Antoninus, Newark'
evidence:
- url: https://www.transfigurationparishnwk.org/
  seen: 2026-11-04
  quote: Parish of the Transfiguration, 103 16th Avenue - Newark, NJ 07103
  note: 'Wix site (probe url: platform wix, no publications, no bulletin links). Menu: Home, About, Sacraments,
    Staff, Ministries, Groups, Links, Blog. ''Church Schedule'' box: Mass Monday-Friday 6:00 pm, Saturday
    10:30 am, Sunday Spanish 8:00 am, English 10:00 am, Spanish 12:00 pm. No bulletin link on any page;
    the blog''s newest post is 5 September 2023 (blog-feed.xml).'
- url: https://www.transfigurationparishnwk.org/about
  seen: 2026-11-04
  quote: St. Ann’s Church is Parish Church of the Catholic Parish of the Transfiguration
  note: The page says St. Ann's and St. Rocco's merged as the Parish of the Transfiguration on 1 July
    2005 and the archbishop 'allowed us to continue with the two worship sites'.
- url: https://www.transfigurationparishnwk.org/staff
  seen: 2026-11-04
  quote: Fr. Josephat Kalema, STD
  note: Pastor Fr. Josephat Kalema; St. Antoninus's pastor is Rev. Joseph A. Meagher (its 23 November
    2025 bulletin), so the two Mission Partners parishes have different pastors.
- url: https://church-bulletin.org/585
  seen: 2026-11-04
  quote: Transfiguration Church Bulletin
  note: 'John Patrick listing transfiguration-church-newark-nj-07103 (contact address 212 Hunterdon Street,
    St. Rocco''s): only the week''s USCCB readings, no bulletin PDFs. Suffixes 585A, 585B, 585O, 585S,
    585L show only the generic archive page. jppc.net/onlinebulletins/585template.pdf redirects to the
    same listing.'
- url: https://rcan.org/wahw-june-2026-letter-cardinal-tobin/
  seen: 2026-11-04
  quote: Parish of the Transfiguration, Newark
  note: Listed with St. Antoninus Parish, Newark among the June 2026 Parish Mission Partners pilot parishes.
revisit: Recheck church-bulletin.org/585 and the parish site for a bulletin; if one appears, set provider
  other with page-pdfs on the listing, read its masthead for the worship sites (St. Ann's, St. Rocco's),
  and run fetch:check.
revisit_after: 2027-02-01
research:
- method: probe url and probe get on the parish site (home, about, sacraments, staff, links, blog, blog-feed.xml)
  url: https://www.transfigurationparishnwk.org/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Recheck the site menu for a bulletin page
  retry_when: Revisit date or the site changes
  revisit_after: 2027-02-01
- method: John Patrick listing church-bulletin.org/585 (and suffixes A, B, O, S, L); Run scan output (scratch/newark-map-1/029-map/jp-*.tsv)
    grepped for transfig, 07103 and newark
  url: https://church-bulletin.org/585
  checked: '2026-11-04'
  outcome: not-found
  next_action: Recheck church-bulletin.org/585 for posted PDFs
  retry_when: Revisit date
  revisit_after: 2027-02-01
- method: probe po transfiguration-church-07103 and -7103
  checked: '2026-11-04'
  outcome: not-found
  next_action: None unless a ParishesOnline link appears
  retry_when: The parish site or a masthead names ParishesOnline
- method: Read St. Antoninus's channels for a shared Mission Partners bulletin (its last online bulletin,
    23 November 2025, names St. Antoninus alone)
  url: https://www.saintantoninuschurch.org/
  checked: '2026-11-04'
  outcome: not-found
  next_action: If the partners start a joint bulletin, read its masthead and link this row
  retry_when: Either parish's site links a bulletin
bulletin_status: not-found
---

## Publisher

No bulletin found. The parish has a John Patrick account (church-bulletin.org/585, 'Transfiguration Church Bulletin', contact address 212 Hunterdon Street, the St. Rocco church) but on 4 November 2026 the listing showed only the week's readings and no issues, which is a parish posting nothing (playbook). The parish website links no bulletin. ParishesOnline has no org under the usual slugs.

The parish is a June 2026 'Parish Mission Partners' pilot with St. Antoninus (rcan.org June 2026 letter). The two have different pastors (Fr. Josephat Kalema here; Rev. Joseph A. Meagher at St. Antoninus) and St. Antoninus's last online bulletin (23 November 2025) names St. Antoninus alone. No joint bulletin was found; separate rows.

## Worship sites

- St. Ann's, 103 16th Avenue (`st-ann-newark`): the parish church (about page: 'St. Ann’s Church is Parish Church of the Catholic Parish of the Transfiguration'); the homepage's single 'Church Schedule' gives Mass Monday-Friday 6:00 pm, Saturday 10:30 am, Sunday 8:00 am (Spanish), 10:00 am (English), 12:00 pm (Spanish), under the 103 16th Avenue address. St. Antoninus's 21 November 2025 newsletter says the Christ the King procession 'will conclude at their church on 16th Ave'.
- St. Rocco's, 212 Hunterdon Street: the second worship site kept at the 2005 merger, and GCatholic's 18511. No current source shows Mass there or says it closed; the website's schedule names no building. Recorded in `open/st-rocco-newark`.

## Website and bulletin provider

https://www.transfigurationparishnwk.org/ is the parish's Wix site (directory 138's website). `no_bulletin`, with research and a revisit, so the row and its churches stay in the records but off the site (Settled policy 4).

## Not yet confirmed

Whether St. Rocco's still holds Mass (open record). Whether the Mission Partners begin a joint bulletin. See research.
