---
name: Our Lady of Fatima Chapel
website: https://www.olfchapel.org/
bulletin_provider: other
provider_id: redirected-pdf https://www.dropbox.com/s/49svgl5o1cp6wbg/Bulletin.pdf?dl=1
publication: ['url:https://www.dropbox.com/s/49svgl5o1cp6wbg/Bulletin.pdf']
group: ''
evidence:
- url: https://www.dropbox.com/s/49svgl5o1cp6wbg/Bulletin.pdf?dl=1
  seen: 2026-11-04
  quote: November 1, 2026 +  Festum Omnium Sanctorum
  note: 'Page 1 masthead: ''Fraternitas Sacerdotalis Sancti Petri'', ''Our Lady of Fatima Chapel'', ''32
    West Franklin Ave., Pequannock, New Jersey 07440'', Administrator Fr. Matthew McNeely, FSSP. Mass
    intentions for Sunday 1 November 2026 at 7:00, 9:00, 10:30 a.m., 1:30 and 5:00 p.m., and weekday Masses
    at 7:00 and 9:00 a.m. (7:00 p.m. some days). The Dropbox file has a fixed name, overwritten each week.'
- url: https://www.olfchapel.org/
  seen: 2026-11-04
  note: 'probe url: Wix site ''HOME | Olf Website'' (http://www.olfchapel.org redirects to https://www.olfchapel.org/);
    its one bulletin link is https://www.dropbox.com/s/49svgl5o1cp6wbg/Bulletin.pdf?dl=0.'
revisit: Check the Dropbox Bulletin.pdf is a current issue (masthead date within two weeks)
revisit_after: 2026-12-04
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

Our Lady of Fatima Chapel, Pequannock, served by the Priestly Fraternity of St. Peter (FSSP) with the Traditional Latin Mass, publishes its own weekly bulletin as a single Dropbox file, `Bulletin.pdf`, replaced each week. The copy read on 2026-11-04 (`https://www.dropbox.com/s/49svgl5o1cp6wbg/Bulletin.pdf?dl=1`) is the 1 November 2026 issue: page 1 reads "Fraternitas Sacerdotalis Sancti Petri", "Our Lady of Fatima Chapel", "32 West Franklin Ave., Pequannock, New Jersey 07440", "Administrator: Fr. Matthew McNeely, FSSP" and "November 1, 2026 + Festum Omnium Sanctorum".

## Worship sites

- `our-lady-of-fatima-chapel-pequannock`: the only place. Page 1's Mass intentions (Sunday 7:00, 9:00, 10:30 a.m., 1:30, 5:00 p.m.; weekdays 7:00 and 9:00 a.m., some evenings 7:00 p.m.) name no other site.

GCatholic lists it (38951, Chapel). The diocese's finder has no pin for it, and Holy Spirit's bulletin (25 October 2026) does not mention it, so it is not part of that row.

## Website and bulletin provider

`olfchapel.org` is a Wix site that `probe url` reads; its only bulletin link is the Dropbox preview `https://www.dropbox.com/s/49svgl5o1cp6wbg/Bulletin.pdf?dl=0`. Provider `other`. Unpinned, `fetch:check` (2026-11-04) took that link by `page-pdfs` and got Dropbox's HTML preview (not_pdf), so the recipe is pinned to the direct download, `redirected-pdf https://www.dropbox.com/s/49svgl5o1cp6wbg/Bulletin.pdf?dl=1`: `fetch:check` then downloaded a PDF (only-link), the 1 November 2026 issue read above. It reports issue date and freshness unknown because the file name carries no date and the resolver found no unambiguous masthead date; since the file is replaced in place each week, the download is whatever issue the chapel last posted. The Dropbox URL (without the query) is recorded as this bulletin's publication id.

## Not yet confirmed

- That the chapel keeps replacing the same Dropbox file weekly (only the 1 November 2026 copy was read). If a later fetch returns an issue older than two weeks, look for a new link on olfchapel.org.
