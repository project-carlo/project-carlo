---
name: Nativity of Our Lord
website: https://www.nativitymonroe.org
bulletin_provider: other
provider_id: page-pdfs https://www.nativitymonroe.org/newsletter
publication: ['url:https://www.nativitymonroe.org/newsletter']
group: ''
evidence:
- url: https://www.nativitymonroe.org/newsletter
  seen: 2026-11-02
  quote: Bulletin Archives
  note: Wix 'Bulletin Archives' page of the parish site (nativitymonroe.org, the finder's website; `probe
    url` reports DEAD-DNS for it but `probe get` fetches it, HTTP 200). It links twelve dated PDFs at
    www.nativitymonroe.org/_files/ugd/c6881a_<hash>.pdf, labelled August 23 to November 1, 2026. The labels
    are not in date order, and in the HTML each label follows its PDF link.
- url: https://www.nativitymonroe.org/_files/ugd/c6881a_284de4297b5747e5aa114bdcc85e3d84.pdf
  seen: 2026-11-02
  quote: 185 APPLEGARTH ROAD, MONROE TOWNSHIP , NJ 08831-5961
  note: 'Page 1 of the 4 October 2026 issue (the file the archive page labels October 4, 2026): ''Pastor:
    Rev. Nalaka Silva'', three deacons, ''Nativity of Our Lord, 185 Applegarth Road, Monroe Township,
    NJ 08831-5961'', and the MASS SCHEDULE: Saturday 4:00 PM (Vigil), Sunday 7:30 AM, 9:00 AM and 11:00
    AM, weekdays Monday to Friday 8:30 AM. Names no other church.'
- url: https://www.nativitymonroe.org/_files/ugd/c6881a_f187d9051ffc440d8c6fcfbc81f151a7.pdf
  seen: 2026-11-02
  quote: H60641 (PK) - Nativity, Monroe Township
  note: 'The 1 November 2026 issue (8 pages; page 2 is headed ''Solemnity of the Saints – November 1,
    2026''), the newest on the archive page. It is the Bon Venture Services layout (page 1, an image,
    carries ''©2012 Bon Venture Services, LLC''; the ad pages carry the code line quoted here), unlike
    the 4 October issue''s plain layout, but it is the same parish-hosted file series. Page 1 (an image,
    read as a 60-dpi render): cover ''Blessed are you Saints of Heaven & Earth'' over ''Nativity of Our
    Lord, Monroe Township, New Jersey, www.nativitymonroe.org''. Page 1 has no text layer, so only the
    code line can be rechecked by quote.'
bulletin_status: available
---

## Publisher

Nativity of Our Lord, 185 Applegarth Road, Monroe Township, publishes its own weekly bulletin as PDFs on its Wix site. The 4 October 2026 issue (page 1, read 2026-11-02) names 'Rev. Nalaka Silva' as Pastor, matching the finder's pastor line, and gives the parish's own address and Mass schedule; it names no other church. The newest issue on the archive page is 1 November 2026 (its content pages name Nativity, Monroe Township in the Bon Venture code line), so the archive is current as of 2026-11-02.

## Worship sites

One church, 185 Applegarth Road (directory:24510, gcatholic:18613). The bulletin schedule (Saturday 4:00 PM vigil; Sunday 7:30, 9:00, 11:00 AM; weekdays 8:30 AM) lists no second site.

## Website and bulletin provider

Provider `other`, recipe `page-pdfs` on `https://www.nativitymonroe.org/newsletter` (the Wix site names its files by hash, not date, so the issue date comes from the label beside each link and the PDF text). The finder lists `http://www.nativitymonroe.org`; the site redirects to https. The 1 November issue is printed by Bon Venture Services, but Bon Venture's sponsor listing was not checked and the parish-hosted copy is the one recorded (settled rule: one bulletin on two hosts is recorded once, on the parish's own).

## Fetch check

`pnpm fetch:check` on 2026-11-02 resolved `page-pdfs https://www.nativitymonroe.org/newsletter` and picked `c6881a_f187d905...pdf`, the 1 November 2026 issue: transport ok, PDF, freshness unknown (the tool finds no date in the file name or masthead, which is an image cover), identity unverified by the tool. I read the issue's cover render and text pages myself (evidence above): it is Nativity's current bulletin. No `recipe` line was printed, so the pinned recipe stays as set. A direct download answered HTTP 429 once (Wix rate limit) and succeeded on retry.

## Not yet confirmed

Nothing open. The fetcher can't date these files; if the archive page's order changes it may pick the wrong week, so recheck its pick against the newest label on the archive page.
