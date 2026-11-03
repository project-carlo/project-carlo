---
name: St. Anthony of Padua, Union City
website: https://stanthonyuc.com/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Planning Area E
evidence:
- url: https://stanthonyuc.com/bulletins
  seen: 2026-11-03
  quote: Weekly Bulletins 2025
  note: GoDaddy Website Builder page (probe get). Newest section 'Weekly Bulletins 2025', newest file
    'October 26 (pdf)' (img1.wsimg.com/.../October%2026.pdf); then 2024. No 2026 issue is listed.
- url: https://img1.wsimg.com/blobby/go/0947f251-d6b0-4652-aa3d-1015f5892acb/downloads/7a5fc1cf-1589-47fd-a0c1-fbf273bad386/October%2026.pdf?ver=1784687031633
  seen: 2026-11-03
  note: Newest posted issue, 6 pages, images only (page 1 rendered). Masthead 'St. Anthony of Padua Church,
    615 8th St. | Union City, NJ | 07087 | 201-867-3818', dated 'October 26th 2025, Thirtieth Sunday in
    Ordinary Time'. Self-produced; no publisher code on page 6.
- url: https://parishesonline.com/organization/st-anthony-church-07087
  seen: 2026-11-03
  note: 'probe po: St. Anthony Church, 615 8th St, Union City (lpi 0018000000QxAAaAAN) - ''no publications:
    this organization does not publish a bulletin here now''.'
- url: https://rcan.org/clergy-appointments-july-2026/
  seen: 2026-11-03
  quote: has been appointed pastor of Saint Anthony of Padua, Union City, effective September 1, 2026
research:
- method: probe get of the parish site's Bulletins page; render of its newest issue; probe po st-anthony-church-07087
    and st-anthony-of-padua-church-07087; homepage links (Facebook, Instagram, YouTube, Twitch) checked
    for a bulletin link
  url: https://stanthonyuc.com/bulletins
  checked: '2026-11-03'
  outcome: not-found
  next_action: Re-read stanthonyuc.com/bulletins for a 2026 issue; try the parish Facebook page (facebook.com/iglesiasanantoniouc)
    with visit.py for posted bulletins
  retry_when: The parish site lists a bulletin dated after 26 October 2025, or a new pastor's site appears
  revisit_after: 2027-01-15
bulletin_status: not-found
---

## Publisher

St. Anthony of Padua, Union City, made its own bulletin: the newest one on its site is the 26 October 2025 issue (images only; page 1 masthead 'St. Anthony of Padua Church, 615 8th St. | Union City, NJ | 07087', 'October 26th 2025, Thirtieth Sunday in Ordinary Time'), with no publisher code. The site's Bulletins page lists 'Weekly Bulletins 2025' (newest 'October 26') and 2024, nothing from 2026. The ParishesOnline org `st-anthony-church-07087` exists with no publications. So no current bulletin was found, and the row is `no_bulletin` (kept in the records, off the site, per Settled policy 4).

## Worship sites

- St. Anthony of Padua church, 615 8th Street (`st-anthony-of-padua-union-city`). The parish site's Mass schedule also lists weekday Masses in the 'School Chapel', on the parish's own campus; it is not given a separate row.

The directory (197) and GCatholic (18566) list only this church.

## Website and bulletin provider

`website` is the parish's Bulletins page, https://stanthonyuc.com/bulletins (GoDaddy Website Builder; files on img1.wsimg.com, named by month and day only, e.g. 'October 26.pdf'). If the parish resumes posting, `page-pdfs https://stanthonyuc.com/bulletins` is the recipe to try, but the undated file names and the old 2024-2025 files on the same page would need checking with fetch:check. GCatholic's http://www.stanthonyuc.org did not answer probe get.

No fetch check was run: there is no current bulletin to pick.

## Not yet confirmed

Whether the parish posts a bulletin anywhere else: its Facebook page (facebook.com/iglesiasanantoniouc) shows no posts without a login. A new pastor started on 1 September 2026; see `research` for the retry.
