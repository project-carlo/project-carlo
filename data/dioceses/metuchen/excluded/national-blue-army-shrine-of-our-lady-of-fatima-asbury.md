---
name: National Blue Army Shrine of Our Lady of Fatima
reason: no-bulletin
line1: 674 Mountain View Road East
city: Asbury
state: NJ
postal_code: 08802
decided: 2026-11-03
roster: ['gcatholic:32367']
evidence:
- url: https://bluearmyshrine.com/
  seen: 2026-11-03
  quote: 12pm NOON daily, including weekends
  note: 'Home page of the World Apostolate of Fatima USA''s shrine: location ''674 Mountain View Rd E,
    Asbury NJ 08802''; Daily Schedule Holy Mass 12pm noon daily, Rosary and Confessions 11:30am; 13th-of-the-month
    celebrations May-October with 1:15pm Mass. Its only PDFs (visit.py --links) are the 2026 schedule
    and a 2026 song sheet.'
- url: https://bluearmyshrine.com/wp-content/uploads/2026/04/Bulletin-2026-download-file-1.pdf
  seen: 2026-11-03
  quote: 11:30 a.m. Rosary & Confessions, 12:00 Noon Mass
  note: 'Despite its file name, a 2-page annual mailer (bulk-mail postage block, ''PO BOX 976, WASHINGTON,
    NJ 07882''), uploaded April 2026: ''EVERY WEEK AT THE SHRINE'' and a list of special Sundays from
    April 5 (Easter) to September 27, 2026. No weekly or monthly issue is posted.'
- url: https://gcatholic.org/churches/usa-03/32367
  seen: 2026-10-30
  quote: 674 Mountain View Rd. E, Washington, New Jersey 08802
  note: GCatholic lists 'Our Lady of Fatima', kind National Blue Army Shrine, website http://wafusa.org/the-shrine/
    (HTTP 404 on 2026-11-03).
revisit: Check bluearmyshrine.com for a weekly or monthly bulletin; the 2026 schedule mailer is linked
  as 'Click to Download our 2026 Schedule'.
revisit_after: 2027-04-30
research:
- method: Shrine home page and its PDF links read with probe get and visit.py --links; DuckDuckGo search
    for the shrine's Mass schedule and bulletin
  url: https://bluearmyshrine.com/
  checked: '2026-11-03'
  outcome: not-found
  next_action: Look for a 2027 schedule or a periodic bulletin on bluearmyshrine.com
  retry_when: The shrine posts its 2027 schedule (spring 2027)
  revisit_after: 2027-04-30
---

## Why it is excluded

The shrine of the World Apostolate of Fatima USA (GCatholic 'Our Lady of Fatima', Washington Township) has public Mass, "12pm NOON daily, including weekends" (home page, read 2026-11-03), but no parish of its own and no bulletin. St. Joseph, Washington's 1 November 2026 masthead does not name it. Its only schedule document is a two-page 2026 mailer ("Bulletin-2026-download-file-1.pdf", uploaded April 2026) listing the standing daily schedule and special Sundays from 5 April to 27 September 2026; it is not a weekly or monthly issue and has no current content for the pipeline to read. Under the diocese's shrine rule (*Rules settled*: a shrine with public Mass, no parish and no bulletin is excluded `no-bulletin`), it is excluded `no-bulletin`.

Address: the shrine's site gives 674 Mountain View Rd E, Asbury NJ 08802 and GCatholic gives the same street as "Washington, New Jersey 08802" (08802 is the Asbury post office; the shrine is in Washington Township); the shrine's own form is recorded. Its mailing address is PO Box 976, Washington, NJ 07882.

## What would change this

A bulletin or a dated schedule the pipeline could read each week or month (a newsletter series on bluearmyshrine.com) would give it a parish row of its own. The 2027 mailer, if it is again only an annual events list, would not.
