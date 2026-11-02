# Factory queue

`queue.json` is the ordered list of dioceses waiting for a map Run. The dispatcher
reads this file from `origin/main`; changing it does not launch workers from this
checkout. See [the factory specification](../docs/factory-spec.md) for operation.

## Coverage and order

The 2026-11-02 inventory covers the 50 states, DC, and the five inhabited U.S.
territories. It includes Latin territorial dioceses, Eastern Catholic eparchies
and archeparchies, the Personal Ordinariate of the Chair of Saint Peter, and the
Archdiocese for the Military Services. Archdioceses are included throughout.

The queue finishes the Northeast first: the remaining New Jersey dioceses,
Brooklyn and Rockville Centre, then Connecticut, Rhode Island, Massachusetts,
New Hampshire, Maine, and Vermont. It then expands through the Mid-Atlantic,
Southeast, South, Great Lakes, Midwest, Plains, Texas/Oklahoma/Arkansas,
Southwest, California/Hawaii, and Northwest/Alaska. U.S. territories follow,
then Eastern Catholic jurisdictions and the two personal jurisdictions.
Within those later regional groups, the USCCB listing order is retained.

There are **205 jurisdictions** in the inventory: 176 Latin territorial
dioceses in the USCCB regional lists, 18 Eastern Catholic jurisdictions,
two personal jurisdictions, and nine additional territorial dioceses outside
the USCCB lists. **188 are queued**. The other 17 are represented by records
already in the repository or by open mapping PRs; New York is in both groups.
Counts come from the named entries rather than the USCCB page's summary totals.

Sources checked on 2026-11-02:

- [USCCB regions and jurisdictions](https://www.usccb.org/about/bishops-and-dioceses)
  and [official diocesan website directory](https://www.usccb.org/about/bishops-and-dioceses/all-dioceses).
  The queue corrects the regional list's spelling of Worcester and distinguishes
  Portland in Maine from Portland in Oregon, all three Springfields, both
  Lafayettes, both Kansas Cities, and overlapping Eastern jurisdictions.
- [Puerto Rican Episcopal Conference](https://ceppr.org/): San Juan de Puerto
  Rico, Arecibo, Caguas, Fajardo-Humacao, Mayagüez, and Ponce.
- [Agaña parish finder](https://www.archagana.org/parishfinder) and
  [Catholic-Hierarchy's Pacific dioceses](https://www.catholic-hierarchy.org/country/dp02.html):
  Agaña (Guam), Chalan Kanoa (Northern Mariana Islands), and Samoa-Pago Pago
  (American Samoa). Saint Thomas in the U.S. Virgin Islands is already in
  the USCCB list and is counted once.

The notes are starting points for survey, not verified parish counts. Survey
must find the current official roster. Eastern and personal jurisdictions
must use their own directories; their geography overlaps territorial dioceses.
Cross-border jurisdictions are limited to U.S. communities, and military
coverage excludes overseas locations and requires checking public access.

## Excluded from this queue

Already represented under `data/dioceses/`: Albany, Allentown,
Altoona-Johnstown, Buffalo, Erie, Greensburg, Harrisburg, New York,
Ogdensburg, Pittsburgh, Rochester, Scranton, and Syracuse. Existing records
are not a reason to start a second full map Run; follow-up work is separate.

Open mapping PRs checked on 2026-11-02:

| Diocese | PR |
| --- | --- |
| New York | [#95](https://github.com/project-carlo/project-carlo/pull/95) |
| Wilmington | [#170](https://github.com/project-carlo/project-carlo/pull/170) |
| Philadelphia | [#174](https://github.com/project-carlo/project-carlo/pull/174) |
| Camden | [#175](https://github.com/project-carlo/project-carlo/pull/175) |
| Trenton | [#179](https://github.com/project-carlo/project-carlo/pull/179) |

The latter four were in the previous queue and have been removed. The seven
remaining old entries retain their research notes. Recheck open mapping PRs
when extending or restoring queue entries so the factory does not duplicate
work underway outside its local ledger.
