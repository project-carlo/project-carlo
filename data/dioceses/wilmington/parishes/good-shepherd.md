---
name: Good Shepherd
website: https://www.goodshepherdcecilmd.org/
bulletin_provider: other
provider_id: page-pdfs http://fataonline.com/bulletins/GoodShepherdPerryville
publication: ['url:https://www.fataonline.com/bulletins/GoodShepherdPerryville']
group: Iron Hill Deanery
evidence:
- url: https://fataonline.com/bulletin/bulletin-591792610031.pdf
  seen: 2026-10-27
  quote: Thirtieth Sunday Ordinary Time October 24 & 25, 2026
  note: 'Newest issue on the FATA Online page (10 pages, text layer; the file name''s number is a Unix
    time of 2026-10-25). Page 1, an image-labelled cover: ''GOOD SHEPHERD PARISH / IRON HILL DEANERY,
    810 Aiken Ave., Perryville, MD'' with four church panels: Good Shepherd Church, Perryville (Saturday
    Evening Mass 4 p.m.; Sunday 12 Noon; Tuesday-Thursday 9 a.m.), St. Agnes, Rising Sun (Sunday 10 a.m.),
    St. Teresa of Avila, Port Deposit (Sunday 8:00 a.m.) and St. Patrick Chapel, Pilottown, Maryland (Mass:
    As Announced). Text layer: ''Pastor: Rev. Jay R. McKee''; ''Trustee for St. Agnes: Bud McFadden'';
    ''Trustee for St. Teresa: Anne Fazio''. Page 3 calendar: ''8:00 am Mass St. T'', ''10:00 am Mass St.
    A''. One bulletin, one parish masthead, no other parish named.'
- url: https://www.fataonline.com/bulletins/GoodShepherdPerryville
  seen: 2026-10-27
  note: 'FATA Online listing for the parish (probe url: 15 dated PDFs, newest 2026-10-25, then 14 October,
    7 October, 30 September ... 29 July at one-week steps). Linked as ''Bulletins'' from the parish home
    page. Issues of 14 October back to 29 July 2026 all carry the Good Shepherd Parish masthead.'
- url: https://www.goodshepherdcecilmd.org/
  seen: 2026-10-27
  quote: 'Good Shepherd Parish serves four churches in western Cecil County, Maryland:'
  note: Home page, read in the browser (probe url gets 200 but curl gets a Cloudflare challenge on inner
    pages). Continues 'Good Shepherd in Perryville, St. Agnes in Rising Sun, St. Teresa in Port Deposit,
    and our mission church, St. Patrick in Pilottown.' eCatholic site 17337; its Bulletins button goes
    to fataonline.com/bulletins/GoodShepherdPerryville, so the eCatholic site hosts no bulletin files.
promoted: 2026-10-27
---

## Publisher

Good Shepherd Parish, Perryville, publishes one weekly bulletin through FATA Online (fataonline.com/bulletins/GoodShepherdPerryville). The 25 October 2026 issue (Thirtieth Sunday in Ordinary Time, October 24 & 25) is headed 'Good Shepherd Parish / Iron Hill Deanery', names Rev. Jay R. McKee as pastor and shows four church panels on page 1. The cover's Mass boxes are in the image layer; the text layer holds the times without the church names, so the panels were read from a render of page 1.

## Worship sites

Four churches, all in the one bulletin: Good Shepherd, Perryville (831 Aiken Ave.); St. Agnes, Rising Sun (150 S. Queen St.); St. Teresa, Port Deposit (162 N. Main St.); and St. Patrick Chapel, Pilottown/Conowingo (237 Pleasant Grove Rd.), the 'mission church' of the home page. The parish site's Church Addresses page lists the same four and says of St. Patrick Chapel: 'Scheduled Masses throughout the year'. The directory (cdow.org) and GCatholic list all four on this site, so the eight roster entries (directory 152/154/158/160, GCatholic 19364/19366/19369/19371) are these four churches. The parish office is at 810 Aiken Ave., next to the school (800 Aiken Ave.); neither is a Mass site.

St. Patrick's Mass is not weekly. The weekly schedule on the bulletin cover says 'As Announced'; the 3 and 9 September 2026 issues announce the chapel's annual Mass on Saturday 12 September 2026 at 10 AM and the site says 'Scheduled Masses throughout the year'. The directory's 'Sat 10:00' for the chapel matches that annual Mass, not a weekly one. See the church record.

## Website and bulletin provider

`other`, with `page-pdfs http://fataonline.com/bulletins/GoodShepherdPerryville` (the pattern the Harrisburg FATA parishes use). The website is the eCatholic home page (goodshepherdcecilmd.org, id 17337) but its eCatholic file store holds no bulletins. `pnpm fetch:check --diocese wilmington --parish good-shepherd` (2026-10-27): picked https://www.fataonline.com/bulletin/bulletin-591792610031.pdf (first-listed, the 25 October issue read above); transport ok, document type PDF, identity and issue date reported unverified/unknown by the tool (the file name carries no date), so overall `unverified`. The identity and date come from the cover read above, which names Good Shepherd Parish and 24-25 October 2026, two days before the check.

## Not yet confirmed

St. Patrick Chapel's dates beyond the annual 12 September Mass; whether it has any other scheduled Mass. The St. Agnes Saturday 7 p.m. Spanish Mass the directory lists is not in the bulletin or on the parish Mass Times page (see the St. Agnes record).
