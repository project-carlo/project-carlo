---
name: Church of Our Lady of Pompei / St. Peter
website: https://ourladyofpompei-stpeters.org
bulletin_provider: other
provider_id: ''
publication: ['url:https://ourladyofpompei-stpeters.org/publications']
group: 'Fr. Foley: OL Pompei/St. Peter + St. John the Baptist/Holy Trinity'
evidence:
- url: https://img1.wsimg.com/blobby/go/16b567ff-1ad1-4630-9f8d-2f2167ffce01/downloads/0036063a-c4b4-4ff4-b536-f3897989c6bc/Bulletin%20September%2013%2C%202026%20(1).pdf?ver=1789490491544
  seen: 2026-09-26
  quote: Church of Our Lady of Pompei / St. Peter Weekly Mass Schedule
  note: Page 1 of the 13 September 2026 issue, the newest linked on the parish's Publications page on
    2026-09-26. Saturday 4 pm vigil, Sunday 7:30 and 11:30 am, Vietnamese Masses daily and Sunday 9 am.
- url: https://ourladyofpompei-stpeters.org/
  seen: 2026-09-26
  quote: Sunday 9:00 am at St. John the Baptist / Holy Trinity
  note: Homepage weekly Mass schedule, which lists the sister parish's one Mass alongside its own ("Saturday
    4:00 pm at Our Lady of Pompei /St. Peter" ...).
- url: https://ourladyofpompei-stpeters.org/publications
  seen: 2026-09-26
  note: 'The Publications page (GoDaddy site) links weekly PDFs: "Bulletin September 13, 2026", "September
    6", "August 30". Fetched with curl; the host answered 502 through the proxy on about half the tries.'
---

## Publisher

Our Lady of Pompei / St. Peter publishes its own bulletin, posted on its Publications page.
The newest on 2026-09-26 was the 13 September 2026 issue: page 1 is the parish's own
(Father Brendan Foley, administrator; Rev. John Nguyen, chaplain to the Vietnamese
community; office at 920 North McBride Street) with Saturday 4 pm and Sunday 7:30 and 11:30
am Masses and Vietnamese Masses. Fr. Foley is also pastor of St. John the Baptist / Holy
Trinity, and the homepage schedule lists that parish's Sunday 9 am Mass too, but St. John
the Baptist / Holy Trinity publishes its own bulletin on its own site (27 September 2026
issue read), so the two are separate rows in one `group`.

## Worship sites

One: the church at 301 Ash Street (`our-lady-of-pompei-st-peter-syracuse`). The former St.
Peter's (Italian) church, merged in 2008, is `excluded/st-peter-syracuse.md`.

## Website and bulletin provider

ourladyofpompei-stpeters.org (GoDaddy website builder) links the PDFs from its
/publications page, so provider `other`. The host is unreliable from here: `probe url` and
visit.py got HTTP 502 through the proxy, and curl got the pages on retry.

## Not yet confirmed

Nothing, beyond the site's flakiness.
