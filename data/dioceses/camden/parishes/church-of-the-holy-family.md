---
name: Church of the Holy Family
website: https://churchoftheholyfamily.org/weekly-bulletin/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/church-of-the-holy-family-sewell-nj-08080
publication: ['url:https://www.church-bulletin.org/church-of-the-holy-family-sewell-nj-08080#john-patrick-6009']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/church-of-the-holy-family-sewell-nj-08080/2026-10-25.pdf
  seen: 2026-10-29
  note: 'Image-only PDF (12 pages); pages 1-2 rendered and read, so recheck can''t find these words as
    text. Page 1 masthead: ''CHURCH OF THE HOLY FAMILY, 226 Hurffville Road, Sewell, NJ 08080'', dated
    October 25, 2026, 30th Sunday in Ordinary Time. Names this parish alone.'
- url: https://www.church-bulletin.org/bulletin/church-of-the-holy-family-sewell-nj-08080/2026-10-25.pdf
  seen: 2026-10-29
  note: 'Page 2 (image) liturgical schedule: Saturday evening 4:30 pm; Sunday 8:00 am, 10:00 am, 11:30
    am (10:00 live streamed); daily Monday-Saturday 9:00 am (and 7:00 pm on First Fridays). Reverend James
    L. Bartoloma, Pastor; Reverend Loi Duc Tran, C.S.F., Part-Time Parochial Vicar. It assigns Mass to
    no other church.'
- url: https://churchoftheholyfamily.org/weekly-bulletin/
  seen: 2026-10-29
  note: 'probe get: the parish''s own bulletin page embeds the John Patrick code link https://church-bulletin.org/6009,
    which curl -L resolves (301, 302) to the church-bulletin.org listing used here.'
- url: https://www.church-bulletin.org/church-of-the-holy-family-sewell-nj-08080
  seen: 2026-10-29
  note: Listing for Church of the Holy Family, Sewell NJ 08080; dated PDFs weekly, latest 2026-11-01 (posted
    ahead), then 2026-10-25, 2026-10-18, 2026-10-11.
promoted: 2026-10-30
---

## Publisher

John Patrick Publishing (id 6009) prints the bulletin and the church-bulletin.org listing serves it. The 25 October 2026 issue (pages 1-2, read 2026-10-29 from rendered images) is headed 'Church of the Holy Family, 226 Hurffville Road, Sewell, NJ 08080' and gives one Mass schedule. Pastor Rev. James L. Bartoloma (the directory's 2015 entry names Fr. James Bartoloma too). It names no other parish and no other church.

## Worship sites

One church, Holy Family at 226 Hurffville Road, Sewell. The directory and GCatholic list the same single address; neither lists a second site. The parish office and the Aquin Center (faith formation) are on the same campus per the bulletin's parish-information page.

## Website and bulletin provider

`other` with `page-pdfs` on the church-bulletin.org listing, reached from the parish's own /weekly-bulletin/ page through church-bulletin.org/6009. The bulletin is image-only (no text layer), so the pipeline has to read it as an image. The publication id is the listing URL with a John Patrick suffix. The parish site page also showed a 'casino' spam-term hit from `probe url`; the page read is a normal parish page and the term is in unrelated text, not a hijack (title 'Church of the Holy Family – Catholic Church of Washington Township').

`fetch:check` (2026-10-29) picked the 2026-11-01 PDF on the listing: transport ok, PDF, issue date inferred from the file name (image-only), freshness 'future' (posted three days ahead, not a wrong pick), publication identity unverified because the text layer is empty.

## Not yet confirmed

Nothing blocking.
