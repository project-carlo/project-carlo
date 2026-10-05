import { MapPinIcon } from "@/components/icons";
import type { ApproxLocation } from "../lib/approxLocation";

interface LocationLineProps {
  /** Null (still working it out, or no guess): the line is held empty. */
  location: ApproxLocation | null;
  /** Called when the visitor wants a different place; the page focuses search. */
  onChange: () => void;
}

/**
 * "Near Rochester, NY · change", under the landing page's search field. The
 * row keeps its height while empty, so the prerendered page (which can't know
 * the visitor) and the client render don't shift the layout around it.
 */
export function LocationLine({ location, onChange }: LocationLineProps) {
  return (
    <div className="flex min-h-[1.5rem] items-center">
      {location ? (
        <p
          key={`${location.lat},${location.lng}`}
          className="rise-in m-0 flex flex-wrap items-baseline gap-x-2 font-serif text-[15px] text-ink-soft"
        >
          <MapPinIcon className="size-4 shrink-0 translate-y-[3px] text-rubric" />
          <span>
            Near{" "}
            <strong className="font-semibold text-ink">{location.label}</strong>
          </span>
          {location.source === "ip" ? (
            <span className="text-[13px] italic text-ink-faint">
              (approximate)
            </span>
          ) : null}
          <span aria-hidden className="text-ink-faint">
            ·
          </span>
          <button
            type="button"
            onClick={onChange}
            className="rubric-link missal-focus"
          >
            change
          </button>
        </p>
      ) : null}
    </div>
  );
}
