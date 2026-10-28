---
name: St. Joseph
website: https://www.sjfschurch.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:14048']
group: City Deanery
evidence:
- url: https://files.ecatholic.com/14048/bulletins/20261011.pdf
  seen: 2026-10-27
  quote: 1012 French Street
  note: 'Page 1 of the 11 October 2026 issue (4 pages): ''THE CRADLE OF AFRICAN AMERICAN CATHOLICISM IN
    DELAWARE'', 302-658-4535; Mass schedule ''Saturday Vigil — 5:00 pm  Sunday — 10:00 am  Tuesday thru
    Thursday — 12:10 pm''. Page 2 staff list ''Pastor: Vy. Rev. Glenn M. Evers, V.C.''. The bulletin names
    this parish alone.'
- url: https://www.sjfschurch.org/bulletins
  seen: 2026-10-27
  note: 'Browser load: the page embeds ecatholic:14048 and lists files.ecatholic.com/14048/bulletins/20261011.pdf,
    20261004, 20260927, 20260830 ... back to 20260607. The 18 and 25 October issues were not yet posted
    on 2026-10-27 (files answer 403).'
- url: https://www.stjosephfrenchst.org/
  seen: 2026-10-27
  note: 'The diocese map''s website. curl and Chrome both fail: certificate not valid for the host (ERR_CERT_COMMON_NAME_INVALID).
    The Wayback Machine copy of 2026-06-05 (web.archive.org/web/20260605215919/https://stjosephfrenchst.org/)
    shows the same eCatholic site, files.ecatholic.com/14048. The live site is www.sjfschurch.org, the
    address the bulletin prints.'
promoted: 2026-10-27
research:
- method: probe url and the Chrome browser on stjosephfrenchst.org and www.stjosephfrenchst.org (http
    and https)
  url: https://www.stjosephfrenchst.org/
  checked: '2026-10-27'
  outcome: access-blocked
  next_action: 'None needed: the bulletin is read through www.sjfschurch.org, the same eCatholic site
    14048. Ask the diocese to change its map website if the old domain stays broken.'
  retry_when: stjosephfrenchst.org serves a valid certificate
- method: fetch:check freshness and issues.py ecatholic 14048 (weeks back from 2026-11-01)
  url: https://www.sjfschurch.org/bulletins
  checked: '2026-10-27'
  outcome: not-found
  next_action: Rerun fetch:check after the weekend of 2026-11-01 and confirm a 2026-10-18 or newer issue
    appears
  retry_when: A newer file than 20261011 is posted
  revisit_after: 2026-11-10
---

## Publisher

St. Joseph (1012 N. French Street) publishes its own weekly bulletin on eCatholic, site 14048. The parish's current site, www.sjfschurch.org (the address its bulletin prints), embeds `ecatholic:14048` on its /bulletins page, which links the dated files `files.ecatholic.com/14048/bulletins/<YYYYMMDD>.pdf`. The 11 October 2026 issue's page 1 gives the parish alone: 1012 French Street, Mass Saturday 5:00 pm, Sunday 10:00 am, Tuesday-Thursday 12:10 pm, pastor Vy. Rev. Glenn M. Evers, V.C. It is separate from Downtown Catholic: a different pastor, office, bulletin publisher (eCatholic, not John Patrick) and site.

## Worship sites

One church, St. Joseph, 1012 N. French Street. The diocese map and GCatholic list the same building; the bulletin schedule matches the map (Sun 10:00; Tue, Wed, Thu 12:10; Sat 17:00).

## Website and bulletin provider

`ecatholic`, read from the eCatholic-hosted site `https://www.sjfschurch.org/`. The diocese map's `stjosephfrenchst.org` fails its TLS certificate (curl and Chrome); it is the same eCatholic site per the Wayback copy, but the working domain is sjfschurch.org. The website recorded here therefore differs from the directory's.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-joseph-wilmington` (2026-10-27): picked files.ecatholic.com/14048/bulletins/20261011.pdf; transport ok, document type PDF, freshness **stale** (16 days; the limit is 14). Identity unverified to the tool; the masthead read above settles it. The pick is the newest file the parish has posted, so stale reflects a late upload, not a wrong pick.

## Not yet confirmed

The 18 and 25 October issues were not posted on 2026-10-27; the 11 October issue is the newest (16 days old). If the next check shows nothing newer, the parish may be posting late or the bulletin may have moved.
