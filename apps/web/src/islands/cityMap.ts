/**
 * The script a prerendered city page loads: it makes the page's map preview
 * live (see CityMapLive), the one part of the page that needs JavaScript. The
 * rest stays the static HTML it was served as.
 *
 * Kept tiny: on a phone, where the preview stays still until tapped, React
 * and the map load only on that tap (or when the URL already has the map
 * open); on a desktop, where the map is live in the page, they load at once.
 */
import {
  CITY_MAP_ATTRIBUTE,
  CITY_MAP_OPEN_ATTRIBUTE,
  CITY_MAP_SLOT_ATTRIBUTE,
  INLINE_MAP_MIN_WIDTH,
  isCityMapOpen,
  openCityMap,
  parseCityMapConfig,
} from "../lib/cityMap";

const preview = document.querySelector<HTMLElement>(`[${CITY_MAP_ATTRIBUTE}]`);
const slot = preview?.querySelector<HTMLElement>(`[${CITY_MAP_SLOT_ATTRIBUTE}]`);
const config = parseCityMapConfig(preview?.getAttribute(CITY_MAP_ATTRIBUTE) ?? undefined);

if (preview && slot && config) {
  let mounted: Promise<void> | null = null;
  const mount = (openedOnMount: boolean) =>
    (mounted ??= import("./mountCityMap").then((m) =>
      m.mountCityMap(slot, config, openedOnMount),
    ));

  if (window.matchMedia(`(min-width: ${INLINE_MAP_MIN_WIDTH}px)`).matches || isCityMapOpen()) {
    void mount(false);
  } else {
    // Until the map is mounted, the preview is still its no-JavaScript link
    // to the home map: a tap opens the map here instead, or follows the link
    // if the map can't load.
    const link = preview.querySelector<HTMLAnchorElement>(`[${CITY_MAP_OPEN_ATTRIBUTE}]`);
    link?.addEventListener("click", (event) => {
      if (mounted) return;
      event.preventDefault();
      openCityMap();
      mount(true).catch(() => window.location.assign(link.href));
    });
    // The back button after an earlier tap, or forward to it.
    window.addEventListener("hashchange", () => {
      if (isCityMapOpen()) void mount(false);
    });
  }
}
