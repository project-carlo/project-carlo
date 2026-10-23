---
name: St. James Parish, New Alexandria
website: https://www.stjamesnewalexandria.org
bulletin_provider: other
provider_id: page-pdfs https://parishesonline.com/publicationWidget?type=bulletin&color=gray&id=0018000000QxC0DAAV filename=*B.pdf
publication: ['po-org:st-james-church-15670', 'lpi:0018000000QxC0DAAV', 'po-container:14/1661']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/1661/20261025B.pdf
  seen: 2026-10-22
  quote: SAINT JAMES CATHOLIC CHURCH A Parish of the Diocese of Greensburg, Pennsylvania
  note: 'Page 1 of the 25 Oct 2026 issue ("OCTOBER 25, 2026 | THE THIRTIETH SUNDAY IN ORDINARY TIME"):
    "306 Saint James Lane New Alexandria, PA 15670", "www.stjamesnewalexandria.org", "Father Bandura,
    Pastor". Names St. James alone. Page 12 footer: "St. James Church | 14-1661".'
- url: https://container.parishesonline.com/bulletins/14/1661/20261025B.pdf
  seen: 2026-10-22
  quote: Saturday | 4:30 p.m. Anticipated Mass Sunday | 9:30 a.m. | Livestreamed
  note: Page 1 "Weekend Masses"; "Weekday Masses" Tuesday to Friday 8:00 a.m. Page 2 intentions (Sat 10/24
    4:30 p.m., Sun 10/25 9:30 a.m., "No Morning Mass" Monday to Friday this week) name no other church.
    grep "chapel" over all 12 pages finds nothing.
- url: https://www.stjamesnewalexandria.org/bulletins
  seen: 2026-10-22
  note: The parish site's bulletin page embeds the LPi publication widget for organization 0018000000QxC0DAAV
    (plain fetch works). It serves no PDFs of its own.
- url: https://parishesonline.com/organization/st-james-church-15670
  seen: 2026-10-22
  note: 'probe po: "St. James Catholic Church", 306 St James Lane, New Alexandria, website stjamesnewalexandria.org,
    container 14/1661, issues 2026-10-25, 10-18, 10-11, 10-04. The org page itself renders blank in headed
    Chrome (screenshot 2026-10-22), so the org-page fetch fails (the working widget recipe is described below). LPi''s coordinates for
    it (40.2594, -79.3723) are about 15 km off; not used.'
- url: https://parishesonline.com/organization/st-james-church-15670
  seen: 2026-10-23
  note: 'Full fetch:check of the diocese on 2026-10-23: 47 rows ok, this one resolve_failed again ("No
    matching anchor link found for parishes-online provider_id=st-james-church-15670"). In headed Chrome
    the org page''s title loads ("St. James Catholic Church - New Alexandria, PA | Parishes Online") but
    the body is empty and the page throws "Failed to construct ''URL'': Invalid URL"; Our Lady of Grace''s
    org page, opened the same way, renders 14 selectedPublication links and no error. The LPi geo-search
    at the org''s coordinates lists only this one St. James organization. The parish site''s widget (https://parishesonline.com/publicationWidget?type=bulletin&color=gray&id=0018000000QxC0DAAV)
    renders in headed Chrome with links to publication-page/st-james-church-15670?selectedPublication=.../14/1661/20261025B.pdf
    (and 10-18, 10-11, 10-04). Tried as `other` with `page-pdfs <widget URL>`: it resolved the 25 Oct
    link but downloaded the publication-page wrapper (not_pdf), because the resolver does not unwrap the
    selectedPublication parameter. container.parishesonline.com/bulletins/14/1661/ answers 403 (no listing).
    Row restored to parishes_online at that point.'
- url: https://parishesonline.com/publicationWidget?type=bulletin&color=gray&id=0018000000QxC0DAAV
  seen: 2026-10-23
  note: 'After adding selectedPublication viewer unwrapping, fetch:check with provider other and recipe
    page-pdfs on this widget, filename=*B.pdf, succeeded: source_url
    https://container.parishesonline.com/bulletins/14/1661/20261025B.pdf, url_date 2026-10-25,
    25,335,309 bytes, status ok. The widget lists current issues even though the org page is broken.
    Recorded its rendered page for the offline fetch replay regression test.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=217
  seen: 2026-10-22
  note: 'Directory: St. James Parish, 306 St. James Lane, New Alexandria, pastor Father Tyler J. Bandura,
    "Saturday: 4:30 p.m.; Sunday: 9:30 a.m.", no Partner Parishes, website stjamesnewalexandria.org.'
promoted: 2026-10-23
---

## Publisher

St. James Parish, New Alexandria (directory 217) publishes its own weekly bulletin through ParishesOnline, container 14/1661. The 25 October 2026 issue (read 2026-10-22 with `probe container` and `probe pdf`) names St. James alone ("SAINT JAMES CATHOLIC CHURCH / A Parish of the Diocese of Greensburg, Pennsylvania", 306 Saint James Lane) and has its own Mass schedule and staff. Its pastor, Fr. Tyler Bandura, is also pastor of St. Ambrose, Avonmore and St. Matthew, Saltsburg. Those two parishes publish a separate bulletin on partnerparishesmas.org (row `st-ambrose-and-st-matthew-avonmore`) that never mentions St. James in its masthead or schedule. The directory gives St. James no partner parishes. One bulletin for one parish, so one row.

## Worship sites

St. James church, New Alexandria. It is the only place in the 25 Oct Mass schedule and intentions, and the only site GCatholic (24133) and the directory list for this parish. GCatholic also lists a "Nativity of the Mother of God" on Shersburg Rd., New Alexandria (17406), a Byzantine church of another jurisdiction, not part of this parish.

## Website and bulletin provider

stjamesnewalexandria.org answers plain fetches. Its `/bulletins` page embeds the LPi publication widget with `id=0018000000QxC0DAAV`, which is the ParishesOnline organization st-james-church-15670 with container 14/1661 (`probe po`). All three ids (po-org, lpi, po-container) are recorded.

The organization page renders blank and throws "Failed to construct 'URL': Invalid URL", so the normal `parishes_online` resolver fails. The widget still lists each current issue as a `publication-page?selectedPublication=<PDF>` link. The `other` resolver now unwraps those viewer links to their container PDFs. The provider is `other`, pinned to `page-pdfs https://parishesonline.com/publicationWidget?type=bulletin&color=gray&id=0018000000QxC0DAAV filename=*B.pdf`. The filename filter keeps weekly bulletins (`YYYYMMDDB.pdf`) and excludes special inserts. The recipe follows the widget's issue list each week without relying on the broken org page or a fixed issue date.

Live `fetch:check` on 2026-10-23 succeeded and downloaded `14/1661/20261025B.pdf` (url_date 2026-10-25, 25,335,309 bytes). The rendered widget page is also recorded in `tests/fixtures/fetch/st-james-new-alexandria.json.gz` for offline replay against the live CSV recipe.

## Not yet confirmed

Nothing about bulletin access. The organization page remains broken; keep the working widget recipe pinned.
