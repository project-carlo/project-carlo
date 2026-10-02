---
name: Church of the Transfiguration / St. Catherine of Siena
website: https://www.pittsfordmendoncatholic.org
bulletin_provider: parishes_online
provider_id: church-of-the-transfiguration-and-st-catherine-of-siena-church
publication: ['po-org:church-of-the-transfiguration-and-st-catherine-of-siena-church', 'lpi:0018000000Qc2eZAAR',
  'po-container:06/0105']
group: 'Cluster: Church of the Transfiguration (Pittsford) and St. Catherine of Siena (Mendon)'
evidence:
- url: https://container.parishesonline.com/bulletins/06/0105/20261004B.pdf
  seen: 2026-10-02
  quote: Saturday 4 pm Transfiguration 5:30 pm St. Catherine Sunday 8:45 am Transfiguration 10:45 am St.
    Catherine
  note: 'Page 1 "Mass Schedule" of the 4 October 2026 issue, container 06/0105 (8 pages, text). The same
    page: "www.pittsfordmendoncatholic.org St Catherine: 585-624-4990 Transfiguration: 585 -248-2427"
    and weekday Masses at both.'
- url: https://www.pittsfordmendoncatholic.org/
  seen: 2026-10-02
  note: 'Read in a browser (visit.py; the site is built in JavaScript). Home page: "St. Catherine of Siena
    Church 26 Mendon-Ionia Rd. Mendon, NY 14506 / Church of the Transfiguration 50 West Bloomfield Rd.
    Pittsford, NY 14534", "the two clustered parishes", and a bulletin widget embedding ParishesOnline
    publications 06/0105 (lpi:0018000000Qc2eZAAR).'
- url: https://www.transfigurationpittsford.org
  seen: 2026-10-02
  note: 'The live row''s website. It redirects to https://www.pittsfordmendoncatholic.org/ (probe url:
    REDIRECT-OFFSITE). The target is this same parish''s own site, not a squat or a different family.'
- url: https://ps.dor.org/directory/church-of-the-transfiguration/
  seen: 2026-10-02
  quote: 'Cluster: St. Catherine of Siena, Mendon'
  note: 'Directory of Parishes: Transfiguration lists the cluster with St. Catherine of Siena and the
    same combined Mass schedule. The St. Catherine listing links https://saintcath.org/, which answered
    HTTP 502 on 2 October.'
promoted: 2026-10-02
---

## Publisher

One bulletin for the Transfiguration / St. Catherine cluster, on ParishesOnline (container
06/0105). The 4 October 2026 issue's page 1 is the cluster's Mass schedule: Saturday 4 pm at
Transfiguration and 5:30 pm at St. Catherine, Sunday 8:45 am at Transfiguration and 10:45 am
at St. Catherine, weekday Masses at both ("T" and "SC" in the intentions). It is not
shared with St. Louis (Pittsford), which has its own container (06/0026); the two share a
deacon in the Directory but not a bulletin.

## Worship sites

Two: `transfiguration` (50 West Bloomfield Road, Pittsford) and `st-catherine-of-siena-mendon`
(26 Mendon-Ionia Road, Mendon). The ParishesOnline organization record gives its address as
"50 West Bloomfield Road, Mendon, NY 14506", a blend of the two; the parish's own site and
the bulletin keep them apart.

## Website and bulletin provider

**Website changed** from `transfigurationpittsford.org` to `https://www.pittsfordmendoncatholic.org`.
The old domain redirects to the new one, which is the cluster's real site (it embeds the
bulletin widget with `lpi:0018000000Qc2eZAAR` / container 06/0105). fetch reads this parish by
`provider_id`, so the change affects only the recorded homepage. The Directory still links
`transfigurationpittsford.org` for Transfiguration and `saintcath.org` (HTTP 502) for St.
Catherine, and the Parish Locator links `pittsfordmendoncatholic.org` for both.

## Not yet confirmed

`saintcath.org` was down when read; if it comes back with its own bulletin, that would need a
look, but the 4 October ParishesOnline issue already covers both churches.
