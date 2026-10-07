import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import type { CityPageData } from "../api";
import { ExpandIcon } from "@/components/icons";
import { CHURCH_PIN_OUTLINE } from "@/lib/churchPin";
import type { LatLng } from "@/lib/cities";
import {
  CITY_MAP_ATTRIBUTE,
  CITY_MAP_OPEN_ATTRIBUTE,
  CITY_MAP_SLOT_ATTRIBUTE,
  type CityMapConfig,
} from "@/lib/cityMap";
import { encodeMapViewToParams } from "@/lib/mapView";
import {
  fitZoom,
  staticMapPosition,
  staticMapTiles,
  type StaticMapPosition,
  type StaticMapSize,
} from "@/lib/staticMap";

/**
 * The tiles' canvas, centered in the preview and cropped by it: wider than
 * the page column ever gets and taller than the preview (whose desktop height
 * fits the live map's pin popups), so the city stays in
 * the middle at any width without measuring anything, and the prerendered
 * page needs no JavaScript to draw it.
 */
const CANVAS: StaticMapSize = { width: 800, height: 448 };

/**
 * How far from the center the city's churches may sit: inside a phone-width
 * preview, with room left above each point for its pin.
 */
const FIT_HALF_WIDTH = 130;
const FIT_HALF_HEIGHT = 72;

/** Close enough for a one-church town to show its streets, far enough for a city. */
const MIN_ZOOM = 9;
const MAX_ZOOM = 14;

const CITY_PIN_WIDTH = 26;
const NEARBY_PIN_WIDTH = 20;

const OSM_COPYRIGHT_URL = "https://www.openstreetmap.org/copyright";

function coordinates(church: {
  latitude: number | null;
  longitude: number | null;
}): LatLng | null {
  return church.latitude != null && church.longitude != null
    ? { lat: church.latitude, lng: church.longitude }
    : null;
}

/** The home map's pin, drawn with its tip on `position`. */
function PreviewPin({
  position,
  width,
  nearby,
}: {
  position: StaticMapPosition;
  width: number;
  nearby: boolean;
}) {
  const height = (width * 42) / 34;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 34 42"
      width={width}
      height={height}
      fill="none"
      className={`city-map-pin absolute ${nearby ? "opacity-70" : ""}`}
      style={{
        left: position.left - width / 2,
        top: position.top - (height * 40) / 42,
      }}
    >
      <path
        d={CHURCH_PIN_OUTLINE}
        fill="var(--paper)"
        stroke="var(--brass)"
        strokeWidth="1.3"
      />
      <g stroke="var(--rubric)" strokeWidth="2" strokeLinecap="round">
        <path d="M17 9.5 V 21.5" />
        <path d="M12.5 13.5 H 21.5" />
      </g>
    </svg>
  );
}

/**
 * A still map of the city with its churches pinned, and the nearby ones that
 * fit. Tiles and pins are plain HTML, laid out here, so the prerendered page
 * shows the same preview as the app.
 *
 * It's the placeholder the live map (CityMapLive) is mounted over, by `live`
 * in the app and by src/islands/cityMap.ts on a prerendered page, into the
 * slot marked CITY_MAP_SLOT_ATTRIBUTE. Without JavaScript it stays a link to
 * the home map at the same view. `.city-map` in app.css hides the still pins
 * and controls once the live map's are up.
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
  const { city, churches, nearby } = data;
  const center = city.center;
  if (!center) return null;

  const cityPoints = churches
    .map((entry) => coordinates(entry.church))
    .filter((point) => point !== null);
  const zoom = fitZoom(
    center,
    cityPoints,
    FIT_HALF_WIDTH,
    FIT_HALF_HEIGHT,
    MIN_ZOOM,
    MAX_ZOOM,
  );
  const tiles = staticMapTiles(center, zoom, CANVAS);

  const pins = [
    ...nearby.map((entry) => ({ entry, nearby: true })),
    ...churches.map((entry) => ({ entry, nearby: false })),
  ]
    .flatMap(({ entry, nearby }) => {
      const point = coordinates(entry.church);
      if (!point) return [];
      const position = staticMapPosition(center, zoom, CANVAS, point);
      const onCanvas =
        position.left >= 0 &&
        position.left <= CANVAS.width &&
        position.top >= 0 &&
        position.top <= CANVAS.height;
      return onCanvas ? [{ id: entry.church.id, position, nearby }] : [];
    })
    // Lower pins over higher ones, as on the map; the city's over the nearby.
    .sort(
      (a, b) =>
        Number(a.nearby === false) - Number(b.nearby === false) ||
        a.position.top - b.position.top,
    );

  const config: CityMapConfig = {
    label: city.label,
    view: { lat: center.lat, lng: center.lng, zoom },
  };
  const mapHref = `/?${encodeMapViewToParams(config.view, new URLSearchParams())}`;

  return (
    <div
      {...{ [CITY_MAP_ATTRIBUTE]: JSON.stringify(config) }}
      className={`city-map group relative h-56 overflow-hidden border border-rule-strong bg-paper-deep shadow-missal-floating md:h-96 ${className}`}
    >
      <div
        aria-hidden="true"
        className="absolute top-1/2 left-1/2"
        style={{
          width: CANVAS.width,
          height: CANVAS.height,
          marginLeft: -CANVAS.width / 2,
          marginTop: -CANVAS.height / 2,
        }}
      >
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
          {pins.map((pin) => (
            <PreviewPin
              key={pin.id}
              position={pin.position}
              width={pin.nearby ? NEARBY_PIN_WIDTH : CITY_PIN_WIDTH}
              nearby={pin.nearby}
            />
          ))}
        </div>
      </div>

      {/* The whole preview opens the map; the attribution link sits above it. */}
      <Link
        to={mapHref}
        {...{ [CITY_MAP_OPEN_ATTRIBUTE]: "" }}
        aria-label={`Open the map of churches around ${city.label}`}
        className="missal-focus absolute inset-0"
      />
      <span
        aria-hidden="true"
        className="city-map-static-chip pointer-events-none absolute top-3 right-3 inline-flex items-center gap-2 border border-rule-strong bg-paper/95 px-3 py-1.5 font-serif text-[0.9375rem] text-rubric shadow-missal-floating transition-colors group-hover:text-rubric-deep"
      >
        <ExpandIcon className="size-3.5" />
        Open full map
      </span>
      <a
        href={OSM_COPYRIGHT_URL}
        className="city-map-attribution absolute right-0 bottom-0 px-1.5 py-0.5"
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
