import { memo, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import type { ChurchMapItem } from "../types";
import { churchPath, dioceseForChurch } from "../lib/places";
import {
  LIST_PAGE_SIZE,
  countSummary,
  describeFilters,
  formatDistance,
  formatNextTimes,
  thenText,
  type ListRow,
  type ListSort,
} from "../lib/churchList";
import { DEFAULT_FILTER_STATE, type FilterState } from "./filterState";

const SORT_OPTIONS: { id: ListSort; label: string }[] = [
  { id: "nearest", label: "Nearest" },
  { id: "soonest", label: "Soonest" },
];

// ---------------------------------------------------------------- one row

interface ChurchListRowProps {
  row: ListRow;
  now: Date;
  /** "Mass", "Confession", … — names what "Next" refers to. */
  typeLabel: string;
  highlighted: boolean;
  onHover: (churchId: number | null) => void;
  onShowOnMap: (church: ChurchMapItem) => void;
}

const ChurchListRow = memo(function ChurchListRow({
  row,
  now,
  typeLabel,
  highlighted,
  onHover,
  onShowOnMap,
}: ChurchListRowProps) {
  const { church } = row;
  const times = formatNextTimes(row, now);
  const diocese = dioceseForChurch(church.slug);
  const name = church.name ?? "Unnamed parish";

  return (
    <li
      data-highlighted={highlighted || undefined}
      onPointerEnter={(event) => {
        if (event.pointerType === "mouse") onHover(church.id);
      }}
      onPointerLeave={(event) => {
        if (event.pointerType === "mouse") onHover(null);
      }}
      onFocus={(event) => {
        // Keyboard focus only: a tap focuses the button it lands on, and the
        // highlight would stick when the list unmounts without a blur.
        if (event.target.matches(":focus-visible")) onHover(church.id);
      }}
      onBlur={() => onHover(null)}
      className={`relative border-b border-rule px-5 py-4 transition-colors last:border-b-0 ${
        highlighted ? "bg-paper-deep/60" : ""
      }`}
    >
      <span
        aria-hidden
        className={`absolute inset-y-0 left-0 w-[3px] bg-rubric transition-opacity ${
          highlighted ? "opacity-100" : "opacity-0"
        }`}
      />
      <div className="flex items-baseline justify-between gap-3">
        <h3 className="min-w-0 font-display text-[1.2rem] leading-[1.15] font-normal text-ink">
          <Link
            to={churchPath(church.slug)}
            className="rubric-link missal-focus !text-ink hover:!text-rubric"
          >
            {name}
          </Link>
        </h3>
        {row.distanceMiles != null ? (
          <span className="smallcaps shrink-0 whitespace-nowrap text-[0.9375rem] tabular-nums text-ink-soft">
            <span className="sr-only">Distance: </span>
            {formatDistance(row.distanceMiles)}
          </span>
        ) : null}
      </div>

      <p className="mt-0.5 font-serif text-[0.875rem] leading-snug text-ink-faint">
        {church.city ?? "Unknown town"}
        {diocese ? (
          <>
            <span aria-hidden className="mx-1.5 text-brass">
              ·
            </span>
            <span className="italic">{diocese.shortName}</span>
          </>
        ) : null}
      </p>

      {times.next ? (
        <div className="mt-2.5 space-y-0.5">
          <p className="flex flex-wrap items-baseline gap-x-2 gap-y-1 font-serif text-[1rem] leading-snug">
            <span className="smallcaps text-[0.8125rem] text-ink-faint">
              Next {typeLabel}
            </span>
            <span className="font-medium tabular-nums text-rubric">
              {times.next.day} {times.next.time}
            </span>
            {times.next.soon ? (
              <span
                title={`Starts in ${times.next.minutesUntil} min`}
                className="smallcaps border border-rubric px-1.5 text-[0.75rem] leading-[1.35] text-rubric"
              >
                Soon
              </span>
            ) : null}
          </p>
          {times.then.length > 0 ? (
            <p className="font-serif text-[0.9rem] leading-snug tabular-nums text-ink-soft">
              {thenText(times.then)}
              {times.moreDays > 0 ? (
                <span className="text-ink-faint">
                  {" "}
                  · +{times.moreDays} more {times.moreDays === 1 ? "day" : "days"}
                </span>
              ) : null}
            </p>
          ) : null}
        </div>
      ) : (
        <p className="mt-2.5 font-serif text-[0.9rem] italic text-ink-faint">
          No upcoming times listed.
        </p>
      )}

      <div className="mt-2.5 flex items-center justify-between gap-3">
        <button
          type="button"
          onClick={() => onShowOnMap(church)}
          aria-label={`Show ${name} on map`}
          className="rubric-link missal-focus font-serif text-[0.9375rem]"
        >
          Show on map
        </button>
        <Link
          to={churchPath(church.slug)}
          tabIndex={-1}
          aria-hidden
          className="font-serif text-[0.9375rem] text-ink-faint hover:text-rubric"
        >
          Full schedule →
        </Link>
      </div>
    </li>
  );
});

// ------------------------------------------------------------- empty state

interface EmptyStateProps {
  filters: FilterState;
  /** Matching churches anywhere on the map; 0 means the filters match nothing. */
  totalCount: number | undefined;
  nearest: ListRow | null;
  onZoomOut: () => void;
  onClearTime: () => void;
  onClearDays: () => void;
  onShowOnMap: (church: ChurchMapItem) => void;
}

function EmptyState({
  filters,
  totalCount,
  nearest,
  onZoomOut,
  onClearTime,
  onClearDays,
  onShowOnMap,
}: EmptyStateProps) {
  const phrases = describeFilters(filters);
  const buttonClass =
    "missal-focus border border-rule-strong bg-transparent px-3 py-2 font-serif text-[0.9375rem] text-ink-soft transition-colors hover:border-rubric hover:text-rubric";
  return (
    <div className="px-5 py-8 text-center">
      <p className="font-display text-[1.2rem] leading-snug text-ink">
        No churches with{" "}
        <em className="not-italic text-rubric">{phrases.type}</em>
        {phrases.days ? (
          <>
            {" "}
            <em className="not-italic text-rubric">{phrases.days}</em>
          </>
        ) : null}
        {phrases.time ? (
          <>
            {" "}
            <em className="not-italic text-rubric">{phrases.time}</em>
          </>
        ) : null}{" "}
        in this area
      </p>
      <div className="mt-5 flex flex-wrap justify-center gap-2">
        {totalCount !== 0 ? (
          <button type="button" onClick={onZoomOut} className={buttonClass}>
            Zoom out
          </button>
        ) : null}
        {phrases.time ? (
          <button type="button" onClick={onClearTime} className={buttonClass}>
            Clear time filter
          </button>
        ) : null}
        {phrases.days ? (
          <button type="button" onClick={onClearDays} className={buttonClass}>
            Clear day filter
          </button>
        ) : null}
      </div>
      {nearest ? (
        <p className="mt-5 font-serif text-[0.9375rem] leading-snug text-ink-soft">
          The nearest match is{" "}
          <span className="text-ink">
            {nearest.church.name ?? "an unnamed parish"}
          </span>
          {nearest.distanceMiles != null
            ? `, ${formatDistance(nearest.distanceMiles)} away`
            : ""}
          .{" "}
          <button
            type="button"
            onClick={() => onShowOnMap(nearest.church)}
            className="rubric-link missal-focus"
          >
            Show on map
          </button>
        </p>
      ) : null}
    </div>
  );
}

// -------------------------------------------------------------- the list

export interface ChurchListProps {
  /** Sorted rows for the area. */
  rows: ListRow[];
  /** `undefined` until the data and map are ready. */
  loading: boolean;
  /** Churches matching the filters anywhere ("in all"). */
  totalCount: number | undefined;
  filters: FilterState;
  sort: ListSort;
  onSortChange: (sort: ListSort) => void;
  now: Date;
  /** What distances are measured from, e.g. "the map centre" or a pin's name. */
  distanceFrom: string;
  highlightedId: number | null;
  onHover: (churchId: number | null) => void;
  onShowOnMap: (church: ChurchMapItem) => void;
  onZoomOut: () => void;
  onClearTime: () => void;
  onClearDays: () => void;
  /** Closest match outside the area, for the empty state. */
  nearestOutside: ListRow | null;
  /** Desktop extras shown under the count: the search-as-I-move controls. */
  extras?: ReactNode;
  /** Desktop: a line summarising the active filters, with a way to change them. */
  onEditFilters?: () => void;
  /** Extra space under the last row, so a floating control never covers it. */
  bottomInset?: boolean;
}

/**
 * The results list: a count, a sort switch and one row per church. Fills the
 * height it is given — the header stays put and the rows scroll under it.
 */
export function ChurchList({
  rows,
  loading,
  totalCount,
  filters,
  sort,
  onSortChange,
  now,
  distanceFrom,
  highlightedId,
  onHover,
  onShowOnMap,
  onZoomOut,
  onClearTime,
  onClearDays,
  nearestOutside,
  extras,
  onEditFilters,
  bottomInset,
}: ChurchListProps) {
  // The page size resets whenever the list is re-sorted or re-filtered, so a
  // long "Show more" session doesn't carry over to an unrelated result set.
  const resetKey = `${sort}|${filters.eventType}|${filters.daysOfWeek.join(",")}|${filters.timeFrom}-${filters.timeTo}`;
  const [paging, setPaging] = useState({ key: resetKey, limit: LIST_PAGE_SIZE });
  const limit = paging.key === resetKey ? paging.limit : LIST_PAGE_SIZE;

  const shown = rows.slice(0, limit);
  const hidden = rows.length - shown.length;
  const phrases = describeFilters(filters);
  const typeLabel = phrases.type;
  const filtersAreDefault =
    filters.eventType === DEFAULT_FILTER_STATE.eventType &&
    !phrases.days &&
    !phrases.time;

  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <div className="shrink-0 border-b border-rule-strong px-5 pt-4 pb-3">
        <h2 className="sr-only">Churches in this area</h2>
        <p
          role="status"
          aria-live="polite"
          aria-atomic="true"
          className="font-serif text-[1.0625rem] leading-snug text-ink"
        >
          {loading
            ? "Loading churches…"
            : countSummary(rows.length, totalCount)}
        </p>
        <div className="mt-2 flex items-center justify-between gap-3">
          <p className="min-w-0 font-serif text-[0.8125rem] italic leading-snug text-ink-faint">
            Distances from {distanceFrom}
          </p>
          <div
            role="group"
            aria-label="Sort churches"
            className="flex shrink-0 border border-rule-strong"
          >
            {SORT_OPTIONS.map((option, index) => (
              <button
                key={option.id}
                type="button"
                aria-pressed={sort === option.id}
                onClick={() => onSortChange(option.id)}
                className={`missal-focus smallcaps px-2.5 py-1.5 text-[0.8125rem] transition-colors ${
                  index > 0 ? "border-l border-rule" : ""
                } ${
                  sort === option.id
                    ? "bg-rubric text-paper"
                    : "text-ink-soft hover:bg-paper-deep/50 hover:text-ink"
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
        {onEditFilters && !filtersAreDefault ? (
          <p className="mt-2 flex flex-wrap items-baseline gap-x-1.5 font-serif text-[0.9375rem] text-ink-soft">
            <span className="smallcaps text-[0.8125rem] text-ink-faint">
              Showing
            </span>
            <span className="text-rubric">
              {[phrases.type, phrases.days, phrases.time]
                .filter(Boolean)
                .join(" ")}
            </span>
            <button
              type="button"
              onClick={onEditFilters}
              className="rubric-link missal-focus ml-auto"
            >
              Change
            </button>
          </p>
        ) : null}
        {extras}
      </div>

      <div
        className={`min-h-0 flex-1 overflow-y-auto overscroll-contain ${
          bottomInset ? "pb-24" : ""
        }`}
      >
        {!loading && rows.length === 0 ? (
          <EmptyState
            filters={filters}
            totalCount={totalCount}
            nearest={nearestOutside}
            onZoomOut={onZoomOut}
            onClearTime={onClearTime}
            onClearDays={onClearDays}
            onShowOnMap={onShowOnMap}
          />
        ) : (
          <>
            <ol aria-label="Churches in this area" className="m-0 list-none p-0">
              {shown.map((row) => (
                <ChurchListRow
                  key={row.church.id}
                  row={row}
                  now={now}
                  typeLabel={typeLabel}
                  highlighted={row.church.id === highlightedId}
                  onHover={onHover}
                  onShowOnMap={onShowOnMap}
                />
              ))}
            </ol>
            {hidden > 0 ? (
              <div className="border-t border-rule px-5 py-4 text-center">
                <button
                  type="button"
                  onClick={() =>
                    setPaging({ key: resetKey, limit: limit + LIST_PAGE_SIZE })
                  }
                  className="missal-focus border border-rule-strong px-4 py-2 font-display text-[1rem] text-ink-soft transition-colors hover:border-rubric hover:text-rubric"
                >
                  Show more
                  <span className="ml-2 font-serif text-[0.875rem] text-ink-faint">
                    {hidden} more
                  </span>
                </button>
              </div>
            ) : null}
          </>
        )}
      </div>
    </div>
  );
}
