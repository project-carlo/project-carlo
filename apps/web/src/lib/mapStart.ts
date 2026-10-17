import {
  approximateLocationZoom,
  isNearAnyChurch,
  type ApproximateLocation,
} from "./approximateLocation";
import type { MapView } from "./mapView";

/** South-west and north-east corners, as Leaflet's bounds literals take them. */
export type LatLngBoundsTuple = [[number, number], [number, number]];

/** Where the home map opens. */
export type MapStart =
  /** A view from the URL, restored exactly as the visitor left it. */
  | { kind: "view"; view: MapView }
  /** The visitor's IP estimate, put in the part of the map the floating UI
   *  leaves clear, as a search result would be. */
  | { kind: "near"; view: MapView }
  /** Every mapped church, fitted into the part of the map the floating UI
   *  leaves clear. */
  | { kind: "area"; bounds: LatLngBoundsTuple };

type MaybeMapped = { latitude: number | null; longitude: number | null };

/** The box around every church with coordinates, or null when none has any. */
export function churchBounds(
  churches: ReadonlyArray<MaybeMapped>,
): LatLngBoundsTuple | null {
  let south = Infinity;
  let west = Infinity;
  let north = -Infinity;
  let east = -Infinity;
  for (const { latitude, longitude } of churches) {
    if (latitude == null || longitude == null) continue;
    south = Math.min(south, latitude);
    north = Math.max(north, latitude);
    west = Math.min(west, longitude);
    east = Math.max(east, longitude);
  }
  return south === Infinity
    ? null
    : [
        [south, west],
        [north, east],
      ];
}

/**
 * The start for a visit with no view in the URL: near the IP estimate when
 * there is one with a church within reach, otherwise the whole area the site
 * covers. `churches` is every church, not the ones the filters leave: whether
 * the visitor is near the covered area mustn't depend on the filters in the
 * link they followed. Null (no church is mapped at all) leaves the map on its
 * built-in default.
 */
export function firstVisitStart(
  estimate: ApproximateLocation | null,
  churches: ReadonlyArray<MaybeMapped>,
  isDesktop: boolean,
): MapStart | null {
  if (estimate && isNearAnyChurch(estimate, churches)) {
    return {
      kind: "near",
      view: {
        lat: estimate.lat,
        lng: estimate.lng,
        zoom: approximateLocationZoom(isDesktop),
      },
    };
  }
  const bounds = churchBounds(churches);
  return bounds ? { kind: "area", bounds } : null;
}
