import { Fragment, memo, useEffect, useMemo, useRef } from "react";
import type { RefObject } from "react";
import { Link } from "react-router-dom";
import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMap,
  useMapEvents,
} from "react-leaflet";
import type { Marker as LeafletMarker } from "leaflet";
import L from "leaflet";
import type { ChurchMapItem } from "../types";
import type { MapView } from "../lib/mapView";
import { rollUpEventsByDay } from "../lib/eventRollup";
import { formatAddress } from "../utils";
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
    <path d="M17 2C9.27 2 3 8.27 3 16c0 3.7 1.73 7.3 4 10.5C9.5 30 13.5 34.4 15.8 38.6a1.35 1.35 0 0 0 2.4 0C20.5 34.4 24.5 30 27 26.5 29.27 23.3 31 19.7 31 16 31 8.27 24.73 2 17 2Z"
          fill="var(--paper)" stroke="var(--brass)" stroke-width="1.3" />
    <circle cx="17" cy="16" r="9.5" fill="none" stroke="var(--rule-strong)" stroke-width="0.8" />
    <g stroke="var(--rubric)" stroke-width="2" stroke-linecap="round">
      <path d="M17 9.5 V 21.5" />
      <path d="M12.5 13.5 H 21.5" />
    </g>
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
  html: pinHtml(CHURCH_PIN_ID, 34, 42),
  className: "church-map-marker",
  iconSize: [34, 42],
  iconAnchor: [17, 40],
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
    zoom?: number;
    requestId?: number;
  } | null;
  /** Camera to mount the map at; falls back to the Rochester-area default. */
  initialView?: MapView | null;
  /** Fires after the user finishes panning/zooming so the view can be persisted. */
  onViewChange?: (view: MapView) => void;
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

function ChangeView({
  center,
}: {
  center: { lat: number; lng: number; zoom?: number; requestId?: number };
}) {
  const map = useMap();
  useEffect(() => {
    if (center.zoom != null) {
      map.flyTo([center.lat, center.lng], center.zoom, { duration: 0.8 });
    } else {
      map.panTo([center.lat, center.lng]);
    }
  }, [map, center.lat, center.lng, center.zoom, center.requestId]);
  return null;
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
 * Popup body for one parish.
 *
 * Split out of `ChurchMarker` on purpose: react-leaflet renders a popup's
 * children only once Leaflet has opened it, so keeping this in its own
 * component means the rollup, the date formatting and ~20 elements per parish
 * are built for the one open popup rather than for all ~130 pins on every
 * filter change.
 */
function ChurchPopupBody({ church }: { church: ChurchMapItem }) {
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
          {church.name ?? "Unnamed parish"}
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
        <Fleuron label="Upcoming" className="mb-2.5" />

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
              No services listed yet.
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
}: {
  church: ChurchMapItem;
  /**
   * Set only on the marker a selection targets, and bumped on every repeat
   * selection. Leaving it undefined everywhere else keeps the other markers'
   * props identical so they never re-render when one pin is picked.
   */
  openPopupRequestId: number | undefined;
}) {
  const markerRef = useRef<LeafletMarker | null>(null);
  useEffect(() => {
    if (openPopupRequestId !== undefined) {
      markerRef.current?.openPopup();
    }
  }, [openPopupRequestId]);

  // A fresh array literal here would look like a moved marker to react-leaflet,
  // which would call setLatLng (and re-project and re-transform the pin) on
  // every render.
  const position = useMemo<[number, number]>(
    () => [church.latitude as number, church.longitude as number],
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

const SearchPlaceMarker = memo(function SearchPlaceMarker({
  place,
}: {
  place: {
    lat: number;
    lng: number;
    title: string;
    subtitle?: string | null;
    requestId?: number;
  };
}) {
  const markerRef = useRef<LeafletMarker | null>(null);
  useEffect(() => {
    markerRef.current?.openPopup();
  }, [place.requestId]);

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
            Searched place
          </div>
          <h3 className="font-display text-[1.25rem] leading-[1.15] font-normal text-ink">
            {place.title}
          </h3>
          {place.subtitle ? (
            <p className="font-serif text-[0.875rem] leading-snug text-ink-soft">
              {place.subtitle}
            </p>
          ) : null}
        </div>
      </Popup>
    </Marker>
  );
});

export const ChurchMap = memo(function ChurchMap({
  churches,
  centerOn,
  initialView,
  onViewChange,
}: ChurchMapProps) {
  const withCoords = useMemo(
    () =>
      churches.filter(
        (church) => church.latitude !== null && church.longitude !== null,
      ),
    [churches],
  );
  // MapContainer only reads center/zoom on mount, which is exactly what we want:
  // restore the persisted view once, then let the user (and `centerOn`) drive it.
  const center: [number, number] = initialView
    ? [initialView.lat, initialView.lng]
    : defaultCenter;
  const zoom = initialView?.zoom ?? 11;

  return (
    <MapContainer
      center={center}
      zoom={zoom}
      className="church-map h-full w-full"
      scrollWheelZoom
      zoomControl={false}
    >
      {centerOn && <ChangeView center={centerOn} />}
      {onViewChange && <ViewReporter onViewChange={onViewChange} />}
      <PopupPaneElevator />
      <TileLayer
        attribution={OSM_ATTRIBUTION}
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        maxZoom={19}
      />
      {withCoords.map((church) => (
        <ChurchMarker
          key={church.id}
          church={church}
          openPopupRequestId={
            centerOn?.churchId === church.id ? (centerOn.requestId ?? 0) : undefined
          }
        />
      ))}
      {centerOn?.placeTitle ? (
        <SearchPlaceMarker
          place={{
            lat: centerOn.lat,
            lng: centerOn.lng,
            title: centerOn.placeTitle,
            subtitle: centerOn.placeSubtitle,
            requestId: centerOn.requestId,
          }}
        />
      ) : null}
    </MapContainer>
  );
});
