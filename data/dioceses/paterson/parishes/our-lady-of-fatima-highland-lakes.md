---
name: Our Lady of Fatima
website: https://olfatimaparish.net/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:25267']
group: ''
evidence:
- url: https://olfatimaparish.net/bulletins
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403). eCatholic site 25267 (the id of finder
    pin directory:25267); /bulletins lists files.ecatholic.com/25267/bulletins/<YYYYMMDD>.pdf weekly,
    newest 'October 25, 2026' (20261025.pdf), then October 18, 11, 4, September 27 ...
- url: https://files.ecatholic.com/25267/bulletins/20261025.pdf
  seen: 2026-11-04
  quote: 184 Breakneck Road, Highland Lakes, NJ 07422
  note: 'Page 1 of the 25 October 2026 issue (6 pages): ''Our Lady of Fatima RC Church'', ''October 25,
    2026 - 30th Sunday in Ordinary Time'', ''Fr. Babu Thelappilly Pastor''; Mass Schedule Saturday 4:00
    pm, Sunday 8:00, 10:00 am, 12:00 noon; weekday Monday-Thursday 9:00 am; ''Msza Po Polsku - 1st Niedziels
    Miesiaca at 2:00 pm''. Last page has a Bon Venture ad footer ''014E (JA) - OL of Fatima, Highland
    Lakes''.'
- url: https://files.ecatholic.com/25267/bulletins/20261101.pdf
  seen: 2026-11-04
  note: 'issues.py ecatholic ecatholic:25267 --weeks 3: 20261108.pdf and 20261101.pdf answer 403 (not
    posted); 20261025.pdf is 200.'
revisit: The 1 November 2026 issue was not posted by 4 November; confirm weekly posting continues (issues.py
  ecatholic ecatholic:25267).
revisit_after: 2026-11-09
research:
- method: visit.py on /bulletins and issues.py ecatholic ecatholic:25267 --weeks 3
  url: https://olfatimaparish.net/bulletins
  checked: '2026-11-04'
  outcome: not-found
  next_action: Re-run issues.py ecatholic ecatholic:25267 and fetch:check; confirm the newest issue is
    within two weeks
  retry_when: After Sunday 8 November 2026
  revisit_after: 2026-11-09
bulletin_status: available
---

## Publisher

Our Lady of Fatima, Highland Lakes publishes its own weekly bulletin (printed by Bon Venture, whose ad footer "014E (JA) - OL of Fatima, Highland Lakes" is on the last page) and posts it to its eCatholic site's `bulletins/` archive (site id 25267). The newest on 4 November 2026, the 25 October 2026 issue (`https://files.ecatholic.com/25267/bulletins/20261025.pdf`, 6 pages), has on page 1 "Our Lady of Fatima RC Church", "184 Breakneck Road, Highland Lakes, NJ 07422", "October 25, 2026 - 30th Sunday in Ordinary Time" and Fr. Babu Thelappilly, Pastor.

## Worship sites

- `our-lady-of-fatima-highland-lakes`: the only church. Page 1's Mass Schedule (25 October 2026) gives Saturday 4:00 pm, Sunday 8:00, 10:00 am, 12:00 noon, weekday Monday-Thursday 9:00 am, and a Polish Mass on the first Sunday at 2:00 pm, and names no other place.

The finder has two pins for this parish: directory:25267 (no address, website olfatimaparish.net, the eCatholic site id, with the current times) and directory:5707 (P.O. Box 242, Highland Lakes 07422, website www.olfatimaparish.net, an old schedule of 5 p.m. and 8, 9:30, 11 a.m.). GCatholic lists one church (19031). All three are this one church.

## Website and bulletin provider

`olfatimaparish.net` is eCatholic site 25267 behind Cloudflare (read with visit.py on 2026-11-04); `/bulletins` lists the `bulletins/<YYYYMMDD>.pdf` archive newest first, so provider is `ecatholic`, not Bon Venture. fetch:check on 2026-11-04 picked `20261025.pdf`, the newest posted issue.

## Not yet confirmed

The 1 November and 8 November 2026 files were not posted by 4 November (403 from files.ecatholic.com); the archive is otherwise weekly back to August. Re-check after 8 November that posting continues (see `research`).
