import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchChurches } from "../api";
import { ArrowRightIcon } from "@/components/icons";
import { SiteLink } from "./SiteLink";
import {
  DEFAULT_FILTER_STATE,
  encodeFiltersToParams,
} from "./filterState";
import { EVENT_TYPE_OPTIONS } from "../constants/eventTypes";
import type { ApproxLocationState } from "../hooks/useApproxLocation";
import { encodeMapViewToParams } from "../lib/mapView";
import { formatDistance, formatWhen, nextEvent } from "../lib/nextService";
import {
  MAP_PATH,
  churchPath,
  dioceseChurchCounts,
  dioceses,
  diocesePath,
  nearestChurches,
} from "../lib/places";
import { cn } from "@/lib/utils";
import type { ChurchMapItem, EventType } from "../types";

const PREVIEW_COUNT = 5;
/** Zoom for "see all on the map": neighbourhood level, like the map's default. */
const MAP_ZOOM = 11;

const SERVICE_NOUN: Record<EventType, string> = {
  mass: "Mass",
  confession: "Confession",
  adoration: "Adoration",
};

interface NearbyPreviewProps {
  approx: ApproxLocationState;
}

/**
 * The landing page's "Nearby" block: the closest churches to the visitor's
 * approximate location, each with its next Mass (or Confession, or Adoration),
 * or, for a visitor outside the covered dioceses, a note saying what is covered.
 *
 * Client-only. The visitor isn't known to the prerenderer, so nothing is
 * rendered until the component has mounted; the static HTML has no trace of it.
 */
export function NearbyPreview({ approx }: NearbyPreviewProps) {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) return null;

  const { status, location, inCoverage } = approx;
  if (status === "ready" && !location) return null;
  if (status === "ready" && !inCoverage) return <OutOfCoverage />;

  return (
    <section
      id="nearby"
      aria-labelledby="nearby-heading"
      className="mx-auto w-full max-w-[720px] scroll-mt-6 px-7 pt-2 pb-6 md:px-0 md:pb-10"
    >
      {status === "ready" && location ? (
        <NearbyList location={location} />
      ) : (
        <NearbySkeleton />
      )}
    </section>
  );
}

// ---------------------------------------------------------------- list

interface NearbyListProps {
  location: NonNullable<ApproxLocationState["location"]>;
}

function NearbyList({ location }: NearbyListProps) {
  const [service, setService] = useState<EventType>("mass");
  // Fixed for the life of the component: "next" is relative to when the page
  // was opened, which keeps the rows stable while the visitor reads them.
  const [now] = useState(() => new Date());

  const { data, isPending, isError, refetch } = useQuery({
    queryKey: ["nearby-churches", service],
    queryFn: () => fetchChurches({ types: [service] }),
    staleTime: Infinity,
  });

  const rows = useMemo(() => {
    if (!data) return [];
    const withNext = data
      .map((church) => ({
        church,
        next: nextEvent(church.upcoming_events, now),
      }))
      .filter(
        (row): row is { church: ChurchMapItem; next: NonNullable<typeof row.next> } =>
          row.next !== null,
      );
    const byId = new Map(withNext.map((row) => [row.church.id, row]));
    return nearestChurches(
      withNext.map((row) => row.church),
      location,
      PREVIEW_COUNT,
    ).map(({ church, distanceMiles }) => ({
      ...byId.get(church.id)!,
      distanceMiles,
    }));
  }, [data, location, now]);

  const mapSearch = useMemo(() => {
    const filters = encodeFiltersToParams(
      { ...DEFAULT_FILTER_STATE, eventType: service },
      new URLSearchParams(),
    );
    return `?${encodeMapViewToParams(
      { lat: location.lat, lng: location.lng, zoom: MAP_ZOOM },
      filters,
    )}`;
  }, [location.lat, location.lng, service]);

  return (
    <>
      <div className="flex flex-col gap-3 border-b border-rule-strong pb-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2
            id="nearby-heading"
            className="smallcaps m-0 text-[0.9375rem] text-ink-soft"
          >
            Nearby
          </h2>
          <p className="m-0 mt-1 font-display text-[1.375rem] leading-tight text-ink">
            Next {SERVICE_NOUN[service]} near {location.label}
          </p>
        </div>
        <ServiceSwitch value={service} onChange={setService} />
      </div>

      {isPending ? (
        <NearbyRowsSkeleton />
      ) : isError ? (
        <p className="py-6 font-serif text-[15px] text-ink-soft">
          Couldn&rsquo;t load nearby churches.{" "}
          <button
            type="button"
            onClick={() => void refetch()}
            className="rubric-link missal-focus"
          >
            Try again
          </button>
        </p>
      ) : rows.length === 0 ? (
        <p className="py-6 font-serif text-[15px] italic text-ink-soft">
          No upcoming {SERVICE_NOUN[service]} times found near here.
        </p>
      ) : (
        <ol className="m-0 list-none p-0">
          {rows.map(({ church, next, distanceMiles }) => (
            <li key={church.id} className="border-b border-rule">
              <SiteLink
                spa
                href={churchPath(church.slug)}
                className="missal-focus group grid grid-cols-[1fr_auto] items-baseline gap-x-4 gap-y-0.5 py-3 transition-colors hover:bg-paper-deep/40 md:px-2"
              >
                <span className="line-clamp-2 min-w-0 font-display text-[1.125rem] leading-tight text-ink group-hover:text-rubric">
                  {church.name ?? "Unnamed parish"}
                </span>
                <span className="text-right font-serif text-[0.9375rem] text-rubric">
                  {formatWhen(next.when, now)}
                </span>
                <span className="min-w-0 truncate font-serif text-[0.875rem] text-ink-soft">
                  {[church.city, formatDistance(distanceMiles)]
                    .filter(Boolean)
                    .join(" · ")}
                </span>
              </SiteLink>
            </li>
          ))}
        </ol>
      )}

      <p className="mt-5 mb-0">
        <SiteLink
          spa
          href={`${MAP_PATH}${mapSearch}`}
          className="rubric-link missal-focus font-serif text-[0.9375rem]"
        >
          See all on the map
          <ArrowRightIcon className="size-[14px] self-center" />
        </SiteLink>
      </p>
    </>
  );
}

function ServiceSwitch({
  value,
  onChange,
}: {
  value: EventType;
  onChange: (next: EventType) => void;
}) {
  return (
    <div
      role="group"
      aria-label="Service"
      className="flex divide-x divide-rule overflow-hidden self-start rounded-sm border border-rule-strong"
    >
      {EVENT_TYPE_OPTIONS.map((option) => {
        const active = value === option.id;
        return (
          <button
            key={option.id}
            type="button"
            aria-pressed={active}
            onClick={() => onChange(option.id)}
            className={cn(
              "missal-focus px-3 py-1.5 font-display text-[0.9375rem] leading-none transition-colors",
              active
                ? "bg-paper-deep/80 text-rubric"
                : "text-ink hover:bg-paper-deep/40",
            )}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}

// ------------------------------------------------------------ skeletons

function NearbySkeleton() {
  return (
    <>
      <div className="border-b border-rule-strong pb-3">
        <h2
          id="nearby-heading"
          className="smallcaps m-0 text-[0.9375rem] text-ink-soft"
        >
          Nearby
        </h2>
        <div className="mt-2 h-6 w-2/3 animate-pulse bg-paper-deep" />
      </div>
      <NearbyRowsSkeleton />
    </>
  );
}

function NearbyRowsSkeleton() {
  return (
    <div role="status" aria-busy="true" aria-label="Loading nearby churches">
      {Array.from({ length: PREVIEW_COUNT }, (_, i) => (
        <div
          key={i}
          className="grid grid-cols-[1fr_auto] gap-x-4 gap-y-2 border-b border-rule py-3 md:px-2"
        >
          <div className="h-[1.125rem] w-3/4 animate-pulse bg-paper-deep" />
          <div className="h-[1.125rem] w-24 animate-pulse bg-paper-deep" />
          <div className="h-3.5 w-1/3 animate-pulse bg-paper-deep" />
        </div>
      ))}
    </div>
  );
}

// ------------------------------------------------------ out of coverage

/** "Albany", "New York": a diocese's short name without its "Diocese of". */
function placeName(shortName: string): string {
  return shortName.replace(/^(Arch)?diocese of /i, "");
}

function OutOfCoverage() {
  const counts = dioceseChurchCounts();
  const covered = dioceses()
    .filter((d) => (counts[d.key] ?? 0) > 0)
    .sort((a, b) => placeName(a.shortName).localeCompare(placeName(b.shortName)));
  return (
    <section
      id="nearby"
      aria-label="Coverage"
      className="mx-auto w-full max-w-[720px] px-7 pt-2 pb-6 md:px-0 md:pb-10"
    >
      <div className="rise-in border-y border-rule-strong py-5">
        <p className="m-0 font-serif text-[1rem] leading-relaxed text-ink-soft">
          Project Carlo covers Catholic parishes in the dioceses of{" "}
          {covered.map((d, i) => (
            <span key={d.key}>
              {i > 0 ? (i === covered.length - 1 ? " and " : ", ") : null}
              <SiteLink href={diocesePath(d.key)} className="rubric-link">
                {placeName(d.shortName)}
              </SiteLink>
            </span>
          ))}{" "}
          (and growing). Search for a New York city or ZIP above to see times
          there.
        </p>
      </div>
    </section>
  );
}
