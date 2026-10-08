/**
 * The script a prerendered city or church page loads: it makes the page's
 * map preview live (see CityMapLive), the one part of the page that needs
 * JavaScript. The rest stays the static HTML it was served as.
 */
import {
  CITY_MAP_ATTRIBUTE,
  CITY_MAP_SLOT_ATTRIBUTE,
  parseCityMapConfig,
} from "../lib/cityMap";
import { reloadOnStaleChunk } from "../lib/staleDeploy";

const preview = document.querySelector<HTMLElement>(`[${CITY_MAP_ATTRIBUTE}]`);
const slot = preview?.querySelector<HTMLElement>(`[${CITY_MAP_SLOT_ATTRIBUTE}]`);
const config = parseCityMapConfig(preview?.getAttribute(CITY_MAP_ATTRIBUTE) ?? undefined);

if (slot && config) {
  reloadOnStaleChunk();
  void import("./mountCityMap").then((m) => m.mountCityMap(slot, config));
}
