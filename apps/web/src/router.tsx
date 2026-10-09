import {
  createBrowserRouter,
  Navigate,
  type RouteObject,
} from "react-router-dom";
import type { QueryClient } from "@tanstack/react-query";
import { AppLayout } from "./views/AppLayout";
import { LandingPage } from "./views/LandingPage";
import { NotFoundPage } from "./views/NotFoundPage";
import { RouteError } from "./views/RouteError";
import { isAboutPageEnabled } from "./lib/featureFlags";

const lazyPageFallback = (
  <main className="flex min-h-svh items-center justify-center bg-paper px-4">
    <p className="font-serif text-sm text-ink-soft">Loading…</p>
  </main>
);

function routes(queryClient: QueryClient): RouteObject[] {
  const list: RouteObject[] = [
    {
      path: "/",
      lazy: () =>
        import("./views/HomePage").then((m) => ({ Component: m.HomePage })),
    },
    {
      path: "/landing",
      element: <LandingPage />,
    },
    {
      path: "/map",
      element: <Navigate to="/" replace />,
    },
    {
      path: "/churches",
      lazy: () =>
        import("./views/ChurchIndexPage").then((m) => ({
          Component: m.ChurchIndexPage,
        })),
      loader: async () => {
        const { prefetchChurchIndex } = await import("./lib/pageQueries");
        await prefetchChurchIndex(queryClient);
        return null;
      },
    },
    {
      path: "/churches/:churchSlug",
      lazy: () =>
        import("./views/ChurchPage").then((m) => ({ Component: m.ChurchPage })),
      loader: async ({ params }) => {
        if (!params.churchSlug) return null;
        const { prefetchChurchPage } = await import("./lib/pageQueries");
        await prefetchChurchPage(queryClient, params.churchSlug);
        return null;
      },
    },
    {
      path: "/dioceses",
      lazy: () =>
        import("./views/DioceseIndexPage").then((m) => ({
          Component: m.DioceseIndexPage,
        })),
      loader: async () => {
        const { prefetchDioceseIndex } = await import("./lib/pageQueries");
        await prefetchDioceseIndex(queryClient);
        return null;
      },
    },
    {
      path: "/dioceses/:dioceseSlug",
      lazy: () =>
        import("./views/DiocesePage").then((m) => ({ Component: m.DiocesePage })),
      loader: async ({ params }) => {
        if (!params.dioceseSlug) return null;
        const { prefetchDiocesePage } = await import("./lib/pageQueries");
        await prefetchDiocesePage(queryClient, params.dioceseSlug);
        return null;
      },
    },
    {
      path: "/mass-times/:citySlug",
      lazy: () =>
        import("./views/CityPage").then((m) => ({ Component: m.CityPage })),
      loader: async ({ params }) => {
        if (!params.citySlug) return null;
        const { prefetchCityPage } = await import("./lib/pageQueries");
        await prefetchCityPage(queryClient, params.citySlug);
        return null;
      },
    },
  ];

  if (isAboutPageEnabled()) {
    list.push({
      path: "/about",
      lazy: () =>
        import("./views/AboutPage").then((m) => ({ Component: m.AboutPage })),
    });
  }

  list.push({
    path: "*",
    element: <NotFoundPage />,
  });
  return list;
}

export function createAppRouter(queryClient: QueryClient) {
  // One error boundary for every route: a failed lazy chunk (a page older than
  // the assets deploys carry over) or any other render error lands here.
  return createBrowserRouter([
    {
      element: <AppLayout />,
      errorElement: <RouteError fallback={lazyPageFallback} />,
      // Shown on the first load, while the first page's code arrives: just
      // the paper, as each page has a loading state of its own (the map's
      // "Loading map…") and this one would only flash before it.
      hydrateFallbackElement: <main className="min-h-svh bg-paper" />,
      children: routes(queryClient),
    },
  ]);
}
