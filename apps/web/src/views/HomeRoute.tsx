import { Navigate, useLocation } from "react-router-dom";
import { FILTER_PARAM_KEYS } from "../components/filterState";
import { MAP_VIEW_PARAM_KEYS } from "../lib/mapView";
import { LandingPage } from "./LandingPage";

/** Query params that only the map understands: the camera (lat/lng/z) and the
 *  filters (see filterState.ts, mapView.ts). */
const MAP_QUERY_KEYS = [...MAP_VIEW_PARAM_KEYS, ...FILTER_PARAM_KEYS];

/**
 * `/` is the landing page. Before the landing page existed the map lived at
 * `/`, so shared links look like `/?lat=..&lng=..&z=..&type=..`; send those on
 * to `/map` with the query intact.
 */
export function HomeRoute({ showAbout }: { showAbout: boolean }) {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  if (MAP_QUERY_KEYS.some((key) => params.has(key))) {
    return <Navigate to={{ pathname: "/map", search }} replace />;
  }
  return <LandingPage showAbout={showAbout} />;
}
