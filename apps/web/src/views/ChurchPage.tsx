import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ChurchNotFoundError, fetchChurch, fetchChurchEvents } from "../api";
import { EVENT_TYPE_ORDER } from "../constants/eventTypes";
import { InlineQueryError } from "@/components/InlineQueryError";
import { SiteHeader } from "@/components/SiteHeader";
import { ChurchPageContent } from "@/components/ChurchPageContent";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import {
  buildChurchDescription,
  buildChurchTitle,
  canonicalForPath,
  churchPath,
} from "@/lib/seo";
import { NotFoundPage } from "./NotFoundPage";

/** React Query's default; a failure that outlasts it shows the error and Retry. */
const MAX_RETRIES = 3;

export function ChurchPage() {
  const { churchSlug } = useParams();
  const enabled = typeof churchSlug === "string" && churchSlug.length > 0;

  const churchQuery = useQuery({
    queryKey: ["church", churchSlug],
    queryFn: () => fetchChurch(churchSlug!),
    enabled,
    retry: (failureCount, error) =>
      failureCount < MAX_RETRIES && !(error instanceof ChurchNotFoundError),
  });
  const eventsQuery = useQuery({
    queryKey: ["church-events", churchSlug],
    queryFn: () => fetchChurchEvents(churchSlug!, [...EVENT_TYPE_ORDER]),
    enabled,
    retry: (failureCount, error) =>
      failureCount < MAX_RETRIES && !(error instanceof ChurchNotFoundError),
  });

  const events = eventsQuery.data;
  const church = churchQuery.data?.church;

  const notFound =
    !enabled ||
    churchQuery.error instanceof ChurchNotFoundError ||
    eventsQuery.error instanceof ChurchNotFoundError;

  useDocumentMeta({
    title: notFound
      ? "Parish not found · Project Carlo"
      : church
        ? buildChurchTitle(church)
        : "Parish · Project Carlo",
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
        title="Parish not found"
        message="We couldn't find that parish."
      />
    );
  }

  if (
    churchQuery.error instanceof ChurchNotFoundError ||
    eventsQuery.error instanceof ChurchNotFoundError
  ) {
    return (
      <NotFoundPage
        title="Parish not found"
        message="We couldn't find that parish."
      />
    );
  }

  if (church && events) {
    return (
      <ChurchPageContent
        church={church}
        city={churchQuery.data?.city ?? null}
        events={events}
      />
    );
  }

  return (
    <main className="min-h-svh bg-paper">
      <SiteHeader />

      <div className="mx-auto w-full max-w-5xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
        {churchQuery.isLoading ? (
          <p className="font-serif text-sm text-ink-soft">Loading parish…</p>
        ) : null}
        {churchQuery.error ? (
          <InlineQueryError
            message={"We couldn't load this parish."}
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
            message={"We couldn't load times for this parish."}
            onRetry={() => eventsQuery.refetch()}
          />
        ) : null}
      </div>
    </main>
  );
}
