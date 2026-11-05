---
name: Our Lady Queen of Peace
website: https://olqpbranchville.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:11413']
group: ''
evidence:
- url: https://files.ecatholic.com/11413/bulletins/20261011.pdf
  seen: 2026-11-04
  quote: A Country Parish with a Big Impact
  note: 'Page 1 of the 11 October 2026 issue (3 pages; its Mass intentions run to ''Sun. Oct. 18''): masthead
    ''Our Lady Queen of Peace'', ''Very Rev. Philip-Michael Tangorra ChM, S.T .L., J.C.L. Pastor''; Sunday
    Mass Schedule Saturday 5:00 PM, Sunday 8:00 AM, 10:00 AM, 12:00 PM Hispanic Ministry Mass, 7:00 PM;
    Daily Masses Monday-Saturday 8:00 AM; Traditional Latin Mass 5:00 PM First Friday, 6:30 PM Second
    & Fourth Mondays, 6:00 PM Third Friday. The bulletin is laid out by the parish (its own ad rates on
    page 3), not a publisher.'
- url: https://olqpbranchville.org/bulletins
  seen: 2026-11-04
  note: 'Read with visit.py (probe url answers 403). ''BULLETIN Archive 2026'' lists files.ecatholic.com/11413/bulletins/<YYYYMMDD>.pdf
    issues, newest ''October 11, 2026'', then October 4, September 27, September 13 (no 20 September),
    September 6 and back to January 4. No later issue: probe get of 20261018, 20261025, 20261101 and 20261108.pdf
    answered 403 (eCatholic''s answer for a missing file).'
- url: https://olqpbranchville.org/
  seen: 2026-11-04
  note: 'visit.py: verdict ok, title ''Our Lady Queen of Peace, Branchville - Branchville, NJ'', publication
    ecatholic:11413; no other bulletin link (no PDF, ParishesOnline or Bon Venture link on the home page).
    Mass Times: Saturday 5:00 PM; Sunday 8:00 AM, 10:00 AM, 12:00 PM Spanish, 7:00 PM; M Tu Th F 8:00
    AM; Wednesday 6:30 PM Spanish; 1st Friday 5:00 PM Latin; Saturday 8:00 PM Latin ''Every Saturday''.'
revisit: Check /bulletins for an issue newer than 11 October 2026; the parish posted none for 18 October-1
  November.
revisit_after: 2026-11-11
promoted: 2026-11-05
research:
- method: visit.py on /bulletins and probe get of the next four Sunday-dated eCatholic files
  url: https://olqpbranchville.org/bulletins
  checked: '2026-11-04'
  outcome: not-found
  next_action: Reload /bulletins with visit.py and run fetch:check; if an issue dated 18 October or later
    is listed, confirm its masthead and Mass times
  retry_when: On or after 2026-11-11, or when the parish posts a new issue (it skipped 20 September before,
    then resumed)
- method: Reconcile fetch:check (headed Chrome) and probe get of the Sunday-dated eCatholic files 18 October-8
    November (newest posted still 11 October, 25 days old (freshness stale); 18 October-8 November answer
    403; the 11 October issue is self-published, no printer footer)
  url: https://files.ecatholic.com/11413/bulletins/20261101.pdf
  checked: '2026-11-05'
  outcome: not-found
  next_action: Rerun fetch:check; if it still picks an issue older than two weeks, look for another place
    the parish posts its bulletin
  retry_when: On or after 2026-11-11, or when the parish posts the 1 November issue
bulletin_status: available
---

## Publisher

Our Lady Queen of Peace, Branchville lays out its own weekly bulletin and posts it on its eCatholic site (id 11413). The newest issue, 11 October 2026 (`https://files.ecatholic.com/11413/bulletins/20261011.pdf`, read 2026-11-04; 3 pages, intentions to Sunday 18 October), is headed "Our Lady Queen of Peace, A Country Parish with a Big Impact", with "Very Rev. Philip-Michael Tangorra ... Pastor", and names no other parish. Page 3 carries the parish's own advertising rates, so no publisher prints it.

## Worship sites

- `our-lady-queen-of-peace-branchville`: the 11 October page 1 gives Saturday 5:00 PM; Sunday 8:00 AM, 10:00 AM, 12:00 PM (Hispanic Ministry) and 7:00 PM; Monday-Saturday 8:00 AM; Traditional Latin Mass at 5:00 PM First Friday, 6:30 PM Second & Fourth Mondays and 6:00 PM Third Friday. The site's Mass Times box (read 2026-11-04) differs on weekdays (M Tu Th F 8:00 AM, Wednesday 6:30 PM Spanish, Saturday 8:00 PM Latin); both are at the one church.

The issue names no other place of Mass. The Sanctuary of Mary, Our Lady of the Holy Spirit, 252 Wantage Ave., Branchville (GCatholic 37948) is not in it; it has its own record (`excluded/sanctuary-of-mary-branchville`, open with daily Mass but no bulletin). The finder (directory:11413) and GCatholic (19034) list this one church.

## Website and bulletin provider

`olqpbranchville.org` is the eCatholic site (id 11413, finder pin 11413) behind Cloudflare: probe url gets 403 and visit.py loads it. Its `/bulletins` page lists `files.ecatholic.com/11413/bulletins/<YYYYMMDD>.pdf` issues; provider `ecatholic`. `fetch:check` on 2026-11-04 picked `https://files.ecatholic.com/11413/bulletins/20261011.pdf`, the newest posted file, and reports it stale (24 days; overall failed) and identity unverified (as for every eCatholic row). The pick is the right file for what the parish has posted; the staleness is the parish not posting, not a fetch problem, so no fetch_gap is recorded.

## Not yet confirmed

Whether the parish still posts every week: on 4 November 2026 the newest issue was 11 October (the files for 18 October-8 November answer 403), and it skipped 20 September earlier in the year. See `research`; recheck from 11 November.
