---
name: Our Lady Queen of Martyrs (Forest Hills)
website: https://ourladyqueenofmartyrs.org/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/407
publication: ['url:https://www.church-bulletin.org/our-lady-queen-of-martyrs-forest-hills-ny-11375']
group: Deanery Q6 (Queens West)
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-queen-of-martyrs-forest-hills-ny-11375/2026-11-08.pdf
  seen: 2026-11-06
  note: '8 November 2026 issue (8 pages, all images; read with render.py). Page 1 masthead: ''Our Lady
    Queen of Martyrs'', Rev. Francis J. Passenant, Pastor, 110-06 Queens Boulevard, Forest Hills, New
    York 11375, tel 718-268-6251; side text ''407 - Our Lady Queen of Martyrs''. Page 2 ''Masses for the
    Week'': Saturday 12:05 p.m. and 5 p.m., Sunday 9 a.m. Family Mass, weekdays 8:05 a.m. and 12:05 p.m.;
    page 1 says ''Watch Sunday Mass Online 11:15 a.m.'''
- url: https://church-bulletin.org/407
  seen: 2026-11-06
  quote: Our Lady Queen of Martyrs Bulletin
  note: 'John Patrick Publishing listing (title); dated PDFs newest first: 2026-11-08, 2026-11-01, 2026-10-25,
    2026-10-18 ... weekly.'
- url: https://ourladyqueenofmartyrs.org/bulletin/
  seen: 2026-11-06
  note: WordPress parish site; probe url lists bulletin links https://www.jppc.net/onlinebulletins/407template.pdf
    and /bulletin-archives/.
promoted: 2026-11-12
bulletin_status: available
---

## Publisher

Our Lady Queen of Martyrs publishes its own weekly bulletin through John Patrick Publishing (JPPC), listing 407. The parish site's bulletin page links `jppc.net/onlinebulletins/407template.pdf`; the listing `church-bulletin.org/407` (title "Our Lady Queen of Martyrs Bulletin") lists dated PDFs newest first. I read the 8 November 2026 issue (read 2026-11-06; every page is an image, drawn with render.py): page 1 is headed "November 8, 2026 - Thirty-Second Sunday in Ordinary Time" with the masthead "Our Lady Queen of Martyrs", Rev. Francis J. Passenant, Pastor, 110-06 Queens Boulevard, Forest Hills, New York 11375.

## Worship sites

One church. Page 2's "Masses for the Week" lists Masses with no place named other than the church (devotions and confessions marked "church"); page 1 adds Sunday Mass at 11:15 a.m. streamed online. OLQM Catholic Academy is a school. The diocese directory, the deanery list (Q6), GCatholic 16654 and Mass finder 1143 list this one church. The directory gives no website; GCatholic gives ourladyqueenofmartyrs.org, which is the parish's live site.

## Website and bulletin provider

`other`, reading the JPPC listing with `page-pdfs https://church-bulletin.org/407` (the pattern Allentown's JPPC rows use). `fetch:check` (2026-11-06) resolved "page-pdfs on https://church-bulletin.org/407: current" and picked `2026-11-08.pdf`, the 8 November 2026 issue (freshness `future`, posted ahead of that Sunday); that is the recipe recorded. The bulletin is image-only: the pipeline has to read its Mass times from images.

## Not yet confirmed

The full Sunday schedule (the page 2 intentions list only the 9 a.m. and the Saturday Masses; 11:15 a.m. is named on page 1) is for the pipeline to read; it does not affect the row.
