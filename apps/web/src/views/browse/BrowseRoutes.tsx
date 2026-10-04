/**
 * Client routes for the browse pages. They render the same components the
 * prerenderer writes to static HTML, from the snapshot the map already loads,
 * so in-app navigation to a diocese or city page needs no page reload.
 */
import type { ReactNode } from "react";
import { useParams } from "react-router-dom";
import { InlineQueryError } from "@/components/InlineQueryError";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { useMapHref } from "@/hooks/useMapHref";
import { usePlaceIndex } from "@/hooks/usePlaceIndex";
import {
  buildCityModel,
  buildDioceseIndex,
  buildDioceseModel,
  buildStateModel,
  type PageSeo,
  type PlaceIndex,
} from "@/lib/browse";
import { isAboutPageEnabled } from "@/lib/featureFlags";
import { canonicalForPath } from "@/lib/seo";
import { NotFoundPage } from "../NotFoundPage";
import { BrowseShell } from "./parts";
import {
  CityView,
  DioceseIndexView,
  DioceseView,
  StateView,
} from "./pages";

const LOADING_TITLE = "Loading · Project Carlo";

/** Shared plumbing: load the index, set the document head, 404 an unknown page. */
function useBrowseRoute<T extends PageSeo>(build: (index: PlaceIndex) => T | null) {
  const query = usePlaceIndex();
  const mapHref = useMapHref();
  const showAbout = isAboutPageEnabled();
  const model = query.data ? build(query.data) : null;
  const notFound = Boolean(query.data) && model === null;

  useDocumentMeta({
    title: model ? model.title : notFound ? "Page not found · Project Carlo" : LOADING_TITLE,
    description: model?.description,
    canonicalUrl: model ? canonicalForPath(model.path) : undefined,
    noindex: !model,
  });

  let status: ReactNode = null;
  if (query.isError) {
    status = (
      <BrowseShell mapHref={mapHref} showAbout={showAbout}>
        <InlineQueryError
          className="mx-auto max-w-2xl"
          message="We couldn't load the church data."
          onRetry={() => query.refetch()}
        />
      </BrowseShell>
    );
  } else if (!query.data) {
    status = (
      <BrowseShell mapHref={mapHref} showAbout={showAbout}>
        <p className="py-16 text-center font-serif text-sm text-ink-soft">Loading…</p>
      </BrowseShell>
    );
  } else if (notFound) {
    status = <NotFoundPage />;
  }
  return { model, status, mapHref, showAbout };
}

export function DioceseIndexRoute() {
  const { model, status, mapHref, showAbout } = useBrowseRoute(buildDioceseIndex);
  if (!model) return status;
  return (
    <DioceseIndexView model={model} updated={null} mapHref={mapHref} showAbout={showAbout} />
  );
}

export function DioceseRoute() {
  const { key = "" } = useParams();
  const { model, status, mapHref, showAbout } = useBrowseRoute((index) =>
    buildDioceseModel(index, key),
  );
  if (!model) return status;
  return <DioceseView model={model} updated={null} mapHref={mapHref} showAbout={showAbout} />;
}

export function StateRoute() {
  const { state = "" } = useParams();
  const { model, status, mapHref, showAbout } = useBrowseRoute((index) =>
    buildStateModel(index, state),
  );
  if (!model) return status;
  return <StateView model={model} updated={null} mapHref={mapHref} showAbout={showAbout} />;
}

export function CityRoute() {
  const { state = "", city = "" } = useParams();
  const { model, status, mapHref, showAbout } = useBrowseRoute((index) =>
    buildCityModel(index, state, city),
  );
  if (!model) return status;
  return <CityView model={model} updated={null} mapHref={mapHref} showAbout={showAbout} />;
}
