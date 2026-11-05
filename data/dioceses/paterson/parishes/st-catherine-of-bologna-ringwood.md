---
name: St. Catherine of Bologna
website: https://stcatherineofbologna.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:33389']
group: ''
evidence:
- url: https://files.ecatholic.com/33389/bulletins/20261025.pdf
  seen: 2026-11-04
  quote: '112 Erskine Rd, Ringwood, NJ 07456, Phone: (973) 962-7032'
  note: 'Page 1 of the 25 October 2026 issue (7 pages): ''ST. CATHERINE OF BOLOGNA'', ''Rev. Pawel Szurek-
    Pastor'', ''OCTOBER 25,2026 30TH SUNDAY IN ORDINARY TIME''. MASS SCHEDULE: Monday-Saturday 9:00am;
    Saturday Vigil 5:00pm; Sunday 7:30am, 9:00am, 11:00am, 6:00pm.'
- url: https://stcatherineofbologna.org/bulletins
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403). eCatholic site 33389; lists files.ecatholic.com/33389/bulletins/<YYYYMMDD>.pdf,
    newest 20261025.pdf, then 20261018, 20261011 ... weekly back to 20260726.
- url: https://scobp.org/
  seen: 2026-11-04
  note: 'visit.py: the finder''s second website (directory:6362) loads the same eCatholic site, title
    ''St. Catherine of Bologna - Ringwood, NJ'', publication ecatholic:33389, bulletin link https://scobp.org/bulletins.
    One site under two domains.'
- url: https://files.ecatholic.com/33389/bulletins/20261101.pdf
  seen: 2026-11-04
  note: 'issues.py ecatholic ecatholic:33389 --weeks 3: 20261108.pdf and 20261101.pdf answer 403 (not
    posted); 20261025.pdf is 200.'
revisit: The 1 November 2026 issue was not posted by 4 November; confirm the parish keeps posting weekly
  (issues.py ecatholic ecatholic:33389).
revisit_after: 2026-11-09
research:
- method: visit.py on /bulletins and issues.py ecatholic ecatholic:33389 --weeks 3
  url: https://stcatherineofbologna.org/bulletins
  checked: '2026-11-04'
  outcome: not-found
  next_action: Re-run issues.py ecatholic ecatholic:33389 and fetch:check; confirm the newest issue is
    within two weeks
  retry_when: After Sunday 8 November 2026
  revisit_after: 2026-11-09
- method: Reconcile fetch:check (headed Chrome) and probe get of the Sunday-dated eCatholic files 18 October-8
    November (newest posted 25 October; 31 October, 1 and 8 November answer 403)
  url: https://files.ecatholic.com/33389/bulletins/20261101.pdf
  checked: '2026-11-05'
  outcome: not-found
  next_action: Rerun fetch:check; if it still picks an issue older than two weeks, look for another place
    the parish posts its bulletin
  retry_when: On or after 2026-11-09, or when the parish posts the 1 November issue
bulletin_status: available
---

## Publisher

St. Catherine of Bologna, Ringwood publishes its own weekly bulletin and posts it to its eCatholic site's `bulletins/` archive (site id 33389). The newest on 4 November 2026, the 25 October 2026 issue (`https://files.ecatholic.com/33389/bulletins/20261025.pdf`, 7 pages), has on page 1 "ST. CATHERINE OF BOLOGNA", "Rev. Pawel Szurek- Pastor", "OCTOBER 25,2026 30TH SUNDAY IN ORDINARY TIME" and the footer "112 Erskine Rd, Ringwood, NJ 07456, Phone: (973) 962-7032". No printer's footer (LPi, Bon Venture) was found in it.

## Worship sites

- `st-catherine-of-bologna-ringwood`: the only church. Page 1's MASS SCHEDULE gives Monday-Saturday 9:00am; Saturday Vigil 5:00pm; Sunday 7:30am, 9:00am, 11:00am, 6:00pm, and names no other place.

The finder has two pins for this parish: directory:6362 (112 Erskine Road, website scobp.org) and directory:33389 (no address, website stcatherineofbologna.org, the eCatholic site id). GCatholic lists one church (18984). All three are this one church.

## Website and bulletin provider

Both `scobp.org` and `stcatherineofbologna.org` load the same eCatholic site (id 33389, behind Cloudflare; read with visit.py on 2026-11-04); the row uses `stcatherineofbologna.org`, the domain the bulletin prints. The `/bulletins` page lists the `bulletins/<YYYYMMDD>.pdf` archive, newest first, so provider is `ecatholic`. `fetch:check` on 2026-11-04 picked `20261025.pdf`, the newest posted issue (freshness fresh, age 10 days; identity unverified because no expected identity is supplied).

## Not yet confirmed

The 1 November and 8 November 2026 files were not posted by 4 November (403 from files.ecatholic.com); the parish has posted in batches before (the 20 September to 18 October files carry upload stamps from the same day). Re-check after 8 November that weekly posting continues (see `research`).
