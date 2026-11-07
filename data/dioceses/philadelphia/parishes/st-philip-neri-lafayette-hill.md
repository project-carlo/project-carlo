---
name: St. Philip Neri
website: https://www.saintphilipnerichurch.com
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-philip-neri-church-lafayette-hill-pa-19444
publication: ['url:https://www.church-bulletin.org/saint-philip-neri-church-lafayette-hill-pa-19444']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-philip-neri-church-lafayette-hill-pa-19444/2026-10-25.pdf
  seen: 2026-10-28
  quote: Parish Mass Schedule
  note: 'John Patrick listing 14, issue of 25 October 2026 (8 pages, text layer; the Sunday title prints
    garbled by font substitution). Page 1 masthead ''St. Philip Neri Church'', www.saintphilipnerichurch.com,
    Church Office 610-834-1975; Rev. George J. Szparagowski, Pastor; one ''Parish Mass Schedule'': Saturday
    vigil 5PM; Sunday 7:30AM (no music), 9:30AM and 11:00AM; Monday through Saturday 8:30AM; Holy Days
    6:30AM, 8:30AM and 7PM. No other church or chapel appears.'
- url: https://www.church-bulletin.org/saint-philip-neri-church-lafayette-hill-pa-19444
  seen: 2026-10-28
  quote: Latest Edition
  note: Listing 14 'Saint Philip Neri Church', Lafayette Hill, PA 19444; latest edition October 25, 2026.
- url: https://www.saintphilipnerichurch.com/bulletins/
  seen: 2026-10-28
  note: The parish's own Bulletins page (probe get HTTP 200) lists dated issues August 16 to October 25,
    2026, files shared/bulletins/2026/<mm>-<dd>-2026.pdf. The 10-25-2026.pdf file is byte-identical (md5
    ab8ad7dba775b1cfb229934737ac02d4) to the listing's 2026-10-25.pdf, so the two channels carry the same
    issue; the home page also links jppc.net/onlinebulletins/014template.pdf.
promoted: 2026-10-29
bulletin_status: available
---

## Publisher

St. Philip Neri, Lafayette Hill (Rev. George J. Szparagowski, Pastor) is a single-church parish with its own school. Its weekly bulletin is John Patrick Publishing's listing 14 ('Saint Philip Neri Church', Lafayette Hill, PA 19444). The 25 October 2026 issue is headed 'St. Philip Neri Church' with one Parish Mass Schedule. The parish's own site carries an archive of the same files: the 25 October 2026 PDF is byte-identical to the listing's (md5 equal), so either channel is current today.

## Website and bulletin provider

`other`, reading `page-pdfs` on the listing, which is the channel the home page's 'jppc.net/onlinebulletins/014template.pdf' link names and which cannot lag behind a parish upload. The parish's own `/bulletins/` page (dated files, newest listed last) is a second, equal channel; if the listing ever stops, switch the recipe to it.

## Fetch check

`fetch:check` (2026-10-28, headed Chrome) with the `page-pdfs` recipe on the listing picked `https://www.church-bulletin.org/bulletin/saint-philip-neri-church-lafayette-hill-pa-19444/2026-10-25.pdf`: transport ok, PDF, fresh (3 days); issue date inferred from the file name; identity `unverified` only because the check was given no expected identity (the masthead was read from the text layer, above). The check printed no separate recipe; the one in `provider_id` is the one used.
