import { lazy, Suspense } from "react";
import type { CityMapConfig } from "@/lib/cityMap";

const CityMapLive = lazy(() => import("@/components/CityMapLive"));

/**
 * Makes a city or church page's map preview live in the app (see
 * CityMapPreview); a prerendered page has src/islands/cityMap.ts do it.
 */
export function liveMap(config: CityMapConfig) {
  return (
    <Suspense fallback={null}>
      <CityMapLive config={config} />
    </Suspense>
  );
}
