---
name: St. Charles Borromeo
website: https://www.stcharlesbridgeport.org/
bulletin_provider: parishes_online
provider_id: st-charles-borromeo-church-06608
publication: ['po-org:st-charles-borromeo-church-06608', 'lpi:0018000000Qc1GeAAJ', 'po-container:03/1118']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1118/20261115B.pdf
  seen: 2026-11-12
  note: 'Page 1 of the 15 November 2026 issue is an image (rendered with parish-site-access render.py).
    Logo ''StCG''; ''ST. CHARLES Nuevo Horario de Misas ... As of Sunday, December 6, 2026'': 8:30 AM
    Spanish, 10:30 AM Brazilian (Portuguese), 11:00 AM English, 12:30 PM Spanish, new 6:00 PM Spanish;
    ''St. George Masses are not changing.'' Footer: ''Saint Charles: 1279 East Main Street, Bridgeport,
    CT 06608''; ''Saint George: 443 Park Avenue, Bridgeport, CT 06604''; ''(Office located in Saint Charles)''.
    Page 2 lists Rev. Abelardo Vasquez, Pastor.'
- url: https://container.parishesonline.com/bulletins/03/1118/20261115B.pdf
  seen: 2026-11-12
  quote: St. Charles Borromeo, Bridgeport, CT 03-1118
  note: LPi ad-page footer on page 8 (the only page with a text layer).
- url: https://parishesonline.com/organization/st-charles-borromeo-church-06608
  seen: 2026-11-12
  note: 'probe po: org ''St. Charles Borromeo Church'', 391 Ogden St, Bridgeport 06608, LPi id 0018000000Qc1GeAAJ,
    container 03/1118, latest issue 2026-11-15. Found by slug pattern; the parish site embeds no widget.'
- url: https://www.stcharlesbridgeport.org/projects-3-1
  seen: 2026-11-12
  quote: This bulletin is distributed to over 2000 families weekly. If you would like to advertise in
    it, please call LPI
  note: The site's Bulletin page (Wix) shows a gallery of cover images with no PDF links (read with parish-site-access
    visit.py).
- url: https://www.stcharlesbridgeport.org/mass-schedule
  seen: 2026-11-12
  quote: Saint George Weekend Masses
  note: 'The site''s Mass page, headed ''Saint Charles & Saint George catholic church'', lists Saint Charles
    weekly and weekend Masses (Upper Church, Lower Church) and Saint George: Monday, Tuesday, Friday 7:00
    pm; Saturday 6:30 pm Spanish vigil; Sunday 8:30 am English, 10:30 am Spanish.'
bulletin_status: available
---

## Publisher

St. Charles Borromeo, Bridgeport publishes a weekly LPi bulletin on ParishesOnline (org `st-charles-borromeo-church-06608`, container 03/1118). The 15 November 2026 issue (`https://container.parishesonline.com/bulletins/03/1118/20261115B.pdf`, read 2026-11-12) is image-only apart from the page 8 ad footer, so pages 1-2 were rendered and read by eye. Page 1 is headed "ST. CHARLES" with the 'StCG' logo, announces a new St. Charles Sunday schedule from 6 December 2026, says "St. George Masses are not changing", and gives both addresses: Saint Charles, 1279 East Main Street, and Saint George, 443 Park Avenue ("Office located in Saint Charles"). Page 2 names Rev. Abelardo Vasquez, Pastor, as the directory does.

## Worship sites

One bulletin covers two churches, both on this row (survey-review rule on a merged parish's campus with Mass):

- `st-charles-borromeo-bridgeport`: Upper Church, Lower Church and chapel in one building (the site's Mass page; the diocese's notes 'Upper Church', 'Lower Church', 'Chapel').
- `st-george-bridgeport`: the 'St. George campus' (mass-times:1327-st-george-campus; GCatholic 21999), with Saturday 6:30 pm, Sunday 8:30 and 10:30 am and evening weekday Masses on the parish's Mass page, unchanged per the bulletin.

## Website and bulletin provider

`stcharlesbridgeport.org` is a Wix site; its Bulletin page (`/projects-3-1`) shows cover images with no PDF links or widget, and names LPI for advertising. The ParishesOnline org was found from LPi's slug pattern (`<name>-church-<zip>`), and its address (391 Ogden St), the 03-1118 footer and the cover match the parish. Provider `parishes_online`, read by org slug. The issues are image-only, so the pipeline will need to read them as images.

`fetch:check` on 2026-11-12 picked `https://container.parishesonline.com/bulletins/03/1118/20261115B.pdf` (the 15 November 2026 issue; freshness `future`, the right pick mid-week; identity unverified as reported, masthead checked by hand above).

## Not yet confirmed

The new St. Charles Sunday schedule takes effect 6 December 2026; the church rows don't carry times, so nothing changes here.
