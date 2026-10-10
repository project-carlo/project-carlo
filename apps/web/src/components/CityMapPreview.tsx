import type { CSSProperties, ReactNode } from "react";
import { Link } from "react-router-dom";
import { CityMapExpandChip } from "./CityMapExpandChip";
import { MapCornerControls } from "./MapCornerControls";
import {
  CHURCH_PIN_ANCHOR,
  CHURCH_PIN_BODY,
  CHURCH_PIN_SIZE,
  clusterAnchor,
  clusterDiameter,
  CLUSTER_Z_INDEX_OFFSET,
  CURRENT_CHURCH_PIN_BODY,
  CURRENT_CHURCH_Z_INDEX_OFFSET,
} from "@/lib/churchPin";
import {
  CITY_MAP_ATTRIBUTE,
  CITY_MAP_SLOT_ATTRIBUTE,
  CITY_MAP_ZOOM_CORNER_CLASS,
  type CityMapConfig,
} from "@/lib/cityMap";
import type { CityMapData, CityMapMarker } from "@/lib/cityMapLayout";
import { encodeMapViewToParams, type MapView } from "@/lib/mapView";
import {
  staticMapPlacement,
  staticMapPosition,
  staticMapTiles,
  type StaticMapPosition,
  type StaticMapSize,
} from "@/lib/staticMap";

const OSM_COPYRIGHT_URL = "https://www.openstreetmap.org/copyright";

/** A marker, and the pixel its point falls on in the canvas. */
interface PlacedMarker {
  marker: CityMapMarker;
  at: StaticMapPosition;
}

/**
 * A marker as Leaflet draws it (ChurchMap's divIcons): the same classes and
 * markup, its anchor on the same pixel, so the live marker lands on it.
 */
function StaticMarker({ marker, at }: PlacedMarker) {
  if (marker.kind === "pin") {
    const [width, height] = CHURCH_PIN_SIZE;
    const [x, y] = CHURCH_PIN_ANCHOR;
    return (
      <div
        className={`leaflet-marker-icon church-map-marker${marker.current ? " is-current" : ""}`}
        style={{ left: at.left - x, top: at.top - y, width, height }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          fill="none"
          aria-hidden="true"
          dangerouslySetInnerHTML={{
            __html: marker.current ? CURRENT_CHURCH_PIN_BODY : CHURCH_PIN_BODY,
          }}
        />
      </div>
    );
  }
  const size = clusterDiameter(marker.count);
  const [x, y] = clusterAnchor(size);
  return (
    <div
      className="leaflet-marker-icon church-map-cluster"
      style={{ left: at.left - x, top: at.top - y, width: size, height: size }}
    >
      <span className="church-map-cluster-disc" style={{ width: size, height: size }}>
        <span className="church-map-cluster-count">{marker.count}</span>
      </span>
    </div>
  );
}

/** A marker's zIndexOffset on the live map. */
function zIndexOffset(marker: CityMapMarker): number {
  if (marker.kind === "cluster") return CLUSTER_Z_INDEX_OFFSET;
  return marker.current ? CURRENT_CHURCH_Z_INDEX_OFFSET : 0;
}

/**
 * The markers in Leaflet's stacking order: lower ones over higher ones,
 * roundels over pins, and a church page's own pin over them all (each its
 * point's `top` plus its zIndexOffset).
 */
function placeMarkers(
  markers: CityMapMarker[],
  view: MapView,
  canvas: StaticMapSize,
): PlacedMarker[] {
  const zIndex = ({ marker, at }: PlacedMarker) => at.top + zIndexOffset(marker);
  return markers
    .map((marker) => ({
      marker,
      at: staticMapPosition(view, view.zoom, canvas, marker),
    }))
    .sort((a, b) => zIndex(a) - zIndex(b));
}

/**
 * A city's map (or a church's, on its page) as the live map opens on it:
 * OpenStreetMap tiles, every church the home map would show there (as its
 * pins or numbered roundels, a church page's own pin marked),
 * the Expand button and, on a desktop, the zoom buttons. Plain HTML, laid out
 * here, so the prerendered page draws it without JavaScript, pixel for pixel
 * as Leaflet will (see src/lib/staticMap.ts).
 *
 * The live map (CityMapLive) is mounted over it, by `live` in the app and by
 * src/islands/cityMap.ts on a prerendered page, into the slot marked
 * CITY_MAP_SLOT_ATTRIBUTE. It stays hidden until its markers are in, then
 * takes over in one frame: `.city-map` in app.css. Without JavaScript the
 * preview links to the home map at the same view.
 */
export function CityMapPreview({
  label,
  map,
  churchId,
  live,
  className = "",
}: {
  /** What the map is around: "East Aurora, NY", or a church's name. */
  label: string;
  map: CityMapData | null;
  /** On a church page, its church (see CityMapConfig). */
  churchId?: number;
  live?: (config: CityMapConfig) => ReactNode;
  className?: string;
}) {
  if (!map) return null;
  const { view, canvas, markers } = map;

  const config: CityMapConfig =
    churchId === undefined ? { label, view } : { label, view, churchId };
  const mapHref = `/?${encodeMapViewToParams(view, new URLSearchParams())}`;
  const tiles = staticMapTiles(view, view.zoom, canvas);
  const canvasStyle = {
    width: canvas.width,
    height: canvas.height,
    // For `.city-map-canvas`'s fallback placement, in app.css.
    "--city-map-canvas-width": `${canvas.width}px`,
    "--city-map-canvas-height": `${canvas.height}px`,
    ...staticMapPlacement(view, view.zoom, canvas),
  } as CSSProperties;

  return (
    <div
      {...{ [CITY_MAP_ATTRIBUTE]: JSON.stringify(config) }}
      className={`city-map group relative h-56 overflow-hidden border border-rule-strong bg-paper-deep shadow-missal-floating md:h-96 ${className}`}
    >
      <div aria-hidden="true" className="city-map-canvas absolute" style={canvasStyle}>
        <div className="city-map-tiles absolute inset-0">
          {tiles.map((tile) => (
            <img
              key={tile.key}
              src={tile.url}
              alt=""
              width={256}
              height={256}
              decoding="async"
              draggable={false}
              className="absolute max-w-none select-none"
              style={{ left: tile.left, top: tile.top }}
            />
          ))}
        </div>
        <div className="city-map-static-pins">
          {placeMarkers(markers, view, canvas).map(({ marker, at }) => (
            <StaticMarker key={`${marker.kind}-${marker.id}`} marker={marker} at={at} />
          ))}
        </div>
      </div>

      {/* The whole preview opens the map; the attribution link sits above it. */}
      <Link
        to={mapHref}
        aria-label={`Open the map of churches around ${label}`}
        className="city-map-link missal-focus absolute inset-0"
      />
      <CityMapExpandChip className="city-map-static-control" />
      <MapCornerControls
        map={null}
        zoom
        className={`city-map-static-control ${CITY_MAP_ZOOM_CORNER_CLASS} hidden md:block`}
      />
      <a
        href={OSM_COPYRIGHT_URL}
        className="city-map-attribution absolute right-0 bottom-0 z-10 px-1.5 py-0.5"
      >
        &copy; OpenStreetMap contributors
      </a>
      {/* `contents`, so it covers nothing until the live map fills it. */}
      <div {...{ [CITY_MAP_SLOT_ATTRIBUTE]: "" }} className="contents">
        {live?.(config)}
      </div>
    </div>
  );
}
