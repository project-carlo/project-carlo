import { MemoryRouter } from "react-router-dom";
import type { ChurchDetail, EventSummary } from "../types";
import type { CityLink } from "../lib/cities";
import type { CityMapData } from "../lib/cityMapLayout";
import { ChurchPageContent } from "../components/ChurchPageContent";
import {
  buildChurchDescription,
  buildChurchTitle,
  churchBreadcrumbJsonLd,
  churchJsonLd,
  churchWebPageJsonLd,
} from "../lib/seo";
import { StaticPageHead } from "./StaticPageHead";

interface StaticChurchPageProps {
  church: ChurchDetail;
  city: CityLink | null;
  map: CityMapData | null;
  events: EventSummary[];
  cssPath: string;
  fontPaths: string[];
  /** Makes the map preview live; the only script the page loads, when it has a map. */
  cityMapScript: string;
  canonicalUrl: string;
  /** ISO date (YYYY-MM-DD) the church's data was last updated, if known. */
  lastModified: string | null;
}

export function StaticChurchPage({
  church,
  city,
  map,
  events,
  cssPath,
  fontPaths,
  cityMapScript,
  canonicalUrl,
  lastModified,
}: StaticChurchPageProps) {
  const jsonLd = [
    churchJsonLd(church, canonicalUrl),
    churchWebPageJsonLd(church, canonicalUrl, lastModified),
    churchBreadcrumbJsonLd(church, city, canonicalUrl),
  ];

  return (
    <html lang="en">
      <StaticPageHead
        title={buildChurchTitle(church)}
        description={buildChurchDescription(church)}
        canonicalUrl={canonicalUrl}
        jsonLd={jsonLd}
        cssPath={cssPath}
        fontPaths={fontPaths}
      />
      <body>
        <MemoryRouter>
          <ChurchPageContent church={church} city={city} map={map} events={events} />
        </MemoryRouter>
        {map ? <script type="module" src={cityMapScript} /> : null}
      </body>
    </html>
  );
}
