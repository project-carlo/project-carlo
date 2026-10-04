import type { MobileView } from "../hooks/useListUrlState";

interface MapListToggleProps {
  /** The view currently showing; the button offers the other one. */
  view: MobileView;
  onChange: (view: MobileView) => void;
  /** Churches in the area, shown beside "List". */
  count?: number;
}

function ListGlyph() {
  return (
    <svg
      aria-hidden
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
    >
      <path d="M8 6h13M8 12h13M8 18h13" />
      <circle cx="3.5" cy="6" r="1" fill="currentColor" stroke="none" />
      <circle cx="3.5" cy="12" r="1" fill="currentColor" stroke="none" />
      <circle cx="3.5" cy="18" r="1" fill="currentColor" stroke="none" />
    </svg>
  );
}

function MapGlyph() {
  return (
    <svg
      aria-hidden
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M9 4 3 6.5v13.5L9 17.5l6 2.5 6-2.5V4L15 6.5 9 4Z" />
      <path d="M9 4v13.5M15 6.5V20" />
    </svg>
  );
}

/**
 * The phone's floating "List" / "Map" pill, bottom centre, like the one in
 * map apps. It names where tapping takes you, and while on the map it carries
 * the number of churches the list would show.
 */
export function MapListToggle({ view, onChange, count }: MapListToggleProps) {
  const toList = view === "map";
  return (
    <button
      type="button"
      onClick={() => onChange(toList ? "list" : "map")}
      aria-label={toList ? "Show results as a list" : "Show results on the map"}
      className="missal-focus pointer-events-auto fixed bottom-[calc(1.25rem+var(--safe-area-inset-bottom))] left-1/2 z-[950] flex -translate-x-1/2 items-center gap-2.5 rounded-full border border-brass bg-ink px-5 py-3 font-display text-[1.05rem] leading-none text-paper shadow-missal-floating transition-transform active:scale-95 md:hidden"
    >
      {toList ? <ListGlyph /> : <MapGlyph />}
      <span>{toList ? "List" : "Map"}</span>
      {toList && count != null ? (
        <span className="font-serif text-[0.9375rem] tabular-nums text-paper/70">
          {count}
        </span>
      ) : null}
    </button>
  );
}
