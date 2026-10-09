import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ChurchNotFoundError } from "../api";
import { InlineQueryError } from "@/components/InlineQueryError";
import { SiteHeader } from "@/components/SiteHeader";
import { ChurchPageContent } from "@/components/ChurchPageContent";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import {
  churchEventsQuery as churchEventsQueryOptions,
  churchQuery as churchQueryOptions,
} from "@/lib/pageQueries";
import {
  buildChurchDescription,
  buildChurchTitle,
  canonicalForPath,
  churchPath,
} from "@/lib/seo";
import { liveMap } from "./liveMap";
import { NotFoundPage } from "./NotFoundPage";

export function ChurchPage() {
  const { churchSlug } = useParams();
  const enabled = typeof churchSlug === "string" && churchSlug.length > 0;

  const churchQuery = useQuery({
    ...churchQueryOptions(churchSlug ?? ""),
    enabled,
  });
  const eventsQuery = useQuery({
    ...churchEventsQueryOptions(churchSlug ?? ""),
    enabled,
  });

  const events = eventsQuery.data;
  const church = churchQuery.data?.church;

  const notFound =
    !enabled ||
    churchQuery.error instanceof ChurchNotFoundError ||
    eventsQuery.error instanceof ChurchNotFoundError;

  useDocumentMeta({
    title: notFound
      ? "Church not found · Project Carlo"
      : church
        ? buildChurchTitle(church)
        : "Church · Project Carlo",
    description: !notFound && church ? buildChurchDescription(church) : undefined,
    canonicalUrl:
      !notFound && church && churchSlug
        ? canonicalForPath(churchPath(churchSlug))
        : undefined,
    noindex: notFound,
  });

  if (!enabled) {
    return (
      <NotFoundPage
        title="Church not found"
        message="That link may be out of date, or the church may have closed or merged with another."
      />
    );
  }

  if (
    churchQuery.error instanceof ChurchNotFoundError ||
    eventsQuery.error instanceof ChurchNotFoundError
  ) {
    return (
      <NotFoundPage
        title="Church not found"
        message="That link may be out of date, or the church may have closed or merged with another."
      />
    );
  }

  if (church && events) {
    return (
      <ChurchPageContent
        church={church}
        city={churchQuery.data?.city ?? null}
        diocese={churchQuery.data?.diocese ?? null}
        map={churchQuery.data?.map ?? null}
        events={events}
        liveMap={liveMap}
      />
    );
  }

  return (
    <main className="min-h-svh bg-paper">
      <SiteHeader />

      <div className="mx-auto w-full max-w-5xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
        {churchQuery.isLoading ? (
          <p className="font-serif text-sm text-ink-soft">Loading church…</p>
        ) : null}
        {churchQuery.error ? (
          <InlineQueryError
            message="We couldn’t load this church."
            onRetry={() => churchQuery.refetch()}
          />
        ) : null}
        {eventsQuery.isLoading && !churchQuery.isLoading ? (
          <p className="mx-auto max-w-2xl font-serif text-sm text-ink-soft">
            Loading times…
          </p>
        ) : null}
        {eventsQuery.error ? (
          <InlineQueryError
            className="mx-auto max-w-2xl"
            message="We couldn’t load times for this church."
            onRetry={() => eventsQuery.refetch()}
          />
        ) : null}
      </div>
    </main>
  );
}
