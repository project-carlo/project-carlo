---
name: St. John the Evangelist
website: https://www.parishofsaintjohn.org
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/664
publication: ['url:https://www.church-bulletin.org/saint-john-the-evangelist-parish-lambertville-nj-08530']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-parish-lambertville-nj-08530/2026-11-01.pdf
  seen: 2026-11-02
  note: '1 November 2026 issue, 8 image-only pages (no text layer). Rendered page 1 masthead: ''St. John
    the Evangelist Parish'', Very Rev. Robert Kolakowski, JCD, Pastor; Parish Office 13 North Main Street,
    Lambertville; Mass schedule ''St John'' weekdays Monday-Friday 8:30 am, Saturday 5:00 pm, Sunday 8:00,
    9:30, 11:00 am; ''St Agnes'' Sunday English 9:30 am, Domingo Misa en Espanol 11:00 am; website parishofsaintjohn.org.'
- url: https://www.parishofsaintjohn.org/mass-times
  seen: 2026-11-02
  quote: 9:30 AM St. Agnes - Stockton
  note: The parish's eCatholic site (ecatholic:22624, loaded with visit.py) lists Saturday 5:00 PM, Sunday
    8:00, 9:30, 11:00 AM and Mon-Fri 8:30 AM at St John the Evangelist, and Sunday 9:30 AM and 11:00 AM
    Spanish at St. Agnes - Stockton. Its 'Current Bulletin' menu item links only https://www.jppc.net/onlinebulletins/664template.pdf.
- url: https://church-bulletin.org/664
  seen: 2026-11-02
  note: Redirects to the John Patrick listing saint-john-the-evangelist-parish-lambertville-nj-08530,
    weekly issues 2026-10-11 through 2026-11-01.
promoted: 2026-11-03
bulletin_status: available
---

## Publisher

St. John the Evangelist Parish, Lambertville, prints its weekly bulletin with John Patrick Publishing (church-bulletin.org id 664). The 1 November 2026 issue (read 2026-11-02) is image-only; its rendered page 1 masthead names 'St. John the Evangelist Parish', Very Rev. Robert Kolakowski, JCD, Pastor (as the finder says), the Parish Office at 13 North Main Street, Lambertville, and a Mass schedule for 'St John' and 'St Agnes'.

## Worship sites

Two churches, the two worship sites the finder lists (directory:24502): St. John the Evangelist, 44 Bridge Street, Lambertville (gcatholic:18659, worship-sites:st-john-the-evangelist-church), and St. Agnes, 21 South Main Street, Stockton (gcatholic:18660, worship-sites:st-john-the-evangelist-st-agnes-church). The masthead and the parish's Mass Times page both give St. Agnes Sunday 9:30 AM (English) and 11:00 AM (Spanish). The parish office at 13 North Main Street is not a church.

## Website and bulletin provider

The finder's `parishofsaintjohn.org` is the parish's eCatholic site (ecatholic:22624). `probe url` said DEAD-DNS and `probe get` got 403, but `visit.py` loaded it on 2026-11-02. Its 'Current Bulletin' menu item links only the John Patrick template `jppc.net/onlinebulletins/664template.pdf`, and no bulletin files are hosted on the eCatholic site, so per the playbook the row is provider `other` with `page-pdfs https://church-bulletin.org/664`. The eCatholic id is the website's, not the bulletin's, and is left out of `publication`.

## Not yet confirmed

Nothing about the publisher. The issues are image-only, so recheck quotes come from the parish's Mass Times page.

## Fetch check

`pnpm fetch:check` on 2026-11-02 (US Eastern) resolved `page-pdfs on https://church-bulletin.org/664: current` and picked `bulletin/saint-john-the-evangelist-parish-lambertville-nj-08530/2026-11-01.pdf` (5.2 MB, page 1 without text): transport ok, PDF, issue date 2026-11-01 from the file name, freshness `fresh`, identity unverified by the tool. That is the 1 November 2026 issue whose page 1 masthead I rendered and read. The recipe it used is the pinned `page-pdfs https://church-bulletin.org/664`.
