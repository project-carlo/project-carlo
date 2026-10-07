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
import { Link } from "react-router-dom";
import { ExpandIcon, XIcon } from "@/components/icons";
import { useMinWidth } from "@/hooks/useMinWidth";
import {
  INLINE_MAP_MIN_WIDTH,
  isCityMapOpen,
  openCityMap,
  type CityMapConfig,
} from "@/lib/cityMap";
import { useDocumentLinks } from "@/lib/documentLinks";
import { encodeMapViewToParams, type MapView } from "@/lib/mapView";

const CityLeafletMap = lazy(() => import("./CityLeafletMap"));

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

const CHIP_CLASS =
  "inline-flex items-center gap-2 border border-rule-strong bg-paper/95 px-3 py-1.5 font-serif text-[0.9375rem] text-rubric shadow-missal-floating transition-colors hover:text-rubric-deep";

const INLINE_HOST_CLASS = "absolute inset-0 isolate";
const OPEN_HOST_CLASS = "fixed inset-0 isolate z-[1200] bg-paper";

/**
 * The city page's live map, mounted over its still preview (CityMapPreview).
 * On a desktop it's live in the page; on a phone the preview stays still and
 * a tap opens the map. Open, it fills the window until it's closed with its
 * button, Escape, or the browser's back button; see src/lib/cityMap.ts.
 *
 * The map is one Leaflet map throughout, in an element of its own that moves
 * between the preview and the end of <body>, so opening it keeps its view and
 * popups, and no ancestor's transform (the page's rise-in animation) can pin
 * the open map inside the page.
 *
 * `openedOnMount` is for a map mounted by the tap that opened it, which added
 * the history entry closing it should go back past.
 */
export default function CityMapLive({
  config,
  openedOnMount = false,
}: {
  config: CityMapConfig;
  openedOnMount?: boolean;
}) {
  const open = useCityMapOpen();
  const inline = useMinWidth(INLINE_MAP_MIN_WIDTH);
  const documentLinks = useDocumentLinks();
  const [host] = useState(() => document.createElement("div"));
  const inlineSlotRef = useRef<HTMLDivElement>(null);
  const openButtonRef = useRef<HTMLButtonElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  // Whether this page added the history entry the open map sits on, so
  // closing goes back past it rather than leaving it for the back button.
  const pushedRef = useRef(openedOnMount);
  const [ready, setReady] = useState(false);
  const [view, setView] = useState<MapView>(config.view);
  const handleReady = useCallback(() => setReady(true), []);

  const expand = useCallback(() => {
    pushedRef.current = true;
    openCityMap();
  }, []);

  const collapse = useCallback(() => {
    if (pushedRef.current) {
      window.history.back();
      return;
    }
    // Opened by a link or a reload: drop the hash in place. The popstate
    // tells this hook, and the app's router, that the URL changed.
    const { pathname, search } = window.location;
    window.history.replaceState(window.history.state, "", pathname + search);
    window.dispatchEvent(new PopStateEvent("popstate", { state: window.history.state }));
  }, []);

  useEffect(() => {
    if (!open) pushedRef.current = false;
  }, [open]);

  // Put the map where it's shown: over the whole window, in the preview, or
  // (a closed map on a phone) nowhere.
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
    if (inline && inlineSlotRef.current) inlineSlotRef.current.appendChild(host);
    else host.remove();
  }, [open, inline, host, config.label]);
  useEffect(() => () => host.remove(), [host]);

  // While open: the page behind doesn't scroll, and Escape closes.
  useEffect(() => {
    if (!open) return;
    const root = document.documentElement;
    const overflow = root.style.overflow;
    root.style.overflow = "hidden";
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") collapse();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => {
      root.style.overflow = overflow;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [open, collapse]);

  // Focus follows the map: to Close as it opens, back to the opener as it closes.
  const wasOpenRef = useRef(open);
  useEffect(() => {
    if (open) closeButtonRef.current?.focus();
    else if (wasOpenRef.current) openButtonRef.current?.focus();
    wasOpenRef.current = open;
  }, [open]);

  const appHref = `/?${encodeMapViewToParams(view, new URLSearchParams())}`;
  const showMap = open || inline;

  return (
    <>
      {inline ? (
        <div
          ref={inlineSlotRef}
          className="city-map-live absolute inset-0"
          data-ready={ready || undefined}
        />
      ) : (
        <button
          ref={openButtonRef}
          type="button"
          onClick={expand}
          aria-label={`Open the map of churches around ${config.label}`}
          className="city-map-live missal-focus absolute inset-0 cursor-pointer"
        >
          <span aria-hidden="true" className={`${CHIP_CLASS} absolute top-3 right-3`}>
            <ExpandIcon className="size-3.5" />
            Open map
          </span>
        </button>
      )}
      {showMap
        ? createPortal(
            <>
              <Suspense fallback={null}>
                <CityLeafletMap
                  view={config.view}
                  open={open}
                  onReady={handleReady}
                  onViewChange={setView}
                />
              </Suspense>
              {open ? (
                <div className="pointer-events-none absolute inset-x-0 top-0 z-[1150] flex items-start justify-between gap-3 px-4 pt-[calc(1rem+var(--safe-area-inset-top))] md:px-6 md:pt-6">
                  <div className="pointer-events-auto min-w-0 border border-rule-strong bg-paper/96 px-4 py-2.5 shadow-missal-floating backdrop-blur-sm">
                    <p className="truncate font-display text-[1.3rem] leading-tight text-ink">
                      {config.label}
                    </p>
                    <Link
                      to={appHref}
                      reloadDocument={documentLinks}
                      className="rubric-link mt-0.5 font-serif text-[0.9375rem]"
                    >
                      Search &amp; filters
                      <span aria-hidden="true">→</span>
                    </Link>
                  </div>
                  <button
                    ref={closeButtonRef}
                    type="button"
                    onClick={collapse}
                    className={`${CHIP_CLASS} missal-focus pointer-events-auto shrink-0 py-2`}
                  >
                    <XIcon className="size-4" />
                    Close
                  </button>
                </div>
              ) : (
                <button
                  ref={openButtonRef}
                  type="button"
                  onClick={expand}
                  className={`${CHIP_CLASS} missal-focus absolute top-3 right-3 z-[1150]`}
                >
                  <ExpandIcon className="size-3.5" />
                  Expand map
                </button>
              )}
            </>,
            host,
          )
        : null}
    </>
  );
}
