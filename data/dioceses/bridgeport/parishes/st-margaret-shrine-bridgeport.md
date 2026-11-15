---
name: St. Margaret's Shrine
website: https://stmargaretshrine.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:25246']
group: ''
evidence:
- url: https://stmargaretshrine.org/bulletins
  seen: 2026-11-12
  note: 'eCatholic Bulletins page (read with parish-site-access visit.py): the newest link is ''June 28,
    2026'' (https://files.ecatholic.com/25246/bulletins/20260628.pdf), then weekly issues back through
    spring 2026.'
- url: https://files.ecatholic.com/25246/bulletins/20260628.pdf
  seen: 2026-11-12
  quote: Fr. Jose Ignacio Ortigas, Rector
  note: 'Page 1 of the 28 June 2026 issue: Clergy & Office Staff; Mass Schedule Monday-Saturday 8:15 a.m.;
    Vigil Mass 4:00 p.m.; Sunday 8:00 a.m., 9:30 a.m. in Italian, 11:00 a.m. Names no other church.'
- url: https://stmargaretshrine.org/
  seen: 2026-11-12
  note: 'Home page (visit.py) Mass Schedule: Daily Mass Monday-Saturday 8:15 a.m.; Saturday Vigil 4:00
    p.m.; Sunday 8:00 a.m., 9:30 a.m. in Italian, 11:00 a.m.; St. Pio Mass last Friday of the month April
    to November 6:00 p.m.; footer 2523 Park Ave, Bridgeport, CT 06604. The only bulletin link is /bulletins.'
revisit: Check https://stmargaretshrine.org/bulletins and issues.py ecatholic ecatholic:25246 for an issue
  after 28 June 2026; if weekly issues resume, set bulletin_provider ecatholic and run fetch:check.
revisit_after: 2027-01-15
research:
- method: issues.py ecatholic ecatholic:25246 --weeks 20 (Sundays 2026-07-05 to 2026-11-15) and --weeks
    6 --day sat
  url: https://files.ecatholic.com/25246/bulletins/
  checked: '2026-11-12'
  outcome: not-found
  next_action: Re-run issues.py and re-read the /bulletins page's first links
  retry_when: By the revisit date, or when the site links an issue newer than 28 June 2026
- method: fetch:check with provider ecatholic
  url: https://stmargaretshrine.org/
  checked: '2026-11-12'
  outcome: not-found
  next_action: Run fetch:check again after setting provider ecatholic
  retry_when: A current issue appears on /bulletins
- method: probe po on guessed ParishesOnline slugs (st-margaret-shrine-06604, st-margarets-shrine-06604,
    st-margaret-of-antioch-shrine-06604)
  checked: '2026-11-12'
  outcome: not-found
  next_action: Search ParishesOnline by name in a browser
  retry_when: An LPi or ParishesOnline id appears on the site
bulletin_status: not-found
---

## Publisher

St. Margaret's Shrine, Bridgeport (rector Fr. Jose Ignacio Ortigas) posted a weekly bulletin on its eCatholic site (site id 25246) until 28 June 2026, and nothing since. The 28 June 2026 issue (`https://files.ecatholic.com/25246/bulletins/20260628.pdf`, read 2026-11-12) lists the shrine's clergy and Mass schedule and names no other church. The site's `/bulletins` page lists that issue first; the archive answers 403 (not posted) for every Sunday from 5 July to 15 November 2026 and for the last six Saturdays.

## Worship sites

- `st-margaret-shrine-bridgeport`: the shrine church at 2523 Park Avenue (directory:1337, GCatholic 22003), with Mass daily (home page, read 2026-11-12).

## Website and bulletin provider

`no_bulletin` for now: the bulletin has not been posted for 4½ months. `fetch:check` on 2026-11-12 with provider `ecatholic` picked the 28 June 2026 issue (age 137 days) and failed on freshness. The eCatholic id stays in `publication`; if weekly issues resume, set `bulletin_provider: ecatholic` (website `https://stmargaretshrine.org/`) and run fetch:check. The row stays in the records off the site (Settled policy 4).

## Not yet confirmed

Whether the shrine stopped publishing or posts its bulletin somewhere not linked from the site (its Facebook page was not read). See research; revisit after 2027-01-15.
