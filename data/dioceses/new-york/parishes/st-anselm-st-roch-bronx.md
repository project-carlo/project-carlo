---
name: St. Anselm - St. Roch, Bronx
website: https://stanselmnyc.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:11115']
group: St. Anselm - St. Roch
evidence:
- url: https://stanselmnyc.org/bulletins
  seen: 2026-11-08
  quote: Bulletin Archive 2026 August 2, 2026 June 7, 2026 May 31, 2026 May 17, 2026 March 22, 2026
  note: 'eCatholic archive (site 11115) read in headed Chrome: the parish posts issues irregularly, the
    newest 2 August 2026, 14 weeks before this check.'
- url: https://files.ecatholic.com/11115/bulletins/20260802.pdf?t=1788972503000
  seen: 2026-11-08
  quote: Sunday August 2nd  / Domingo , Agosto
  note: The 2 August 2026 issue is two pages (collection, RCIA notice 'SS.Anselm &  Roch’s'), published
    by St. Anselm - St. Roch.
- url: https://stanselmnyc.org/
  seen: 2026-11-08
  quote: 'Sun: 9:30 AM English 11:00 AM Español 12:30 PM English'
  note: Home page header 'Church of St.Anselm & St.Roch 685 Tinton Ave, Bronx, New York 10455' with Sunday
    and daily Mass times.
research:
- method: visit.py (headed Chrome) on the bulletin archive; issues.py ecatholic ecatholic:11115 over 15
    Sundays to 8 November 2026
  url: https://stanselmnyc.org/bulletins
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-read the archive or run issues.py ecatholic ecatholic:11115; if issues are again weekly,
    set bulletin_provider ecatholic and run fetch:check
  retry_when: The archive lists an issue dated after 2 August 2026
  revisit_after: 2027-01-10
- method: Discover Mass slug st-anselm-bronx-ny (404); ParishesOnline st-anselm-10455, st-anselm-st-roch-10455,
    st-anselm-church-10455 (no org)
  url: https://discovermass.com/church/st-anselm-bronx-ny/
  checked: '2026-11-08'
  outcome: not-found
  next_action: None
  retry_when: The parish site links another publisher
bulletin_status: not-found
---

## Publisher

St. Anselm - St. Roch publishes its bulletin on its own eCatholic site (11115), but posts it irregularly: the 2026 archive has 1, 8 and 22 February, 8, 15 and 22 March, 17 and 31 May, 7 June and 2 August, and nothing after 2 August as of 8 November 2026. With no current issue found, the row is `no_bulletin` and kept off the site (Settled policy 4). This is about the online archive, not a statement that printing stopped.

## Worship sites

One church, St. Anselm, Tinton Avenue, with Sunday 9:30 AM (English), 11:00 AM (Spanish), 12:30 PM (English) and daily Masses per the home page (8 November 2026). St. Roch on Wales Avenue was relegated to profane use by decree and is excluded separately; its name stays in the parish title only.

## Website and bulletin provider

The website is the eCatholic bulletin archive. When issues resume weekly, set `bulletin_provider: ecatholic` and run fetch:check.

## Not yet confirmed

Whether weekly issues exist in print between the posted ones.
