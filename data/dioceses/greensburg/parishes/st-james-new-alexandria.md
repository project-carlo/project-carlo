---
name: St. James Parish, New Alexandria
website: https://www.stjamesnewalexandria.org
bulletin_provider: parishes_online
provider_id: st-james-church-15670
publication: ['po-org:st-james-church-15670', 'lpi:0018000000QxC0DAAV', 'po-container:14/1661']
group: ''
revisit: 'fetch:check fails because parishesonline.com/organization/st-james-church-15670 renders blank (no selectedPublication link). Re-run it. If it still fails, ask the orchestrator whether to switch the row to a container-based read; the container 14/1661 itself is live.'
revisit_after: 2026-10-29
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
  note: 'Page 1 "Weekend Masses"; "Weekday Masses" Tuesday to Friday 8:00 a.m. Page 2 intentions (Sat 10/24
    4:30 p.m., Sun 10/25 9:30 a.m., "No Morning Mass" Monday to Friday this week) name no other church.
    grep "chapel" over all 12 pages finds nothing.'
- url: https://www.stjamesnewalexandria.org/bulletins
  seen: 2026-10-22
  note: 'The parish site''s bulletin page embeds the LPi publication widget for organization
    0018000000QxC0DAAV (plain fetch works). It serves no PDFs of its own.'
- url: https://parishesonline.com/organization/st-james-church-15670
  seen: 2026-10-22
  note: 'probe po: "St. James Catholic Church", 306 St James Lane, New Alexandria, website
    stjamesnewalexandria.org, container 14/1661, issues 2026-10-25, 10-18, 10-11, 10-04. The org page itself
    renders blank in headed Chrome (screenshot 2026-10-22), so fetch:check fails (see Not yet confirmed).
    LPi''s coordinates for it (40.2594, -79.3723) are about 15 km off; not used.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=217
  seen: 2026-10-22
  note: 'Directory: St. James Parish, 306 St. James Lane, New Alexandria, pastor Father Tyler J. Bandura,
    "Saturday: 4:30 p.m.; Sunday: 9:30 a.m.", no Partner Parishes, website stjamesnewalexandria.org.'
---

## Publisher

St. James Parish, New Alexandria (directory 217) publishes its own weekly bulletin through ParishesOnline, container 14/1661. The 25 October 2026 issue (read 2026-10-22 with `probe container` and `probe pdf`) names St. James alone ("SAINT JAMES CATHOLIC CHURCH / A Parish of the Diocese of Greensburg, Pennsylvania", 306 Saint James Lane) and has its own Mass schedule and staff. Its pastor, Fr. Tyler Bandura, is also pastor of St. Ambrose, Avonmore and St. Matthew, Saltsburg. Those two parishes publish a separate bulletin on partnerparishesmas.org (row `st-ambrose-and-st-matthew-avonmore`) that never mentions St. James in its masthead or schedule. The directory gives St. James no partner parishes. One bulletin for one parish, so one row.

## Worship sites

St. James church, New Alexandria. It is the only place in the 25 Oct Mass schedule and intentions, and the only site GCatholic (24133) and the directory list for this parish. GCatholic also lists a "Nativity of the Mother of God" on Shersburg Rd., New Alexandria (17406), a Byzantine church of another jurisdiction, not part of this parish.

## Website and bulletin provider

stjamesnewalexandria.org answers plain fetches. Its `/bulletins` page embeds the LPi publication widget with `id=0018000000QxC0DAAV`, which is the ParishesOnline organization st-james-church-15670 with container 14/1661 (`probe po`). Its newest issue is dated 2026-10-25, the coming Sunday. The provider is `parishes_online` and the provider_id is the org slug. All three ids (po-org, lpi, po-container) are recorded.

`fetch:check` on 2026-10-22 failed four times: "No matching anchor link found for parishes-online provider_id=st-james-church-15670". Both the org page and `/publication-page/st-james-church-15670` render blank in headed Chrome: a screenshot shows a white page and the text is empty. Our Lady of Grace's org page passed `fetch:check` in the same session, so ParishesOnline itself was up. Switching to `other` on the parish site was tried and failed ("No PDF links found on bulletin page", because the widget is rendered by JavaScript), so the row stays `parishes_online`.

## Not yet confirmed

The fetch does not work yet: the ParishesOnline organization page for this parish renders blank. The bulletin itself is live and current in container 14/1661. Next step (revisit 2026-10-29): re-run `fetch:check`. If the page is still blank, the row needs a way to read the container directly, which is a pipeline decision for the orchestrator.
