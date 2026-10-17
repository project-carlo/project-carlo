---
name: Parish Communities of Norfolk, Norwood and Brasher Falls
website: https://norfolknorwoodraymondville.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:15674']
group: Parish of the Visitation and St. Raymond / St. Andrew's / St. Patrick's
evidence:
- url: https://files.ecatholic.com/15674/bulletins/20260927.pdf
  seen: 2026-09-30
  note: '27 September 2026 issue, 5 pages, scanned images (no text layer; read with render.py, page 1
    and 2). Page 1 masthead: three church photographs labelled "Church of the Visitation", "St. Andrew''s
    Church" and "St. Patrick''s Church" over the title "Catholic Parish Weekly". Its "LITURGICAL SCHEDULE"
    gives Masses at Church of the Visitation, St. Patrick''s and St. Andrew''s only, and the Sanctuary
    Lamp box names the same three. recheck cannot find text in this file.'
- url: https://files.ecatholic.com/15674/bulletins/20260906.pdf
  seen: 2026-09-30
  quote: 'Office for St Andrew’s Church of the Visitation & St. Patrick’s: 3 Morris St., Norfolk, NY 13667'
  note: '6 September 2026 issue (text layer on pages 1-3), page 1: one office for the three churches.
    Trustees are listed for "Parish of the Visitation & St. Raymond", "St. Andrew''s Parish" and "St.
    Patrick''s Parish": three canonical parishes, one bulletin.'
- url: https://files.ecatholic.com/15674/bulletins/20260906.pdf
  seen: 2026-09-30
  quote: St. Patrick’s Church – $1,647.00
  note: 'Page 2, "God''s Plan for Giving": collections for "Parish of the Visitation & St. Raymond", "St.
    Andrew''s Church" and "St. Patrick''s Church". The Raymondville building is never named as a place
    of Mass: grep of this and five other 2026 issues for "Raymondville" finds only the pastor''s given
    name Raymond and the parish title.'
- url: https://norfolknorwoodraymondville.org/
  seen: 2026-09-30
  quote: 8:30 AM St. Patrick's, Brasher Falls
  note: 'Parish site home page (eCatholic, behind Cloudflare; read in a browser with visit.py). Mass Times:
    Saturday 4:00 PM St. Andrew''s, Norwood; Sunday 8:30 AM St. Patrick''s, Brasher Falls and 10:30 AM
    Visitation, Norfolk; Monday, Tuesday, Wednesday, Thursday 8:30 AM Visitation (Tuesday and Thursday
    also St. Patrick''s); Friday 8:30 AM St. Andrew''s.'
- url: https://norfolknorwoodraymondville.org/bulletins
  seen: 2026-09-30
  quote: September 27, 2026
  note: 'Bulletin archive page (browser): weekly PDFs at files.ecatholic.com/15674/bulletins/YYYYMMDD.pdf
    back to January 2026 and earlier years; the newest is 27 September 2026 (issues.py ecatholic ecatholic:15674
    finds all Sundays back to March 2026). Site behind Cloudflare, so recheck answers 403.'
- url: https://norfolknorwoodraymondville.org/pvsr
  seen: 2026-09-30
  quote: comprised of three Catholic Parishes (St. Andrew's / Visitation and St. Raymond / St. Patrick's)
  note: 'About Us: one pastor serves the three parishes, "serving the communities of Norwood, Norfolk,
    Raymondville, Stockholm, Winthrop, Brasher Falls, North Lawrence and Lawrenceville". (Site behind
    Cloudflare; read in a browser.)'
- url: https://www.rcdony.org/parish/norfolk
  seen: 2026-09-30
  quote: Parish of the Visitation and St. Raymond Church of the Visitation 3 Morris Street Norfolk, New
    York 13667
  note: Diocesan directory entry for Norfolk; the Norwood and Brasher Falls entries (rcdony.org/parish/norwood,
    /brasher-falls) give the same pastor, the same website and the office phone 315-384-4242.
- url: https://www.nny360.com/news/final-masses-celebrated-at-two-local-churches/article_13690a16-3219-5b15-b685-08ea76e9264c.html
  seen: 2026-09-30
  quote: Parishes will technically remain open, but will not hold regular services
  note: 'Watertown Daily Times, 27 Jan 2019: St. Lawrence (North Lawrence) and St. Raymond (Raymondville)
    celebrated their final regular Masses. Body scrambled in the raw HTML (paywall), readable in a browser;
    the subhead quoted is in the page text.'
promoted: 2026-09-30
---

## Publisher

Fr. Raymond Moreau is pastor of three canonical parishes (the Parish of the Visitation and St. Raymond, St. Andrew's Parish, St. Patrick's Parish) and they publish **one** weekly bulletin, "Catholic Parish Weekly", through eCatholic (site id 15674, files at `files.ecatholic.com/15674/bulletins/YYYYMMDD.pdf`). The 27 September 2026 issue is scanned images; its page 1 masthead shows Church of the Visitation, St. Andrew's Church and St. Patrick's Church, one "Liturgical Schedule" covers all three and one Sanctuary Lamp box names them. The 6 September 2026 issue has a text layer and gives the same structure: a single office (3 Morris St., Norfolk) for St. Andrew's, Visitation and St. Patrick's, with trustees named per canonical parish.

The diocese's directory shows the same grouping (all three entries share the pastor, the website and phone 315-384-4242) but only the Norfolk entry has a `group` ("Parish of the Visitation and St. Raymond"); the Norwood and Brasher Falls entries have none. The tri-parish site says the parishes serve "Norwood, Norfolk, Raymondville, Stockholm, Winthrop, Brasher Falls, North Lawrence and Lawrenceville".

## Worship sites

- `visitation-norfolk` (3 Morris St., Norfolk): Sunday 10:30 am, weekdays 8:30 am.
- `st-andrews-norwood` (Norwood): Saturday 4 pm, Friday 8:30 am.
- `st-patricks-brasher-falls` (Brasher Falls): Sunday 8:30 am, Tuesday and Thursday 8:30 am.

Two buildings the rosters list are not here because they no longer have Mass: **St. Raymond, Raymondville** (`excluded/st-raymond-raymondville.md`) and **St. Lawrence, North Lawrence** (`excluded/st-lawrence-north-lawrence.md`, sold; now a fitness center). Both had their final regular Masses before 27 January 2019 (Watertown Daily Times). "St. Raymond" survives only in the corporate name of the Norfolk parish, whose church is the Church of the Visitation.

## Website and bulletin provider

norfolknorwoodraymondville.org is an eCatholic site behind Cloudflare (`probe url` answers 403; `visit.py` loads it, in 2-3 tries). Its Bulletin page lists the weekly PDFs on `files.ecatholic.com/15674`, which fetch without a browser; `issues.py ecatholic ecatholic:15674` finds 30 consecutive Sundays to 27 September 2026 (the 4 October issue is not up yet). Provider `ecatholic`, `publication: ecatholic:15674`. Several issues (27 September, 20 September, 13 September, 2 August, 12 July) are scanned images or mostly images: the pipeline will need to read them as images too. The diocese's Parish Bulletins page links norfolknorwoodraymondville.org/bulletins for Norfolk and Norwood (Brasher Falls has no entry there). A ParishesOnline organization "St Andrew, St Raymond & Visitation of the BVM Church" (`po-org:st-andrew-st-raymond-visitation-of-the-bvm-church`, lpi:0018000000Qx7PbAAJ, 3 Morris St.) exists but `probe po` shows no publications, so it is an unused account and is not recorded as a bulletin.

## Not yet confirmed

- Whether the building at Raymondville is still owned by the diocese or sold; only the 2019 report and the current schedule were read.
- Fr. Moreau's parishes were not mentioned in the 2 September 2026 Massena/Waddington announcement, so no change is expected here.
