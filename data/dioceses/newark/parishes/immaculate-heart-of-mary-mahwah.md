---
name: Immaculate Heart of Mary, Mahwah
website: https://ihmcmahwah.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:5565']
group: ''
evidence:
- url: https://files.ecatholic.com/5565/bulletins/20261101.pdf
  seen: 2026-11-03
  quote: 47 Island Road Mahwah, NJ 07430
  note: 'Page 1 masthead of the 1 November 2026 (Solemnity of All Saints) issue names the Church of the
    Immaculate Heart of Mary alone, with Rev. Jacek Marchewka, Pastor, and its MASS SCHEDULE: Weekdays
    and Saturday 8am; Saturday Vigil 5pm; Sunday 7:30am, 9am (Polish), 10:30am, 12 Noon.'
- url: https://ihmcmahwah.org/
  seen: 2026-11-03
  note: 'Parish site, ''Login powered by eCatholic''; HTTP 403 to probe get, loaded with parish-site-access
    visit.py, which reported ecatholic:5565 and a Bulletins page. Homepage Mass schedule: SAT 5:00 PM;
    SUN 7:30 AM, 9:00 AM PL, 10:30 AM, 12:00 PM; M-Sa 8:00 AM.'
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

Immaculate Heart of Mary, 47 Island Road, Mahwah, publishes its own weekly bulletin on its eCatholic site (site 5565). I read the 1 November 2026 issue: the page 1 masthead names the Church of the Immaculate Heart of Mary, 47 Island Road, alone, with Rev. Jacek Marchewka as pastor and its own Mass schedule; page 2 lists that week's Mass intentions, all at this church.

## Worship sites

- Immaculate Heart of Mary Church, 47 Island Road (`immaculate-heart-of-mary-mahwah`): every Mass in the schedule (weekdays and Saturday 8am; Saturday vigil 5pm; Sunday 7:30am, 9am in Polish, 10:30am, 12 noon).

The directory (111) and GCatholic (18476) list only this church. It shares nothing with the other Mahwah parish, Immaculate Conception (`immaculate-conception-mahwah`), whose John Patrick bulletin (template 598) has its own masthead, pastor and Masses; the IHM issue of 1 November 2026 has no mention of "Immaculate Conception" (grep, 0 hits).

## Website and bulletin provider

https://ihmcmahwah.org/ is the eCatholic-hosted parish site. It answers `probe get` with 403 (Cloudflare), but parish-site-access's `visit.py` loaded it on the first try and reported `ecatholic:5565`; the issues are at `files.ecatholic.com/5565/bulletins/YYYYMMDD.pdf` (issues.py found 20261101; 20261108 not yet up on 3 November). Provider `ecatholic`. The site has a Polish Apostolate and a Polish 9am Sunday Mass; the bulletin itself is in English with Polish items.

Fetch check (2026-11-03): the eCatholic resolver read https://ihmcmahwah.org/bulletins and picked `files.ecatholic.com/5565/bulletins/20261101.pdf` (`fresh`).

## Not yet confirmed

Nothing open.
