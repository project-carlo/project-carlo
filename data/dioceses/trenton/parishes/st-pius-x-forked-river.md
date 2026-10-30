---
name: St. Pius X Parish
website: https://churchofstpius.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/590
publication: ['url:https://www.church-bulletin.org/the-church-of-saint-pius-the-tenth-forked-river-nj-08731']
group: Cohort 25 (Bayville, Forked River)
evidence:
- url: https://www.church-bulletin.org/bulletin/the-church-of-saint-pius-the-tenth-forked-river-nj-08731/2026-11-01.pdf
  seen: 2026-10-30
  quote: The Church of St. Pius the Tenth 300 Lacey Road, Forked River, New Jersey 08731 609-693-5107
    www.churchofstpius.org
  note: 'Masthead (page 1), page 2 and page 3 of the 1 November 2026 issue (12 pages, scanned images with
    no text layer; read from renders). Page 2: ''PASTOR Rev. Richard Basznianin'', ''ST. PIUS X CHURCH
    IS OPEN Monday - Friday 7:30AM - 3:00PM, Saturday 2:30PM - 5:30PM & Sunday 7:30AM - 1:00PM'', footer
    ''Page 1-590''. Page 3 (Solemnity of All Saints, Mass intentions): Sat 4:00pm; Sun 8:00am, 10:00am,
    12:00pm; Mon-Fri 8:00am. Names this parish alone; its Hispanic Ministry line is ''ST. BARNABAS Bayville,
    NJ'' with a St. Barnabas phone number, a ministry contact and not a shared bulletin.'
- url: https://www.church-bulletin.org/the-church-of-saint-pius-the-tenth-forked-river-nj-08731
  seen: 2026-10-30
  quote: The Church of Saint Pius the Tenth Bulletin
  note: 'John Patrick Publishing listing 590 on church-bulletin.org (tools/jppc-trenton.tsv: latest edition
    25 Oct 2026; 1 Nov now present), PDFs at /bulletin/the-church-of-saint-pius-the-tenth-forked-river-nj-08731/<yyyy-mm-dd>.pdf.'
- url: https://churchofstpius.org/parish-events/bulletin
  seen: 2026-10-30
  note: Parish Solutio site (finder website churchofstpius.org; plain fetch answers 403, the browser loads
    it). Its Bulletin page lists numbered issues to '122-november-1-2026' (/file), the same Sunday as
    the listing; the /file PDFs are the 403 ones.
- url: https://dioceseoftrenton.org/parishfinder
  seen: 2026-10-30
  note: Finder pin directory:14657 'St. Pius X Parish', 300 Lacey Road, Forked River 08731-2619, (609)
    693-5107, website churchofstpius.org; one pin for the parish. GCatholic's churchofstpiusx.net does
    not resolve (no DNS, 2026-10-30).
promoted: 2026-10-30
research:
- method: fetch:check on the row (page-pdfs church-bulletin.org/590), 1 November 2026 issue
  url: https://www.church-bulletin.org/bulletin/the-church-of-saint-pius-the-tenth-forked-river-nj-08731/2026-11-01.pdf
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: 'None while the row picks the current issue: it resolves to the 1 November file (future
    freshness, posted before its date); identity is unverified only because the 12 pages are scanned images
    with no text. Read the masthead from a render if the pick changes.'
  retry_when: A text-layer issue appears, or the pick stops being the newest dated listing PDF
- method: pnpm diocese probe url / recheck on the parish's own Solutio site
  url: https://churchofstpius.org/parish-events/bulletin
  checked: '2026-10-30'
  outcome: access-blocked
  next_action: 'Read the site with parish-site-access visit.py (done 2026-10-30: the Bulletin page lists
    issues to 1 Nov 2026, the same Sunday as the listing); its /file PDFs answer 403 to plain fetch, so
    the row reads the John Patrick listing'
  retry_when: Plain fetch of the parish site stops answering 403, or the listing stops carrying the newest
    issue
bulletin_status: available
---

## Publisher

St. Pius X Parish (Forked River) publishes its own weekly bulletin through John Patrick Publishing (listing 590 on church-bulletin.org). The 1 November 2026 issue (every recent issue is image-only) has a masthead, read from a render of page 1, reading "The Church of St. Pius the Tenth, 300 Lacey Road, Forked River", and page 2 names Rev. Richard Basznianin as pastor; page 3 lists the week's Masses. It names no other parish. Its ministry list has a "Hispanic Ministry - St. Barnabas, Bayville" contact, which is a ministry link between the two cohort parishes, not a shared bulletin: St. Barnabas prints its own.

## Worship sites

One church, St. Pius X, 300 Lacey Road (`st-pius-x-forked-river`). The bulletin names no mission or second site.

## Website and bulletin provider

churchofstpius.org is a Solutio CMS site (Bulletin page `/parish-events/bulletin`), 403 to plain fetch and loaded with visit.py. Its issues' `/file` PDFs are blocked like the other Solutio sites, so the row reads the John Patrick listing, which carries the same Sunday.

## Not yet confirmed

Nothing outstanding.
