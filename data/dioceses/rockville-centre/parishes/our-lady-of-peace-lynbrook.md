---
name: Our Lady of Peace Catholic Community
website: https://olplynbrook.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-of-peace-catholic-community-lynbrook-ny-11563
publication: ['url:https://www.church-bulletin.org/our-lady-of-peace-catholic-community-lynbrook-ny-11563']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-of-peace-catholic-community-lynbrook-ny-11563/2026-11-15.pdf
  seen: 2026-11-12
  note: 'Page 1 masthead of the 15 November 2026 issue (12 pages, all images; read rendered with render.py,
    so recheck can''t find text) names "Our Lady of Peace Catholic Community" alone: Weekday Mass Monday-Friday
    7:00 AM, 9:00 AM, Saturday 9:00 AM; Sunday Mass Saturday 5:00 PM, Sunday 8:00 AM, 10:00 AM, 12:00
    PM; footer "25 Fowler Avenue • Lynbrook, NY 11563 • olplynbrook.com".'
- url: https://www.olplynbrook.com
  seen: 2026-11-12
  note: The home page (visit.py --bulletin; probe url could not connect) links the bulletin listing at
    church-bulletin.org/our-lady-of-peace-catholic-community-lynbrook-ny-11563, which lists weekly PDFs
    from 2026-11-15 back through 2026-09-20.
bulletin_status: available
---

## Publisher

Our Lady of Peace, 25 Fowler Avenue, Lynbrook publishes its own weekly bulletin through John Patrick Publishing (church-bulletin.org). Page 1 of the 15 November 2026 issue (`https://www.church-bulletin.org/bulletin/our-lady-of-peace-catholic-community-lynbrook-ny-11563/2026-11-15.pdf`, 12 pages, read 2026-11-12 as a rendered image) has the masthead "Our Lady of Peace Catholic Community" alone. It gives Weekday Mass Monday-Friday at 7:00 AM and 9:00 AM and Saturday at 9:00 AM, and Sunday Mass Saturday at 5:00 PM and Sunday at 8:00 AM, 10:00 AM and 12:00 PM. The footer reads "25 Fowler Avenue • Lynbrook, NY 11563 • olplynbrook.com".

The drvc.org Mass-times page (read 2026-11-12) gives an older Sunday schedule (8:00, 9:30, 11:00 AM, 12:30 PM); the bulletin is followed.

## Worship sites

One: the church at 25 Fowler Avenue (`our-lady-of-peace-lynbrook-church`). The diocesan locator (directory:22), GCatholic (16875) and the Mass-times page list only this building, and the masthead gives the Masses with no other place.

## Website and bulletin provider

olplynbrook.com is the parish site. `probe url` could not connect to it (egress proxy EOF), but it loaded in `visit.py` (2026-11-12) and links the bulletin listing `https://www.church-bulletin.org/our-lady-of-peace-catholic-community-lynbrook-ny-11563`, where the PDFs are named by date (`/bulletin/<id>/2026-11-15.pdf`). The issues are image-only: `probe pdf` finds no text on any of the 12 pages, so the pipeline has to read them as images.

## Not yet confirmed

Nothing open.
