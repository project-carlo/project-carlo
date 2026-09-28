---
name: St. Mary's Church
website: https://www.stmarysglensfalls.org
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.stmarysglensfalls.org/']
group: ''
evidence:
- url: https://www.stmarysglensfalls.org/_files/ugd/91aab8_bb1c8973bb4a41bd9806eb081cb399d9.pdf
  seen: 2026-09-28
  quote: September 27th, 2026 ~ 26th Sunday in Ordinary Time
  note: Page 1 of the bulletin linked as "Bulletin" on the homepage on 2026-09-28 (redirects to a filesusr.com
    copy). Masthead "St. Mary's Church 62 Warren Street, Glens Falls, NY 12801", Pastor Father Scott VanDerveer,
    Mass Schedule Saturday 4:00 p.m., Sunday 8:30 a.m. & 11:15 a.m., Wednesday and Thursday 12:10 p.m.
    Names this church alone.
- url: https://www.stmarysglensfalls.org/_files/ugd/91aab8_bb1c8973bb4a41bd9806eb081cb399d9.pdf
  seen: 2026-09-28
  quote: 62 Warren Street, Glens Falls, NY 12801
- url: https://www.stmarysglensfalls.org/
  seen: 2026-09-28
  note: 'Homepage (behind Cloudflare; read with parish-site-access visit.py): menu item "Bulletin" links
    _files/ugd/91aab8_bb1c8973bb4a41bd9806eb081cb399d9.pdf; "Mass Times Wednesday: 12:10 PM Thursday:
    12:10 PM Saturday: 4:00 PM Sunday: 8:30 AM 11:15 AM".'
promoted: 2026-09-28
---

## Publisher

St. Mary's Church, Glens Falls publishes its own weekly bulletin, an 8-page PDF it posts on
its Wix website. The issue linked on 2026-09-28 is dated "September 27th, 2026 ~ 26th Sunday
in Ordinary Time" (page 1): masthead "St. Mary's Church 62 Warren Street, Glens Falls",
Pastor Fr. Scott VanDerveer, Mass Schedule Saturday 4:00 p.m., Sunday 8:30 & 11:15 a.m.,
Wednesday and Thursday 12:10 p.m. Page 3 prints a "Local Daily Mass Schedule" of neighbouring
parishes (OLA, St. Michael's South Glens Falls, Sacred Heart, St. Mary's-St. Paul's, St.
Joseph's), which is a courtesy list, not a membership list.

## Worship sites

One: `st-mary-glens-falls`. The institutional-records index gives the records of the closed
St. Alphonsus, Glens Falls to St. Mary's/St. Paul's, Hudson Falls, not to this parish; St.
Alphonsus is in neither roster and was not researched further.

## Website and bulletin provider

stmarysglensfalls.org is a Wix site behind Cloudflare (`probe url`: HTTP4XX; visit.py loads
it first try). The homepage's "Bulletin" menu item links one PDF under `_files/ugd/`, which
redirects to a `*.filesusr.com` copy; it appears to be a single rolling link replaced each
week (only one bulletin link is on the site), so the publication is the homepage itself
(`url:`). Wix answered HTTP 429 to `probe pdf` for this file, while `curl -L` fetched it; the
text layer is good.

## Not yet confirmed

Whether the "Bulletin" link keeps the same file name week to week (check it again after
4 October 2026). If Wix keeps rate-limiting the pipeline's fetcher, reading this bulletin
may need a slower fetch.
