---
name: 'Saint John Gualbert Cathedral Parish and Saint Patrick Parish, Johnstown'
website: https://www.stjohngualbert.org/welcome
bulletin_provider: other
provider_id: 'page-pdfs https://www.stjohngualbert.org/welcome#WeeklyBulletin'
publication: ['url:https://www.stjohngualbert.org/welcome']
group: Very Rev. Matthew Baum (Johnstown)
evidence:
- url: https://irp.cdn-website.com/747b2262/files/uploaded/2026-10-18.pdf
  seen: 2026-10-21
  quote: Saint Patrick Church
  note: 'Page 1 of the 18 October 2026 issue (12 pages, 16 MB; "Twenty Ninth Sunday in Ordinary Time"). The cover carries two Mass-time blocks. Block one: "Mass Times: Saturday 6PM Sunday 7AM, 11AM, 5PM ... Saint John Gualbert Cathedral ... V. Rev Matthew Baum, Rector". Block two: "Mass Times: Saturday 4PM Sunday 9AM Thursday 8AM ... Saint Patrick Church ... V. Rev Matthew Baum, Pastor". One bulletin therefore names both churches (the text layer has them on separate lines, so the quote is the heading alone).'
- url: https://www.stjohngualbert.org/welcome
  seen: 2026-10-21
  quote: St. John Gualbert Cathedral & St. Patrick Catholic Parishes
  note: 'The parish site''s page header (a Duda site). Its "Weekly Bulletin" section shows "Current Bulletin 2026-10-18" and past issues 2026-10-11, 10-04, 09-27 and 09-20, each a PDF under irp.cdn-website.com/747b2262/files/uploaded/. The page says "our combined activity calendar for both parishes" and carries both parishes'' addresses (cathedral 117 Clinton Street, St. Patrick 609 Park Ave) and offices.'
- url: http://stpatrickjtown.com
  seen: 2026-10-21
  note: 'The St. Patrick domain printed on the bulletin cover (the cover reads "http://stpatrickjtown.com") answers 200 after redirecting to https://www.stjohngualbert.org/ (checked with probe url and curl -L). So St. Patrick has no separate site or bulletin channel of its own: the redirect is a fold-in, not a squat, because the target is the pastor''s own parish site, whose title is "St John Gualbert Cathedral & St Patrick Parish".'
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'The directory lists the cathedral (117 Clinton Street, Johnstown 15901, homepage http://www.stjohngualbert.org/) and St. Patrick (609 Park Avenue, 15902, no homepage) as two parishes. The bulletin cover names Very Rev. Matthew Baum as rector of one and pastor of the other, matching the lead.'
- url: https://stjohngualbert.flocknote.com/SJSP
  seen: 2026-10-21
  note: 'The site''s Flocknote sign-up ("SJSP", text SJGC to 84576) serves both parishes. A sign-up page, not a bulletin source.'
---

## Publisher

The cathedral parish publishes one weekly bulletin on its own Duda site, and it covers Saint
Patrick Parish as well. The 18 October 2026 issue (page 1) prints two Mass-time blocks on its
cover: "Saint John Gualbert Cathedral" ("V. Rev Matthew Baum, Rector": Saturday 6PM; Sunday
7AM, 11AM, 5PM; weekdays 7AM and 12:05PM) and "Saint Patrick Church" ("V. Rev Matthew Baum,
Pastor": Saturday 4PM; Sunday 9AM; Thursday 8AM). The site header reads "St. John Gualbert
Cathedral & St. Patrick Catholic Parishes", and St. Patrick's own domain on the bulletin cover
(stpatrickjtown.com) redirects to the cathedral site. I found no separate St. Patrick
bulletin. The directory lists no St. Patrick homepage. That is one bulletin, so one row.

## Worship sites

Two: the cathedral (117 Clinton Street) and St. Patrick (609 Park Avenue), each named with its
own Mass times on the 18 October cover. Nothing else is listed for this pastor in the
directory.

GCatholic has the cathedral on its own page (churches/northamerica/2438, Plus Code
87G383GM+4R), not in the roster that was fetched; the church record cites it.

## Website and bulletin provider

`bulletin_provider: other`, website https://www.stjohngualbert.org/welcome (the page that
holds the "Weekly Bulletin" list; the home page has only a link to it). `fetch:check` on
2026-10-21 resolved it with `page-pdfs https://www.stjohngualbert.org/welcome#WeeklyBulletin`
to https://irp.cdn-website.com/747b2262/files/uploaded/2026-10-18.pdf, current (url date
2026-10-18, 16 MB, status ok); that recipe is recorded as `provider_id`. File names are the
Sunday date but not zero-padded every time (`2026-9-27.pdf`). Publication id is the page URL,
as there is no provider id.

## Not yet confirmed

Only 3 of 12 pages of the 18 October issue have a text layer; the Mass times of the cover
page are enough to settle the structure. Whether weekday Masses at St. Patrick beyond Thursday
exist is not stated in what I read.
