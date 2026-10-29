---
name: St. Charles Borromeo Parish
website: https://www.churchofscb.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-charles-borromeo-church-sicklerville-nj-08081
publication: ['url:https://www.church-bulletin.org/saint-charles-borromeo-church-sicklerville-nj-08081#john-patrick-584']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-charles-borromeo-church-sicklerville-nj-08081/2026-10-25.pdf
  seen: 2026-10-29
  quote: ST. CHARLES BORROMEO CATHOLIC CHURCH
  note: 'Page 1 masthead of the 25 October 2026 issue (8 pages, image-only, read from a rendering): ''176
    Stagecoach Road - Sicklerville, New Jersey 08081'', www.churchofscb.org, ''Reverend Thomas A. Newton
    - Pastor'', John Patrick page code ''1 - 584''. Names this parish alone.'
- url: https://www.church-bulletin.org/bulletin/saint-charles-borromeo-church-sicklerville-nj-08081/2026-10-25.pdf
  seen: 2026-10-29
  quote: Saturday Vigil Mass 4:00 pm
  note: 'Page 1 side panel: Sunday Masses 7:30am, 9am & 11am; weekday Masses 9:00 am (Mon-Fri) in Emmaus
    Chapel; Emmaus Chapel open daily (Mon-Fri) 8:00 am - 2:00 pm; Reconciliation Saturday 3:00-3:30 pm.'
- url: https://www.churchofscb.org/bulletin
  seen: 2026-10-29
  quote: St. Charles Borromeo Catholic Church 176 Stagecoach Road, Sicklerville, NJ 08081
  note: 'Read in the browser (probe url answers 403): a Solutio CMS page whose ''This week''s Bulletin''
    link is /bulletin/17-this-week-s-bulletin-2/file, a fixed-name file with an archive page; the same
    parish, with address and phone 856-629-0411.'
- url: https://www.church-bulletin.org/saint-charles-borromeo-church-sicklerville-nj-08081
  seen: 2026-10-29
  note: 'Listing ''Saint Charles Borromeo Church Bulletin'' (John Patrick 584): 11 dated PDFs, weekly,
    latest 2026-10-25.'
research:
- method: pnpm fetch:check --diocese camden --parish st-charles-borromeo-sicklerville
  url: https://www.church-bulletin.org/saint-charles-borromeo-church-sicklerville-nj-08081
  checked: '2026-10-29'
  outcome: found
  next_action: None; the pick is the 2026-10-25 issue, whose masthead was read from a rendering (image-only
    PDF).
- method: probe url on the parish's own site (https://www.churchofscb.org) answered 403; read in the browser
    with visit.py instead
  url: https://www.churchofscb.org/bulletin
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: None needed while the church-bulletin.org listing serves each issue; if it stops, read
    the site's /bulletin/17-this-week-s-bulletin-2/file with the browser
  retry_when: The church-bulletin.org listing stops posting weekly issues
---

## Publisher

John Patrick Publishing (page code 584) prints the bulletin and the church-bulletin.org listing serves it. The 25 October 2026 issue (page 1, read 2026-10-29 from a rendering, since the PDF has no text layer) is headed "St. Charles Borromeo Catholic Church, 176 Stagecoach Road, Sicklerville, New Jersey 08081", names Rev. Thomas A. Newton as pastor, and lists Saturday vigil 4:00 pm, Sunday 7:30, 9 and 11 am, weekday Mass 9:00 am Monday to Friday in Emmaus Chapel. It names no other parish. The diocese directory (2015) gives Rev. Michael Matveenko as pastor; the 2026 bulletin names Fr. Newton, so the directory is out of date and there is no shared-pastor question here.

## Worship sites

One church, 176 Stagecoach Road, Sicklerville (Washington Township). Emmaus Chapel is a chapel at the church where the weekday Mass is said ("9:00 am (Mon-Fri) in Emmaus Chapel"); it is not a separate building in the bulletin and has no record of its own. The bulletin also names Our Lady of Hope Regional School, which is not a place of Mass.

## Website and bulletin provider

`other` with `page-pdfs` on the church-bulletin.org listing. The directory and GCatholic give saint-charles-borromeo.org, which now redirects to https://www.churchofscb.org (a Solutio CMS site: `probe url` gets 403, the browser loads it). Its own `/bulletin` page serves one fixed-name file, `/bulletin/17-this-week-s-bulletin-2/file`, plus an archive, which `fetch:check` cannot resolve under a Solutio site (see the playbook); the John Patrick listing found by the printer's page code is the stable source. The publication id is the listing URL with a John Patrick suffix.

## Not yet confirmed

Nothing blocking. Most issues are image-only, so `fetch:check` reports the date from the file name.
