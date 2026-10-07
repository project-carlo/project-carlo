import { MemoryRouter } from "react-router-dom";
import type { ChurchBase } from "../types";
import { cityPath, citySlugFor, type City } from "../lib/cities";
import {
  CHURCH_INDEX_TITLE,
  SITE_NAME,
  absoluteUrl,
  buildChurchIndexDescription,
  churchPath,
} from "../lib/seo";
import { ALL_CHURCHES, SOURCE_PHRASE, UNNAMED_CHURCH } from "../copy";
import { Fleuron } from "../components/Fleuron";
import { SiteHeader } from "../components/SiteHeader";
import { CHURCH_INDEX_SEARCH_SCRIPT } from "./churchIndexSearch";
import { StaticPageHead } from "./StaticPageHead";

/** What the all-churches index lists for each church. */
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
        <main className="min-h-svh bg-paper">
          {/* The church and city pages' header. The memory router is only
           *  there for its links to render; the page has no app to route. */}
          <MemoryRouter>
            <SiteHeader />
          </MemoryRouter>

          <div className="mx-auto w-full max-w-3xl px-6 py-10 pb-[calc(3rem+var(--safe-area-inset-bottom))] md:py-14">
            <section className="mx-auto max-w-2xl text-center">
              <h1 className="font-display text-[clamp(2.25rem,6vw,3.75rem)] leading-[1.05] font-normal tracking-tight text-ink">
                {ALL_CHURCHES}
              </h1>
              <p className="mt-4 font-serif text-[1rem] text-ink-soft">
                Mass, Confession, and Adoration times at {churches.length} Catholic
                churches, {SOURCE_PHRASE}.
              </p>
              <Fleuron className="mt-7" />
            </section>

            <form
              id="church-search-form"
              role="search"
              hidden
              className="mt-4"
            >
              <label htmlFor="church-search" className="sr-only">
                Search churches and cities
              </label>
              <input
                id="church-search"
                type="search"
                placeholder="Search for a church or city"
                autoComplete="off"
                spellCheck={false}
                className="w-full appearance-none border-b border-rule-strong bg-transparent py-2 font-serif text-[1.0625rem] text-ink outline-none placeholder:text-ink-soft placeholder:italic focus:border-rubric [&::-webkit-search-cancel-button]:appearance-none"
              />
              <p
                id="church-search-status"
                aria-live="polite"
                className="mt-2 min-h-[1.25rem] font-serif text-sm text-ink-soft"
              />
            </form>

            <p
              id="church-search-empty"
              hidden
              className="mt-10 text-center font-serif text-[0.95rem] text-ink-soft"
            >
              {/* The search script fills in the text, echoing the query. */}
            </p>

            <div className="mt-8 space-y-10">
              {groups.map((group) => (
                <section key={group.label} data-city-group="">
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
                          {church.name ?? UNNAMED_CHURCH}
                        </a>
                      </li>
                    ))}
                  </ul>
                </section>
              ))}
            </div>
          </div>
        </main>
        <script dangerouslySetInnerHTML={{ __html: CHURCH_INDEX_SEARCH_SCRIPT }} />
      </body>
    </html>
  );
}
