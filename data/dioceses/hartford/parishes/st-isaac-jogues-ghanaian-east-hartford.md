---
name: St. Isaac Jogues Ghanaian Catholic Quasi Parish
website: https://ijghanaianparish.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://ijghanaianparish.org/
  seen: 2026-11-13
  quote: 1 Community St, East Hartford, CT 06108
  note: 'The quasi-parish''s own diocesanweb site, titled ''Isaac Jogues Ghanaian Parish – East Hartford,
    CT''; Mass Times: ''Sunday Mass … Sundays: 11:00 AM - 1:00 PM''. The site links no ParishesOnline
    org or other publisher.'
- url: https://ijghanaianparish.org/bulletins/
  seen: 2026-11-13
  quote: TWENTY-THIRD SUNDAY IN ORDINARY TIME • SEPTEMBER 06, 2026
  note: The Bulletins page holds only an HTML list of that Sunday's readings, with no PDF, no Mass schedule
    and no parish news.
- url: https://namct.org/st-isaac-jogues-church
  seen: 2026-11-13
  quote: On January 1, 2019, St. Isaac Jogues Church separated from the North American Martyrs Parish
    and became the St. Isaac Jogues Ghanaian Catholic Quasi Parish.
  note: The parish finder's link for the quasi-parish (directory 37) goes to this North American Martyrs
    history page.
- url: https://container.parishesonline.com/bulletins/03/1253/20261115B.pdf
  seen: 2026-11-13
  quote: 'East Hartford Mobile Food Truck: St. Isaac'
  note: The North American Martyrs bulletin of 15 November 2026 names St. Isaac Jogues only for a food-truck
    stop in its parking lot (page 6); its Mass schedule (page 1) has no Mass there, and grep finds no
    'Ghana' or 'Twi'.
revisit: Check https://ijghanaianparish.org/bulletins/ for a PDF or a ParishesOnline widget; it showed
  only an HTML readings sheet for 6 September 2026
revisit_after: 2027-03-01
research:
- method: probe url and probe get of the quasi-parish site and its /bulletins/ page; WordPress media API
    (401)
  url: https://ijghanaianparish.org/bulletins/
  checked: '2026-11-13'
  outcome: not-found
  next_action: Reread /bulletins/ for an uploaded PDF or a publicationWidget, and try probe po with a
    guessed org slug
  retry_when: The /bulletins/ page changes from the 6 September 2026 readings sheet, or after 2027-03-01
- method: probe po with guessed ParishesOnline org slugs (st-isaac-jogues-ghanaian-catholic-quasi-parish,
    st-isaac-jogues-ghanaian-catholic-community, st-isaac-jogues-06108)
  checked: '2026-11-13'
  outcome: not-found
  next_action: Look for an LPi or other publisher link on the quasi-parish site
  retry_when: The site links a publisher
- method: probe pdf grep of the North American Martyrs 15 November 2026 bulletin for Isaac, Ghana and
    Twi
  url: https://container.parishesonline.com/bulletins/03/1253/20261115B.pdf
  checked: '2026-11-13'
  outcome: not-found
  next_action: None needed unless the two communities rejoin
  retry_when: The North American Martyrs masthead names St. Isaac Jogues
bulletin_status: not-found
---

## Publisher

No bulletin was found. The St. Isaac Jogues Ghanaian Catholic Quasi Parish has its own site, ijghanaianparish.org (diocesanweb, titled "Isaac Jogues Ghanaian Parish", 1 Community St, East Hartford, phone 860-290-1880). On 2026-11-13 its Bulletins page held only an HTML list of the readings for 6 September 2026, with no PDF, no Mass schedule and no news. The site links no ParishesOnline or other publisher, and three guessed ParishesOnline slugs found no org.

It is not part of the North American Martyrs bulletin, despite the earlier lead. namct.org's St. Isaac Jogues page, which the parish finder links, is a history page: "On January 1, 2019, St. Isaac Jogues Church separated from the North American Martyrs Parish and became the St. Isaac Jogues Ghanaian Catholic Quasi Parish." Like every namct.org page, it links North American Martyrs' LPi org. The 15 November 2026 North American Martyrs bulletin has no Mass at St. Isaac Jogues and no Ghanaian or Twi Mass. It names the church only as a food-truck stop in the parking lot.

## Worship sites

St. Isaac Jogues Church, 1 Community St (`st-isaac-jogues-east-hartford`), with Sunday Mass at 11:00 AM according to the quasi-parish's site and Sunday 11:00 Twi according to the parish finder (37). This is GCatholic's 22063 "St. Isaac Jogues" (73 Cannon Rd). GCatholic's Plus Code and the finder's pin for 1 Community St are about 10 m apart, so they are the same building: the history page describes the church built on Laurel Park Heights beside the Cannon Road community building.

## Website and bulletin provider

`no_bulletin`. Under Settled policy 4 the row and its church stay in the records and off the site. The website is the quasi-parish's own site, where a bulletin would appear.

## Not yet confirmed

Whether the quasi-parish publishes a bulletin anywhere, for example a printed sheet or a WhatsApp group. See `research` and `revisit`.
