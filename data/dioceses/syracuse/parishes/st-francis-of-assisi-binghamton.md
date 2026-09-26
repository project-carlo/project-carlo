---
name: St. Francis of Assisi Parish
website: https://www.stfrancisbing.org
bulletin_provider: parishes_online
provider_id: st-francis-of-assisi-church-13901
publication: ['po-org:st-francis-of-assisi-church-13901', 'lpi:0018000000Qc1WXAAZ', 'po-container:06/0168',
  'url:https://www.stfrancisbing.org/bulletins.html']
group: ''
evidence:
- url: https://www.stfrancisbing.org/uploads/2/1/9/0/21905376/09272026.pdf
  seen: 2026-09-26
  quote: St. Francis of Assisi Parish 1031 Chenango Street, Binghamton, New York 13901 September 27, 2026
  note: The 27 September 2026 issue as posted on the parish's own Bulletins page. Page 2 lists Saturday
    4:00 p.m. and Sunday 10:30 a.m. Masses and "NO MASS" Monday to Friday.
- url: https://container.parishesonline.com/bulletins/06/0168/20260920B.pdf
  seen: 2026-09-26
  quote: St. Francis of Assisi Parish 1031 Chenango Street, Binghamton, New York 13901 September 20, 2026
  note: '`probe po st-francis-of-assisi-church-13901`: LPi id 0018000000Qc1WXAAZ, container 06/0168, issues
    through 2026-09-27. Same masthead as the self-hosted PDFs, so it is the same bulletin.'
- url: https://www.syracusediocese.org/st-francis-of-assisi-binghamton
  seen: 2026-09-26
  note: 'Diocese page (behind Cloudflare; read with visit.py): 1031 Chenango Street; "Sacramental Records
    for St. Catherine of Sienna, Binghamton; St. Christopher, Binghamton; and St. Rita, Chenango Forks
    are retained here."'
promoted: 2026-09-26
---

## Publisher

St. Francis of Assisi publishes its own weekly bulletin. I read the 27 September 2026 issue: the
page-1 masthead is "St. Francis of Assisi Parish, 1031 Chenango Street", pastor Rev. Timothy
Taugher, and page 2 lists the week's Masses, Saturday 4:00 pm and Sunday 10:30 am at the one
church, with no weekday Mass. The same issues go to ParishesOnline (container 06/0168, same
masthead) and to the parish's own Bulletins page.

## Worship sites

One: the church at 1031 Chenango Street (`churches/st-francis-of-assisi-binghamton.md`). The
diocese says St. Francis keeps the records of St. Catherine of Siena, St. Christopher and St. Rita
(Chenango Forks), all "CLOSED - See St. Francis of Assisi" in its parish list. Two church-listing
sites put St. Catherine of Sienna parish at 1031 Chenango Street with St. Francis's phone number,
so the St. Francis church appears to be St. Catherine's former building and that finder entry is
linked to the church record. St. Christopher and St. Rita are excluded as closed
(`excluded/st-christopher-binghamton.md`, `excluded/st-rita-chenango-forks.md`): the bulletin's
schedule has only the one church.

## Website and bulletin provider

stfrancisbing.org is the parish's own site; its Bulletins page links a PDF per Sunday
(uploads/.../MMDDYYYY.pdf) through 27 September 2026. The same bulletin is on ParishesOnline
(organization `st-francis-of-assisi-church-13901`, container 06/0168), which the pipeline reads
by org slug, so the provider is `parishes_online`. All ids and the Bulletins page are in
`publication`.

## Not yet confirmed

That 1031 Chenango Street is St. Catherine of Siena's former church rests on two directory-style
listings, not a parish or diocesan history (see the church record).
