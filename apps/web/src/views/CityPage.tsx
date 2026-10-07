import { lazy, Suspense } from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { CityNotFoundError, fetchCityPage } from "../api";
import { CityPageContent } from "@/components/CityPageContent";
import { InlineQueryError } from "@/components/InlineQueryError";
import { SiteHeader } from "@/components/SiteHeader";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { cityPath } from "@/lib/cities";
import type { CityMapConfig } from "@/lib/cityMap";
import {
  buildCityDescription,
  buildCityTitle,
  canonicalForPath,
} from "@/lib/seo";
import { NotFoundPage } from "./NotFoundPage";

const CityMapLive = lazy(() => import("@/components/CityMapLive"));

function liveMap(config: CityMapConfig) {
  return (
    <Suspense fallback={null}>
      <CityMapLive config={config} />
    </Suspense>
  );
}

/** React Query's default; a failure that outlasts it shows the error and Retry. */
const MAX_RETRIES = 3;

export function CityPage() {
  const { citySlug } = useParams();
  const enabled = typeof citySlug === "string" && citySlug.length > 0;

  const cityQuery = useQuery({
    queryKey: ["city", citySlug],
    queryFn: () => fetchCityPage(citySlug!),
    enabled,
    retry: (failureCount, error) =>
      failureCount < MAX_RETRIES && !(error instanceof CityNotFoundError),
  });

  const data = cityQuery.data;
  const notFound = !enabled || cityQuery.error instanceof CityNotFoundError;

  useDocumentMeta({
    title: notFound
      ? "City not found · Project Carlo"
      : data
        ? buildCityTitle(data.city)
        : "Mass Times · Project Carlo",
    description: !notFound && data ? buildCityDescription(data.city) : undefined,
    canonicalUrl:
      !notFound && data ? canonicalForPath(cityPath(data.city.slug)) : undefined,
    noindex: notFound,
  });

  if (notFound) {
    return (
      <NotFoundPage
        title="City not found"
        message="We don’t list any churches in that city yet."
      />
    );
  }

  if (data) return <CityPageContent data={data} liveMap={liveMap} />;

  return (
    <main className="min-h-svh bg-paper">
      <SiteHeader />
      <div className="mx-auto w-full max-w-5xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
        {cityQuery.isLoading ? (
          <p className="font-serif text-sm text-ink-soft">Loading churches…</p>
        ) : null}
        {cityQuery.error ? (
          <InlineQueryError
            message="We couldn’t load the churches in this city."
            onRetry={() => cityQuery.refetch()}
          />
        ) : null}
      </div>
    </main>
  );
}
