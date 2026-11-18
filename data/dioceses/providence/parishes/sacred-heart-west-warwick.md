---
name: Sacred Heart
website: https://parishesonline.com/organization/sacred-heart-church-02893
bulletin_provider: unsupported
provider_id: ''
publication: ['po-org:sacred-heart-church-02893', 'lpi:0018000000Qx7uhAAB']
group: St. Joseph and Sacred Heart, West Warwick (one administrator)
evidence:
- url: https://customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/0018000000Qx7uhAAB/publications/1794497254559-2026_11_15.pdf
  seen: 2026-11-14
  note: '15 November 2026 issue, uploaded by the parish to ParishesOnline (4 pages; pages 1 and 4 images,
    page 1 read rendered): masthead ''Sacred Heart Church / Chiesa del Sacro Cuore di Gesu / West Warwick,
    RI 02893'', ''Rev. Gregory P. Stowe, Administrator Pro Tem''; ''RECTORY: 820 Providence Street'';
    ''MASS SCHEDULE SATURDAY AT 5:00 PM SUNDAY AT 10:00 AM''. Page 2 (text) is headed ''SACRED HEART CHURCH
    ... WEST WARWICK, RI'' with Mass intentions for Saturday 14 November 5:00 PM and Sunday 15 November
    10:00 AM.'
- url: https://parishesonline.com/organization/sacred-heart-church-02893
  seen: 2026-11-14
  note: 'probe po: org ''Sacred Heart Church'', 820 Providence St, West Warwick, RI, 02893; LPi 0018000000Qx7uhAAB,
    no container; weekly user-uploaded PDFs, latest 2026-11-14 (the 15 November issue).'
- url: https://dioceseofprovidence.org/parishfinder
  seen: 2026-11-14
  note: 'Finder entry 12240 ''Sacred Heart'', 820 Providence St.: ''Administrator pro tem: Very Rev. Gregory
    P. Stowe''; its website field is a masstimes.org map, not a parish site. Read in a browser.'
bulletin_status: available
fetch_gap:
  kind: po-user-upload
  seen: 2026-11-14
  url: https://customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/0018000000Qx7uhAAB/publications/1794497254559-2026_11_15.pdf
  note: 'The parish uploads its own bulletin to its ParishesOnline org as a user publication (customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/0018000000Qx7uhAAB/publications/<n>-YYYY_MM_DD.pdf),
    not as an LPi container issue. fetch:check on 2026-11-14 with parishes_online, provider_id sacred-heart-church-02893,
    failed: ''No matching anchor link found for parishes-online provider_id''. probe po lists the uploads
    with dates. The parish has no website of its own.'
publication_reviews:
- parish: st-joseph-west-warwick
  decision: separate
  evidence:
  - url: https://customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/0018000000Qx7uhAAB/publications/1794497254559-2026_11_15.pdf
    seen: 2026-11-14
    note: The 15 November 2026 masthead names Sacred Heart Church alone (820 Providence Street), with
      its own Mass times (Saturday 5:00 PM, Sunday 10:00 AM).
  - url: https://container.parishesonline.com/bulletins/03/0824/20261115B.pdf
    seen: 2026-11-14
    note: The 15 November 2026 St. Joseph masthead names Saint Joseph Church alone (854 Providence Street),
      with its own Mass times and no mention of Sacred Heart.
---

## Publisher

Sacred Heart, West Warwick (Natick) uploads its own weekly bulletin to ParishesOnline (org `sacred-heart-church-02893`, LPi id 0018000000Qx7uhAAB; no LPi container). The 15 November 2026 issue (https://customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/0018000000Qx7uhAAB/publications/1794497254559-2026_11_15.pdf) is headed "Sacred Heart Church / Chiesa del Sacro Cuore di Gesu / West Warwick, RI 02893" with "Rev. Gregory P. Stowe, Administrator Pro Tem" (page 1, an image, read rendered) and "MASS SCHEDULE SATURDAY AT 5:00 PM SUNDAY AT 10:00 AM".

Fr. Stowe is also pastor of St. Joseph, next door at 854 Providence St., whose LPi bulletin (container 03/0824) has a St. Joseph masthead and its own Mass times and does not mention Sacred Heart. Sacred Heart's issue names no St. Joseph Mass. So the shared administrator has not produced a shared bulletin: separate rows (see `publication_reviews`).

## Worship sites

One church, Sacred Heart, 820 Providence St. The bulletin mentions a chapel in the same building, open for personal prayer; it is not a separate worship site. The finder (12240) and GCatholic (22458) list only this church.

## Website and bulletin provider

`unsupported` (gap `po-user-upload`): the bulletin is a ParishesOnline user upload, which the parishes_online collector does not read (fetch:check 2026-11-14 with provider_id `sacred-heart-church-02893`: "No matching anchor link found"). The website is the org page, which lists the uploads; the parish has no website of its own (the finder links a masstimes.org map). When a collector reads org uploads, set `parishes_online` (or its provider) with the org slug and rerun fetch:check.

## Not yet confirmed

The finder still gives the old schedule (Saturday 5:00 PM; Sunday 7:30, 9:00 and 11:15 AM; daily 9:00 AM). The 15 November 2026 bulletin gives Saturday 5:00 PM and Sunday 10:00 AM only, and its intentions agree; the bulletin is followed.
