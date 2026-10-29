---
name: St. Agnes
website: https://stagneschurch.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-agnes-roman-catholic-church-sellersville-pa-18960
publication: ['url:https://www.church-bulletin.org/saint-agnes-roman-catholic-church-sellersville-pa-18960']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-agnes-roman-catholic-church-sellersville-pa-18960/2026-10-25.pdf
  seen: 2026-10-29
  note: 'John Patrick listing 225, issue of 25 October 2026 (8 pages, image only, md5 008518b9c7eb3a2eefd5a7f238c5e234;
    read by rendering pages 1-2). Page 1 masthead ''St. Agnes Roman Catholic Church, 445 N. Main Street,
    Sellersville, PA 18960'', Rev. Anthony T. Rossi, Pastor; Mass Schedule: Saturday Vigil 5:15 PM, Sundays
    8:00 AM, 10:00 AM and 12:00 (Noon), Weekdays 8:00 AM (Monday-Friday), Saturdays 9:00 AM, Holy Days
    Vigil 5:15 PM, 9:00 AM and 7:00 PM. Page 2 header ''St. Agnes Church #225''. It also lists the ''St.
    John Paul II Adoration Chapel'' (open all days, access code), with no Mass.'
- url: https://www.church-bulletin.org/saint-agnes-roman-catholic-church-sellersville-pa-18960
  seen: 2026-10-29
  quote: Latest Edition
  note: Listing 225 'Saint Agnes Roman Catholic Church', Sellersville, PA 18960; weekly issues 2026-10-11,
    2026-10-18 and 2026-10-25 listed.
- url: https://stagneschurch.org/
  seen: 2026-10-29
  note: 'probe url (HTTP 200): the home page links https://church-bulletin.org/?id=225 and http://www.jppc.net/onlinebulletins/225template.pdf
    as its bulletin and hosts no PDFs of its own.'
bulletin_status: available
---

## Publisher

St. Agnes, Sellersville (Rev. Anthony T. Rossi, pastor) is a single-church parish. Its weekly bulletin is John Patrick Publishing's listing 225 ('Saint Agnes Roman Catholic Church', Sellersville, PA 18960), the channel the parish home page links (`church-bulletin.org/?id=225`, `jppc.net/onlinebulletins/225template.pdf`). The 25 October 2026 issue is image only (`pdftotext` and `probe pdf` read no text), so I rendered pages 1 and 2: page 1 carries the masthead 'St. Agnes Roman Catholic Church, 445 N. Main Street, Sellersville, PA 18960', the staff list and the Mass Schedule; page 2 is headed 'St. Agnes Church #225'.

## Worship sites

One church, `st-agnes-sellersville`. The bulletin also lists a 'St. John Paul II Adoration Chapel' (open all days, door code on the website) and a Monday 6:30 PM Rosary there; no Mass is listed, so it is not a church row. The directory shows a cemetery at the same address.

## Website and bulletin provider

`other`, reading `page-pdfs` on the listing. The parish site hosts no PDFs of its own. Because the current issue has no text layer, `fetch:check` reports `publication_identity` unverified, by design; the masthead above was read from the render. Older issues may carry a text layer.

## Fetch check

`fetch:check` (2026-10-29, headed Chrome) with the `page-pdfs` recipe in `provider_id` picked `https://www.church-bulletin.org/bulletin/saint-agnes-roman-catholic-church-sellersville-pa-18960/2026-10-25.pdf`: transport ok, PDF, fresh (4 days); issue date inferred from the file name; the first page has no extractable text. The check printed no separate recipe; the one in `provider_id` is the one used. Identity is `unverified` only because the check is given no expected identity; the masthead was read from the file (above).
