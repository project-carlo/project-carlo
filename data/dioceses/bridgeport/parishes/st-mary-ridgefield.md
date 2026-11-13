---
name: St. Mary
website: https://www.smcr.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-mary-parish-ridgefield-ct-06877
publication: ['url:https://www.church-bulletin.org/saint-mary-parish-ridgefield-ct-06877']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-mary-parish-ridgefield-ct-06877/2026-11-15.pdf
  seen: 2026-11-12
  note: '15 November 2026 issue, 16 pages, image-only (probe pdf: readable_pages 0); page 1 rendered:
    ''NOVEMBER 15, 2026'', ''GOOD NEWS'', ''St. Mary Parish Weekly Bulletin''; Mass schedule Sunday 7:30
    AM, 9 AM, 12 PM, 5 PM, 10:30 AM (HALL); Saturday 8:00 AM, 4:30 PM Vigil; Monday-Friday 7:00 AM & noon;
    footer ''St. Mary Parish, 55 Catoonah Street, Ridgefield, CT 06877, 203-438-6538, smcr.org''. Names
    no other church.'
- url: https://www.church-bulletin.org/saint-mary-parish-ridgefield-ct-06877
  seen: 2026-11-12
  quote: Latest Edition November 15, 2026 Bulletin
  note: John Patrick Publishing's church-bulletin.org page for the parish; links dated issues bulletin/saint-mary-parish-ridgefield-ct-06877/<YYYY-MM-DD>.pdf
    to 2026-11-15.
- url: https://www.smcr.org/bulletins-1
  seen: 2026-11-12
  note: 'eCatholic site (ecatholic:2512), behind Cloudflare (probe url 403; read with visit.py). ''Bulletins
    & Newsletters'' page: ''our weekly bulletin, Good News''; ''Click image above to view this week''s
    bulletin and our archive of bulletins'' links https://church-bulletin.org/?id=936, which redirects
    to the church-bulletin.org page above.'
promoted: 2026-11-12
bulletin_status: available
---

## Publisher

John Patrick Publishing prints St. Mary, Ridgefield's weekly bulletin, *Good News*, and posts it on church-bulletin.org. The 15 November 2026 issue (`https://www.church-bulletin.org/bulletin/saint-mary-parish-ridgefield-ct-06877/2026-11-15.pdf`, read 2026-11-12) is image-only; page 1, rendered, reads "NOVEMBER 15, 2026", "GOOD NEWS", "St. Mary Parish Weekly Bulletin", with the Mass schedule and the footer "St. Mary Parish, 55 Catoonah Street, Ridgefield, CT 06877".

## Worship sites

- `st-mary-ridgefield`: page 1 lists Sunday 7:30 AM, 9 AM, 12 PM, 5 PM and "10:30 AM (HALL)", Saturday 8:00 AM and 4:30 PM Vigil, Monday-Friday 7:00 AM and noon, and an adoration chapel open 24/7.

The 10:30 Sunday Mass is in the parish hall, which the diocese's directory also notes ("In parish hall"); it is on the parish's own premises and is not recorded as a separate worship site (not checked whether the hall has its own street address). The issue names no other church. The diocese's directory (directory:1420) and GCatholic (22018) list this one church.

## Website and bulletin provider

`smcr.org` is an eCatholic site (site 2512) behind Cloudflare: `probe url` got HTTP 403 and `visit.py` read it. Its *Bulletins & Newsletters* page links `https://church-bulletin.org/?id=936`, which redirects to the parish's church-bulletin.org page listing dated PDFs (`bulletin/<slug>/<YYYY-MM-DD>.pdf`). The eCatholic site id is the site's account, kept in evidence, not `publication`. The parish's separate weekly e-newsletter, *Keeping Us Connected*, was not read. Provider `other`, pinned `page-pdfs` on the church-bulletin.org page; see the fetch check below. The issues are image-only, so the pipeline's text extraction will need OCR.

`fetch:check` on 2026-11-12 (headed Chrome) resolved "page-pdfs on https://www.church-bulletin.org/saint-mary-parish-ridgefield-ct-06877: current" and picked `2026-11-15.pdf`, the 15 November 2026 issue read above (dated from the URL; freshness `future`, posted 3 days ahead).

## Not yet confirmed

Nothing open.
