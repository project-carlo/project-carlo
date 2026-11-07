---
name: Our Lady of Good Counsel Parish
website: https://olgc.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-of-good-counsel-church-southampton-pa-18966
publication: ['url:https://www.church-bulletin.org/our-lady-of-good-counsel-church-southampton-pa-18966']
group: ''
evidence:
- url: https://www.church-bulletin.org/our-lady-of-good-counsel-church-southampton-pa-18966
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 6, 'Our Lady of Good Counsel Church', Southampton, PA 18966, 611 Knowles
    Avenue, phone (215) 357-1300; latest edition October 25, 2026.
- url: https://www.church-bulletin.org/bulletin/our-lady-of-good-counsel-church-southampton-pa-18966/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (12 pages, image-only). Rendered page 1: ''30th Sunday in Ordinary Time,
    October 25, 2026 ... Forty Hours Devotions ... Our Lady of Good Counsel, 611 Knowles Avenue, Southampton,
    PA 18966''; page 2 ''Mass Schedule: Sunday Mass: Saturday Evening: 4:30pm; Sunday: 8:00am, 10:00am,
    and 12:00pm. Daily Mass: Monday-Friday: 9:00am; Saturday: 8:00am''; ''All Masses are in the Upper
    Church''. Names this parish alone.'
- url: https://olgc.org/bulletin/
  seen: 2026-10-29
  quote: The weekly bulletin is the principal means by which the community is informed about affairs and
    events of the parish.
  note: Parish site Bulletins page lists newest first, e.g. wp-content/uploads/2026/10/006-October-25th-2026.pdf
    (page source). That file is byte-identical (md5 d59e9d71428000691f1d5c35699dab28) to the listing's
    2026-10-25.pdf; its 'jppc.net/onlinebulletins/006template.pdf' link and the '006-' file prefix name
    the listing.
- url: https://archphila.org/parish/our-lady-of-good-counsel-southampton/
  seen: 2026-10-29
  quote: Rev. Robert G. Suskey
  note: 'Directory: pastor; 611 Knowles Ave., Southampton 18966-4198; Bucks County Southeast deanery;
    Mass times match the bulletin.'
promoted: 2026-10-29
research:
- method: Read listing 6, the parish site's Bulletins page and compared md5 of the 25 October PDF from
    both
  url: https://olgc.org/bulletin/
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

Our Lady of Good Counsel Parish, Southampton (Rev. Robert G. Suskey, Pastor) prints with John Patrick Publishing: listing 6 (`church-bulletin.org/?id=6`) has an issue for 25 October 2026. The parish's own Bulletins page (olgc.org/bulletin/) also posts each issue, newest first, with a byte-identical copy of the current one (md5 d59e9d71428000691f1d5c35699dab28 for both). Following the diocese's rule for such copies, the row keeps the listing as the `page-pdfs` channel and notes the self-hosted copy as equal.

The PDF has no text layer; the page-2 Mass box was read from the rendered page. It names this parish alone.

## Worship sites

One church, Our Lady of Good Counsel, 611 Knowles Avenue. The Mass schedule says 'All Masses are in the Upper Church'; the parish has a lower church, but no Mass is listed there. The weekday 'Chaplet of Divine Mercy' and 'Miraculous Medal Novena' are devotions in the church.

## Website and bulletin provider

`https://olgc.org` (directory: `http://www.olgc.org`, which redirects) is the parish's WordPress site.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (issue age 4 days, date inferred from the listing's file name); identity `unverified` because the check is given no expected identity and the PDF has no text layer to match, so the masthead was read by hand above. It printed no `recipe` line, as the pinned `provider_id` already holds it.
