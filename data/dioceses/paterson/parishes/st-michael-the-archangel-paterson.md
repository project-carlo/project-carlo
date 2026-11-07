---
name: St. Michael the Archangel
website: https://stmichaelpaterson.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:13153']
group: ''
evidence:
- url: https://stmichaelpaterson.com/bulletins
  seen: 2026-11-05
  quote: 70 CIANCI STREET, PATERSON, NJ 07501-1831
  note: Read with parish-site-access visit.py (probe url gets 403; eCatholic site 13153). The Bulletin
    page shows only the headings 'Bulletin' and 'ARCHIVE' and the footer 'ST. MICHAEL THE ARCHANGEL CATHOLIC
    CHURCH', with no file links.
- url: https://stmichaelpaterson.com/
  seen: 2026-11-05
  quote: Please contact The Cathedral of St. John The Baptist to obtain your Sacramental Records.
  note: Read with visit.py. The home page's only content is this 'Sacramental Records' notice (and its
    Spanish version); the menu has Home, Notice (photos only) and Contact Us, no Mass times and no bulletin.
- url: https://discovermass.com/church/st-michael-the-archangel-paterson-nj/
  seen: 2026-11-05
  note: 'issues.py discovermass: the church page exists (70 Cianci St.) but lists no bulletins.'
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: Finder pin directory:13153 'St. Michael the Archangel, Paterson', 70 Cianci St, 07501, website
    https://stmichaelpaterson.com/; Saturday 7:00 PM Spanish; Sunday 10:00 AM Italian/English, 11:30 AM
    and 1:00 PM Spanish; Tuesday 12:00 PM Spanish.
- url: https://beaconnj.org/bishop-visits-sisters-of-mercy-of-alma-serving-the-cathedral/
  seen: 2026-11-05
  quote: welcomed Bishop Kevin J. Sweeney into their convent, established at nearby St. Michael Parish,
    also in Paterson
  note: 'Beacon, 22 December 2025: the Sisters serving the Cathedral live in a convent at St. Michael;
    the article still calls St. Michael a parish. The priest directory (visit.py, 2026-11-05) lists no
    pastor or administrator for St. Michael, Paterson, and no Cathedral priest with it.'
revisit: Reopen https://stmichaelpaterson.com/bulletins with visit.py and run issues.py ecatholic ecatholic:13153;
  check the parish Facebook page and Discover Mass for a posted bulletin, and whether the Cathedral's
  site now lists Mass at St. Michael.
revisit_after: 2027-02-01
research:
- method: visit.py on the eCatholic /bulletins page, then issues.py ecatholic (Sunday and --day sat file
    names)
  url: https://stmichaelpaterson.com/bulletins
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reopen /bulletins and rerun issues.py ecatholic ecatholic:13153; look for a bulletin on
    the parish Facebook page (findglocal lists page id 1585682698354932) or a Flocknote group
  retry_when: The site lists bulletin files, or another source names a current St. Michael bulletin
  revisit_after: 2027-02-01
- method: issues.py discovermass on the Discover Mass church page found by a DuckDuckGo search
  url: https://discovermass.com/church/st-michael-the-archangel-paterson-nj/
  checked: '2026-11-05'
  outcome: not-found
  next_action: Rerun issues.py discovermass discovermass:st-michael-the-archangel-paterson-nj
  retry_when: Discover Mass lists issues for this church
- method: 'Lead check: who administers St. Michael. Priest directory (rcdop.org/priest-directory, visit.py)
    and The Beacon API search for St. Michael Paterson'
  url: https://rcdop.org/priest-directory
  checked: '2026-11-05'
  outcome: not-found
  next_action: Look for a decree or Beacon notice naming a pastor or administrator of St. Michael, Paterson,
    or the Cathedral listing Mass at 70 Cianci St; if the Cathedral runs it, move the church to cathedral-st-john-the-baptist-paterson
  retry_when: The priest directory names a priest for St. Michael, Paterson, or the Cathedral's site or
    a bulletin mentions it
  revisit_after: 2027-02-01
bulletin_status: not-found
---

## Publisher

No bulletin found. The parish's eCatholic site (site 13153, the finder pin id) has a Bulletin page with only the headings "Bulletin" and "ARCHIVE" and no file links (visit.py, 2026-11-05), and `issues.py ecatholic ecatholic:13153` found no file for any of the 12 Sundays from 23 August to 8 November 2026, nor for Saturday-dated names (403 each, which means never posted). Discover Mass has a page for the church (`discovermass.com/church/st-michael-the-archangel-paterson-nj/`) listing no bulletins. The site's home page carries only the notice "Please contact The Cathedral of St. John The Baptist to obtain your Sacramental Records."

## Worship sites

One church, `st-michael-the-archangel-paterson` (70 Cianci Street). The diocese's parish finder (directory:13153, read 2026-11-04) still lists it with Mass Saturday 7:00 PM Spanish, Sunday 10:00 AM Italian/English, 11:30 AM and 1:00 PM Spanish, and Tuesday 12:00 PM Spanish; GCatholic (19047) lists it as a church. No source read says it closed.

## Website and bulletin provider

`https://stmichaelpaterson.com/`, an eCatholic site behind Cloudflare (probe url 403, visit.py loads it). Provider `no_bulletin` (Settled policy 4: kept in the records, left off the site); `ecatholic:13153` is kept as the site's id in case issues appear there.

## Not yet confirmed

- Whether St. Michael is still a parish of its own. The home page sends sacramental-records requests to the Cathedral of St. John the Baptist, which suggests the Cathedral now administers it, but no source read states a merger, and the Cathedral's Mass page (rcdopcathedral.org/mass-schedule-1, read 2026-11-05) does not mention St. Michael. Reconcile checked on 2026-11-05: the priest directory names no pastor or administrator for St. Michael, Paterson, and no Cathedral priest with it; The Beacon (22 December 2025) still calls it "St. Michael Parish", where the Sisters who serve the Cathedral have their convent. Nothing read says the Cathedral administers it, so the church stays here. If a source shows the Cathedral runs it, move the church to `cathedral-st-john-the-baptist-paterson` (also `no_bulletin` today, so the site is unaffected either way).
- Whether the finder's Mass times are current: the parish's own site gives none. Revisit after 2027-02-01.
