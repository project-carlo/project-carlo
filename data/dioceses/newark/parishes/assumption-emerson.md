---
name: Assumption, Emerson
website: https://www.assumptionemersonnj.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:36468']
group: ''
evidence:
- url: https://files.ecatholic.com/36468/bulletins/20261025.pdf
  seen: 2026-11-03
  quote: 'Rectory: 29 Jefferson Avenue, Emerson, NJ 07630'
  note: '25 October 2026 issue (Thirtieth Sunday in Ordinary Time; 8 pages, text layer). Page 1 masthead:
    Church of the Assumption of the Blessed Virgin Mary, Emerson; Rev. John P. Ginty, Administrator; Mass
    Schedule Saturday 5:00 PM, Sunday 8:30 AM, 10:00 AM, 12:15 PM, daily (including Saturday) 8:00 AM
    and 12:05 PM. No other church or chapel of the parish named; no publisher footer.'
- url: https://www.assumptionemersonnj.org/bulletins
  seen: 2026-11-03
  note: eCatholic bulletin page (answers probe get 403; read with visit.py). Lists weekly files.ecatholic.com/36468/bulletins/YYYYMMDD.pdf
    issues, newest 20261025.pdf; no 1 November 2026 issue posted as of 3 November.
bulletin_status: available
---

## Publisher

The Church of the Assumption of the Blessed Virgin Mary, Emerson, self-publishes a weekly bulletin on its eCatholic site (ecatholic:36468). I read the 25 October 2026 issue: the page 1 masthead names this church alone, with its rectory at 29 Jefferson Avenue, its Mass schedule and its staff (Rev. John P. Ginty, Administrator). It carries no LPi, John Patrick or Bon Venture footer.

## Worship sites

- Church of the Assumption, 29 Jefferson Avenue (`assumption-emerson`): Saturday 5:00 PM; Sunday 8:30, 10:00 AM, 12:15 PM; daily including Saturday 8:00 AM and 12:05 PM.

The directory (40) and GCatholic (18399) list only this church; Assumption School is a school. The two chapels the 25 October issue mentions (Siegfried Hall, the Basilica of the Sacred Heart) are in a reprinted Notre Dame reflection, not places of this parish.

## Website and bulletin provider

The directory's http://www.assumptionemersonnj.org/ redirects to https://www.assumptionemersonnj.org/, an eCatholic site behind Cloudflare (`probe get` 403; `visit.py` loads it). Its /bulletins page lists Sunday-dated issues on files.ecatholic.com. Provider `ecatholic`, read from the site.

Fetch check (2026-11-03, headed): transport ok, PDF, picked `files.ecatholic.com/36468/bulletins/20261025.pdf`, the 25 October 2026 issue read above (the newest posted); freshness fresh (9 days). Publication identity `unverified` in the check; the masthead read above confirms it.

## Not yet confirmed

The 1 November 2026 issue was not yet posted on 3 November (issues.py: 403 for 20261101.pdf). Nothing else open.
