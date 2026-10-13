# Project Carlo — UI Copy Audit

An audit of every visitor-facing string in `apps/web` (October 2026): the map,
the landing page, church, city and all-churches pages, errors and empty states,
and page titles and share metadata. The internal labeler (`apps/labeler`) is out
of scope.

Each finding gives the current copy, a suggested replacement, and the file it
lives in. The priority list comes first, then a terminology guide, then the
findings screen by screen.

**Status.** Recommendations 2, 4, 5, 6 and 7 are implemented, along with the
filter headings ("Looking for", "Starting"), next steps on error and empty
states, query echoes in "no results" messages, curly apostrophes, shorter
church page titles, and `apps/web/src/copy.ts` for shared strings. The rest
(1, 3, 8, 9, and the other per-screen suggestions) are still open. The tables
below describe the copy as it was before those changes.

## Summary

**What already works.** The voice is distinctive and mostly consistent:
sentence case, lowercase `a.m.`/`p.m.`, small caps for labels, italic serif for
asides, and no exclamation marks or marketing filler. Microcopy is short and
concrete ("Show 12 churches", "Suggest an edit", "Latest parish bulletin
(PDF)"). The bulletin page references ("Found on bulletin page 3") are a strong
trust feature that few listing sites have.

**What holds it back.** The gaps are not tone. They are things the copy never
says:

1. **It never says where it works.** Every surface promises times "near you",
   but the data covers about 540 churches in five New York dioceses (Albany,
   Buffalo, New York, Rochester, Syracuse). A visitor from Ohio lands on a map
   of New York with no explanation.
2. **It never says how fresh the times are.** The disclaimer says "latest
   available bulletin" but gives no date, and that date is what a visitor needs
   in order to decide whether to trust a time.
3. **The map popup mislabels its own contents.** It is headed "Upcoming", but it
   shows a weekly schedule filtered to one service, and it never names the
   service.
4. **One action has seven names.** "Use my location" alone appears as "Or use my
   current location", "Use your current location", "Use exact location", "Go to
   my exact location", "Requesting your location…", "Finding your location…" and
   "Locating…".
5. **Empty and error states are dead ends.** Nothing says "no churches match"
   when filters empty the map. "Couldn't load data" and "Page not found" offer
   no next step.

## Top recommendations (in priority order)

| # | Recommendation | Effort | Where |
|---|---|---|---|
| 1 | **State the coverage area** in the tagline area, the index intro, and the meta descriptions, and show a notice when the visitor's estimated location is outside it. | S–M | `HomePage.tsx`, `LandingPage.tsx`, `seo.ts`, `index.html`, `StaticChurchIndexPage.tsx` |
| 2 | **Name the service in the map popup.** Replace the "Upcoming" kicker with the active service ("Mass", "Confession", "Adoration"). | S | `ChurchMap.tsx:395` |
| 3 | **Add a map empty state** for when filters leave no churches, with a way out ("Try another day or a wider time range" plus "Reset filters"). Change the "Show 0 churches" button to match. | S | `HomePage.tsx`, `FilterPanel.tsx:233` |
| 4 | **Use one disclaimer and one source line everywhere**, and say "times", not "Mass times", on pages that also list Confession and Adoration. | S | `ChurchPageContent.tsx:382`, `CityPageContent.tsx:246`, `LandingPage.tsx:249`, `seo.ts` |
| 5 | **Show the bulletin date** on church pages ("From the bulletin for Sunday, Oct 5"). This needs the pipeline to put the bulletin date in the snapshot. | M (data) | snapshot, `ChurchPageContent.tsx` |
| 6 | **Settle on one label for each action and concept** (see the terminology guide below) and keep the shared strings in one module. | S | new `src/copy.ts` |
| 7 | **Rename "Back to map"** to "Map" or "Open the map" on pages a visitor can enter directly from a search engine. "Back" is wrong for a first page view. | XS | `SiteHeader.tsx:14`, `StaticChurchIndexPage.tsx:116`, `NotFoundPage.tsx`, `AboutPage.tsx` |
| 8 | **Write the About page.** It is all placeholder and lorem ipsum (behind a feature flag), and it is the natural place to explain the name, the method and the coverage. A draft is below. | M | `AboutPage.tsx` |
| 9 | **Turn on church-name search on the map**, or say in the placeholder that you can't search by name. Both callers pass `hideModeToggle`, so church search is unreachable in the app, yet "St. Mary's" is the most natural thing to type. | S | `HomePage.tsx:421`, `LandingPage.tsx:178`, `SearchTypeahead.tsx` |

## Terminology guide

Choose one term for each concept and use it everywhere. Suggested choices:

| Concept | Use | Avoid (currently in use) |
|---|---|---|
| The three things you can search for | **Mass, Confession, Adoration**, collectively **"services"** in UI and **"times"** in prose | "Service type" as a heading (see the filter panel below), "Mass times" when the page lists all three |
| A place of worship | **church** | "parish" (internal search mode), "Unnamed church" vs "Catholic Church" vs "Catholic church" vs "Church" as fallbacks |
| Where the data comes from | **"the parish bulletin"** | "weekly bulletin", "latest available bulletin", "official parish source", "parsed", "extracted", "sourced" in rotation |
| How it was read | **"read by AI"** (once, in the disclaimer) | "parsed" (developer jargon) in public copy |
| Browser geolocation | **"Use my location"** / **"Finding your location…"** | the seven variants listed in the summary |
| A searched place's marker | **"pin"** throughout: "Pinned: Buffalo" / "Remove pin" | "Searched place" (popup kicker) |
| Clearing a filter | **"Any day"** / **"Any time"** / **"Clear filters"** | "Reset" / "Reset all" |
| The church list page | **"Church list"** | "Browse all churches" (footer), "All churches" (the earlier name) |
| Link to the map | **"Map"** or **"Open the map"** | "Back to map" on pages entered directly |

**Fallback name.** Use `"Unnamed church"` in the UI and the same string in
titles and JSON-LD. Today `seo.ts` uses "Catholic Church", "Catholic church",
"Church" and "this church" in different places.

## Screen-by-screen findings

### Map home (`/`) — floating card

| Element | Current | Suggested | Why |
|---|---|---|---|
| Tagline (`<h1>`) — `Masthead.tsx:20` | Mass, Confession & Adoration times near you | Keep it. Add a short coverage line under the search box on a first visit: *"Covering 540 churches in five New York dioceses."* | "Near you" overpromises outside New York. One quiet line fixes that without losing the hook. |
| Approximate-location line — `HomePage.tsx:447` | Near **Buffalo, NY** · approximate *(the "approximate" note is hidden on phones)* | **Near Buffalo, NY** (estimated) — or show "approximate" on phones too, since it is short | On phones nothing says the location is a guess, so "Use exact location" beside it reads like a correction of an error. |
| Visitor outside the covered area | *(nothing; the map silently shows the whole of New York)* | *"We don't cover your area yet. Showing New York State."* | `firstVisitStart` already knows when no church is in range (`kind: "area"`). Say so. |
| Exact-location button — `HomePage.tsx:464` | Use exact location / Locating… | Use my location / Finding your location… | One label everywhere (see the terminology guide). |
| Pinned place row — `HomePage.tsx:471` | Pinned: **Buffalo** · Remove pin | Keep it. | Clear. Make the popup kicker match ("Pinned place", not "Searched place"). |
| Header links — `HomePage.tsx:406` | All churches · About | Keep them. | — |
| Loading — `HomePage.tsx:366` | Loading map… | Keep it. | — |
| Load error — `HomePage.tsx:375` | **Couldn't load data** / Check your connection and try again. / Try again | **Couldn't load churches** / Check your connection and try again. / Try again | "Data" is developer language. Name the thing that failed. |
| Filters button (mobile) | Filters | Show a count when filters are active: **Filters (2)** | A visitor can see at a glance that the map is filtered. The mobile `FilterPills` row helps, but it isn't on the button. |
| Active filters row (mobile) — `FilterPills.tsx` | SHOWING Confession · Saturday · 3 p.m. – 6 p.m. | Keep it. For 4+ days, list abbreviations ("Mon, Wed, Fri, Sat") rather than "4 days". | "4 days" makes the visitor open the panel to learn which days. |
| No churches match *(not handled)* | *(empty map, no message)* | Overlay: *"No churches have Confession on Tuesday between 6 and 8 a.m."* + **Clear filters** | Today an empty map looks like a broken map. |

### Search box and suggestions — `SearchTypeahead.tsx`

| Element | Current | Suggested | Why |
|---|---|---|---|
| Placeholder | Search for a city, ZIP, or address… | If church search is turned on: **"Search a town, ZIP, or church name…"**. Otherwise keep it. | Most people will type a church name. Today they get Geoapify place results for it. |
| First suggestion | Use your current location / *Center the map where you are* | **Use my location** / *Show churches around you* | Matches the other location labels. The subtitle describes the benefit, not the mechanism. |
| Current-location pin — `placeSearch.ts:65` | Your current location / *From your browser* | **Your location** (no subtitle) | "From your browser" exposes plumbing. |
| Popover heading | Places / Matching churches | Keep it. | — |
| Empty result | No matching places. | No places match "**{query}**". Try a town name or ZIP code. | Echo the query and suggest a fix. |
| Place search error | Place search failed. Try again. | Couldn't search places just now. Try again, or search by ZIP code. | Softer, and offers a path. |
| Missing-key error | Place search needs a Geoapify API key. | Keep it for dev builds. In production show the generic error above. | Developer-facing string that could reach visitors. |
| Attribution | Powered by Geoapify | Keep it (required). | — |

### Filter panel — `FilterPanel.tsx` (map) and `LandingPage.tsx` (refine section)

| Element | Current | Suggested | Why |
|---|---|---|---|
| Section heading | SERVICE TYPE | **LOOKING FOR** | Reads as a question the visitor answers. "Service type" is form language, and many Catholics wouldn't call Adoration a "service". |
| Section heading | DAY OF WEEK | **DAY** | "of week" adds nothing next to Sun–Sat buttons. |
| Section heading | TIME OF DAY | **STARTING** | The filter matches a service's *start* time (`api.ts:115`). The current label implies a service that runs within the window. |
| Slider readout (default) | 12 a.m. *through* 11:59 p.m. | **Any time** | The default state reads like a mistake. Show the range only once it has been narrowed. |
| Slider readout (narrowed) | 6 a.m. *through* 12 p.m. | **6 a.m. – noon** | Use the en dash the rest of the site uses for ranges, and "noon"/"midnight" to match the tick labels (which already say "noon"). |
| Per-section clear | Reset | **Any day** / **Any time** | Name the state the button returns to, not the operation. |
| Panel clear | Reset all | **Clear filters** | — |
| Mobile apply button | Show 12 churches / Show 0 churches | Show 12 churches / **No churches match** (disabled), with a hint above it | "Show 0 churches" is a button that leads nowhere. |
| Desktop footer link | Share feedback | Move it to the card's header links or a site footer, so phones get it too | Feedback sits inside the filter panel on desktop and is missing from the map on phones. |

### Map popup — `ChurchMap.tsx`

| Element | Current | Suggested | Why |
|---|---|---|---|
| Schedule kicker | ── UPCOMING ── | ── **MASS** ── (or CONFESSION / ADORATION, matching the filter) | The rows are weekly days ("Sunday 8 a.m."), not upcoming dates, and they show only the selected service. A visitor who filtered to Confession sees times with no word saying they are Confession times. Keep "Upcoming" only for the dated fallback (churches with no weekly schedule). |
| Filtered schedule | *(rows silently limited by the day and time filters)* | When filters narrow the rows, add a foot line: *"Showing Saturday only · Full schedule →"* | Otherwise the popup suggests the church has a single Mass a week. |
| Overflow | …and 2 more days | Keep it. | — |
| Empty | No services listed yet. | No times listed yet. | Matches the "times" vocabulary. It is rarely reachable, since unmatched churches aren't drawn. |
| Footer link | Full schedule → | Keep it. | — |
| Cluster tooltip | 12 churches — zoom in | Keep it. | — |
| Place pin kicker | SEARCHED PLACE | **PINNED PLACE** or **YOUR LOCATION** | Matches the card's "Pinned:" row. |

### Church page — `ChurchPageContent.tsx`

| Element | Current | Suggested | Why |
|---|---|---|---|
| Header link — `SiteHeader.tsx` | ← Back to map | **← Map** or **Find churches on the map** | Most church page visits start on Google. There is no "back". |
| Action links | Visit the parish website · Latest parish bulletin (PDF) · Suggest an edit | Keep them. If the bulletin link is the one the times were read from, say **"Bulletin these times came from (PDF)"**. | "Latest" may not be the bulletin the times came from, and that is the one that matters for checking. |
| Freshness *(missing)* | — | Under the address: *"Times from the bulletin for Sunday, October 5."* | The single strongest trust signal available. It needs the bulletin date in the snapshot. |
| Section page reference | *Found on bulletin page 3* | *Bulletin, p. 3* ↗ | It is a link, so a shorter noun phrase reads more like one. Optional. |
| Dated-row fallback | SPECIAL | **ONE-TIME** | "Special" is vague. These are one-off dated services with no date recorded. |
| No events | No Mass, Confession, or Adoration times are listed for this church yet. | **No times listed yet.** The parish bulletin may not include them, or we couldn't read it. Check the parish website, or *suggest an edit*. | Explain why, and give the next step. |
| Disclaimer | Mass times are extracted with AI from each parish's latest available bulletin and may contain mistakes. Please confirm details with an official parish source before attending. | **Times are read from the parish bulletin by AI and can contain mistakes. Please check with the parish before you go.** | "Mass times" is wrong on a page that also lists Confession and Adoration. Shorter and plainer, and "check with the parish" is concrete where "an official parish source" is vague. |
| Footer link | Browse all churches | **All churches** | Same label as the breadcrumb. |
| Not found — `ChurchPage.tsx` | Church not found / We couldn't find that church. / ← Back to map | Church not found / *It may have closed, merged, or moved to a new address.* / **All churches** · **Map** | Closed churches 404 by design (`seo-plan.md`), so say that is the likely reason, and give two ways forward. |
| Load errors | We couldn't load this church. / We couldn't load times for this church. | Keep them. | — |

### City page — `CityPageContent.tsx`

| Element | Current | Suggested | Why |
|---|---|---|---|
| `<h1>` | Mass Times in East Aurora, NY | **Mass times in East Aurora, NY** | Every other heading is sentence case. Search engines don't weigh case. |
| Subhead | Sourced from each parish's weekly bulletin. | **3 churches · times from each parish bulletin** | A fragment that starts with "Sourced" reads oddly alone. A count orients the visitor. |
| No Mass row | No weekly Mass times listed. | Keep it. | — |
| Secondary disclosure | ▶ Confession & Adoration times | Keep it. | — |
| Nearby distance | Aurora, NY · 2.3 mi | Aurora, NY · **2.3 mi away** (or "from East Aurora") | Distance from what? It is measured from the town center, so say so. |
| Disclaimer | *(the "Mass times are extracted with AI…" text)* | Use the shared disclaimer above. | One string, one place. |
| Not found — `CityPage.tsx` | City not found / We don't list any churches in that city yet. | Keep it, and add an **All churches** link. | Good copy, but no way forward. |

### All-churches index — `StaticChurchIndexPage.tsx`

| Element | Current | Suggested | Why |
|---|---|---|---|
| Top link | Back to map | **Map** | Same reason as the church page. |
| Intro | Mass, Confession & Adoration times at 540 Catholic churches, parsed from each parish's weekly bulletin. | Mass, Confession & Adoration times at 540 Catholic churches **across five New York dioceses**, from each parish's weekly bulletin. | Coverage again. Drop "parsed". |
| Search status | Showing 3 of 540 churches. | Keep it. | — |
| Empty search | No churches or cities match your search. | No churches or cities match "**{query}**". | Echo the query. |
| Group fallback | Other locations | **Address unknown** | Says why these churches are grouped together. |

### Landing page (`/landing`, not indexed)

| Element | Current | Suggested | Why |
|---|---|---|---|
| Location link | Or use my current location / Requesting your location… | **Or use my location** / Finding your location… | Matches the other location labels. |
| Refine toggle | Refine your search / Hide refinements | **Filter by service, day & time** / **Hide filters** | Says what's inside. "Refinements" is an unusual word. |
| Submit | Show on map → | Keep it. | — |
| Footer (desktop) | A directory of Catholic churches — schedules parsed from each parish's weekly bulletin. | **Catholic churches across New York, with times from each parish's weekly bulletin.** | Coverage, no "parsed". |
| Footer (mobile) | Schedules parsed from each parish's weekly bulletin. | **Times from each parish's weekly bulletin.** | — |

### About page — `AboutPage.tsx`

Currently all placeholder text, including lorem ipsum. It is hidden behind
`isAboutPageEnabled`, but it needs real copy before the flag goes on. A draft
is under [Draft About copy](#draft-about-copy) below.

### Generic 404 — `NotFoundPage.tsx`

| Current | Suggested |
|---|---|
| Page not found / We couldn't find what you were looking for. / ← Back to map | Page not found / *That link may be out of date.* / **Map** · **All churches** |

### Location errors — `browserLocation.ts`

| Current | Suggested | Why |
|---|---|---|
| Location is blocked. Allow it in your browser's site settings. | Keep it. | Clear and actionable. |
| Couldn't get your current location. | Couldn't find your location. **Try searching for your town instead.** | Give a fallback. |
| Location is not available in this browser. | Your browser can't share your location. Try searching for your town instead. | — |

## Titles, descriptions and share metadata — `seo.ts`, `index.html`, `site.webmanifest`

| Item | Current | Suggested | Why |
|---|---|---|---|
| Home description (4 copies: `seo.ts` plus 3 meta tags in `index.html`) | Find Mass, Confession, and Adoration times at Catholic churches on an interactive map. Schedules are parsed from each parish's weekly bulletin. | Find Mass, Confession, and Adoration times at 540 Catholic churches across New York, on a map, from each parish's weekly bulletin. | Coverage and scale in the snippet, and no "parsed". Consider generating `index.html`'s copies from `seo.ts` (as the JSON-LD already is) so they can't drift. |
| Church title | {Name} — Mass, Confession & Adoration Times in {City, ST} | {Name}, {City} — Mass & Confession Times | It currently runs to 70–90 characters and is truncated in results before the city. Lead with name and city. |
| City title | Catholic Mass Times in {City, ST} — Confession & Adoration · Project Carlo | Mass Times in {City, ST} · Catholic Churches · Project Carlo | Shorter. The "— Confession & Adoration" tail is cut off in most results. |
| Separators | Mix of "—" and "·" between title parts | Use "·" before the site name and "—" (or ",") inside the title | Mixed today. |
| Manifest description | Find Mass, Confession, and Adoration times at Catholic churches on an interactive map. | Keep it, or add "in New York". | — |
| Share image / OG alt | Mass, Confession & Adoration times near you | Keep it as the brand line, but coverage should appear in the description. | — |

## Mechanics and style

- **Apostrophes are mixed.** JSX uses curly quotes in some places (`parish’s`,
  `&rsquo;`) and straight ones in others (`&apos;`, and every JS string such as
  `"Couldn't load data"`, `"We couldn't find…"`). For a typographically careful
  design, use `’` everywhere.
- **Ampersand vs "and".** Displays and titles use "Mass, Confession &
  Adoration"; sentences use "Mass, Confession, and Adoration". That is a fine
  rule. Write it down and fix the exceptions (the index intro uses "&" in a
  sentence).
- **Time ranges.** The site uses an en dash with spaces ("3 p.m. – 6 p.m."),
  except the slider, which says "through". Use the en dash there too, and use
  "noon" and "midnight" in place of "12 p.m." and "12 a.m." in readouts, as the
  tick labels already do.
- **Day labels.** The schedule uses "Sunday", the rollups "Mon – Fri" and
  "Sat & Sun", and the filters "Sun"–"Sat". All are consistent with each other.
  Keep them.
- **Ellipses.** Loading states use a true ellipsis (`…`). Keep it that way.
- **Shared strings.** The disclaimer is duplicated verbatim in two components,
  and the home description in four places. Put shared copy (disclaimer, source
  line, location labels, fallback church name, empty and error states) in one
  `src/copy.ts` so a wording change is a one-line edit. The prerenderer already
  imports from `src/`, so static pages would pick it up too.

## Draft About copy

> **About**
>
> Project Carlo helps you find Mass, Confession and Adoration times at Catholic
> churches near you, all on one map.
>
> **How it works**
> Every week we collect each parish's bulletin, the one handed out at Mass, and
> use AI to read its schedule. You can always open the bulletin page a time came
> from. AI makes mistakes, and parishes change times for holidays and feasts, so
> please check with the parish before you go.
>
> **Where it works**
> We currently cover about 540 churches in the dioceses of Albany, Buffalo, New
> York, Rochester and Syracuse, and we're adding more.
>
> **The name**
> *(If it refers to St. Carlo Acutis, the young patron of the internet, one
> sentence on why he fits a project like this.)*
>
> **Get in touch**
> Spotted a wrong time, or want your parish added? Use *Suggest an edit* on any
> church page, or *Share feedback*.

## Implementation notes

- Most changes above are string edits in the files cited. The exceptions:
  - **Coverage notice for out-of-area visitors** needs `firstVisitStart`'s
    `"area"` outcome surfaced to `HomePage` (it is already computed).
  - **Map empty state** needs a check on `mappedChurchCount === 0` in
    `HomePage`.
  - **Popup service kicker** needs the active event type passed into the
    popup, or attached to `ChurchMapItem`.
  - **Bulletin date** needs a new field in the snapshot from the pipeline.
  - **Church-name search** is already implemented in `SearchTypeahead`. Only
    the `hideModeToggle` props hide it.
- Keep the prerendered pages (`src/prerender/*`) in step with their SPA twins.
  They share `ChurchPageContent` and `CityPageContent`, but the index page and
  `seo.ts` strings are separate.
