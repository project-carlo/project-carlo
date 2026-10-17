import { MemoryRouter } from "react-router-dom";
import type { CityPageData } from "../api";
import { CityPageContent } from "../components/CityPageContent";
import { buildCityDescription, buildCityTitle, cityJsonLd } from "../lib/seo";
import { StaticPageHead } from "./StaticPageHead";

interface StaticCityPageProps {
  data: CityPageData;
  cssPath: string;
  fontPaths: string[];
  /** Makes the map preview live; the only script the page loads. */
  cityMapScript: string;
  canonicalUrl: string;
}

export function StaticCityPage({
  data,
  cssPath,
  fontPaths,
  cityMapScript,
  canonicalUrl,
}: StaticCityPageProps) {
  return (
    <html lang="en">
      <StaticPageHead
        title={buildCityTitle(data.city)}
        description={buildCityDescription(data.city)}
        canonicalUrl={canonicalUrl}
        jsonLd={cityJsonLd(data.city, canonicalUrl)}
        cssPath={cssPath}
        fontPaths={fontPaths}
      />
      <body>
        <MemoryRouter>
          <CityPageContent data={data} />
        </MemoryRouter>
        <script type="module" src={cityMapScript} />
      </body>
    </html>
  );
}
