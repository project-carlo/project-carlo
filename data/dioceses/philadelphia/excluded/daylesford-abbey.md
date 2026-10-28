---
name: Daylesford Abbey
reason: no-bulletin
line1: 220 S. Valley Road
city: Paoli
state: PA
postal_code: '19301'
decided: 2026-10-28
roster: ['gcatholic:40344']
evidence:
- url: https://daylesford.org/the-abbey/mass-prayer-and-sacraments/
  seen: 2026-10-28
  quote: The Daylesford Abbey Church is open to the public but is not a parish church.
  note: 'Abbey page (updated 2026-02-27): Regular Schedule Eucharist Sunday 10:30 am and Saturday 9:00
    am, Monday thru Friday 8:30 am; Sunday Mass live-streamed at 10:30 am. Baptisms and marriages are
    not permitted.'
- url: https://daylesford.org/wp-json/wp/v2/bulletins/34705
  seen: 2026-10-28
  note: 'The abbey''s own newest Sunday bulletin, ''SUNDAY BULLETIN | MARCH 15, 2026'', posted 2026-03-16
    as four page images (page01-1-659x800.jpg ...). Page 1 (read) lists the Regular Schedule: Sunday Mass
    10:30 a.m., Saturday Mass 9:00 a.m., Morning Mass 8:30 a.m. Monday to Friday. The front-end post URL
    answers 404 and no later bulletin exists in the REST list (the three newest are 16 March, 3 March
    and 26 February 2026).'
- url: https://www.church-bulletin.org/bulletin/saint-norbert-catholic-community-paoli-pa-19301/2026-10-25.pdf
  seen: 2026-10-28
  note: St. Norbert's 25 October 2026 bulletin (page 1, rendered) lists St. Norbert's own Masses only
    and never names Daylesford Abbey Mass.
- url: https://gcatholic.org/churches/usa-03/40344
  seen: 2026-10-28
  note: GCatholic lists 'Daylesford Abbey', 220 S Valley Rd., Paoli 19301-1900, type Monastery, phone
    +1 (610) 647-2530, Plus Code 87G62GJ8+24; website daylesford.org.
parish: st-norbert-paoli
revisit: Check https://daylesford.org/sunday-bulletins/ (or the REST list /wp-json/wp/v2/bulletins) for
  a Sunday bulletin newer than 15 March 2026; if the abbey posts current issues, make a parish row reading
  it
revisit_after: 2027-01-15
research:
- method: Read daylesford.org (Chrome), its Mass, Prayer and Sacraments page, the Sunday Bulletins page
    and the WordPress REST list of bulletin posts
  url: https://daylesford.org/sunday-bulletins/
  checked: '2026-10-28'
  outcome: not-found
  next_action: Look again for a Sunday bulletin posted after 16 March 2026 at daylesford.org/sunday-bulletins/
  retry_when: The abbey posts a bulletin dated after 15 March 2026, or St. Norbert's bulletin starts listing
    abbey Masses
  revisit_after: 2027-01-15
---

## Why it is excluded

Daylesford Abbey (the Norbertine monastery, 220 S. Valley Rd., Paoli) holds public Mass: its page says "The Daylesford Abbey Church is open to the public but is not a parish church", with Sunday Mass at 10:30 am, Saturday 9:00 am and weekdays 8:30 am (read 2026-10-28). Under the diocese's settled rule for abbey churches it gets a church row only if a parish bulletin lists its public Mass, or a parish row if the abbey publishes a readable bulletin. Neither holds today: St. Norbert's 25 October 2026 bulletin lists no abbey Mass (the abbey's priests serve St. Norbert, but the parish schedule is its own), and the abbey's own Sunday bulletin, posted as page images, stops at 15 March 2026 (posted 16 March; nothing newer in the REST list on 2026-10-28), seven months old. So the place is open with public Mass but no current bulletin lists it: excluded `no-bulletin`, not `closed` or `no-public-mass`.

## What would change this

A current abbey bulletin (the page-image posts at daylesford.org/sunday-bulletins/ resume), or a parish bulletin listing the abbey's Masses. The abbey's schedule above is the Mass times to use if a row is created. The pastor's residence at the abbey (directory: 'In residence at Daylesford Abbey') does not make St. Norbert's bulletin an abbey bulletin.
