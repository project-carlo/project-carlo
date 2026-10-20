---
name: Saint Joseph Parish
website: https://www.stjosephmech.org/
bulletin_provider: discover_mass
provider_id: st-joseph-mechanicsburg-pa
publication: ['discovermass:st-joseph-mechanicsburg-pa']
group: ''
evidence:
- url: https://discovermass.com/church/st-joseph-mechanicsburg-pa/
  seen: 2026-10-19
  quote: 400 East SimpsonS t| Mechanicsburg
  note: 'Issue of 18 October 2026 (12 pages), page 1 (the text layer splits words): "Saint Joseph School,
    420 East Simpson St ... Church, 400 East Simpson St | Mechanicsburg, www.stjosephmech.org, Parish
    Office, 410 East Simpson St"; "October 18, 2026, Twenty-Ninth Sunday in Ordinary Time".'
- url: https://discovermass.com/church/st-joseph-mechanicsburg-pa/
  seen: 2026-10-19
  quote: 8:00 AM Mass -P eopleo ft he Parish
  note: 'Issue of 18 October 2026, page 2: Saturday 17 October 4:00 PM Mass; Sunday 18 October 8:00 AM,
    9:45 AM and 11:30 AM Masses; pastor Very Reverend John B. Bateman, J.C.L., V.F.'
- url: https://discovermass.com/church/st-joseph-mechanicsburg-pa/
  seen: 2026-10-19
  quote: Saint Joseph, Mechanicsburg - Mass at 8:30 AM Monday, Wednesday, Thursday
  note: Issue of 18 October 2026, the deanery's weekday Mass list for the priests' continuing-education
    week; it also lists Good Shepherd, Saint Patrick (Shrine and Marsh Drive churches), Saint Katharine
    Drexel and Saint Theresa.
- url: https://www.stjosephmech.org/
  seen: 2026-10-19
  note: Behind Cloudflare (probe url 403; parish-site-access visit.py BLOCKED on every load). The bulletin
    was read on Discover Mass.
promoted: 2026-10-20
---

## Publisher

Saint Joseph, Mechanicsburg (church 400 East Simpson Street, office 410, school 420)
publishes its own weekly bulletin through Diocesan (Discover Mass). The 18 October 2026 issue
(12 pages) names Saint Joseph alone, Very Rev. John B. Bateman, pastor, with Saturday 4:00 PM
and Sunday 8:00, 9:45 and 11:30 AM Masses.

## Worship sites

- Saint Joseph, Mechanicsburg (`st-joseph-mechanicsburg`). The bulletin has a "Saint Pio
  Shrine" offering line and a pie sale for "the lighting at the Padre Pio Chapel and the
  statues of Saint Joseph and the Blessed Mother", which reads as an outdoor devotional
  shrine on the parish grounds (inferred, not checked); no Mass is listed there. The diocese's page notes the 9:45AM Sunday Mass is interpreted in
  American Sign Language (the parish has a Deaf ministry); it is in the church.

## Website and bulletin provider

stjosephmech.org is behind Cloudflare and never loaded in the sandbox. Discover Mass's
church page `st-joseph-mechanicsburg-pa` (found with its search for "mechanicsburg") lists
weekly issues through 18 October 2026 whose masthead is this parish's. Provider
`discover_mass` with that slug.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows): the resolver found the newest issue on the Discover Mass church page, but the download returned Discover Mass's 134-byte "Maximum number of files downloaded today" page (a per-IP daily cap the sandbox's shared egress reached; curl got the same page). Not a resolver fault; re-run on another day.
Re-run on 2026-10-20 after the cap cleared: `ok`, the newest issue downloaded (4,023,880 bytes).

## Not yet confirmed

That the parish site links Discover Mass (blocked); the bulletin's masthead settles whose it
is.
