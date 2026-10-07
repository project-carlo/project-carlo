import {
  Fragment,
  memo,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import type { ReactNode, Ref, RefObject } from "react";
import { Link } from "react-router-dom";
import {
  MapContainer,
  Marker,
  Polygon,
  Popup,
  TileLayer,
  useMap,
  useMapEvents,
} from "react-leaflet";
import type {
  LeafletEventHandlerFnMap,
  Map as LeafletMap,
  Marker as LeafletMarker,
} from "leaflet";
import L from "leaflet";
import type { ChurchMapItem, EventSummary } from "../types";
import type { MapView } from "../lib/mapView";
import type { MapStart } from "../lib/mapStart";
import {
  buildClusterIndex,
  convexHull,
  PIN_ZOOM,
  type BBox,
  type ClusterIndex,
  type MapCluster,
} from "../lib/mapClusters";
import {
  CHURCH_PIN_ANCHOR,
  CHURCH_PIN_BODY,
  CHURCH_PIN_SIZE,
  clusterAnchor,
  clusterDiameter,
  CLUSTER_Z_INDEX_OFFSET,
} from "../lib/churchPin";
import { useDocumentLinks } from "../lib/documentLinks";
import { OSM_TILE_URL } from "../lib/staticMap";
import { rollUpEventsByDay } from "../lib/eventRollup";
import { formatAddress } from "../utils";
import { EVENT_TYPE_LABELS } from "../constants/eventTypes";
import { UNNAMED_CHURCH } from "../copy";
import { Fleuron } from "@/components/Fleuron";

const OSM_ATTRIBUTION =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

const defaultCenter: [number, number] = [43.1566, -77.6088];

/** Day rows shown in a pin popup before it spills into "…and N more days". */
const POPUP_DAY_ROWS = 3;

/** Every popup on the map is cut to one card size, so pins don't each open a
 *  differently-shaped panel as you click along a street. */
const POPUP_MIN_WIDTH = 225;
const POPUP_MAX_WIDTH = 275;

/* A cross-in-roundel pin: cream disc with a brass ring, a rubric-red Latin
 * cross at the center — and, for a searched place, a solid rubric pin. Both
 * shapes live in one hidden sprite so nothing is fetched from a CDN at runtime
 * and, more importantly, so each marker's icon is a three-node
 * `<svg><use/></svg>` rather than ~15 nodes parsed out of an HTML string:
 * `L.DivIcon.createIcon` runs once per marker, and ~130 pins are re-created
 * whenever the service-type filter changes.
 *
 * The church pin's shadow comes from `.church-map-marker svg`'s CSS
 * `drop-shadow` in app.css — it used to also carry an SVG `feDropShadow`,
 * which painted a second shadow on top of the first at ~130 pins' expense.
 * The searched-place pin has no CSS shadow, so it keeps its filter. */
const MARKER_SPRITE_ID = "church-map-pin-sprite";
const CHURCH_PIN_ID = "church-map-pin";
const PLACE_PIN_ID = "church-map-place-pin";

const markerSpriteSvg = `
<svg xmlns="http://www.w3.org/2000/svg" id="${MARKER_SPRITE_ID}" aria-hidden="true"
     style="position:absolute;width:0;height:0;overflow:hidden">
  <defs>
    <filter id="place-pin-shadow" x="-30%" y="-10%" width="160%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="1.8" flood-color="#161210" flood-opacity="0.32"/>
    </filter>
  </defs>
  <symbol id="${CHURCH_PIN_ID}" viewBox="0 0 34 42" fill="none">
    ${CHURCH_PIN_BODY}
  </symbol>
  <symbol id="${PLACE_PIN_ID}" viewBox="0 0 32 42" fill="none">
    <g filter="url(#place-pin-shadow)">
      <path d="M16 2C8.82 2 3 7.82 3 15c0 4.02 2.22 7.95 4.87 11.4 2.35 3.06 5.38 6.18 6.92 10.9a1.27 1.27 0 0 0 2.42 0c1.54-4.72 4.57-7.84 6.92-10.9C26.78 22.95 29 19.02 29 15 29 7.82 23.18 2 16 2Z"
            fill="var(--rubric)" stroke="var(--paper)" stroke-width="1.6" />
      <circle cx="16" cy="15" r="5.2" fill="var(--paper)" stroke="var(--brass)" stroke-width="1.2" />
    </g>
  </symbol>
</svg>`;

/** Add the sprite to the document once, on first import of the map bundle. */
function ensureMarkerSprite(): void {
  if (typeof document === "undefined") return;
  if (document.getElementById(MARKER_SPRITE_ID)) return;
  const holder = document.createElement("div");
  holder.innerHTML = markerSpriteSvg;
  const sprite = holder.firstElementChild;
  if (sprite) document.body.appendChild(sprite);
}

ensureMarkerSprite();

const pinHtml = (symbolId: string, width: number, height: number) =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" aria-hidden="true"><use href="#${symbolId}" /></svg>`;

const markerIcon = L.divIcon({
  html: pinHtml(CHURCH_PIN_ID, ...CHURCH_PIN_SIZE),
  className: "church-map-marker",
  iconSize: CHURCH_PIN_SIZE,
  iconAnchor: CHURCH_PIN_ANCHOR,
  popupAnchor: [0, -34],
});

const placeMarkerIcon = L.divIcon({
  html: pinHtml(PLACE_PIN_ID, 32, 42),
  className: "searched-place-marker",
  iconSize: [32, 42],
  iconAnchor: [16, 40],
  popupAnchor: [0, -34],
});

interface ChurchMapProps {
  churches: ChurchMapItem[];
  centerOn?: {
    lat: number;
    lng: number;
    churchId?: number;
    placeTitle?: string;
    placeSubtitle?: string | null;
    /** False leaves the pin's popup closed until it's clicked. */
    openPlacePopup?: boolean;
    zoom?: number;
    requestId?: number;
  } | null;
  /** Where to mount the map; falls back to the Rochester-area default. Read
   *  once, on mount. */
  start?: MapStart | null;
  /** Fires after the user finishes panning/zooming so the view can be persisted. */
  onViewChange?: (view: MapView) => void;
  /** Removes the searched-place pin; the popup offers it as a button. */
  onClearPlace?: () => void;
  /** Extra layers and behaviors, rendered inside the map so they can `useMap`. */
  children?: ReactNode;
  /** Gets the Leaflet map, for controls laid over it (MapCornerControls). */
  mapRef?: Ref<LeafletMap>;
}

/**
 * Relocate the popup pane from inside `.leaflet-map-pane` (whose `transform`
 * creates a stacking context that traps child z-indexes) to the container
 * root. The pane's transform is kept in sync via MutationObserver so popups
 * stay geo-anchored, but its z-index now participates in the page-level
 * stacking context — letting popups render above the header overlay.
 */
function PopupPaneElevator() {
  const map = useMap();
  useEffect(() => {
    const mapPane = map.getPane("mapPane");
    const popupPane = map.getPane("popupPane");
    const container = map.getContainer();
    if (!mapPane || !popupPane) return;

    container.appendChild(popupPane);
    popupPane.style.zIndex = "1100";

    const sync = () => {
      popupPane.style.transform = mapPane.style.transform;
    };
    const observer = new MutationObserver(sync);
    observer.observe(mapPane, {
      attributes: true,
      attributeFilter: ["style"],
    });
    sync();

    return () => {
      observer.disconnect();
      mapPane.appendChild(popupPane);
    };
  }, [map]);
  return null;
}

/**
 * Marks the page's floating UI laid over the map (HomePage's search card and
 * desktop filter panel), so the map can tell which part of itself is left in
 * view.
 */
const MAP_OVERLAY_SELECTOR = "[data-map-overlay]";

/**
 * How much of the map, in pixels from its left and top edges, the floating
 * UI covers, measured when it's needed: the layout changes between desktop
 * and phone widths, and the card's height with its filter pills.
 *
 * A box with more than twice as much map to its right as to its left is a
 * column (the desktop panels), so it covers everything to its left; anything
 * else is a band across the top (the phone's search card, centred with a
 * narrow gutter each side), so it covers everything above its bottom. The mobile filter sheet isn't marked:
 * while it's open it blocks the map anyway. Each inset leaves at least a
 * third of the map, so an odd window size can't squeeze the free area away.
 */
function overlayInsets(map: LeafletMap): L.Point {
  const box = map.getContainer().getBoundingClientRect();
  let left = 0;
  let top = 0;
  for (const el of document.querySelectorAll(MAP_OVERLAY_SELECTOR)) {
    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) continue;
    if (rect.right <= box.left || rect.left >= box.right) continue;
    if (rect.bottom <= box.top || rect.top >= box.bottom) continue;
    const before = rect.left - box.left;
    const beside = box.right - rect.right;
    if (beside > 2 * before) left = Math.max(left, rect.right - box.left);
    else top = Math.max(top, rect.bottom - box.top);
  }
  return L.point(
    Math.min(left, (box.width * 2) / 3),
    Math.min(top, (box.height * 2) / 3),
  );
}

/**
 * How far a target is moved from the map's centre towards the middle of the
 * uncovered area, as a fraction of the way there. The dead centre of the
 * space beside the desktop panel reads as off to the right of the screen,
 * so across it stops halfway; down (below the phone's search card)
 * it goes all the way.
 */
const FREE_AREA_PULL = { x: 0.5, y: 1 };

/** The on-screen shift from the map's centre to where a target is put. */
function freeAreaOffset(insets: L.Point): L.Point {
  return L.point(
    (insets.x / 2) * FREE_AREA_PULL.x,
    (insets.y / 2) * FREE_AREA_PULL.y,
  );
}

/**
 * The map centre that puts `latlng` in (or, across, nearly in) the middle
 * of the part of the map the floating UI leaves uncovered, at `zoom`.
 */
function centerInFreeArea(
  map: LeafletMap,
  latlng: L.LatLngExpression,
  zoom: number,
  insets: L.Point,
): L.LatLng {
  return map.unproject(
    map.project(latlng, zoom).subtract(freeAreaOffset(insets)),
    zoom,
  );
}

/** Fastest a camera move may zoom, in zoom levels per second. Leaflet's
 *  flyTo takes a fixed duration, so a four-level jump in the same time as a
 *  one-level one rushes past everything in between. */
const MAX_ZOOM_LEVELS_PER_SECOND = 3;
const MIN_FLY_SECONDS = 0.6;
const MAX_FLY_SECONDS = 2;

/** Fly to `zoom`, taking longer the further the zoom has to change. */
function flyGently(map: LeafletMap, target: L.LatLng, zoom: number): void {
  const levels = Math.abs(zoom - map.getZoom());
  const duration = Math.min(
    Math.max(levels / MAX_ZOOM_LEVELS_PER_SECOND, MIN_FLY_SECONDS),
    MAX_FLY_SECONDS,
  );
  map.flyTo(target, zoom, { duration });
}

function ChangeView({
  center,
  minZoom,
}: {
  center: { lat: number; lng: number; zoom?: number; requestId?: number };
  /**
   * Zoom the camera must reach, when a selected church would otherwise sit
   * inside a cluster at the requested (or current) zoom. Read through a ref:
   * a filter change can move it, and that alone mustn't re-fly the map.
   */
  minZoom?: number | null;
}) {
  const map = useMap();
  const minZoomRef = useRef(minZoom);
  minZoomRef.current = minZoom;
  useEffect(() => {
    let zoom = center.zoom;
    const floor = minZoomRef.current;
    if (floor != null && (zoom ?? map.getZoom()) < floor) zoom = floor;
    // Centred in the ground the floating UI leaves clear, not under the
    // search card or the filter panel.
    const target = centerInFreeArea(
      map,
      [center.lat, center.lng],
      zoom ?? map.getZoom(),
      overlayInsets(map),
    );
    if (zoom != null) {
      flyGently(map, target, zoom);
    } else {
      map.panTo(target);
    }
  }, [map, center.lat, center.lng, center.zoom, center.requestId]);
  return null;
}

/** Room kept between the covered area and the edges of the free area. */
const START_AREA_MARGIN = 24;

/**
 * Puts a start chosen for the visitor in the part of the map the floating UI
 * leaves clear: the point of a "near" start where a search result would go,
 * every church of an "area" start in view. Run as the map is created, before
 * any layer or listener is added, so no tiles load for the provisional view
 * and the move isn't reported as the visitor's own (which would write a
 * location they never chose into the URL).
 */
function placeStart(map: LeafletMap, start: MapStart): void {
  if (start.kind === "near") {
    const { lat, lng, zoom } = start.view;
    map.setView(
      centerInFreeArea(map, [lat, lng], zoom, overlayInsets(map)),
      zoom,
      { animate: false },
    );
  } else if (start.kind === "area") {
    map.fitBounds(start.bounds, {
      paddingTopLeft: overlayInsets(map).add([
        START_AREA_MARGIN,
        START_AREA_MARGIN,
      ]),
      paddingBottomRight: [START_AREA_MARGIN, START_AREA_MARGIN],
      animate: false,
    });
  }
}

/**
 * Reports the map's camera up to the parent after each pan/zoom settles, so the
 * view can be persisted to the URL. Read-only — it never moves the map itself.
 */
function ViewReporter({ onViewChange }: { onViewChange: (view: MapView) => void }) {
  const map = useMapEvents({
    moveend: () => {
      const center = map.getCenter();
      onViewChange({ lat: center.lat, lng: center.lng, zoom: map.getZoom() });
    },
  });
  return null;
}

/**
 * The popup schedule's caption: the service its times are for. The map shows
 * one service at a time, so every time in a popup is the same service; the
 * caption says which, since the rows themselves are only days and times.
 */
function scheduleCaption(events: EventSummary[]): string {
  const types = new Set(events.map((event) => event.type));
  if (types.size === 1) {
    const [type] = types;
    return EVENT_TYPE_LABELS[type];
  }
  return "Times";
}

/**
 * Popup body for one church.
 *
 * Split out of `ChurchMarker` on purpose: react-leaflet renders a popup's
 * children only once Leaflet has opened it, so keeping this in its own
 * component means the rollup, the date formatting and ~20 elements per church
 * are built for the one open popup rather than for all ~130 pins on every
 * filter change.
 */
function ChurchPopupBody({ church }: { church: ChurchMapItem }) {
  const documentLinks = useDocumentLinks();
  // upcoming_events arrives pre-sorted from fetchChurches; rolling it up keeps
  // that order while collapsing each day's several times onto one row.
  const dayRows = useMemo(
    () => rollUpEventsByDay(church.upcoming_events),
    [church.upcoming_events],
  );
  const visibleRows = dayRows.slice(0, POPUP_DAY_ROWS);
  const hiddenRowCount = dayRows.length - visibleRows.length;
  const addressLine = formatAddress(church);

  return (
    <div className="w-full">
      {/* The card's three registers — head, schedule, foot. Each owns its own
          padding so the tinted bands run to the card's edges; see
          `.map-popup-*` in app.css. */}
      <div className="map-popup-head space-y-1">
        <h3 className="font-display text-[1.35rem] leading-[1.15] font-normal text-ink">
          {church.name ?? UNNAMED_CHURCH}
        </h3>
        {addressLine ? (
          <p className="font-serif text-[0.875rem] leading-snug text-ink-soft">
            {addressLine}
          </p>
        ) : null}
      </div>

      <div className="map-popup-body">
        {/* The caption rides in the rule rather than sitting on its own line
            below it — one divider instead of two in a 250px-wide card. */}
        <Fleuron
          label={scheduleCaption(church.upcoming_events)}
          className="mb-2.5"
        />

        <ul role="list" className="m-0 space-y-1.5 p-0 list-none">
          {visibleRows.length > 0 ? (
            visibleRows.map((row) => (
              <li
                key={row.key}
                className="flex items-baseline gap-2 font-serif text-[0.9rem]"
              >
                {/* Small caps here so a day reads the same in the popup
                    as it does in the church page's schedule column. */}
                <span className="smallcaps text-[0.9375rem] text-ink">
                  {row.label || "Upcoming"}
                </span>
                <span className="min-w-3 flex-1 translate-y-[-3px] border-b border-dotted border-rule-strong" />
                <span className="text-right tabular-nums text-rubric">
                  {row.times.map((time, index) => (
                    // The separator sits outside the nowrap span so a long
                    // day wraps between times, never inside "10:30 a.m.".
                    <Fragment key={time}>
                      {index > 0 ? " · " : null}
                      <span className="whitespace-nowrap">{time}</span>
                    </Fragment>
                  ))}
                </span>
              </li>
            ))
          ) : (
            <li className="font-serif text-[0.9rem] italic text-ink-faint">
              No times listed yet.
            </li>
          )}
          {hiddenRowCount > 0 ? (
            <li className="pt-1 font-serif text-[0.8125rem] italic text-ink-faint">
              …and {hiddenRowCount} more {hiddenRowCount === 1 ? "day" : "days"}
            </li>
          ) : null}
        </ul>
      </div>

      <div className="map-popup-foot">
        <Link
          to={`/churches/${church.slug}/`}
          reloadDocument={documentLinks}
          className="map-popup-foot-link font-serif text-[0.9375rem]"
        >
          <span>Full schedule</span>
          <span aria-hidden="true">→</span>
        </Link>
      </div>
    </div>
  );
}

const SELECTED_MARKER_CLASS = "is-selected";

/**
 * Marks the pin whose popup is open. Leaflet gives that marker no class of
 * its own, so along a city street the card could be pointing at any one of a
 * dozen pins; `.church-map-marker.is-selected` in app.css lifts and haloes
 * the right one. The handler object is memoized because react-leaflet
 * re-binds every listener when its identity changes.
 */
function useSelectedMarkerClass(markerRef: RefObject<LeafletMarker | null>) {
  return useMemo(
    () => ({
      popupopen: () =>
        markerRef.current?.getElement()?.classList.add(SELECTED_MARKER_CLASS),
      popupclose: () =>
        markerRef.current
          ?.getElement()
          ?.classList.remove(SELECTED_MARKER_CLASS),
    }),
    [markerRef],
  );
}

const ChurchMarker = memo(function ChurchMarker({
  church,
  openPopupRequestId,
  onPopupRequestHandled,
}: {
  church: MappedChurch;
  /**
   * Set only on the marker a selection targets, and bumped on every repeat
   * selection. Leaving it undefined everywhere else keeps the other markers'
   * props identical so they never re-render when one pin is picked.
   */
  openPopupRequestId: number | undefined;
  /**
   * Called once the requested popup is open. Pins mount and unmount as
   * clusters split and merge, so without this a pin that was selected once
   * would re-open its popup every time zooming brought it back.
   */
  onPopupRequestHandled: (requestId: number) => void;
}) {
  const markerRef = useRef<LeafletMarker | null>(null);
  useEffect(() => {
    if (openPopupRequestId !== undefined) {
      markerRef.current?.openPopup();
      onPopupRequestHandled(openPopupRequestId);
    }
  }, [openPopupRequestId, onPopupRequestHandled]);

  // A fresh array literal here would look like a moved marker to react-leaflet,
  // which would call setLatLng (and re-project and re-transform the pin) on
  // every render.
  const position = useMemo<[number, number]>(
    () => [church.latitude, church.longitude],
    [church.latitude, church.longitude],
  );
  const eventHandlers = useSelectedMarkerClass(markerRef);

  return (
    <Marker
      ref={markerRef}
      icon={markerIcon}
      position={position}
      eventHandlers={eventHandlers}
    >
      <Popup minWidth={POPUP_MIN_WIDTH} maxWidth={POPUP_MAX_WIDTH}>
        <ChurchPopupBody church={church} />
      </Popup>
    </Marker>
  );
});

/** A church the map can place. */
type MappedChurch = ChurchMapItem & { latitude: number; longitude: number };

function hasCoords(church: ChurchMapItem): church is MappedChurch {
  return church.latitude !== null && church.longitude !== null;
}

// One icon per count: `L.divIcon` options are plain data, and reusing the
// same object keeps react-leaflet from calling setIcon on every re-render.
const clusterIcons = new Map<number, L.DivIcon>();

function clusterIcon(count: number): L.DivIcon {
  let icon = clusterIcons.get(count);
  if (!icon) {
    const size = clusterDiameter(count);
    icon = L.divIcon({
      html: `<span class="church-map-cluster-disc" style="width:${size}px;height:${size}px"><span class="church-map-cluster-count">${count}</span></span>`,
      className: "church-map-cluster",
      iconSize: [size, size],
      iconAnchor: clusterAnchor(size),
    });
    clusterIcons.set(count, icon);
  }
  return icon;
}

const ClusterMarker = memo(function ClusterMarker({
  cluster,
  onSelect,
  onHover,
}: {
  cluster: MapCluster;
  onSelect: (cluster: MapCluster) => void;
  onHover: (cluster: MapCluster | null) => void;
}) {
  const position = useMemo<[number, number]>(
    () => [cluster.lat, cluster.lng],
    [cluster.lat, cluster.lng],
  );
  const eventHandlers = useMemo<LeafletEventHandlerFnMap>(
    () => ({
      click: () => onSelect(cluster),
      mouseover: () => onHover(cluster),
      mouseout: () => onHover(null),
    }),
    [cluster, onSelect, onHover],
  );
  return (
    <Marker
      icon={clusterIcon(cluster.count)}
      position={position}
      title={`${cluster.count} ${cluster.count === 1 ? "church" : "churches"} — zoom in`}
      zIndexOffset={CLUSTER_Z_INDEX_OFFSET}
      eventHandlers={eventHandlers}
    />
  );
});

/** Margin, in pixels, kept round a clicked roundel's churches once the map
 *  has zoomed in to them. */
const ZOOM_INTO_MARGIN = 48;

/** How far past the visible map, as a fraction of its size on each side,
 *  markers are still drawn, so a short pan doesn't reveal empty ground. */
const VIEWPORT_PADDING = 0.5;

interface Viewport {
  zoom: number;
  bbox: BBox;
}

function readViewport(map: LeafletMap): Viewport {
  const bounds = map.getBounds().pad(VIEWPORT_PADDING);
  return {
    zoom: map.getZoom(),
    bbox: [
      bounds.getWest(),
      bounds.getSouth(),
      bounds.getEast(),
      bounds.getNorth(),
    ],
  };
}

/**
 * The church pins and cluster roundels for the current view.
 *
 * Only what falls in (and just around) the viewport is rendered, and the set
 * is recomputed once each pan or zoom settles, so the DOM holds tens of
 * markers however many churches the snapshot has.
 */
function ClusteredChurchMarkers({
  index,
  popupRequest,
  onPopupRequestHandled,
}: {
  index: ClusterIndex<MappedChurch>;
  popupRequest: { churchId: number; requestId: number } | null;
  onPopupRequestHandled: (requestId: number) => void;
}) {
  const map = useMap();
  const [viewport, setViewport] = useState(() => readViewport(map));
  const [hovered, setHovered] = useState<MapCluster | null>(null);
  useMapEvents({
    moveend: () => setViewport(readViewport(map)),
  });

  const entries = useMemo(
    () => index.entries(viewport.bbox, viewport.zoom),
    [index, viewport],
  );

  const zoomInto = useCallback(
    (cluster: MapCluster) => {
      setHovered(null);
      const leaves = index.leaves(cluster.id);
      const bounds = L.latLngBounds(
        leaves.map((church) => [church.latitude, church.longitude]),
      );
      // As close as keeps every church in the roundel in the part of the
      // map the floating UI leaves uncovered, but at least far enough to
      // split it, and never past the zoom where every church has its own
      // pin. A roundel of one has no extent to fit, so it goes straight to
      // that zoom.
      const insets = overlayInsets(map);
      // The target stops short of the free area's middle across (see
      // FREE_AREA_PULL), so the fit keeps that much more room on each side
      // to stay clear of the panel.
      const shortfall = insets.divideBy(2).subtract(freeAreaOffset(insets));
      const fitZoom = map.getBoundsZoom(
        bounds,
        false,
        insets
          .add(shortfall.multiplyBy(2))
          .add([2 * ZOOM_INTO_MARGIN, 2 * ZOOM_INTO_MARGIN]),
      );
      const zoom = Math.max(
        Math.min(Math.max(fitZoom, index.expansionZoom(cluster.id)), PIN_ZOOM),
        map.getZoom() + 1,
      );
      // Leaflet's flyToBounds takes the same padding but can only cap the
      // zoom, not floor it, so the centre is worked out here instead.
      flyGently(
        map,
        centerInFreeArea(map, bounds.getCenter(), zoom, insets),
        zoom,
      );
    },
    [index, map],
  );

  // Looked up in what's drawn, so the shading goes as soon as a zoom splits
  // or merges the hovered roundel (or a filter change rebuilds the index),
  // whether or not Leaflet sent a mouseout.
  const hoveredCluster = hovered
    ? entries.find(
        (entry) => entry.kind === "cluster" && entry.id === hovered.id,
      )
    : undefined;
  const coverage = useMemo(
    () =>
      hoveredCluster && hoveredCluster.kind === "cluster"
        ? convexHull(
            index
              .leaves(hoveredCluster.id)
              .map((church) => [church.latitude, church.longitude]),
          )
        : null,
    [index, hoveredCluster],
  );

  return (
    <>
      {coverage ? (
        // Options as props, not `pathOptions`: react-leaflet applies those
        // through setStyle, which ignores `className`.
        <Polygon
          positions={coverage}
          className="church-map-coverage"
          interactive={false}
          opacity={1}
          fillOpacity={1}
        />
      ) : null}
      {entries.map((entry) =>
        entry.kind === "cluster" ? (
          <ClusterMarker
            key={`cluster-${entry.id}`}
            cluster={entry}
            onSelect={zoomInto}
            onHover={setHovered}
          />
        ) : (
          <ChurchMarker
            key={entry.item.id}
            church={entry.item}
            openPopupRequestId={
              popupRequest?.churchId === entry.item.id
                ? popupRequest.requestId
                : undefined
            }
            onPopupRequestHandled={onPopupRequestHandled}
          />
        ),
      )}
    </>
  );
}

const SearchPlaceMarker = memo(function SearchPlaceMarker({
  place,
  onClear,
}: {
  place: {
    lat: number;
    lng: number;
    title: string;
    subtitle?: string | null;
    openPopup?: boolean;
    requestId?: number;
  };
  onClear?: () => void;
}) {
  const markerRef = useRef<LeafletMarker | null>(null);
  const openPopup = place.openPopup ?? true;
  useEffect(() => {
    if (openPopup) markerRef.current?.openPopup();
  }, [place.requestId, openPopup]);

  return (
    <Marker
      ref={markerRef}
      icon={placeMarkerIcon}
      position={[place.lat, place.lng]}
      zIndexOffset={1000}
    >
      <Popup minWidth={POPUP_MIN_WIDTH} maxWidth={POPUP_MAX_WIDTH}>
        <div className="map-popup-solo space-y-1.5">
          <div className="smallcaps text-[0.8125rem] text-ink-faint">
            Pinned place
          </div>
          <h3 className="font-display text-[1.25rem] leading-[1.15] font-normal text-ink">
            {place.title}
          </h3>
          {place.subtitle ? (
            <p className="font-serif text-[0.875rem] leading-snug text-ink-soft">
              {place.subtitle}
            </p>
          ) : null}
          {onClear ? (
            <button
              type="button"
              onClick={onClear}
              className="rubric-link missal-focus font-serif text-[0.875rem]"
            >
              Remove pin
            </button>
          ) : null}
        </div>
      </Popup>
    </Marker>
  );
});

export const ChurchMap = memo(function ChurchMap({
  churches,
  centerOn,
  start,
  onViewChange,
  onClearPlace,
  children,
  mapRef,
}: ChurchMapProps) {
  const withCoords = useMemo(() => churches.filter(hasCoords), [churches]);
  const clusterIndex = useMemo(
    () => buildClusterIndex(withCoords),
    [withCoords],
  );
  // MapContainer only reads center/zoom (and whenReady) on mount, which is
  // exactly what we want: open on the start once, then let the user (and
  // `centerOn`) drive it. A view from the URL is mounted as it is; any other
  // start is placed by `placeStart`, which MapContainer runs synchronously
  // once the map has a view, before it renders a single layer.
  const initialView = start?.kind === "view" ? start.view : null;
  const center: [number, number] = initialView
    ? [initialView.lat, initialView.lng]
    : defaultCenter;
  const zoom = initialView?.zoom ?? 11;
  // Leaflet calls it with the map as `this`.
  function handleReady(this: LeafletMap) {
    if (start) placeStart(this, start);
  }

  // The last selection whose popup has been opened; see ChurchMarker.
  const [handledRequestId, setHandledRequestId] = useState<number | null>(
    null,
  );
  const selectedChurchId = centerOn?.churchId;
  const selectionRequestId = centerOn?.requestId ?? 0;
  const popupRequest = useMemo(
    () =>
      selectedChurchId != null && selectionRequestId !== handledRequestId
        ? { churchId: selectedChurchId, requestId: selectionRequestId }
        : null,
    [selectedChurchId, selectionRequestId, handledRequestId],
  );
  const selectedSoloZoom =
    selectedChurchId != null ? clusterIndex.soloZoom(selectedChurchId) : null;

  return (
    <MapContainer
      ref={mapRef}
      center={center}
      zoom={zoom}
      className="church-map h-full w-full"
      scrollWheelZoom
      zoomControl={false}
      whenReady={handleReady}
    >
      {centerOn && <ChangeView center={centerOn} minZoom={selectedSoloZoom} />}
      {onViewChange && <ViewReporter onViewChange={onViewChange} />}
      <PopupPaneElevator />
      <TileLayer
        attribution={OSM_ATTRIBUTION}
        url={OSM_TILE_URL}
        maxZoom={19}
      />
      <ClusteredChurchMarkers
        index={clusterIndex}
        popupRequest={popupRequest}
        onPopupRequestHandled={setHandledRequestId}
      />
      {centerOn?.placeTitle ? (
        <SearchPlaceMarker
          place={{
            lat: centerOn.lat,
            lng: centerOn.lng,
            title: centerOn.placeTitle,
            subtitle: centerOn.placeSubtitle,
            openPopup: centerOn.openPlacePopup,
            requestId: centerOn.requestId,
          }}
          onClear={onClearPlace}
        />
      ) : null}
      {children}
    </MapContainer>
  );
});
