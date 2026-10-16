---
name: St. Michael Parish
website: https://stmichaelscanton.com/bulletins/
bulletin_provider: other
provider_id: ''
publication: ['url:https://stmichaelscanton.com/bulletins/']
group: Saint Michael Parish Canton
evidence:
- url: https://cdn.diocesanweb.org/crossroads/micanton/wp-content/uploads/2026/10/2026-29th-Sunday-in-Ordinary-Time-bulletin-7.pdf
  seen: 2026-10-16
  quote: (covering worship sites in Ralston, Canton & Troy)
  note: 'Masthead, page 1 of the 18 October 2026 issue (29th Sunday in Ordinary Time), under "Reverend
    Joseph P. Kutch, MA, Pastor / 106 N. Washington Street, Canton, PA 17724".'
- url: https://cdn.diocesanweb.org/crossroads/micanton/wp-content/uploads/2026/10/2026-29th-Sunday-in-Ordinary-Time-bulletin-7.pdf
  seen: 2026-10-16
  quote: 8:00 am, Ralston … 9:30 am, Canton … 11:15 am, Troy
  note: 'Page 2 "LITURGY SCHEDULE": Saturday 17 Oct 4:00 pm Canton; Sunday 18 Oct 8:00 am Ralston, 9:30
    am Canton, 11:15 am Troy; weekdays at the Canton rectory chapel, Troy (Tue 5:30 pm) and Canton (Wed
    5:30 pm).'
- url: https://stmichaelscanton.com/bulletins/
  seen: 2026-10-16
  note: The parish's bulletin page lists one PDF per Sunday on cdn.diocesanweb.org (199 links, 2023 to
    the 18 October 2026 issue).
- url: https://stmichaelscanton.com/mass-times/
  seen: 2026-10-16
  quote: 8:00 AM Saint Aloysius Church, Ralston; 9:30 AM Saint Michael Church, Canton; 11:15 AM Saint John Nepomucene Church, Troy
---

## Publisher

St. Michael Parish, Canton (Rev. Joseph P. Kutch) publishes one weekly bulletin for its three
churches. The 18 October 2026 issue's masthead (page 1) reads "(covering worship sites in
Ralston, Canton & Troy)", and its page 2 liturgy schedule has the weekend Masses at all three:
Saturday 4 pm Canton, Sunday 8 am Ralston, 9:30 am Canton and 11:15 am Troy. The diocesan
finder lists the same three worship sites under "Saint Michael Parish Canton". No neighbouring
parish shares this bulletin or this pastor (Mansfield, Towanda and Wellsboro each have their
own pastor and bulletin).

## Worship sites

Three, all with Sunday Mass in the 18 October 2026 schedule:

- `st-michael-canton` (St. Michael, Canton; church and parish row share the slug)
- `st-john-nepomucene-troy` (St. John Nepomucene, Troy)
- `st-aloysius-ralston` (St. Aloysius, Ralston)

The parish site's About page lists exactly these three churches; no roster lists any other
building for this parish.

## Website and bulletin provider

The bulletin page https://stmichaelscanton.com/bulletins/ (the parish's WordPress site, hosted
by Diocesan/Crossroads) links one PDF per Sunday under
`cdn.diocesanweb.org/crossroads/micanton/wp-content/uploads/<yyyy>/<mm>/<yyyy>-<Nth>-Sunday-...-bulletin.pdf`,
with the newest issue (18 October 2026) already up on 16 October. The file names carry the
liturgical Sunday, not a date, so the `other` resolver has to read the page. No ParishesOnline,
eCatholic or Discover Mass id was found (`probe url` on the homepage found none).
`provider_id` is left empty until a `fetch:check` run after promotion suggests a recipe
(likely `page-pdfs`).

## Not yet confirmed

Nothing about structure. The recipe for the `other` resolver is still to be pinned after
promotion.
