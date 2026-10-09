import { MemoryRouter } from "react-router-dom";
import {
  DioceseIndexContent,
  type DioceseIndexEntry,
} from "../components/DioceseIndexContent";
import {
  DIOCESE_INDEX_TITLE,
  buildDioceseIndexDescription,
  dioceseIndexJsonLd,
} from "../lib/seo";
import { StaticPageHead } from "./StaticPageHead";

interface StaticDioceseIndexPageProps {
  dioceses: DioceseIndexEntry[];
  cssPath: string;
  fontPaths: string[];
  canonicalUrl: string;
}

/** The list of dioceses; it needs no script of its own. */
export function StaticDioceseIndexPage({
  dioceses,
  cssPath,
  fontPaths,
  canonicalUrl,
}: StaticDioceseIndexPageProps) {
  return (
    <html lang="en">
      <StaticPageHead
        title={DIOCESE_INDEX_TITLE}
        description={buildDioceseIndexDescription(dioceses)}
        canonicalUrl={canonicalUrl}
        jsonLd={dioceseIndexJsonLd(dioceses, canonicalUrl)}
        cssPath={cssPath}
        fontPaths={fontPaths}
      />
      <body className="bg-paper">
        <MemoryRouter>
          <DioceseIndexContent dioceses={dioceses} />
        </MemoryRouter>
      </body>
    </html>
  );
}
