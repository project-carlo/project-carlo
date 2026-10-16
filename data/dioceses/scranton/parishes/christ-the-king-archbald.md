---
name: Christ the King Parish
website: https://christthekingpa.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/257
publication: ['url:https://www.church-bulletin.org/christ-the-king-parish-archbald-pa-18403']
group: Christ the King Parish
evidence:
- url: https://www.church-bulletin.org/bulletin/christ-the-king-parish-archbald-pa-18403/2026-10-18.pdf
  seen: 2026-10-16
  note: 'Page 1 of the 18 October 2026 issue (the whole PDF is scanned images with no text layer;
    read rendered). Masthead "Christ the King Parish"; SUNDAY MASS TIMES "Saturday Vigil: 4:00pm
    (St. Thomas Aquinas) / Sunday: 7:30am (St. Mary of Czestochowa) 9:00am (St. Thomas Aquinas)
    10:30am (St. Thomas Aquinas)"; "All daily Masses & Adoration at St. Thomas Aquinas Church";
    footer gives ST. THOMAS AQUINAS CHURCH, 429 Church Street, Archbald and ST. MARY OF
    CZESTOCHOWA CHURCH, 417 Main Street, Eynon. No third church.'
- url: https://www.church-bulletin.org/bulletin/christ-the-king-parish-archbald-pa-18403/2026-06-07.pdf
  seen: 2026-10-16
  note: 'Page 1 of the 7 June 2026 issue (image; read rendered) still names three churches:
    St. Thomas Aquinas Church, St. Mary of Czestochowa Church, Sacred Heart of Mary Church. The
    October issue has dropped Sacred Heart of Mary (closed 7 June 2026, see excluded/).'
- url: https://www.church-bulletin.org/christ-the-king-parish-archbald-pa-18403
  seen: 2026-10-16
  quote: Christ the King Parish Archbald, PA 18403
  note: John Patrick Publishing's listing for the parish (church-bulletin.org/?id=257 and
    church-bulletin.org/257 land here). Weekly PDFs at /bulletin/christ-the-king-parish-archbald-pa-18403/YYYY-MM-DD.pdf,
    newest 18 October 2026, archive back to October 2024.
- url: https://christthekingpa.org/
  seen: 2026-10-16
  note: The parish homepage (WordPress). probe url found its bulletin link https://church-bulletin.org/?id=257
    and the relegation notice for Sacred Heart of Mary Church, Jermyn.
---

## Publisher

Christ the King Parish (Archbald) publishes one weekly bulletin through John Patrick
Publishing (church-bulletin.org). I read the 18 October 2026 issue: its page-1 masthead is
"Christ the King Parish", with one weekend schedule (Saturday 4:00 pm and Sunday 9:00 and
10:30 am at St. Thomas Aquinas, Sunday 7:30 am at St. Mary of Czestochowa) and all weekday
Masses at St. Thomas Aquinas. The diocesan finder lists Christ the King as one canonical
parish with these two worship sites. The whole PDF is scanned images; read rendered.

Christ the King's pastor also led the former Sacred Hearts of Jesus and Mary Parish, Jermyn
(the site links a 24 September 2023 letter from Bishop Bambera "to Christ the King Parish &
Sacred Hearts of Jesus and Mary Parish"); by 2026 Jermyn's Sacred Heart of Mary church was
one of Christ the King's own "secondary worship sites" (relegation notice, February 2026), so
there is no separate Jermyn bulletin to look for.

## Worship sites

- St. Thomas Aquinas, 429 Church Street, Archbald (`st-thomas-aquinas-archbald`).
- St. Mary of Czestochowa, 417 Main Street, Eynon (`st-mary-of-czestochowa-eynon`).

Ruled out: Sacred Heart of Mary, 624 Madison Avenue, Jermyn (GCatholic 23984), closed with a
Closing Mass on 7 June 2026 by the bishop's decree of 18 February 2026; see
`excluded/sacred-heart-of-mary-jermyn.md`.

## Website and bulletin provider

christthekingpa.org is the parish's own site and links its bulletin as
https://church-bulletin.org/?id=257, which lands on the John Patrick Publishing listing
recorded in `publication`. Provider `other`, with the recipe `page-pdfs
https://church-bulletin.org/257` (the same form as Syracuse's Christ the Good Shepherd,
Oswego, which fetch:check verified for this publisher). fetch:check reads only the live
CSV, so this recipe has not been run for this row; check it after promotion. The bulletin is
image-only (no text layer in the 4, 11 or 18 October 2026 issues), so the pipeline has to
read it as images.

A ParishesOnline organization `christ-the-king-18403` (lpi 0018000000Qx8JZAAZ) exists but
has no publications; it is not this bulletin and is not recorded.

## Not yet confirmed

The fetch recipe has not been run (see above); run `pnpm fetch:check -- --parish
christ-the-king-archbald` after promotion.
