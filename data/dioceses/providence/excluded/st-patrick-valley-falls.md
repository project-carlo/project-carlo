---
name: St. Patrick
reason: closed
line1: 309 Broad St.
city: Cumberland
state: RI
postal_code: 02864
decided: 2026-11-14
roster: ['directory:12142', 'gcatholic:22357']
evidence:
- url: https://dioceseofprovidence.org/parishfinder
  seen: 2026-11-14
  quote: St. Patrick Church building closed.
  note: 'Finder entry 12142 ''St. Patrick (merged into St. Aidan, Cumberland)'': ''Established July 28,
    1861, 309 Broad St., Cumberland, RI 02864. St. Patrick Church building closed. Merged into St. Aidan-St.
    Patrick July 1, 2018''. Behind Cloudflare; read in a browser (parish-site-access visit.py).'
- url: https://container.parishesonline.com/bulletins/03/1212/20261115B.pdf
  seen: 2026-11-14
  quote: St. Patrick and Mt. Calvary Cemeteries
  note: The merged parish's 15 November 2026 bulletin gives one Mass schedule under 1460 Diamond Hill
    Road; its only St. Patrick references are the cemeteries.
- url: https://gcatholic.org/churches/usa-01/22357
  seen: 2026-11-14
  note: GCatholic 22357 still lists St. Patrick, 309 Broad St., Cumberland, Rhode Island 02864-7802 (Plus
    Code 87HCWJ44+RQ), with no closure noted.
parish: st-aidan-st-patrick-cumberland
research:
- method: Read the finder entries 12142/20485, the 15 November 2026 bulletin (03/1212) and GCatholic 22357
    for a date of the last Mass at St. Patrick
  url: https://dioceseofprovidence.org/parishfinder
  checked: '2026-11-14'
  outcome: not-found
  next_action: Search Rhode Island Catholic / Valley Breeze news for the St. Patrick, Valley Falls closing
    Mass, or read early St. Aidan-St. Patrick bulletins in ParishesOnline container 03/1212
  retry_when: A news archive or older container issues can be searched
---

## Why it is excluded

The Diocese of Providence parish finder (entry 12142, read 2026-11-14) says of St. Patrick, Valley Falls: "Established July 28, 1861, 309 Broad St., Cumberland, RI 02864. St. Patrick Church building closed." and "Merged into St. Aidan-St. Patrick July 1, 2018". It lists no Mass times for the entry. The merged parish's 15 November 2026 bulletin (ParishesOnline 03/1212) gives a single Mass schedule under 1460 Diamond Hill Road and mentions St. Patrick only for the St. Patrick and Mt. Calvary cemeteries. GCatholic (22357) still lists the church with no closure noted; the finder is the diocese's own and more recent. No source read gives the date of the last Mass, so `last_mass` is empty; the merger date (1 July 2018) is not taken as the closing date.

The finder gives 301 Broad St. and GCatholic 309 Broad St.; the finder's own legal-title note says 309 Broad St., which is recorded.

## What would change this

A St. Aidan - St. Patrick bulletin or the diocese listing a Mass at St. Patrick, 309 Broad St., Valley Falls. A source dating the closure would fill `last_mass`.
