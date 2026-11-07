---
name: Our Lady of Peace Parish
website: https://olopp.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-of-peace-parish-williamstown-nj-08094
publication: ['url:https://www.church-bulletin.org/our-lady-of-peace-parish-williamstown-nj-08094#john-patrick-525']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-of-peace-parish-williamstown-nj-08094/2026-10-25.pdf
  seen: 2026-10-29
  quote: Our Lady of Peace Parish
  note: 'Page 1 masthead of the 25 October 2026 issue (12 pages, image-only, read from a rendering): ''Our
    Lady of Peace Parish, October 25, 2026, Thirtieth Sunday in Ordinary Time'', pastor Rev. Sanjai Devis,
    V.C., address 32 Carroll Ave. Williamstown; John Patrick page code 525 at the foot of the page. Names
    this parish alone.'
- url: https://www.church-bulletin.org/bulletin/our-lady-of-peace-parish-williamstown-nj-08094/2026-10-25.pdf
  seen: 2026-10-29
  quote: 'Saturday: 8:00am & 4:00pm (Vigil Mass)'
  note: 'Page 1 MASSES block: Sunday 7:45am, 9:30am, 11:30am & 6:00pm; Monday-Friday 6:45 & 8:00am, Thursday
    6:30pm.'
- url: https://olopp.org/
  seen: 2026-10-29
  note: 'probe url: site alive (title ''Our Lady of Peace Parish – St Mary Church – Williamstown, NJ'');
    its bulletin link is https://www.jppc.net/onlinebulletins/525template.pdf, which curl -L resolves
    to the church-bulletin.org listing used here; the footer reads ''Proudly Designed and Hosted by John
    Patrick Publishing Company''.'
- url: https://www.church-bulletin.org/our-lady-of-peace-parish-williamstown-nj-08094
  seen: 2026-10-29
  note: 'Listing ''Our Lady of Peace Parish Bulletin'': dated PDFs weekly, latest 2026-10-25, then 10-18,
    10-11, 10-04.'
promoted: 2026-10-30
research:
- method: pnpm fetch:check --diocese camden --parish our-lady-of-peace-williamstown
  url: https://www.church-bulletin.org/our-lady-of-peace-parish-williamstown-nj-08094
  checked: '2026-10-29'
  outcome: found
  next_action: None; the pick is the 2026-10-25 issue, whose masthead was read from a rendering (image-only
    PDF, so fetch:check shows identity unverified and the date inferred from the file name).
---

## Publisher

John Patrick Publishing (id 525) prints the bulletin and the church-bulletin.org listing serves it. The 25 October 2026 issue (page 1, read 2026-10-29 from a rendering, since the PDF has no text layer) is headed "Our Lady of Peace Parish", names Rev. Sanjai Devis, V.C. as pastor, and gives the parish address 32 Carroll Ave., Williamstown, with Masses Saturday 8:00 am and 4:00 pm (Vigil), Sunday 7:45 am, 9:30 am, 11:30 am and 6:00 pm. It names no other church. The parish site's own Mass schedule (read 2026-10-29) gives the same times, and its header calls the parish "Our Lady of Peace Parish – St Mary Church".

## Worship sites

One church, St. Mary Church at 32 Carroll Ave., which is the parish's own name for its building (see its church record). The bulletin also lists the St. John Neumann Adoration Chapel (open daily 5:30 am to 9:00 pm); it is an adoration chapel, and no bulletin or site line gives Mass there, so it is not a separate church. The diocese directory and GCatholic list one entry each at the same address. Sts. Peter and Paul, Williamstown (Ukrainian) is Eastern Catholic and belongs to another batch.

## Website and bulletin provider

`other` with `page-pdfs` on the church-bulletin.org listing, which the parish's site reaches through jppc.net 525. The directory and GCatholic both give the old http://www.olopp.org (now https://olopp.org). The publication id is the listing URL with a John Patrick suffix; John Patrick has no id scheme of its own here.

## Not yet confirmed

Nothing blocking. Most issues are image-only, so `fetch:check` reports the date from the file name rather than the text.
