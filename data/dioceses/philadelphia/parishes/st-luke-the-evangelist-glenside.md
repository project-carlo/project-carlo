---
name: St. Luke the Evangelist
website: https://stlukeglenside.org
bulletin_provider: ecatholic
provider_id: '28474'
publication: ['ecatholic:28474', 'url:https://www.church-bulletin.org/saint-luke-the-evangelist-parish-glenside-pa-19038']
group: ''
evidence:
- url: https://files.ecatholic.com/28474/bulletins/20261025.pdf
  seen: 2026-10-29
  quote: SAINT LUKE THE EVANGELIST PARISH
  note: 'Page 1 of the 25 October 2026 issue (12 pages, text layer): masthead ''Saint Luke the Evangelist
    Parish, Easton Road & Fairhill Avenue, Glenside, Pennsylvania'', rectory 2316 Fairhill Avenue, www.stlukeglenside.org.
    One Mass schedule box: Saturday Vigil 5:00 PM (Livestreamed); Sunday 7:30, 10:30 AM; Monday, Wednesday,
    Friday 6:30 AM; Tuesday, Thursday, Saturday 8:30 AM. Names St. Luke alone.'
- url: https://stlukeglenside.org/bulletins
  seen: 2026-10-29
  note: Loaded in Chrome (visit.py; probe url answers 403). The parish's eCatholic Bulletin page (site
    28474) links files.ecatholic.com/28474/bulletins/<yyyymmdd>.pdf, newest 20261025, then 20261018 and
    20261011.
- url: https://www.church-bulletin.org/saint-luke-the-evangelist-parish-glenside-pa-19038
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick Publishing listing 61 'Saint Luke the Evangelist Parish', Glenside, PA 19038; latest
    edition October 25, 2026. Its 2026-10-25.pdf and the parish's eCatholic 20261025.pdf are byte-identical
    (md5 829a0600592556e8079586f1de44963c, 12 pages), so they are one bulletin.
- url: https://archphila.org/parish/st-luke-the-evangelist-glenside/
  seen: 2026-10-28
  note: 'Directory entry: Rev. Joseph D. Brandt, pastor; S.W. corner of Easton Rd. and Fairhill Ave.;
    names no worship site or chapel. Its Sunday 7:30, 9:30, 11:30 AM is 7 months old and no longer matches
    the bulletin.'
promoted: 2026-10-29
bulletin_status: available
publication_reviews:
- parish: queen-of-peace-ardsley
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/28474/bulletins/20261025.pdf
    seen: 2026-10-29
    note: The 25 October 2026 masthead (page 1) names Saint Luke the Evangelist Parish, Easton Road &
      Fairhill Avenue, Glenside, alone, with its own Mass schedule (Saturday 5:00 PM; Sunday 7:30, 10:30
      AM).
  - url: https://www.church-bulletin.org/bulletin/queen-of-peace-parish-ardsley-glenside-pa-19038/2026-10-25.pdf
    seen: 2026-10-29
    note: The 25 October 2026 masthead (page 1) names Queen of Peace Parish, 820 North Hills Avenue, Ardsley,
      alone, with its own Masses box (Saturday 4:30 pm; Sunday 7:30, 9:30, 11:00 am).
- parish: st-david-willow-grove
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/28474/bulletins/20261025.pdf
    seen: 2026-10-29
    note: The 25 October 2026 masthead (page 1) names Saint Luke the Evangelist Parish, Easton Road &
      Fairhill Avenue, Glenside, alone, with its own Mass schedule (Saturday 5:00 PM; Sunday 7:30, 10:30
      AM).
  - url: https://www.church-bulletin.org/bulletin/saint-david-roman-catholic-church-willow-grove-pa-19090/2026-10-25.pdf
    seen: 2026-10-29
    note: The 25 October 2026 header (page 1) names St. David Roman Catholic Church, Willow Grove, alone,
      with its own Mass Schedule (Saturday 4:00 PM; Sunday 7:00, 9:00, 11:00 AM).
---

## Publisher

St. Luke the Evangelist, Glenside (Rev. Joseph D. Brandt, pastor) publishes its own weekly bulletin, printed by John Patrick Publishing (listing 61) and posted on the parish's own eCatholic site. The 25 October 2026 issue's masthead names 'Saint Luke the Evangelist Parish, Easton Road & Fairhill Avenue, Glenside' alone and carries one Mass schedule (Saturday vigil 5:00 PM; Sunday 7:30 and 10:30 AM; weekdays Monday, Wednesday, Friday 6:30 AM and Tuesday, Thursday, Saturday 8:30 AM). It is a single-church parish. The directory's Sunday 9:30 and 11:30 AM are not in the bulletin.

## Worship sites

One: St. Luke the Evangelist church (churches/st-luke-the-evangelist-glenside.md). The directory page and the bulletin's Mass box name no other church or chapel. GCatholic lists only the one church (19284).

## Website and bulletin provider

`ecatholic`, site 28474: stlukeglenside.org is the parish's eCatholic site and its /bulletins page links a current `files.ecatholic.com/28474/bulletins/20261025.pdf`. That file is byte-identical to the John Patrick listing's issue, so both ids are in `publication` and the listing (https://www.church-bulletin.org/saint-luke-the-evangelist-parish-glenside-pa-19038) is the fallback `other` channel. `probe url` and curl answer 403 on the site's pages; the files.ecatholic.com URL downloads with plain curl.

## Not yet confirmed

Nothing outstanding. Neighbouring Glenside-area parishes (Queen of Peace, Ardsley) publish their own listings with their own mastheads (see their records).

## Fetch check

`fetch:check` (2026-10-29, headed Chrome) with the `ecatholic` provider picked `https://files.ecatholic.com/28474/bulletins/20261025.pdf`: transport ok, PDF, fresh (4 days), issue date observed in the text ("October 25, 2026"); identity `unverified` only because the check was given no expected identity (the masthead was read from the text layer, above).
