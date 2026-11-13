---
name: St. Peter
website: https://stpeterdanb.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:24336']
group: ''
evidence:
- url: https://files.ecatholic.com/24336/bulletins/20261101.pdf
  seen: 2026-11-12
  quote: 16 Cottage Street, Danbury
  note: 'Page 1 of the 1 November 2026 issue (7 pages): masthead ''Saint Peter Parish'', ''NOVEMBER 1,
    2026'', ''MASS SCHEDULE 104 Main Street, Danbury, CT 06810''; St. Peter Church: Saturday Vigil 5:00
    p.m., Sunday 7:30, 9:00 a.m. (Spanish), 10:30 a.m., 12:00 N, 5:00 p.m. (Spanish), weekdays Mon-Sat
    7:30 a.m., Mon-Fri 12:10 p.m.; Sacred Heart Church, 16 Cottage Street, Danbury: Saturday Vigil 5:00
    p.m., Sunday 7:30, 9:00 a.m. and 12:00 noon (Spanish).'
- url: https://files.ecatholic.com/24336/bulletins/20261101.pdf
  seen: 2026-11-12
  quote: Sacred Heart of Jesus Church
  note: 'Page 2: pastor Rev. Gregg D. Mecca; separate office hours for St. Peter (104 Main Street) and
    Sacred Heart Church (12 Cottage Street, ''Mail to: 46 Stone Street''); sacrificial giving reported
    for both St. Peter Church and Sacred Heart of Jesus Church. No mention of Our Lady of Aparecida, Portuguese
    Masses or Immaculate Heart of Mary (grep for Aparecida, Portug, Brazil: 0 hits).'
- url: https://stpeterdanb.org/bulletins
  seen: 2026-11-12
  note: Read with parish-site-access visit.py (probe url gets 403, Cloudflare). eCatholic site 24336;
    lists files.ecatholic.com/24336/bulletins/ issues weekly from 20260802 to 20261101 (the newest on
    2026-11-12; 20261108 and 20261115 answered 403).
research:
- method: issues.py ecatholic ecatholic:24336 --weeks 4
  url: https://files.ecatholic.com/24336/bulletins/20261108.pdf
  checked: '2026-11-12'
  outcome: not-found
  next_action: Rerun issues.py ecatholic ecatholic:24336 and fetch:check; if no issue after 1 November
    appears, read the /bulletins page with visit.py for a changed host
  retry_when: After 2026-11-22, when the 22 November issue should be up
  revisit_after: 2026-11-23
bulletin_status: available
---

## Publisher

St. Peter, Danbury publishes one weekly bulletin for its two churches, St. Peter and Sacred Heart of Jesus, posted on its eCatholic site (id 24336). The 1 November 2026 issue (`https://files.ecatholic.com/24336/bulletins/20261101.pdf`, read 2026-11-12) is headed "Saint Peter Parish", "NOVEMBER 1, 2026", with pastor Rev. Gregg D. Mecca, and its page 1 Mass schedule covers "St. Peter Church" (104 Main Street) and "Sacred Heart Church, 16 Cottage Street, Danbury". Page 2 gives office hours and the weekly collection for both churches.

## Worship sites

- `st-peter-danbury`: Saturday Vigil 5:00pm; Sunday 7:30, 9:00am (Spanish), 10:30am, 12:00 noon, 5:00pm (Spanish); weekdays Mon-Sat 7:30am, Mon-Fri 12:10pm.
- `sacred-heart-danbury`: Saturday Vigil 5:00pm; Sunday 7:30, 9:00am and 12:00 noon (Spanish). The diocese's directory lists it as the "Sacred Heart of Jesus campus" of St. Peter (mass-times:1360-sacred-heart-of-jesus-campus); GCatholic lists it separately (22024). Per the diocese's settled rule on merged parishes' campuses, it is a church of this row: it has no bulletin of its own (the shared bulletin carries its schedule and collection).

The diocese's directory notes Masses of Our Lady of Aparecida "At St. Peter Parish, Danbury" (directory:1167, mass-times:1167-st-peter-church-aparecida-masses). The 1 November 2026 St. Peter bulletin lists no Portuguese or Aparecida Mass, and Aparecida's own site (read 2026-11-12) gives its whole schedule at 42 Vail Road, Bethel and says it moved to "a new location in Bethel". That roster entry is linked to the St. Peter church as the same building; see `our-lady-of-aparecida-bethel`.

## Website and bulletin provider

`stpeterdanb.org` is the eCatholic site (id 24336), behind Cloudflare: `probe url` gets 403, `visit.py` loads it. Its `/bulletins` page lists `files.ecatholic.com/24336/bulletins/<YYYYMMDD>.pdf` issues; on 2026-11-12 the newest was 20261101 (8 and 15 November answered 403). The home page also links monthly schedule PDFs under `/documents/2026/11/` (`SP11.26.pdf`, `SH 11.26 v2.pdf`), which are not the bulletin. Provider `ecatholic`.

`fetch:check` on 2026-11-12 picked `https://files.ecatholic.com/24336/bulletins/20261101.pdf` (the 1 November 2026 issue, the newest posted; freshness `fresh`, 11 days). Identity unverified, as for every eCatholic row; masthead checked by hand above.

## Not yet confirmed

The newest issue on 2026-11-12 was 11 days old; the 8 November issue was not posted. See research for the retry.
