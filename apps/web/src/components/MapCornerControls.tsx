import { useEffect, useState } from "react";
import type { Map as LeafletMap } from "leaflet";
import { cn } from "@/lib/utils";
import { LocateButton } from "./LocateButton";
import type { BrowserLocationStatus } from "../hooks/useBrowserLocation";

const BUTTON_CLASS =
  "missal-focus flex size-11 items-center justify-center font-display text-[1.6rem] leading-none text-ink-soft transition-colors hover:text-rubric disabled:cursor-default disabled:text-ink-faint";

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
 * buttons (once the map exists) over the locate button, either left out.
 * `className` places the corner.
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
  const showZoom = zoom && map != null;
  if (!showZoom && !locate) return null;
  return (
    <div className={cn("pointer-events-none absolute z-[900]", className)}>
      <div className="pointer-events-auto ml-auto flex w-fit flex-col items-end gap-2">
        {showZoom ? <ZoomButtons map={map} /> : null}
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
