---
name: Divine Mercy
website: https://archphila.org/parish/divine-mercy-philadelphia/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://archphila.org/parish/divine-mercy-philadelphia/
  seen: 2026-10-28
  quote: 9 AM at worship site, 7200 Grovers Ave.
  note: 'Directory page (updated 2 weeks ago; no website listed): 67th Street and Chester Ave., rectory
    6667 Chester Avenue 19142; Rev. Quan M. Trinh; Vigil Saturday 4 PM; Sunday 8:30 (Vietnamese), 11 AM;
    9 AM at worship site, 7200 Grovers Ave.; Holydays 9 AM (worship site), 7 PM (parish church); weekdays
    Monday through Saturday 8 AM; First Fridays 7 PM. ''Worship Site: St. Irenaeus''.'
- url: http://divinemercyrc.com/
  seen: 2026-10-29
  note: 'The website Discover Mass and the ParishesOnline organization give for the parish: probe url
    redirects to a casino-spam page (verdict SPAM-SQUAT), so the domain has lapsed to a squatter.'
- url: https://www.facebook.com/p/Divine-Mercy-Parish-at-Southwest-Philadelphia-61575253469567/
  seen: 2026-10-29
  quote: Divine Mercy Parish is the Catholic Church in Southwest Philadelphia. Originally Good Shepherd
    Catholic Church.
  note: 'Facebook page (visit.py): 6667 Chester Avenue, (215) 727-8300, Rev. Quan M. Trinh and Deacon
    Diep T. Nguyen; one event ''Divine Mercy Sunday'', Sun Apr 12, at ''72nd Grover Avenue, Philadelphia,
    PA. 19153''. No bulletin posted.'
- url: https://catholicmasstime.org/church/divine-mercy/14403/
  seen: 2026-10-29
  note: 'Aggregator text: Sunday Masses 4:00 PM Saturday vigil at 6667 Chester Avenue (English); 8:30
    AM at 72nd & Grovers Avenue (Vietnamese); 10:30 AM at 72nd & Grover Avenue (English); Holyday Masses
    9:00 AM and 7:00 PM at 72nd & Grovers Avenue; First Fridays 7:00 PM Vietnamese Masses at 7200 Grovers
    Avenue. Its times differ from the directory''s (Sunday 11 AM and 9 AM): the page is older, and aggregators
    are weak evidence.'
revisit: Find a Divine Mercy bulletin or current website (it has no John Patrick listing and an empty
  ParishesOnline organization) and read the Sunday Mass times for the 6667 Chester Ave. and 7200 Grovers
  Ave. churches.
revisit_after: 2027-01-15
research:
- method: John Patrick listing scan (ids 1-1300, no Divine Mercy or Good Shepherd listing in 19142), ParishesOnline
    search near 6667 Chester Ave. (organizations divine-mercy-parish-19142 and good-shepherd-church-19142,
    both without publications), Discover Mass church page (Bulletins tab empty)
  url: https://parishesonline.com/organization/divine-mercy-parish-19142
  checked: '2026-10-29'
  outcome: not-found
  next_action: None until a bulletin host is named
  retry_when: The directory, the Facebook page or a new website links a bulletin publisher
- method: probe url on divinemercyrc.com (the website both organization pages give)
  url: http://divinemercyrc.com/
  checked: '2026-10-29'
  outcome: access-blocked
  next_action: 'None: the domain is a spam squat, so it holds nothing to read'
  retry_when: The parish names a new website
- method: visit.py on the parish's Facebook page and web searches for a parish site or bulletin
  url: https://www.facebook.com/p/Divine-Mercy-Parish-at-Southwest-Philadelphia-61575253469567/
  checked: '2026-10-29'
  outcome: not-found
  next_action: Read the Facebook page's posts when it can be read in full; none showed a bulletin
  retry_when: A bulletin or schedule is posted there
bulletin_status: not-found
---

## Publisher

Divine Mercy (6667 Chester Ave., Southwest Philadelphia; the former Good Shepherd parish, merged in 2004) has no website of its own: the directory lists none, and divinemercyrc.com, which Discover Mass and the ParishesOnline organization give, is a casino-spam squat. It has no John Patrick listing and no bulletin on ParishesOnline or Discover Mass. No bulletin was found, so the row is `no_bulletin` (kept in the records, left off the site) and the `website` is the directory page, the one stable page that states its Mass times.

## Worship sites

Two, both from the directory (updated two weeks before 2026-10-28) and the parish's Facebook page: the parish church at 6667 Chester Ave. (Saturday 4 PM, Sunday 11 AM, holyday 7 PM) and the St. Irenaeus worship site at 7200 Grovers Ave. (Sunday 9 AM, holyday 9 AM). The Facebook page lists a Divine Mercy Sunday event at 72nd and Grover Avenue in April 2026, which shows the building in use. No bulletin Mass box confirms them, so the St. Irenaeus church row is kept with `address_verified` false.

## Not yet confirmed

The Sunday times: the directory (11 AM at the church, 9 AM at St. Irenaeus) and Discover Mass (8:30 Vietnamese, 11 AM) and catholicmasstime (8:30 Vietnamese and 10:30 English at Grovers Ave.) disagree. A bulletin would settle them.
