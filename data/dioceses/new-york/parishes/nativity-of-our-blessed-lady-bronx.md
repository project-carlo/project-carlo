---
name: Nativity of Our Blessed Lady, Bronx
website: https://nativityofourblessedladychurch.org/bulletins
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:32546']
group: Holy Rosary - Nativity of Our Blessed Lady, Bronx
evidence:
- url: https://files.ecatholic.com/32546/bulletins/20261025.pdf
  seen: 2026-10-31
  quote: Sunday, October 25, 2026
  note: Latest issue found (eCatholic site 32546). Page 1 lists that Sunday's 9:30am, 11:30am and 1:00pm
    Mass intentions and weekday 7:00AM intentions, and gives 'Zelle- 917-882-2411 (Nativity Church)'.
    Issues for 13, 20, 27 September and 4, 11, 18, 25 October 2026 all answer HTTP 200 at files.ecatholic.com/32546/bulletins/<yyyymmdd>.pdf;
    1 November not yet posted on 31 October.
- url: https://files.ecatholic.com/32546/bulletins/20261025.pdf
  seen: 2026-10-31
  quote: Nativity Parish Harvest 2026
  note: Page 3 of the 25 October 2026 issue; the bulletin is published by Nativity of Our Blessed Lady
    for its own church.
- url: https://nativityofourblessedladychurch.org/
  seen: 2026-10-08
  quote: 1531 East 233rd Street,
  note: 'Old-session T3 browser read: the home page pairs the church address with Sunday 9:30 AM, 11:30
    AM Spanish and 1:00 PM Igbo Masses.'
- url: https://files.ecatholic.com/14148/documents/2026/10/November%201%202026.pdf?t=1793278592000
  seen: 2026-10-31
  quote: 1510 Adee Avenue    1500 Arnow Avenue
  note: Holy Rosary's 1 November 2026 issue (ecatholic:14148) keeps 'Nativity of Our Blessed Lady' in
    its page-2 heading but gives only the Adee Avenue office and its own 7:00/8:15/9:45/11:30/1:15 schedule;
    it is a different bulletin.
promoted: 2026-11-09
research:
- method: probe get of dated eCatholic bulletin URLs files.ecatholic.com/32546/bulletins/<yyyymmdd>.pdf
  url: https://files.ecatholic.com/32546/bulletins/20261025.pdf
  checked: '2026-10-31'
  outcome: found
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check (ecatholic provider; probe url
    alone gets HTTP 403)
  url: https://nativityofourblessedladychurch.org/bulletins
  checked: '2026-10-31'
  outcome: found
- method: fetch:check re-run and probe get of files.ecatholic.com/32546/bulletins/20261101.pdf and 20261108.pdf
  url: https://nativityofourblessedladychurch.org/bulletins
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-run fetch:check; if the archive is still at 25 October, look for a notice of a publication
    pause before changing the provider
  retry_when: The next weekly upload, or by 2026-11-22
  revisit_after: 2026-11-22
- method: fetch:check on 2026-11-08 and 2026-11-09; the parish homepage read in Chrome (visit.py --links)
    for another bulletin link; web search of discovermass.com, parishesonline.com, church-bulletin.org
    and bonventure.net for the parish; Discover Mass nativity-of-our-blessed-lady-bronx-ny lists no bulletins
  url: https://nativityofourblessedladychurch.org/bulletins
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-run fetch:check; the parish's own archive lags (newest October 25, 2026 on 2026-11-09)
    and no other current channel was found. If it stays over two weeks behind, look again for a publisher
    listing (church-bulletin.org, ParishesOnline).
  retry_when: The archive posts an issue dated after October 25, 2026
  revisit_after: 2026-11-16
bulletin_status: available
publication_reviews:
- parish: holy-rosary-nativity-of-our-blessed-lady-bronx
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/32546/bulletins/20261025.pdf
    seen: 2026-10-31
    note: 'The 25 October 2026 issue is published by Nativity of Our Blessed Lady (eCatholic 32546): Nativity
      Church Zelle, Nativity intentions at 9:30am, 11:30am and 1:00pm.'
  - url: https://files.ecatholic.com/14148/documents/2026/10/November%201%202026.pdf?t=1793278592000
    seen: 2026-10-31
    note: The 1 November 2026 Holy Rosary masthead names Nativity only in its title and lists Holy Rosary's
      own Adee Avenue schedule; it is a bulletin for Holy Rosary (eCatholic 14148).
---

## Publisher

Nativity of Our Blessed Lady (1531 East 233rd Street) publishes its own weekly bulletin on eCatholic (site 32546), separate from Holy Rosary's (eCatholic 14148) although the two share a pastor and a canonical title (merged 2015 per GCatholic). The 25 October 2026 issue, read 31 October, lists that week's Nativity Mass intentions (Sunday 9:30am, 11:30am, 1:00pm; weekdays 7:00AM; Saturday 9:00AM) and the 'Nativity Church' Zelle account. Weekly issues 13 September to 25 October 2026 are all present at their dated eCatholic paths. The old session's 8 October read of the archive stopped at 6 September; the gap was archive-listing lag, not a stopped bulletin.

## Worship sites

One church, Nativity of Our Blessed Lady, 1531 E 233rd St. Holy Rosary's bulletin (1 November 2026) keeps Nativity in its title but schedules only Holy Rosary on Adee Avenue, so Nativity is not one of its churches.

## Website and bulletin provider

eCatholic: nativityofourblessedladychurch.org/bulletins is the eCatholic bulletin archive. It returns HTTP 403 to `probe url`, but the 31 October headed-Chrome fetch check read it and picked the 25 October 2026 issue (files.ecatholic.com/32546/bulletins/20261025.pdf), the latest posted. Its 'conflict' date verdict comes only from the weekday intention dates inside the issue.

## Not yet confirmed

The bulletin's first-page masthead is an image; parish identity rests on the Nativity-specific intentions, Mass times and Zelle line, plus the site that hosts it.

On 8 November 2026 the newest issue was still 25 October: fetch:check picked it again and the 1 and 8 November files answered 403 (missing). Every Sunday from 19 July to 25 October 2026 had an issue, and the old session saw the archive lag a month behind the files, so this reads as upload lag, not a stopped bulletin. See `research` for the retry.
