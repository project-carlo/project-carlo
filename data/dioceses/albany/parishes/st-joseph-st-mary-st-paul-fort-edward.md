---
name: The Parishes of St. Joseph's and St. Mary's/St. Paul's
website: https://parishes.rcda.org/St.JosephsFt.Edward/index.php
bulletin_provider: parishes_online
provider_id: st-joseph-church-12828
publication: ['po-org:st-joseph-church-12828', 'lpi:0018000000Qc1XOAAZ', 'po-container:03/0420']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/0420/20260927B.pdf
  seen: 2026-09-28
  quote: St. Joseph Church  |  03-0420
  note: 'The 27 September 2026 issue (5 pages). Pages 1-4 are images with no text layer; page 1, read
    as an image (parish-site-access render.py), is headed "The Parishes of St. Joseph''s and St. Mary''s/St.
    Paul''s" with two boxes: "164 Broadway Fort Edward ... Saturday Mass 4pm ... Daily Mass Friday ...
    Mass 5:30pm" and "11 Wall St. Hudson Falls ... Sunday Mass 10am ... Daily Mass Wednesday ... Mass at
    5:30pm", dated "SEPTEMBER 26-27, 2026". The quote is the LPi footer on page 5, the only text layer.'
- url: https://parishesonline.com/organization/st-joseph-church-12828
  seen: 2026-09-28
  note: '`probe po st-joseph-church-12828`: ''St. Joseph Church'', 164 Broadway, Fort Edward, LPi 0018000000Qc1XOAAZ,
    container 03/0420, weekly issues through 2026-09-27.'
- url: https://parishes.rcda.org/St.JosephsFt.Edward/Bulletin.php
  seen: 2026-09-28
  note: St. Joseph's site (on the diocese's parish host) posts the same LPi PDFs as bulletins/2026/<Month>_<DD>.pdf
    (newest September_20.pdf on 2026-09-28, whose page 5 footer is also "St. Joseph Church | 03-0420").
---

## Publisher

St. Joseph's, Fort Edward and St. Mary's/St. Paul's, Hudson Falls share one weekly LPi
bulletin (ParishesOnline container 03/0420, registered to St. Joseph Church). Page 1 of the
26-27 September 2026 issue is headed "The Parishes of St. Joseph's and St. Mary's/St.
Paul's" and has a box for each church: St. Joseph's, 164 Broadway, Fort Edward, "Saturday
Mass 4pm", Friday 5:30 pm; St. Mary's/St. Paul's, 11 Wall St., Hudson Falls, "Sunday Mass
10am", Wednesday 5:30 pm. Parochial Vicar Fr. Adam Feisthamel, Deacon Bill Bazinet; trustees
listed for each parish.

**The bulletin is image-only** (pages 1-4 have no text layer; page 5 is the LPi ad page).
The pipeline will need to read it as images.

## Worship sites

Two: `st-joseph-fort-edward` and `st-mary-st-paul-hudson-falls`. The institutional-records
index gives St. Mary's/St. Paul's the records of St. Alphonsus, Glens Falls (closed); that
building is in neither roster and was not researched further.

## Website and bulletin provider

The diocese lists parishes.rcda.org/St.JosephsFt.Edward/ for St. Joseph's and no website for
Hudson Falls. That site's Bulletin page posts the same LPi PDFs (the page 5 footer names
container 03-0420), a week behind ParishesOnline. The ParishesOnline organization was found
by web search; its record says 164 Broadway, and `probe po` gives the ids. Fetching goes by
`provider_id`.

## Not yet confirmed

Nothing about the bulletin. Whether St. Mary's/St. Paul's ever published separately was not
checked: no ParishesOnline organization answered for the Hudson Falls <name>-12839 slugs
tried, and the diocese lists no website for it.
