---
name: Holy Trinity Church, Hackensack
website: https://www.hthackensack.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6004
publication: ['url:https://www.church-bulletin.org/holy-trinity-catholic-church-hackensack-nj-07601']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/holy-trinity-catholic-church-hackensack-nj-07601/2026-11-01.pdf
  seen: 2026-11-03
  note: 'Page 1 of the 1 November 2026 issue (image only, no text layer; read rendered with parish-site-access
    render.py). Masthead shows HOLY TRINITY CHURCH, Roman Catholic, est. 1861, "Church: 34 Maple Avenue
    · Parish Center & Office: 20 Pangborn Place · Hackensack, NJ 07601". SUNDAY MASS: Saturday Vigil 5:00
    PM English, 6:30 PM Español; Sunday 7:00 AM English, 8:00 AM Español – Misa Solemne, 9:30 AM Español,
    11:00 AM English – Solemn Mass, 4:00 PM Tagalog (2nd Sunday). DAILY MASS: Monday–Friday 7:00 AM &
    12:10 PM, Saturday 8:00 AM, Lun./Miér./Vie. 7:00 PM en español; "Morning Masses in the Parish Center
    Chapel".'
- url: https://www.church-bulletin.org/holy-trinity-catholic-church-hackensack-nj-07601
  seen: 2026-11-03
  quote: holy-trinity-catholic-church-hackensack-nj-07601/2026-11-01.pdf
  note: John Patrick Publishing listing (church-bulletin.org/?id=6004 lands here), one PDF per Sunday,
    newest 2026-11-01.
- url: https://www.hthackensack.org/bulletins
  seen: 2026-11-03
  note: Parish Squarespace bulletins page; links /s/6004101826.pdf and /s/6004102526.pdf (John Patrick
    file names, id 6004 + MMDDYY) and older /s/2025MMDD.pdf files; newest posted is 25 October 2026, one
    week behind church-bulletin.org.
- url: https://www.hthackensack.org/mass-times
  seen: 2026-11-03
  quote: Mon- Fri 7:00 AM Parish Center Chapel 12:10 PM Main Church
  note: Parish site Mass Times page; Saturday 8:00 AM also in the Parish Center Chapel.
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

Holy Trinity, 34 Maple Avenue, Hackensack, publishes its own weekly bulletin through John Patrick Publishing (id 6004). I read page 1 of the 1 November 2026 issue (image only, rendered): its masthead names Holy Trinity Church alone, "Church: 34 Maple Avenue · Parish Center & Office: 20 Pangborn Place".

## Worship sites

- Holy Trinity Church, 34 Maple Avenue (`holy-trinity-hackensack`): every weekend Mass and the 12:10 PM weekday Mass ("Main Church" on the Mass Times page).
- Parish Center Chapel, 20 Pangborn Place (`holy-trinity-parish-center-chapel-hackensack`): the bulletin says "Morning Masses in the Parish Center Chapel" (Monday–Friday 7:00 AM, Saturday 8:00 AM), and the site's Mass Times page agrees. It is a separate building at the parish center's address, with daily Mass on the public schedule, so it is its own church row.

The directory (56) and GCatholic (18415) list only the church.

## Website and bulletin provider

The directory's https://www.hthackensack.org/ is the parish's Squarespace site (GCatholic's holytrinitysite.org was not checked). Its /bulletins page posts copies of the John Patrick PDFs but ran a week behind on 3 November, so the recipe reads the church-bulletin.org listing instead. Provider `other`. The bulletin is image-only (no text on any of the 9 pages of the 25 October issue), so the pipeline has to read it as images.

Fetch check (2026-11-03): `page-pdfs on https://church-bulletin.org/6004: current`, picked the 2026-11-01 PDF. Recipe pinned in `provider_id`.

## Not yet confirmed

Nothing open.
