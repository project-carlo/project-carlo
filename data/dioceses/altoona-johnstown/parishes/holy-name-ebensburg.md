---
name: Holy Name Parish, Ebensburg
website: https://www.holynameebg.org
bulletin_provider: parishes_online
provider_id: holy-name-church-15931
publication: ['po-org:holy-name-church-15931', 'lpi:0018000000QxAlVAAV', 'po-container:14/4019']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/4019/20261018B.pdf
  seen: '2026-10-21'
  note: 'ParishesOnline container 14/4019, issue of 18 Oct 2026 (12 pages, mostly images: only the footer "Holy Name Church | 14-4019" has a text layer, so `probe pdf --grep` finds nothing). Page 2, read from a render (pdftoppm), is headed "WELCOME! OCTOBER 18, 2026 | TWENTY-NINTH SUNDAY IN ORDINARY TIME" with PARISH STAFF "Fr. Brian L. Warchola, Pastor", "Mrs. Victoria Cornetti, Parish Manager 472-7244" and MASS INTENTIONS for Sat. Oct 24 4:00PM and Sun. Oct 25 7:45AM, 9:15AM, 10:30AM; weekdays Mon 8:00AM, Tue 6:30AM, Wed 6:30AM, Thu 8:00AM and 9:15AM on Fri. It names Holy Name alone. A "Masses offered by Franciscan Friars TOR, Loretto PA" box lists intentions, not a place.'
- url: https://parishesonline.com/organization/holy-name-church-15931
  seen: '2026-10-21'
  note: '`probe po holy-name-church-15931`: LPi 0018000000QxAlVAAV, "Holy Name Church", 500 N Julian St, Ebensburg, website holynameebg.org, container 14/4019, latest issue 2026-10-18 (the container already had the 25 Oct file when probed).'
- url: https://www.holynameebg.org
  seen: '2026-10-21'
  note: '`probe url` of the parish site finds the embedded publication id po-org:holy-name-church-15931.'
- url: https://discovermass.com/church/holy-name-ebensburg-pa/
  seen: '2026-10-21'
  quote: Shucks! There are no bulletins available.
  note: Discover Mass page for Holy Name, Ebensburg has an empty Bulletins tab; not a channel.
- url: https://www.dioceseaj.org/parishes/
  seen: '2026-10-21'
  note: 'Directory: Holy Name Parish, Ebensburg, 500 North Julian Street 15931, homepage holynameebg.org; Masses Sat 4:00 PM, Sun 7:45, 9:15 and 10:30 AM, Mon-Thu 8:00 AM, Fri 6:30 and 9:00 AM. The bulletin shows Tue/Wed 6:30 AM, Fri 9:15 AM intention times in the week of 19 Oct (intention times, which vary weekly).'
---

## Publisher

Holy Name Parish (pastor Fr. Brian L. Warchola, parish office 814-472-7244) publishes its own weekly bulletin through ParishesOnline, organization `holy-name-church-15931`, container 14/4019 (`probe po`, 2026-10-21; latest issue dated 18 Oct 2026). The issue's page 2 names Holy Name alone and its Mass intentions match the Mass times below. It is not shared with another parish. The parish's own site (`holynameebg.org`) embeds the same organization id.

## Worship sites

One: Holy Name, 500 N Julian St (see `churches/holy-name-ebensburg.md`). Nothing else is named in the bulletin.

## Website and bulletin provider

`parishes_online`, `provider_id: holy-name-church-15931`. `fetch:check` on 2026-10-21 picked `20261018B.pdf` (url_date 2026-10-18), status ok. The PDF is 12 image pages (38 MB), so text extraction later in the pipeline may need OCR; the fetch itself works.

## Not yet confirmed

Nothing blocking.
