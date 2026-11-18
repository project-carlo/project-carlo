import { Fragment, type ReactNode } from "react";
import { Link } from "react-router-dom";
import type { CityChurchEntry, CityPageData } from "../api";
import {
  type ChurchBase,
  type ContinuousAdoration,
  continuousRow,
  EVENT_TYPE_LABELS,
  type EventSummary,
  type EventType,
  formatAddress,
  type ScheduleRollupRow,
  weeklyScheduleRows,
} from "@carlo/core";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { CityMapPreview } from "@/components/CityMapPreview";
import { Fleuron } from "@/components/Fleuron";
import { MapPinIcon } from "@/components/icons";
import { SiteHeader } from "@/components/SiteHeader";
import { cityPath, formatMiles } from "@/lib/cities";
import type { CityMapConfig } from "@/lib/cityMap";
import { CHURCH_INDEX_PATH, churchPath } from "@/lib/seo";
import { CHURCH_LIST, DISCLAIMER, SOURCE_PHRASE, UNNAMED_CHURCH } from "@/copy";

/** The services a card tucks behind "Confession & Adoration times". */
const SECONDARY_TYPES: EventType[] = ["confession", "adoration"];

function eventsOfType(events: EventSummary[], type: EventType): EventSummary[] {
  return events.filter((e) => e.type === type);
}

/** Day → times rows with a dotted leader, the map popup's schedule layout. */
function ScheduleRows({ rows }: { rows: ScheduleRollupRow[] }) {
  return (
    <ul className="space-y-1">
      {rows.map((row) => (
        <li key={row.key} className="font-serif text-[0.975rem]">
          <div className="flex items-baseline gap-2">
            <span className="smallcaps text-[0.9375rem] text-ink">{row.label}</span>
            <span className="min-w-3 flex-1 translate-y-[-3px] border-b border-dotted border-rule-strong" />
            <span className="text-right tabular-nums text-rubric">
              {row.times.map((time, index) => (
                <Fragment key={time}>
                  {index > 0 ? " · " : null}
                  <span className="whitespace-nowrap">{time}</span>
                </Fragment>
              ))}
            </span>
          </div>
          {/* A monthly or seasonal slot's qualifier, as in the map popup. */}
          {row.note ? (
            <div className="text-[0.875rem] leading-snug italic text-ink-faint">
              {row.note}
            </div>
          ) : null}
        </li>
      ))}
    </ul>
  );
}

/**
 * A native disclosure, so it opens and closes on the prerendered page too,
 * which ships no JavaScript.
 */
function Disclosure({
  summary,
  children,
}: {
  summary: string;
  children: ReactNode;
}) {
  return (
    <details className="group mt-3">
      <summary className="missal-focus inline-flex cursor-pointer list-none items-baseline gap-2 font-serif text-[0.9375rem] text-rubric hover:text-rubric-deep [&::-webkit-details-marker]:hidden">
        <span
          aria-hidden="true"
          className="inline-block text-[0.7rem] transition-transform group-open:rotate-90"
        >
          ▶
        </span>
        {summary}
      </summary>
      <div className="mt-2.5 pl-4">{children}</div>
    </details>
  );
}

/**
 * A type's weekly rows; for Adoration, a chapel open 24 hours first, as in the
 * map popup.
 */
function typeRows(
  events: EventSummary[],
  type: EventType,
  continuous: ContinuousAdoration | null,
): ScheduleRollupRow[] {
  const rows = weeklyScheduleRows(eventsOfType(events, type));
  return type === "adoration" && continuous
    ? [continuousRow(continuous, { compact: true }), ...rows]
    : rows;
}

/** An Adoration chapel at its own address has no Mass: its card leads with Adoration. */
function isChapel(church: ChurchBase): boolean {
  return church.kind === "adoration_chapel";
}

function MainSchedule({ entry }: { entry: CityChurchEntry }) {
  if (isChapel(entry.church)) {
    const rows = typeRows(entry.schedule, "adoration", entry.continuous);
    if (rows.length === 0) {
      return (
        <p className="font-serif text-[0.95rem] italic text-ink-faint">
          No weekly Adoration times listed.
        </p>
      );
    }
    return <ScheduleRows rows={rows} />;
  }
  return <MassSchedule events={entry.schedule} />;
}

function MassSchedule({ events }: { events: EventSummary[] }) {
  const rows = weeklyScheduleRows(eventsOfType(events, "mass"));
  if (rows.length === 0) {
    return (
      <p className="font-serif text-[0.95rem] italic text-ink-faint">
        No weekly Mass times listed.
      </p>
    );
  }
  return <ScheduleRows rows={rows} />;
}

function SecondarySchedules({ entry }: { entry: CityChurchEntry }) {
  // A chapel's card already shows its Adoration.
  const types = isChapel(entry.church)
    ? SECONDARY_TYPES.filter((type) => type !== "adoration")
    : SECONDARY_TYPES;
  const sections = types.map((type) => ({
    type,
    rows: typeRows(entry.schedule, type, entry.continuous),
  })).filter((s) => s.rows.length > 0);
  if (sections.length === 0) return null;
  const summary = sections
    .map((s) => EVENT_TYPE_LABELS[s.type])
    .join(" & ");
  return (
    <Disclosure summary={`${summary} times`}>
      <div className="space-y-4">
        {sections.map((s) => (
          <div key={s.type}>
            <h4 className="mb-1.5 font-display text-[1.05rem] text-ink">
              {EVENT_TYPE_LABELS[s.type]}
            </h4>
            <ScheduleRows rows={s.rows} />
          </div>
        ))}
      </div>
    </Disclosure>
  );
}

function FullScheduleLink({ slug }: { slug: string }) {
  return (
    <Link
      to={churchPath(slug)}
      className="rubric-link mt-3 font-serif text-[0.9375rem]"
    >
      Full schedule
      <span aria-hidden="true">→</span>
    </Link>
  );
}

/** One of the city's own churches: its Mass times shown, the rest a click away. */
function CityChurch({ entry }: { entry: CityChurchEntry }) {
  const { church } = entry;
  const address = formatAddress(church);
  return (
    <li className="py-7">
      <h3 className="font-display text-[1.5rem] leading-tight text-ink">
        <Link to={churchPath(church.slug)} className="hover:text-rubric-deep">
          {church.name ?? UNNAMED_CHURCH}
        </Link>
      </h3>
      {address ? (
        <p className="mt-1.5 flex items-baseline gap-2 font-serif text-[0.95rem] text-ink-soft">
          <MapPinIcon className="size-3.5 shrink-0 translate-y-[2px] text-brass" />
          {address}
        </p>
      ) : null}
      <div className="mt-4">
        <MainSchedule entry={entry} />
      </div>
      <SecondarySchedules entry={entry} />
      <div>
        <FullScheduleLink slug={church.slug} />
      </div>
    </li>
  );
}

/** A church outside the city: where and how far, with its Mass times folded away. */
function NearbyChurch({ entry }: { entry: CityChurchEntry }) {
  const { church, citySlug, distanceMiles } = entry;
  const place = [church.city?.trim(), church.state?.trim()]
    .filter(Boolean)
    .join(", ");
  return (
    <li className="py-6">
      <h3 className="font-display text-[1.3rem] leading-tight text-ink">
        <Link to={churchPath(church.slug)} className="hover:text-rubric-deep">
          {church.name ?? UNNAMED_CHURCH}
        </Link>
      </h3>
      <p className="mt-1 font-serif text-[0.95rem] text-ink-soft">
        {place && citySlug ? (
          <Link to={cityPath(citySlug)} className="rubric-link">
            {place}
          </Link>
        ) : (
          place
        )}
        {distanceMiles != null ? (
          <>
            {place ? <span className="mx-2 text-ink-faint">·</span> : null}
            <span className="tabular-nums">{formatMiles(distanceMiles)}</span>
          </>
        ) : null}
      </p>
      <Disclosure summary={isChapel(church) ? "Adoration times" : "Mass times"}>
        <MainSchedule entry={entry} />
        <FullScheduleLink slug={church.slug} />
      </Disclosure>
    </li>
  );
}

/**
 * A city page. `liveMap` makes its map preview live (see CityMapPreview); the
 * prerendered page leaves it out and src/islands/cityMap.ts does the same.
 */
export function CityPageContent({
  data,
  liveMap,
}: {
  data: CityPageData;
  liveMap?: (config: CityMapConfig) => ReactNode;
}) {
  const { city, churches, nearby } = data;

  return (
    <>
      <main className="min-h-svh bg-paper">
        <SiteHeader />

        <div className="mx-auto w-full max-w-5xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
          <section className="rise-in mx-auto max-w-2xl text-center">
            <Breadcrumbs
              className="mb-6"
              crumbs={[
                { label: CHURCH_LIST, to: CHURCH_INDEX_PATH },
                { label: city.label },
              ]}
            />
            <h1 className="font-display text-[clamp(2.25rem,6vw,3.75rem)] leading-[1.05] font-normal tracking-tight text-ink">
              Mass Times in {city.label}
            </h1>
            <p className="mt-4 font-serif text-[1rem] text-ink-soft">
              Times {SOURCE_PHRASE}.
            </p>
          </section>

          <div
            className="rise-in mx-auto max-w-3xl"
            style={{ animationDelay: "80ms" }}
          >
            {/* Keyed by city: when the app goes from one city's page
             *  straight to another's (back to one it has cached, say), the
             *  live map starts again on the new city's view. */}
            <CityMapPreview
              key={city.slug}
              label={city.label}
              map={data.map}
              live={liveMap}
              className="mt-8 mb-3"
            />

            <section aria-label={`Churches in ${city.name}`} className="mt-2">
              <ul className="divide-y divide-rule">
                {churches.map((entry) => (
                  <CityChurch key={entry.church.id} entry={entry} />
                ))}
              </ul>
            </section>

            {nearby.length > 0 ? (
              <section aria-labelledby="nearby-churches" className="mt-12">
                <h2
                  id="nearby-churches"
                  className="font-display text-[1.75rem] leading-none font-normal text-ink"
                >
                  Nearby churches
                </h2>
                <ul className="mt-2 divide-y divide-rule">
                  {nearby.map((entry) => (
                    <NearbyChurch key={entry.church.id} entry={entry} />
                  ))}
                </ul>
              </section>
            ) : null}
          </div>

          <div className="mx-auto mt-16 max-w-2xl">
            <Fleuron solo className="text-brass" />
            <p className="mt-4 text-center font-serif text-[0.9rem] text-ink-faint">
              {DISCLAIMER}
            </p>
          </div>
        </div>
      </main>
      <footer className="bg-paper pb-[calc(3rem+var(--safe-area-inset-bottom))] text-center">
        <Link to={CHURCH_INDEX_PATH} className="rubric-link font-serif text-[0.9375rem]">
          {CHURCH_LIST}
        </Link>
      </footer>
    </>
  );
}
