---
name: St. Francis Chapel
revisit: Grep the June-August 2027 St. John XXIII bulletins (container 03/1158) for St. Francis Chapel
  or Crescent Beach, and ask the parish office (860-739-9722) whether summer Masses are held there; a
  church record if they are, excluded closed if a source says they ended.
revisit_after: 2027-07-15
roster: ['directory:st-francis-chapel-niantic', 'gcatholic:22271', 'locator-map:saint-francis-chapel-crescent-beach-niantic']
evidence:
- url: https://www.norwichdiocese.org/Portals/dioceseofnorwich/CMAdmin/Parishes_CCD9Mar26.pdf
  seen: 2026-11-14
  note: 'Diocese of Norwich List of Parishes (March 6, 2026): ''St. Francis Chapel (Est. 1908), 2 Central
    Ave. cor. Crescent Ave., Crescent Beach. Mission of St. Agnes, Niantic. Summer Chapel-Seasonal'';
    no Mass times given.'
- url: https://gcatholic.org/churches/usa-01/22271
  seen: 2026-11-14
  note: 'GCatholic: ''St. Francis'', Central Ave., Niantic 06357; Plus Code 87H98Q8R+3W.'
- url: https://www.google.com/maps/d/viewer?mid=1VTpfhm6bXf8ZfwM_tX0Ikl--m9E8l7a5
  seen: 2026-11-14
  note: 'Diocese parish locator map: ''Saint Francis Chapel'', 2 Central Avenue, Crescent Beach, Niantic.'
- url: https://www.saintagnescatholicchurch.com/?page_id=2511
  seen: 2026-11-14
  quote: Rev. Francis P. Nolan dedicated St. Francis Chapel in the summer of 1908
  note: The parish site's St. Francis Chapel page is a history only; it gives no current Mass times, and
    the sidebar schedule lists only St. Agnes and St. Matthias.
- url: https://container.parishesonline.com/bulletins/03/1158/20260712B.pdf
  seen: 2026-11-14
  note: 'Grepped for ''St. Francis'' and ''Crescent'': no match. Nor in the 2025-07-06, 2025-08-03, 2026-05-31,
    2026-06-28, 2026-07-05, 2026-07-26, 2026-08-09 and 2026-08-30 issues; their page 1 schedules list
    only St. Agnes and St. Matthias.'
parish: st-john-xxiii-niantic
line1: 2 Central Ave.
city: Niantic
state: CT
postal_code: '06357'
research:
- method: probe pdf --grep 'Francis|Crescent|summer' on the newest St. John XXIII bulletin (container
    03/1158, November 15, 2026)
  url: https://container.parishesonline.com/bulletins/03/1158/20261115B.pdf
  checked: '2026-11-14'
  outcome: not-found
  next_action: Grep the June-August 2027 issues of container 03/1158 for St. Francis or Crescent, or call
    the parish office (860-739-9722)
  retry_when: Summer 2027 bulletins are published (from June 2027)
- method: probe get of the parish site's Masses page and its 'Mass Schedule for St. Agnes & St. Matthias'
    post; St. Francis Chapel appears only as a menu link to the history page
  url: https://www.saintagnescatholicchurch.com/?page_id=2350
  checked: '2026-11-14'
  outcome: not-found
  next_action: Re-read the Masses page for a summer schedule
  retry_when: June 2027, when a summer schedule would be posted
---

## What is known

The diocese's List of Parishes (March 6, 2026) lists St. Francis Chapel, 2 Central Ave. at Crescent Ave., Crescent Beach, as "Mission of St. Agnes, Niantic. Summer Chapel-Seasonal"; GCatholic and the locator map list it too. The parish site's St. Francis Chapel page tells its history (dedicated 1908, summer Masses for the Crescent Beach summer residents) but gives no current schedule.

## Why it is not decided

No source read shows a Mass there now and none says the summer Masses ended. Nine summer issues of the St. John XXIII bulletin (container 03/1158: 2025-07-06, 2025-08-03, 2026-05-31, 2026-06-28, 2026-07-05, 2026-07-12, 2026-07-26, 2026-08-09, 2026-08-30) never mention St. Francis or Crescent; each page 1 schedule lists only St. Agnes and St. Matthias. That is absence only, so it is not excluded. The summer 2027 bulletins or the parish office would settle it.
