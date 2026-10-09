# Project Carlo: Expo port to iOS and Android

Planning baseline: October 5, 2026. This document proposes implementation; it does not add a mobile app.

Build a new Expo React Native application in `apps/mobile`, keep the Vite website, and extract their shared data and schedule logic into `packages/core`. Use native navigation, controls, and maps while preserving Project Carlo's typography, colors, and schedule presentation. Keep the Python extraction pipeline and static snapshot distribution.

The confirmed first-release scope is the current public church-finder features plus offline access to previously downloaded schedules. Favorites and reminders are separate follow-ups. The internal bulletin labeler and Python administration tools remain desktop tools.

## What the repository already provides

| Existing code | Porting implication |
| --- | --- |
| `apps/web/src/api.ts` | Despite its name, this downloads one snapshot and queries it locally. Extract the query functions; replace its browser download implementation. |
| `src/pdf_extract/extract_frontend_db.py`, `apps/web/src/lib/snapshot.ts` | Shared column-oriented JSON format, currently version 1. Reuse the decoder with stronger runtime validation at the download boundary. |
| `lib/schedule.ts`, `lib/eventRollup.ts`, `types.ts`, `constants/*`, `src/utils.ts` | Mostly reusable TypeScript, with clock and timezone behavior to make explicit. |
| `components/filterState.ts`, `lib/mapView.ts`, `lib/currentLocationQuery.ts` | Reuse filter semantics, link parameters, and current-location query recognition. Move these out of UI directories where appropriate. |
| `lib/mapClusters.ts` | Pure clustering algorithm worth sharing. Native viewport, zoom, camera, and marker integration need an adapter. |
| `components/SearchTypeahead.tsx`, `placeSearch.ts` | Extract Fuse search configuration and Geoapify request/result logic; rebuild the search UI and inject configuration. |
| `components/ChurchMap.tsx` | Leaflet, DOM markers, and DOM measurements require a native map implementation. |
| React Router, Radix/shadcn, Tailwind, `tally.ts`, browser hooks | Replace their presentation/platform integration. CSS classes and HTML components do not transfer to native views. |
| Web prerendering and SEO | Stay in `apps/web`; public church URLs continue to work in browsers. |

The local snapshot inspected for this plan contains **544 churches and 3,803 events**, at **54,697 bytes compressed** and **330,553 bytes of JSON**. This is a local measurement, not a claim about the current production dataset. A single snapshot is a reasonable starting point; measure native memory and rendering before adopting regional downloads or a database API. The older browser measurements in `scaling-plan.md` are context, not native performance results.

## First-release experience

Launch directly into Explore, with a search bar, event-type selection, map, and a collapsible results sheet. Provide a list view as an accessible alternative and as the useful surface when map tiles are unavailable offline.

| Flow | Required behavior |
| --- | --- |
| Explore | Mass, Confession, and Adoration; weekday and time-range filters; clustered markers; selected-church preview. Preserve current defaults and filter semantics. |
| Search | Local church/parish name search, online place/ZIP search, and an explicit current-location action. Clearly distinguish no results from an unavailable online service. |
| Church detail | Address; weekly and dated schedules grouped by event type; notes; bulletin page references; parish website and bulletin links; the existing accuracy notice. |
| Navigation | Native back behavior returns to the same map position and filters. A church opened directly from a link has a usable path back to Explore. |
| Useful native actions | Open directions in a mapping app, share the public church URL, and open feedback with church context. |
| Offline access | After a successful download, local search, filters, results list, and church schedules survive an app restart without a connection. Display download/freshness status. |
| About/settings | Finished About copy, privacy/support links, data status, manual refresh, and a way to reset saved Explore state. The current web About page contains placeholder copy. |

Use a stack with Explore at `/`, church detail at `/churches/[churchSlug]`, and About/settings at `/about`; filters can be a sheet. Keep marketing content such as `/landing` on the website. The results list also covers the website's “browse all parishes” use case.

Offline access covers downloaded church data. Base-map tiles, Geoapify searches, feedback, websites, bulletins, and external directions require their respective services. First launch without a connection shows a clear retry screen; a bundled seed dataset is optional and is not assumed here.

## Architecture and dependencies

```text
Python extraction -> validated static snapshots on projectcarlo.com
                                     |
                          +----------+----------+
                          |                     |
                     apps/web              apps/mobile
                          |                     |
                          +--- packages/core ---+
                          +--- packages/theme --+
```

`packages/core` owns domain types, snapshot validation/decoding, schedule calculations, filtering, rollups, search ranking, clustering, and portable link codecs. It should have no React, DOM, Leaflet, Vite, or Expo dependencies. Inject configuration, a clock/calendar context, and data access where needed. Move existing unit tests and the cross-language snapshot fixture with their code.

`packages/theme` contains a small set of semantic color, spacing, and typography tokens. Convert the existing OKLCH colors to native-compatible values and retain a web mapping. Share assets where practical; maintain separate web and native components.

`apps/mobile` owns screens, Expo Router layouts, snapshot storage/refresh, native permissions, map rendering, links, and app lifecycle handling. Put providers and query setup in the root layout. Keep filter and camera state in a small context/reducer; persist only useful preferences, not every in-flight search or raw location fix.

| Concern | Initial choice |
| --- | --- |
| Runtime/navigation | Stable Expo SDK selected and pinned at implementation kickoff, TypeScript, Expo Router, development builds, Continuous Native Generation. |
| Maps | `react-native-maps`, with Apple Maps on iOS and Google Maps on Android. Validate the selected versions in a real build before developing the full map. |
| UI | React Native `StyleSheet`, shared tokens, `react-native-safe-area-context`, `react-native-svg` for ornaments/icons, and an Expo-compatible bottom-sheet library such as `@gorhom/bottom-sheet`. |
| Gestures | Expo-compatible React Native Gesture Handler and Reanimated versions; verify sheet/map/slider gesture interaction early. |
| Fonts | `expo-font` with bundled, appropriately licensed Cardo and EB Garamond font files. Prefer tested static weights initially; web Fontsource CSS is not a native font loader. |
| Data/query lifecycle | Retain TanStack Query where useful for network state, and connect its focus/online managers to native app state and connectivity. |
| Storage | `expo-file-system` document storage for the snapshot; AsyncStorage for small preferences. Use a recoverable file-and-metadata commit protocol. |
| Decompression | A React Native-compatible gzip library such as `fflate`, verified on Hermes. The current `DecompressionStream`/`Blob.stream()` path is browser-specific. |
| Device integrations | `expo-location` for foreground location; `expo-web-browser` for web content; React Native Linking and Share for external actions. |
| Builds/releases | EAS Build and Submit; introduce EAS Update only with runtime-version policy and separate preview/production channels. |

Select exact package versions through the chosen Expo SDK's compatibility guidance and `expo install`; run Expo Doctor and inspect native-library compatibility. Do not independently choose the newest React/React Native versions. Keep React a peer dependency if any future shared package contains hooks, and prevent multiple React copies in a single app's dependency graph.

Add `packages/*` to `pnpm-workspace.yaml`. Use workspace package exports rather than importing `apps/web/src` from mobile. Check Metro, Vite, Vitest, and the `tsx` prerenderer against the shared exports. Test the repository's pnpm 12 install/linker behavior in EAS before changing workspace-wide package-manager settings; the web package currently declares a different pnpm version from the root.

## Data delivery, offline storage, and schedule correctness

### Preserve static distribution, add a durable mobile contract

The existing `/frontend.json.gz` is served as opaque gzip bytes, with browser-side decompression and cache revalidation. A native app needs an absolute HTTPS URL and must not rely on browser streaming APIs or browser cache options. Start the prototype with that payload.

Before public beta, publish a small **versioned manifest and immutable snapshot files** alongside the current web asset, for example `/data/v1/manifest.json` referencing `/data/v1/<hash>.json.gz`. Proposed manifest fields are `schemaVersion`, `generatedAt`, `snapshotUrl`, `sha256`, and `byteLength`. These fields and endpoints do not exist yet; add them to the exporter/publishing workflow and test them.

The manifest must become visible only after its referenced snapshot is available. Keep previously published assets and supported schema endpoints available across deployments. An old installed app must continue receiving a compatible feed after a web deployment; a single overwritten asset with a new schema would strand it. Verify static-host routing returns the actual manifest/data, not the SPA fallback for missing paths. Schema changes require a supported-version and retirement policy.

Use conditional requests for the manifest where supported. Persist the last good snapshot, its revision/hash, publication metadata, and local download time. A successful check can update `lastCheckedAt`; it must not relabel old data as newly generated. Global snapshot generation time is not the age of each parish's bulletin. Per-parish freshness requires extra source metadata if added later.

### Refresh behavior

1. On launch, validate and open the last good local snapshot immediately, then check for updates when online.
2. On a new revision, download to a temporary file with timeout and size bounds; verify bytes/hash, supported schema, table lengths, and references before accepting it.
3. Commit the validated snapshot and metadata through a recoverable pointer/version swap, then rebuild the repository indexes and invalidate dependent queries. An interrupted write must leave the previous snapshot usable.
4. On download, validation, disk, or unsupported-version errors, retain the last good data and show a non-blocking status with retry. With no valid data, show the first-load error state.
5. Recheck on foregrounding if the last successful check is more than six hours old, on connectivity recovery when stale, and on manual refresh. Treat six hours as an initial policy to tune, not a server guarantee. Background execution is not required.

Do not persist computed `SnapshotEvent` objects: their methods/getters and cached occurrences are derived state. Persist the source data and decode it again. The current module-level `snapshotPromise`, map-item memo, and lazily cached occurrence assume a short-lived immutable web session; replace them with a repository scoped to a snapshot revision and calendar context. Query keys/invalidation must account for both.

### Time and cancellation behavior

Schedule times are local wall-clock times at the church. Current occurrence calculations use the device's local timezone and memoize results indefinitely. Introduce an explicit reference time and church timezone before reusing this in a long-running mobile app.

For the current New York coverage, an explicitly configured `America/New_York` region is a viable initial default after confirming coverage. Before expansion across timezones, publish an IANA timezone per church or region; never infer it solely from a state name. Use a timezone-aware implementation tested on Hermes and Node.

Recompute derived schedules on foregrounding and at the church-local date boundary while active, even when no data download occurs. Preserve the existing date-based behavior that includes earlier events on the same day; a future “next service starting now” feature needs separate semantics. Keep cancellations excluded and dated events from past days hidden in schedule views. Test and resolve the existing difference between map filtering and detail filtering for past dated events, so the mobile list/map does not advertise expired-only matches.

## Native integrations that need explicit work

**Map:** reuse clustering and viewport culling, not Leaflet components. Convert native camera/region information into the shared algorithm's bounds and zoom convention; verify cluster expansion, padding for the results sheet, and selection persistence on both providers. Native zoom values and screen density cannot be assumed to match Leaflet. Start with simple image markers and cluster counts, then add branding after profiling. Keep map attributions visible.

**Search and location:** inject Geoapify configuration instead of reading `import.meta.env`. Preserve debounce, request cancellation, country restriction, ZIP handling, and local Fuse ranking. Review the current Rochester proximity bias for broader coverage. Request foreground location only after the user taps the action; support denial, approximate location, timeout, and disabled services with manual search. No background-location permission is needed.

**API configuration:** Expo public environment variables are bundled into the application. Confirm Geoapify's supported mobile-client restrictions, attribution, and quota configuration. If the browser-only key policy does not support native clients, use a small rate-limited proxy for place search. Google Maps Android configuration requires a restricted key and build-variant signing fingerprints. Keep R2 credentials and extraction-service keys out of the app.

**Feedback and bulletin links:** open the hosted Tally form in the system browser surface with the existing `page_path`, `full_url`, `church_slug`, and `church_name` parameters. Construct context from the route and canonical website URL rather than `window.location`. Preserve visible bulletin page numbers; external PDF viewers may ignore `#page=`, so do not promise automatic navigation to that page. Test external links on Android and iOS.

**Deep links:** preserve `https://projectcarlo.com/churches/<slug>` and the current filter/map query parameters where meaningful. Add iOS Associated Domains and Android App Links, with correctly served `apple-app-site-association` and `assetlinks.json` files on the website. Test real release signing identities, cold/warm starts, invalid slugs, and browser fallback. Invalid link parameters fall back to safe defaults. Use a custom scheme for development if useful.

**Accessibility and visual design:** retain the paper/ink/rubric palette, serif hierarchy, ornaments, and clear schedule grouping. Adapt to safe areas, Android edge-to-edge behavior, keyboard overlap, text scaling, screen readers, reduced motion, and platform-sized touch targets. Provide accessible time inputs as well as any slider. Keep the list fully usable without manipulating the map.

## Implementation sequence and estimates

Estimates assume one engineer experienced with React/TypeScript, access to both platforms for testing, the scope above, and no account system or notification service. These are planning ranges, not commitments; revise them after the map/build spike.

| Phase | Work and dependency | Exit condition | Engineering days |
| --- | --- | --- | --- |
| 1. Native feasibility | Create Expo shell, workspace wiring and EAS profiles. Prove snapshot decoding, native map, fonts, and location in development builds. Start developer-account/signing setup. | iPhone and Android builds show real churches, load the same fixture, and handle denied location; package/provider choices recorded. | 2–3 |
| 2. Shared core | Extract types, queries, schedule, filters, search configuration, clustering, and tokens. Move tests; separate browser transport and configuration. | Web unit tests, typecheck, and prerender/build pass with shared packages; mobile imports no DOM/Vite modules. | 3–5 |
| 3. Data lifecycle | Versioned static publication, validation, persistent storage, refresh, clock/timezone handling, and failure recovery. Depends on the data interfaces from phase 2. | Offline restart, interrupted download, incompatible schema, midnight/resume, and old-client compatibility cases pass. | 4–6 |
| 4. Product flows | Explore map/list, filter sheet, local/place search, church detail, external actions, feedback, About/settings, and deep links. Depends on shared core; use fixture data while phase 3 settles. | The first-release flows work on both platforms, including back navigation, missing data, and accessible list use. | 6–9 |
| 5. Beta and release | Device profiling, accessibility fixes, native E2E tests, signing/link verification, store assets/privacy disclosures, TestFlight and Play testing, release workflow. | Release checklist passes; installable production candidates and store submissions are ready. | 5–7 |

Total: **20–30 engineering days**, roughly **4–6 focused weeks**. Allow **5–7 calendar weeks** for beta feedback and coordination; store review, account verification, and any account-specific testing requirements can extend this. A build/map proof of concept should be available in the first week.

Use small reviewable changes: Expo spike; shared domain extraction; data contract/storage; Explore/search; church detail/links; release hardening. Avoid combining the web refactor and complete native UI into one change. This is an implementation order, not authorization to create or publish releases now.

## Validation and release gates

- **Shared behavior:** retain existing Vitest coverage for filtering, weekday mapping, schedule ordering, rollups, clustering, and snapshot fixtures. Add meaningful regressions for explicit timezone/reference-time behavior, expired events, malformed payloads, and revision invalidation. Keep Python exporter/TypeScript decoder agreement tested.
- **Web regression:** run `pnpm --filter web test`, `pnpm check:web`, `pnpm lint:web`, and `pnpm build:web`, plus existing home/landing/not-found Playwright flows when shared behavior changes. Supply a valid snapshot for prerendering. Update `deploy-web.yml` path filters to include shared packages so core changes actually deploy.
- **Native component tests:** use React Native Testing Library with an Expo-compatible test setup for filter application, denied location, offline status, error recovery, and navigation state. Unit tests cannot validate real map/provider behavior.
- **Native E2E:** use Maestro against development/release-like builds on both platforms for launch, search, filters, detail/back, deep links, and cached offline restart. Use controlled fixtures for deterministic flows and separate live-service smoke checks.
- **Lifecycle/data matrix:** first launch online/offline; airplane-mode restart with saved data; network recovery; corrupt cache; interrupted replacement; manifest referencing missing data; unsupported schema; app suspension across midnight/DST; device timezone different from church; same-day schedules and cancellations.
- **Performance:** profile release builds on a named mid-range Android device and an older supported iPhone, with current and expanded fixtures. Initial goals: cached Explore usable within two seconds, settled filter changes reflected within 100 ms at current scale, and smooth map/sheet interaction without rendering the whole dataset as markers. Treat these as targets to verify in phase 1/5, not measured results.
- **CI:** add core/mobile typecheck, lint, and unit jobs. Keep build checks for shared-package consumers. Run native simulator/emulator smoke tests on suitable runners and EAS builds for release candidates; do not require full signed store builds for every documentation change.
- **Store readiness:** stable bundle/package IDs and signing ownership; production map keys; app/adaptive icons and splash; phone screenshots; support and privacy URLs; location purpose strings; accurate Apple privacy/Google Data Safety answers covering maps, geocoding, and feedback. Finish About copy. Start Apple Developer and Google Play account work early.
- **Delivery environment:** Windows can run Metro and the Android emulator. EAS supplies cloud iOS builds; physical iPhone development builds require appropriate signing/provisioning. Local iOS simulator or Xcode debugging requires macOS, so arrange Mac or hosted macOS test access.
- **Release/rollback:** separate development, preview, and production configuration. Verify both store candidates on devices. If adopting EAS Update, pin runtime compatibility and test rollback; native module/config changes require a new binary. Data refreshes remain independent of app updates and must preserve old-client compatibility.

## Follow-ups after the first release

Favorites can start as local church slugs without accounts, with migration/removal handling when coverage changes. Reminders need a separate design for church-local timezones, DST, changing/cancelled schedules, notification permission, and rescheduling limits; remote push would add infrastructure. Neither should hold up the initial port.

Revisit regional snapshot downloads only when measured load/memory/refresh costs justify them. Consider offline base maps only with a provider and download policy that support that feature. Cross-device sync/accounts are a separate product/backend decision.

The current-features-plus-offline scope is confirmed. Before implementation, establish access to both store accounts and devices, minimum OS/device support, and whether identical map appearance across platforms is a requirement. The plan otherwise assumes native Apple/Google basemaps and one mobile codebase serving both platforms.

## Implementation reference points

Check current guidance when pinning the SDK and libraries; this plan intentionally does not prescribe an unverified latest version.

- [Expo monorepos](https://docs.expo.dev/guides/monorepos/)
- [Expo development builds](https://docs.expo.dev/develop/development-builds/introduction/)
- [Expo Router](https://docs.expo.dev/router/introduction/)
- [React Native Maps in Expo](https://docs.expo.dev/versions/latest/sdk/map-view/)
- [Expo linking](https://docs.expo.dev/linking/overview/)
- [EAS Build](https://docs.expo.dev/build/introduction/) and [EAS Submit](https://docs.expo.dev/submit/introduction/)
- [EAS Update runtime versions](https://docs.expo.dev/eas-update/runtime-versions/)
