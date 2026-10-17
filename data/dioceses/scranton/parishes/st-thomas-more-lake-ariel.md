---
name: St. Thomas More Parish
website: https://stthomas-stmary.com/bulletin/
bulletin_provider: other
provider_id: ''
publication: ['url:https://stthomas-stmary.com/bulletin/']
group: Saint Thomas More Parish
evidence:
- url: https://stthomas-stmary.com/download/19/bulletin/18800/bul-october-11-2026.pdf
  seen: 2026-10-16
  quote: Fr. Stephen Bosomafi Pastor
  note: 'Page 1 of the 11 October 2026 issue ("The Bully", Volume V, #13): masthead with both churches,
    "St. Thomas More 105 Gravity Rd." and "St. Mary 334 St. Mary Church Rd.", PO Box 188, Lake Ariel,
    and the weekend schedule (Saturday 4:00pm St. Mary''s, 6:00pm St. Thomas More; Sunday 8:00am St. Thomas
    More, 9:30am St. Mary''s, 11:00am St. Thomas More). The text layer splits lines oddly, so these words
    are paraphrased in this note, not quoted.'
- url: https://stthomas-stmary.com/download/19/bulletin/18800/bul-october-11-2026.pdf
  seen: 2026-10-16
  quote: 6:00pm(STM)
  note: Page 4, Mass intentions for the week of 12-18 October 2026, coded (STM) St. Thomas More, (SM)
    St. Mary's, and (JR) for a Tuesday 10:00am Mass.
- url: https://stthomas-stmary.com/bulletin/
  seen: 2026-10-16
  note: The parish site's Bulletin page embeds the current issue in a 3D FlipBook (WordPress plugin);
    the page's FB3D_CLIENT_DATA (base64 JSON) holds the PDF address https://stthomas-stmary.com/download/19/bulletin/18800/bul-october-11-2026.pdf.
promoted: 2026-10-17
---

## Publisher

St. Thomas More Parish, Lake Ariel publishes a weekly bulletin ("The Bully") for its two
churches on its own site. The 11 October 2026 issue's masthead names St. Thomas More, 105
Gravity Rd. and St. Mary, 334 St. Mary Church Rd., with Fr. Stephen Bosomafi as pastor, and
its weekend schedule and page 4 intentions cover both. The diocese does not group it with
another parish.

## Worship sites

Two: St. Thomas More (`st-thomas-more-lake-ariel`) and St. Mary (`st-mary-lake-ariel`),
both in Lake Ariel. The intentions also list a Tuesday 10:00am Mass coded "(JR)", not
explained in the issue; it is probably a nursing-home Mass (the Julia Ribaudo extended care
center is in Lake Ariel), which would not be a public worship site. Not recorded.

## Website and bulletin provider

stthomas-stmary.com/bulletin/ shows the current issue in a "3D FlipBook" viewer. The PDF
address is in the page's FB3D_CLIENT_DATA (base64 JSON), as
`/download/19/bulletin/<id>/bul-<month>-<day>-<year>.pdf`; plain curl got the page and the
PDF. The PDF has a text layer, but its lines are split one character late ("S t. Thomas
More1 05 Gravity Rd."), which may trouble extraction. No publisher id, so `other`.
The homepage answered curl with a "Please wait while your request is being verified"
challenge page once. No `fetch:check` recipe yet; the collector needs `linked-issue-page`
(flipbook) handling.

## Not yet confirmed

What "(JR)" is.
