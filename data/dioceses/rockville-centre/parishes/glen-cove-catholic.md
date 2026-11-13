---
name: Glen Cove Catholic
website: https://www.glencovecatholic.org/bulletin
bulletin_provider: other
provider_id: page-pdfs https://www.glencovecatholic.org/bulletin
publication: ['url:https://www.glencovecatholic.org/bulletin#glen-cove-catholic']
group: ''
evidence:
- url: https://irp.cdn-website.com/b5c3ff4d/files/uploaded/Patrick11-8.pdf
  seen: 2026-11-13
  quote: St Patrick Parish—St Rocco Church—St Hyacinth Church
  note: Page 1 masthead of the 8 November 2026 issue names Glen Cove Catholic with St Patrick Parish,
    St Rocco Church and St Hyacinth Church, and its Mass Times table has a column for each of the three
    churches. No other church is named; Sea Cliff appears only in an advertiser's address on page 8.
- url: https://www.glencovecatholic.org/bulletin
  seen: 2026-11-13
  note: Bulletin page (Duda site, read with visit.py and probe get) links the current issue as 'November
    8' (irp.cdn-website.com/b5c3ff4d/files/uploaded/Patrick11-8.pdf) and links LPi (4lpi.com) as its printer;
    no LPi id is embedded.
- url: https://irp.cdn-website.com/b5c3ff4d/files/uploaded/Patrick11-8.pdf
  seen: 2026-11-13
  quote: The Very Rev’d Dom Gabriel Rach, Can.Reg.
  note: Page 4 lists one pastor and the Canonry of Saint Leopold clergy for all three churches.
promoted: 2026-11-13
bulletin_status: available
publication_reviews:
- parish: st-boniface-martyr-sea-cliff
  decision: separate
  evidence:
  - url: https://irp.cdn-website.com/b5c3ff4d/files/uploaded/Patrick11-8.pdf
    seen: 2026-11-13
    note: The 8 November 2026 masthead names St Patrick Parish, St Rocco Church and St Hyacinth Church,
      not St. Boniface Martyr; a grep for Boniface finds nothing.
  - url: https://www.saintboniface.org/wordpress/wp-content/uploads/2024/08/November-8-2026-Bulletin.pdf
    seen: 2026-11-13
    note: The 8 November 2026 St. Boniface masthead names Church of St. Boniface Martyr alone, with its
      own Mass schedule.
---

## Publisher

Glen Cove Catholic publishes one weekly bulletin for St. Patrick Parish (235 Glen Street, Glen Cove), St. Rocco Church (18 Third Street, Glen Cove) and St. Hyacinth Church (319 Cedar Swamp Road, Glen Head), which share a pastor from the Canonry of Saint Leopold. The 8 November 2026 issue (`https://irp.cdn-website.com/b5c3ff4d/files/uploaded/Patrick11-8.pdf`, 8 pages, made in PowerPoint, read 2026-11-13) has the page-1 masthead "Glen Cove Catholic / St Patrick Parish—St Rocco Church—St Hyacinth Church" and a Mass Times table with one column per church (page 1 rendered to read the columns):

- St Patrick: Monday-Friday 9:00 AM; Saturday 4:30 PM; Sunday 7:45 AM, 8:30 AM (Spanish), 11:00 AM, 5:00 PM.
- St Hyacinth: Saturday 9:00 AM; Saturday 5:00 PM; Sunday 9:00 AM, 10:15 AM (Polish).
- St Rocco: Monday-Friday 7:30 AM; Saturday 4:00 PM; Sunday 7:30 AM, 8:45 AM (Italian), 10:15 AM, 11:30 am (Extraordinary Form, Latin).

Page 4 lists the pastor, "The Very Rev’d Dom Gabriel Rach, Can.Reg.", and the parish staff with a music director for each of the three churches.

## Worship sites

Three: `st-patrick-glen-cove-church`, `st-rocco-glen-cove-church` and `st-hyacinth-glen-head-church`. The diocesan locator (directory:59, 65, 45), GCatholic (16849, 16850, 16851) and the Mass-times page list the same three buildings.

St. Boniface Martyr, Sea Cliff, shares a parochial vicar with these three churches (June 2026 appointments, per the batch brief), but this bulletin does not cover it: a grep of the 8 November issue for "Boniface" finds nothing, and "Sea Cliff" appears only in an advertiser's address on page 8. Sea Cliff publishes its own bulletin on saintboniface.org (`st-boniface-martyr-sea-cliff`).

## Website and bulletin provider

glencovecatholic.org (the locator's link for all three churches) is a Duda site. Its /bulletin page links the current issue by date ("November 8") as a self-hosted PDF on irp.cdn-website.com, and links 4lpi.com as the printer; it embeds no LPi id, and the issue's PDF metadata shows PowerPoint and Acrobat Distiller, not an LPi container. `fetch` reads it with the `other` resolver from the bulletin page.

The Mass-times page's entries (read 2026-11-12) give older schedules (for example St. Patrick Sunday 8:00, 10:15, 11:45 and 5:00 PM); the current bulletin is followed. GCatholic links stroccoglencove.com for St. Rocco, which did not load (certificate hostname mismatch, 2026-11-13), and the Mass-times page links churchsthyacinth.com for St. Hyacinth, now an unrelated blog (squatted; read 2026-11-13). Neither is used.

`fetch:check` (2026-11-13) read `page-pdfs https://www.glencovecatholic.org/bulletin` and picked Patrick11-8.pdf, dated 2026-11-08 from its file name; that recipe is recorded in `provider_id`. The page links one issue at a time, so each week's file replaces the last.

## Not yet confirmed

Nothing open.
