import { queryOptions, type QueryClient } from "@tanstack/react-query";
import {
  ChurchNotFoundError,
  CityNotFoundError,
  fetchChurch,
  fetchChurchEvents,
  fetchCityPage,
} from "../api";
import { EVENT_TYPE_ORDER } from "../constants/eventTypes";

/** React Query's default; a failure that outlasts it shows the error and Retry. */
const MAX_RETRIES = 3;

/**
 * The church and city pages' queries, shared by the pages and the router's
 * loaders (src/router.tsx), which fetch them before a page is shown so it
 * arrives whole rather than as a "Loading…" line.
 */
export function cityQuery(slug: string) {
  return queryOptions({
    queryKey: ["city", slug],
    queryFn: () => fetchCityPage(slug),
    retry: (failureCount, error) =>
      failureCount < MAX_RETRIES && !(error instanceof CityNotFoundError),
  });
}

export function churchQuery(slug: string) {
  return queryOptions({
    queryKey: ["church", slug],
    queryFn: () => fetchChurch(slug),
    retry: (failureCount, error) =>
      failureCount < MAX_RETRIES && !(error instanceof ChurchNotFoundError),
  });
}

export function churchEventsQuery(slug: string) {
  return queryOptions({
    queryKey: ["church-events", slug],
    queryFn: () => fetchChurchEvents(slug, [...EVENT_TYPE_ORDER]),
    retry: (failureCount, error) =>
      failureCount < MAX_RETRIES && !(error instanceof ChurchNotFoundError),
  });
}

/** Fetches what a city page shows. Never throws: the page shows any error. */
export async function prefetchCityPage(
  queryClient: QueryClient,
  slug: string,
): Promise<void> {
  await queryClient.prefetchQuery(cityQuery(slug));
}

/** Fetches what a church page shows. Never throws: the page shows any error. */
export async function prefetchChurchPage(
  queryClient: QueryClient,
  slug: string,
): Promise<void> {
  await Promise.all([
    queryClient.prefetchQuery(churchQuery(slug)),
    queryClient.prefetchQuery(churchEventsQuery(slug)),
  ]);
}
