---
name: Belmont Catholic Community (Our Lady of Mount Carmel and St. Martin of Tours), Bronx
website: https://ourladymtcarmelbx.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:11116']
group: Belmont Catholic Community
evidence:
- url: https://files.ecatholic.com/11116/bulletins/20260218.pdf?t=1770910894000
  seen: 2026-11-08
  quote: BELMONT CATHOLIC COMMUNITY
  note: 'Newest issue posted on either parish site: 18 February 2026 (Ash Wednesday). Page 1 masthead
    names Our Lady of Mount Carmel Church and Saint Martin of Tours Church, each with its own Mass box
    and office (664 Grote Street and 2380 Belmont Ave).'
- url: https://ourladymtcarmelbx.org/bulletins
  seen: 2026-11-08
  quote: February 18, 2026
  note: 'Bulletin archive (eCatholic 11116) read in headed Chrome: newest entry 18 February 2026, then
    2 March 2025, 8 December 2024; posting has been occasional since 2024.'
- url: https://stmartinoftoursbronx.org/bulletins
  seen: 2026-10-31
  note: 'St. Martin''s own eCatholic archive (site 6761), read in headed Chrome: newest issue 26 November
    2023 (files.ecatholic.com/6761/bulletins/20231126.pdf). No 2026 issue at the dated eCatholic paths
    for the ten Sundays to 1 November.'
- url: https://ourladymtcarmelbx.org/
  seen: 2026-11-08
  quote: 'Saturday: 5:00 PM Sunday: 9:30 AM Spanish 11:00 AM Italian 12:15 PM 1:30 PM Spanish'
  note: Home page Mass schedule for Our Lady of Mount Carmel.
- url: https://stmartinoftoursbronx.org/
  seen: 2026-11-08
  quote: SATURDAY VIGIL 6:00 PM Spanish SUNDAY 9:30 AM 11:00 AM Spanish
  note: Home page Mass schedule for St. Martin of Tours; the page shows the 32nd Sunday readings, so it
    is maintained.
research:
- method: visit.py (headed Chrome) on both parish bulletin archives
  url: https://ourladymtcarmelbx.org/bulletins
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-read both archives (ourladymtcarmelbx.org/bulletins, stmartinoftoursbronx.org/bulletins)
    or run issues.py ecatholic on ecatholic:11116 and ecatholic:6761
  retry_when: Either archive lists an issue dated after 18 February 2026
  revisit_after: 2027-01-10
- method: issues.py ecatholic, 10 Sundays back from 1 November 2026, on ecatholic:11116 and ecatholic:6761
  url: https://files.ecatholic.com/11116/bulletins/
  checked: '2026-10-31'
  outcome: not-found
  next_action: Repeat with issues.py when an archive shows a new issue
  retry_when: A new archive entry appears
- method: Discover Mass church pages our-lady-of-mount-carmel-bronx-ny and st-martin-of-tours-bronx-ny
    (issues.py discovermass)
  url: https://discovermass.com/church/our-lady-of-mount-carmel-bronx-ny/
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-check the Discover Mass pages
  retry_when: The parish sites link a Discover Mass bulletin
- method: probe po on ParishesOnline org slugs our-lady-of-mount-carmel-church-10458 and st-martin-of-tours-church-10457
  url: https://parishesonline.com/organization/st-martin-of-tours-church-10457
  checked: '2026-11-08'
  outcome: not-found
  next_action: None unless a parish page links an LPi widget
  retry_when: An LPi widget or ParishesOnline link appears on either site
- method: Flocknote network olmcbx.flocknote.com read in headed Chrome
  url: https://olmcbx.flocknote.com/home
  checked: '2026-11-08'
  outcome: not-found
  next_action: 'None: the network page is a sign-up form with no public notes'
  retry_when: Either parish site links a public Flocknote bulletin
bulletin_status: not-found
---

## Publisher

Our Lady of Mount Carmel (627 E 187th St) and St. Martin of Tours (664 Grote St) form the Belmont Catholic Community and, when they publish a bulletin online, publish one together: the newest posted issue, 18 February 2026 on Mount Carmel's eCatholic site (11116), names both churches in its page-1 masthead with a Mass box for each. Before that the archive has 2 March 2025 and 8 December 2024; St. Martin's own eCatholic archive (6761) stopped on 26 November 2023. No current bulletin was found anywhere checked on 31 October and 8 November 2026 (see `research`), so the row is `no_bulletin` and kept off the site (Settled policy 4). It is not a statement that the community stopped printing a bulletin.

## Worship sites

Both churches hold public Mass now, per their own home pages read 8 November 2026: Mount Carmel Saturday 5:00 PM, Sunday 9:30 (Spanish), 11:00 (Italian), 12:15 and 1:30 (Spanish), weekdays 12:00 and 6:00 PM; St. Martin Saturday 6:00 PM (Spanish), Sunday 9:30 and 11:00 (Spanish). The archdiocesan map titles both 'Belmont Catholic Community'.

## Website and bulletin provider

The website is Mount Carmel's eCatholic bulletin archive, because the only 2026 issue is there. If a current issue appears on either site, set `bulletin_provider: ecatholic` with that site's bulletin page, run fetch:check, and re-read the masthead: if St. Martin's site resumes its own issues, split the row.

## Not yet confirmed

Whether the community still prints a weekly paper bulletin offline is unknown; nothing online since 18 February 2026. Discover Mass, ParishesOnline (St. Martin has an org listing with no publications), and the Mount Carmel Flocknote network (sign-up only) carry no bulletin.
