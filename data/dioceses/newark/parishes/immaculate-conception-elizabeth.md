---
name: Immaculate Conception, Elizabeth
website: https://ic-rcc.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6010
publication: ['url:https://www.church-bulletin.org/immaculate-conception-church-elizabeth-nj-07208']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/immaculate-conception-church-elizabeth-nj-07208/2026-11-08.pdf
  seen: 2026-11-05
  note: 'Image-only issue (no text layer; page 1 rendered, recheck cannot find it in text). Page 1 masthead:
    ''IMMACULATE CONCEPTION CHURCH'', ''Thirty-Second Sunday in Ordinary Time November 8, 2026'', ''PHONE:
    (908) 352 6662'', ''425 UNION AVE, ELIZABETH, NJ 07208 PARKING LOT (TRAILER)''. Schedule: Santa Misa
    Español Sábado 7:00 p.m., Domingo 9:00 a.m., 1:00 p.m. y 6:00 p.m., Martes 7:00 p.m.; Holy Mass English
    Sunday 11:00 a.m., Monday-Friday 12:15 p.m. No other church named.'
- url: https://church-bulletin.org/6010
  seen: 2026-11-05
  note: 'John Patrick listing: redirects to church-bulletin.org/immaculate-conception-church-elizabeth-nj-07208,
    ''Immaculate Conception Church Bulletin'', dated issues 2026-11-08, 11-01, 10-25, 10-18, 10-11. Found
    by grepping the Run''s saved JP scan (029-map/jp-6000-6200.tsv).'
- url: https://ic-rcc.org/
  seen: 2026-11-05
  quote: Aquí se publicarán los boletines de la parroquia.
  note: 'The parish''s Tithely site (directory website; visit.py --text): ''Visita la parroquia 425 Union
    Ave., Elizabeth, NJ 07208 Oficina en el tráiler del estacionamiento''; same Mass times as the bulletin.
    Its Boletín section posts no issues and links no publisher.'
bulletin_status: available
---

## Publisher

John Patrick Publishing prints the bulletin (listing 6010, church-bulletin.org/immaculate-conception-church-elizabeth-nj-07208). I read the 8 November 2026 issue: it is image-only, and the rendered page 1 reads "IMMACULATE CONCEPTION CHURCH ... November 8, 2026" with "425 UNION AVE, ELIZABETH, NJ 07208 PARKING LOT (TRAILER)" (the office) and the Mass schedule.

## Worship sites

One church, `immaculate-conception-elizabeth`: the page-1 schedule gives Spanish Masses Saturday 7:00pm, Sunday 9:00am, 1:00pm and 6:00pm, Tuesday 7:00pm, and English Masses Sunday 11:00am and Monday-Friday 12:15pm, naming no other place. GCatholic (18387) and the directory (30) list only this church.

Planning area K is not recorded as `group` (diocese.md *Sources*).

## Website and bulletin provider

The directory's https://ic-rcc.org/ (Tithely) is the current site; its bulletin section says bulletins will be posted there and links none. GCatholic's http://www.iconceptionparish.org answered HTTP 522 through Cloudflare on 2026-11-05 and is an older domain. The bulletin is read from the John Patrick listing: provider `other`, `page-pdfs https://church-bulletin.org/6010`. The issues are image-only; the pipeline will need to read them as images.

Fetch check (2026-11-05, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/6010: current` and picked .../immaculate-conception-church-elizabeth-nj-07208/2026-11-08.pdf, the 8 November 2026 issue read above (date observed in the document, "November 8, 2026"); freshness `future` (the coming Sunday). Identity `unverified` only because no expected identity is supplied; the masthead confirms it. The recipe is the one in `provider_id`.

## Not yet confirmed

Nothing open.
