---
name: St. Mary Parish
website: https://stmarystfd.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-mary-church-stamford-ct-06902
publication: ['url:https://www.church-bulletin.org/saint-mary-church-stamford-ct-06902']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-mary-church-stamford-ct-06902/2026-11-15.pdf
  seen: 2026-11-12
  note: '15 November 2026 issue, 8 pages, image-only (probe pdf: readable_pages 0); page 1 rendered. Masthead:
    ''St. Mary Parish - St. Benedict / OLOM Church, Stamford CT'', ''566 Elm Street, Stamford, CT 06902'',
    ''Thirty-Third Sunday in Ordinary Time, November 15th, 2026''; ''Rev. Juan Gabriel Acosta, Pastor''.'
- url: https://www.church-bulletin.org/bulletin/saint-mary-church-stamford-ct-06902/2026-11-15.pdf
  seen: 2026-11-12
  note: 'Page 1 (image) Mass schedule: Saturday Vigil at St. Benedict/OLOM 4:00 PM (English), 6:00 PM
    (Spanish); Sunday at St. Mary Church 8:00 AM (Spanish), 10:00 AM (English), 12:00 PM (Spanish), 5:00
    PM (English), 7:00 PM (Spanish); daily: St. Joseph''s Chapel (St. Mary) Monday-Friday 9:00 AM (English),
    St. Benedict/OLOM Monday-Friday 7:00 PM (Spanish); civil holidays St. Joseph''s Chapel 9:00 AM; confession
    Fridays 5:00-6:30 PM (St. Benedict/OLOM).'
- url: https://church-bulletin.org/?id=9003
  seen: 2026-11-12
  note: Linked from stmarystfd.org's home page; probe get followed it to https://www.church-bulletin.org/saint-mary-church-stamford-ct-06902,
    which lists dated issues bulletin/saint-mary-church-stamford-ct-06902/2026-11-15.pdf, 2026-11-08,
    2026-11-01, 2026-10-25 ...
- url: https://stmarystfd.org/
  seen: 2026-11-12
  quote: The original parish church, founded in 1907. Home to Sunday Masses in both English and Spanish,
    weekday Masses in the St. Joseph Chapel, and Sunday Adoration of the Blessed Sacrament.
  note: Parish site's card for St. Mary's Church, 566 Elm Street; a second card 'St. Benedict / OLOM Church',
    '1 St. Benedict Circle, Stamford, CT 06902', with Saturday Vigil and Spanish weekday Masses.
- url: https://www.bridgeportdiocese.org/wp-json/custom/v1/mass-times?parish_id=1451
  seen: 2026-11-12
  note: 'Diocese''s schedule for St. Mary Parish: Sunday 8:00, 10:00, 12:00, 17:00, 19:00 ''St. Mary'';
    Monday-Friday 09:00 ''St. Mary, in St. Joseph Chapel''; Monday-Friday 19:00 and Saturday 16:00, 18:00
    ''St. Benedict campus''.'
promoted: 2026-11-12
bulletin_status: available
---

## Publisher

John Patrick Publishing (church-bulletin.org) prints St. Mary's weekly bulletin. The 15 November 2026 issue (`https://www.church-bulletin.org/bulletin/saint-mary-church-stamford-ct-06902/2026-11-15.pdf`, read 2026-11-12) is image-only; page 1, rendered, has the masthead "St. Mary Parish - St. Benedict / OLOM Church, Stamford CT", "566 Elm Street, Stamford, CT 06902" and "Thirty-Third Sunday in Ordinary Time, November 15th, 2026", with Rev. Juan Gabriel Acosta, Pastor.

## Worship sites

The page 1 Mass schedule names two buildings:

- `st-mary-stamford`: Sunday 8:00 AM (Spanish), 10:00 AM, 12:00 PM (Spanish), 5:00 PM, 7:00 PM (Spanish); weekdays 9:00 AM in "St. Joseph's Chapel (St. Mary)", which the parish site calls "weekday Masses in the St. Joseph Chapel" of the 566 Elm Street church. The chapel is part of that church, not a separate place, so mass-times:1451-st-joseph-chapel is linked to this church row.
- `st-benedict-our-lady-of-montserrat-stamford`: Saturday Vigil 4:00 PM (English) and 6:00 PM (Spanish); Monday-Friday 7:00 PM (Spanish); confession Fridays. The former St. Benedict-Our Lady of Montserrat parish's church (GCatholic 21960; the diocese's 'St. Benedict campus'), on this row under the diocese's settled rule for merged parishes' campuses, since it publishes no bulletin of its own (the masthead names it).

The diocese's schedule for directory:1451 agrees on the times and places.

## Website and bulletin provider

`stmarystfd.org` links `https://church-bulletin.org/?id=9003`, which redirects to the parish's church-bulletin.org page listing dated PDFs (`bulletin/<slug>/<YYYY-MM-DD>.pdf`). Provider `other`, pinned `page-pdfs` on that page. The issues are image-only, so the pipeline's text extraction will need OCR.

`fetch:check` on 2026-11-12 (headed Chrome) with the pinned recipe picked `https://www.church-bulletin.org/bulletin/saint-mary-church-stamford-ct-06902/2026-11-15.pdf`, the 15 November 2026 issue whose masthead is read above (date from the file name; freshness `future`, the right pick mid-week).

## Not yet confirmed

Nothing open.
