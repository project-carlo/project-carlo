import { MemoryRouter } from "react-router-dom";
import type { ChurchDetail, EventSummary } from "../types";
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
  events: EventSummary[];
  cssPath: string;
  fontPaths: string[];
  canonicalUrl: string;
  /** ISO date (YYYY-MM-DD) the parish's data was last updated, if known. */
  lastModified: string | null;
}

export function StaticChurchPage({
  church,
  events,
  cssPath,
  fontPaths,
  canonicalUrl,
  lastModified,
}: StaticChurchPageProps) {
  const jsonLd = [
    churchJsonLd(church, canonicalUrl),
    churchWebPageJsonLd(church, canonicalUrl, lastModified),
    churchBreadcrumbJsonLd(church, canonicalUrl),
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
          <ChurchPageContent church={church} events={events} />
        </MemoryRouter>
      </body>
    </html>
  );
}
