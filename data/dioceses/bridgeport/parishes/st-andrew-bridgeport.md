---
name: St. Andrew
website: https://standrewchurchbpt.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:30688']
group: ''
evidence:
- url: https://files.ecatholic.com/30688/bulletins/20261025.pdf
  seen: 2026-11-12
  quote: 'Office: 435 Anton Street, Bridgeport, CT'
  note: 'Page 1 of the 25 October 2026 issue (6 pages): ''Saint Andrew Parish'', Pastor Father Arthur
    Mollenhauer; MASSES Saturday Vigil 4:00 PM, Sundays 9:00, 10:30 AM, 12:00 PM (Spanish), weekdays 9:00
    AM Monday-Friday. No ''Good Counsel'' or ''Ortega'' in the 25 Oct or 18 Oct issues (grep).'
- url: https://standrewchurchbpt.org/bulletins
  seen: 2026-11-12
  note: eCatholic Bulletins page (read with parish-site-access visit.py; probe url gets 403) lists files.ecatholic.com/30688/bulletins/
    issues newest first, latest 20261025.pdf, then 1018, 1011, 1004, 0927 ... (no 30 Aug or 6 Sep issue).
- url: https://standrewchurchbpt.org/mass-times
  seen: 2026-11-12
  note: 'Mass Times page: Saturday 4:00 PM; Sunday 9:00, 10:30 AM, 12:00 PM Spanish; Monday-Friday 9:00
    AM. One church; no chapel or mission listed.'
research:
- method: issues.py ecatholic ecatholic:30688 --weeks 4 and the Bulletins page in visit.py
  url: https://standrewchurchbpt.org/bulletins
  checked: '2026-11-12'
  outcome: found
  next_action: Check that issues after 25 October 2026 appear
  retry_when: On the next fetch run
bulletin_status: available
---

## Publisher

St. Andrew, Bridgeport (North End) posts its weekly bulletin on its eCatholic site (`ecatholic:30688`). The latest posted, 25 October 2026 (`https://files.ecatholic.com/30688/bulletins/20261025.pdf`, read 2026-11-12 with issues.py; 1, 8 and 15 November answered 403), is headed "Saint Andrew Parish ... Office: 435 Anton Street, Bridgeport, CT" and names Father Arthur Mollenhauer, Pastor. Its schedule: Saturday Vigil 4:00 PM; Sundays 9:00, 10:30 AM and 12:00 PM (Spanish); weekdays 9:00 AM Monday-Friday.

## Worship sites

One church, `st-andrew-bridgeport`. GCatholic lists a Chapel of Our Lady of Good Counsel, 163 Ortega Ave., as a mission of St. Andrew and gives it the dead `standrewbptparishesonline.com` website; neither the 25 or 18 October 2026 bulletins (grep 'Good Counsel', 'Ortega') nor the parish's Mass Times page name it, and the diocese's directory has no entry. Nothing read says it closed either, so it is an `open/` record (`our-lady-of-good-counsel-bridgeport`).

## Website and bulletin provider

eCatholic site behind Cloudflare (`probe url` 403; `visit.py` reads it). Provider `ecatholic`, read from the website. GCatholic's website for St. Andrew, `standrewbptparishesonline.com`, no longer resolves (DEAD-DNS 2026-11-12). The parish posts irregularly: the Bulletins page skips 30 August and 6 September 2026, and on 12 November the newest issue was 25 October.

`fetch:check` on 2026-11-12 picked `https://files.ecatholic.com/30688/bulletins/20261025.pdf`, the newest issue the parish has posted, and reported freshness `stale` (18 days; overall failed) because no November issue is up yet. The pick is right; the staleness is the parish's posting lag, not a fetch fault.

## Not yet confirmed

Whether the parish resumes weekly posting after 25 October 2026; see research.
