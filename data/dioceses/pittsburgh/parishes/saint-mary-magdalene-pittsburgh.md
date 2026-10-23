---
name: Saint Mary Magdalene Parish (Point Breeze, Homewood and Wilkinsburg)
website: https://www.saintmarymagdalenepgh.org
bulletin_provider: discover_mass
provider_id: st-bede-pittsburgh-pa
publication: ['discovermass:st-bede-pittsburgh-pa', 'discovermass:st-mary-magdalene-pa', 'discovermass:st-james-wilkinsburg-pa']
group: Saint Mary Magdalene Parish
evidence:
- url: https://discovermass.com/church/st-bede-pittsburgh-pa/
  seen: 2026-10-23
  quote: Mother of Good Counsel Church
  note: 'Issue of 25 October 2026 (listed on the church page; download token changes per load), page 1
    masthead, 12 pages: three church blocks ''St. Bede Church 509 South Dallas Avenue Pittsburgh PA 15208'',
    ''Mother of Good Counsel Church 7705 Bennett Street Pittsburgh PA 15208'', ''St. James Church 718
    Franklin Avenue Wilkinsburg PA 15221'', then ''October 25, 2026 - The Thirtieth Sunday in Ordinary
    Time''. The 18 October issue (same church page) has the same masthead and the Mass Schedule box on
    page 1: Saturday Vigil 4:00 pm St. James; Sunday 8:30 am and 11:00 am St. Bede; Monday - Saturday
    9:00 am St. Bede; Eucharistic Adoration Wednesday 7:00 pm and Saturday 9:30 am at St. Bede. Mass Intentions
    18-25 October list only St. James (Sat 4:00 pm) and St. Bede (all others). The text layer is letter-split
    in places; the quote is the clean masthead line.'
- url: https://discovermass.com/church/st-mary-magdalene-pa/
  seen: 2026-10-23
  note: Second DiscoverMass listing for the parish (titled 'St. Mary Magdalene Parish (St. Bede)'); its
    25 October 2026 issue has the same masthead page (three churches, Thirtieth Sunday in Ordinary Time)
    and 12 pages, so it carries the same bulletin.
- url: https://discovermass.com/church/st-james-wilkinsburg-pa/
  seen: 2026-10-23
  note: Third DiscoverMass listing (titled 'St. Mary Magdalene Parish (St. James)'); the 25 October 2026
    issue has the same masthead and page count. The parish site's two Bulletins links point at st-mary-magdalene-pa
    and st-james-wilkinsburg-pa; its /bulletins page redirects to st-bede-pittsburgh-pa.
- url: https://www.saintmarymagdalenepgh.org
  seen: 2026-10-23
  quote: Please note our Mass time change goes into effect Sunday, Oct. 18. Our 9am Mass will move to
    8:30am at St. Bede.
  note: 'Rendered in headed Chrome (visit.py; Cloudflare-protected eCatholic site 21498, no bulletin files:
    issues.py ecatholic answers 403 for three Sundays). Home page Mass box: Saturday 4:00 PM St. James;
    Sunday 8:30 AM St. Bede, 11:00 AM St. Bede; Daily Mon-Sat 9:00 AM St. Bede. It lists no Mass at Mother
    of Good Counsel. Nav: ''Parish Office & Churches'' with St. Bede, Mother of Good Counsel and St. James
    pages. Parish office 509 South Dallas Avenue, 412.661.7222.'
- url: https://parishesonline.com/organization/saint-mary-magdalene-parish
  seen: 2026-10-23
  note: 'probe po: LPi org 0018000000Qx7qIAAR ''Saint Mary Magdalene Parish'', 509 S Dallas Ave, ''no
    publications: this organization does not publish a bulletin here now''. An empty account, not a channel;
    not recorded as a publication id.'
- url: https://www.saintmarymagdalenepgh.org/history-of-our-parish
  seen: 2026-10-23
  quote: Saint Mary Magdalene Parish, in the East End of Pittsburgh, PA, was established on Jan. 6, 2020.
  note: Parish history page (headed Chrome). Merger of St. Bede (Point Breeze), St. Charles Lwanga (Homewood
    and Lincoln-Lemington; itself formed 1992 from six parishes) and St. James (Wilkinsburg). Also says
    'We continue to worship in three churches' (undated).
- url: https://diopitt.org/saint-mary-magdalene-parish
  seen: 2026-10-23
  note: 'Diocese parish page (directory roster): Rev. Adam C. Potter, STL (Administrator); Deacon John
    S. Maier; weekend schedule by church building: Saint Bede Sunday 9:00 a.m. | 11:00 a.m.; Saint James
    Saturday Vigil 4:00 p.m.; Mother of Good Counsel ''No Masses Scheduled''. The 9:00 a.m. is now 8:30
    a.m. (change effective 18 October 2026, per the parish site and bulletin).'
research:
- method: pnpm fetch:check --diocese pittsburgh --parish saint-mary-magdalene-pittsburgh (headed Chrome)
  url: https://discovermass.com/church/st-bede-pittsburgh-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: None; recheck after the 25 October issue rolls off (about twelve weeks).
  retry_when: Discover Mass changes the listing slug or the masthead drops a church
bulletin_status: available
---

## Publisher

Saint Mary Magdalene Parish (established 6 January 2020 from St. Bede, St. Charles Lwanga and St. James) publishes one weekly bulletin through J.S. Paluch's Discover Mass. The 25 October 2026 and 18 October 2026 issues (read 2026-10-23, 12 pages each) carry one masthead naming the three churches: "St. Bede Church 509 South Dallas Avenue", "Mother of Good Counsel Church 7705 Bennett Street" and "St. James Church 718 Franklin Avenue". Administrator Rev. Adam C. Potter; parish office 509 South Dallas Avenue, 412.661.7222. The bulletin carries the same pastoral staff and a Mass Schedule box for the whole parish.

Discover Mass has three church listings that all serve the issue (st-bede-pittsburgh-pa, st-mary-magdalene-pa, st-james-wilkinsburg-pa; same masthead and page count on 25 October). I record all three in `publication` and read the parish's `/bulletins` target, st-bede-pittsburgh-pa, as `provider_id`. The twelve issues listed there run 9 August to 25 October 2026.

## Worship sites

Two churches hold public Mass in the current schedule: St. Bede (Sunday 8:30 am from 18 October, formerly 9:00 am, and 11:00 am; Monday-Saturday 9:00 am) and St. James, Wilkinsburg (Saturday vigil 4:00 pm). Mother of Good Counsel is named in the masthead but has no Mass in any of the twelve listed issues (9 August - 25 October): see open/mother-of-good-counsel-brushton.md. Holy Rosary, Homewood (GCatholic 24278, the other building the old St. Charles Lwanga kept) is in no masthead or schedule: see excluded/holy-rosary-homewood.md. St. James also has a 'St. James Chapel' used for blood drives, small groups and a fair-trade sale (named in the events column); no Mass there is listed apart from the church.

## Website and bulletin provider

The parish site is diocese-provided eCatholic (site 21498) behind Cloudflare, readable in headed Chrome; it hosts no bulletin files and its Bulletins links go to Discover Mass. `fetch` reads Discover Mass by `provider_id`.

## Not yet confirmed

Whether Mother of Good Counsel hosts any occasional Mass (see its open record). Discover Mass keeps about twelve weeks of issues, so older ones can't be checked from it.
