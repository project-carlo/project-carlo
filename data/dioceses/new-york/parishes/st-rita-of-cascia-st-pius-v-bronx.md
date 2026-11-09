---
name: St. Rita of Cascia - St. Pius V, Bronx
website: https://santaritabronx.com/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: St. Rita of Cascia - St. Pius V
evidence:
- url: https://santaritabronx.com/bulletins
  seen: 2026-11-09
  quote: Bulletin Archive
  note: The eCatholic site's (6766) Bulletin Archive, read in headed Chrome, lists no issues.
- url: https://santaritabronx.com
  seen: 2026-11-09
  quote: 'StaRita: Horario especial por visita de obispo Ronald Hicks al Bronx'
  note: The home page shows the parish's Flocknote messages (short notices, not a bulletin), posted hours
    before this read.
- url: https://santaritabronx.com/mass-times
  seen: 2026-11-09
  quote: SATURDAY VIGIL 7:00 PM Spanish SUNDAY 10:00 AM Spanish 11:30 AM 6:00 PM Spanish
  note: Mass Times page.
research:
- method: visit.py --bulletin on santaritabronx.com and /bulletins; issues.py ecatholic ecatholic:6766
    over 10 Sundays to 8 November 2026
  url: https://santaritabronx.com/bulletins
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-read the archive; if issues appear, set bulletin_provider ecatholic and run fetch:check
  retry_when: The archive lists an issue
  revisit_after: 2027-02-01
- method: issues.py discovermass st-rita-of-cascia-bronx-ny ('no bulletins available'); ParishesOnline
    st-rita-of-cascia-10451, st-rita-of-cascia-st-pius-v-10451, st-rita-of-cascia-church-10451 (no org)
  url: https://discovermass.com/church/st-rita-of-cascia-bronx-ny/
  checked: '2026-11-08'
  outcome: not-found
  next_action: None
  retry_when: The parish site links another publisher
bulletin_status: not-found
---

## Publisher

St. Rita of Cascia - St. Pius V has an eCatholic site (6766) with an empty Bulletin Archive, no dated eCatholic issue for the 10 Sundays to 8 November 2026, no Discover Mass bulletins and no ParishesOnline org under the likely slugs. Its live channel is Flocknote: short text notices shown on the home page (one posted 9 November about a schedule change for a bishop's visit), which are not a bulletin and carry no full schedule. No bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, St. Rita of Cascia, 448 College Avenue: Saturday 7:00 PM vigil (Spanish), Sunday 10:00 AM (Spanish), 11:30 AM and 6:00 PM (Spanish), and weekday Masses, per the Mass Times page read 9 November 2026. The former St. Pius V church was relegated by decree and is excluded separately.

## Website and bulletin provider

`no_bulletin`; the website is the parish's (empty) bulletin archive.

## Not yet confirmed

Whether the parish prints a bulletin it does not post.
