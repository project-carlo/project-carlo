import { useLayoutEffect, useRef } from "react";
import { useQuery } from "@tanstack/react-query";
import { ChurchIndexContent } from "@/components/ChurchIndexContent";
import { InlineQueryError } from "@/components/InlineQueryError";
import { SiteHeader } from "@/components/SiteHeader";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { attachChurchIndexSearch } from "@/lib/churchIndexSearch";
import { churchIndexQuery } from "@/lib/pageQueries";
import {
  CHURCH_INDEX_PATH,
  CHURCH_INDEX_TITLE,
  buildChurchIndexDescription,
  canonicalForPath,
} from "@/lib/seo";

/**
 * The all-churches index in the app, reached from its other pages; a visit
 * that starts here gets the prerendered copy (StaticChurchIndexPage). Being
 * in the app, its Map link goes back to the map as it was left, at once.
 */
export function ChurchIndexPage() {
  const { data, error, isLoading, refetch } = useQuery(churchIndexQuery());

  useDocumentMeta({
    title: CHURCH_INDEX_TITLE,
    description: data ? buildChurchIndexDescription(data.churches.length) : undefined,
    canonicalUrl: canonicalForPath(CHURCH_INDEX_PATH),
  });

  // The search box works on the rendered list, as on the prerendered page.
  // It's revealed before the page is painted, and before back or forward
  // scrolls to where the list was left, so nothing under it moves after.
  const rootRef = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    if (!data || !rootRef.current) return;
    return attachChurchIndexSearch(rootRef.current);
  }, [data]);

  if (data) {
    return (
      <div ref={rootRef}>
        <ChurchIndexContent churches={data.churches} cities={data.cities} />
      </div>
    );
  }

  return (
    <main className="min-h-svh bg-paper">
      <SiteHeader />
      <div className="mx-auto w-full max-w-3xl px-6 py-10 md:py-14">
        {isLoading ? (
          <p className="font-serif text-sm text-ink-soft">Loading churches…</p>
        ) : null}
        {error ? (
          <InlineQueryError
            message="We couldn’t load the list of churches."
            onRetry={() => refetch()}
          />
        ) : null}
      </div>
    </main>
  );
}
