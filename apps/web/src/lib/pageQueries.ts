import { queryOptions, type QueryClient } from "@tanstack/react-query";
import {
  ChurchNotFoundError,
  CityNotFoundError,
  DioceseNotFoundError,
  fetchChurch,
  fetchChurchEvents,
  fetchChurchIndex,
  fetchCityPage,
  fetchDioceseIndex,
  fetchDiocesePage,
} from "../api";
import { EVENT_TYPE_ORDER } from "../constants/eventTypes";

/** React Query's default; a failure that outlasts it shows the error and Retry. */
const MAX_RETRIES = 3;

/**
 * The church, city, diocese and all-churches pages' queries, shared by the pages and
 * the router's loaders (src/router.tsx), which fetch them before a page is
 * shown so it arrives whole rather than as a "Loading…" line. A page opens
 * on whatever its loader got, an error included: the loader has already made
 * every retry, so the page doesn't start over (as `retryOnMount` would, with
 * a "Loading…" line until it fails again), and shows the error and Retry, or
 * its not-found page, at once.
 */
export function cityQuery(slug: string) {
  return queryOptions({
    queryKey: ["city", slug],
    queryFn: () => fetchCityPage(slug),
    retryOnMount: false,
    retry: (failureCount, error) =>
      failureCount < MAX_RETRIES && !(error instanceof CityNotFoundError),
  });
}

export function dioceseQuery(slug: string) {
  return queryOptions({
    queryKey: ["diocese", slug],
    queryFn: () => fetchDiocesePage(slug),
    retryOnMount: false,
    retry: (failureCount, error) =>
      failureCount < MAX_RETRIES && !(error instanceof DioceseNotFoundError),
  });
}

export function dioceseIndexQuery() {
  return queryOptions({
    queryKey: ["diocese-index"],
    queryFn: fetchDioceseIndex,
    retryOnMount: false,
    retry: MAX_RETRIES,
  });
}

export function churchQuery(slug: string) {
  return queryOptions({
    queryKey: ["church", slug],
    queryFn: () => fetchChurch(slug),
    retryOnMount: false,
    retry: (failureCount, error) =>
      failureCount < MAX_RETRIES && !(error instanceof ChurchNotFoundError),
  });
}

export function churchEventsQuery(slug: string) {
  return queryOptions({
    queryKey: ["church-events", slug],
    queryFn: () => fetchChurchEvents(slug, [...EVENT_TYPE_ORDER]),
    retryOnMount: false,
    retry: (failureCount, error) =>
      failureCount < MAX_RETRIES && !(error instanceof ChurchNotFoundError),
  });
}

export function churchIndexQuery() {
  return queryOptions({
    queryKey: ["church-index"],
    queryFn: fetchChurchIndex,
    retryOnMount: false,
    retry: MAX_RETRIES,
  });
}

/** Fetches what the all-churches index shows. Never throws: the page shows any error. */
export async function prefetchChurchIndex(queryClient: QueryClient): Promise<void> {
  await queryClient.prefetchQuery(churchIndexQuery());
}

/** Fetches what the list of dioceses shows. Never throws: the page shows any error. */
export async function prefetchDioceseIndex(queryClient: QueryClient): Promise<void> {
  await queryClient.prefetchQuery(dioceseIndexQuery());
}

/** Fetches what a diocese page shows. Never throws: the page shows any error. */
export async function prefetchDiocesePage(
  queryClient: QueryClient,
  slug: string,
): Promise<void> {
  await queryClient.prefetchQuery(dioceseQuery(slug));
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
