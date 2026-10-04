import type {
  CityModel,
  DioceseIndexModel,
  DioceseModel,
  StateModel,
} from "../lib/browse";
import { browsePageJsonLd } from "../lib/seo";
import {
  CityView,
  DioceseIndexView,
  DioceseView,
  StateView,
} from "../views/browse/pages";
import { StaticHead } from "./StaticHead";

export type BrowseModel =
  | DioceseIndexModel
  | DioceseModel
  | StateModel
  | CityModel;

interface StaticBrowsePageProps {
  model: BrowseModel;
  cssPath: string;
  fontPaths: string[];
  canonicalUrl: string;
  /** ISO date (YYYY-MM-DD) the schedules were last refreshed (the build date). */
  lastModified: string;
  /** Whether the About page exists (build-time flag). */
  showAbout?: boolean;
}

/**
 * A prerendered browse page (diocese index, diocese, state hub or city): the
 * same view component the client route renders, in a full HTML document with
 * title, description, canonical, OG/Twitter and CollectionPage + ItemList +
 * BreadcrumbList JSON-LD.
 */
export function StaticBrowsePage({
  model,
  cssPath,
  fontPaths,
  canonicalUrl,
  lastModified,
  showAbout = false,
}: StaticBrowsePageProps) {
  const origin = new URL(canonicalUrl).origin;
  const jsonLd = browsePageJsonLd({
    origin,
    path: model.path,
    title: model.title,
    description: model.description,
    dateModified: lastModified,
    crumbs: model.crumbs,
    items: model.items,
  });
  const view = { updated: lastModified, showAbout };

  return (
    <html lang="en">
      <StaticHead
        title={model.title}
        description={model.description}
        canonicalUrl={canonicalUrl}
        jsonLd={jsonLd}
        cssPath={cssPath}
        fontPaths={fontPaths}
      />
      <body className="bg-paper">
        {model.kind === "city" ? (
          <CityView model={model} {...view} />
        ) : model.kind === "diocese" ? (
          <DioceseView model={model} {...view} />
        ) : model.kind === "state" ? (
          <StateView model={model} {...view} />
        ) : (
          <DioceseIndexView model={model} {...view} />
        )}
      </body>
    </html>
  );
}
