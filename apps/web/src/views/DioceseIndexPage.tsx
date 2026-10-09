import { useQuery } from "@tanstack/react-query";
import { DioceseIndexContent } from "@/components/DioceseIndexContent";
import { InlineQueryError } from "@/components/InlineQueryError";
import { SiteHeader } from "@/components/SiteHeader";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { DIOCESE_INDEX_PATH } from "@/lib/dioceses";
import { dioceseIndexQuery } from "@/lib/pageQueries";
import {
  DIOCESE_INDEX_TITLE,
  buildDioceseIndexDescription,
  canonicalForPath,
} from "@/lib/seo";

/**
 * The list of dioceses in the app; a visit that starts here gets the
 * prerendered copy (StaticDioceseIndexPage).
 */
export function DioceseIndexPage() {
  const { data, error, isLoading, refetch } = useQuery(dioceseIndexQuery());

  useDocumentMeta({
    title: DIOCESE_INDEX_TITLE,
    description: data ? buildDioceseIndexDescription(data) : undefined,
    canonicalUrl: canonicalForPath(DIOCESE_INDEX_PATH),
  });

  if (data) return <DioceseIndexContent dioceses={data} />;

  return (
    <main className="min-h-svh bg-paper">
      <SiteHeader />
      <div className="mx-auto w-full max-w-3xl px-6 py-10 md:py-14">
        {isLoading ? (
          <p className="font-serif text-sm text-ink-soft">Loading dioceses…</p>
        ) : null}
        {error ? (
          <InlineQueryError
            message="We couldn’t load the list of dioceses."
            onRetry={() => refetch()}
          />
        ) : null}
      </div>
    </main>
  );
}
