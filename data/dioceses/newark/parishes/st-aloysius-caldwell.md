---
name: St. Aloysius, Caldwell
website: https://stalscaldwell.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/691
publication: ['url:https://www.church-bulletin.org/saint-aloysius-parish-caldwell-nj-07006']
group: Planning Area G
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-aloysius-parish-caldwell-nj-07006/2026-11-01.pdf
  seen: 2026-11-04
  note: '1 November 2026 issue, 16 pages, image only (no text layer; read with render.py). Page 1 masthead:
    ''St. Aloysius Parish All Saints'' Day November 1, 2026''. Page 2: ''RECTORY Administrative Offices
    219 Bloomfield Avenue Caldwell, NJ 07006''; ''MASS SCHEDULE Saturday Evening: 5:30 pm Sunday: 7:30
    am • 9:00 am • 10:30 am • 12:00 pm Sunday Evening: 5:00 pm Spanish Mass Weekdays: 8:00 am • 12:00
    pm Saturday Morning: 8:00 am''; pastor Rev. Wojciech Jaskowiak; ''Church Website: StAlsCaldwell.org''.
    Page 16 footer: ''691 St. Aloysius, Caldwell, NJ (back) John Patrick Publishing Company, Inc.''.'
- url: https://church-bulletin.org/691
  seen: 2026-11-04
  quote: Saint Aloysius Parish Bulletin
  note: Redirects to church-bulletin.org/saint-aloysius-parish-caldwell-nj-07006 ('Caldwell, NJ 07006',
    'Latest Edition'); PDFs 2026-11-01, 2026-10-25, 2026-10-18, 2026-10-11 and weekly back.
- url: https://stalscaldwell.org/
  seen: 2026-11-04
  note: 'eCatholic site (id 14348); probe url got 403, visit.py (headed Chrome) read it: title ''Saint
    Aloysius Parish'', links ''Current Bulletin'' to jppc.net/onlinebulletins/691template.pdf, ''Bulletins''
    to church-bulletin.org/?id=691 and ''Bulletin Archive'' to /bulletins.'
bulletin_status: available
---

## Publisher

St. Aloysius, Caldwell, publishes a weekly bulletin printed by John Patrick Publishing (id 691). I read the 1 November 2026 issue (image only, rendered pages 1, 2 and 16): page 1 masthead 'St. Aloysius Parish All Saints' Day November 1, 2026'; page 2 gives the rectory at 219 Bloomfield Avenue, Caldwell, one Mass schedule (Saturday Evening 5:30 pm; Sunday 7:30, 9:00, 10:30 am and 12:00 pm; Sunday Evening 5:00 pm Spanish Mass; Weekdays 8:00 am and 12:00 pm; Saturday Morning 8:00 am) and the pastor, Rev. Wojciech Jaskowiak; page 16 footer '691 St. Aloysius, Caldwell, NJ (back) John Patrick Publishing Company, Inc.'.

## Worship sites

- St. Aloysius Church, 219 Bloomfield Avenue (`st-aloysius-caldwell`): the schedule names no other place; the Spanish Mass is listed in the same schedule with no other location (inferred to be in the church).

The directory (14) and GCatholic (18370) list only this church. The Parish Center at 253 Bloomfield Avenue (page 2) is the religious education office, not a worship site.

## Website and bulletin provider

https://stalscaldwell.org/ is eCatholic (id 14348) behind a 403 for `probe url`; in the browser it links the John Patrick template 691template.pdf and church-bulletin.org/?id=691. Following the playbook, the row pins `page-pdfs https://church-bulletin.org/691` (not `?id=`, which runs a week ahead) and leaves the eCatholic id out of `publication`, since the site's /bulletins archive is only a copy. The issues are image only (no text layer), so the pipeline has to read them as images.

Fetch check (2026-11-04, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/691: current` and picked church-bulletin.org/bulletin/saint-aloysius-parish-caldwell-nj-07006/2026-11-01.pdf, the 1 November 2026 issue read above (date inferred from the URL); freshness fresh (3 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open for the row.
