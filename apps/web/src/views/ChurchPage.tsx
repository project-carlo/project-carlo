import { useMemo } from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { ChurchNotFoundError, fetchChurch, fetchChurchEvents } from "../api";
import { EVENT_TYPE_ORDER } from "../constants/eventTypes";
import { InlineQueryError } from "@/components/InlineQueryError";
import { SiteHeader } from "@/components/SiteHeader";
import { ChurchPageContent } from "@/components/ChurchPageContent";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { useMapHref } from "@/hooks/useMapHref";
import { usePlaceIndex } from "@/hooks/usePlaceIndex";
import { buildChurchPlaceContext } from "@/lib/browse";
import { isAboutPageEnabled } from "@/lib/featureFlags";
import {
  buildChurchDescription,
  buildChurchTitle,
  canonicalForPath,
} from "@/lib/seo";
import { NotFoundPage } from "./NotFoundPage";

export function ChurchPage() {
  const { churchSlug } = useParams();
  const mapHref = useMapHref();
  const showAbout = isAboutPageEnabled();
  const enabled = typeof churchSlug === "string" && churchSlug.length > 0;

  const churchQuery = useQuery({
    queryKey: ["church", churchSlug],
    queryFn: () => fetchChurch(churchSlug!),
    enabled,
    retry: (_failureCount, error) =>
      !(error instanceof ChurchNotFoundError),
  });
  const eventsQuery = useQuery({
    queryKey: ["church-events", churchSlug],
    queryFn: () => fetchChurchEvents(churchSlug!, [...EVENT_TYPE_ORDER]),
    enabled,
    retry: (_failureCount, error) =>
      !(error instanceof ChurchNotFoundError),
  });

  const events = eventsQuery.data;
  const church = churchQuery.data;

  // The city-page link and "Nearby churches" come from the whole snapshot. It
  // is the data the two queries above already read, so this settles at once;
  // if it ever fails the page simply renders without those extras.
  const placeQuery = usePlaceIndex();
  const place = useMemo(
    () =>
      church && placeQuery.data
        ? buildChurchPlaceContext(placeQuery.data, church)
        : null,
    [church, placeQuery.data],
  );
  const placeSettled = placeQuery.isSuccess || placeQuery.isError;

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
        ? canonicalForPath(`/churches/${encodeURIComponent(churchSlug)}/`)
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

  if (church && events && placeSettled) {
    return (
      <ChurchPageContent
        church={church}
        events={events}
        showAbout={showAbout}
        place={place}
      />
    );
  }

  return (
    <main className="min-h-svh bg-paper">
      <SiteHeader sticky mapHref={mapHref} showAbout={showAbout} />

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
        {church && events && !placeSettled ? (
          <p className="font-serif text-sm text-ink-soft">Loading parish…</p>
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
