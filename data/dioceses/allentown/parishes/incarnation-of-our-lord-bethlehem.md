---
name: Incarnation of Our Lord Parish
website: https://www.incarnationofourlord.org/bulletins/
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.incarnationofourlord.org/bulletins/']
group: 'Rev. Andrew N. Gehringer, pastor of Holy Infancy and Incarnation of Our Lord'
revisit: 'Confirm a new issue after 2026.10.03 has been posted, and that the pipeline can fetch over the incomplete TLS chain.'
revisit_after: 2026-10-26
evidence:
- url: https://www.incarnationofourlord.org/wp-content/uploads/2026/10/2026.10.03.pdf
  seen: 2026-10-18
  quote: Incarnation of our lord parish
  note: 'Page 1 of the issue dated "OCTOBER 3rd – 11th, 2026" (two weekends per issue): "Incarnation of our lord
    parish, 617 Pierce St., Bethlehem, PA 18015-3427", Pastor Rev. Andrew N. Gehringer, Parish Secretary Beth
    Perkins. Saturday "Confessions/Adoration 3:00PM – 4:00PM", "Vigil – 27th Sunday in Ordinary Time 4:15PM";
    Sunday "10:00AM – Mass in Ordinariate Form". The site''s TLS chain is incomplete: curl and Python refuse it,
    so the PDF was downloaded through Chrome.'
- url: https://www.incarnationofourlord.org/bulletins/
  seen: 2026-10-18
  note: The parish's Bulletins page (WordPress; read in a browser) lists self-hosted PDFs newest first, 2026.10.03,
    2026.09.26, 2026.09.19, 2026.09.12, 2026.08.29, 2026.08.15 ...
- url: https://container.parishesonline.com/bulletins/03/1407/20261018B.pdf
  seen: 2026-10-18
  note: 'Holy Infancy''s 18 October 2026 bulletin (page 2, image) announces "3 PM to 4 PM Confessions and 4:15 PM
    Vigil Mass at Incarnation Church, 617 Pierce St., Bethlehem" for Saturday 24 October.'
---

## Publisher

Incarnation of Our Lord, 617 Pierce Street, South Bethlehem, publishes its own bulletin on
its WordPress site, one PDF per issue named by the Saturday it starts. I read the newest one
listed on 18 October 2026, `2026.10.03.pdf`, headed "OCTOBER 3rd – 11th, 2026": the masthead
names Incarnation alone (pastor Rev. Andrew Gehringer, secretary Beth Perkins, its own
collection report). Issues are spaced one to two weeks apart (09.12, 09.19, 09.26, 10.03), and
this one covers two weekends.

Its pastor also leads Holy Infancy, whose ParishesOnline bulletin advertises Incarnation's
Saturday Vigil; Holy Infancy's bulletin does not carry Incarnation's masthead, intentions or
finances, and this site keeps posting Incarnation's own issues, so the two are separate rows
(one live member channel means no merge).

## Worship sites

- Incarnation of Our Lord, 617 Pierce Street, Bethlehem (`incarnation-of-our-lord-bethlehem`):
  Saturday Vigil 4:15 PM, and a Sunday 10:00 AM "Mass in Ordinariate Form" (the Anglican-use
  liturgy of the Personal Ordinariate; the bulletin gives it as Incarnation's Sunday Mass and
  names no separate community).

## Website and bulletin provider

`other`, self-hosted: the website is the /bulletins page that lists the PDFs. The site's TLS
certificate chain is incomplete (curl: "unable to get local issuer certificate"; Chrome
completes it). See the fetch check below for whether the pipeline can read it.

## Not yet confirmed

- No issue for 17–18 October was posted by 18 October; the newest covers 3–11 October.
  Re-check the page after 25 October that issues keep coming.
- Who celebrates the Sunday Ordinariate Mass (the parish clergy or an Ordinariate priest) is
  not stated; it does not change the row.
