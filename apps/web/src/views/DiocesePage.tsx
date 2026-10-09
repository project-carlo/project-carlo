import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { DioceseNotFoundError } from "../api";
import { DiocesePageContent } from "@/components/DiocesePageContent";
import { InlineQueryError } from "@/components/InlineQueryError";
import { SiteHeader } from "@/components/SiteHeader";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { diocesePath } from "@/lib/dioceses";
import { dioceseQuery as dioceseQueryOptions } from "@/lib/pageQueries";
import {
  buildDioceseDescription,
  buildDioceseTitle,
  canonicalForPath,
} from "@/lib/seo";
import { liveMap } from "./liveMap";
import { NotFoundPage } from "./NotFoundPage";

export function DiocesePage() {
  const { dioceseSlug } = useParams();
  const enabled = typeof dioceseSlug === "string" && dioceseSlug.length > 0;

  const dioceseQuery = useQuery({
    ...dioceseQueryOptions(dioceseSlug ?? ""),
    enabled,
  });

  const data = dioceseQuery.data;
  const notFound = !enabled || dioceseQuery.error instanceof DioceseNotFoundError;

  useDocumentMeta({
    title: notFound
      ? "Diocese not found · Project Carlo"
      : data
        ? buildDioceseTitle(data.diocese)
        : "Mass Times · Project Carlo",
    description: !notFound && data ? buildDioceseDescription(data.diocese) : undefined,
    canonicalUrl:
      !notFound && data ? canonicalForPath(diocesePath(data.diocese.slug)) : undefined,
    noindex: notFound,
  });

  if (notFound) {
    return (
      <NotFoundPage
        title="Diocese not found"
        message="We don’t have a page for that diocese."
      />
    );
  }

  if (data) return <DiocesePageContent data={data} liveMap={liveMap} />;

  return (
    <main className="min-h-svh bg-paper">
      <SiteHeader />
      <div className="mx-auto w-full max-w-5xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
        {dioceseQuery.isLoading ? (
          <p className="font-serif text-sm text-ink-soft">Loading the diocese…</p>
        ) : null}
        {dioceseQuery.error ? (
          <InlineQueryError
            message="We couldn’t load this diocese."
            onRetry={() => dioceseQuery.refetch()}
          />
        ) : null}
      </div>
    </main>
  );
}
