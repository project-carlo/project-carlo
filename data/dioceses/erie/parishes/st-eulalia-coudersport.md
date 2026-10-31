---
name: St. Eulalia Parish
website: https://www.steulaliacoudersport.org
bulletin_provider: ecatholic
provider_id: '2448'
publication: ['ecatholic:2448']
group: ''
evidence:
- url: https://files.ecatholic.com/2448/bulletins/20261025.pdf
  seen: 2026-10-23
  quote: Thu Oct 29 No Weekday Mass at St. Eulalia or St. Bibiana
  note: Page 1 (graphic cover) reads 'St. Eulalia Parish and Sacred Heart Mission, October 25, 2026, The
    Thirtieth Sunday in Ordinary Time' with the addresses of St. Eulalia (6 E. Maple Street, Coudersport)
    and Sacred Heart Mission (263 Main Street, Genesee); the quoted line is on page 2 (text layer). Page
    4 carries the St. Bibiana Thursday notice. The issue is posted on the parish site and carries a future
    date (read 2026-10-23).
- url: https://files.ecatholic.com/2448/bulletins/20260913.pdf
  seen: 2026-10-23
  quote: Sunday—8:30AM—Sacred Heart; and 11:00AM—St. Eulalia
  note: 'Parish Mass-schedule box in the 13 September 2026 issue: Monday 9:00AM St. Eulalia; Tuesday 6:00PM
    Sacred Heart; Wednesday 9:00AM St. Eulalia; Thursday 9:00AM St. Eulalia and 6:00PM St. Bibiana; Friday
    9:00AM; Saturday 4:00PM St. Eulalia; Sunday 8:30AM Sacred Heart and 11:00AM St. Eulalia. The October
    issues have no such box in the text layer.'
- url: https://www.steulaliacoudersport.org/
  seen: 2026-10-23
  quote: WITH THE MISSION CHURCH OF SACRED HEART
  note: 'Read in headed Chrome (visit.py --bulletin; probe url gets HTTP 403). Home page header ''ST.
    EULALIA PARISH WITH THE MISSION CHURCH OF SACRED HEART''; the page embeds ecatholic:2448 and links
    files.ecatholic.com/2448/bulletins/20261025.pdf and 20261018.pdf. Sunday schedule on the page: Sat
    4:00 PM Saint Eulalia; Sun 8:30 AM Sacred Heart, 11:00 AM Saint Eulalia.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor ..............................................................................................
    St. Eulalia, Coudersport
  note: 'Clergy PDF (updated 8/7/2026): Very Rev. Richard J. Allen, V.F., pastor of St. Eulalia, Coudersport,
    one assignment. (The locator''s pastor field for Sacred Heart, Austin and Galeton names Rev. Joseph
    V. Dougherty, which this list does not support.)'
- url: https://parishesonline.com/organization/st-eulalia-st-gabriel
  seen: 2026-10-23
  note: 'probe po st-eulalia-st-gabriel: LPi 0018000000QxBkyAAF, 6 E Maple St, Coudersport, website http://www.steulalia-stgabriel.org/;
    no publications (''does not publish a bulletin here now''). A stale org name from before the merger;
    not a channel.'
promoted: 2026-10-23
research:
- method: probe url on steulaliacoudersport.org (HTTP 403), then visit.py --bulletin in headed Chrome
  url: https://www.steulaliacoudersport.org/
  checked: '2026-10-23'
  outcome: found
  next_action: 'None: eCatholic 2448 is the channel; fetch:check run.'
- method: probe url on the directory's alternative domains steulalia-stgabriel.org (printed in the GCatholic
    entry and the ParishesOnline org) and steulaliacouderport.org (directory typo)
  url: https://steulalia-stgabriel.org/
  checked: '2026-10-23'
  outcome: not-found
  next_action: 'None needed: steulalia-stgabriel.org is a SPAM-SQUAT (casino/betting vocabulary, Russian
    title) and the typo domain is dead.'
  retry_when: Only if the parish site stops serving bulletins
---

## Publisher

St. Eulalia, Coudersport (pastor Very Rev. Richard J. Allen, V.F., per the clergy PDF updated 8/7/2026) publishes one weekly bulletin through eCatholic site 2448, linked from the parish home page. The 25 October 2026 issue is headed 'St. Eulalia Parish and Sacred Heart Mission' and gives the addresses of St. Eulalia (Coudersport) and Sacred Heart (Genesee). One bulletin therefore covers the parish church, its mission Sacred Heart and the secondary church St. Bibiana (weekly Thursday Mass this season); St. Augustine, Austin is a secondary church with only a feast-day Mass (see its excluded record).

## Worship sites

- St. Eulalia, 6 E. Maple St., Coudersport: Saturday 4:00 PM, Sunday 11:00 AM, weekday Masses.
- Sacred Heart, 263 Main St., Genesee (secondary mission): Sunday 8:30 AM, Tuesday 6:00 PM.
- St. Bibiana, 111 Germania St., Galeton (secondary church): Thursday 6:00 PM, 18 June to 19 November 2026 (church record).
- Not a row: St. Augustine, 33 Turner St., Austin: only the 28 August feast Mass and a private funeral Mass in the 53 issues read (excluded record, no-public-mass).

The directory's printable PDF (6 Oct 2026) lists exactly these four buildings under St. Eulalia: Sacred Heart 'Secondary Mission', St. Augustine and St. Bibiana 'Secondary Church'.

## Website and bulletin provider

The site (steulaliacoudersport.org) returns HTTP 403 to `probe url` and needs the headed browser. It is an eCatholic site; bulletins are `files.ecatholic.com/2448/bulletins/<yyyymmdd>.pdf`, one per Sunday, all 53 Sundays from 26 Oct 2025 to 25 Oct 2026 downloaded from that path. The directory also lists the misspelt steulaliacouderport.org (dead) and the printable directory and GCatholic give steulalia-stgabriel.org, now a casino spam site; the ParishesOnline org 'st-eulalia-st-gabriel' publishes nothing.

## Not yet confirmed

Nothing outstanding on identity. The parish site's Mass schedule is the only source for the Sunday times beyond the September bulletin box (October issues omit the box).
