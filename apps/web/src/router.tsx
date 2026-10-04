import { lazy, Suspense } from "react";
import {
  createBrowserRouter,
  Navigate,
  type RouteObject,
} from "react-router-dom";
import { NotFoundPage } from "./views/NotFoundPage";
import { isAboutPageEnabled } from "./lib/featureFlags";
import { HomeRoute } from "./views/HomeRoute";

const MapPage = lazy(() =>
  import("./views/MapPage").then((m) => ({ default: m.MapPage })),
);

const ChurchPage = lazy(() =>
  import("./views/ChurchPage").then((m) => ({ default: m.ChurchPage })),
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

export const router = createBrowserRouter(routes);
