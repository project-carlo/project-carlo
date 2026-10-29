---
name: St. Mary Parish
website: https://www.churchofsaintmary.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-mary-roman-catholic-church-schwenksville-pa-19473
publication: ['url:https://www.church-bulletin.org/saint-mary-roman-catholic-church-schwenksville-pa-19473']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-mary-roman-catholic-church-schwenksville-pa-19473/2026-10-25.pdf
  seen: 2026-10-28
  note: 'John Patrick Publishing listing 4, issue of 25 October 2026 (12 pages, image-only, md5 07a106ee;
    pages 1-2 rendered). Page 1 cover reads ''SAINT MARY ROMAN CATHOLIC CHURCH'', ''OCTOBER 25, 2026 THIRTIETH
    SUNDAY IN ORDINARY TIME'', a MASS SCHEDULE box (Saturday 4:00pm; Sunday 7:30, 9:00, 10:30 a.m., 12:00
    p.m.; Daily Monday-Saturday 9:00 a.m.), ''Reverend James M. Cox, Pastor'' and ''Saint Mary Roman Catholic
    Church, 40 Spring Mount Road, Schwenksville, PA 19473, Phone: (610) 287-8156''.'
- url: https://www.church-bulletin.org/saint-mary-roman-catholic-church-schwenksville-pa-19473
  seen: 2026-10-28
  quote: Latest Edition
  note: Listing 4 'Saint Mary Roman Catholic Church', Schwenksville, PA 19473, 40 Spring Mount Road; latest
    edition October 25, 2026.
- url: https://www.churchofsaintmary.org/
  seen: 2026-10-28
  quote: 40 SPRING MOUNT ROAD SCHWENKSVILLE, PA 19473
  note: Parish site (probe url HTTP 200, eCatholic id 16446 in its markup) links only 'jppc.net/onlinebulletins/004template.pdf'
    as its bulletin; /bulletins answers 404. Private prayer Monday-Saturday 10am-3pm and Perpetual Adoration
    of the Blessed Sacrament are in the church.
- url: https://archphila.org/parish/st-mary-schwenksville/
  seen: 2026-10-28
  quote: Rev. James M. Cox
  note: 'Directory: pastor Rev. James M. Cox; rectory 40 Spring Mount Rd., Schwenksville 19473.'
promoted: 2026-10-29
---

## Publisher

St. Mary Parish, Schwenksville (Rev. James M. Cox, Pastor) is distributed by John Patrick Publishing as listing 4, 'Saint Mary Roman Catholic Church'. The 25 October 2026 issue is 12 pages of images; the cover names the church and gives its Mass schedule and 40 Spring Mount Road. The parish site links only the listing's template (004) as its bulletin and has no `/bulletins` archive (404). The eCatholic id 16446 in the site's markup is not a publication. The row is `other` with `page-pdfs` on the listing.

## Worship sites

One church, St. Mary Church, 40 Spring Mount Road. The bulletin's Mass schedule lists only that church; page 2 mentions the 10:30 AM 'Children's Liturgy of the Word' Mass (October-April) in the same Sunday schedule and PREP classes at the campus. The directory names a "Perpetual Adoration Chapel" coordinator and the site lists perpetual adoration with no separate address, and the bulletin Mass schedule gives no Mass there, so it is not a church row. No mission or worship site appears.

## Website and bulletin provider

churchofsaintmary.org is the parish's own site; it hosts no bulletin PDFs. The listing's dated PDFs `https://www.church-bulletin.org/bulletin/saint-mary-roman-catholic-church-schwenksville-pa-19473/<yyyy-mm-dd>.pdf` are the channel.

## Fetch check

`fetch:check` (2026-10-28) resolved `page-pdfs` on the listing to the 2026-10-25 issue: transport ok, PDF, fresh (3 days); issue date inferred from the file name; identity `unverified` because the PDF has no text layer (the cover was read from a render, above). The recipe is already in `provider_id`.

## Not yet confirmed

The issue has no text layer, so `fetch:check` identity is unverified by design. Pages 3-12 were not read.
