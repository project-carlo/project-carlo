---
name: Most Blessed Trinity
website: https://mostblessedtrinity.us/parish-bulletins/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://mostblessedtrinity.us/parish-bulletins/']
group: ''
evidence:
- url: https://mostblessedtrinity.us/wp-content/uploads/2026/10/10-18-26-The-Twenty-Ninth-Sunday-in-Ordinary-Time-Website-Edition.pdf
  seen: 2026-10-18
  note: 'Page 1 of the 18 October 2026 issue, an image with no text layer (rendered with parish-site-access
    render.py and read): "Most Blessed Trinity Parish of the Diocese of Allentown", "Church/Rectory: 113 Cherry
    Street, Tremont, PA 17981", "Chapel: 840 E. Grand Avenue, Tower City, PA 17980"; "Liturgical Schedule
    Church: Saturday Vigil 4:00 PM, Sunday 10:30 AM Chapel: Sunday 9:00 AM Daily Masses: 9:00 AM, except for
    Tuesday at 6:00 PM in the Tremont Church, no Saturdays."'
- url: https://mostblessedtrinity.us/
  seen: 2026-10-18
  quote: 9:00 AM - Mass (Chapel - Tower City) 10:30 AM - Mass (Church - Tremont)
  note: 'Homepage "Sunday Liturgy Schedule": also "4:00 PM - Mass (Church - Tremont)" on Saturday; footer "Ss.
    Peter & Paul Chapel 840 E. Grand Avenue Tower City, PA 17980".'
- url: https://mostblessedtrinity.us/parish-history/
  seen: 2026-10-18
  quote: Most Blessed Trinity Church now occupies the former Immaculate Conception Church building in Tremont
    and the parish also has a Chapel located in the former Ss. Peter & Paul Church building in Tower City.
  note: 'The same page: the parish "was established on July 15, 2008" from Sacred Heart of Jesus in Newtown,
    Immaculate Conception in Tremont and Saints Peter & Paul in Tower City.'
- url: https://mostblessedtrinity.us/parish-bulletins/
  seen: 2026-10-18
  note: 'probe url: the "Parish Bulletins" page links one PDF per Sunday under /wp-content/uploads/YYYY/MM/,
    named like "10-18-26-The-Twenty-Ninth-Sunday-in-Ordinary-Time-Website-Edition.pdf", newest 18 October 2026.'
- url: https://www.allentowndiocese.org/places/most-blessed-trinity
  seen: 2026-10-18
  quote: 'Weekend Mass Tower City: | Sunday 9 a.m.'
---

## Publisher

Most Blessed Trinity, Tremont, publishes its own weekly bulletin as PDFs on its WordPress
site. I read the 18 October 2026 issue. Page 1 is an image with no text, which I rendered
and read. Its masthead is "Most Blessed Trinity Parish of the Diocese of Allentown", with
"Church/Rectory: 113 Cherry Street, Tremont" and "Chapel: 840 E. Grand Avenue, Tower City".
Its "Liturgical Schedule" gives the Church Saturday Vigil 4:00 PM and Sunday 10:30 AM, the
Chapel Sunday 9:00 AM, and daily Masses in the Tremont church. It covers two worship sites.
The parish was formed on 15 July 2008 from Sacred Heart of Jesus (Newtown), Immaculate
Conception (Tremont) and Ss. Peter & Paul (Tower City), per its history page. Nothing groups
it with another parish.

## Worship sites

- Most Blessed Trinity Church, 113 Cherry St., Tremont, the former Immaculate Conception
  church (`most-blessed-trinity-tremont`).
- Ss. Peter & Paul Chapel, 840 E. Grand Avenue, Tower City, the former Ss. Peter & Paul
  church (`ss-peter-paul-chapel-tower-city`). Neither roster lists it: GCatholic has no Tower
  City entry, and the diocesan map mentions it only inside the Tremont entry ("Weekend Mass
  Tower City: Sunday 9 a.m."). It's a church row because the bulletin, the parish site and
  the diocese all give it a Sunday Mass.

Sacred Heart of Jesus, Newtown, closed as a parish in 2008. The parish history calls it one
of "the closed parishes that formed Most Blessed Trinity", and nothing current lists a Mass
there. It's in neither roster, so it has no record of its own.

## Website and bulletin provider

`other`: the "Parish Bulletins" page (mostblessedtrinity.us/parish-bulletins/) links one
PDF per Sunday from /wp-content/uploads/, dated in the file name ("10-18-26-...pdf"). The
issue was up on the Sunday. **The bulletins are image-only**: the 4, 11 and 18 October 2026
issues have no text layer, so the pipeline has to read them as images.

Fetch check (2026-10-18, `fetch_check_rows.py`): the resolver read the Parish Bulletins
page ("page-pdfs ... current") and picked the 18 October 2026 issue, which is this week's.
Its recipe, `page-pdfs`, is recorded as `provider_id`.

## Not yet confirmed

Nothing. The bulletin's text can only be read from images.
