---
name: St. Thomas the Apostle
website: https://www.stawh.church/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stawh.church/bulletin#st-thomas-the-apostle']
group: ''
evidence:
- url: https://www.stawh.church/bulletin/231-11-15-2026/file
  seen: 2026-11-13
  quote: St. Thomas the Apostle Chapel
  note: 'Issue for the Thirty Third Sunday, 15 November 2026 (20 pages, LibreOffice Draw, uploaded 12
    Nov). Page 1 masthead: St. Thomas the Apostle Church, 24 Westminster Road, West Hempstead, www.stawh.church;
    Weekend: Saturday Evening 5:00pm, Sunday 9:00am, 10:30am, 12:00noon, 6:00pm; Weekday Masses 9:00am
    Lower Church; ''St. Thomas the Apostle Chapel, Hempstead Ave. & Nassau Blvd.'', Sunday: 7:30am, 10:00am,
    11:30am; Rev. Tony Stanganelli, Pastor. Page 3 lists intentions for the Chapel''s 7:30, 10:00 and
    11:30 AM Masses on 15 and 22 November. Downloaded through Chrome (tools/browser_get.py).'
- url: https://www.stawh.church/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin page, read with parish-site-access visit.py (probe url answers 403):
    issues newest first as /bulletin/<n>-<M-D-YYYY>/file, the newest 231-11-15-2026, then 230-11-8-2026,
    229-11-1-2026 ...'
- url: https://www.stawh.church/im-new/directions-to-church-chapel
  seen: 2026-11-13
  note: 'Directions to Church & Chapel (visit.py): Church 24 Westminster Road; Chapel 876 Hempstead Avenue,
    West Hempstead, NY 11552, at the intersection of Hempstead Ave & Nassau Blvd.'
research:
- method: fetch:check, page-pdfs on the Solutio bulletin page
  url: https://www.stawh.church/bulletin
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Rerun fetch:check once a collector reads Solutio /file links
  retry_when: pnpm diocese gaps shows a collector for joomla-file-endpoint
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (page-pdfs on /bulletin) failed: "No PDF links
    found on bulletin page: https://www.stawh.church/bulletin". The issues are /bulletin/<n>-<M-D-YYYY>/file
    links, which Chrome downloads with tools/browser_get.py. The issue is made in LibreOffice Draw; no
    printer listing.'
  url: https://www.stawh.church/bulletin/231-11-15-2026/file
---

## Publisher

St. Thomas the Apostle, West Hempstead publishes its own weekly bulletin, made in LibreOffice Draw and posted on its Solutio (Joomla) site; it carries no printer's name. The newest issue on 2026-11-13, `https://www.stawh.church/bulletin/231-11-15-2026/file` (20 pages, Thirty Third Sunday, 15 November 2026), has the masthead "St. Thomas the Apostle Church, 24 Westminster Road, West Hempstead, New York 11552, www.stawh.church" and names Rev. Tony Stanganelli, Pastor. Its schedule: Saturday Evening 5:00pm; Sunday 9:00am, 10:30am, 12:00noon, 6:00pm; weekday Masses 9:00am in the Lower Church; and "St. Thomas the Apostle Chapel, Hempstead Ave. & Nassau Blvd., Celebration of the Eucharist Sunday: 7:30am, 10:00am, 11:30am".

## Worship sites

Two, both in this bulletin's schedule:

- the church at 24 Westminster Road (`st-thomas-the-apostle-west-hempstead-church`; directory:67, GCatholic 16931, Mass-times page);
- St. Thomas the Apostle Chapel, 876 Hempstead Avenue at Nassau Blvd. (`st-thomas-the-apostle-chapel-west-hempstead-church`), which the diocesan locator lists as "Lakeview Mission" (directory:11, 875 Hempstead Ave). It still has Mass: three Sunday Masses, with named intentions on page 3 for 15 and 22 November 2026. The bulletin notes the Chapel "is not in use on weekdays from mid-December through mid-March". GCatholic does not list it.

GCatholic places the Syro-Malabar St. Mary community at the St. Thomas building. Under the diocese's rule this church row stays with this parish, since it still has public Latin Mass there; the Syro-Malabar entry is the eastern-catholic batch's. The 15 November issue does not mention a Syro-Malabar community or Mass.

## Website and bulletin provider

stawh.church is the locator's link. GCatholic and the drvc.org Mass-times page link stthomasapostle.org, the parish's old site, which on 2026-11-13 still served a page frozen in spring 2023 ("Lent 2023", events dated 3/31/2023). `probe url` answers 403 on stawh.church; visit.py reads it. The bulletin page lists issues newest first as `/bulletin/<n>-<M-D-YYYY>/file`, which Chrome downloads (tools/browser_get.py) but `fetch:check` can't: on 2026-11-13 it reported "No PDF links found on bulletin page". The row is `unsupported` with `fetch_gap` `joomla-file-endpoint`, following the diocese's rule for Solutio sites with no printer listing.

## Not yet confirmed

The Chapel's address: the parish site says 876 Hempstead Avenue, the diocesan locator 875; see the chapel's record. Nothing else open.
