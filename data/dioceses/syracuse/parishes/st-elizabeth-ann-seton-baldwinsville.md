---
name: St. Elizabeth Ann Seton
website: https://stelizabethbville.org
bulletin_provider: other
provider_id: ''
publication: ['url:https://stelizabethbville.org/category/bulletins/']
group: Baldwinsville Catholic Parishes
evidence:
- url: https://stelizabethbville.org/wp-content/uploads/09.20.26.pdf
  seen: 2026-09-26
  quote: Mass Schedule for Baldwinsville Parishes
  note: 'The 20 September 2026 bulletin, page 1: Most Rev Douglas J Lucia, Pastor; Reverend Benjamin Schrantz,
    Parochial Vicar; Deacon Mark Kay; the three parishes'' shared weekend and weekday schedule (St. EAS
    Saturday 5:30pm, Sunday 7:30am and 10:30am, Thursday 6:45am, Friday 9:00am); "Church Office Phone
    – 315.652.4300"; "@SEASBville stelizabethbville.org". Page 2 is headed "ST. ELIZABETH ANN SETON PARISH
    STAFF".'
- url: https://stelizabethbville.org/category/bulletins/
  seen: 2026-09-26
  note: The site's Bulletins category, one WordPress post per issue (bulletin-9-20-3, bulletin-9-13-2,
    bulletin-8-30-2 ...); each post embeds its PDF from wp-content/uploads through the PDF Embedder plugin.
- url: https://stelizabethbville.org/
  seen: 2026-09-26
  quote: Saturday 5:30 pm & Sunday 7:30 & 10:30 am
  note: Homepage, under "Weekend Masses", with 3494 Rt. 31, Baldwinsville.
promoted: 2026-09-26
---

## Publisher

St. Elizabeth Ann Seton publishes its own weekly bulletin on its website, one WordPress post per
issue in the Bulletins category, each wrapping a PDF (the newest on 26 September was "Bulletin
9/20", posted 17 September, wp-content/uploads/09.20.26.pdf). I read that issue: page 1 carries
the clergy shared by the three Baldwinsville parishes (Bishop Lucia pastor, Fr. Schrantz
parochial vicar) and a "Mass Schedule for Baldwinsville Parishes" covering St. Mary, St. EAS
and St. Augustine, but its office, phone and handles are SEAS's own, and page 2 is "St. Elizabeth
Ann Seton Parish Staff" and its mission statement.

St. Mary of the Assumption (ParishesOnline 06/0074) and St. Augustine's (ParishesOnline 04/0667)
each publish their own bulletin too, all current, so this is its own row in the group
"Baldwinsville Catholic Parishes" (see `parishes/st-mary-of-the-assumption-baldwinsville.md`).

## Worship sites

One: St. Elizabeth Ann Seton, 3494 State Route 31 (`churches/st-elizabeth-ann-seton-baldwinsville.md`).

## Website and bulletin provider

stelizabethbville.org is the parish's own site and hosts the bulletins itself, so the provider
is `other` and the publication is the Bulletins category page. `probe url` found no ids and the
guessed /bulletins/ path is a 404; the category page was found from the post links.

**Fetch gap:** a test run of the pipeline's `other` fetcher on 2026-09-26
(`build_latest_other_bulletin_links(provider_id="https://stelizabethbville.org")`) reached the
latest post (bulletin-9-20-3) but failed with "No PDF links found on bulletin post page": the
PDF Embedder plugin replaces the `<a href="…/09.20.26.pdf" class="pdfemb-viewer">` anchor with a
canvas viewer when the page renders, so neither the anchors nor the rendered HTML still hold the
URL. The raw HTML does. Reported to the orchestrator.

## Not yet confirmed

Whether the pipeline can fetch this bulletin (see the gap above).
