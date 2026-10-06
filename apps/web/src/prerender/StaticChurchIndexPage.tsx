import type { ChurchBase } from "../types";
import { cityPath, citySlugFor } from "../lib/cities";
import {
  CHURCH_INDEX_TITLE,
  SITE_NAME,
  absoluteUrl,
  buildChurchIndexDescription,
} from "../lib/seo";
import { StaticPageHead } from "./StaticPageHead";

/** What the all-parishes index lists for each church. */
type ChurchIndexEntry = Pick<ChurchBase, "slug" | "name" | "city" | "state">;

interface StaticChurchIndexPageProps {
  churches: ChurchIndexEntry[];
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

/** Group churches by "City, ST" (alphabetical), with unknown locations last. */
function groupByCity(churches: ChurchIndexEntry[]): CityGroup[] {
  const groups = new Map<string, ChurchIndexEntry[]>();
  const slugs = new Map<string, string | null>();
  for (const church of churches) {
    const city = church.city?.trim();
    const label = city
      ? church.state?.trim()
        ? `${city}, ${church.state.trim()}`
        : city
      : UNKNOWN_CITY;
    const group = groups.get(label);
    if (group) group.push(church);
    else groups.set(label, [church]);
    if (!slugs.has(label)) slugs.set(label, city ? citySlugFor(church) : null);
  }
  return [...groups.entries()]
    .sort(([a], [b]) =>
      a === UNKNOWN_CITY ? 1 : b === UNKNOWN_CITY ? -1 : a.localeCompare(b),
    )
    .map(([label, entries]) => ({
      label,
      slug: slugs.get(label) ?? null,
      churches: entries.sort((a, b) => (a.name ?? "").localeCompare(b.name ?? "")),
    }));
}

export function StaticChurchIndexPage({
  churches,
  cssPath,
  fontPaths,
  canonicalUrl,
  lastModified,
}: StaticChurchIndexPageProps) {
  const title = CHURCH_INDEX_TITLE;
  const description = buildChurchIndexDescription(churches.length);
  const origin = new URL(canonicalUrl).origin;
  const groups = groupByCity(churches);

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
                        href={`/churches/${encodeURIComponent(church.slug)}/`}
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
