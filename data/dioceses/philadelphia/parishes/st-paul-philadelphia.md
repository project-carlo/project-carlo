---
name: St. Paul
website: http://www.stpaulphilly.org/
bulletin_provider: parishes_online
provider_id: st-paul-church-19147
publication: ['po-org:st-paul-church-19147', 'lpi:0018000000Qc2MvAAJ', 'po-container:03/0254']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/0254/20261025B.pdf
  seen: 2026-10-29
  quote: Saint Paul Friary and Parish Offices
  note: 'Page 1 of the 25 October 2026 issue (12 pages), headed MASS SCHEDULE: Saint Paul Church, 923
    Christian Street (Vigil 5:00 PM, Sunday 8:00 AM, 12:00 PM, 5:00 PM, Mon-Fri 7:30 AM) and St. Mary
    Magdalen de Pazzi Church, 714 Montrose Street (Sunday 10:00 AM). Contact block: Rev. Paul W. Galetto,
    OSA, Pastor. The masthead names St. Paul alone; St. Nicholas of Tolentine appears nowhere as a church
    or Mass site.'
- url: https://parishesonline.com/organization/st-paul-church-19147
  seen: 2026-10-29
  note: 'probe po st-paul-church-19147: St. Paul Church, 808 S Hutchinson St 19147, website stpaulphilly.org;
    ids lpi:0018000000Qc2MvAAJ, po-container:03/0254; issues 2026-09-27 to 2026-11-01 (the 1 November
    file was already posted on 29 October).'
- url: http://www.stpaulphilly.org/bulletins
  seen: 2026-10-29
  note: probe url on the parish site found po-org:st-paul-church-19147 and a /bulletins page (Astro site).
- url: https://archphila.org/parish/st-paul-philadelphia/
  seen: 2026-10-28
  note: 'Directory: 923 Christian St.; rectory 808 S. Hutchinson St.; Pastor Rev. Paul W. Galetto, O.S.A.;
    Worship Site: St. Mary Magdalen De Pazzi Church.'
research:
- method: 'pnpm fetch:check --diocese philadelphia --parish st-paul-philadelphia: resolved the ParishesOnline
    container; transport ok, pdf, picked 20261101B.pdf, freshness ''future'' (the 1 November issue was
    posted on 29 October; the 25 October issue is the current one, read for this record)'
  url: https://container.parishesonline.com/bulletins/03/0254/20261101B.pdf
  checked: '2026-10-29'
  outcome: found
  next_action: If the pipeline rejects future-dated issues, check that the 25 October issue is picked
    until 1 November; no other channel exists (no John Patrick listing for St. Paul, 19147).
publication_reviews:
- parish: st-nicholas-of-tolentine-philadelphia
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/the-parish-community-of-saint-nicholas-of-tolentine-philadelphia-pa-19148/2026-10-25.pdf
    seen: 2026-10-29
    note: The 25 October 2026 masthead of St. Nicholas of Tolentine's John Patrick issue (listing 275)
      names St. Nicholas alone at 910 Watkins Street, with its own Mass Schedule; St. Paul's ParishesOnline
      issue (03/0254) of the same Sunday lists only St. Paul and St. Mary Magdalen de Pazzi.
---

## Publisher

St. Paul publishes its own weekly bulletin through ParishesOnline (org `st-paul-church-19147`, container 03/0254). The 25 October 2026 issue's page 1 is a Mass Schedule box for two churches, St. Paul at 923 Christian Street and St. Mary Magdalen de Pazzi at 714 Montrose Street, with the contact block of Saint Paul Friary and Parish Offices and Rev. Paul W. Galetto, OSA, Pastor. Page 2 lists Mass intentions, the 10:00 AM Sunday Mass for the St. Mary Magdalen de Pazzi Purgatorial Society.

## Worship sites

Two: St. Paul and St. Mary Magdalen de Pazzi, both in the Mass box (the directory's worship-site line is confirmed by the bulletin, not only the directory). GCatholic's 'St. Paul, 10th St. & Christian St.' (19144) is the same church as 923 Christian St.

## Not a shared bulletin with St. Nicholas of Tolentine

St. Nicholas of Tolentine's pastor, Rev. Nicholas Martorano, O.S.A., lives at St. Paul (directory: 'In residence at Saint Paul'), but St. Nicholas prints its own John Patrick issue (listing 275) with its own masthead and Mass times. A residence is not a shared bulletin (see diocese.md, Rules settled).

## John Patrick listing 62

The lead pointing to church-bulletin.org/?id=62 is the Cathedral Basilica of Saints Peter & Paul (19103), not this parish; no John Patrick listing for St. Paul, 19147, was found in the scan (raw/jppc-pa.json).

## Not yet confirmed

Nothing outstanding.
