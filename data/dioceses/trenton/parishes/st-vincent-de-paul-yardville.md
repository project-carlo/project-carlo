---
name: St. Vincent de Paul Parish
website: https://www.church-bulletin.org/saint-vincent-de-paul-parish-yardville-nj-08620
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-vincent-de-paul-parish-yardville-nj-08620
publication: ['url:https://www.church-bulletin.org/saint-vincent-de-paul-parish-yardville-nj-08620']
group: Cohort 27 (Yardville, Allentown; linkage delayed)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-vincent-de-paul-parish-yardville-nj-08620/2026-10-25.pdf
  seen: 2026-10-30
  quote: Rev. Stanley Krzyston, Pastor
  note: '4-page issue of 25 October 2026 (text layer). Page 1: ''St. Vincent de Paul Parish, 555 Yardville
    Allentown Road, Yardville, NJ 08620'', Rectory 609-585-6470, ''Rev. Stanley Krzyston, Pastor'', ''Rev.
    Rogatus Mpeka, Parochial Vicar''; Masses: Saturday Vigil 4:00 PM, Sunday 7:30, 9:30 & 11:30 AM & 4:00
    PM, weekdays 9:00 AM Tuesday, Thursday, Friday, Saturday and 4:00 PM Wednesday. The text layer also
    holds a stale ''JUNE 30, 2019 / THE THIRTEENTH SUNDAY IN ORDINARY TIME'' line from an old template,
    next to the real ''OCTOBER 25, 2026''. No mention of St. John or Allentown''s parish.'
- url: https://www.church-bulletin.org/bulletin/saint-vincent-de-paul-parish-yardville-nj-08620/2026-11-01.pdf
  seen: 2026-10-30
  note: '1 November 2026 issue, 4 pages. Its text layer is font-garbled (glyph codes, not words), so I
    rendered page 1: same masthead, Pastor Rev. Stanley Krzyston, Masses Saturday Vigil 4:00 PM, Sunday
    7:30, 9:30 & 11:30 AM & 4:00 PM, weekdays 9:00 AM Tuesday, Thursday, Friday, Saturday and 4:00 PM
    Wednesday.'
- url: https://www.church-bulletin.org/saint-vincent-de-paul-parish-yardville-nj-08620
  seen: 2026-10-30
  quote: Latest Edition November 1, 2026 Bulletin
  note: John Patrick Publishing listing 6044, 'Saint Vincent de Paul Parish, Yardville, NJ 08620', 555
    Yardville Allentown Road, phone (609) 585-6470; weekly archive.
- url: https://svdpnj.org/
  seen: 2026-10-30
  note: 'The finder''s website for the parish. It does not load: probe url, probe get and the browser
    all fail the TLS check (''certificate is not valid for svdpnj.org'', ERR_CERT_COMMON_NAME_INVALID,
    also for www. and over http://). The bulletin''s own email domain is svdpnj.org, so the domain is
    the parish''s but its site cannot be read.'
promoted: 2026-10-30
research:
- method: pnpm fetch:check --diocese trenton --parish st-vincent-de-paul-yardville (headed Chrome); page-pdfs
    on https://www.church-bulletin.org/saint-vincent-de-paul-parish-yardville-nj-08620
  url: https://www.church-bulletin.org/saint-vincent-de-paul-parish-yardville-nj-08620
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: it picked the 1 November 2026 issue (garbled text layer, ''future'' freshness; identity
    read by rendering page 1).'
- method: probe url, probe get and visit.py on svdpnj.org, www.svdpnj.org, http and https
  url: https://svdpnj.org/
  checked: '2026-10-30'
  outcome: access-blocked
  next_action: Reread the parish site if its certificate is fixed; the John Patrick listing 6044 is the
    bulletin meanwhile.
  retry_when: svdpnj.org serves a certificate valid for its name
bulletin_status: available
publication_reviews:
- parish: st-john-the-baptist-allentown-nj
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-vincent-de-paul-parish-yardville-nj-08620/2026-10-25.pdf
    seen: 2026-10-30
    note: The 25 October 2026 masthead names St. Vincent de Paul Parish alone (pastor Rev. Stanley Krzyston,
      555 Yardville Allentown Road), with its own Mass times. (John Patrick 6044)
  - url: https://www.stjohnromancatholic.org/sjrc/News%20%26%20Bulletins/October%2025%2C%202026%20Bulletin.pdf
    seen: 2026-10-30
    note: The 25 October 2026 masthead names Saint John the Baptist Roman Catholic Church, Allentown alone
      (pastor Very Rev. Michael Wallack, 1282 Yardville-Allentown Road), with its own Holy Mass schedule.
---

## Publisher

St. Vincent de Paul Parish, Yardville in Hamilton Township (Cohort 27 in the July 2024 list, marked "*linkage delayed", with St. John the Baptist, Allentown). It publishes its own bulletin through John Patrick Publishing (listing 6044). The 2017 decisions planned a Linkage Model (one pastor) for St. John and St. Vincent de Paul "no later than July 1, 2019"; it had not happened by 25 October 2026: this bulletin's pastor is Rev. Stanley Krzyston and St. John's is Very Rev. Michael Wallack, and neither bulletin mentions the other parish. Even a linkage would keep separate parishes; one row would need a masthead naming both.

## Worship sites

One church, St. Vincent de Paul, 555 Yardville Allentown Road (the bulletin says Yardville; the finder and GCatholic say Hamilton, same street number). All Masses in the bulletin are at that address.

## Website and bulletin provider

The row's `website` is the John Patrick listing because the parish's own site, svdpnj.org (the finder's and GCatholic's address for it), fails TLS verification in every client. See research.
