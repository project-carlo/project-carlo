---
name: Our Lady of Lourdes, West Orange
website: https://www.lourdeswestorange.org/index.php/sunday-bulletins
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.lourdeswestorange.org/index.php/sunday-bulletins']
group: ''
evidence:
- url: https://www.lourdeswestorange.org/images/bulletin2026/bulletin110126.pdf
  seen: 2026-11-03
  quote: Rev. James Ferry, Pastor
  note: '1 November 2026 issue, 6 pages. Page 1: OUR LADY OF LOURDES CHURCH, One Eagle Rock Avenue, West
    Orange, New Jersey 07052; Sunday, November 1, 2026 – All Saints; Mass Schedule @ Main Church: Saturday
    Evening 5:30 pm, Sunday Morning 7:30, 9:30, 11:30 am; Weekday Monday – Friday 8:30 am. Page 6 footer:
    151D (CK) • Our Lady of Lourdes Church • West Orange, NJ … Bon Venture Services, LLC.'
- url: https://www.lourdeswestorange.org/index.php/sunday-bulletins
  seen: 2026-11-03
  quote: November 1, 2026 - Feast of All Saints
  note: Joomla page listing issues January 2025 to 1 November 2026, each a weblink.go redirect to /images/bulletin2026/bulletin<MMDDYY>.pdf.
- url: http://sponsors.bonventure.net/?page=151D
  seen: 2026-11-03
  note: Redirects to http://www.bonventure.net/; no listing for code 151D.
research:
- method: fetch:check with default page-pdfs on the Sunday Bulletins page; probe get of /images/bulletin2026/
    and sponsors.bonventure.net/?page=151D
  url: https://www.lourdeswestorange.org/index.php/sunday-bulletins
  checked: '2026-11-03'
  outcome: unsupported-format
  next_action: Read the issues through a collector that follows Joomla weblink.go redirects, or find a
    direct PDF listing
  retry_when: A collector for joomla-weblink-redirect lands, or the site links PDFs directly
bulletin_status: available
fetch_gap:
  kind: joomla-weblink-redirect
  seen: 2026-11-03
  note: The Sunday Bulletins page links each issue only through Joomla weblink.go redirects (e.g. weblink/484-november-1-2026-feast-of-all-saints?…&task=weblink.go
    -> /images/bulletin2026/bulletin110126.pdf); page-pdfs sees no issue PDFs and picks /images/pdf/funeralsmemorial2026.pdf.
    Bon Venture code 151D has no sponsors listing.
  url: https://www.lourdeswestorange.org/images/bulletin2026/bulletin110126.pdf
publication_reviews:
- parish: st-joseph-west-orange
  decision: separate
  evidence:
  - url: https://www.lourdeswestorange.org/images/bulletin2026/bulletin110126.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Our Lady of Lourdes Church, West Orange alone, with its own
      Mass schedule and pastor Rev. James Ferry; Bon Venture 151D.
  - url: https://container.parishesonline.com/bulletins/04/1242/20261101B.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names St. Joseph, West Orange alone, with its own Mass schedule;
      LPi container 04/1242.
- parish: st-raphael-livingston
  decision: separate
  evidence:
  - url: https://www.lourdeswestorange.org/images/bulletin2026/bulletin110126.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Our Lady of Lourdes Church, West Orange alone, with its own
      Mass schedule and pastor Rev. James Ferry; Bon Venture 151D.
  - url: https://www.church-bulletin.org/bulletin/the-parish-family-of-saint-raphael-church-livingston-nj-07039/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names St. Raphael Church, Livingston alone, with its own Mass schedule;
      John Patrick id 526.
---

## Publisher

Our Lady of Lourdes, West Orange, publishes a weekly bulletin printed by Bon Venture Services and posted on its own site. I read the 1 November 2026 issue (bulletin110126.pdf, 6 pages, text layer): page 1 masthead 'OUR LADY OF LOURDES CHURCH, One Eagle Rock Avenue, West Orange, New Jersey 07052', 'Sunday, November 1, 2026 – All Saints', 'Rev. James Ferry, Pastor', with one Mass schedule 'Mass Schedule @ Main Church'. The page 6 ad footer reads '151D (CK) • Our Lady of Lourdes Church • West Orange, NJ … Bon Venture Services, LLC'.

## Worship sites

- Our Lady of Lourdes Church, One Eagle Rock Avenue (`our-lady-of-lourdes-west-orange`): Saturday 5:30 PM; Sunday 7:30, 9:30, 11:30 AM; Monday-Friday 8:30 AM.

The directory (212) and GCatholic (18581) list only this church; the bulletin names no other worship site. Its pastor (Rev. James Ferry) is not the pastor of St. Joseph, West Orange.

## Website and bulletin provider

https://www.lourdeswestorange.org/ is a Joomla site. Its 'Sunday Bulletins' page (index.php/sunday-bulletins) lists every issue from January 2025 to 'November 1, 2026 - Feast of All Saints', each linked as a Joomla weblink (index.php/component/weblinks/weblink/484-november-1-2026-feast-of-all-saints?catid=24&Itemid=101&task=weblink.go) that redirects to /images/bulletin2026/bulletin<MMDDYY>.pdf. The page has no direct PDF links to the issues, and /images/bulletin2026/ gives no listing (44 bytes). Bon Venture code 151D has no sponsors.bonventure.net listing (?page=151D redirects to bonventure.net), as the playbook says for lettered codes.

Fetch check (2026-11-03, headed): resolved `page-pdfs on …/sunday-bulletins: first-listed` and picked /images/pdf/funeralsmemorial2026.pdf, a funeral-memorial list (freshness stale, 196 days), not the bulletin. So the row is `unsupported` with `fetch_gap` kind `joomla-weblink-redirect` until a collector follows weblink.go links; the publication id is the bulletin page.

## Not yet confirmed

Nothing about the parish. When a collector can follow Joomla weblink redirects, set the provider to `other` with that recipe, rerun fetch:check and clear the gap.
