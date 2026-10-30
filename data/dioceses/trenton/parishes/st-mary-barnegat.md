---
name: St. Mary Parish
website: https://stmarybarnegat.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-mary-s-barnegat-nj-08005
publication: ['url:https://www.church-bulletin.org/saint-mary-s-barnegat-nj-08005']
group: Cohort 30 (Barnegat, Long Beach Island, Little Egg Harbor)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-mary-s-barnegat-nj-08005/2026-11-01.pdf
  seen: 2026-10-30
  quote: ST. MARY OF THE PINES - MANAHAWKIN
  note: 'Page 1 (text layer, 12 pages) of the 1 November 2026 issue: the Masses block lists two churches,
    ''ST. MARY’S CHURCH - BARNEGAT'' (Sat 5:30 PM; Sun 8:00, 10, 12:00 noon and 5:00 PM) and ''ST. MARY
    OF THE PINES - MANAHAWKIN'' (Sat 4:00 PM; Sun 7:30, 9:00, 11:30 AM; Spanish Sun 2:00 PM). Masthead
    block: ''REV. MSGR. KEN TUZENEU, PASTOR'', church and rectory 747 West Bay Avenue, P.O. Box 609, Barnegat
    08005, and ''St. Mary of the Pines, 100 Bishop Lane, Manahawkin''. Names this parish alone.'
- url: https://www.church-bulletin.org/saint-mary-s-barnegat-nj-08005
  seen: 2026-10-30
  quote: Saint Mary's Bulletin
  note: 'John Patrick Publishing listing 563 (probe url): issues 2026-09-06 to 2026-11-01 as /bulletin/saint-mary-s-barnegat-nj-08005/<yyyy-mm-dd>.pdf;
    the 1 November issue is the newest.'
- url: https://stmarybarnegat.com/
  seen: 2026-10-30
  note: Finder website directory:14653, a Solutio site. Plain fetch answers 403 (probe url HTTP4XX); its
    /file PDFs are the blocked kind, so the row reads the printer's listing. The site itself was not re-read
    for this row.
- url: https://dioceseoftrenton.org/parishfinder
  seen: 2026-10-30
  note: 'Finder pin directory:14653 ''St. Mary Parish'', 747 W Bay Ave, Barnegat 08005-2130, (609) 698-5531:
    one pin for the parish, at the Barnegat church. GCatholic lists St. Mary (18783) and, grouped under
    ''St. Mary Parish'', St. Mary of the Pines, Manahawkin (18820).'
research:
- method: fetch:check on the row (page-pdfs church-bulletin.org/saint-mary-s-barnegat-nj-08005), run 2026-10-30
  url: https://www.church-bulletin.org/bulletin/saint-mary-s-barnegat-nj-08005/2026-11-01.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: 'None while the pick is the newest dated listing PDF: it resolves to the 1 November 2026
    file (issue date inferred 2026-11-01, future freshness because it is posted before its date, identity
    unverified because no expected identity was supplied).'
  retry_when: The pick stops being the newest dated listing PDF
- method: probe url on the parish site stmarybarnegat.com
  url: https://stmarybarnegat.com/
  checked: '2026-10-30'
  outcome: access-blocked
  next_action: Read the site with parish-site-access visit.py if its Contact page or a later issue is
    needed (e.g. to settle the Manahawkin street name)
  retry_when: The listing stops carrying the newest issue, or the Manahawkin street name needs settling
bulletin_status: available
publication_reviews:
- parish: st-francis-of-assisi-long-beach-island
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-mary-s-barnegat-nj-08005/2026-11-01.pdf
    seen: 2026-10-30
    quote: 747 West Bay Avenue
    note: The 1 November 2026 masthead of St. Mary's bulletin names St. Mary's Church, Barnegat and St.
      Mary of the Pines, Manahawkin only, with its own pastor; the Long Beach Island parish publishes
      its own Brant Beach bulletin (St. Francis of Assisi, 4700 Long Beach Boulevard).
- parish: st-theresa-little-egg-harbor
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-mary-s-barnegat-nj-08005/2026-11-01.pdf
    seen: 2026-10-30
    quote: 747 West Bay Avenue
    note: The 1 November 2026 masthead of St. Mary's bulletin names St. Mary's Church, Barnegat and St.
      Mary of the Pines only; St. Theresa, Little Egg Harbor publishes a bulletin with its own masthead
      and pastor (Rev. Selvam J. Asirvatham).
- parish: st-mary-mother-of-god-middletown
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-mary-s-barnegat-nj-08005/2026-11-01.pdf
    seen: 2026-10-30
    quote: 747 West Bay Avenue
    note: The 1 November 2026 masthead of St. Mary's bulletin (Barnegat, Ocean County) names a pastor,
      Msgr. Ken Tuzeneu, and two Ocean County churches; St. Mary, Mother of God in Middletown (Monmouth
      County) publishes ParishesOnline container 03/1430 with its own masthead. GCatholic's 'St. Mary
      Parish' group is the same name only.
---

## Publisher

St. Mary Parish (Barnegat) publishes its own weekly bulletin through John Patrick Publishing (listing 563 on church-bulletin.org). The 1 November 2026 issue has a text layer; page 1 gives the Mass schedule for St. Mary's Church, Barnegat and St. Mary of the Pines, Manahawkin, with Msgr. Ken Tuzeneu as pastor and the Barnegat rectory (747 West Bay Avenue) as the parish address. It names no other parish. Cohort 30's other two parishes, St. Francis of Assisi (Long Beach Island) and St. Theresa (Little Egg Harbor), publish their own bulletins under their own mastheads (see their rows), so the cohort is three rows by the *Rules settled*.

## Worship sites

Two churches: St. Mary, Barnegat (`st-mary-barnegat`) and St. Mary of the Pines, Manahawkin (`st-mary-of-the-pines-manahawkin`, GCatholic 18820, grouped under St. Mary Parish there). Both hold weekend and weekday Mass in the 1 November 2026 schedule (Barnegat Monday-Saturday 8:00 AM; the Pines Monday-Friday 9:00 am). Nothing the rosters list for this parish is left out.

## Website and bulletin provider

stmarybarnegat.com is a Solutio CMS site that refuses plain fetch; the row reads the John Patrick listing with `page-pdfs`. GCatholic's website for it (stmary.shoresurfer.com) has no DNS. The listing's name is "Saint Mary's".

## Not yet confirmed

Nothing outstanding. The parish's own site was not read, so whether it carries a later issue than the listing is unchecked; the listing had the 1 November issue on 2026-10-30.
