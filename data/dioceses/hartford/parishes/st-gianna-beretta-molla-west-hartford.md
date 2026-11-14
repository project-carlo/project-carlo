---
name: Saint Gianna Parish
website: https://saintgiannaparish.org/bulletins/
bulletin_provider: parishes_online
provider_id: st-gianna-beretta-molla-06110
publication: ['po-org:st-gianna-beretta-molla-06110', 'lpi:0018000000Qx9TEAAZ', 'po-container:03/1398']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1398/20261115B.pdf
  seen: 2026-11-13
  note: 'Page 1 is an image (read by rendering it; pages 1-11 have no text layer): masthead "Saint Gianna
    Parish", Parish Office 1088 New Britain Avenue, West Hartford CT 06110; Daily Mass Mon-Wed 8:30 AM
    SB, Thu-Sat 8:30 AM SM; Saturday Vigil 4:00 PM SB; Sunday 8:30 AM (English) SB, 8:30 AM (Tieng Viet)
    SM, 10:30 AM (English) SM, 12:30 PM (Tieng Viet) SM; drawings captioned "Saint Brigid Church (SB)
    ... 1088 New Britain Avenue" and "Saint Mark the Evangelist Church (SM) ... 467 S Quaker Lan"; 33rd
    Sunday of Ordinary Time (15 November 2026).'
- url: https://saintgiannaparish.org/bulletins/
  seen: 2026-11-13
  note: Bulletins page embeds the ParishesOnline publication widget for id 0018000000Qx9TEAAZ and links
    parishesonline.com/organization/st-gianna-beretta-molla-06110.
- url: https://parishesonline.com/organization/st-gianna-beretta-molla-06110
  seen: 2026-11-13
  note: 'probe po: org ''St Gianna Beretta Molla'', 1088 New Britain Ave, West Hartford; container 03/1398,
    latest issue 15 November 2026.'
promoted: 2026-11-14
bulletin_status: available
---

## Publisher

Saint Gianna Beretta Molla Parish, West Hartford publishes one weekly bulletin through ParishesOnline (org `st-gianna-beretta-molla-06110`, LPi id 0018000000Qx9TEAAZ, container 03/1398); the parish site's Bulletins page embeds that org's widget. The 15 November 2026 issue's page 1 (an image, read by rendering it) has the masthead "Saint Gianna Parish", Parish Office 1088 New Britain Avenue, West Hartford, in English and Vietnamese.

## Worship sites

Two, both on page 1 of the 15 November 2026 issue with their addresses and Masses: Saint Brigid Church (SB), 1088 New Britain Avenue (Mon-Wed 8:30 AM, Saturday Vigil 4:00 PM, Sunday 8:30 AM English; `st-brigid-west-hartford`) and Saint Mark the Evangelist Church (SM), 467 S Quaker Lane (Thu-Sat 8:30 AM, Sunday 8:30 AM Vietnamese, 10:30 AM English, 12:30 PM Vietnamese; `st-mark-the-evangelist-west-hartford`). These are the directory's two churches of the parish (20, 14) and GCatholic's 22222 and 22224.

GCatholic also lists St. Helena, 30 Echo Lane (22223), the third church merged into St. Gianna in 2017. The bulletin schedules nothing there, and the building is now used by the St. Thomas Syro-Malabar church: see `excluded/st-helena-west-hartford` (other-jurisdiction). The Vietnamese Masses at Saint Mark are in Saint Gianna's own schedule; in 2021 the archbishop's letter (We-Ha, 8 January 2021) said the St. Andrew Dung-Lac quasi-parish leased St. Mark's, and no roster lists that quasi-parish separately now.

## Website and bulletin provider

`parishes_online`, org `st-gianna-beretta-molla-06110`. The issue is scanned: pages 1-11 of 12 have no text layer, so the pipeline must read it as images. The file is large (the 15 November issue is about 93 MB); the skill's render.py browser closed on it, and pdftoppm on a `probe get` download rendered it.

`fetch:check` on 2026-11-13 picked `03/1398/20261115B.pdf`, the 15 November 2026 issue.

## Not yet confirmed

Nothing open.
