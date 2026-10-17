---
name: Our Lady of Victory Parish
website: https://olvchurch.com
bulletin_provider: other
provider_id: page-pdfs https://olvchurch.com/bulletin/
publication: ['url:https://olvchurch.com/bulletin/']
group: Our Lady of Victory Parish Tannersville
evidence:
- url: https://olvchurch.com/wp-content/uploads/2026/10/Bulletin_10_11_2026.pdf
  seen: 2026-10-16
  note: 'The 11 October 2026 issue (3 pages, all images with no text layer; page 1 rendered with render.py
    and read): header "28th SUNDAY IN ORDINARY TIME www.olvchurch.com October 11, 2026", Mass intentions
    for the week (Monday-Friday 8:00 A.M., Saturday 5:00 P.M., Sunday 8:30 A.M. and 10:30 A.M.), "MESSAGE
    FROM FATHER RICH". recheck cannot find this text.'
- url: https://olvchurch.com/bulletin/
  seen: 2026-10-16
  note: 'The bulletin page shows only the current issue (iframe title "Bulletin_10_11_2026", data-pdf-id
    11561), through the PDF Embedder plugin''s iframe; its address is base64-encoded in the iframe''s
    pdfemb-data parameter (decoded: wp-content/uploads/2026/10/Bulletin_10_11_2026.pdf). No plain link
    to the PDF.'
- url: https://olvchurch.com/mass-schedule/
  seen: 2026-10-16
  quote: WEEKDAYS Monday through Friday 8:00 am WEEKENDS SATURDAY – 5:00 pm SUNDAY — 8:30 & 10:30 am
revisit: Run fetch:check -- --parish our-lady-of-victory-tannersville after promotion; the PDF is only
  in a base64 pdfemb-data iframe parameter.
revisit_after: 2026-11-15
promoted: 2026-10-17
---

## Publisher

Our Lady of Victory Parish publishes its own weekly bulletin on its WordPress site. The 11
October 2026 issue (image-only) is headed "www.olvchurch.com October 11, 2026" and gives
this church's week of Masses: weekdays 8 am, Saturday 5 pm, Sunday 8:30 and 10:30 am, with
a message from the pastor, Father Rich. It names no other church; the diocese finder lists
the parish with one worship site.

## Worship sites

One: Our Lady of Victory Church, 327 Cherry Lane Road (`our-lady-of-victory-tannersville`).

## Website and bulletin provider

olvchurch.com (the finder's link). Its /bulletin/ page embeds the current PDF through the
PDF Embedder plugin's iframe, with the file address only base64-encoded
(`?pdfemb-data=...`), not as a link; past issues are not listed. Provider `other` with
recipe `page-pdfs https://olvchurch.com/bulletin/`, but **the resolver does not find the
PDF**: its PDF Embedder fallback looks for the plugin's `pdfemb-viewer` anchor, and this
page uses the iframe variant. `fetch:check` (run on 2026-10-17 against a temporary parishes.csv holding this row) failed as expected: "resolve_failed ... No PDF links found on bulletin page: https://olvchurch.com/bulletin/". The bulletin is also **image-only** (no text layer on any page), so it has to be read
as images.

## Not yet confirmed

The resolver cannot read the embedded PDF (fetch:check above). Either the `other`
collector gets a case for the PDF Embedder iframe's base64 `pdfemb-data`, or the row has to
become `no_bulletin`; left as `other` for the coordinator to decide.
