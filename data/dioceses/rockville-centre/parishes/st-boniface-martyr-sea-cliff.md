---
name: Church of St. Boniface Martyr
website: https://www.saintboniface.org/2024/08/11/our-parish-bulletin-2/
bulletin_provider: other
provider_id: page-pdfs https://www.saintboniface.org/tag/parish-bulletin/
publication: ['url:https://www.saintboniface.org/2024/08/11/our-parish-bulletin-2/#st-boniface-martyr']
group: ''
evidence:
- url: https://www.saintboniface.org/wordpress/wp-content/uploads/2024/08/November-8-2026-Bulletin.pdf
  seen: 2026-11-13
  quote: Serving the People of God
  note: 'Page 1 masthead of the 8 November 2026 issue: ''Church of St. Boniface Martyr'', 145 Glen Avenue,
    Sea Cliff, ''The Very Reverend Dom Josef Norys, Can. Reg., Pastor''; Mass Schedule Saturday 9am, 4pm;
    Sunday 8am, 10:30am; Mondays - Fridays 8am.'
- url: https://www.saintboniface.org/2024/08/11/our-parish-bulletin-2/
  seen: 2026-11-13
  note: The 'Our Parish Bulletin' post links the weekly issues newest first (November-8-2026-Bulletin.pdf,
    November-1-2026-Bulletin.pdf, October-11-2026-Bulletin.pdf ...) under wp-content/uploads/2024/08/.
promoted: 2026-11-13
bulletin_status: available
publication_reviews:
- parish: glen-cove-catholic
  decision: separate
  evidence:
  - url: https://www.saintboniface.org/wordpress/wp-content/uploads/2024/08/November-8-2026-Bulletin.pdf
    seen: 2026-11-13
    note: The 8 November 2026 masthead names Church of St. Boniface Martyr alone, with its own Mass schedule;
      a grep for Patrick, Rocco and Hyacinth finds nothing.
  - url: https://irp.cdn-website.com/b5c3ff4d/files/uploaded/Patrick11-8.pdf
    seen: 2026-11-13
    note: The 8 November 2026 Glen Cove Catholic masthead names St Patrick Parish, St Rocco Church and
      St Hyacinth Church, not St. Boniface; a grep for Boniface finds nothing.
---

## Publisher

St. Boniface Martyr, 145 Glen Avenue, Sea Cliff publishes its own weekly bulletin on its WordPress site. The 8 November 2026 issue (`https://www.saintboniface.org/wordpress/wp-content/uploads/2024/08/November-8-2026-Bulletin.pdf`, 8 pages, read 2026-11-13) has the page-1 masthead "Church of St. Boniface Martyr / Serving the People of God in Sea Cliff, Glen Cove, Glen Head, Glenwood Landing and surrounding communities", names "The Very Reverend Dom Josef Norys, Can. Reg., Pastor", and gives the Mass Schedule: Saturday 9am, 4pm; Sunday 8am, 10:30am; Mondays - Fridays 8am. This agrees with the diocese's Mass-times page.

## Worship sites

One: the church at 145 Glen Avenue (`st-boniface-martyr-sea-cliff-church`). The diocesan locator (directory:36), GCatholic (16912) and the Mass-times page list only this building, and the bulletin names no other place.

## Website and bulletin provider

saintboniface.org's "Our Parish Bulletin" post (`https://www.saintboniface.org/2024/08/11/our-parish-bulletin-2/`) links each week's PDF newest first, all uploaded under wp-content/uploads/2024/08/ and named by date (November-8-2026-Bulletin.pdf). `fetch` reads it with the `other` resolver from that page.

The batch brief asked whether Sea Cliff shares the Glen Cove Catholic bulletin: the June 2026 appointments name one parochial vicar for St. Patrick, St. Rocco, St. Hyacinth and St. Boniface Martyr, and Dom Josef Norys is also listed among Glen Cove's assisting clergy. It does not: the two 8 November 2026 issues have different mastheads and schedules, and neither names the other's churches (`publication_reviews`). They stay separate rows.

`fetch:check` (2026-11-13) resolved the site to `page-pdfs https://www.saintboniface.org/tag/parish-bulletin/` (the tag archive, which lists the same post) and picked November-8-2026-Bulletin.pdf, dated 2026-11-08; that recipe is recorded in `provider_id`.

## Not yet confirmed

Nothing open.
