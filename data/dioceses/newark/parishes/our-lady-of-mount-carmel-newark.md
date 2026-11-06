---
name: Our Lady of Mount Carmel, Newark
website: https://mountcarmelnewark.com/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6017
publication: ['url:https://church-bulletin.org/6017#john-patrick']
group: ''
evidence:
- url: https://church-bulletin.org/6017
  seen: 2026-11-04
  quote: Our Lady of Mount Carmel (Chiesa della Madonna del Carmine)
  note: John Patrick listing (redirects to church-bulletin.org/bulletin/our-lady-of-mount-carmel-chiesa-della-madonna-del-carmine-newark-nj-07105);
    'Latest Edition November 1, 2026', weekly issues back through 2026. Address 259 Oliver Street, Newark,
    NJ 07105.
- url: https://www.church-bulletin.org/bulletin/our-lady-of-mount-carmel-chiesa-della-madonna-del-carmine-newark-nj-07105/2026-11-01.pdf
  seen: 2026-11-04
  note: 'Image-only issue, read with render.py. Page 1 masthead ''OUR LADY OF MOUNT CARMEL CHURCH Chiesa
    della Madonna del Carmine 259 Oliver St, Newark, NJ 07105'', ''NOVEMBER 1, 2026 ALL SAINTS DAY'',
    ''Rev. Paulo dos Santos Frade, Pastor''; Mass schedule: weekdays 8:30AM Monday through Saturday, Saturday
    5:00PM (English) and 7:15PM (Espanol), Sunday 8:30AM (English), 10:00AM (Italiano), 12 Noon (English).
    No other church named. Page 6 footer ''6017 Our Lady of Mount Carmel (B) ... John Patrick Publishing
    Company, Inc.'''
- url: https://files.ecatholic.com/28815/bulletins/20261011.pdf
  seen: 2026-11-04
  quote: OUR LADY OF MOUNT CARMEL CHURCH
  note: 'The parish''s eCatholic repost of the 11 October 2026 issue (text layer): the same masthead and
    Mass schedule; no mention of Holy Trinity, Epiphany or Adams Street anywhere in the issue. The eCatholic
    /bulletins page''s newest file on 2026-11-04 was this 11 October issue, three weeks behind the John
    Patrick listing.'
- url: https://rcan.org/clergy-appointments-september-2025/
  seen: 2026-11-04
  quote: Reverend Paulo dos Santos Frade has been appointed pastor of Our Lady of Mount Carmel and Holy
    Trinity – Epiphany, Newark, effective September 8, 2025, and ending June 30, 2031.
  note: 'Shared pastor with Holy Trinity-Epiphany (also 2022: rcan.org/clergy-appointments-june-2022/);
    the bulletin nonetheless covers Mount Carmel alone.'
research:
- method: John Patrick suffixed listings 6017A-E, H, O, P, S, T (jp_scan.sh) and ParishesOnline slugs
    for a Holy Trinity-Epiphany bulletin on the shared account
  url: https://church-bulletin.org/6017
  checked: '2026-11-04'
  outcome: not-found
  next_action: Rescan 6017 letter suffixes if a Mount Carmel issue starts naming Holy Trinity-Epiphany
  retry_when: A Mount Carmel masthead names Holy Trinity-Epiphany
bulletin_status: available
---

## Publisher

John Patrick Publishing prints the bulletin as listing 6017. The 1 November 2026 issue on https://church-bulletin.org/6017 is image-only, so I read it with `render.py`. The page 1 masthead reads "OUR LADY OF MOUNT CARMEL CHURCH Chiesa della Madonna del Carmine 259 Oliver St, Newark, NJ 07105" and "NOVEMBER 1, 2026 ALL SAINTS DAY", and names Rev. Paulo dos Santos Frade as pastor. The page 6 footer reads "6017 Our Lady of Mount Carmel (B) … John Patrick Publishing Company, Inc." The parish's eCatholic site (ecatholic 28815) reposts the same issues at `files.ecatholic.com/28815/bulletins/<yyyymmdd>.pdf`. On 4 November 2026 its newest repost was the 11 October issue, three weeks behind, so I recorded the publisher and not the copy. The eCatholic id is left out of `publication`.

## Worship sites

One church, `our-lady-of-mount-carmel-newark` (259 Oliver Street). The masthead schedule lists weekdays at 8:30 AM (Monday through Saturday), Saturday 5:00 PM (English) and 7:15 PM (Spanish), and Sunday 8:30 AM (English), 10:00 AM (Italian) and 12 noon (English). It names no other building. The parish shares its pastor with Holy Trinity-Epiphany: Fr. Frade was appointed pastor of both on 8 September 2025, and Fr. Danny Santos Rodrigues held both from 1 July 2022. But no Mount Carmel issue I read mentions Holy Trinity, Epiphany or Adams Street: the eCatholic text of the 11 October 2026 issue and of the 14 June 2026 and 14 August 2022 issues had no match. Holy Trinity-Epiphany is therefore not a church of this row (see `open/holy-trinity-epiphany-newark`). GCatholic's Stella Maris chapel at Port Newark (37946) is not in this schedule either; it is the port chaplaincy's own chapel (see `excluded/stella-maris-chapel-port-newark`).

## Website and bulletin provider

The website is the parish's eCatholic site, https://mountcarmelnewark.com/. The page 3 text of the 11 October issue gives "WEBSITE MountCarmelNewark.com". GCatholic's mountcarmelnewark.org did not answer. The provider is `other`, pinned to `page-pdfs https://church-bulletin.org/6017` as the playbook prescribes for John Patrick (not the `?id=` form).

## Not yet confirmed

- Whether John Patrick carries a separate Holy Trinity-Epiphany listing on another id. The Run's scans (ids 1-1100 and 6000-6400) have no 07105 listing besides Mount Carmel, St. James and St. Casimir, and the suffixed 6017 ids I tried do not exist.
