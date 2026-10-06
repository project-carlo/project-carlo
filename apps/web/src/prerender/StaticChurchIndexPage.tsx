import type { ChurchBase } from "../types";
import { cityPath, citySlugFor, type City } from "../lib/cities";
import {
  CHURCH_INDEX_TITLE,
  SITE_NAME,
  absoluteUrl,
  buildChurchIndexDescription,
  churchPath,
} from "../lib/seo";
import { StaticPageHead } from "./StaticPageHead";

/** What the all-parishes index lists for each church. */
type ChurchIndexEntry = Pick<ChurchBase, "slug" | "name" | "city" | "state">;

interface StaticChurchIndexPageProps {
  churches: ChurchIndexEntry[];
  /** The city pages, as `cityIndex` builds them, so headings match their titles. */
  cities: Pick<City, "slug" | "label" | "churches">[];
  cssPath: string;
  fontPaths: string[];
  canonicalUrl: string;
  /** ISO date (YYYY-MM-DD) — latest parish bulletin date site-wide. */
  lastModified: string;
}

interface CityGroup {
  label: string;
  /** Slug of the city's page; null for the "Other locations" group. */
  slug: string | null;
  churches: ChurchIndexEntry[];
}

const UNKNOWN_CITY = "Other locations";

/**
 * One group per city page, under that page's label (alphabetical), then the
 * churches whose address has no city.
 */
function groupByCity(
  churches: ChurchIndexEntry[],
  cities: StaticChurchIndexPageProps["cities"],
): CityGroup[] {
  const groups: CityGroup[] = cities.map((city) => ({
    label: city.label,
    slug: city.slug,
    churches: city.churches,
  }));
  const unknown = churches
    .filter((church) => citySlugFor(church) === null)
    .sort((a, b) => (a.name ?? "").localeCompare(b.name ?? ""));
  if (unknown.length > 0) {
    groups.push({ label: UNKNOWN_CITY, slug: null, churches: unknown });
  }
  return groups;
}

export function StaticChurchIndexPage({
  churches,
  cities,
  cssPath,
  fontPaths,
  canonicalUrl,
  lastModified,
}: StaticChurchIndexPageProps) {
  const title = CHURCH_INDEX_TITLE;
  const description = buildChurchIndexDescription(churches.length);
  const origin = new URL(canonicalUrl).origin;
  const groups = groupByCity(churches, cities);

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
          name: "Parishes",
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
        <main className="mx-auto w-full max-w-3xl px-6 py-12 pb-[calc(3rem+var(--safe-area-inset-bottom))]">
          <header className="text-center">
            <a href="/" className="rubric-link font-serif text-[0.9375rem]">
              Back to map
            </a>
            <h1 className="mt-6 font-display text-[clamp(2rem,5vw,3rem)] leading-[1.05] font-normal tracking-tight text-ink">
              All parishes
            </h1>
            <p className="mt-4 font-serif text-[0.95rem] text-ink-soft">
              Mass, Confession &amp; Adoration times at {churches.length} Catholic
              parishes, parsed from each parish&rsquo;s weekly bulletin.
            </p>
          </header>

          <div className="mt-12 space-y-10">
            {groups.map((group) => (
              <section key={group.label}>
                <h2 className="smallcaps border-b border-rule-strong pb-2 text-[0.95rem] text-ink">
                  {group.slug ? (
                    <a href={cityPath(group.slug)} className="rubric-link">
                      {group.label}
                    </a>
                  ) : (
                    group.label
                  )}
                </h2>
                <ul className="mt-4 space-y-2">
                  {group.churches.map((church) => (
                    <li key={church.slug}>
                      <a
                        href={churchPath(church.slug)}
                        className="rubric-link font-serif text-[1.05rem] text-ink"
                      >
                        {church.name ?? "Unnamed parish"}
                      </a>
                    </li>
                  ))}
                </ul>
              </section>
            ))}
          </div>
        </main>
      </body>
    </html>
  );
}
