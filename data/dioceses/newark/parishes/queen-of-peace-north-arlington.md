---
name: Our Lady Queen of Peace, North Arlington
website: https://qpcna.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/621
publication: ['url:https://www.church-bulletin.org/queen-of-peace-church-north-arlington-nj-07031']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/queen-of-peace-church-north-arlington-nj-07031/2026-11-01.pdf
  seen: 2026-11-03
  note: 'Page 1 (an image; rendered with parish-site-access render.py, so recheck can''t find the words)
    of the 1 November 2026 issue, 8 pages: ''NOVEMBER 1, 2026 | THIRTY-FIRST SUNDAY IN ORDINARY TIME'',
    ''Our Lady Queen of Peace Church, 10 FRANKLIN PLACE, NORTH ARLINGTON, NJ 07031'', www.qpcna.org, pastor
    Rev. Yuvan Alvarez. Regular Mass Schedule: Monday to Friday 7:30 AM, 9:00 AM, 5:30 PM; Saturday 7:30
    AM, 9:00 AM, 5:00 PM (Anticipated Mass); Sunday 7:30 AM, 9:00 AM (Spanish), 10:30 AM, 12 NOON. No
    other worship site is named.'
- url: https://www.church-bulletin.org/bulletin/queen-of-peace-church-north-arlington-nj-07031/2026-11-01.pdf
  seen: 2026-11-03
  note: 'Page 8 (image) footer: ''621 Queen of Peace, N. Arlington, NJ (back)'' and ''John Patrick Publishing
    Company • 800-333-3166 • www.jppc.net''.'
- url: https://church-bulletin.org/621
  seen: 2026-11-03
  quote: Queen of Peace Church Bulletin
  note: 'probe get: the John Patrick listing (page title) links bulletin/queen-of-peace-church-north-arlington-nj-07031/2026-11-01.pdf,
    2026-10-25.pdf, 2026-10-18.pdf.'
- url: https://qpcna.org/
  seen: 2026-11-03
  note: The WordPress homepage links https://www.jppc.net/onlinebulletins/621template.pdf as its bulletin
    (read from the page source with probe get).
bulletin_status: available
---

## Publisher

John Patrick Publishing prints the bulletin (id 621). I read the 1 November 2026 issue (8 pages, all images; pages 1, 2 and 8 rendered with render.py): the page-1 masthead reads "Our Lady Queen of Peace Church, 10 Franklin Place, North Arlington, NJ 07031", dated November 1, 2026, pastor Rev. Yuvan Alvarez, and the page-8 footer reads "621 Queen of Peace, N. Arlington, NJ (back) … John Patrick Publishing Company".

## Worship sites

One church, `queen-of-peace-north-arlington`. The page-1 Regular Mass Schedule gives weekdays 7:30, 9:00 AM and 5:30 PM, Saturday 7:30, 9:00 AM and 5:00 PM (anticipated) and Sunday 7:30, 9:00 (Spanish), 10:30 AM and 12 noon, with no other place named. The archdiocese directory (151) and GCatholic (18515) each list only this church.

## Website and bulletin provider

The website is the directory's https://qpcna.org/, whose homepage links jppc.net/onlinebulletins/621template.pdf. Provider `other`, pinned to `page-pdfs https://church-bulletin.org/621` per the playbook. GCatholic's http://www.qpgs.org/church.htm is an older (school) domain, not checked. The bulletin is image-only, so the pipeline has to read it as images.

Fetch check (2026-11-03, headed): ok, PDF, resolved `page-pdfs on https://church-bulletin.org/621: current` and picked bulletin/queen-of-peace-church-north-arlington-nj-07031/2026-11-01.pdf, the 1 November 2026 issue read above (date from the URL); freshness fresh (2 days). Identity `unverified` only because no expected identity is supplied; the rendered masthead confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open.
