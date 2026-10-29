---
name: Holy Angels Korean Catholic Church
website: https://www.philaholyangels.org
bulletin_provider: other
provider_id: page-pdfs https://www.philaholyangels.org/5145248372.html filename=*26*
publication: ['url:https://www.philaholyangels.org/5145248372.html']
group: ''
evidence:
- url: https://www.philaholyangels.org/uploads/5/5/7/9/5579625/10-25-26.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (4 pages, text layer, in Korean): masthead ''주보 제 2026-1598호, 2026년 10월
    25일, 연중 제30주일, 천주교 필라델피아 한인성당, Holy Angels Parish of Archdiocese of Philadelphia, www.philaholyangels.org,
    7000 Old York Road, Philadelphia, PA 19126, 사무실 (215) 927-1662''; pastor 김순진(요셉) (Rev. Joseph Soon-Jin
    Kim). Mass box: Weekday PM 8:00 (Tuesday, Thursday); Saturday PM 8:00; Sunday AM 7:00, 10:00. No other
    church named.'
- url: https://www.philaholyangels.org/5145248372.html
  seen: 2026-10-29
  note: 'The site''s 주보 (bulletin) page, a Weebly page that lists /uploads/5/5/7/9/5579625/<M-D-YY>.pdf
    links newest first: 10-25-26, 10-18-26, 10-11-26, 10-4-26__1_, 9-27-2026 ... back to 2012.'
- url: https://www.philaholyangels.org/
  seen: 2026-10-29
  quote: Holy Angels Korean Catholic Church of Philadelphia
  note: 'Home page, Korean Mass notice: Sunday 7 AM, 10 AM, 11:30 AM (Sunday school Mass), 5 PM (young
    adult Mass); Saturday vigil 8 PM; weekdays Tuesday and Thursday 8 PM.'
- url: https://archphila.org/parish/holy-angels-philadelphia/
  seen: 2026-10-28
  quote: Rev. Joseph Soon-Jin Kim (Parochial Administrator)
  note: 'Directory page (updated 1 year before): 7000 Old York Rd. 19126, website philaholyangels.org,
    all Masses in Korean; the 11:30 AM and 5 PM Sunday Masses it lists the site also gives, the 25 October
    bulletin box shows only 7 and 10 AM.'
bulletin_status: available
---

## Publisher

Holy Angels (Korean) publishes its own weekly PDF bulletin in Korean on its Weebly site (page `5145248372.html`, newest first). It has no John Patrick listing (none for 19126 in `raw/jppc-pa.json`). Row: `other`, `page-pdfs` on that page, with `filename=*26*`.

## Why the filename filter

The page links about 760 PDFs back to 2012, many misnamed, and `page-pdfs` took `2017_11-02.pdf` (titled '2017-11-5.pdf' on the page), which its date reader reads as 2 November 2026, over the real 25 October issue. `filename=*26*` keeps names holding '26' (`10-25-26.pdf`, `9-27-2026.pdf`) and drops that file; it works only for 2026 files, so the filter needs changing in January 2027 (`*27*`) or if the site renames its files.

## Worship sites

One church, 7000 Old York Rd. The directory and the site's notice add Sunday 11:30 AM and 5 PM Masses that the 25 October bulletin's Mass box does not show; the box and site agree on Sunday 7 and 10 AM, Saturday 8 PM and Tuesday/Thursday 8 PM.

## Fetch check

`fetch:check` (2026-10-29) with the filter picked `10-25-26.pdf`: transport ok, PDF, fresh; identity `unverified` (no expected identity supplied; the masthead read above is Holy Angels Parish, 7000 Old York Road). Without the filter it picked the 2017 file.
