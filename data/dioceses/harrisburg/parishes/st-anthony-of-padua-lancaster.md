---
name: St. Anthony of Padua Church
website: https://www.stanthonylancaster.com/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:32688']
group: ''
evidence:
- url: https://files.ecatholic.com/32688/bulletins/20261018.pdf
  seen: 2026-10-20
  note: 'Image-only issue (8 pages, no text layer), read rendered (render.py). Page 1: "October 18, 2026
    - Twenty-ninth Sunday in Ordinary Time ... St. Anthony of Padua Church, 501 East Orange Street, Lancaster,
    Pennsylvania 17602 ... Fr. Luis Rodriguez, Pastor; Fr. Kevin Key, Parochial Vicar ... Sunday Mass
    Schedule: Saturday evening: 5:00 p.m. English; Sunday morning: 9:00 a.m. English, 11:00 a.m. Spanish.
    Weekday Mass Schedule: Tuesday-Saturday: 8:00 a.m.". Page 2 "A message from the pastor".'
- url: https://stanthonylancaster.com/bulletins
  seen: 2026-10-20
  note: 'Behind Cloudflare (visit.py challenged on every load on 19 October, through on the first load
    on 20 October). eCatholic bulletins page: "October 18, 2026" -> files.ecatholic.com/32688/bulletins/20261018.pdf,
    one issue per Sunday back to May 2026 and earlier.'
- url: https://sanjuanbautistalancaster.com/s/Bishop-Letter-May-2026-3.pdf
  seen: 2026-10-19
  note: 'Image-only letter of Bishop Senior, 23 May 2026, to St. Anthony''s parishioners: one pastor for
    St. Anthony and San Juan Bautista from 20-21 June 2026; "For the present, both parishes will remain
    proper canonical parishes".'
- url: https://discovermass.com/church/st-anthony-of-padua-church-lancaster-pa/
  seen: 2026-10-19
  note: Discover Mass page with no bulletins listed (issues.py); LPi organization st-anthony-of-padua-church-17602
    also has none.
promoted: 2026-10-20
---

## Publisher

St. Anthony of Padua Church, 501 East Orange Street, Lancaster, publishes its own weekly
bulletin on its eCatholic site. The 18 October 2026 issue (image-only, read rendered on 20
October) has the page 1 masthead "St. Anthony of Padua Church, 501 East Orange Street,
Lancaster, Pennsylvania 17602", Fr. Luis Rodriguez pastor and Fr. Kevin Key parochial vicar,
and its own Mass schedule: Saturday 5:00 p.m. (English); Sunday 9:00 a.m. (English) and 11:00
a.m. (Spanish); weekdays Tuesday-Saturday 8:00 a.m.

Since 20-21 June 2026 St. Anthony shares its pastor and vicar with San Juan Bautista (Bishop
Senior's letter of 23 May 2026), but each parish still prints its own bulletin: San Juan's 18
October issue never mentions St. Anthony, and this one is St. Anthony's alone. Two rows,
`group` left empty as for the other shared-pastor pairs.

## Worship sites

One church, `st-anthony-of-padua-lancaster`.

## Website and bulletin provider

`ecatholic`, website https://www.stanthonylancaster.com/ (directory and GCatholic),
publication `ecatholic:32688`, from the bulletins page's file links. Behind Cloudflare; the PDFs
on files.ecatholic.com fetch without a browser. **Image-only bulletin:** the 18 October issue
has no text layer, so the pipeline must read it as an image.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows, under xvfb-run with Chrome): ok, picked files.ecatholic.com/32688/bulletins/20261018.pdf, this week's bulletin. The resolver got past the site's Cloudflare where plain curl could not.

## Not yet confirmed

Whether St. Anthony and San Juan Bautista later merge their bulletins.
