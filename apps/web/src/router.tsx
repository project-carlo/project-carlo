import { lazy, Suspense } from "react";
import {
  createBrowserRouter,
  Navigate,
  Outlet,
  ScrollRestoration,
  type RouteObject,
} from "react-router-dom";
import { NotFoundPage } from "./views/NotFoundPage";
import { isAboutPageEnabled } from "./lib/featureFlags";
import { statePath } from "./lib/places";
import { HomeRoute } from "./views/HomeRoute";

const MapPage = lazy(() =>
  import("./views/MapPage").then((m) => ({ default: m.MapPage })),
);

const ChurchPage = lazy(() =>
  import("./views/ChurchPage").then((m) => ({ default: m.ChurchPage })),
);

// One chunk for the four browse pages: they share the place index and parts.
const DioceseIndexRoute = lazy(() =>
  import("./views/browse/BrowseRoutes").then((m) => ({
    default: m.DioceseIndexRoute,
  })),
);
const DioceseRoute = lazy(() =>
  import("./views/browse/BrowseRoutes").then((m) => ({ default: m.DioceseRoute })),
);
const StateRoute = lazy(() =>
  import("./views/browse/BrowseRoutes").then((m) => ({ default: m.StateRoute })),
);
const CityRoute = lazy(() =>
  import("./views/browse/BrowseRoutes").then((m) => ({ default: m.CityRoute })),
);

const AboutPage = lazy(() =>
  import("./views/AboutPage").then((m) => ({ default: m.AboutPage })),
);

const lazyPageFallback = (
  <main className="flex min-h-svh items-center justify-center bg-paper px-4">
    <p className="font-serif text-sm text-ink-soft">Loading…</p>
  </main>
);

const aboutPageEnabled = isAboutPageEnabled();

const routes: RouteObject[] = [
  {
    path: "/",
    element: <HomeRoute showAbout={aboutPageEnabled} />,
  },
  {
    path: "/landing",
    element: <Navigate to="/" replace />,
  },
  {
    path: "/map",
    element: (
      <Suspense fallback={lazyPageFallback}>
        <MapPage />
      </Suspense>
    ),
  },
  {
    path: "/dioceses",
    element: (
      <Suspense fallback={lazyPageFallback}>
        <DioceseIndexRoute />
      </Suspense>
    ),
  },
  {
    path: "/dioceses/:key",
    element: (
      <Suspense fallback={lazyPageFallback}>
        <DioceseRoute />
      </Suspense>
    ),
  },
  { path: "/mass-times", element: <Navigate to={statePath()} replace /> },
  {
    path: "/mass-times/:state",
    element: (
      <Suspense fallback={lazyPageFallback}>
        <StateRoute />
      </Suspense>
    ),
  },
  {
    path: "/mass-times/:state/:city",
    element: (
      <Suspense fallback={lazyPageFallback}>
        <CityRoute />
      </Suspense>
    ),
  },
  {
    path: "/churches/:churchSlug",
    element: (
      <Suspense fallback={lazyPageFallback}>
        <ChurchPage />
      </Suspense>
    ),
  },
];

if (aboutPageEnabled) {
  routes.push({
    path: "/about",
    element: (
      <Suspense fallback={lazyPageFallback}>
        <AboutPage />
      </Suspense>
    ),
  });
}

routes.push({
  path: "*",
  element: <NotFoundPage />,
});

// A root layout so every client navigation starts at the top of the page
// (and back/forward restores the old scroll), instead of keeping the previous
// page's scroll offset.
export const router = createBrowserRouter([
  {
    element: (
      <>
        <Outlet />
        <ScrollRestoration />
      </>
    ),
    children: routes,
  },
]);
