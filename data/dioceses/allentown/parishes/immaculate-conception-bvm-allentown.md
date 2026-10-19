---
name: Immaculate Conception BVM Church
website: http://www.immaculateconceptionallentown.org/news.html
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:http://www.immaculateconceptionallentown.org/latestbulletin.pdf']
group: Immaculate Conception BVM Parish (same pastor as Sacred Heart of Jesus)
evidence:
- url: http://www.immaculateconceptionallentown.org/latestbulletin.pdf
  seen: 2026-10-18
  quote: Immaculate Conception BVM Church
  note: 'Page 1 masthead of the issue dated "29th Sunday in Ordinary Time OCTOBER 18, 2026" (file Last-Modified
    13 Oct 2026): 501 Ridge Avenue, Rev. John M. Gibbons, Pastor; MASS SCHEDULE Saturdays 4:00 PM, Sundays
    9:00 AM (English) and 10:30 AM (Polish), Daily 8:00 AM. This file is overwritten weekly, so the quote
    is good only until the next issue.'
- url: http://www.immaculateconceptionallentown.org/latestbulletin.pdf
  seen: 2026-10-18
  quote: SHRINE OF OUR LADY OF GUADALUPE
  note: Same page; "Mass & Novena Mondays 8:00 AM" at the shrine, which is inside this church (the diocesan
    map says the church was "Declared National Shrine of Our Lady of Guadalupe").
- url: http://www.immaculateconceptionallentown.org/news.html
  seen: 2026-10-18
  quote: Please click HERE for our Latest Bulletin
  note: The parish site's News page links latestbulletin.pdf ("Latest Bulletin") and archive.pdf ("Bulletin
    Archive"). The home page does not link the bulletin, so the News page is the website.
promoted: 2026-10-19
---

## Publisher

Immaculate Conception BVM, 501 Ridge Avenue, publishes its own bulletin as one PDF that is
overwritten each week (`latestbulletin.pdf`). The issue read on 18 October 2026 is dated
"29th Sunday in Ordinary Time, October 18, 2026"; its page-1 masthead names this church
alone, with Masses Saturday 4 PM, Sunday 9 AM (English) and 10:30 AM (Polish), and daily
8 AM.

Its pastor, Fr. John M. Gibbons, and assistant, Fr. David J. Kozak, also serve Sacred
Heart of Jesus (diocesan map), but Sacred Heart publishes a separate bulletin on its own
site (`sacred-heart-of-jesus-allentown`): the 18 October issues are different documents
with different mastheads and schedules. Two rows.

## Worship sites

- `immaculate-conception-bvm-allentown`, 501 Ridge Avenue (also the National Shrine of
  Our Lady of Guadalupe).

GCatholic lists "Our Lady of Mercy" (Syriac rite) at the same address, 501 Ridge Ave.;
that is a Syriac Catholic community, excluded as `other-jurisdiction`
(`our-lady-of-mercy-syriac-allentown`). This bulletin does not mention it.

## Website and bulletin provider

`other`, self-hosted on the parish's own static site (JMS). The website is the News page
because that is the only page linking the PDF. The PDF keeps one address, so the pipeline
has to fetch it again each week and tell issues apart by content.

Fetch check (2026-10-19, `fetch_check` on a temporary CSV of these records): the resolver picked latestbulletin.pdf, the first PDF on the News page (the 18 October 2026 issue on that day). Its recipe, `page-pdfs`, is recorded as `provider_id`.

## Not yet confirmed

Nothing.
