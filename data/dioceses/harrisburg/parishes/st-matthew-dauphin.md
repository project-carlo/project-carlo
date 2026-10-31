---
name: Saint Matthew the Apostle and Evangelist
website: https://sites.google.com/site/saintmatthewcatholicchurch/bulletin-news
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://sites.google.com/site/saintmatthewcatholicchurch/bulletin-news']
group: ''
evidence:
- url: https://sites.google.com/site/saintmatthewcatholicchurch/bulletin-news
  seen: 2026-10-19
  note: 'Read in a browser (visit.py screenshot) on 19 October 2026: the Google Sites ''Bulletin'' page
    shows the bulletin as images, one per page, headed "St. Matthew the Apostle and Evangelist Catholic
    Church, 607 Stoney Creek Drive, Dauphin, PA 17018" and dated "October 18, 2026" (Volume 53, Number
    47). Its Mass schedule lists Saturday 17 October 5:00 pm and Sunday 18 October 8:00 and 10:15 am,
    weekday Masses cancelled 19-23 October. No text layer: the images are not readable by recheck.'
- url: https://sites.google.com/site/saintmatthewcatholicchurch/
  seen: 2026-10-19
  note: The parish's Google Sites homepage (the diocesan directory's and GCatholic's website), with a
    'Bulletin' page.
revisit: 'The bulletin is posted only as undated, unlabelled images (one per page) on the Google Sites
  page, which no resolver reads (the `page-images` collector takes one image that is dated or labelled
  "bulletin"). Set back to `other` with a recipe when a collector reads a multi-image issue, or when the
  parish posts a PDF.'
revisit_after: 2026-11-15
---

## Publisher

Saint Matthew the Apostle and Evangelist, 607 Stoney Creek Drive, Dauphin publishes its own weekly
bulletin on its Google Sites page. I read the 18 October 2026 issue there (in a browser, as
images): its head names this church alone and its Mass schedule lists the Saturday 5:00 p.m. and
Sunday 8:00 and 10:15 a.m. Masses; the directory names Very Rev. Paul M. Clark as pastor.

## Worship sites

- Saint Matthew, 607 Stoney Creek Dr., Dauphin (`st-matthew-dauphin`).

## Website and bulletin provider

The bulletin is not a PDF: the 'Bulletin' page of
`sites.google.com/site/saintmatthewcatholicchurch` is overwritten each week with the issue's pages
as images (`sites.google.com/sitesv-images-rt/...`). It is image-only, so the pipeline would have
to read the images. Set to `no_bulletin` on 2026-10-20 (Settled policy 4: kept in the records, left off the site)
because nothing the pipeline has can read it: the `page-images` collector takes a single image
whose address or alt text is dated or says "bulletin", and these images have neither (no alt
text, `sitesv-images-rt/<hash>=w1280` addresses) and make up one issue between them.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows, under xvfb-run with Chrome): resolve_failed, "NoBulletin: No PDF links found on bulletin page". The page holds the issue as images, which the `other` resolver does not read; nothing in src/ was changed. Until a resolver reads Google Sites image pages (or the parish posts PDFs), this row fetches nothing.

## Not yet confirmed

Whether a collector for multi-image issues is worth writing for this one parish (see `revisit`).
