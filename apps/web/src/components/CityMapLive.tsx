import {
  lazy,
  Suspense,
  useCallback,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
  useSyncExternalStore,
} from "react";
import { createPortal } from "react-dom";
import {
  closeCityMapInPlace,
  isCityMapOpen,
  openCityMap,
  type CityMapConfig,
} from "@/lib/cityMap";

const CityMapView = lazy(() => import("./CityMapView"));

function subscribeToHash(onChange: () => void): () => void {
  window.addEventListener("hashchange", onChange);
  window.addEventListener("popstate", onChange);
  return () => {
    window.removeEventListener("hashchange", onChange);
    window.removeEventListener("popstate", onChange);
  };
}

/** Whether the URL has the map open, kept in step with back and forward. */
function useCityMapOpen(): boolean {
  return useSyncExternalStore(subscribeToHash, isCityMapOpen, () => false);
}

const INLINE_HOST_CLASS = "city-map-host absolute inset-0 isolate";
// Over the page (its sticky header is z-40), and under what the open map opens
// in portals of its own: the search's suggestions (z-[950]) and the phone's
// filter sheet (z-[1200]).
const OPEN_HOST_CLASS = "city-map-host fixed inset-0 isolate z-[900] bg-paper";

/**
 * The city page's live map (and the church page's), mounted over its still
 * preview (CityMapPreview).
 * It's live in the page, and opens to fill the window until it's closed with
 * its button, Escape, or the browser's back button; see src/lib/cityMap.ts.
 * What it shows, in the page and open, is CityMapView's.
 *
 * The map is one Leaflet map throughout, in an element of its own that moves
 * between the preview and the end of <body>, so opening it keeps its view and
 * popups, and no ancestor's transform (the page's rise-in animation) can pin
 * the open map inside the page.
 */
export default function CityMapLive({ config }: { config: CityMapConfig }) {
  const open = useCityMapOpen();
  const [host] = useState(() => document.createElement("div"));
  const inlineSlotRef = useRef<HTMLDivElement>(null);
  // Whether this page added the history entry the open map sits on, so
  // closing goes back past it rather than leaving it for the back button.
  const pushedRef = useRef(false);
  const [ready, setReady] = useState(false);
  const handleReady = useCallback(() => setReady(true), []);
  // Whether the map has moved off the view the still preview draws.
  const [moved, setMoved] = useState(false);
  const handleMove = useCallback(() => setMoved(true), []);

  const expand = useCallback(() => {
    pushedRef.current = true;
    openCityMap();
  }, []);

  const collapse = useCallback(() => {
    if (pushedRef.current) {
      window.history.back();
      return;
    }
    // Opened by a link or a reload: drop the hash in place.
    closeCityMapInPlace();
  }, []);

  useEffect(() => {
    if (!open) pushedRef.current = false;
  }, [open]);

  // Put the map where it's shown: over the whole window, or in the preview.
  useLayoutEffect(() => {
    if (open) {
      host.className = OPEN_HOST_CLASS;
      host.setAttribute("role", "dialog");
      host.setAttribute("aria-modal", "true");
      host.setAttribute("aria-label", `Map of churches around ${config.label}`);
      document.body.appendChild(host);
      return;
    }
    host.className = INLINE_HOST_CLASS;
    host.removeAttribute("role");
    host.removeAttribute("aria-modal");
    host.removeAttribute("aria-label");
    inlineSlotRef.current?.appendChild(host);
  }, [open, host, config.label]);
  useEffect(() => () => host.remove(), [host]);

  // While open: the page behind doesn't scroll and is inert, so Tab stays in
  // the map and screen readers don't wander out of it (what the map opens in
  // portals of its own, appended later, isn't touched); and Escape closes,
  // unless something on the map (a popup, the phone's filter sheet) took it
  // first.
  useEffect(() => {
    if (!open) return;
    const root = document.documentElement;
    const overflow = root.style.overflow;
    root.style.overflow = "hidden";
    const madeInert = [...document.body.children].filter(
      (el): el is HTMLElement =>
        el instanceof HTMLElement && el !== host && !el.inert,
    );
    for (const el of madeInert) el.inert = true;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape" && !event.defaultPrevented) collapse();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => {
      root.style.overflow = overflow;
      for (const el of madeInert) el.inert = false;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [open, collapse, host]);

  return (
    <>
      <div
        ref={inlineSlotRef}
        className="city-map-live absolute inset-0"
        data-ready={ready || undefined}
        data-moved={moved || undefined}
      />
      {createPortal(
        <Suspense fallback={null}>
          <CityMapView
            view={config.view}
            churchId={config.churchId}
            open={open}
            onOpen={expand}
            onClose={collapse}
            onReady={handleReady}
            onMove={handleMove}
          />
        </Suspense>,
        host,
      )}
    </>
  );
}
