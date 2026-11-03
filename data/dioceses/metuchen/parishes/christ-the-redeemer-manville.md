---
name: Christ the Redeemer
website: http://www.ctrmanville.com
bulletin_provider: other
provider_id: page-pdfs http://www.ctrmanville.com/Parish/Bulletin
publication: ['url:http://www.ctrmanville.com/Parish/Bulletin']
group: ''
evidence:
- url: http://www.ctrmanville.com/UploadFiles/Bulletins/2026-11-01.pdf
  seen: 2026-11-02
  quote: November 1, 2026                  All Saint’s Day
  note: 1 November 2026 issue (8 pages). Page 1 is mostly an image; rendered, its masthead reads 'The
    Redemptorists, Christ the Redeemer Parish', phone (908) 725-0072, www.ctrmanville.com, and names 'Sacred
    Heart - Worship Site, 98 South 2nd Ave., Manville', the parish office at the same address, 'Christ
    the King Parish Center, Religious Education, 99 North 13th Ave., Manville' and Sacred Heart Cemetery;
    staff 'Rev. Stanislaw Slaby, C.Ss.R., Pastor', 'Rev. Piotr Grzeskiewicz C.Ss.R., Associate Pastor'.
- url: http://www.ctrmanville.com/Parish/Mass
  seen: 2026-11-02
  quote: SUNDAY Sacred Heart Sacred Heart Sacred Heart 7:00AM 9:00AM 10:30AM Polish English Polish
  note: 'The parish''s Mass page puts every Mass at Sacred Heart: Saturday 8:00 am (Polish), 11:00 am
    (English), 5:00 pm Vigil (English); Sunday 7:00 am Polish, 9:00 am English, 10:30 am Polish; weekdays
    and holy days also at Sacred Heart. No Mass is listed at Christ the King.'
- url: http://www.ctrmanville.com/Parish/Bulletin
  seen: 2026-11-02
  note: Self-hosted Bulletin page listing ../UploadFiles/Bulletins/<YYYY-MM-DD>.pdf from 2014-02-02 to
    2026-11-01 (newest).
bulletin_status: available
---

## Publisher

Christ the Redeemer Parish, Manville (Redemptorists), publishes its own weekly bulletin as PDFs on its own site (http://www.ctrmanville.com/UploadFiles/Bulletins/<YYYY-MM-DD>.pdf). The 1 November 2026 issue (8 pages, read 2026-11-02; page 1 rendered because it is mostly an image) has the masthead 'The Redemptorists, Christ the Redeemer Parish' and names Rev. Stanislaw Slaby, C.Ss.R. as Pastor, as the finder does. The finder's parochial vicar, Rev. Marcin Gacek, CSsR, is not on the masthead, which names Rev. Piotr Grzeskiewicz C.Ss.R. as Associate Pastor. No publisher's account appears on the site or in the issue.

## Worship sites

One church, Sacred Heart, 98 South Second Avenue (gcatholic:18630, worship-sites:christ-the-redeemer-sacred-heart-church; the finder's parish pin directory:24504 is also at this address). The 1 November 2026 masthead calls it 'Sacred Heart - Worship Site', and the parish's Mass page (read 2026-11-02) puts every weekend, weekday and holy day Mass there.

The finder and GCatholic still list Christ the King Church, 211 Louis Street (gcatholic:18595, worship-sites:christ-the-redeemer-christ-the-king-church), and the finder gives holy-day Masses there. The parish's own sources don't: the 5 July 2020 bulletin says 'As of now there will be no Masses scheduled at Christ the King Church', the 2026 Mass page lists none, and the 2026 masthead names only a 'Christ the King Parish Center' for religious education. It is excluded as closed; see `excluded/christ-the-king-manville.md`.

## Website and bulletin provider

`probe url` gave http://www.ctrmanville.com DEAD-DNS on 2026-11-02, a verdict the playbook calls unreliable here: `probe get` fetched the site and its Bulletin page the same day. Provider `other` with `page-pdfs http://www.ctrmanville.com/Parish/Bulletin`. The Bulletin page lists issues oldest first, from 2014. A Discover Mass page for Christ the King (discovermass.com/church/christ-the-king-church-parish-of-christ-the-redeemer-manville-nj/) said 'There are currently no bulletins available' on 2026-11-02, so it is not recorded.

## Fetch check

`pnpm fetch:check` on 2026-11-02 resolved `page-pdfs http://www.ctrmanville.com/Parish/Bulletin` and picked https://www.ctrmanville.com/UploadFiles/Bulletins/2026-11-01.pdf: transport ok, PDF, issue date 2026-11-01 inferred from the file name, freshness fresh, identity unverified by the tool. That is the 1 November 2026 issue whose masthead I read (above). It printed no `recipe` line, so the provider settings stay as set.

## Not yet confirmed

Nothing open.
