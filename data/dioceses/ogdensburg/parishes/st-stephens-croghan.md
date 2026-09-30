---
name: St. Stephen's Parish, Croghan
website: https://www.ststephenscroghan.org
bulletin_provider: ecatholic
provider_id: '29575'
publication: ['ecatholic:29575']
group: ''
evidence:
- url: https://files.ecatholic.com/29575/bulletins/20260927.pdf
  seen: 2026-09-30
  quote: St. Stephen’s Parish
  note: 'Page 1 masthead of the 27 September 2026 issue (2 pages, text layer): "St. Stephen’s Parish
    http://www.ststephenscroghan.org/ 9748 Main Street/PO Box 38 Croghan, NY 13327", Rev. Joseph A. Morgan,
    VG, Deacon Peter Woolschlager. Mass list: Saturday 26 September 5:00 pm, Sunday 27 September 8:30 am,
    weekdays 8:15 am, Friday 2 October 6:30 pm Eucharistic Adoration. No other church or place is named
    (searched for "Harrisville" and "Solanus": no hits).'
- url: https://www.ststephenscroghan.org/
  seen: 2026-09-30
  quote: St. Stephen's Catholic Church - Croghan, NY
  note: 'The parish site (eCatholic, behind Cloudflare; loaded on the first try with visit.py). It embeds
    ecatholic:29575 and links /bulletins and /mass-times.'
- url: https://www.rcdony.org/parish/croghan
  seen: 2026-09-30
  quote: 'Administrator: Reverend Joseph A. Morgan, VG'
  note: 'The diocese directory entry for Croghan (St. Stephen''s Church, 9748 State Route 812, website
    www.ststephenscroghan.org). The Harrisville entry has the same administrator but its own bulletin (see
    `st-francis-solanus-harrisville`).'
- url: https://www.rcdony.org/directory/parish-bulletins.html
  seen: 2026-09-30
  note: 'The diocese''s bulletin page lists Croghan with "#" (no link), so the bulletin came from the parish
    site, not the diocese page.'
---

## Publisher

St. Stephen's Parish, Croghan publishes its own weekly bulletin as dated PDFs on eCatholic
(site 29575, `files.ecatholic.com/29575/bulletins/<YYYYMMDD>.pdf`; the 27 September 2026
issue was read, and the 6 September, 9 August and 12 July issues exist too). The masthead and
Mass list are for St. Stephen's alone.

## Worship sites

One: `st-stephen-croghan`. The administrator, Fr. Joseph A. Morgan, VG, also administers St.
Francis Solanus, Harrisville, but that parish publishes its own separate
bulletin (a PDF on rcdony.org, with no mention of Croghan beyond the pastor's phone number),
and St. Stephen's bulletin never mentions Harrisville, so they are two rows. The directory
does not group them.

## Website and bulletin provider

`www.ststephenscroghan.org` is the directory's and GCatholic's link. It answers 403 to curl
and `probe url`, but visit.py loads it and reports `ecatholic:29575` and a Bulletins page.
`issues.py ecatholic ecatholic:29575` reads the PDFs without a browser (the 4 October file
was not yet posted on 2026-09-30).

## Not yet confirmed

Nothing.
