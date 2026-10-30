---
name: St. Francis of Assisi Parish
website: https://www.stfrancisparishlbi.org/
bulletin_provider: other
provider_id: page-pdfs https://www.stfrancisparishlbi.org/weekly-bulletin
publication: ['url:https://www.stfrancisparishlbi.org/weekly-bulletin']
group: Cohort 30 (Barnegat, Long Beach Island, Little Egg Harbor)
evidence:
- url: https://www.stfrancisparishlbi.org/s/046a_2026_11_01-1.pdf
  seen: 2026-10-30
  quote: THE WEEKLY BULLETIN OF ST . FRANCIS OF ASSISI PARISH
  note: 'Page 1 of the 1 November 2026 issue (''THE BRIDGE'', 12 pages, text layer): footer ''4700 Long
    Beach Boulevard, Brant Beach, NJ 08008 | Phone: 609. 494. 8861''. Page 5 ''Mass Schedule Oct. 17/18-Nov.
    21/22'': St. Francis of Assisi, Brant Beach, 9:00 AM daily (Mon.-Sat.), Sat 5:00 PM, Sun 8:30, 10:00,
    11:30 AM; ''ST. THOMAS OF VILLANOVA, Surf City - CLOSED'', ''ST. THOMAS AQUINAS, Beach Haven - CLOSED'',
    ''ST. CLARE, Loveladies - CLOSED''. Names this parish alone.'
- url: https://www.stfrancisparishlbi.org/weekly-bulletin
  seen: 2026-10-30
  quote: WEEKLY BULLETIN
  note: 'The parish''s Squarespace Weekly Bulletin page (plain fetch reads it): an archive of dated issues,
    newest ''November 1, 2026'', each a /s/046a_<yyyy>_<mm>_<dd>*.pdf link (visit.py --links). The page
    is not strictly newest-first in its PDF links.'
- url: https://www.stfrancisparishlbi.org/mass-schedule
  seen: 2026-10-30
  quote: Four sanctuaries, one spirit.
  note: 'Seasonal schedule on the parish site: Oct 10/11, Oct 17/18-Nov 21/22 and Nov 28/29-Dec 19/20,
    2026 list Surf City, Beach Haven and Loveladies as CLOSED; ''Associated Churches'' lists St. Francis
    of Assisi (4700 Long Beach Blvd., Brant Beach), St. Thomas Aquinas (2nd St and N Atlantic Ave, Beach
    Haven), St. Thomas of Villanova (13th & LB Blvd., Surf City) and St. Clare (59 Long Beach Blvd, Long
    Beach).'
- url: https://dioceseoftrenton.org/parishfinder
  seen: 2026-10-30
  note: 'Finder pin directory:14644 ''St. Francis of Assisi Parish'', 4700 Long Beach Blvd, Long Beach
    Township 08008-3926, (609) 492-2893, website stfrancisparishlbi.org: one pin for the parish, at the
    Brant Beach church.'
research:
- method: fetch:check on the row (page-pdfs stfrancisparishlbi.org/weekly-bulletin), run 2026-10-30
  url: https://www.stfrancisparishlbi.org/s/046a_2026_11_01-1.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: The pick is the correct current issue (1 November 2026, 'THE BRIDGE'; with --expected-identity
    'St. Francis of Assisi' identity matched on page 1). The resolver's date inference misreads the file
    name 046a_2026_11_01-1.pdf as 2026-01-01 and reports it stale (age 302 days, overall failed); the
    issue date on the cover is November 1, 2026. Recheck when a normally named issue is posted (the 25
    October file 046A_2026_10_25.pdf has no suffix).
  retry_when: The next Sunday's issue is posted, or the resolver reads a trailing -1 in the file name
    correctly
bulletin_status: available
publication_reviews:
- parish: st-theresa-little-egg-harbor
  decision: separate
  evidence:
  - url: https://www.stfrancisparishlbi.org/s/046a_2026_11_01-1.pdf
    seen: 2026-10-30
    quote: THE WEEKLY BULLETIN OF ST . FRANCIS OF ASSISI PARISH
    note: The 1 November 2026 masthead of 'The Bridge' names St. Francis of Assisi Parish alone, with
      its Brant Beach footer address; St. Theresa's bulletin is a separate Bon Venture-printed issue on
      the eCatholic site.
- parish: st-mary-barnegat
  decision: separate
  evidence:
  - url: https://www.stfrancisparishlbi.org/s/046a_2026_11_01-1.pdf
    seen: 2026-10-30
    quote: THE WEEKLY BULLETIN OF ST . FRANCIS OF ASSISI PARISH
    note: The 1 November 2026 masthead of 'The Bridge' names St. Francis of Assisi Parish alone; Mass
      at Barnegat and Manahawkin is in St. Mary's own bulletin (John Patrick listing 563).
---

## Publisher

St. Francis of Assisi Parish (Long Beach Island) publishes its own weekly bulletin, "The Bridge", as dated PDFs on its Squarespace site (stfrancisparishlbi.org/weekly-bulletin). The 1 November 2026 issue (text layer) is headed "THE WEEKLY BULLETIN OF ST . FRANCIS OF ASSISI PARISH" and gives one Mass schedule for four churches. It names no other parish of Cohort 30.

## Worship sites

Four churches, all in the parish's 1 November 2026 schedule: St. Francis of Assisi, Brant Beach (the parish seat), St. Thomas Aquinas, Beach Haven (GCatholic's "St. Thomas"), St. Thomas of Villanova, Surf City and St. Clare, Loveladies. The three island churches are seasonal, closed from the Oct 17/18 weekend through at least 20 December 2026 and open in summer (the 9 August 2026 issue lists Mass at all four). See each church row and the *Rules settled* on seasonal shore churches.

## Website and bulletin provider

The finder's site stfrancisparishlbi.org is a Squarespace site; GCatholic's lbisaintfrancis.org timed out in the survey. The row reads the Weekly Bulletin page with `page-pdfs`; the PDFs live under /s/ on the same host.

## Not yet confirmed

The `fetch:check` run on 2026-10-30 picks the right file (the 1 November 2026 issue) but reports it stale: the resolver reads the file name `046a_2026_11_01-1.pdf` as 2026-01-01. The cover says November 1, 2026, and identity matched with `--expected-identity "St. Francis of Assisi"`. Recheck when the next week's normally named issue is posted (see research). The three island churches' winter and 2027 summer schedules are not yet read (see their revisits).
