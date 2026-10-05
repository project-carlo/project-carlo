import { MemoryRouter } from "react-router-dom";
import type { ChurchDetail, EventSummary } from "../types";
import { ChurchPageContent } from "../components/ChurchPageContent";
import { churchCrumbs, type ChurchPlaceContext } from "../lib/browse";
import {
  buildChurchDescription,
  buildChurchTitle,
  churchBreadcrumbJsonLd,
  churchJsonLd,
  churchWebPageJsonLd,
} from "../lib/seo";
import { StaticHead } from "./StaticHead";

interface StaticChurchPageProps {
  church: ChurchDetail;
  events: EventSummary[];
  cssPath: string;
  fontPaths: string[];
  canonicalUrl: string;
  /** ISO date (YYYY-MM-DD) the parish's data was last updated, if known. */
  lastModified: string | null;
  /** Whether the About page exists (build-time flag). */
  showAbout?: boolean;
  /** City-page link and nearby churches (see `buildChurchPlaceContext`). */
  place?: ChurchPlaceContext | null;
}

export function StaticChurchPage({
  church,
  events,
  cssPath,
  fontPaths,
  canonicalUrl,
  lastModified,
  showAbout = false,
  place = null,
}: StaticChurchPageProps) {
  const jsonLd = [
    churchJsonLd(church, canonicalUrl),
    churchWebPageJsonLd(church, canonicalUrl, lastModified),
    churchBreadcrumbJsonLd(church, canonicalUrl, churchCrumbs(church, place)),
  ];

  return (
    <html lang="en">
      <StaticHead
        title={buildChurchTitle(church)}
        description={buildChurchDescription(church)}
        canonicalUrl={canonicalUrl}
        jsonLd={jsonLd}
        cssPath={cssPath}
        fontPaths={fontPaths}
      />
      <body>
        <MemoryRouter>
          <ChurchPageContent
            church={church}
            events={events}
            showAbout={showAbout}
            place={place}
          />
        </MemoryRouter>
      </body>
    </html>
  );
}
