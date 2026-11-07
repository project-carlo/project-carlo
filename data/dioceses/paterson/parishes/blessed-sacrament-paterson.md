---
name: Blessed Sacrament
website: https://blessedsacramentrcc.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://blessedsacramentrcc.com/bulletins
  seen: 2026-11-05
  note: 'Read with parish-site-access visit.py (probe url gets 403; eCatholic site 12000). The page shows
    the headings ''Bulletin'' and ''Archive'' and no bulletin files: its links are the menu, Facebook
    and eCatholic only.'
- url: https://blessedsacramentrcc.com/mass-times
  seen: 2026-11-05
  quote: 'SATURDAY/SABADO:  4:30 PM  |  7:00 PM (Spanish)'
  note: 'visit.py. Also ''SUNDAY/DOMINGO: 9:00 AM | 11:00 AM (Spanish)'' and ''LUNES - VIERNES: 7:30 AM'';
    footer ''Blessed Sacrament Roman Catholic Church 224 East 18th Street, Paterson, NJ, 07524''. The
    home page menu links no bulletin either.'
- url: https://parishesonline.com/organization/blessed-sacrament-church-07524
  seen: 2026-11-05
  note: 'probe po: org ''Blessed Sacrament Church'', 224 E 18th St, Paterson 07524-1897, LPi id 0018000000QxAY3AAN,
    with no publications (''this organization does not publish a bulletin here now'').'
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: Finder pin directory:12000 'Blessed Sacrament, Paterson', 224 East 18th Street, Paterson 07524,
    website https://blessedsacramentrcc.com/; Saturday 4:30 PM English, 7:00 PM Spanish; Sunday 9:00 AM
    English, 11:00 AM Spanish; Monday-Friday 7:30 AM.
revisit: Reload https://blessedsacramentrcc.com/bulletins with visit.py and probe files.ecatholic.com/12000/bulletins/<Sunday>.pdf;
  probe po blessed-sacrament-church-07524. If issues appear, set the provider, its publication id, and
  run fetch:check.
revisit_after: 2027-02-01
research:
- method: parish-site-access visit.py on /bulletins (text and links), the home page and /mass-times (links)
  url: https://blessedsacramentrcc.com/bulletins
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reload the /bulletins page and the home menu
  retry_when: On the revisit date, or when the site or finder links a bulletin
- method: 'issues.py ecatholic ecatholic:12000: Sundays 20 Sep - 8 Nov 2026 and Saturday- and Friday-dated
    names for the four weeks to 8 Nov 2026 (all 403, not posted)'
  url: https://files.ecatholic.com/12000/bulletins/20261108.pdf
  checked: '2026-11-05'
  outcome: not-found
  next_action: Probe the coming Sundays' file names again
  retry_when: On the revisit date
- method: probe po blessed-sacrament-church-07524 (ParishesOnline org exists, no publications)
  url: https://parishesonline.com/organization/blessed-sacrament-church-07524
  checked: '2026-11-05'
  outcome: not-found
  next_action: Probe the org again for a publication
  retry_when: On the revisit date
- method: 'Facebook page https://www.facebook.com/pages/Blessed-Sacrament-Church/116390118386237 (linked
    from the site) not read: Facebook needs a login for the probes'
  url: https://www.facebook.com/pages/Blessed-Sacrament-Church/116390118386237
  checked: '2026-11-05'
  outcome: access-blocked
  next_action: Look at the page's posts for bulletin PDFs or images
  retry_when: When a way to read Facebook posts is available
bulletin_status: not-found
---

## Publisher

No bulletin found. Blessed Sacrament runs an eCatholic site (site id 12000, the finder pin id) whose Bulletin page, read 2026-11-05 with parish-site-access visit.py, shows the headings "Bulletin" and "Archive" and no issues. `files.ecatholic.com/12000/bulletins/<YYYYMMDD>.pdf` answered 403 (not posted) for every Sunday 20 September - 8 November 2026 and for Friday- and Saturday-dated names in the last four weeks. A ParishesOnline org for the parish (`blessed-sacrament-church-07524`, LPi `0018000000QxAY3AAN`) exists but publishes nothing. The site's Facebook page was not read. See `research`.

## Worship sites

One church, `blessed-sacrament-paterson`. The site's Mass Times page (2026-11-05) gives Saturday 4:30 PM and 7:00 PM (Spanish), Sunday 9:00 AM and 11:00 AM (Spanish), and Monday-Friday 7:30 AM, matching the finder (directory:12000). The finder's notes also name Blessed Sacrament School (277 Sixth Ave.) and a convent (289 Sixth Ave.); neither is listed as a place of public Mass, so neither has a record. The finder and GCatholic (19000) list this one church.

## Website and bulletin provider

`https://blessedsacramentrcc.com/` (the finder's website; eCatholic behind Cloudflare). Provider `no_bulletin`: public Mass but no bulletin posted, so promote keeps the row and its church off the site until one turns up. If issues appear on the site they will be `ecatholic:12000`; if on ParishesOnline, `po-org:blessed-sacrament-church-07524` and `lpi:0018000000QxAY3AAN` (not recorded as publication ids now, since the org publishes nothing).

## Not yet confirmed

Whether the parish posts a bulletin on Facebook (not readable by the probes). Revisit on 2027-02-01 as above.
