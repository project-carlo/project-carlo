---
name: St. Mary, Nutley
website: https://stmarysnutley.org/
bulletin_provider: other
provider_id: dated-post https://stmarysnutley.org/category/bulletin-archive/
publication: ['url:https://stmarysnutley.org/category/bulletin-archive/']
group: ''
evidence:
- url: https://stmarysnutley.org/wp-content/uploads/2026/10/108-November-1-St-Marys-Final.pdf
  seen: 2026-11-03
  note: '1 November 2026 issue (11 pages, image only, rendered pages 1 and 11). Page 1 masthead: ''St.
    Mary''s Church of Nutley 17 Msgr. Owens Place Nutley, New Jersey 07110 973 235 1100 www.stmarysnutley.org'',
    ''Feast of All Saints Day'' ''November 1, 2026''. Page 11 ''Parish Weekend Mass Schedule'': Saturday
    Evenings 5:00PM; Sundays 7:30 AM, 10:00AM & 12 PM; Daily Mass Schedule Monday to Friday 8:00 AM, ''Parish
    Chapel-145 St. Mary''s Place unless noted''; Parish Office Address 145 St. Mary''s Place; pastor Very
    Rev. Thomas D. Nicastro. No other church is named and no publisher''s footer appears on pages 1 or
    11.'
- url: https://stmarysnutley.org/category/bulletin-archive/
  seen: 2026-11-03
  quote: Feast of All Saints
  note: The parish's WordPress 'Bulletin Archive' category lists one post per issue, newest '“Feast of
    All Saints” November 1, 2026', then October 25, 18, 11 …; each post (e.g. /feast-of-all-saints-november-1-2026/)
    embeds that week's PDF under wp-content/uploads/.
- url: https://church-bulletin.org/656
  seen: 2026-11-03
  note: John Patrick keeps a listing 'Saint Mary's Parish Bulletin' (saint-mary-s-parish-nutley-nj-07110,
    id 656) that shows only the week's readings and no issues; the parish posts its own bulletin instead.
bulletin_status: available
---

## Publisher

The parish publishes its own bulletin as a PDF on its WordPress site, one post per issue in the Bulletin Archive category. I read the 1 November 2026 issue (108-November-1-St-Marys-Final.pdf, 11 pages, image only; I rendered pages 1 and 11): the page-1 masthead reads "St. Mary's Church of Nutley 17 Msgr. Owens Place Nutley, New Jersey 07110" and "November 1, 2026". Neither page carries a printer's footer. John Patrick keeps a listing for the parish (church-bulletin.org/656) with no issues.

## Worship sites

One church, `st-mary-nutley`. Page 11's schedule gives Saturday 5:00pm and Sunday 7:30, 10:00am and noon, and weekday Masses at 8:00am in the "Parish Chapel-145 St. Mary's Place unless noted", which is also the parish office address. I took the chapel to be on the parish campus beside the church and gave it no church row (see *Not yet confirmed*). The directory (159) and GCatholic (18524) list only this church.

## Website and bulletin provider

The directory's https://stmarysnutley.org/ (WordPress). The archive page links each issue's post, not the PDF, so the row is pinned to the `dated-post` collector on the archive page. The issues are image only, so the pipeline needs OCR to read them.

Fetch check (2026-11-03, headed): ok. With `dated-post` on the archive page it picked 108-November-1-St-Marys-Final.pdf, fresh (date inferred from the post), identity `unverified`; that is the issue whose masthead I read.

## Not yet confirmed

Whether the parish chapel at 145 St. Mary's Place is on the church's grounds at 17 Msgr. Owens Place. If it is a separate building away from the church, it needs its own church row with the weekday Masses.
