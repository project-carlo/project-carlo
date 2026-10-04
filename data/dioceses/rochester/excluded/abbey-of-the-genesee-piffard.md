---
name: Our Lady of the Genesee
reason: no-bulletin
line1: 3258 River Rd.
city: Piffard
state: NY
postal_code: '14533'
decided: 2026-10-02
roster:
- gcatholic:17867
- directory:ind-abbey-of-the-genesee
evidence:
- url: https://gcatholic.org/churches/usa-02/17867
  seen: 2026-10-02
  quote: 3258 River Rd., Piffard, New York 14533
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Rochester as ''Our Lady of the Genesee'',
    3258 River Rd., Piffard, NY, 14533; kind: Our Lady'
- url: https://www.dor.org/parishes-campuses-cemeteries/parish-locator-and-mass-times/
  seen: 2026-10-02
  note: 'Listed in Diocese of Rochester Parish Locator and Mass Times as ''Abbey of the Genesee'', Piffard, NY,
    14533; group: Individual'
- url: https://www.geneseeabbey.org/visit-us
  seen: '2026-10-02'
  quote: Daily Mass is presently celebrated at 7am, (Sunday mass 8am) and is open to the public.
  note: The Abbey's own Visit Us page (eCatholic site, readable with parish-site-access visit.py; plain fetchers
    get HTTP 403). Address 3258 River Rd., Piffard, NY 14533.
- url: https://www.geneseeabbey.org/liturgy
  seen: '2026-10-02'
  quote: Mass is presently celebrated at 7 am Monday-Saturday and at 8 am on Sunday.
- url: https://www.geneseeabbey.org/
  seen: '2026-10-02'
  note: Embeds ecatholic:36249 (the site host). issues.py ecatholic ecatholic:36249 found no weekly issue in six
    Sundays probed (403 each), and the site has no bulletin or Mass-times page beyond the liturgy page above.
---

## Why it is excluded

**Abbey of the Genesee (GCatholic: Our Lady of the Genesee), 3258 River Road, Piffard: open, public Mass daily, no bulletin.** The Trappist abbey's own pages (read 2 October 2026) say "Daily Mass is presently celebrated at 7am, (Sunday mass 8am) and is open to the public." That makes it a real public worship site (the Diocese's Parish Locator lists "Mass: Sun: 9:45am", which is stale).

It is not a parish and has no bulletin: its eCatholic site (ecatholic:36249) carries no weekly issue (checked six Sundays back to 30 August 2026) and no schedule beyond the liturgy page. The pipeline has nothing to read, so it is filed as `no-bulletin`, not `closed`. It belongs to no parish row. Address: GCatholic (3258 River Rd., Piffard 14533, Monastery) and the abbey's own pages agree; OSM puts a place of worship on River Road at the same point (42.8447, -77.8634; GCatholic Plus Code 42.84469, -77.86319).

## What would change this

A weekly bulletin or a schedule feed the pipeline can read, or the diocese attaching it to a parish bulletin. Revisit with the next diocese-wide audit.
