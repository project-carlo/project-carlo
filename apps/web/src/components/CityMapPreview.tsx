import type { CSSProperties, ReactNode } from "react";
import { Link } from "react-router-dom";
import type { CityPageData } from "../api";
import { CityMapExpandChip } from "./CityMapExpandChip";
import { MapCornerControls } from "./MapCornerControls";
import {
  CHURCH_PIN_ANCHOR,
  CHURCH_PIN_BODY,
  CHURCH_PIN_SIZE,
  clusterAnchor,
  clusterDiameter,
} from "@/lib/churchPin";
import {
  CITY_MAP_ATTRIBUTE,
  CITY_MAP_SLOT_ATTRIBUTE,
  type CityMapConfig,
} from "@/lib/cityMap";
import { CITY_MAP_CANVAS, type CityMapMarker } from "@/lib/cityMapLayout";
import { encodeMapViewToParams, type MapView } from "@/lib/mapView";
import {
  staticMapPlacement,
  staticMapPosition,
  staticMapTiles,
} from "@/lib/staticMap";

const OSM_COPYRIGHT_URL = "https://www.openstreetmap.org/copyright";

/**
 * A marker as Leaflet draws it (ChurchMap's divIcons): the same classes and
 * markup, its anchor on the same pixel, so the live marker lands on it.
 */
function StaticMarker({ marker, view }: { marker: CityMapMarker; view: MapView }) {
  const at = staticMapPosition(view, view.zoom, CITY_MAP_CANVAS, marker);
  if (marker.kind === "pin") {
    const [width, height] = CHURCH_PIN_SIZE;
    const [x, y] = CHURCH_PIN_ANCHOR;
    return (
      <div
        className="leaflet-marker-icon church-map-marker"
        style={{ left: at.left - x, top: at.top - y, width, height }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          fill="none"
          aria-hidden="true"
          dangerouslySetInnerHTML={{ __html: CHURCH_PIN_BODY }}
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

/** Leaflet's stacking: lower markers over higher ones, roundels over pins. */
function stackOrder(view: MapView) {
  const key = (marker: CityMapMarker) =>
    staticMapPosition(view, view.zoom, CITY_MAP_CANVAS, marker).top +
    (marker.kind === "cluster" ? 500 : 0);
  return (a: CityMapMarker, b: CityMapMarker) => key(a) - key(b);
}

/**
 * The city's map as the live map opens on it: OpenStreetMap tiles, every
 * church the home map would show there (as its pins or numbered roundels),
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
  data,
  live,
  className = "",
}: {
  data: CityPageData;
  live?: (config: CityMapConfig) => ReactNode;
  className?: string;
}) {
  const { city, map } = data;
  if (!map) return null;
  const { view, markers } = map;

  const config: CityMapConfig = { label: city.label, view };
  const mapHref = `/?${encodeMapViewToParams(view, new URLSearchParams())}`;
  const tiles = staticMapTiles(view, view.zoom, CITY_MAP_CANVAS);
  const canvasStyle: CSSProperties = {
    width: CITY_MAP_CANVAS.width,
    height: CITY_MAP_CANVAS.height,
    ...staticMapPlacement(view, view.zoom, CITY_MAP_CANVAS),
  };

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
          {[...markers].sort(stackOrder(view)).map((marker) => (
            <StaticMarker key={`${marker.kind}-${marker.id}`} marker={marker} view={view} />
          ))}
        </div>
      </div>

      {/* The whole preview opens the map; the attribution link sits above it. */}
      <Link
        to={mapHref}
        aria-label={`Open the map of churches around ${city.label}`}
        className="city-map-link missal-focus absolute inset-0"
      />
      <CityMapExpandChip className="city-map-static-control" />
      <MapCornerControls
        map={null}
        zoom
        className="city-map-static-control right-3 bottom-7 hidden md:block"
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
