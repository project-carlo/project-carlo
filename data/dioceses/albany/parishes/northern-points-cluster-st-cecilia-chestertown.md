---
name: Northern Points Cluster and St. Cecilia's
website: https://www.blessedsacramentbolton.org
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.blessedsacramentbolton.org/2026-bulletins.html', 'url:http://northernpointscluster.weebly.com/2026-bulletins.html', 'url:https://www.stceciliaschurch.org/2026.html']
group: Northern Points Cluster
evidence:
- url: https://www.blessedsacramentbolton.org/uploads/3/8/1/3/38133239/09-27-26_26th_sun_ord_tm_cyc_a.pdf
  seen: 2026-09-28
  quote: The Catholic Community
  note: 'Page 1 of the 27 September 2026 issue. The left column is "The Catholic Community of Saint Cecilia,
    3802 Main St., Warrensburg" (Sunday Mass 10:00 am, Pastor Rev. Joseph G. Busch); the right column
    is Blessed Sacrament, 7 Goodman Ave., Bolton Landing and St. Isaac Jogues, Chestertown, with one Mass
    schedule for the two (Pastor Rev. John O''Kane). Same pastoral associate (Barbara Carlozzi) for all
    three.'
- url: https://www.blessedsacramentbolton.org/uploads/3/8/1/3/38133239/09-27-26_26th_sun_ord_tm_cyc_a.pdf
  seen: 2026-09-28
  quote: 5:30 pm, Saturday, St. Isaac Jogues
  note: Page 1 Mass Schedule, followed by "9:00 am, Sunday, St. Isaac Jogues" and "10:30 am, Sunday, Blessed
    Sacrament".
- url: https://www.blessedsacramentbolton.org/uploads/3/8/1/3/38133239/09-27-26_26th_sun_ord_tm_cyc_a.pdf
  seen: 2026-09-28
  quote: 'Intentions & Mass Cards:  Please call the office at'
  note: Page 2 carries intentions and news for all three churches (Blessed Sacrament, then St. Cecilia's
    "518-623-3021", then St. Isaac Jogues "518-824-1176"); page 3 "Thanksgiving Baskets including St.
    Cecilia's" and a Mass time change at St. Isaac Jogues.
- url: https://www.blessedsacramentbolton.org/2026-bulletins.html
  seen: 2026-09-28
  note: Lists one PDF per Sunday, newest 09-27-26_26th_sun_ord_tm_cyc_a.pdf; the same files are under
    northernpointscluster.weebly.com/2026-bulletins.html (weebly host, behind Cloudflare; read with visit.py).
- url: https://www.stceciliaschurch.org/2026.html
  seen: 2026-09-28
  note: St. Cecilia's own site posts the same bulletin, but its newest file on 2026-09-28 was 08-23-26_21st_sun_ord_tm_cyc_a.pdf,
    whose page 1 is the same two-column masthead (St. Cecilia's plus Blessed Sacrament / St. Isaac Jogues).
- url: https://evangelist.org/news/2024/dec/26/trust-the-spirit/
  seen: 2026-09-28
  quote: Now, the cluster includes Blessed Sacrament in Bolton Landing and St. Isaac Jogues in Chestertown-Hague.
  note: The Evangelist, 26 December 2024, on the closing of St. James, North Creek.
---

## Publisher

One weekly bulletin serves three churches with two pastors: the Northern Points Cluster
(Blessed Sacrament, Bolton Landing and St. Isaac Jogues, Chestertown; Rev. John O'Kane) and
the Catholic Community of St. Cecilia, Warrensburg (Rev. Joseph G. Busch, who is also pastor
of Sacred Heart, Lake George and OLA, Queensbury). Page 1 of the 27 September 2026 issue is a
two-column masthead: St. Cecilia's ("Sunday Mass Schedule …10:00 am") on the left, and on the
right Blessed Sacrament and St. Isaac Jogues with their joint schedule "5:30 pm, Saturday, St.
Isaac Jogues / 9:00 am, Sunday, St. Isaac Jogues / 10:30 am, Sunday, Blessed Sacrament". Page
2 carries intentions and news for each of the three, and page 3 cluster news ("Mass Time
Change: We will change the 5:30 pm Mass time at St. Isaac Jogues to 4:00 pm beginning
Saturday, October 17, 2026").

St. Cecilia's own website posts the same file (the 23 August 2026 issue there has the same
two-column page 1), so St. Cecilia's is in this row rather than in its pastor's other
bulletins (Sacred Heart 03/1267, OLA 03/0098), which carry nothing of St. Cecilia's but its
Sunday time.

## Worship sites

Three: `blessed-sacrament-bolton-landing`, `st-isaac-jogues-chestertown`,
`st-cecilia-warrensburg`, every church whose Mass schedule the bulletin prints.

Ruled out or undecided:
- **St. James, North Creek** (`excluded/st-james-north-creek.md`): closing Mass 27 October
  2024; the diocese's directory still lists it as an "Other Worship Site" of St. Isaac Jogues.
- **Blessed Sacrament / St. Isaac Jogues summer chapel, Hague** (`open/blessed-sacrament-hague.md`):
  summer Sunday 9 am Mass through 2023; in no 2024-2026 summer bulletin.
- The institutional-records index also lists St. Teresa, Brant Lake and St. John the Baptist,
  Chestertown (now St. Isaac Jogues) as ended parishes of the Hague/Chestertown parish, and
  St. Pius X, Pottersville (closed 2000 per the Evangelist). None is in either roster; not
  researched further.
- The Monday 2:00 pm Mass at Elderwood, North Creek (a nursing home, on the cluster's Mass
  Times page) is not a public worship site and is not in any roster.

## Website and bulletin provider

The cluster's weebly site answers at two addresses: blessedsacramentbolton.org (no
Cloudflare on 2026-09-28) and northernpointscluster.weebly.com (the address the bulletin and
the diocese give; Cloudflare in front, loads in visit.py). Both list the same files
(uploads/3/8/1/3/38133239/MM-DD-YY_<Sunday>.pdf, one per Sunday), so the unblocked address is
the `website`; its /2026-bulletins.html page lists the year's issues. File names are not
predictable (they carry the liturgical Sunday), so the issue has to be read from the list
page. The PDFs have a text layer. The diocese's other address for the cluster,
northernpointscluster.org (GCatholic), does not resolve (DEAD-DNS). The weebly host answered
HTTP 429 to repeated `probe pdf` calls; spacing requests a second apart worked.

## Not yet confirmed

Nothing about the bulletin.
