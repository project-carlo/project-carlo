---
name: Church of the Holy Spirit
website: https://www.holyspiritstamford.org/bulletin
bulletin_provider: parishes_online
provider_id: holy-spirit-church-06903
publication: ['po-org:holy-spirit-church-06903', 'lpi:0018000000QxB07AAF', 'po-container:03/1409']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1409/20261115B.pdf
  seen: 2026-11-12
  note: 'Page 1 is an image (pages 1-7 have no text layer; rendered): ''The Roman Catholic Church of the
    Holy Spirit'', ''November 15, 2026 | Thirty-Third Sunday in Ordinary Time''. Weekend Masses Saturday
    8:30am and 5:15pm Vigil; Sunday 7:30am, 9:30am (Latin chant), 11:30am. Weekday Masses Monday-Wednesday
    7:30am, Friday 7:30am. Contact ''403 Scofieldtown Rd Stamford, CT 06903'', ''HolySpiritStamford.org''.'
- url: https://www.holyspiritstamford.org/bulletin
  seen: 2026-11-12
  note: Duda Bulletin page embeds the LPi publication widget 'parishesonline.com/publicationWidget?type=bulletin&color=gray&id=0018000000QxB07AAF'
    (found in the HTML saved with probe get --out).
- url: https://parishesonline.com/organization/holy-spirit-church-06903
  seen: 2026-11-12
  note: 'probe po: ''Church of the Holy Spirit'', 403 Scofieldtown Rd, Stamford, CT, 06903; LPi 0018000000QxB07AAF,
    container 03/1409; latest issue 2026-11-15.'
promoted: 2026-11-12
bulletin_status: available
---

## Publisher

The parish publishes a weekly LPi bulletin on ParishesOnline (org `holy-spirit-church-06903`, container 03/1409). The 15 November 2026 issue (`https://container.parishesonline.com/bulletins/03/1409/20261115B.pdf`, read 2026-11-12 by rendering page 1, which is an image) is headed "The Roman Catholic Church of the Holy Spirit", "November 15, 2026 | Thirty-Third Sunday in Ordinary Time", with contact "403 Scofieldtown Rd Stamford, CT 06903".

## Worship sites

- `holy-spirit-stamford`: Saturday 8:30am and 5:15pm Vigil; Sunday 7:30, 9:30 (Latin chant) and 11:30am; Monday-Wednesday and Friday 7:30am.

The page names no other church. The diocese's directory (directory:1433) and GCatholic (21957) list this one church.

## Website and bulletin provider

`holyspiritstamford.org` is a Duda site; its Bulletin page embeds the LPi publication widget for LPi id 0018000000QxB07AAF. Provider `parishes_online`, provider_id the org slug. The issue is image-only apart from page 8 (`probe pdf` reads one page of eight), so read the masthead and schedule by rendering page 1.

`fetch:check` on 2026-11-12 (headed Chrome) picked `https://container.parishesonline.com/bulletins/03/1409/20261115B.pdf`, the 15 November 2026 issue read above (issue date inferred 2026-11-15, freshness `future` because it was checked on the Thursday before; the PDF exceeds fetch:check's 25 MB inspection limit, so only its signature was checked).

## Not yet confirmed

Nothing open.
