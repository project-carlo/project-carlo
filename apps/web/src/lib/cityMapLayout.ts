import type { City, LatLng } from "./cities";
import type { ClusterIndex, ClusterablePoint } from "./mapClusters";
import type { MapView } from "./mapView";
import {
  fitZoom,
  staticMapBounds,
  type StaticMapSize,
} from "./staticMap";

/**
 * The city and church pages' map as it opens: its view, and the markers the
 * live map draws there. The still preview (CityMapPreview) draws exactly
 * these, so the live map, mounted over it, changes nothing until it's moved.
 */

/**
 * The still preview's canvas, centered in the preview and cropped by it:
 * wider than the page column ever gets and taller than the preview (whose
 * desktop height fits the live map's pin popups), so the city stays in the
 * middle at any width without measuring anything.
 */
export const CITY_MAP_CANVAS: StaticMapSize = { width: 800, height: 448 };

/** The church page's canvas, the same way: its map sits in a wider column. */
export const CHURCH_MAP_CANVAS: StaticMapSize = { width: 960, height: 448 };

/**
 * A church page's map: the church's part of town, with the churches near it,
 * a step closer in than a place search (zoom 12). Closer, a phone's preview
 * shows a few blocks and seldom a neighbour.
 */
const CHURCH_MAP_ZOOM = 13;

/**
 * How far from the center the city's churches may sit: inside a phone-width
 * preview, with room left above each point for its pin.
 */
const FIT_HALF_WIDTH = 130;
const FIT_HALF_HEIGHT = 72;

/** Close enough for a one-church town to show its streets, far enough for a city. */
const MIN_ZOOM = 9;
const MAX_ZOOM = 14;

/**
 * How far past the canvas a marker's point may be and still show on it: a
 * roundel's disc rises up to 49 px above its point, and is up to 50 px across.
 */
const MARKER_REACH_PX = 64;

/**
 * A marker as the live map draws it: a church's pin (`current` for the church
 * a church page is about), or a numbered roundel.
 */
export type CityMapMarker =
  | { kind: "pin"; id: number; lat: number; lng: number; current?: boolean }
  | { kind: "cluster"; id: number; lat: number; lng: number; count: number };

export interface CityMapData {
  view: MapView;
  /** The still preview's canvas (CITY_MAP_CANVAS or CHURCH_MAP_CANVAS). */
  canvas: StaticMapSize;
  markers: CityMapMarker[];
}

/** The view a city's map opens on: centered on the city, its churches in view. */
export function cityMapView(city: City): MapView | null {
  if (!city.center) return null;
  const points: LatLng[] = city.churches.flatMap((church) =>
    church.latitude != null && church.longitude != null
      ? [{ lat: church.latitude, lng: church.longitude }]
      : [],
  );
  const zoom = fitZoom(
    city.center,
    points,
    FIT_HALF_WIDTH,
    FIT_HALF_HEIGHT,
    MIN_ZOOM,
    MAX_ZOOM,
  );
  return { lat: city.center.lat, lng: city.center.lng, zoom };
}

/** The view a church's map opens on: the church in the middle, its part of town in view. */
export function churchMapView(church: {
  latitude: number | null;
  longitude: number | null;
}): MapView | null {
  if (church.latitude == null || church.longitude == null) return null;
  return { lat: church.latitude, lng: church.longitude, zoom: CHURCH_MAP_ZOOM };
}

/**
 * What the live map draws over a canvas of `canvas` at `view`, from `index`,
 * the index it builds from the churches its default filters leave.
 */
export function cityMapMarkers<T extends ClusterablePoint>(
  index: ClusterIndex<T>,
  view: MapView,
  canvas: StaticMapSize,
): CityMapMarker[] {
  const reach = {
    width: canvas.width + 2 * MARKER_REACH_PX,
    height: canvas.height + 2 * MARKER_REACH_PX,
  };
  return index
    .entries(staticMapBounds(view, view.zoom, reach), view.zoom)
    .map((entry) =>
      entry.kind === "cluster"
        ? {
            kind: "cluster",
            id: entry.id,
            lat: entry.lat,
            lng: entry.lng,
            count: entry.count,
          }
        : {
            kind: "pin",
            id: entry.item.id,
            lat: entry.item.latitude,
            lng: entry.item.longitude,
          },
    );
}

/**
 * What the live map draws over a church page's canvas at `view`: the default
 * filters' markers, with the church's own pin marked as its page's. A church
 * the default filters leave out (one with no Mass listed) still gets its pin,
 * as the live map adds it (CityMapView).
 */
export function churchMapMarkers<T extends ClusterablePoint>(
  index: ClusterIndex<T>,
  view: MapView,
  church: { id: number; lat: number; lng: number },
): CityMapMarker[] {
  let found = false;
  const markers = cityMapMarkers(index, view, CHURCH_MAP_CANVAS).map(
    (marker): CityMapMarker => {
      if (marker.kind !== "pin" || marker.id !== church.id) return marker;
      found = true;
      return { ...marker, current: true };
    },
  );
  if (!found) markers.push({ kind: "pin", ...church, current: true });
  return markers;
}
