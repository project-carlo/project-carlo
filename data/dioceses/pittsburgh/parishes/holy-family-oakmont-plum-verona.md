---
name: Holy Family Parish (Oakmont, Plum, Verona)
website: https://www.holyfamilypgh.org
bulletin_provider: parishes_online
provider_id: holy-family-parish-opv
publication: ['po-org:holy-family-parish-opv', 'lpi:0018000000Qx7r6AAB', 'po-container:14/1224', 'ecatholic:24616']
group: Holy Family Parish
evidence:
- url: https://container.parishesonline.com/bulletins/14/1224/20261025B.pdf
  seen: 2026-10-23
  quote: WEEKEND MASSES
  note: 'Page 2 of the 25 October 2026 issue (20 pages, text layer readable), container 14/1224. One parish-wide
    list: Saturday vigil 4:00 PM St. John the Baptist and 5:30 PM St. Joseph; Sunday 7:30 AM and 10:30
    AM Our Lady of Joy, 8:00 AM and 11:00 AM St. Irenaeus, 9:00 AM, 12:00 PM and 5:30 PM St. John the
    Baptist, 9:30 AM St. Joseph; last Sunday of the month 2:00 PM Spanish Mass at St. John the Baptist;
    weekday Mass Tuesday 8:30 AM Our Lady of Joy; confessions and adoration at all four. Matches the diocese
    directory for every church except the time of the Spanish Mass (directory 4:00 PM).'
- url: https://container.parishesonline.com/bulletins/14/1224/20261025B.pdf
  seen: 2026-10-23
  quote: ST. IRENAEUS ST. JOHN THE BAPTIST
  note: 'Page 1 masthead of the 25 October 2026 issue: ''HOLY FAMILY PARISH / OCTOBER 25, 2026 | 30TH
    SUNDAY IN ORDINARY TIME'', with the four churches'' addresses (387 Maryland Ave., Oakmont; 444 Holy
    Family Way, Plum; 2000 O''Block Road, Plum; 825 Second Street, Verona) and ''Website: www.holyfamilypgh.org''.
    The text layer interleaves the four church headings.'
- url: https://parishesonline.com/organization/holy-family-parish-opv
  seen: 2026-10-23
  note: 'probe po: org ''Holy Family Parish'', 444 Holy Family Way, Pittsburgh 15239, lpi 0018000000Qx7r6AAB,
    container 14/1224, issues 2026-10-25 and 10-18 (and earlier). No other ParishesOnline org names any
    of the four churches (lpi-catholic.tsv lists no St. Irenaeus, St. John the Baptist, St. Joseph or
    Our Lady of Joy org for Plum/Oakmont/Verona).'
- url: https://www.holyfamilypgh.org/holyfamily-bulletins
  seen: 2026-10-23
  note: 'Rendered in headed Chrome (visit.py --bulletin / --links). Site is eCatholic 24616 (probe url
    alone answers 403). Its Bulletins page links PDFs named ''October 25 2026 FROM LPI.pdf'', ''October
    18 2026 FROM LPI-1.pdf'' ... under files.ecatholic.com/24616/documents/2026/10/. I downloaded the
    25 October file and the container file: 20 pages each, identical text on pages 1-2 (different bytes,
    25.30 MB vs 25.33 MB). Same bulletin reposted, not a second publication.'
- url: https://diopitt.org/holy-family-parish
  seen: 2026-10-23
  note: 'Diocese parish page (headed Chrome): Holy Family Parish, Rev. Daniel J. D''Antonio (Administrator),
    phone 412-793-4511, four churches in the weekend-schedule table (St. Irenaeus, St. John the Baptist,
    St. Joseph, Our Lady of Joy).'
promoted: 2026-10-23
bulletin_status: available
---

## Publisher

Holy Family Parish (Oakmont, Plum and Verona), formed 2020-07-01 from St. Irenaeus (Oakmont), St. Januarius, St. John the Baptist and Our Lady of Joy (Plum) and St. Joseph (Verona), publishes one weekly bulletin on ParishesOnline container 14/1224 (org `holy-family-parish-opv`). The 25 October 2026 issue (read 2026-10-23, two days ahead of its date) is headed "HOLY FAMILY PARISH" and prints one Mass list for four churches (see the evidence). The parish site holyfamilypgh.org (eCatholic 24616) reposts each issue as "<date> FROM LPI.pdf": I compared the 25 October file with the container file and pages 1-2 are identical text, so `ecatholic:24616` is recorded as the same bulletin. The diocese gives one pastor-administrator (Rev. Daniel J. D'Antonio) and one phone, 412-793-4511, for all four churches.

## Worship sites

Four churches, each with Mass in the 25 October bulletin: St. Irenaeus (Oakmont), St. John the Baptist (Plum), St. Joseph (Verona), Our Lady of Joy (Plum). Ruled out: St. Januarius, 1450 Renton Rd., Plum (GCatholic 24306), closed 2024-09-23, see excluded/st-januarius-plum.md; the bulletin's Mass list does not name it. Disagreement on the Spanish Mass: the bulletin says 2:00 PM on the last Sunday of the month, the diocese directory says 4:00 PM; the bulletin is followed.

## Website and bulletin provider

holyfamilypgh.org is diocese-provided eCatholic (24616) behind Cloudflare (probe url 403; read with headed Chrome). Its Bulletins page carries the ParishesOnline issues, so fetch reads the container by `provider_id`. The bulletin has a text layer in the issue read.

## Not yet confirmed

Nothing outstanding for the row. Weekday Masses other than Tuesday 8:30 AM at Our Lady of Joy were not extracted from page 2 (the text layer is truncated around the Confession list); the pipeline reads the full page.
