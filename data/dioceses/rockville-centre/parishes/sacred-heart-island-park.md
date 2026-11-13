---
name: Sacred Heart
website: https://sacredheartislandpark.com/bulletins/
bulletin_provider: other
provider_id: page-pdfs https://sacredheartislandpark.com/bulletins/
publication: ['url:https://sacredheartislandpark.com/bulletins/#sacred-heart']
group: ''
evidence:
- url: https://sacredheartislandpark.com/wp-content/uploads/2026/11/2026_11_08_sacred_heart_ip-WS.pdf
  seen: 2026-11-13
  quote: 'Sacred Heart RC Church–Bulletin: 32nd Sunday in Ordinary Time, November 8th, 2026'
  note: Page 1 masthead names 'Sacred Heart Church, 282 Long Beach Road, Island Park, NY 11558' alone,
    Monsignor John J. Tutoné, Pastor; Masses Sat. Eve. 5:00 p.m., Sunday 8:00 a.m., 10:00 a.m., & 12:15
    p.m., Mon. – Fri. 8:00 a.m. 12 pages, made in Microsoft Word (downloaded through Chrome with tools/browser_get.py;
    probe pdf could not connect).
- url: https://sacredheartislandpark.com/bulletins/
  seen: 2026-11-13
  note: 'The WordPress Bulletins page lists one PDF per Sunday, newest first: 2026_11_08_sacred_heart_ip-WS.pdf,
    2026_11_01_..., 2026_10_25_... (read with parish-site-access visit.py).'
bulletin_status: available
---

## Publisher

Sacred Heart, 282 Long Beach Road, Island Park publishes its own weekly bulletin, made in Microsoft Word and posted on its WordPress site. The newest issue on 2026-11-13, `https://sacredheartislandpark.com/wp-content/uploads/2026/11/2026_11_08_sacred_heart_ip-WS.pdf` (12 pages), has the running head "Sacred Heart RC Church–Bulletin: 32nd Sunday in Ordinary Time, November 8th, 2026". Its page-1 masthead names "Sacred Heart Church, 282 Long Beach Road, Island Park, NY 11558" alone, with Monsignor John J. Tutoné as pastor and Masses on Sat. Eve. at 5:00 p.m.; Sunday at 8:00 a.m., 10:00 a.m. and 12:15 p.m.; and Mon. – Fri. at 8:00 a.m. This matches the drvc.org Mass-times page.

## Worship sites

One: the church at 282 Long Beach Road (`sacred-heart-island-park-church`). The masthead's schedule names no other place, and the diocesan locator (directory:26), GCatholic (16867) and the Mass-times page list only this building.

## Website and bulletin provider

sacredheartislandpark.com is the link of all three lists. `probe url` and `probe pdf` could not connect ("Remote end closed connection"); the site loads in the browser (visit.py), and fetch reads it. Its `/bulletins/` page lists the issues newest first. `fetch:check` (2026-11-13) with page-pdfs on `/bulletins/` picked the 8 November 2026 issue, the newest posted; the home page also links flyers, so the recipe is pinned on `/bulletins/`.

## Not yet confirmed

Nothing open.
