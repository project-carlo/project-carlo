---
name: Our Lady of Lourdes
website: https://ollourdespaterson.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:11325']
group: ''
evidence:
- url: https://files.ecatholic.com/11325/bulletins/20261101.pdf
  seen: 2026-11-05
  quote: 440 River Street, Paterson, NJ 07524
  note: 'Page 1 masthead of the 1 November 2026 issue (4 pages, text layer): ''OUR LADY OF LOURDES'',
    ''Rev. Raimundo Rivera, Pastor'', ''SOLEMNIDAD DE TODOS LOS SANTOS | SOLEMNITY OF ALL SAINTS''; Sunday
    Mass: Saturday 7:00 pm Espanol; Sundays 9:00 am Espanol, 11:00 am English, 12:30 pm Espanol; daily
    Mass 7:00 pm Espanol. Page 4 footer: ''6059 Our Lady of Lourdes, Paterson, NJ John Patrick Publishing
    Company''. Names no other church.'
- url: https://ollourdespaterson.org/bulletins
  seen: 2026-11-05
  note: Read with parish-site-access visit.py (probe url gets 403). eCatholic site 11325; the 2026 list
    runs from 'November 1, 2026' back to 'January 4, 2026', linking files.ecatholic.com/11325/bulletins/
    files.
- url: https://church-bulletin.org/?id=6059
  seen: 2026-11-05
  note: 'probe get: redirects to https://www.church-bulletin.org/nuestra-senora-de-lourdes-our-lady-of-lourdes-paterson-nj-07524,
    John Patrick Publishing''s listing of the same bulletin (newest 2026-11-01.pdf). The parish site does
    not link it.'
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: Finder pin directory:11325 'Our Lady of Lourdes, Paterson', 440 River Street, Paterson 07524,
    website https://ollourdespaterson.org/; Sunday 9:00 AM Spanish, 11:00 AM English, 12:30 PM Spanish;
    Monday-Saturday 7:00 PM Spanish.
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

Our Lady of Lourdes, Paterson prints its weekly bulletin with John Patrick Publishing (footer "6059 Our Lady of Lourdes, Paterson, NJ") and posts each issue on its eCatholic site. The 1 November 2026 issue (`https://files.ecatholic.com/11325/bulletins/20261101.pdf`, read 2026-11-05 with `probe pdf`) has the masthead "OUR LADY OF LOURDES 440 River Street, Paterson, NJ 07524 Rev. Raimundo Rivera, Pastor". It names no other parish.

## Worship sites

- `our-lady-of-lourdes-paterson`: page 1 gives Saturday 7:00 pm (Spanish), Sunday 9:00 am (Spanish), 11:00 am (English) and 12:30 pm (Spanish), and daily Mass at 7:00 pm (Spanish).

The issue names no other place of Mass. The finder (directory:11325) and GCatholic (19048) list this one church. GCatholic's website for it, `miracleoflourdes.org`, does not resolve (probe url DEAD-DNS, 2026-11-05).

## Website and bulletin provider

`https://ollourdespaterson.org/` (the finder's website) is the eCatholic site 11325, behind Cloudflare: `probe url` gets 403 and `visit.py` loads it. Its Bulletins page lists the 2026 issues up to 1 November 2026, and `issues.py ecatholic ecatholic:11325` found `20261101.pdf` (8 November not yet posted on 2026-11-05). Provider `ecatholic`, publication `ecatholic:11325`; `fetch:check` on 2026-11-05 picked `https://files.ecatholic.com/11325/bulletins/20261101.pdf` (freshness `fresh`, age 4 days; identity reported "unverified", "No expected identity supplied"; the masthead was checked by hand above). John Patrick also lists the same issues at `https://www.church-bulletin.org/nuestra-senora-de-lourdes-our-lady-of-lourdes-paterson-nj-07524` (reached from `church-bulletin.org/?id=6059`), which is a fallback if the eCatholic posting stops.

## Not yet confirmed

Nothing open.
