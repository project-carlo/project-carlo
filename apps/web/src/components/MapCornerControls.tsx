import { useEffect, useState } from "react";
import type { Map as LeafletMap } from "leaflet";
import { cn } from "@/lib/utils";
import { LocateButton } from "./LocateButton";
import type { BrowserLocationStatus } from "../hooks/useBrowserLocation";

const BUTTON_CLASS =
  "missal-focus flex size-11 items-center justify-center font-display text-[1.6rem] leading-none text-ink-soft transition-colors hover:text-rubric disabled:cursor-default disabled:text-ink-faint";

/**
 * An inert copy of the zoom buttons, drawn by a still map (the city page's
 * preview) on the pixels the live ones will take.
 */
function ZoomButtonsPlaceholder() {
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none flex flex-col border border-rule-strong bg-paper/96 shadow-missal-floating backdrop-blur-sm"
    >
      <span className={BUTTON_CLASS}>+</span>
      <span className={cn(BUTTON_CLASS, "border-t border-rule-strong")}>−</span>
    </div>
  );
}

/** Zoom in and out, one card of two buttons, each off at its end of the range. */
function ZoomButtons({ map }: { map: LeafletMap }) {
  const [zoom, setZoom] = useState(() => map.getZoom());
  useEffect(() => {
    const update = () => setZoom(map.getZoom());
    update();
    map.on("zoomend", update);
    return () => {
      map.off("zoomend", update);
    };
  }, [map]);
  return (
    <div className="flex flex-col border border-rule-strong bg-paper/96 shadow-missal-floating backdrop-blur-sm">
      <button
        type="button"
        onClick={() => map.zoomIn()}
        disabled={zoom >= map.getMaxZoom()}
        aria-label="Zoom in"
        title="Zoom in"
        className={BUTTON_CLASS}
      >
        <span aria-hidden="true">+</span>
      </button>
      <button
        type="button"
        onClick={() => map.zoomOut()}
        disabled={zoom <= map.getMinZoom()}
        aria-label="Zoom out"
        title="Zoom out"
        className={cn(BUTTON_CLASS, "border-t border-rule-strong")}
      >
        <span aria-hidden="true">−</span>
      </button>
    </div>
  );
}

export interface LocateControl {
  status: BrowserLocationStatus;
  error: string | null;
  onLocate: () => void;
}

/**
 * The controls in a map's bottom-right corner, above its attribution: zoom
 * buttons over the locate button, either left out. Until the map exists the
 * zoom buttons are an inert copy, so they don't shift anything when it
 * arrives. `className` places the corner.
 */
export function MapCornerControls({
  map,
  zoom = false,
  locate,
  className,
}: {
  map: LeafletMap | null;
  zoom?: boolean;
  locate?: LocateControl;
  className?: string;
}) {
  if (!zoom && !locate) return null;
  return (
    <div className={cn("pointer-events-none absolute z-[900]", className)}>
      <div className="pointer-events-auto ml-auto flex w-fit flex-col items-end gap-2">
        {zoom ? map ? <ZoomButtons map={map} /> : <ZoomButtonsPlaceholder /> : null}
        {locate ? (
          <LocateButton
            status={locate.status}
            error={locate.error}
            onLocate={locate.onLocate}
          />
        ) : null}
      </div>
    </div>
  );
}
