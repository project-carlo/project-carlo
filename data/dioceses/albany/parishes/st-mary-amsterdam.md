---
name: St. Mary's Church
website: https://stmarysamsterdam.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:33341']
group: ''
evidence:
- url: https://files.ecatholic.com/33341/bulletins/20260927.pdf
  seen: 2026-09-28
  quote: ST. MARY'S CHURCH 156 EAST MAIN STREET AMSTERDAM NY 12010
  note: 'Masthead, page 1 of the 27 September 2026 issue. The whole issue is scanned images (no text layer):
    read by rendering page 1 (parish-site-access render.py), so recheck cannot find the quote. The page''s
    Mass schedule: ''Daily Mass – Monday-Friday 8 am … Saturday Vigil Mass – 4 pm … Sunday Mass – 10 am
    & 12 pm Spanish'', then ''St. Stephen''s Church, Hagaman Saturday 5:30 pm Sunday 8 am''; clergy Father
    Nathaniel Resila, Pastor.'
- url: https://stmarysamsterdam.org/bulletins
  seen: 2026-09-28
  note: 'The parish''s eCatholic site (behind Cloudflare; read with parish-site-access visit.py --bulletin
    on 2026-09-28, loaded on the 3rd try). Embeds eCatholic site id 33341; issues are files.ecatholic.com/33341/bulletins/YYYYMMDD.pdf,
    newest 20260927 (20261004 not yet up: 403).'
- url: https://www.rcda.org/parishes/parish/st-marys-church-amsterdam-ny
  seen: 2026-09-28
  quote: 'Sunday: 12:00 pm (Spanish Mass)'
  note: 'Diocese''s Find A Parish page: website stmarysamsterdam.org, no ''Other Worship Sites''.'
promoted: 2026-09-28
---

## Publisher

St. Mary's Church, Amsterdam publishes its own weekly bulletin on its eCatholic site
(`ecatholic:33341`). The 27 September 2026 issue's cover (page 1, an image) is headed "ST.
MARY'S CHURCH, 156 East Main Street Amsterdam NY 12010" with its own Mass schedule (weekdays
8 am, Saturday 4 pm, Sunday 10 am and 12 pm in Spanish).

The same cover also prints the weekend times of **St. Stephen's Church, Hagaman** (Saturday
5:30 pm, Sunday 8 am): the two parishes share a pastor (Fr. Nathaniel Resila), and the
weekday 8 am Mass at St. Mary's serves both. But St. Stephen's publishes its own bulletin on
ParishesOnline (container 03/1004, current to 27 September 2026, its own masthead "ST.
STEPHEN'S PARISH, 51 Pawling Street"). Two live channels, so two rows: St. Stephen is a church
of `st-stephen-hagaman`, not of this row. The same pastor also has St. Cecilia, Fonda and
Sacred Heart, Tribes Hill, which publish a third bulletin (`st-cecilia-sacred-heart-fonda`).

## Worship sites

One: `st-mary-amsterdam` (156 E. Main St.). The diocese's page for St. Mary's lists no other
worship sites. The Institutional Records index lists St. Mary's Church as holding the records
of St. Casimir's, Amsterdam, a closed parish; its building is not in either roster and was
not researched (see the region notes).

The Sunday 12 pm Mass is in Spanish; the diocese's separate "Spanish Apostolate" directory
entry (directory:445, no address) is not linked here since nothing ties it to this church
specifically.

## Website and bulletin provider

stmarysamsterdam.org is the site the diocese lists and the bulletin cover prints. It is
eCatholic behind Cloudflare (`probe url`: HTTP 403); visit.py read it and found site id 33341,
whose `/bulletins` page lists the weekly PDFs at `files.ecatholic.com/33341/bulletins/<Sunday>.pdf`.

**Image-only:** the 20 and 27 September 2026 issues have no text layer at all (probe pdf:
0 readable pages of 5). The pipeline will need to read this bulletin as images.

## Not yet confirmed

Nothing about the structure. Whether St. Casimir's building still exists or holds Mass was
not checked (it is in no roster).
