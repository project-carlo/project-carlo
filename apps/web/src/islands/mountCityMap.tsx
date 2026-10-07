import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import CityMapLive from "../components/CityMapLive";
import type { CityMapConfig } from "../lib/cityMap";
import { DocumentLinksContext } from "../lib/documentLinks";

/**
 * Mounts the live map into a prerendered city page's preview. The page has no
 * router, so links load their page (DocumentLinksContext); the memory router
 * is only there for the router links to render.
 */
export function mountCityMap(slot: HTMLElement, config: CityMapConfig): void {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { staleTime: 60_000, retry: 2 } },
  });
  createRoot(slot).render(
    <StrictMode>
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <DocumentLinksContext.Provider value={true}>
            <CityMapLive config={config} />
          </DocumentLinksContext.Provider>
        </MemoryRouter>
      </QueryClientProvider>
    </StrictMode>,
  );
}
