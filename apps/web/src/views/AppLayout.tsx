import { useLayoutEffect } from "react";
import {
  Outlet,
  useLocation,
  useNavigation,
  useNavigationType,
} from "react-router-dom";

/**
 * Every page. Moving between pages, the router loads the next one's code
 * (and a church or city page's data) before it leaves the current one, so
 * the page in view stays put rather than giving way to a "Loading…" screen;
 * a thin bar across the top says something is on its way if that takes a
 * moment. A new page opens at its top, as a page load would.
 */
export function AppLayout() {
  const navigation = useNavigation();
  const { pathname } = useLocation();
  const navigationType = useNavigationType();
  useLayoutEffect(() => {
    if (navigationType === "PUSH") window.scrollTo(0, 0);
  }, [pathname, navigationType]);

  return (
    <>
      {navigation.state === "loading" ? (
        <div role="progressbar" aria-label="Loading page" className="nav-progress" />
      ) : null}
      <Outlet />
    </>
  );
}
