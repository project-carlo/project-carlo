import { MemoryRouter } from "react-router-dom";
import {
  ChurchIndexContent,
  type ChurchIndexCity,
  type ChurchIndexEntry,
} from "../components/ChurchIndexContent";
import {
  CHURCH_INDEX_TITLE,
  SITE_NAME,
  absoluteUrl,
  buildChurchIndexDescription,
} from "../lib/seo";
import { ALL_CHURCHES } from "../copy";
import { StaticPageHead } from "./StaticPageHead";

interface StaticChurchIndexPageProps {
  churches: ChurchIndexEntry[];
  cities: ChurchIndexCity[];
  cssPath: string;
  fontPaths: string[];
  /** Wires up the search box; the only script the page loads. */
  churchIndexScript: string;
  canonicalUrl: string;
  /** ISO date (YYYY-MM-DD) — latest parish bulletin date site-wide. */
  lastModified: string;
}

export function StaticChurchIndexPage({
  churches,
  cities,
  cssPath,
  fontPaths,
  churchIndexScript,
  canonicalUrl,
  lastModified,
}: StaticChurchIndexPageProps) {
  const title = CHURCH_INDEX_TITLE;
  const description = buildChurchIndexDescription(churches.length);
  const origin = new URL(canonicalUrl).origin;

  const jsonLd = [
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "@id": `${canonicalUrl}#webpage`,
      url: canonicalUrl,
      name: title,
      description,
      dateModified: lastModified,
      inLanguage: "en-US",
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: [
        {
          "@type": "ListItem",
          position: 1,
          name: SITE_NAME,
          item: absoluteUrl(origin, "/"),
        },
        {
          "@type": "ListItem",
          position: 2,
          name: ALL_CHURCHES,
          item: canonicalUrl,
        },
      ],
    },
  ];

  return (
    <html lang="en">
      <StaticPageHead
        title={title}
        description={description}
        canonicalUrl={canonicalUrl}
        jsonLd={jsonLd}
        cssPath={cssPath}
        fontPaths={fontPaths}
      />
      <body className="bg-paper">
        <MemoryRouter>
          <ChurchIndexContent churches={churches} cities={cities} />
        </MemoryRouter>
        <script type="module" src={churchIndexScript} />
      </body>
    </html>
  );
}
