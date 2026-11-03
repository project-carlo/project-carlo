---
name: Holy Family Parish
website: https://www.holyfamilyforall.org
bulletin_provider: parishes_online
provider_id: st-ladislaus-church-08901
publication: ['po-container:03/0936', 'po-org:st-ladislaus-church-08901', 'lpi:0018000000QxA3vAAF', 'po-org:st-joseph-church-08901',
  'lpi:0018000000QxA3uAAF']
group: ''
evidence:
- url: https://www.holyfamilyforall.org/wp-content/uploads/2026/10/20261101B-3.pdf
  seen: 2026-11-03
  quote: Sacred Heart - St. Joseph - St.Ladislaus Churches, New Brunswick NJ
  note: 'Page 1 masthead of the 1 November 2026 issue (6 pages, text), posted on the parish''s WordPress
    News page: ''Holy Family Parish'', ''HFP PARISH CENTER 56 Throop Ave, New Brunswick'', ''Rev. Thomas
    RYAN, D. Min., pastor'', ''Rev. Fredy TRIANA, parochial vicar''. ''We worship: The Lord''s Day: 4:30pm
    Sat. Vigil at Sacred Heart; 8:00am (English, St. Ladislaus); 9:00am (Polish, St. Joseph); 9:00am (Hungarian,
    St. Ladislaus); 10:00am (Spanish/English, Sacred Heart); 12:00pm (Spanish, St. Joseph); 7:00pm (Spanish,
    St. Joseph)''; weekdays at St. Ladislaus and Sacred Heart, Tuesday evening at St. Joseph. Page 6 footer:
    ''Holy Family Parish at Sacred Heart Church | 03-0936'', www.4lpi.com.'
- url: https://container.parishesonline.com/bulletins/03/0936/20261108B.pdf
  seen: 2026-11-03
  quote: THIRTY-SECOND SUNDAY in  ORDINARY TIME
  note: 'probe container 03/0936: the 8 November 2026 issue is already posted (6 pages); page 2''s Mass
    intentions list (SH), (SL) and (SJ) Masses, the same three churches.'
- url: https://www.parishesonline.com/organization/st-ladislaus-church-08901
  seen: 2026-11-03
  note: 'probe po: organization ''St. Ladislaus Church'', 215 Somerset St, New Brunswick 08901; ids po-org:st-ladislaus-church-08901,
    lpi:0018000000QxA3vAAF, po-container:03/0936; latest issue 2026-11-01. A second organization, st-joseph-church-08901
    (''St. Joseph Church'', 15 Maple St; lpi:0018000000QxA3uAAF), points to the same container 03/0936,
    so both orgs are one bulletin.'
- url: https://www.holyfamilyforall.org/liturgy-sacraments/worship/
  seen: 2026-11-03
  quote: Masses are held in Sacred Heart Church (56 Throop Ave.), St. Ladislaus Church (213 Somerset St.),
    and St. Joseph Church (293 Somerset St.)
promoted: 2026-11-03
bulletin_status: available
---

## Publisher

Holy Family Parish, New Brunswick (parish center 56 Throop Avenue), publishes one weekly bulletin for its three churches through LPi / ParishesOnline, container 03/0936. The parish's own WordPress site posts the same LPi files under LPi names (`20261101B-3.pdf`) on its News page. The 1 November 2026 issue (page 1, read 2026-11-03) is headed 'Holy Family Parish / Sacred Heart - St. Joseph - St.Ladislaus Churches, New Brunswick NJ' and names Rev. Thomas Ryan, D. Min., as pastor and Rev. Fredy Triana as parochial vicar, matching the finder. Its footer reads 'Holy Family Parish at Sacred Heart Church | 03-0936'. The container already holds the 8 November issue.

Two ParishesOnline organizations, `st-ladislaus-church-08901` and `st-joseph-church-08901`, both point to container 03/0936. They are org names left from before the merger, not separate bulletins, so all their ids go on this one row. No Sacred Heart org was found (`sacred-heart-church-08901` and several other guessed slugs do not exist).

## Worship sites

The masthead's 'We worship' schedule covers three churches, each with weekend Mass:

- Sacred Heart, 56 Throop Avenue (`sacred-heart-new-brunswick`): Saturday 4:30 pm vigil, Sunday 10:00 am, weekdays 8:00 am.
- St. Ladislaus, 215 Somerset Street (`st-ladislaus-new-brunswick`): Sunday 8:00 am English and 9:00 am Hungarian, weekdays 7:00 am.
- St. Joseph, 293 Somerset Street at Maple Street (`st-joseph-new-brunswick`): Sunday 9:00 am Polish, 12:00 pm and 7:00 pm Spanish, Tuesday 7:00 pm.

The finder's worship-site list (directory:24513) and GCatholic (18631, 18666, 18671) name the same three churches and no others.

## Website and bulletin provider

Website https://www.holyfamilyforall.org (WordPress; `probe url` said DEAD-DNS on 2026-11-03, but `probe get` loaded it). Bulletin: ParishesOnline, `provider_id` the St. Ladislaus org slug, which carries container 03/0936. Either org slug reaches the same container.

## Not yet confirmed

Nothing about the publisher.

## Fetch check

`pnpm fetch:check` on 2026-11-03 resolved the ParishesOnline organization and picked container.parishesonline.com/bulletins/03/0936/20261101B.pdf: transport ok, PDF, issue date inferred from the file name (2 days old, freshness `fresh`), identity unverified by the tool. I read the 1 November masthead myself (above). No `recipe` is needed for ParishesOnline.
