---
name: St. Jude Parish
website: https://www.stjudechalfont.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-jude-church-shrine-chalfont-pa-18914
publication: ['url:https://www.church-bulletin.org/saint-jude-church-shrine-chalfont-pa-18914']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-jude-church-shrine-chalfont-pa-18914
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 120, 'Saint Jude Church & Shrine', Chalfont, PA 18914, 321 West Butler Avenue,
    phone (215) 822-0179; latest edition October 25, 2026, dated archive back to November 2024.
- url: https://www.church-bulletin.org/bulletin/saint-jude-church-shrine-chalfont-pa-18914/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (12 pages, image-only; pages 1-2 rendered). Page-1 masthead ''St. Jude
    Parish, Live, Love, and Serve in Christ, October 25, 2026, 30th Sunday in Ordinary Time''; ''321 W.
    Butler Ave., Chalfont, PA 18914''; ''Mass Schedule: Saturday Vigil 4:30pm, Sunday 8:30am, 10:30am,
    Monday - Saturday 9:00am, Tuesday, Thursday 6:30am''; ''Thursday St. Jude Shrine Novena Devotions'';
    ''Chapel & Shrine Hours''. Names this parish alone.'
- url: https://www.stjudechalfont.org/bulletins
  seen: 2026-10-29
  note: 'Parish site (eCatholic 20043; answers 403 to probe url, loads in the browser): its Bulletins
    page links church-bulletin.org/120 and files.ecatholic.com/20043/bulletins/<yyyymmdd>.pdf, newest
    20261018 on 2026-10-29 while the listing has 25 October. The 18 October eCatholic file (10 pages,
    text layer, md5 1b7c5ae1...) differs from the listing''s 18 October file (12 pages, md5 a77da143...),
    so it is a differently laid-out edition, not a copy. Read in the browser, so not a quotable string.'
- url: https://archphila.org/parish/st-jude-chalfont/
  seen: 2026-10-29
  quote: Rev. Anthony J. Costa
  note: 'Directory: pastor; 321 West Butler Ave., Chalfont 18914.'
research:
- method: visit.py on stjudechalfont.org and /bulletins; curl of the eCatholic 20261018 PDF against the
    listing's 18 October PDF
  url: https://www.stjudechalfont.org/bulletins
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

St. Jude Parish, Chalfont (Fr. Anthony J. Costa, Pastor) is listed by John Patrick Publishing as 'Saint Jude Church & Shrine' (listing 120), with the 25 October 2026 issue as latest and a dated archive back to November 2024. The masthead names St. Jude Parish alone. The row is `other`, `page-pdfs` on the listing. The current issue has no text layer, so the masthead and Mass box were read from a render of page 1.

## Worship sites

One church, St. Jude Church and Shrine, 321 West Butler Avenue. The shrine and its chapel are in the church (a shrine in a parish church is that church's row; the Rules settled name St. Jude, Chalfont). The page-1 'Chapel & Shrine Hours' (Monday-Friday 7:00am-7:00pm, Saturday 8:00am to the 4:30pm vigil, Sunday 8:00am-noon) are opening hours, not extra Masses. No other location holds Mass in the box.

## Website and bulletin provider

`https://www.stjudechalfont.org` is eCatholic-hosted (20043). Its `/bulletins` archive posts its own PDFs, a week behind the listing (18 October newest on 2026-10-29), in a different layout from the listing's issue of the same Sunday. The listing is current and is the channel; `ecatholic:20043` is left out of `publication` because its files are not shown to be the listing's issue. Directory Mass times (vigil 4:30pm, Sunday 8:30 and 10:30am, Monday-Saturday 9:00am) match the bulletin.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (4 days, date inferred from the file name); identity `unverified` because no expected identity is supplied by the check and the PDF has no text layer (masthead read from a render). It printed no `recipe` line, as the pinned `provider_id` already holds it.

## Not yet confirmed

Pages 3-12 of the bulletin were not read. Whether the eCatholic issues are the parish's own edition of the same bulletin, or an earlier layout, was not settled; it doesn't change the channel while the listing is current.
