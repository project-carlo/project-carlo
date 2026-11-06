---
name: Immaculate Conception, Norwood
website: https://iccnorwood.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:6955']
group: ''
evidence:
- url: https://files.ecatholic.com/6955/bulletins/20261025.pdf
  seen: 2026-11-03
  note: '25 October 2026 issue, image-only (no text layer), pages 1-2 rendered with render.py. Page 1
    cover: ''Welcome To The Catholic Parish Family Of Immaculate Conception Church 211 Summit Street,
    Norwood, NJ 07648'', ''Thirtieth Sunday In Ordinary Time October 25, 2026'', ''Parish Office 201-768-1600''.
    Page 2: ''SERVED BY Fr. Doroteo Layosa MA.M.Div Pastor''; Mass Intentions Saturday 5:00pm, Sunday
    8:00am, 10:00am, 12:00pm; weekdays 8:00am.'
- url: https://iccnorwood.org/bulletins
  seen: 2026-11-03
  note: 'eCatholic bulletin page (probe get 403; read with visit.py): newest link ''October 25, 2026''
    files.ecatholic.com/6955/bulletins/20261025.pdf, then October 18, October 11 ...; issues.py found
    no 1 November issue (403).'
bulletin_status: available
---

## Publisher

Immaculate Conception, Norwood, publishes its own weekly bulletin on its eCatholic site (ecatholic:6955). The newest issue on 3 November 2026 is 25 October 2026; it is image-only, so I rendered pages 1-2. The cover reads 'Welcome To The Catholic Parish Family Of Immaculate Conception Church 211 Summit Street, Norwood, NJ 07648'; page 2 names Fr. Doroteo Layosa, Pastor. No other parish is named.

## Worship sites

- Immaculate Conception Church, 211 Summit Street (`immaculate-conception-norwood`): page 2 Mass intentions Saturday 5:00pm; Sunday 8:00am, 10:00am, 12:00pm; weekdays 8:00am.

The directory (156) and GCatholic (18521) list only this church.

## Website and bulletin provider

https://iccnorwood.org/ is an eCatholic site behind Cloudflare (`probe get` 403; `visit.py` loads it). Its /bulletins page lists Sunday-dated files.ecatholic.com/6955 issues. Provider `ecatholic`. The issues have no text layer: the pipeline has to read them as images, and `recheck` can't find quotes in them, so they are cited by note.

Fetch check (2026-11-03, headed): transport ok, PDF, picked `files.ecatholic.com/6955/bulletins/20261025.pdf`, the 25 October 2026 issue read above, the newest posted; freshness fresh (9 days). Publication identity `unverified` in the check; the rendered cover confirms it.

## Not yet confirmed

The 1 November issue was not posted by 3 November; the parish posts late some weeks. Nothing else open.
