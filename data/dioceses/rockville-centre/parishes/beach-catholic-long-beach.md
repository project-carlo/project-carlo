---
name: Beach Catholic
website: https://beachcatholic.com/
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://beachcatholic.com/#beach-catholic']
group: ''
evidence:
- url: https://www.canva.com/design/DAHaFZ7Oocw/BbqlQDwr1yEnwgiMKG4OnQ/view
  seen: 2026-11-13
  quote: ST. IGNATIUS MARTYR CHURCH  +  ST. MARY OF THE ISLE CHURCH  +  OUR LADY OF THE MIRACULOUS MEDAL
    CHURCH
  note: Page 1 masthead of the Beach Catholic bulletin for 'THIRTY-THIRD SUNDAY IN ORDINARY TIME + NOVEMBER
    15, 2026' names the three churches together; read in the browser (parish-site-access visit.py), linked
    as 'Current Bulletin' from beachcatholic.com.
- url: https://beachcatholic.com/
  seen: 2026-11-13
  quote: 'St. Mary of the Isle:'
  note: 'Home page (read with parish-site-access visit.py; probe url could not connect) gives one schedule
    for the three churches: St. Ignatius Martyr weekend 5:30pm (Sat), 8am, 9:45am, 5pm (Sun); St. Mary
    of the Isle 4pm (Sat), 8:30am, 10am en Español, 11:30am (Sun); Our Lady of the Miraculous Medal 7:30am,
    10:30am (Grotto) (Sun); one tri-parish rectory at 721 W Broadway, Long Beach.'
research:
- method: fetch:check page-pdfs on the home page
  url: https://beachcatholic.com/
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Set provider other with a Canva recipe once a collector reads Canva design views, or pin
    page-pdfs if the parish starts posting PDFs
  retry_when: A Canva collector lands or the site links a bulletin PDF
bulletin_status: unsupported-format
fetch_gap:
  kind: canva-design-viewer
  seen: 2026-11-13
  url: https://www.canva.com/design/DAHaFZ7Oocw/BbqlQDwr1yEnwgiMKG4OnQ/view
  note: The home page's 'Current Bulletin' link opens a Canva design (titled 'Bulletin - 11/15', 10 pages)
    readable only in Canva's JavaScript viewer; no PDF is linked. beachcatholic.com/bulletin redirects
    to the home page. fetch:check (2026-11-13) picked the home page's first PDF, a 2020 parish history
    (Parishhistorypart-1-3-12.pdf).
---

## Publisher

Beach Catholic, the three parishes on the Long Beach barrier island served from one tri-parish rectory (721 W Broadway, Long Beach), publishes one weekly bulletin. The home page's "Current Bulletin" link (read 2026-11-13 in the browser with parish-site-access visit.py; `probe url` could not connect) opens a Canva design, `https://www.canva.com/design/DAHaFZ7Oocw/BbqlQDwr1yEnwgiMKG4OnQ/view`, titled "Bulletin - 11/15", 10 pages. Its page-1 masthead reads "BEACH CATHOLIC", "THIRTY-THIRD SUNDAY IN ORDINARY TIME + NOVEMBER 15, 2026" and "ST. IGNATIUS MARTYR CHURCH + ST. MARY OF THE ISLE CHURCH + OUR LADY OF THE MIRACULOUS MEDAL CHURCH". The diocesan locator, GCatholic and the Mass-times page list the three as separate parishes, but they share this one bulletin, so they are one row.

## Worship sites

Three, the churches the masthead names and the home page's Mass schedule (2026-11-13) lists:

- St. Ignatius Martyr, 721 W Broadway, Long Beach (`st-ignatius-martyr-long-beach-church`): weekend 5:30pm (Sat), 8am, 9:45am, 5pm (Sun).
- St. Mary of the Isle, 315 E Walnut Street, Long Beach (`st-mary-of-the-isle-long-beach-church`): 4pm (Sat), 8:30am, 10am en Español, 11:30am (Sun).
- Our Lady of the Miraculous Medal, 75 Parkside Drive, Point Lookout (`our-lady-of-the-miraculous-medal-point-lookout-church`): 7:30am, 10:30am (Grotto) (Sun).

The diocesan locator, GCatholic and the Mass-times page list no other building for these parishes.

## Website and bulletin provider

beachcatholic.com is the locator's and Mass-times page's link for all three (GCatholic still gives the older stmaryoftheisle.com and olmmc.com). The bulletin is published only as a Canva design viewed in Canva's JavaScript viewer; the site links no bulletin PDF, and `beachcatholic.com/bulletin` (the link given in its video descriptions) redirects to the home page. `fetch:check` (2026-11-13, page-pdfs on the home page) picked the first PDF there, a 2020 parish history (`Parishhistorypart-1-3-12.pdf`), so the row is `unsupported` with fetch_gap `canva-design-viewer`, as in the other dioceses with Canva bulletins.

## Not yet confirmed

Only page 1 of the Canva issue was read; the Mass schedule comes from the home page. Whether the Canva link is a new design each week or one design edited weekly is not known: check the home page's link next week.
