---
name: Archdiocese of New York
state: NY
website: https://www.archny.org
status: promoted
gcatholic: newy0
city_aliases:
  Southeast: Brewster
  Town of Southeast: Brewster
promoted: 2026-10-11
---

Opened for one requested parish in September 2026; expanded into an archdiocese-wide
survey at the owner's request on October 7, 2026. The September promotion date records
that first addition, not completion of this survey. Current roster coverage, the number
of unresolved physical sites, and the latest promotion are recorded in the Log.

## Sources

- **Official parish map:** https://www.archny.org/map/parishes; all 326 locations were
  imported into `rosters/directory.json`. The server-rendered `div[data-pf-item]` elements
  contain the original numeric CMS ids, full parish/site titles, street addresses,
  coordinates, homepages and links to the individual `archny.org/places/` pages. The page
  and browser both reported 326 locations. This snapshot was fetched on October 6 EDT
  (October 7 UTC). It is a list of physical locations, not 326 bulletin publishers.
  Colon-separated titles provide a grouping lead, not evidence of a shared bulletin.
  Missing websites, unnumbered addresses, ZIP-only locality fields and absent Mass tags
  were retained with notes; none implies closure. Directory coordinates can point to a
  parish office or another frontage of the same complex.
- **GCatholic:** key `newy0`, https://gcatholic.org/churches/local/newy0;
  `rosters/gcatholic.json` contains all 426 entries, enriched from individual church pages
  with addresses, Plus Codes, websites, rite and history where supplied. It includes
  Eastern Catholic jurisdictions, old canonical names, historic buildings and stale
  parish domains. Its coverage denominator therefore differs from the official map.
  A merger in a history field does not establish that a building stopped holding Mass.
- **Current bulletins and parish websites:** these establish the publisher and actual
  worship buildings. The dated issue, its quoted masthead or schedule, and the reading
  date are attached to each settled record. A church whose status remains unconfirmed
  is an `open/` record with a specific next step, not an invented closure or no-bulletin
  exclusion. Several parishes use Bon Venture sponsor pages; their current PDFs have
  dated paths such as `sponsors.bonventure.net/pdfs/6686/2026-10-04.pdf`.
- **Canonical restructuring:** the official map preserves many merged parish names.
  The archdiocese's decree index is a lead for subsequent bulletin research:
  https://www.archny.org/posts/decisions-of-the-office-of-the-archbishop-of-new-york-2026-8-13.
  Legal parish mergers and relegation plans do not replace dated evidence about public
  Mass in a building. No archdiocese-wide canonical list is treated as a bulletin list.
- **Closed parishes / sacramental records:** no complete closed-building roster was
  imported. Exclusions are individual decisions supported by their own cited sources;
  uncertainty and conflicting evidence are explicitly retained.

### Bulletin channels and local research

- eCatholic homepages frequently put the bulletin one click away. A site id alone does
  not prove that its eCatholic archive is current. St. Clare's archive stops in January
  2023 while its current Bulletin button points to Bon Venture; St. Sylvester has a
  September 2023 eCatholic archive but a live LPi channel. Record the active publication.
- LPi generic covers and inserts are not independent publishers. Read the parish pages
  and actual Mass schedule, including image-only pages, before deciding membership.
- A current bulletin can retain an old template heading. The October 4 St. Teresa issue
  has a June 13, 2021 contact-page header but a current footer and current issue pages.
  Such contradictions are documented in the record, not silently corrected in a quote.
- Automatic fetching was initially disabled for three real publishers using the supported
  `no_bulletin` skip provider, with their publication identities and active venues retained:
  Resurrection in Rye publishes readable Flocknote HTML rather than the tested PDF format;
  the Sullivan County St. Francis Xavier joint publisher's newer-dated PDF is a supplement,
  not the full issue; and St. Augustine in Highland's archive still ends August 16, 2026.
  Each has a separate actionable connector question in `open/`. Under the October 7 policy
  incorporated from current main on October 8, unsupported publishers and their associated
  venues stay in the evidence records but are omitted from the live CSVs and site until
  a safe supported channel is available. They have no promoted stamps. This operational
  hold is not a statement that publication or public Mass has ceased, and is not an exclusion.
  The resumed research adds any genuinely unsupported channels to the same policy, without
  treating client TLS trust problems, a later HTTP 403 or incomplete replay as cessation.
  The current totals and every original-question disposition are in
  [the October 8-11 research follow-up](research-followup.md).
- Refreshes on October 8 found Holy Rosary Hawthorne and St. Matthew/Our Lady of Perpetual
  Help issues dated October 4. Sacred Heart/St. Patrick's latest linked issue remained
  September 20. Image-only pages were rendered and visually read; archive lag is explicit.
  St. Martin de Porres's `Bulletin 100426.pdf` is dated October 4, 2026 inside the document,
  despite an automatic filename parser reading it as April 26, 2010.
- This survey runs on the owner's Windows machine, not the Claude cloud sandbox. The
  Linux Chrome/proxy/xvfb setup script is not needed. The shared T3 browser is preferred;
  when it explicitly reported an unavailable host, local Chrome and the skill's probing
  approach were used. Headed Chrome read parish pages that challenged headless requests.
  Python's Windows TLS chain selection failed on some sites while verified httpx/certifi
  or Windows curl succeeded; certificate verification was not disabled globally.

## Rules settled for this diocese

Brewster is the village and the postal city; it sits in the Town of Southeast. Store Brewster.
The archdiocese's "Town of Southeast" is the same place, recorded in `city_aliases`.

The owner explicitly requested the whole archdiocese for this survey; the earlier
single-parish scope does not limit the October expansion.

The physical worship site and bulletin decide records, not the number of names in a
canonical parish title. A shared pastor does not combine separate current bulletins.
A title that still names a building with no current schedule leaves an open question
unless an explicit source settles its use. Sunday Vigil Mass in a separate school
building counts as public Mass; school-only administrative listings do not.

Repeated dedications in one city need disambiguated slugs and separate roster links.
For example, Staten Island has distinct St. Joseph churches at Poplar Avenue and
Tompkins Avenue. Do not allow a same-name match to silently absorb the other building.

Leave verification flags false when there is an address conflict or only one independent
source. A parish bulletin and its own homepage are one source. Buildings absent from both
rosters can still be added when their parish provides a current Mass schedule and address;
their lack of a roster entry is explained. The resumed research supplies sourced representative
OSM/Nominatim coordinates for the Lourdes Chapel and St. Patrick School on Staten Island,
while retaining the street-number mismatch and school-site/interior-room fidelity caveats.

Two Eastern Catholic roster entries identify an already-mapped Latin physical host at
the same address: Holy Spirit in Cortlandt Manor and St. Francis in Mount Kisco. These
are location-coverage aliases, not incorporation of Eastern communities into Latin
jurisdiction. Same-name sites at different addresses remain distinct: the Latin St. Mary
at Grand Street is an open question, not the Ruthenian St. Mary exclusion on East 15th.
St. John the Baptist in Manhattan is excluded with `reason: other` for its explicit temporary
repair suspension, repeated in the October 11 issue despite a standing printed schedule.
It is not labeled permanently closed and no final-Mass date is invented.

## Log

- 2026-09-26: Added St. Lawrence O'Toole and Sacred Heart (Brewster and Patterson) because the
  parish was requested. One bulletin, two churches, read from the 27 September 2026 issue.
  The GCatholic roster was not fetched, so there is no coverage number.
- 2026-10-08: Completed the first archdiocese-wide mapping pass: 186 bulletin publishers,
  237 public-Mass venues, 43 evidence-backed exclusions and 171 actionable open questions.
  Open questions include publication connectors and unidentified chapel locations, not
  171 distinct closed or inactive buildings. Both baselines are fully accounted for,
  not fully modeled: the official directory has 230 church-linked and 96 open entries
  (326/326); GCatholic has 229 church-linked, 43 excluded and 154 open entries (426/426).
  There are no unmatched entries, duplicate roster references or street-only matches.
  Two additional Staten Island worship venues are absent from both rosters; their unknown
  coordinates remain unset rather than guessed. Existing Brewster/Patterson verification
  flags and live rows are preserved.
  Structural audit finds no groups spanning publisher rows and no missing publication ids.
  Validation of all dioceses passes with no errors or incomplete records; New York retains
  20 warnings for explicit closed exclusions whose exact last-Mass dates are unknown.
  The initial promotion dry run on the original worktree base adds 185 publishers and
  235 churches, updates/removes no live rows
  and removes no rows with attached events. Research uses the local Windows adaptations
  above. Resolver checks vary in fidelity: actual saved HTML replay and downloaded/read
  PDFs are recorded separately from reconstructed-anchor checks; Cloudflare HTTP blocks
  are not treated as bad recipes or closures. This is a documented first-pass map with
  follow-up work retained, not a claim that every archdiocesan building is settled.
- 2026-10-08 (current-main integration): Incorporated main through `cb85c5fe`, including
  the October 7 policy that `no_bulletin` publishers and their churches remain off-site.
  Re-promoted New York: the records still contain 186 publishers and 237 venues, but
  183 publishers and 232 venues are live, with three publishers/five venues on hold for
  the connector questions above. Against current main this adds 182 publisher rows and
  230 church rows, preserving every pre-existing CSV row exactly, including the earlier
  Brewster/Patterson records. No pre-existing rows or events are removed by this mapping.
  Coverage remains fully accounted: the directory's 230 church-linked entries include
  five off-site entries, leaving 225 live church-linked entries and 96 open questions;
  GCatholic's 229 church-linked entries include four off-site entries, leaving 225 live
  church-linked entries, 43 exclusions and 154 open questions. Structural audit is clean
  and validation of all dioceses passes after this policy-aware promotion. The full Python
  suite passes after current-main integration and promotion: 877 tests. The focused
  diocese suite previously passed 35 tests on the original base. CSV preservation,
  unique-slug checks and `git diff --check` also pass.
- 2026-10-11 (completed research follow-up): Reviewed all 171 original questions from
  `ff7cf609`: 89 are resolved and 82 retain concrete missing facts or ingestion blockers.
  The disposition register also lists newly discovered follow-ups, so resolved original
  identities do not hide a remaining chapel-location or connector question. Current records
  comprise 227 publishers, 291 public-Mass venues, 78 exclusions and 86 open records.
  Six unsupported publishers and their eight venues remain operationally off-site, not
  classified as closed or as permanently non-publishing. No parish inquiries were sent.
  Integrated current main through `fbaaf44d` and promoted 221 publishers / 283 venues,
  adding 220 publishers and 281 churches relative to main. All 266 pre-existing parish
  rows and 534 church rows remain exactly unchanged, including Brewster/Patterson flags;
  no existing rows or attached events are removed. Promotion is idempotent.
  Coverage is still 326/326 official directory entries and 426/426 GCatholic entries,
  with no repeated or unmatched references. Directory coverage includes 273 live and eight
  off-site church-linked entries; GCatholic includes 271 live and seven off-site entries,
  78 exclusions and 70 open entries. The two additional Staten Island venues now have
  sourced representative coordinates with their address/interior-room caveats preserved.
  Structural and relative-link/publication/address audits pass. Validation of all dioceses
  has zero errors and zero incomplete records; New York retains 43 explicit-closure
  warnings without a known exact final-Mass day. Actual last-Mass evidence is distinguished
  from merger, relegation, sale and scheduled dates; no missing days are invented.
  Final post-promotion Python suite: 976 passed, using `PYTHONUTF8=1` on Windows to
  avoid the platform-default cp1252 report-reading issue. `git diff --check` passes.
