import { Outlet, ScrollRestoration, useNavigation } from "react-router-dom";

/**
 * Every page. Moving between pages, the router loads the next one's code
 * (and a church or city page's data) before it leaves the current one, so
 * the page in view stays put rather than giving way to a "Loading…" screen;
 * a thin bar across the top says something is on its way if that takes a
 * moment. A new page opens at its top, as a page load would, and back and
 * forward return to where each page was left: the browser can't do that
 * itself, as it scrolls before the page it returns to is shown. Opening or
 * closing a city page's map (src/lib/cityMap.ts) keeps its history entry, so
 * the page stays where it is.
 */
export function AppLayout() {
  const navigation = useNavigation();
  return (
    <>
      {navigation.state === "loading" ? (
        <div role="progressbar" aria-label="Loading page" className="nav-progress" />
      ) : null}
      <Outlet />
      {/* After the page, so it scrolls once the page's own layout effects
          have set it out (as the all-churches index reveals its search). */}
      <ScrollRestoration />
    </>
  );
}
