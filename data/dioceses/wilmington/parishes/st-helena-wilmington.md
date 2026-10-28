---
name: St. Helena's Church
website: https://sainthelenas.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-helena-s-church-wilmington-de-19809
publication: ['url:https://www.church-bulletin.org/saint-helena-s-church-wilmington-de-19809']
group: Brandywine Hundred Deanery; pastor shared with Holy Child
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-helena-s-church-wilmington-de-19809/2026-10-25.pdf
  seen: 2026-10-27
  quote: ST. HELENA CHURCH
  note: 'Page 1 of the 25 October 2026 issue, masthead ''602 PHILADELPHIA PIKE, WILMINGTON, DELAWARE 19809'',
    for this parish alone. Staff list: ''Very Reverend Michael J Carrier, KHS, V.F.'' / ''Pastor & Dean
    ~ Brandywine Hundred Deanery'' and ''Reverend Sylvester Obumneme'' / ''Parochial Vicar''.'
- url: https://www.church-bulletin.org/bulletin/saint-helena-s-church-wilmington-de-19809/2026-10-25.pdf
  seen: 2026-10-27
  quote: Immaculate Heart of Mary, St. Helena, St. Joseph on the
  note: 'Page 3, ''From the desk of the pastor'': lists the seven parishes of the Brandywine Hundred Deanery.
    It is a deanery list, not a membership of this bulletin.'
- url: https://sainthelenas.org/
  seen: 2026-10-27
  note: 'probe url: HTTP 200, links https://church-bulletin.org/?id=311, which redirects to the church-bulletin.org
    listing of dated weekly PDFs (latest 2026-10-25).'
publication_reviews:
- parish: church-of-the-holy-child-wilmington
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1109/20261018B.pdf
    seen: 2026-10-27
    quote: Church of the Holy Child
    note: 'Holy Child''s 18 October 2026 issue: its own cover, Mass intentions (e.g. ''9:00 a.m.   Brenda
      Howard ~ Rosemary Lynch'') and a second collection ''for Parish Deficit Reduction''. Checked 2026-10-27:
      each masthead names its own parish only (St. Helena Church; Church of the Holy Child). St. Helena''s
      issue names Holy Child only in a deanery parish list (p.3); Holy Child''s names St. Helena only
      in a deanery list (p.3) and a staff line (p.7).'
  - url: https://www.church-bulletin.org/bulletin/saint-helena-s-church-wilmington-de-19809/2026-10-25.pdf
    seen: 2026-10-27
    quote: ST. HELENA CHURCH
    note: 'St. Helena''s 25 October 2026 issue: different publisher, masthead, intentions (''9:00 AM —
      Samuel & Marie Emmi'') and a second collection for ''All Saints Day Maintenance & Repair''. Different
      weeks, so the content test is the mastheads, intentions and publishers, not the collection.'
---

## Publisher

St. Helena's bulletin is a John Patrick Publishing issue, listed at church-bulletin.org/saint-helena-s-church-wilmington-de-19809 (the parish site links `church-bulletin.org/?id=311`, a redirect to that listing). The newest issue, 25 October 2026, carries a masthead for St. Helena Church alone, with its own Mass intentions (Monday 26 to Sunday 1 November) and parish calendar.

## Worship sites

One church, 602 Philadelphia Pike. The map and GCatholic agree on the address. Mass in the diocese map: Sunday 8:00 and 10:00, Saturday 5:00 pm vigil, weekdays and Saturday 9:00; the Holy Rosary and IHM bulletin covers print the same.

## Shared pastor, separate bulletin

Very Rev. Michael J. Carrier is pastor here and at Holy Child (since 14 January 2026; The Dialog 2025-12-01). Both bulletins name him, and both name Fr. Sylvester Obumneme as parochial vicar, but the two are separate publications from separate publishers with different content (Holy Child: LPi container 03/1109; St. Helena: church-bulletin.org), so this is its own row.

## Website and bulletin provider

sainthelenas.org is the parish site; the PDFs are on church-bulletin.org, so the resolver reads the listing page (`page-pdfs`). The fetch check is described under *Fetch check* below.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-helena-wilmington` (2026-10-27): Resolved with the pinned `page-pdfs` recipe to `2026-10-25.pdf` (4.9 MB), fresh, transport ok, document type PDF. Identity is reported 'unverified' by the tool (no expected identity supplied); the masthead read above settles it.

## Not yet confirmed

Nothing outstanding.
