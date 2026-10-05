import { useCallback, useState } from "react";
import { CrosshairIcon, XIcon } from "@/components/icons";
import type { ApproxLocation } from "../lib/approxLocation";
import type { PlaceSearchResult } from "../placeSearch";

interface ApproxLocationNoticeProps {
  location: ApproxLocation;
  /** Called with the device's position; the map re-centers and remembers it
   *  exactly as for a searched place. */
  onPlaceSelect: (place: PlaceSearchResult) => void;
  onDismiss: () => void;
}

/** What the notice says about where the map opened. */
function describe(location: ApproxLocation): {
  where: string;
  qualifier: string | null;
} {
  switch (location.source) {
    case "ip":
      return { where: location.label, qualifier: "approximate" };
    case "search":
      return { where: location.label, qualifier: "your last search" };
    case "device":
      return { where: "your current location", qualifier: null };
  }
}

/**
 * A small dismissible line in the map's floating card, explaining why the map
 * opened where it did, with a one-tap path to a precise location.
 */
export function ApproxLocationNotice({
  location,
  onPlaceSelect,
  onDismiss,
}: ApproxLocationNoticeProps) {
  const [status, setStatus] = useState<"idle" | "requesting" | "error">("idle");
  const [error, setError] = useState<string | null>(null);
  const { where, qualifier } = describe(location);

  const usePrecise = useCallback(() => {
    if (!navigator.geolocation) {
      setStatus("error");
      setError("Location is not available in this browser.");
      return;
    }
    setStatus("requesting");
    setError(null);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setStatus("idle");
        onPlaceSelect({
          id: `current-location-${position.coords.latitude}-${position.coords.longitude}`,
          title: "Your current location",
          subtitle: "From your browser",
          lat: position.coords.latitude,
          lng: position.coords.longitude,
          resultType: "unknown",
        });
        onDismiss();
      },
      (failure) => {
        setStatus("error");
        setError(
          failure.code === failure.PERMISSION_DENIED
            ? "Location permission was denied."
            : "Couldn't get your current location.",
        );
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 },
    );
  }, [onDismiss, onPlaceSelect]);

  return (
    <div
      role="status"
      className="mt-3 flex items-start justify-between gap-3 border-t border-rule pt-3 font-serif text-[0.9375rem] leading-snug"
    >
      <p className="m-0 min-w-0 text-ink-soft">
        Showing the area near <span className="text-ink">{where}</span>
        {qualifier ? <span className="italic"> ({qualifier})</span> : null}
        {location.source !== "device" ? (
          <>
            {" · "}
            <button
              type="button"
              onClick={usePrecise}
              disabled={status === "requesting"}
              className="rubric-link missal-focus inline-flex items-center gap-1.5 disabled:opacity-60"
            >
              <CrosshairIcon className="size-3.5 shrink-0 self-center" />
              <span>
                {status === "requesting" ? "Locating…" : "Use precise location"}
              </span>
            </button>
          </>
        ) : null}
        {error ? (
          <span className="mt-1 block text-[0.8125rem] italic text-ink-faint">
            {error}
          </span>
        ) : null}
      </p>
      <button
        type="button"
        onClick={onDismiss}
        aria-label="Dismiss location notice"
        className="missal-focus -mr-1 mt-0.5 flex size-5 shrink-0 items-center justify-center text-ink-soft transition-colors hover:text-rubric"
      >
        <XIcon className="size-3.5" />
      </button>
    </div>
  );
}
