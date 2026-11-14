---
name: Our Lady of Fatima Parish
website: https://olfatimahartfordct.org/bulletins/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:our-lady-of-fatima-church-06106', 'lpi:0018000000Qx9T6AAJ']
group: ''
evidence:
- url: https://olfatimahartfordct.org/mass-times/
  seen: 2026-11-13
  quote: For the most current schedule, please check our weekly bulletin
  note: 'The parish''s diocesanweb site (50 Kane Street, Hartford): Saturday 5:00 PM Portuguese (Fall/Winter),
    6:00 PM (Spring/Summer); Sunday 8:00 AM and 9:30 AM Portuguese, 11:45 AM English, 6:00 PM Brazilian
    Community; Monday, Tuesday, Thursday 6:00 PM Portuguese; Friday 7:00 PM Brazilian Community.'
- url: https://olfatimahartfordct.org/bulletins/
  seen: 2026-11-13
  note: 'The Bulletins page has a heading and no content: no PDF, widget or iframe, in probe get or in
    the browser.'
- url: https://parishesonline.com/organization/our-lady-of-fatima-church-06106
  seen: 2026-11-13
  note: 'probe po: org ''Our Lady of Fatima Church'', 50 Kane St - Fatima Square, Hartford 06106, website
    ourladyoffatimachurch.org, LPi id 0018000000Qx9T6AAJ; no publications.'
revisit: Check olfatimahartfordct.org/bulletins/ and the ParishesOnline org our-lady-of-fatima-church-06106
  for a posted bulletin; if one appears, set the provider and run fetch:check.
revisit_after: 2027-02-15
research:
- method: probe get and browser visit of the parish site's Bulletins page
  url: https://olfatimahartfordct.org/bulletins/
  checked: '2026-11-13'
  outcome: not-found
  next_action: Re-read the Bulletins page for uploaded PDFs or a widget
  retry_when: The page shows content, or after 2027-02-15
- method: probe po of the ParishesOnline org
  url: https://parishesonline.com/organization/our-lady-of-fatima-church-06106
  checked: '2026-11-13'
  outcome: not-found
  next_action: probe po our-lady-of-fatima-church-06106 again
  retry_when: The org lists a publication, or after 2027-02-15
- method: The directory's listed site, a Facebook group (facebook.com/groups/olfhartfordct)
  url: https://www.facebook.com/groups/olfhartfordct/
  checked: '2026-11-13'
  outcome: access-blocked
  next_action: Check whether the group posts the weekly bulletin, with a logged-in browser
  retry_when: A way to read Facebook groups is available
bulletin_status: not-found
---

## Publisher

No bulletin found. Our Lady of Fatima, the Portuguese parish at 50 Kane Street, has a diocesanweb site (olfatimahartfordct.org) whose Mass times page says "please check our weekly bulletin", but its Bulletins page is empty (no PDF, widget or iframe, in probe get or a browser, 2026-11-13). Its old ParishesOnline org (`our-lady-of-fatima-church-06106`, LPi id 0018000000Qx9T6AAJ) has no publications. The directory's only listed site is a Facebook group (facebook.com/groups/olfhartfordct), which can't be read without logging in. The ParishesOnline ids are kept so a later bulletin there is recognised.

## Worship sites

One: Our Lady of Fatima Church, 50 Kane St (`our-lady-of-fatima-hartford`). The site's schedule (Saturday 5:00 or 6:00 PM, Sunday 8:00, 9:30 and 11:45 AM and 6:00 PM, weekday evenings) names no other place. The directory (167) and GCatholic (22092) list this church only.

## Website and bulletin provider

`no_bulletin` (Settled policy 4: kept in the records, left off the site). The website is the parish's Bulletins page, where a bulletin would appear.

## Not yet confirmed

Whether the weekly bulletin the site mentions is posted anywhere readable (the Facebook group was not readable). See `research` and `revisit`.
