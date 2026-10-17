---
name: Saint John Parish
website: https://www.churchofstjohn.com
bulletin_provider: other
provider_id: page-pdfs https://www.churchofstjohn.com/Bulletin
publication: ['url:https://www.churchofstjohn.com/Bulletin']
group: Saint John Parish
evidence:
- url: https://d11n7da8rpqbjy.cloudfront.net/creditprimeusa/239014714838October_18_2026.pdf
  seen: 2026-10-16
  quote: '5171 Milford Road East Stroudsburg, PA 18302-9106 Phone: 570-223-9144 Website: www.churchofstjohn.com
    October 18, 2026 / Twenty-ninth Sunday in Ordinary Time'
  note: Page 1 of the 18 October 2026 issue, headed "Church of St. John". One church.
- url: https://d11n7da8rpqbjy.cloudfront.net/creditprimeusa/239014714838October_18_2026.pdf
  seen: 2026-10-16
  quote: Saturday – 4:00 PM Sunday – 8:30 AM, 11:00 AM, and First Sunday of each month at 1:30 PM (Spanish
    Mass)
- url: https://www.churchofstjohn.com/Bulletin
  seen: 2026-10-16
  note: The parish site (Kartra; plain fetches get 403, read with visit.py) links "This Week's Bulletin"
    to /Bulletin, which lists the PDFs on a Kartra CloudFront bucket (d11n7da8rpqbjy.cloudfront.net/creditprimeusa/<number><Month>_<D>_<YYYY>.pdf),
    newest October_18_2026.
---

## Publisher

The Church of St. John publishes its own weekly bulletin on its site. The 18 October 2026
issue's first page, "Church of St. John, 5171 Milford Road, East Stroudsburg" (Fr. David
Cramer, Pastor), gives one Mass schedule: Monday 7 pm, Tuesday and Thursday noon,
Wednesday and Friday 9 am, Saturday 4 pm, Sunday 8:30 and 11 am and a monthly 1:30 pm
Spanish Mass. Not shared with another parish.

## Worship sites

One: Church of St. John (`st-john-east-stroudsburg`).

## Website and bulletin provider

churchofstjohn.com (the finder's link), a Kartra site that answers 403 to plain fetches
and loads in a browser. Its "This Week's Bulletin" link (a Kartra redirect) lands on
/Bulletin, which links each issue as a PDF on Kartra's CloudFront bucket; the file names
carry the date after a numeric prefix ("…October_18_2026.pdf"), older ones are named
"…060Aweb_37.pdf". Provider `other`, recipe `page-pdfs https://www.churchofstjohn.com/Bulletin`
pinned by inspection; `fetch:check` (run on 2026-10-17 against a temporary parishes.csv holding this row) picked the 18 October 2026 issue ("current"), so its browser got past the bot-blocking. The
PDFs have text.

## Not yet confirmed

Whether the resolver's browser gets past the site's bot-blocking (visit.py did, first try).
