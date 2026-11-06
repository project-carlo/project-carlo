---
name: St. Mary's of Winfield (Woodside)
website: https://stmarysofwinfield.com/
bulletin_provider: other
provider_id: page-pdfs https://stmarysofwinfield.com/important-information/bulletin/
publication: ['po-container:03/4076']
group: Deanery Q2 (Queens West)
evidence:
- url: http://stmarysofwinfield.com/wp-content/uploads/sites/91/2026/11/nov8_2026_stmarywin_compressed.pdf
  seen: 2026-11-06
  quote: BVM Help of Christians
  note: 8 November 2026 issue, 8 pages. Page 1 masthead 'ST. MARY'S WINFIELD', 'BVM Help of Christians',
    'SINCE 1854', 'THIRTY-SECOND SUNDAY IN ORDINARY TIME • NOVEMBER 08, 2026'; Mass schedule Saturday
    5:00 pm English; Sunday 10:00 am English, 12:00 pm Spanish; weekdays 8:30 am; Friday 7:30 pm Spanish;
    First Saturday 8:00 am Spanish; '70-31 48th Avenue, Woodside, NY 11377'. Page 2 lists Rev. Jonas Achacoso,
    J.C.D., Pastor. Last page footer 'Blessed Virgin Mary Help of Christians | 03-4076' (an LPi issue).
- url: https://container.parishesonline.com/bulletins/03/4076/20261108B.pdf
  seen: 2026-11-06
  note: 'probe container 03/4076: the same 8 November 2026 issue (8 pages, same page 1 schedule and rectory
    hours) is live in the LPi container.'
- url: https://stmarysofwinfield.com/important-information/bulletin/
  seen: 2026-11-06
  note: Parish site (diocesan WordPress multisite, uploads under /sites/91/; probe url UNREACHABLE, read
    with visit.py) lists weekly PDFs newest first, nov8_2026_stmarywin_compressed.pdf back to july26_2026_stmarywin.pdf.
research:
- method: probe po on slugs blessed-virgin-mary-help-of-christians-11377, -church-11377, st-marys-of-winfield-11377,
    st-mary-s-of-winfield-11377, st-mary-church-11377, st-marys-church-11377, bvm-help-of-christians-11377
    and others
  url: https://parishesonline.com/organization/blessed-virgin-mary-help-of-christians-church-11377
  checked: '2026-11-06'
  outcome: not-found
  next_action: Find the ParishesOnline org slug or LPi widget id for container 03/4076 (search parishesonline.com
    for Woodside 11377, or read an LPi link on the parish site) and switch the row to parishes_online
  retry_when: A ParishesOnline search or a link naming the org is found; until then the page-pdfs recipe
    reads the reposted issues
- method: fetch:check other page-pdfs https://stmarysofwinfield.com/important-information/bulletin/
  url: http://stmarysofwinfield.com/wp-content/uploads/sites/91/2026/11/nov8_2026_stmarywin_compressed.pdf
  checked: '2026-11-06'
  outcome: found
bulletin_status: available
---

## Publisher

St. Mary's of Winfield (canonically Blessed Virgin Mary, Help of Christians) publishes a weekly LPi bulletin, container 03/4076, and reposts each issue on its parish site's `/important-information/bulletin/` page. I read the 8 November 2026 issue (read 2026-11-06): page 1 masthead "ST. MARY'S WINFIELD", "BVM Help of Christians", "SINCE 1854", 70-31 48th Avenue; page 2 names Rev. Jonas Achacoso, J.C.D., Pastor; the last page footer reads "Blessed Virgin Mary Help of Christians | 03-4076". The container holds the same issue.

The parish's own bulletin names no other parish in its masthead. St. Sebastian's bulletin mentions St. Mary of Winfield only as one of the parishes the St. Sebastian Catholic Academy serves.

## Worship sites

One church, St. Mary's of Winfield, 70-31 48th Avenue (`st-marys-of-winfield-woodside`). The page 1 schedule covers this church alone; no mission or chapel is named.

## Website and bulletin provider

`other` with the `page-pdfs https://stmarysofwinfield.com/important-information/bulletin/` recipe that `fetch:check` printed on 2026-11-06, when it picked `nov8_2026_stmarywin_compressed.pdf`, this weekend's issue (freshness `unknown`, the date is in the file name and masthead). I couldn't find the ParishesOnline org for container 03/4076 (slugs tried are in research), so the row can't be `parishes_online` yet; `po-container:03/4076` is recorded as its publication id.

## Not yet confirmed

The ParishesOnline org slug for container 03/4076 (see research). With it the row would become `parishes_online`.
