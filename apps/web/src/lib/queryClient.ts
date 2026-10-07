import { QueryClient } from "@tanstack/react-query";

/**
 * The app's query client. A prerendered city page's live map, mounted
 * without the app (src/islands/mountCityMap.tsx), makes its own, so it
 * fetches and caches as the app's maps do.
 */
export function createQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60_000,
        retry: 2,
      },
    },
  });
}
