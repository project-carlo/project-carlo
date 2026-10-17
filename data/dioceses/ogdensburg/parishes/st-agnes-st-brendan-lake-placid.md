---
name: St. Agnes & St. Brendan's
website: https://stagneslakeplacid.com
bulletin_provider: other
provider_id: linked-issue-page https://stagneslakeplacid.com/bulletin
publication: ['url:https://www.church-bulletin.org/saint-agnes-saint-brendan-lake-placid-ny-12946', 'url:https://stagneslakeplacid.com/bulletin']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-agnes-saint-brendan-lake-placid-ny-12946/2026-09-20.pdf
  seen: 2026-09-30
  quote: You are invited, welcomed, accepted, loved, and respected at St. Agnes and St. Brendan Catholic
    Churches
  note: Page 1 (cover) of the 20 September 2026 issue (text layer). Its header block reads "ST. AGNES
    & ST. BRENDAN'S, Rev. JoseKaniyankunnel John, HGN, Pastor, 169 Hillcrest Ave., Lake Placid, NY 12946".
    One bulletin, both churches.
- url: https://www.church-bulletin.org/bulletin/saint-agnes-saint-brendan-lake-placid-ny-12946/2026-09-20.pdf
  seen: 2026-09-30
  quote: 4047 St. Agnes & St. Brendan, Lake Placid, NY (B) John Patrick Publishing Co.
  note: Page 6 footer of the same issue, the publisher's id for this bulletin (4047), matching the church-bulletin.org/?id=4047
    link on the parish site.
- url: https://www.church-bulletin.org/bulletin/saint-agnes-saint-brendan-lake-placid-ny-12946/2026-09-20.pdf
  seen: 2026-09-30
  quote: SAINT BRENDAN’S CHURCH25 Church St, Keene, NY 12942
  note: Page 2 of the same issue, the Mass intentions block. It lists "ST. AGNES CHURCH 2338 Saranac Ave,
    Lake Placid, NY", "SAINT BRENDAN’S CHURCH 25 Church St, Keene, NY 12942" and "ELDERWOOD AT UIHLEIN,
    125 Old Military Road, Lake Placid, NY 12946" (text layer joins "CHURCH" and "25").
- url: https://www.church-bulletin.org/bulletin/saint-agnes-saint-brendan-lake-placid-ny-12946/2026-09-27.pdf
  seen: 2026-09-30
  note: 'Latest issue (27 September 2026, 6 pages) is scanned images with no text layer, so recheck cannot
    find quotes in it; read as images with parish-site-access render.py. Page 1 cover: "ST. AGNES & ST.
    BRENDAN''S". Page 2: Saturday 26 September 5:30 PM St. Agnes; Sunday 27 September 8:00 AM and 10:00
    AM St. Agnes; Saturday 26 September 4:00 PM (rosary and reconciliation 3:30 PM) St. Brendan''s, Keene.
    The 4 October Sunday also lists an 11:30 AM "Mountain Mass" (the annual outdoor Mass at Cobble Lookout).'
- url: https://stagneslakeplacid.com/bulletin
  seen: 2026-09-30
  quote: 'BULLETINS: We invite you to read recent bulletins'
  note: The parish site (Squarespace) Bulletin page links church-bulletin.org/?id=4047, which redirects
    to church-bulletin.org/saint-agnes-saint-brendan-lake-placid-ny-12946, and lists one PDF per Sunday
    (2026-08-02 to 2026-09-27 read on 2026-09-30). The page also links "St. Agnes Parishioners" and "St.
    Brendan's Parishioners" online giving.
- url: https://www.church-bulletin.org/saint-agnes-saint-brendan-lake-placid-ny-12946
  seen: 2026-09-30
  quote: Saint Agnes & Saint Brendan Bulletin
  note: 'John Patrick Publishing''s archive page for the parish: "Latest Edition September 27, 2026 Bulletin".'
promoted: 2026-09-30
---

## Publisher

St. Agnes (Lake Placid) and St. Brendan's (Keene) publish **one** weekly bulletin, printed by
John Patrick Publishing (JPP) as its bulletin 4047 and archived one PDF per Sunday at
`church-bulletin.org/bulletin/saint-agnes-saint-brendan-lake-placid-ny-12946/<YYYY-MM-DD>.pdf`.
The 20 September 2026 issue (6 pages, text layer) has a cover addressed to "St. Agnes and
St. Brendan Catholic Churches" under the header "ST. AGNES & ST. BRENDAN'S", pastor Rev.
Jose Kaniyankunnel John, HGN, parish office 169 Hillcrest Ave., Lake Placid. Page 2 lists Mass
intentions for St. Agnes Church (2338 Saranac Ave), Saint Brendan's Church (25 Church St,
Keene) and Elderwood at Uihlein. The 27 September issue (the latest on 2026-09-30; 4 October
was still 404) has the same structure but is scanned images.

The directory (rcdony.org) lists St. Agnes (`directory:lake-placid`) and St. Brendan's
(`directory:keene`) as two separate entries, both with the office phone 518-523-2200 and Fr.
Jose Kaniyankunnel John as pastor, and gives St. Brendan's no website. The bulletin, not the
directory, settles that they are one row. The 20 September issue's "Autumn Outdoor Mass" notice (annual Mountain Mass at Cobble Lookout, 4 October 2026, a
one-mile trail off County Road 72) is a one-off event, not a worship site.

## Worship sites

Two: St. Agnes, Lake Placid (`st-agnes-lake-placid`: Saturday 5:30 PM, Sunday 8:00 and 10:00
AM, weekdays Monday, Wednesday, Thursday and Friday 8:30 AM and Tuesday 5:30 PM) and St. Brendan's, Keene (`st-brendans-keene`: Saturday 4:00 PM, with
rosary and reconciliation at 3:30 PM), as printed on page 2 of the 27 September 2026 issue.

The bulletin also lists a Sunday 1:30 PM Mass at Elderwood at Uihlein, 125 Old Military Road,
Lake Placid (a nursing and rehabilitation facility; the Lake Placid News religious directory
gives "185 Old Military Road"). It is in no roster and nothing read says whether it is open
to the public, so it is **not** recorded as a church: it is a care-home Mass. Worth an inquiry
if the pipeline wants care-home Masses.

## Website and bulletin provider

`stagneslakeplacid.com` is the directory's website for St. Agnes; `probe url` on the bare
domain answers 404 but `/bulletin` loads (200) and links the JPP archive. Provider is `other`:
JPP's `church-bulletin.org` pages list the PDFs (see the parish-site-access skill's "Other
bulletin hosts"), fetchable without a browser. Publication ids are the archive page and the
parish's own bulletin page; there is no ParishesOnline, eCatholic or Discover Mass id. Several
issues are image-only (13 and 6 September, 27 September; the 20 September and 16 August ones
have a text layer), so the pipeline will need to read some weeks as images.

Recipe `linked-issue-page https://stagneslakeplacid.com/bulletin`, pinned after `fetch:check` on 2026-10-17 picked church-bulletin.org's `2026-10-18.pdf`, this week's issue (`current`).

## Not yet confirmed

- Whether Elderwood at Uihlein's Sunday Mass is public (see above).
- The Lake Placid News directory says St. Brendan's Saturday Mass is 4 p.m. and St. Agnes's
  pastor is "The Rev. John Yonkovig" (now Pastor Emeritus in the bulletin); it is out of date.
