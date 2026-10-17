---
name: St. Elizabeth Ann Seton Parish
website: https://www.setonpa.com
bulletin_provider: other
provider_id: page-pdfs https://www.setonpa.com/seton-sentinel-archives
publication: ['url:https://www.setonpa.com/seton-sentinel-archives']
group: Saint Elizabeth Ann Seton Parish
evidence:
- url: https://www.setonpa.com/_files/ugd/160730_80dc95dc23914bed9e21760f1f57e7b6.pdf
  seen: 2026-10-16
  quote: 'No Mass on Wednesday'
  note: 'Page 1 of the 18 October 2026 "Seton Sentinel": St. Elizabeth Ann Seton, 116 Hughes Street, Swoyersville; Monday, Tuesday, Thursday & Friday 8:00am, Saturday 4:00pm (vigil), Sundays 8:30am, 11:00am & 5:30pm.'
- url: https://www.setonpa.com/_files/ugd/160730_80dc95dc23914bed9e21760f1f57e7b6.pdf
  seen: 2026-10-16
  quote: 'St. Elizabeth Ann Seton, Pray for us!'
  note: 'Page 2: Mass intentions for 19-25 October at the same times; no other church named.'
- url: https://www.setonpa.com
  seen: 2026-10-16
  note: 'Parish homepage (Wix; read in a browser): link "SETON SENTINEL" to the current issue (a /_files/ugd/160730_<hash>.pdf file) and "SETON SENTINEL ARCHIVES" to /seton-sentinel-archives.'
---

## Publisher

St. Elizabeth Ann Seton Parish, Swoyersville publishes its own weekly bulletin, the "Seton
Sentinel", on its website. The 18 October 2026 issue (page 1) names the parish alone, 116 Hughes
Street, with Monday, Tuesday, Thursday and Friday 8 am ("No Mass on Wednesday"), Saturday 4 pm and
Sunday 8:30 am, 11 am and 5:30 pm; page 2 lists the week's intentions at those times. Pastor: Fr.
Chmil.

## Worship sites

One: `holy-trinity-swoyersville`, Holy Trinity Church at 116 Hughes Street, the finder's only worship
site for the parish. The diocese's consolidated-parishes list gives Holy Name of Jesus, Swoyersville
as closed in 1996 (in no roster here). St. Nicholas, 271 Tripp St., Swoyersville, which GCatholic
lists, is a Ruthenian (Byzantine) church: `excluded/st-nicholas-swoyersville.md`.

## Website and bulletin provider

setonpa.com is the finder's website for the parish. Its homepage links the current issue as "SETON
SENTINEL", a Wix file `/_files/ugd/160730_<hash>.pdf` whose name changes every week and carries no
date, and "SETON SENTINEL ARCHIVES" (`/seton-sentinel-archives`, several hundred PDF links).
`bulletin_provider: other` with no recipe: `fetch:check` reads only promoted rows. The resolver will
have to take the link titled SETON SENTINEL on the homepage (choose `titled`), not the newest of the
archive. St. Ignatius's Wix site uses the same Wix account (160730), but its bulletin is a different
publication (Bonventure).

`provider_id` pins the recipe `page-pdfs https://www.setonpa.com/seton-sentinel-archives`. Without it the resolver found no bulletin page from the homepage. With it, `fetch:check` on 2026-10-17 read the archive page ("page-pdfs on https://www.setonpa.com/seton-sentinel-archives: current").

## Not yet confirmed

Nothing about the fetch: the recipe above is pinned (2026-10-17).
