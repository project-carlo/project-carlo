import { MemoryRouter } from "react-router-dom";
import type { DiocesePageData } from "../api";
import { DiocesePageContent } from "../components/DiocesePageContent";
import { buildDioceseDescription, buildDioceseTitle, dioceseJsonLd } from "../lib/seo";
import { StaticPageHead } from "./StaticPageHead";

interface StaticDiocesePageProps {
  data: DiocesePageData;
  cssPath: string;
  fontPaths: string[];
  /** Makes the map preview live; the only script the page loads. */
  cityMapScript: string;
  canonicalUrl: string;
}

export function StaticDiocesePage({
  data,
  cssPath,
  fontPaths,
  cityMapScript,
  canonicalUrl,
}: StaticDiocesePageProps) {
  return (
    <html lang="en">
      <StaticPageHead
        title={buildDioceseTitle(data.diocese)}
        description={buildDioceseDescription(data.diocese)}
        canonicalUrl={canonicalUrl}
        jsonLd={dioceseJsonLd(data.diocese, canonicalUrl)}
        cssPath={cssPath}
        fontPaths={fontPaths}
      />
      <body>
        <MemoryRouter>
          <DiocesePageContent data={data} />
        </MemoryRouter>
        {data.map ? <script type="module" src={cityMapScript} /> : null}
      </body>
    </html>
  );
}
