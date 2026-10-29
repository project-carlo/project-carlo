---
name: St. Helena Parish
website: https://sainthelena-centersquare.net
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-helena-church-blue-bell-pa-19422
publication: ['url:https://www.church-bulletin.org/saint-helena-church-blue-bell-pa-19422']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-helena-church-blue-bell-pa-19422/2026-10-25.pdf
  seen: 2026-10-28
  note: 'John Patrick Publishing listing 43, issue of 25 October 2026 (16 pages, image-only: probe pdf
    reads 0 pages, so pages 1-3 were rendered). Page 1 cover reads ''October 25, 2026'', ''SAINT HELENA
    PARISH'', ''Worship God. Love Others. Make Disciples.'', a Mass Schedule (Monday-Saturday 9:00 AM
    Saint Helena Chapel; Saturday Vigil 4:00 PM; Sunday 7:30, 9:00, 11:00 AM), ''Church Address 1489 DeKalb
    Pike, Blue Bell, PA 19422'' and ''Phone: 610-275-7711''. Page 2 ''Parish Information'' lists the priests
    (Rev. Joseph W. Bongard, ''Pastor of St. Helena & Parochial Administrator of St. Titus'') and, in
    two boxes, a ''St. Helena Mass Schedule'' and a ''St. Titus Mass Schedule''. Page 3 lists ''St. Helena/St.
    Titus Mass Intentions'' for both churches.'
- url: https://www.church-bulletin.org/saint-helena-church-blue-bell-pa-19422
  seen: 2026-10-28
  quote: Latest Edition
  note: Listing 43 'Saint Helena Church', Blue Bell, PA 19422; latest edition October 25, 2026.
- url: https://sainthelena-centersquare.net/
  seen: 2026-10-28
  quote: Proudly Designed & Hosted by John Patrick Publishing Company
  note: Parish site (probe url HTTP 200 after redirect from www.sainthelena-centersquare.net) links only
    'https://church-bulletin.org/?id=043' as its bulletin and hosts no PDFs. Its home page gives the St.
    Helena and the St. Titus Mass schedules side by side.
- url: https://archphila.org/parish/st-helena-blue-bell/
  seen: 2026-10-28
  quote: Rev. Joseph W. Bongard
  note: 'Directory: pastor Rev. Joseph W. Bongard; rectory 1489 DeKalb Pike, Blue Bell 19422.'
publication_reviews:
- parish: st-titus-norristown
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-helena-church-blue-bell-pa-19422/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image rendered) names Saint Helena Parish, 1489 DeKalb
      Pike, Blue Bell, alone, with its own Mass schedule and a green Saint Helena layout; 16 pages, md5
      28af7c1e.
  - url: https://www.church-bulletin.org/bulletin/saint-titus-parish-east-norriton-pa-19403/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image rendered) names St. Titus Parish, 3000 Keenwood
      Road, East Norriton, alone, with its own cover (an Anointing Mass notice); 12 pages, md5 8ecb9184,
      a different file in a different listing (95). Both bulletins print the partner parish's Mass times
      and a joint Mass-intentions list, but each is its own issue.
---

## Publisher

St. Helena Parish, Blue Bell (Rev. Joseph W. Bongard, Pastor of St. Helena and Parochial Administrator of St. Titus) is distributed by John Patrick Publishing as listing 43, 'Saint Helena Church'. The 25 October 2026 issue is 16 pages of images; its page-1 cover reads 'SAINT HELENA PARISH' with 1489 DeKalb Pike, Blue Bell, PA 19422. The parish site is built and hosted by John Patrick Publishing and links only the listing. The row is `other` with `page-pdfs` on the listing.

**One bulletin or two with St. Titus?** Two. St. Titus has its own listing (95), its own 12-page issue with its own cover, and a different file (md5 differs from this 16-page issue). What they share is content: page 2 of this bulletin gives both a 'St. Helena Mass Schedule' and a 'St. Titus Mass Schedule', and page 3 is a joint 'St. Helena/St. Titus Mass Intentions' list; St. Titus's page 2 and its 'Partner Parishes Mass Intentions' do the same. The shared pastor (the directory names Fr. Bongard on both pages) is why. Following the Run's rule that a shared pastor does not make a shared bulletin, each parish stays a row and each church stays under its own parish; see `publication_reviews`.

## Worship sites

One church, St. Helena Church, 1489 DeKalb Pike. The weekday 9:00 AM Mass is said in the 'Saint Helena Chapel' (the parish site: 'Monday – Saturday 9:00 AM in Saint Theresa Chapel'; the bulletin's adoration and devotions list the same chapel), which is a room of the 1489 DeKalb Pike campus, not another building, so it gets no church row. St. Titus's Masses appear in this bulletin but are St. Titus's own church row (see `st-titus-norristown`). Nothing else is listed.

## Website and bulletin provider

sainthelena-centersquare.net hosts no PDFs; the listing's dated PDFs `https://www.church-bulletin.org/bulletin/saint-helena-church-blue-bell-pa-19422/<yyyy-mm-dd>.pdf` are the channel.

## Fetch check

`fetch:check` (2026-10-28) resolved `page-pdfs` on the listing to the 2026-10-25 issue: transport ok, PDF, fresh; issue date inferred from the file name; identity `unverified` because the PDF has no text layer (the masthead was read from a render, above). The recipe is already in `provider_id`.

## Not yet confirmed

The issue has no text layer, so `fetch:check` identity is unverified by design; the cover was read from a render. Pages 4-16 were not read.
