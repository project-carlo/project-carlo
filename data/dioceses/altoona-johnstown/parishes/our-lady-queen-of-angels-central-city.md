---
name: Our Lady Queen of Angels Parish, Central City
website: https://www.ladyqueenofangels.org
bulletin_provider: discover_mass
provider_id: our-lady-queen-of-angels-central-city-pa
publication: ['discovermass:our-lady-queen-of-angels-central-city-pa']
group: Rev. Aron M. Maghsoudi (north Somerset County)
evidence:
- url: https://discovermass.com/church/our-lady-queen-of-angels-central-city-pa/
  seen: 2026-10-21
  quote: Current Bulletin
  note: 'Discover Mass page of Our Lady Queen of Angels; its Bulletins tab lists "Current Bulletin Oct 18, 2026" and weekly issues back to 2 Aug 2026 (Oct 11, Oct 4, Sep 27 ...). I read the 18 Oct 2026 issue (29th Sunday in Ordinary Time, 6 pages) through its download link (tokenised, so not cited as a URL). Its page 1 header is "THE CATHOLIC CHURCHES OF QUEEN OF ANGELS, HOLY FAMILY, ALL SAINTS", with Fr. Aron Maghsoudi as pastor and the rectory and "Worship Site" blocks for Hooversville (321 Sugar Street), Boswell (325 Quemahoning Street) and Central City (738 Sunshine Avenue; Church (Sacred Heart) and Chapel (St. John, 162 Wheeler Street)). Page 2 has the line (text layer garbled) "OurL adyQ ueen of Angels,C entral City, A ll Saints Parish,B oswell, H olyF amily, Hooversville". The text layer is garbled, so the quote above is of the page, not the PDF.'
- url: https://discovermass.com/church/holy-family-hooversville-pa/
  seen: 2026-10-21
  quote: Shucks! There are no bulletins available.
  note: Holy Family, Hooversville has its own Discover Mass page with an empty Bulletins tab, so it is not a separate live channel.
- url: https://discovermass.com/church/all-saints-boswell-pa/
  seen: 2026-10-21
  quote: Shucks! There are no bulletins available.
  note: All Saints, Boswell has its own Discover Mass page with an empty Bulletins tab, so it is not a separate live channel.
- url: https://www.webparish.com/aj/AllSaints/index.php
  seen: 2026-10-21
  quote: This site maintained by
  note: 'Old diocesan webparish.com stub for All Saints (325 Quemahoning St., allsaints.parish@verizon.net): a generic Catholic-links page with no Mass times or bulletin (opened in Chrome; curl gets a 406 from Mod_Security). The Holy Family stub (/aj/HolyFamilyHooversville/index.php) is the same. Neither is a bulletin source.'
- url: https://www.ladyqueenofangels.org/bulletin/
  seen: 2026-10-21
  note: 'The parish site (WordPress, behind Cloudflare: curl gets 403, headed Chrome opens it) has a Bulletin page of year accordions "Bulletin 2026" ... "Bulletin 2015" (WP File Download tree, loaded by script). I did not open them; the Discover Mass listing above is the channel used.'
- url: https://www.ladyqueenofangels.org/
  seen: 2026-10-21
  quote: 'Sunday: 8AM (Sacred Heart) | 10:30AM (St. John)'
  note: Home page Mass times (rendered in Chrome). The site names Our Lady Queen of Angels at 738 Sunshine Avenue and does not mention All Saints or Holy Family on the home page.
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'Directory: All Saints (Boswell), Holy Family (Hooversville) and Our Lady Queen of Angels (Central City, with its two worship sites) are three parishes with no homepage for the first two; the batch task names Rev. Aron M. Maghsoudi as pastor of all three, which the bulletin masthead matches.'
---

## Publisher

Three canonical parishes (Our Lady Queen of Angels, Central City; All Saints, Boswell; Holy Family, Hooversville) share the pastor Rev. Aron M. Maghsoudi and publish **one** weekly bulletin through J.S. Paluch / Discover Mass. The 18 October 2026 issue (read 2026-10-21, 6 pages) is headed "THE CATHOLIC CHURCHES OF QUEEN OF ANGELS, HOLY FAMILY, ALL SAINTS". It lists the three rectories and the worship sites, and its week of Masses is arranged by site: "OLQA Church" (Sacred Heart), "OLQA Chapel" (St. John), "Holy Family" and "All Saints" (its Sunday 25 October column lists 8:00 am and 10:30 am sites and 10:30 am at All Saints; the Saturday vigil, 4:00 pm, is at Holy Family). The cover page also gives confessions: "Following 4pm Mass at Holy Family", "Following 8am Mass at Sacred Heart Site", "10:00-10:20 am at Saint John Site", "10:00 am All Saints Church". (Wording is read from a garbled text layer, so spacing in the original differs.) Page 2 closes with the line naming all three: Our Lady Queen of Angels, Central City; All Saints Parish, Boswell; Holy Family, Hooversville.

The Discover Mass listing for this bulletin is under the Central City page; the Boswell and Hooversville Discover Mass pages exist but say "no bulletins available", and their old diocesan webparish.com stubs carry no bulletin or Mass times. There is no live separate channel for either, so the three are one row (the Boswell and Hooversville roster entries are worship sites of this row, not parishes of their own).

## Worship sites

Four churches, all in the 18 October bulletin's Mass schedule: Sacred Heart (OLQA Church, 738 Sunshine Ave, Central City), St. John (OLQA Chapel, 162 Wheeler St, Central City), Holy Family (321 Sugar St, Hooversville) and All Saints (325 Quemahoning St, Boswell). Nothing the directory or GCatholic lists for these parishes is left out: GCatholic 23822 ("Our Lady Queen of Angels", 738 Sunshine Ave) is the Sacred Heart building, GCatholic 23896 ("St. John" chapel) is the Wheeler Street chapel the diocese's directory has as "Saint John Worship Site".

## Website and bulletin provider

`website` is the parish site https://www.ladyqueenofangels.org (the directory's homepage for the Central City parish; GCatholic lists the same for the St. John chapel). It is behind Cloudflare, so curl gets 403 and `fetch:check` reads the bulletin from Discover Mass instead: `bulletin_provider: discover_mass`, `provider_id: our-lady-queen-of-angels-central-city-pa` (the church slug on discovermass.com), and `publication: discovermass:our-lady-queen-of-angels-central-city-pa`. The two other Discover Mass slugs (holy-family-hooversville-pa, all-saints-boswell-pa) have no bulletins and are not recorded as publications.

## Not yet confirmed

Whether the parish's own Bulletin page (WP File Download accordion) carries the same issues; not needed while Discover Mass is current. If Discover Mass lapses, open "Bulletin 2026" on https://www.ladyqueenofangels.org/bulletin/ in headed Chrome and point an `other` recipe at it.
