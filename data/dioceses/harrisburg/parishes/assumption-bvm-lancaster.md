---
name: Assumption of the Blessed Virgin Mary (Historic St. Mary's)
website: https://www.church-bulletin.org/assumption-of-the-blessed-virgin-mary-lancaster-pa-17603
bulletin_provider: other
provider_id: dated-post https://www.church-bulletin.org/assumption-of-the-blessed-virgin-mary-lancaster-pa-17603
publication: ['url:https://www.church-bulletin.org/assumption-of-the-blessed-virgin-mary-lancaster-pa-17603',
  'ecatholic:33649']
group: ''
evidence:
- url: https://www.church-bulletin.org/assumption-of-the-blessed-virgin-mary-lancaster-pa-17603
  seen: 2026-10-20
  quote: Assumption of the Blessed Virgin Mary Lancaster, PA 17603 Latest Edition October 18, 2026
  note: John Patrick Publishing's listing (church-bulletin.org/?id=242), linked as "Bulletin" from the
    parish's eCatholic bulletins page.
- url: https://stmaryslancaster.org/bulletins
  seen: 2026-10-20
  note: 'The parish''s eCatholic site (ecatholic:33649) is behind Cloudflare: plain curl gets the challenge,
    and parish-site-access visit.py was challenged on every one of about 26 loads on 19 October, then
    got through on the first load on 20 October. Its bulletins page has one "Bulletin" link, to https://church-bulletin.org/?id=242.'
- url: https://www.church-bulletin.org/bulletin/assumption-of-the-blessed-virgin-mary-lancaster-pa-17603/2026-10-18.pdf
  seen: 2026-10-20
  note: 'Image-only issue (8 pages, no text layer), read rendered (render.py). Page 1: "October 18, 2026
    | Twenty-ninth Sunday in Ordinary Time ... Mass Schedule. Daily Mass: Monday through Friday 12:05
    PM. Sunday Mass: Saturday Vigil 4:30 PM; Sunday 8:30 AM, 11:00 AM ... Assumption of the Blessed Virgin
    Mary, Est. 1741, Parish Office 717.392.2578, 119 S Prince St Lancaster, PA 17603". Page 2: "Rev. Brian
    T.C. Olkowski, Pastor" and Mass intentions for each of those Masses, 17-25 October.'
- url: https://lancasterlatinmass.com/mass-confession-schedule/
  seen: 2026-10-20
  quote: Holy Family Chapel at Historic St. Mary's Church 119 South Prince Street Lancaster, PA 17603
    Daily Mass is typically offered every Tuesday at 7:30 a.m.
  note: The Lancaster Latin Mass Community (of St. Joseph's parish) says the chapel "is on the 2nd floor
    of the old convent at Historic St. Mary's Church". Not in St. Mary's bulletin.
---

## Publisher

Assumption of the Blessed Virgin Mary ("Historic St. Mary's"), 119 S. Prince Street, Lancaster,
publishes its own weekly bulletin through John Patrick Publishing. The 18 October 2026 issue
(image-only; read rendered on 20 October) has a page 1 masthead "Assumption of the Blessed
Virgin Mary, Est. 1741 ... 119 S Prince St Lancaster, PA 17603" and one schedule: daily Mass
Monday-Friday 12:05 PM; Saturday Vigil 4:30 PM; Sunday 8:30 AM and 11:00 AM. Page 2 names Rev.
Brian T.C. Olkowski as pastor and lists intentions for each of those Masses. No other building
is named.

## Worship sites

One church, `assumption-bvm-lancaster`. Holy Family Chapel, on the second floor of the old
convent on the St. Mary's campus, has a Tuesday 7:30 a.m. Traditional Latin Mass of the
Lancaster Latin Mass Community (a community of St. Joseph's parish), per that community's
site; it is not in St. Mary's bulletin and has no row of its own (same address and campus;
see Not yet confirmed).

## Website and bulletin provider

`other`, website the church-bulletin.org listing, which lists dated PDFs
(/bulletin/<slug>/YYYY-MM-DD.pdf). The parish's eCatholic site stmaryslancaster.org
(ecatholic:33649, recorded as a publication id) posts no PDFs of its own; its bulletins page
links this listing. **Image-only bulletin:** the 18 October issue has no text layer, so the
pipeline must read it as an image. The parish's LPi organization
(assumption-of-the-blessed-virgin-mary-historic-st-marys-church) has no publications.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows, under xvfb-run with Chrome): "dated-post on https://www.church-bulletin.org/assumption-of-the-blessed-virgin-mary-lancaster-pa-17603: current", which is the 2026-10-18 issue, this week's bulletin, so the printed recipe is pinned as `provider_id`.

## Not yet confirmed

Whether Holy Family Chapel's weekly Latin Mass should be a church row of its own (a chapel in a
separate building on the same campus, published by the Latin Mass community's own site and
newsletter, not by this bulletin).
