---
name: St. Hedwig, Elizabeth
website: https://sainthedwignj.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:34102']
group: ''
evidence:
- url: https://files.ecatholic.com/34102/bulletins/20261101.pdf
  seen: 2026-11-05
  quote: 600 Myrtle Street,  Elizabeth, New Jersey  07202
  note: 'Page 1 masthead of the 12-page monthly issue: ''Saint Hedwig Roman Catholic Church X Rzymskokatolicka
    Parafia Świętej Jadwigi'', ''Sundays of November 1st, 8th, 15th and 22nd, 2026'', ''Rev. Maciej (MJ)
    Zając, Pastor'', ''Parish Website: www.sainthedwignj.org'', office 717 Polonia Avenue. Pages 2-3:
    Sunday Masses 8:00 am, 10:00 am, 12:00 pm; weekday Masses 12:15 pm or 7:00 pm; ''Mass Celebrated in
    the Church''. No other church named.'
- url: https://sainthedwignj.org/
  seen: 2026-11-05
  note: 'eCatholic site (probe url gets 403; visit.py reads it): title ''St. Hedwig''s Church - Elizabeth,
    NJ'', eCatholic id 34102, Bulletins page https://sainthedwignj.org/bulletins.'
- url: https://rcan.org/parishes/
  seen: 2026-11-05
  note: 'Archdiocese directory entry 38: St. Hedwig Parish, 717 Polonia Avenue, Elizabeth, NJ 07202, website
    https://sainthedwignj.org/.'
promoted: 2026-11-05
research:
- method: issues.py ecatholic:34102 --weeks 4
  url: https://files.ecatholic.com/34102/bulletins/20261101.pdf
  checked: '2026-11-05'
  outcome: found
  next_action: Check that the next monthly issue (expected dated 2026-11-29) appears and that fetch:check
    still calls the 1 November issue current mid-month
  retry_when: After 2026-11-29
  revisit_after: 2026-11-30
bulletin_status: available
---

## Publisher

The parish posts its own bulletin on eCatholic (site id 34102, `files.ecatholic.com/34102/bulletins/<yyyymmdd>.pdf`). It is **monthly**: the 1 November 2026 issue (12 pages, English and Polish) is headed "Sundays of November 1st, 8th, 15th and 22nd, 2026". Its page-1 masthead reads "Saint Hedwig R. C. Church 600 Myrtle Street, Elizabeth, New Jersey 07202", "Rev. Maciej (MJ) Zając, Pastor", "Parish Website: www.sainthedwignj.org" and gives the parish office at 717 Polonia Avenue. `issues.py` found no 8 November file (403), as expected for a monthly issue.

## Worship sites

One church, `st-hedwig-elizabeth`. The Mass intentions on pages 2-3 give Sunday Masses at 8:00 am, 10:00 am and 12:00 pm and weekday Masses at 12:15 pm or 7:00 pm, marked "Mass Celebrated in the Church", and name no other place. The directory (38) and GCatholic (18394) each list only this church.

## Website and bulletin provider

https://sainthedwignj.org/ (directory) is the eCatholic site. Cloudflare gives `probe url` a 403 and `visit.py` reads it. Provider `ecatholic`, publication `ecatholic:34102`.

Fetch check (2026-11-05, headed): transport ok, PDF; the eCatholic resolver read https://sainthedwignj.org/bulletins and picked `files.ecatholic.com/34102/bulletins/20261101.pdf`, the November 2026 monthly issue read above (date inferred from the URL); freshness `fresh` (4 days). Identity `unverified` only because no expected identity is supplied; the masthead confirms it.

## Not yet confirmed

The issue is monthly, so from mid-month a 14-day freshness window may call the 1 November issue stale even though it covers the Sundays through 22 November. The research item schedules a recheck after the next issue, expected 29 November.
