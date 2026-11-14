---
name: Sacred Heart of Jesus Korean Catholic Parish
website: https://ctkoreancatholic.org/bulletins/
bulletin_provider: unsupported
provider_id: ''
publication: []
group: ''
evidence:
- url: https://ctkoreancatholic.org/community-news/weekly-bulletin/2026-11-15-%ec%a3%bc%eb%b3%b4/
  seen: 2026-11-13
  note: 'Post "2026-11-15 주보" (bulletin), published 12 November 2026: one image, cdn.diocesanweb.org/beacon/ctkoreancatholic/wp-content/uploads/2026/11/11-15-2026.jpg,
    a page headed 공동체 소식 (community news) with the parish''s notices, including 25일 수요미사는 추수감사절 관계로 없습니다
    (no Wednesday Mass on the 25th for Thanksgiving). Read as an image; it has no text layer.'
- url: https://ctkoreancatholic.org/bulletins/
  seen: 2026-11-13
  quote: 최신 주보가 맨 위에 표시됩니다.
  note: The 주보 (Bulletins) page loads the weekly-bulletin category's posts by AJAX (Ajax Load More), newest
    first; the server-rendered category archive /category/weekly-bulletin/ shows the newest issue's image
    (11-15-2026.jpg on 2026-11-13).
- url: https://ctkoreancatholic.org/mass-times/
  seen: 2026-11-13
  quote: 미사 일정은 변경될 수 있습니다. 변경 사항은 주보 및 본당 공지를 통해 안내됩니다.
  note: 'Mass-times page: 주일미사 (Sunday Mass) 오전 10시 30분 (10:30 AM); 수요미사 (Wednesday Mass) 오후 8시 00분 (8:00
    PM); Holy Hour first Friday 8 PM; at 56 Hartford Ave, Wethersfield.'
bulletin_status: unsupported-format
fetch_gap:
  kind: board-post-images
  seen: 2026-11-13
  note: 'Each week''s 주보 is a WordPress post in the weekly-bulletin category whose page is a JPEG (2026-11-15
    post: wp-content/uploads/2026/11/11-15-2026.jpg). /bulletins/ lists the posts only by AJAX (Ajax Load
    More) and the category archive shows the newest image only as a CSS background-image, so page-images
    on https://ctkoreancatholic.org/category/weekly-bulletin/ found nothing (fetch:check 2026-11-13: ''No
    PDF links found on bulletin page''). A collector would follow the newest post in /category/weekly-bulletin/feed/
    and take its image.'
  url: https://ctkoreancatholic.org/community-news/weekly-bulletin/2026-11-15-%ec%a3%bc%eb%b3%b4/
---

## Publisher

The Sacred Heart of Jesus Korean Catholic Parish (예수성심 천주교 커네티컷 성당), a quasi-parish of the archdiocese since January 2019 (its church-history page), publishes its own weekly 주보 (bulletin) on its diocesanweb site ctkoreancatholic.org as one post per week in the `weekly-bulletin` category, each carrying a JPEG page. The 15 November 2026 post (published 12 November) has one image, `11-15-2026.jpg`, headed 공동체 소식 (community news), with the parish's own notices (feast-day greetings, the 29 November Advent talk, "25일 수요미사는 추수감사절 관계로 없습니다": no Wednesday Mass on the 25th for Thanksgiving). Christ the King Parish's bulletin, the other publisher in Wethersfield, does not mention this parish or its church.

## Worship sites

One: Sacred Heart Church, 56 Hartford Ave, Wethersfield (`sacred-heart-wethersfield`). The parish's Mass-times page gives Sunday 10:30 AM and Wednesday 8:00 PM there, and its church-history page says that in 2001 its Masses, until then at St. Lawrence and Sacred Heart, were consolidated at Sacred Heart (Wethersfield). The directory (36) lists the Korean parish at 56 Hartford Avenue, and GCatholic's 'Sacred Heart', 56 Hartford Ave. (22236), is the same building. The Hartford Courant's 7 May 2017 list says Sacred Heart parish merged with Corpus Christi and St. Luke to form Christ the King; the building is now this quasi-parish's church, and Christ the King's schedule (Incarnation and Corpus Christi) does not include it.

## Website and bulletin provider

`unsupported`, with a `fetch_gap` of kind `board-post-images` (the same problem as a MangBoard site elsewhere: each issue is a weekly post whose page is a JPEG). The Bulletins page (/bulletins/) loads its posts by AJAX, so the fetcher sees none; the category archive /category/weekly-bulletin/ shows the newest issue's image only as a CSS background, and `fetch:check` on 2026-11-13 with recipe `page-images https://ctkoreancatholic.org/category/weekly-bulletin/` failed ("No PDF links found on bulletin page"). The category's RSS feed (/category/weekly-bulletin/feed/) lists each week's post newest first with its image, which a collector could follow. The bulletin is image-only (Korean) and carries notices rather than a Mass schedule.

## Not yet confirmed

Whether older issues ran to more than one image per week (the archive's June 2026 posts used one large JPEG each) was not checked.
