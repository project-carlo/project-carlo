---
name: Schoenstatt Shrine of Light
revisit: Re-read https://schoenstattnewyork.org/en/ (Upcoming Events and Calendar) and its Newsletters
  page for a dated 2026-2027 Mass at the shrine with a time, and search schoenstatt.org / schoenstatt.com
  news for a dated Staten Island shrine Mass. A dated public Mass with nothing readable for the shrine
  makes it excluded/no-bulletin; a dated statement that it closed makes it excluded/closed.
revisit_after: 2027-02-01
roster: ['gcatholic:149071']
evidence:
- url: https://schoenstattnewyork.org/en/
  seen: 2026-10-08
  quote: Monthly Covenant Day Mass
  note: 'Direct verified HTTP read: header gives 337 Cary Avenue and 718-727-8005; July 18 card says all
    are welcome. Cards lack a year and Mass time, so they do not establish an October 2026 celebration.
    This read returned shrine content rather than the casino material previously observed.'
- url: https://schoenstattnewyork.org/en/calendar/
  seen: 2026-10-08
  quote: Calendar
  note: Direct HTTP 200 page has header/navigation/footer only; no dated event or public Mass timetable
    appears in the returned document. This is a missing primary fact, not closure evidence.
- url: https://schoenstattnewyork.org/en/newsletters/
  seen: 2026-10-08
  quote: Showing 4 Available Publications
  note: Direct archive read lists July, June and May 2021 English bulletins and May 2021 Spanish; no current
    issue listed. A library of old issues cannot prove no present publication exists.
- url: https://gcatholic.org/churches/usa-02/149071
  seen: 2026-10-06
  quote: 337 Cary Ave., Staten Island, New York 10310
  note: 'Listed in GCatholic: churches of the Archdiocese of New York as ''Mary Mother Thrice Admirable,
    Queen and Victress of Schoenstatt'', 337 Cary Ave., Staten Island, NY, 10310; kind: Shrine'
- url: https://schoenstattnewyork.org/en/
  seen: 2026-11-09
  quote: Monthly Covenant Day Mass
  note: 'Homepage re-read: the Upcoming Events cards are still Jul 18 (Monthly Covenant Day Mass, all
    welcome), Aug 15 and Sep 8, with no year and no time, so they don''t date a current Mass. Phone (718)
    727-8005.'
- url: https://schoenstattnewyork.org/en/newsletters/
  seen: 2026-11-09
  quote: Showing 4 Available Publications
  note: Archive still ends at the July 2021 Shrine Bulletin.
line1: 337 Cary Ave.
city: Staten Island
state: NY
postal_code: '10310'
research:
- method: Shrine website homepage, Calendar and Newsletters pages re-read with probe get; web search for
    a dated 2026 Covenant Day Mass at the Staten Island shrine
  url: https://schoenstattnewyork.org/en/
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-read the Upcoming Events, Calendar and Newsletters pages and search Schoenstatt movement
    news for a dated Staten Island shrine Mass
  retry_when: The shrine site's events change from the undated Jul 18 / Aug 15 / Sep 8 cards, a newsletter
    after July 2021 appears, or a dated notice is found elsewhere
  revisit_after: 2027-02-01
---

## What is known

The Schoenstatt Shrine (GCatholic: Mary Mother Thrice Admirable, Queen and Victress of Schoenstatt), 337 Cary Avenue, is run by the Schoenstatt Sisters of Mary. Its website (re-read 9 November 2026) advertises a "Monthly Covenant Day Mass" that "all are welcome to attend", but the event cards (Jul 18, Aug 15, Sep 8) carry no year or time and have not changed since 8 October; the Calendar page has no events; the newsletter archive ends in July 2021. A web search found no dated 2026 Mass at this shrine. It has never been a parish bulletin publisher.

## Why it is not decided

No dated source shows a public Mass there now, and none says Mass ended or the shrine closed. An undated, unchanging events list can't establish either. If a dated public Mass is found, the shrine becomes `excluded/` `no-bulletin` (public Mass, nothing the pipeline can read); a dated closure makes it `excluded/` `closed`. See `research` for the checks made and the retry trigger.
